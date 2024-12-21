from __future__ import annotations

from dataclasses import dataclass

from ._bulk_data_entry import _BulkDataEntry


@dataclass
class Spc(_BulkDataEntry):
    """Defines a set of single-point constraints and enforced motion."""

    sid: int
    "Identification number of the single-point constraint set."

    g1: int
    "Grid or scalar point identification number."

    c1: int
    "Component number."

    d1: float = 0.0
    "Value of enforced motion for components g1 at grid c1."

    g2: int | None = None
    "Grid or scalar point identification number."

    c2: int | None = None
    "Component number."

    d2: float | None = None
    "Value of enforced motion for components g2 at grid c2."

    @classmethod
    def from_file_content(cls, file_content: list[str]) -> Spc:
        """Construct a Spc from the entry in a nastran file."""
        return Spc(
            sid=int(file_content[1]),
            g1=int(file_content[2]),
            c1=int(file_content[3]),
            d1=cls._read_optional_field(file_content, 4, float, 0.0),
            g2=cls._read_optional_field(file_content, 5, int, None),
            c2=cls._read_optional_field(file_content, 6, int, None),
            d2=cls._read_optional_field(file_content, 7, float, None),
        )

    def to_file_content(self) -> str:
        """Export this Spc into a line for saving to a nastran file."""
        return "SPC     " + self._fields_to_line(
            fields=[
                self.sid,
                self.g1,
                self.c1,
                self.d1,
                self.g2,
                self.c2,
                self.d2,
            ]
        )

    def __hash__(self) -> int:
        """Return a hash of this instance."""
        attributes = tuple(sorted(vars(self).items()))
        return hash(attributes)
