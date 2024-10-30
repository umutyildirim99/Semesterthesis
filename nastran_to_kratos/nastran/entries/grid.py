from __future__ import annotations

from dataclasses import dataclass

from ._nastran_entry import _NastranEntry


@dataclass
class Grid(_NastranEntry):
    """A geometric grid point."""

    id: int
    """Grid point identification number."""

    cp: int | None = None
    """Identification number of coordinate system in which the location is defined."""

    x1: float = 0.0
    """Location of the grid point in coordinate system CP in the x-axis."""

    x2: float = 0.0
    """Location of the grid point in coordinate system CP in the y-axis."""

    x3: float = 0.0
    """Location of the grid point in coordinate system CP in the z-axis."""

    cd: int | None = None
    """Identification number of coordinate system in which the displacements, degrees-of-freedom,
    constraints, and solution vectors are defined at the grid point."""

    ps: str | None = None
    """Permanent single-point constraints associated with the grid point (example: "234", "123456",
    "135")."""

    seid: int = 0
    """Superelement identification number."""

    @classmethod
    def read(cls, raw_entry: list[str]) -> Grid:
        """Construct a Grid from the entry in a nastran file."""
        return Grid(
            id=int(raw_entry[1]),
            cp=cls._read_optional_field(raw_entry, 2, int, None),
            x1=cls._read_optional_field(raw_entry, 3, float, 0.0),
            x2=cls._read_optional_field(raw_entry, 4, float, 0.0),
            x3=cls._read_optional_field(raw_entry, 5, float, 0.0),
            cd=cls._read_optional_field(raw_entry, 6, int, None),
            ps=cls._read_optional_field(raw_entry, 7, str, None),
            seid=cls._read_optional_field(raw_entry, 8, int, 0),
        )
