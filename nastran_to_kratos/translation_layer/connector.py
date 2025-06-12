from __future__ import annotations

from abc import ABC
from dataclasses import dataclass

from nastran_to_kratos.kratos import KratosSimulation
from nastran_to_kratos.kratos.material import KratosMaterial
from nastran_to_kratos.kratos.model import Element, SubModel
from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Crod, Mat1, Prod, Rbe2

from .material import Material


@dataclass
class Connector(ABC):
    """The base class of all connectors between two elements."""

    first_point_index: int
    second_point_index: int
    material: Material

    def to_kratos_element(self) -> Element:
        """Export this connector to a kratos element."""
        return Element(property_id=0, node_ids=[self.first_point_index, self.second_point_index])


@dataclass
class RBE2Connector:
    """Represents an RBE2 connection from Nastran as a connector.

    Attributes:
        dependent_node (int): The dependent node (GN).
        independent_nodes (list[int]): List of independent nodes (GMI).
        cm (int): Component bitmask specifying constrained DOFs.
    """

    dependent_node: int
    independent_nodes: list[int]
    cm: int

    @classmethod
    def from_nastran(cls, rbe2: Rbe2) -> RBE2Connector:
        """Creates an RBE2Connector from a Nastran RBE2 entry."""
        return cls(dependent_node=rbe2.gn, independent_nodes=rbe2.gmi, cm=rbe2.cm)

    def to_nastran(self) -> Rbe2:
        """Converts this connector back to a Nastran RBE2 entry."""
        return Rbe2(
            eid=0,  # You can set a proper EID if needed
            gn=self.dependent_node,
            gmi=self.independent_nodes,
            cm=self.cm,
        )

    def get_constrained_dofs(self) -> list[str]:
        """Returns the list of constrained DOFs based on the component bitmask (CM).
        Bitmask interpretation is 1-based (bit 1 = X, bit 2 = Y, etc).
        """  # noqa: D205
        dof_map = {
            1: "DISPLACEMENT_X",
            2: "DISPLACEMENT_Y",
            3: "DISPLACEMENT_Z",
            4: "ROTATION_X",
            5: "ROTATION_Y",
            6: "ROTATION_Z",
        }
        dofs = []
        for bit in range(1, 7):
            if self.cm & (1 << (bit - 1)):
                dofs.append(dof_map[bit])  # noqa: PERF401
        return dofs

    def to_kratos_process(self, model_part_name: str = "Structure") -> dict:
        """Converts this connector to a Kratos custom impose process (ImposeRBE2Process)."""
        constrained_dofs = self.get_constrained_dofs()
        if not constrained_dofs:
            raise ValueError("No constrained DOFs specified in CM bitmask.")

        if not self.independent_nodes:
            raise ValueError("Independent nodes list cannot be empty.")

        return {
            "python_module": "impose_rbe2_process",
            "kratos_module": "StructuralMechanicsApplication",
            "process_name": "ImposeRBE2Process",
            "Parameters": {
                "model_part_name": model_part_name,
                "dependent_node": self.dependent_node,
                "independent_nodes": self.independent_nodes,
                "constrained_dofs": self.get_constrained_dofs(),
                "interval": [0.0, "End"],
            },
        }

    @staticmethod
    def rbe2_connectors_from_nastran(bulk_data: BulkDataSection) -> list[RBE2Connector]:
        """Extracts all RBE2 entries from a BulkDataSection and converts them to RBE2Connector objects."""
        return [
            RBE2Connector.from_nastran(entry)
            for entry in bulk_data.entries
            if isinstance(entry, Rbe2)
        ]


@dataclass
class Truss(Connector):
    """A connector, which can only transfer forces along its primary axis."""

    cross_section: float

    @classmethod
    def from_nastran(cls, crod: Crod, prod: Prod, mat1: Mat1) -> Truss:
        """Construct this class from nastran."""
        if crod.pid != prod.pid:
            raise KeyError

        if prod.mid != mat1.mid:
            raise KeyError

        return Truss(
            first_point_index=crod.g1,
            second_point_index=crod.g2,
            cross_section=prod.a,
            material=Material.from_nastran(mat1),
        )

    def to_kratos_submodel(self, element_index: int) -> SubModel:
        """Export this truss to a kratos sub-model."""
        return SubModel(
            nodes=[self.first_point_index, self.second_point_index], elements=[element_index]
        )

    def to_kratos_material(self, truss_id: int) -> KratosMaterial:
        """Export this truss to a kratos material."""
        variables = {"CROSS_AREA": self.cross_section, "DENSITY": 0}

        if self.material.young_modulus is not None:
            variables["YOUNG_MODULUS"] = self.material.young_modulus

        return KratosMaterial(
            model_part_name=f"Structure.truss_{truss_id}",
            properties_id=0,
            material_name=self.material.name,
            constitutive_law="TrussConstitutiveLaw",
            variables=variables,
        )


def trusses_from_nastran(bulk_data: BulkDataSection) -> list[Connector]:
    """Construct all trusses from the nastran Crods."""
    prods_by_pid = {prod.pid: prod for prod in bulk_data.prods}
    mat1s_by_mid = {mat1.mid: mat1 for mat1 in bulk_data.mat1s}
    return [
        Truss.from_nastran(crod, prods_by_pid[crod.pid], mat1s_by_mid[prods_by_pid[crod.pid].mid])
        for crod in bulk_data.crods
    ]


def connectors_from_nastran(bulk: BulkDataSection) -> list[RBE2Connector]:
    """Extracts all RBE2 connectors from the bulk data section."""
    rbe2s = [entry for entry in bulk.entries if isinstance(entry, Rbe2)]
    return [RBE2Connector.from_nastran(rbe2) for rbe2 in rbe2s]


def trusses_from_kratos(kratos: KratosSimulation) -> list[Connector]:
    """Construct all trusses from a kratos simulation."""
    if kratos.model is None or kratos.materials is None:
        return []
    if "TrussLinearElement3D2N" not in kratos.model.elements:
        return []

    connectors: list[Connector] = []
    for truss_id, truss in kratos.model.elements["TrussLinearElement3D2N"].items():
        truss_material = None
        for material in kratos.materials:
            if int(material.model_part_name.split("_")[-1]) == truss_id:
                truss_material = material
                break

        if truss_material is None:
            raise KeyError

        connectors.append(
            Truss(
                first_point_index=truss.node_ids[0],
                second_point_index=truss.node_ids[1],
                cross_section=truss_material.variables["CROSS_AREA"],
                material=Material.from_kratos(truss_material),
            )
        )

    return connectors
