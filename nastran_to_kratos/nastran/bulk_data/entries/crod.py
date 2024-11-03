from __future__ import annotations

from dataclasses import dataclass

from ._bulk_data_entry import _BulkDataEntry


@dataclass
class Crod(_BulkDataEntry):
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
        """Construct a Crod from the entry in a nastran file."""
        return Crod(
            eid=int(raw_entry[1]),
            pid=cls._read_optional_field(raw_entry, 2, int, None),
            g1=int(raw_entry[3]),
            g2=int(raw_entry[4]),
        )
