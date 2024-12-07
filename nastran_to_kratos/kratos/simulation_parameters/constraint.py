from dataclasses import dataclass


@dataclass
class Constraint:
    """Fixation of an element."""

    model_part_name: str
    constrained_per_axis: tuple[bool | None, bool | None, bool | None]
    value_per_axis: tuple[float, float, float]

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
