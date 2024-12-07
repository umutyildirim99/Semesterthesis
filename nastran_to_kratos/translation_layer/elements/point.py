from __future__ import annotations

from dataclasses import dataclass

from quantio import Length

from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Grid


@dataclass
class Point:
    """A point in 3D space."""

    x: Length
    y: Length
    z: Length

    @classmethod
    def from_nastran(cls, grid: Grid) -> Point:
        """Construct this class from nastran."""
        return Point(
            x=Length(millimeters=grid.x3),
            y=Length(millimeters=grid.x2),
            z=Length(millimeters=grid.x1),
        )


def nodes_from_nastran(bulk_data: BulkDataSection) -> list[Point]:
    """Construct all nodes from the nastran grid."""
    return [Point.from_nastran(grid) for grid in _sort_by_grid_id(bulk_data.grids)]


def _sort_by_grid_id(grids: list[Grid]) -> list[Grid]:
    return sorted(grids, key=lambda grid: grid.id)
