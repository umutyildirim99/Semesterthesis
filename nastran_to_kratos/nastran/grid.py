from __future__ import annotations

from dataclasses import dataclass

from ._nastran_entry import _NastranEntry


@dataclass
class Grid(_NastranEntry):
    """A geometric grid point."""

    id: int
    cp: int | None = None
    x1: float = 0.0
    x2: float = 0.0
    x3: float = 0.0
    cd: int | None = None
    ps: str | None = None
    seid: int = 0

    @classmethod
    def read(cls, raw_entry: list[str]) -> Grid:
        """Construct a grid from the entry in a nastran file."""
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
