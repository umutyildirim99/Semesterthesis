from __future__ import annotations

from dataclasses import dataclass

from ._bulk_data_entry import _BulkDataEntry


@dataclass
class Force(_BulkDataEntry):
    """Defines a static concentrated force at a grid point by specifying a vector."""

    sid: int
    "Load set identification number."

    g: int
    "Grid point identification number."

    cid: int
    "Coordinate system identification number."

    f: float
    "Scale factor."

    n1: float
    "X-Components of a vector measured in coordinate system defined by CID."

    n2: float
    "Y-Components of a vector measured in coordinate system defined by CID."

    n3: float
    "Z-Components of a vector measured in coordinate system defined by CID."

    @classmethod
    def read(cls, raw_entry: list[str]) -> Force:
        """Construct a Force from the entry in a nastran file."""
        return Force(
            sid=int(raw_entry[1]),
            g=int(raw_entry[2]),
            cid=cls._read_optional_field(raw_entry, 3, int, 0),
            f=float(raw_entry[4]),
            n1=float(raw_entry[5]),
            n2=float(raw_entry[6]),
            n3=float(raw_entry[7]),
        )
