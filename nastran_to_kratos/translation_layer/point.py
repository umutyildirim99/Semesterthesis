from __future__ import annotations

from dataclasses import dataclass

from quantio import Length

from nastran_to_kratos.kratos.model import Node
from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Grid


@dataclass
class Point:
    """A point in 3D space."""

    id: int
    """Number identifying the point for the entire simulation."""

    x: Length
    """Position of the point on the x-axis."""

    y: Length
    """Position of the point on the y-axis."""

    z: Length
    """Position of the point on the z-axis."""

    @classmethod
    def origin(cls, id_: int) -> Point:
        """Construct a point at with all positions at zero."""
        return Point(id_, Length.zero(), Length.zero(), Length.zero())

    @classmethod
    def from_nastran(cls, grid: Grid) -> Point:
        """Construct this class from nastran."""
        return Point(
            id=grid.id,
            x=Length(millimeters=grid.x1),
            y=Length(millimeters=grid.x2),
            z=Length(millimeters=grid.x3),
        )

    def to_kratos(self) -> Node:
        """Export this Point as a kratos Node."""
        return Node(x=self.x.millimeters, y=self.y.millimeters, z=self.z.millimeters)


def nodes_from_nastran(bulk_data: BulkDataSection) -> list[Point]:
    """Construct all nodes from the nastran grid."""
    return [Point.from_nastran(grid) for grid in _sort_by_grid_id(bulk_data.grids)]


def _sort_by_grid_id(grids: list[Grid]) -> list[Grid]:
    return sorted(grids, key=lambda grid: grid.id)
