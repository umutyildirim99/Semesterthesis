from __future__ import annotations

from dataclasses import dataclass, field

from nastran_to_kratos.nastran import NastranSimulation

from .constraints import Constraint, constraints_from_nastran
from .elements import Connector, Point, nodes_from_nastran
from .loads import Load, loads_from_nastran


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
            constraints=constraints_from_nastran(nastran.bulk_data),
            loads=loads_from_nastran(nastran.bulk_data),
        )
