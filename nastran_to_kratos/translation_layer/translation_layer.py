from __future__ import annotations

from dataclasses import dataclass, field

from nastran_to_kratos.kratos.kratos_simulation import KratosSimulation, SimulationParameters
from nastran_to_kratos.kratos.material import KratosMaterial
from nastran_to_kratos.kratos.model import Condition, Element, Model, SubModel
from nastran_to_kratos.nastran import BulkDataSection, NastranSimulation
from nastran_to_kratos.nastran.bulk_data.entries import Crod, Force, Grid, Mat1, _BulkDataEntry

from .connector import Connector, Truss, trusses_from_kratos, trusses_from_nastran
from .constraint import Constraint, constraints_from_kratos, constraints_from_nastran
from .load import Load, loads_from_kratos, loads_from_nastran
from .point import Point, nodes_from_kratos, nodes_from_nastran


@dataclass
class TranslationLayer:
    """A representation of a simulation used as a translation between nastran and kratos."""

    nodes: list[Point] = field(default_factory=list)
    connectors: list[Connector] = field(default_factory=list)
    constraints: list[Constraint] = field(default_factory=list)
    loads: list[Load] = field(default_factory=list)

    @classmethod
    def from_nastran(cls, nastran: NastranSimulation) -> TranslationLayer:
        """Construct this class from nastran."""
        return TranslationLayer(
            nodes=nodes_from_nastran(nastran.bulk_data),
            connectors=trusses_from_nastran(nastran.bulk_data),
            constraints=constraints_from_nastran(nastran.bulk_data),
            loads=loads_from_nastran(nastran.bulk_data),
        )

    @classmethod
    def from_kratos(cls, kratos: KratosSimulation) -> TranslationLayer:
        """Construct this class from kratos."""
        return TranslationLayer(
            nodes=nodes_from_kratos(kratos),
            connectors=trusses_from_kratos(kratos),
            constraints=constraints_from_kratos(kratos),
            loads=loads_from_kratos(kratos),
        )

    def to_kratos(self) -> KratosSimulation:
        """Export this simulation to kratos."""
        return KratosSimulation(
            model=_to_kratos_model(self),
            materials=_to_kratos_materials(self.connectors),
            parameters=_to_kratos_parameters(self),
        )

    def to_nastran(self) -> NastranSimulation:
        """Export this simulation to nastran."""
        return NastranSimulation(
            bulk_data=BulkDataSection(
                entries=_to_nastran_crods(self.connectors)
                + _to_nastran_forces(self.loads)
                + _to_nastran_grids(self.nodes)
                + _to_nastran_mat1s(self.connectors)
            )
        )


def _to_kratos_model(simulation: TranslationLayer) -> Model:
    return Model(
        properties={0: {}},
        nodes={point.id: point.to_kratos() for point in simulation.nodes},
        elements=_to_kratos_elements(simulation.connectors),
        conditions=_to_kratos_conditions(simulation.loads),
        sub_models=_merge_dicts(
            [
                _to_kratos_submodels_trusses(simulation.connectors),
                _to_kratos_submodels_constraints(simulation.constraints),
                _to_kratos_submodels_loads(simulation.loads),
            ]
        ),
    )


def _to_kratos_materials(connectors: list[Connector]) -> list[KratosMaterial]:
    return [
        connector.to_kratos_material(i + 1)
        for i, connector in enumerate(connectors)
        if isinstance(connector, Truss)
    ]


def _to_kratos_parameters(simulation: TranslationLayer) -> SimulationParameters:
    return SimulationParameters(
        constraints=[
            constraint.to_kratos_constraint(i + 1)
            for i, constraint in enumerate(simulation.constraints)
        ],
        loads=[load.to_kratos_load(i + 1) for i, load in enumerate(simulation.loads)],
    )


def _merge_dicts(dicts: list[dict]) -> dict:
    merged_dict = {}
    for d in dicts:
        merged_dict.update(d)
    return merged_dict


def _to_kratos_elements(connectors: list[Connector]) -> dict[str, dict[int, Element]]:
    return {
        "TrussLinearElement3D2N": {
            i + 1: connector.to_kratos_element() for i, connector in enumerate(connectors)
        }
    }


def _to_kratos_conditions(loads: list[Load]) -> dict[str, dict[int, Condition]]:
    return {
        "PointLoadCondition2D1N": {i + 1: load.to_kratos_condition() for i, load in enumerate(loads)}
    }


def _to_kratos_submodels_trusses(connectors: list[Connector]) -> dict[str, SubModel]:
    return {
        f"truss_{i+1}": connector.to_kratos_submodel(i + 1)
        for i, connector in enumerate(connectors)
        if isinstance(connector, Truss)
    }


def _to_kratos_submodels_constraints(constraints: list[Constraint]) -> dict[str, SubModel]:
    return {
        f"constraint_{i+1}": constraint.to_kratos_submodel()
        for i, constraint in enumerate(constraints)
    }


def _to_kratos_submodels_loads(loads: list[Load]) -> dict[str, SubModel]:
    return {f"load_{i+1}": load.to_kratos_submodel(i + 1) for i, load in enumerate(loads)}


def _to_nastran_crods(connectors: list[Connector]) -> list[_BulkDataEntry]:
    crods: list[_BulkDataEntry] = []
    for i, connector in enumerate(connectors):
        crods.append(
            Crod(
                eid=i + 1, pid=i + 1, g1=connector.first_point_index, g2=connector.second_point_index
            )
        )

    return crods


def _to_nastran_forces(loads: list[Load]) -> list[_BulkDataEntry]:
    forces: list[_BulkDataEntry] = []
    for i, load in enumerate(loads):
        forces.append(
            Force(
                sid=i + 1,
                g=load.node_id,
                cid=0,
                f=load.modulus,
                n1=load.direction[0],
                n2=load.direction[1],
                n3=load.direction[2],
            )
        )

    return forces


def _to_nastran_grids(nodes: list[Point]) -> list[_BulkDataEntry]:
    return [
        Grid(
            id=node.id,
            cp=None,
            x1=node.x.millimeters,
            x2=node.y.millimeters,
            x3=node.z.millimeters,
        )
        for node in nodes
    ]


def _to_nastran_mat1s(connectors: list[Connector]) -> list[_BulkDataEntry]:
    mat1s: list[_BulkDataEntry] = []
    for i, connector in enumerate(connectors):
        mat1s.append(
            Mat1(
                mid=i + 1,
                e=connector.material.young_modulus.megapascal
                if connector.material.young_modulus is not None
                else None,
            )
        )

    return mat1s
