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
    def from_file_content(cls, file_content: list[str]) -> Force:
        """Construct a Force from the entry in a nastran file."""
        return Force(
            sid=int(file_content[1]),
            g=int(file_content[2]),
            cid=cls._read_optional_field(file_content, 3, int, 0),
            f=float(file_content[4]),
            n1=float(file_content[5]),
            n2=float(file_content[6]),
            n3=float(file_content[7]),
        )
