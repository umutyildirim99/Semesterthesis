from __future__ import annotations

from abc import ABC
from dataclasses import dataclass

from nastran_to_kratos.kratos import KratosSimulation
from nastran_to_kratos.kratos.material import KratosMaterial
from nastran_to_kratos.kratos.model import Element, SubModel
from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Crod, Mat1, Prod

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
