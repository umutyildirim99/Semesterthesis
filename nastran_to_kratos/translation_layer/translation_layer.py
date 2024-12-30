from __future__ import annotations

from dataclasses import dataclass, field

from quantio import Area

from nastran_to_kratos.kratos.kratos_simulation import KratosSimulation, SimulationParameters
from nastran_to_kratos.kratos.material import KratosMaterial
from nastran_to_kratos.kratos.model import Condition, Element, Model, SubModel
from nastran_to_kratos.nastran import NastranSimulation

from .connector import Connector, Truss, trusses_from_nastran
from .constraint import Constraint, constraints_from_nastran
from .load import Load, loads_from_nastran
from .material import Material
from .point import Point, nodes_from_nastran


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
            nodes=_nodes_from_kratos(kratos),
            connectors=_connectors_from_kratos(kratos),
            constraints=_constraints_from_kratos(kratos),
            loads=_loads_from_kratos(kratos),
        )

    def to_kratos(self) -> KratosSimulation:
        """Export this simulation to kratos."""
        return KratosSimulation(
            model=_to_kratos_model(self),
            materials=_to_kratos_materials(self.connectors),
            parameters=_to_kratos_parameters(self),
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


def _nodes_from_kratos(kratos: KratosSimulation) -> list[Point]:
    if kratos.model is None:
        return []
    return [Point.from_kratos(id_, node) for id_, node in kratos.model.nodes.items()]


def _connectors_from_kratos(kratos: KratosSimulation) -> list[Connector]:
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
                cross_section=Area(square_millimeters=truss_material.variables["CROSS_AREA"]),
                material=Material.from_kratos(truss_material),
            )
        )

    return connectors


def _constraints_from_kratos(kratos: KratosSimulation) -> list[Constraint]:
    if kratos.parameters is None or kratos.model is None:
        return []

    constraints = []
    for constraint in kratos.parameters.constraints:
        constraint_id = constraint.model_part_name.split(".")[-1]
        node_id = kratos.model.sub_models[constraint_id].nodes[0]

        constraints.append(
            Constraint(
                node_id,
                translation_by_axis=constraint.constrained_per_axis,
                rotation_by_axis=(False, False, False),
            )
        )

    return constraints


def _loads_from_kratos(kratos: KratosSimulation) -> list[Load]:
    if kratos.parameters is None or kratos.model is None:
        return []

    loads = []
    for load in kratos.parameters.loads:
        load_id = load.model_part_name.split(".")[-1]
        node_id = kratos.model.sub_models[load_id].nodes[0]

        loads.append(
            Load(
                node_id,
                modulus=load.modulus,
                direction=load.direction,
            )
        )

    return loads
