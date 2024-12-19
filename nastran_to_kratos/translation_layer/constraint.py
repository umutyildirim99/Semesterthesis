from __future__ import annotations

from dataclasses import dataclass

from nastran_to_kratos.kratos.model import SubModel
from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Spc


@dataclass
class Constraint:
    """Limitation on the movement of an element."""

    node_id: int
    translation_by_axis: tuple[bool, bool, bool]
    rotation_by_axis: tuple[bool, bool, bool]

    @classmethod
    def from_nastran(cls, spc: Spc) -> Constraint:
        """Construct this class from nastran."""
        return Constraint(
            node_id=spc.g1,
            translation_by_axis=(
                "1" in str(spc.c1),
                "2" in str(spc.c1),
                "3" in str(spc.c1),
            ),
            rotation_by_axis=(
                "4" in str(spc.c1),
                "5" in str(spc.c1),
                "6" in str(spc.c1),
            ),
        )

    def to_kratos_submodel(self) -> SubModel:
        """Export this constraint to a kratos sub-model."""
        return SubModel(nodes=[self.node_id])


def constraints_from_nastran(bulk_data: BulkDataSection) -> list[Constraint]:
    """Construct all constraints from nastran."""
    return [Constraint.from_nastran(spc) for spc in bulk_data.spcs]
