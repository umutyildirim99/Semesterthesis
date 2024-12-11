from __future__ import annotations

from dataclasses import dataclass

from nastran_to_kratos.nastran import NastranSimulation

from .elements import Element, elements_from_nastran


@dataclass
class TranslationLayer:
    """A representation of a simulation used as a translation between nastran and kratos."""

    elements: list[Element] | None = None

    @classmethod
    def from_nastran(cls, nastran: NastranSimulation) -> TranslationLayer:
        """Construct this class from nastran."""
        return TranslationLayer(elements=elements_from_nastran(nastran.bulk_data))
