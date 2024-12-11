from __future__ import annotations

from dataclasses import dataclass

from ._bulk_data_entry import _BulkDataEntry


@dataclass
class Prod(_BulkDataEntry):
    """Defines the properties of a rod element (CROD entry)."""

    pid: int
    "Property identification number."

    mid: int
    "Material identification number."

    a: float
    "Cross-sectional area."

    j: float | None = None
    "Torsional constant."

    c: float = 0.0
    "Coefficient to determine torsional stress."

    nsm: float | None = None
    "Nonstructural mass per unit length."

    @classmethod
    def from_file_content(cls, file_content: list[str]) -> Prod:
        """Construct a Prod from the entry in a nastran file."""
        return Prod(
            pid=int(file_content[1]),
            mid=int(file_content[2]),
            a=float(file_content[3]),
            j=cls._read_optional_field(file_content, 4, float, None),
            c=cls._read_optional_field(file_content, 5, float, 0.0),
            nsm=cls._read_optional_field(file_content, 6, float, None),
        )

    def __hash__(self) -> int:
        """Return a hash of this instance."""
        attributes = tuple(sorted(vars(self).items()))
        return hash(attributes)
