from __future__ import annotations

from dataclasses import dataclass

from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Force


@dataclass
class Load:
    """A force applied to an element."""

    node_id: int
    modulus: float
    direction: tuple[float, float, float]

    @classmethod
    def from_nastran(cls, force: Force) -> Load:
        """Construct this class from nastran."""
        return Load(
            node_id=force.g,
            modulus=force.f,
            direction=(force.n1, force.n2, force.n3),
        )


def loads_from_nastran(bulk_data: BulkDataSection) -> list[Load]:
    """Construct all loads from nastran."""
    return [Load.from_nastran(force) for force in bulk_data.forces]
