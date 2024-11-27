from dataclasses import dataclass


@dataclass
class Element:
    """An assignment between a property and nodes."""

    property_id: int
    "Identifyer of the model property this element refers to."

    node_ids: list[int]
    "Identifyers of the nodes in this element."

    def to_mdpa(self, element_id: int) -> str:
        """Export this element to a string, that can be inserted in a .mdpa file."""
        mdpa_content = f"{element_id} {self.property_id}"

        for node_id in self.node_ids:
            mdpa_content += f" {node_id}"

        return mdpa_content
