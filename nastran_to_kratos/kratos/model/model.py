from dataclasses import dataclass, field

from .node import Node

INDENT = "    "


@dataclass
class Model:
    """The parameters defining the shape and properties of the model in kratos."""

    properties: dict[int, dict[str, float]] = field(default_factory=dict)
    nodes: dict[int, Node] = field(default_factory=dict)

    def to_mdpa(self) -> list[str]:
        """Export this model to a list of string compatible with the kratos .mdpa files."""
        mdpa_content = []

        if len(self.properties) != 0:
            mdpa_content.extend(_properties_to_mdpa(self.properties))
            mdpa_content.append("")

        if len(self.nodes) != 0:
            mdpa_content.extend(_nodes_to_mdpa(self.nodes))
            mdpa_content.append("")

        return _remove_empty_last_row(mdpa_content)


def _properties_to_mdpa(properties: dict[int, dict[str, float]]) -> list[str]:
    mdpa_content = []

    for property_id, property_ in properties.items():
        mdpa_content.append(f"Begin Properties {property_id}")

        for key, value in property_.items():
            mdpa_content.append(INDENT + f"{key} {value}")

        mdpa_content.append("End Properties")
        mdpa_content.append("")

    return _remove_empty_last_row(mdpa_content)


def _nodes_to_mdpa(nodes: dict[int, Node]) -> list[str]:
    mdpa_content = []

    mdpa_content.append("Begin Nodes")

    for node_id, node in nodes.items():
        mdpa_content.append(INDENT + node.to_mdpa(node_id))

    mdpa_content.append("End Nodes")

    return mdpa_content


def _remove_empty_last_row(mdpa_content: list[str]) -> list[str]:
    if len(mdpa_content) != 0 and mdpa_content[-1] == "":
        return mdpa_content[:-1]
    return mdpa_content
