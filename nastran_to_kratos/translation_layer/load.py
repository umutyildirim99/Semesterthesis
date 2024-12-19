from __future__ import annotations

from dataclasses import dataclass

from nastran_to_kratos.kratos.model import Condition, SubModel
from nastran_to_kratos.kratos.simulation_parameters import KratosLoad
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

    def to_kratos_condition(self) -> Condition:
        """Export this load to a kratos condition."""
        return Condition(property_id=0, node_ids=[self.node_id])

    def to_kratos_submodel(self, condition_index: int) -> SubModel:
        """Export this load to a kratos sub-model."""
        return SubModel(nodes=[self.node_id], conditions=[condition_index])

    def to_kratos_load(self, load_index: int) -> KratosLoad:
        """Export this load to kratos."""
        return KratosLoad(
            model_part_name=f"load_{load_index}",
            modulus=self.modulus,
            direction=self.direction,
        )


def loads_from_nastran(bulk_data: BulkDataSection) -> list[Load]:
    """Construct all loads from nastran."""
    return [Load.from_nastran(force) for force in bulk_data.forces]
