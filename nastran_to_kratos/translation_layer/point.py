from __future__ import annotations

from dataclasses import dataclass

from nastran_to_kratos.kratos import KratosSimulation
from nastran_to_kratos.kratos.model import Node
from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Grid


@dataclass
class Point:
    """A point in 3D space."""

    id: int
    """Number identifying the point for the entire simulation."""

    x: float
    """Position of the point on the x-axis."""

    y: float
    """Position of the point on the y-axis."""

    z: float
    """Position of the point on the z-axis."""

    @classmethod
    def origin(cls, id_: int) -> Point:
        """Construct a point at with all positions at zero."""
        return Point(id_, 0, 0, 0)

    @classmethod
    def from_nastran(cls, grid: Grid) -> Point:
        """Construct this class from nastran."""
        return Point(
            id=grid.id,
            x=grid.x1,
            y=grid.x2,
            z=grid.x3,
        )

    @classmethod
    def from_kratos(cls, id_: int, node: Node) -> Point:
        """Construct this class from nastran."""
        return Point(
            id=id_,
            x=node.x,
            y=node.z,
            z=node.y,
        )

    def to_kratos(self) -> Node:
        """Export this Point as a kratos Node."""
        return Node(x=self.x, y=self.y, z=self.z)


def nodes_from_nastran(bulk_data: BulkDataSection) -> list[Point]:
    """Construct all nodes from the nastran grid."""
    return [Point.from_nastran(grid) for grid in _sort_by_grid_id(bulk_data.grids)]


def nodes_from_kratos(kratos: KratosSimulation) -> list[Point]:
    """Construct all nodes from a kratos simulation."""
    if kratos.model is None:
        return []
    return [Point.from_kratos(id_, node) for id_, node in kratos.model.nodes.items()]


def _sort_by_grid_id(grids: list[Grid]) -> list[Grid]:
    return sorted(grids, key=lambda grid: grid.id)
