from dataclasses import dataclass, field

from .node import Node

_EMPTY_DICT: dict = field(default_factory=dict)
INDENT = "    "


@dataclass
class Model:
    """The parameters defining the shape and properties of the model in kratos."""

    nodes: dict[int, Node] = _EMPTY_DICT

    def to_mdpa(self) -> list[str]:
        """Export this model to a list of string compatible with the kratos .mdpa files."""
        mdpa_content = []

        if len(self.nodes) != 0:
            mdpa_content.extend(_nodes_to_mdpa(self.nodes))

        return mdpa_content


def _nodes_to_mdpa(nodes: dict[int, Node]) -> list[str]:
    mdpa_content = []

    mdpa_content.append("Begin Nodes")

    for node_id, node in nodes.items():
        mdpa_content.append(INDENT + node.to_mdpa(node_id))

    mdpa_content.append("End Nodes")

    return mdpa_content
