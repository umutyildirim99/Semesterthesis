from __future__ import annotations

from dataclasses import dataclass, field

from nastran_to_kratos.kratos import KratosSimulation
from nastran_to_kratos.kratos.simulation_parameters import Constraint as KratosConstraint
from nastran_to_kratos.kratos.simulation_parameters import Load as KratosLoad
from nastran_to_kratos.kratos.simulation_parameters import SimulationParameters
from nastran_to_kratos.nastran import NastranSimulation

from .constraints import Constraint, constraints_from_nastran
from .elements import Element, elements_from_nastran
from .loads import Load, loads_from_nastran


@dataclass
class TranslationLayer:
    """A representation of a simulation used as a translation between nastran and kratos."""

    elements: list[Element] = field(default_factory=list)
    constraints: list[Constraint] = field(default_factory=list)
    loads: list[Load] = field(default_factory=list)

    @classmethod
    def from_nastran(cls, nastran: NastranSimulation) -> TranslationLayer:
        """Construct this class from nastran."""
        return TranslationLayer(
            elements=elements_from_nastran(nastran.bulk_data),
            constraints=constraints_from_nastran(nastran.bulk_data),
            loads=loads_from_nastran(nastran.bulk_data),
        )

    def to_kratos(self) -> KratosSimulation:
        """Export this TranslationLayer to a KratosSimulation."""
        element_index_by_node_index = _index_elements_by_global_node_id(self.elements)

        return KratosSimulation(
            parameters=SimulationParameters(
                constraints=_constraints_to_kratos(self.constraints, element_index_by_node_index),
                loads=_loads_to_kratos(self.loads, element_index_by_node_index),
            )
        )


def _index_elements_by_global_node_id(elements: list[Element]) -> dict[int, int]:
    element_index_by_node_index: dict[int, int] = {}
    for element_index, element in enumerate(elements):
        for _ in element.nodes:
            element_index_by_node_index[len(element_index_by_node_index)] = element_index
    return element_index_by_node_index


def _constraints_to_kratos(
    constraints: list[Constraint], element_index_by_node_index: dict[int, int]
) -> list[KratosConstraint]:
    return [
        KratosConstraint(
            model_part_name=f"element_{element_index_by_node_index[constraint.node_id]}",
            constrained_per_axis=constraint.translation_by_axis,
            value_per_axis=(
                0 if constraint.translation_by_axis[0] is True else None,
                0 if constraint.translation_by_axis[1] is True else None,
                0 if constraint.translation_by_axis[2] is True else None,
            ),
        )
        for constraint in constraints
    ]


def _loads_to_kratos(
    loads: list[Load], element_index_by_node_index: dict[int, int]
) -> list[KratosLoad]:
    return [
        KratosLoad(
            model_part_name=f"element_{element_index_by_node_index[load.node_id]}",
            modulus=load.modulus,
            direction=load.direction,
        )
        for load in loads
    ]
