from __future__ import annotations

from dataclasses import dataclass, field

from nastran_to_kratos.nastran import NastranSimulation

from .constraints import Constraint, constraints_from_nastran
from .elements import Element, elements_from_nastran


@dataclass
class TranslationLayer:
    """A representation of a simulation used as a translation between nastran and kratos."""

    elements: list[Element] = field(default_factory=list)
    constraints: list[Constraint] = field(default_factory=list)

    @classmethod
    def from_nastran(cls, nastran: NastranSimulation) -> TranslationLayer:
        """Construct this class from nastran."""
        return TranslationLayer(
            elements=elements_from_nastran(nastran.bulk_data),
            constraints=constraints_from_nastran(nastran.bulk_data),
        )
