from dataclasses import dataclass


@dataclass
class KratosMaterial:
    """A material."""

    model_part_name: str
    "Identifyer of the SubModelPart this material is mapped to."

    properties_id: int
    "Identifyer of the property for which this material is applied."

    material_name: str
    "Name of the material used for clarity."

    constitutive_law: str
    "I don't know."

    variables: dict[str, float]
    "Container of the material properties, like YOUNG_MODULUS or DENSITY."

    def to_json(self) -> dict:
        """Export this material to a dictionary in a Kratos compatible format."""
        return {
            "model_part_name": self.model_part_name,
            "properties_id": self.properties_id,
            "Material": {
                "name": self.material_name,
                "constitutive_law": {"name": self.constitutive_law},
                "Variables": self.variables,
                "tables": {},
            },
        }
