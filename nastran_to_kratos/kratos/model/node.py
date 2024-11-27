from dataclasses import dataclass


@dataclass
class Node:
    """A single point in space used in the model mesh."""

    x: float
    y: float
    z: float

    def to_mdpa(self, node_id: int) -> str:
        """Export this node to a string, that can be inserted in a .mdpa file."""
        return f"{node_id} {self.x} {self.y} {self.z}"
