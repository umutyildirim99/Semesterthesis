from __future__ import annotations

from dataclasses import dataclass


@dataclass
class KratosConstraint:
    """Fixation of an element."""

    model_part_name: str
    constrained_per_axis: tuple[bool, bool, bool]
    value_per_axis: tuple[float | None, float | None, float | None]

    @classmethod
    def from_json(cls, json: dict) -> KratosConstraint:
        """Construct this class from Kratos json content."""
        return KratosConstraint(
            model_part_name=json["Parameters"]["model_part_name"],
            constrained_per_axis=tuple(json["Parameters"]["constrained"]),
            value_per_axis=tuple(json["Parameters"]["value"]),
        )

    def to_json(self) -> dict:
        """Export this constraint to a dictionary in a Kratos compatible format."""
        return {
            "python_module": "assign_vector_variable_process",
            "kratos_module": "KratosMultiphysics",
            "process_name": "AssignVectorVariableProcess",
            "Parameters": {
                "model_part_name": self.model_part_name,
                "variable_name": "DISPLACEMENT",
                "interval": [0.0, "End"],
                "constrained": self.constrained_per_axis,
                "value": self.value_per_axis,
            },
        }
