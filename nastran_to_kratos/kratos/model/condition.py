from dataclasses import dataclass


@dataclass
class Condition:
    """TODO: find out what this is."""

    property_id: int
    "Identifyer of the model property this condition refers to."

    node_ids: list[int]
    "Identifyers of the nodes in this condition."

    def to_mdpa(self, condition_id: int) -> str:
        """Export this condition to a string, that can be inserted in a .mdpa file."""
        mdpa_content = f"{condition_id} {self.property_id}"

        for node_id in self.node_ids:
            mdpa_content += f" {node_id}"

        return mdpa_content
