from __future__ import annotations

from dataclasses import dataclass

from ._bulk_data_entry import _BulkDataEntry


@dataclass
class Conrod(_BulkDataEntry):
    """A tension-compression-torsion element."""

    eid: int
    """Element identification number."""

    g1: int
    """Grid point identification numbers of connection point 1."""

    g2: int
    """Grid point identification numbers of connection point 2."""

    mid: int
    """ Material identification number. (Integer > 0) """
    a: float
    """Area of the rod. (Real)"""
    j: float | None = None
    """Torsional constant. (Real)"""
    c: float | None = None
    """Coefficient for torsional stress determination. (Real)"""
    nsm: float | None = None
    """Nonstructural mass per unit length. (Real)"""

    @classmethod
    def from_file_content(cls, file_content: list[str]) -> Conrod:
        """Construct a CONTROD from the entry in a nastran file."""
        return Conrod(
            eid=int(file_content[1]),
            g1=int(file_content[2]),
            g2=int(file_content[3]),
            mid=int(file_content[4]),
            a=float(file_content[5]),
            j=cls._read_optional_field(file_content, 6, float, None),
            c=cls._read_optional_field(file_content, 7, float, None),
            nsm=cls._read_optional_field(file_content, 8, float, None),
        )

    def to_file_content(self) -> str:
        """Export this Crod into a line for saving to a nastran file."""
        return "CONROD    " + self._fields_to_line(
            [self.eid, self.g1, self.g2, self.mid, self.a, self.j, self.c, self.nsm]
        )

    def __hash__(self) -> int:
        """Return a hash of this instance."""
        attributes = tuple(sorted(vars(self).items()))
        return hash(attributes)
