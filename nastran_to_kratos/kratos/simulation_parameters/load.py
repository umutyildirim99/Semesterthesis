from dataclasses import dataclass


@dataclass
class KratosLoad:
    """A mechanical load applied to the model."""

    model_part_name: str
    modulus: float
    direction: tuple[float, float, float]

    def to_json(self) -> dict:
        """Export this load to a dictionary in a Kratos compatible format."""
        return {
            "python_module": "assign_vector_by_direction_to_condition_process",
            "kratos_module": "KratosMultiphysics",
            "check": "DirectorVectorNonZero direction",
            "process_name": "ApplyVectorByDirectionToConditionProcess",
            "Parameters": {
                "model_part_name": self.model_part_name,
                "variable_name": "POINT_LOAD",
                "interval": [0.0, "End"],
                "modulus": self.modulus,
                "direction": self.direction,
            },
        }
