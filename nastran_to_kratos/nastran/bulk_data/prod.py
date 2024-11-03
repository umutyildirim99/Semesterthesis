from __future__ import annotations

from dataclasses import dataclass

from ._nastran_entry import _NastranEntry


@dataclass
class Prod(_NastranEntry):
    """Defines the properties of a rod element (CROD entry)."""

    pid: int
    mid: int
    a: float
    j: float
    nsm: float
    c: float = 0.0

    @classmethod
    def read(cls, raw_entry: list[str]) -> Prod:
        """Construct a Prod from the entry in a nastran file."""
        return Prod(
            pid=int(raw_entry[1]),
            mid=int(raw_entry[2]),
            a=float(raw_entry[3]),
            j=float(raw_entry[4]),
            c=cls._read_optional_field(raw_entry, 5, float, 0.0),
            nsm=float(raw_entry[6]),
        )
