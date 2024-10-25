from __future__ import annotations

from dataclasses import dataclass

from ._nastran_entry import _NastranEntry


@dataclass
class Crod(_NastranEntry):
    """A tension-compression-torsion element."""

    eid: int
    """Element identification number."""

    g1: int
    """Grid point identification numbers of connection point 1."""

    g2: int
    """Grid point identification numbers of connection point 2."""

    pid: int | None = None
    """Property identification number of a PROD entry."""

    @classmethod
    def read(cls, raw_entry: list[str]) -> Crod:
        """Construct a crod from the entry in a nastran file."""
        return Crod(
            eid=int(raw_entry[1]),
            pid=cls._read_optional_field(raw_entry, 2, int, None),
            g1=int(raw_entry[3]),
            g2=int(raw_entry[4]),
        )
