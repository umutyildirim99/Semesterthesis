from __future__ import annotations

from dataclasses import dataclass

from ._bulk_data_entry import _BulkDataEntry


@dataclass
class Prod(_BulkDataEntry):
    """Defines the properties of a rod element (CROD entry)."""

    pid: int
    mid: int
    a: float
    j: float
    nsm: float
    c: float = 0.0

    @classmethod
    def from_file_content(cls, file_content: list[str]) -> Prod:
        """Construct a Prod from the entry in a nastran file."""
        return Prod(
            pid=int(file_content[1]),
            mid=int(file_content[2]),
            a=float(file_content[3]),
            j=float(file_content[4]),
            c=cls._read_optional_field(file_content, 5, float, 0.0),
            nsm=float(file_content[6]),
        )
