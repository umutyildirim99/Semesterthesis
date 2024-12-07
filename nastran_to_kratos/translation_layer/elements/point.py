from __future__ import annotations

from dataclasses import dataclass

from quantio import Length

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
