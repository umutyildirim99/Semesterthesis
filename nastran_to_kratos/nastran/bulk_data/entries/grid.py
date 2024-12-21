from __future__ import annotations

from dataclasses import dataclass

from ._bulk_data_entry import _BulkDataEntry


@dataclass
class Grid(_BulkDataEntry):
    """A geometric grid point."""

    id: int
    """Grid point identification number."""

    cp: int | None = None
    """Identification number of coordinate system in which the location is defined."""

    x1: float = 0.0
    """Location of the grid point in coordinate system CP in the x-axis."""

    x2: float = 0.0
    """Location of the grid point in coordinate system CP in the y-axis."""

    x3: float = 0.0
    """Location of the grid point in coordinate system CP in the z-axis."""

    cd: int | None = None
    """Identification number of coordinate system in which the displacements, degrees-of-freedom,
    constraints, and solution vectors are defined at the grid point."""

    ps: str | None = None
    """Permanent single-point constraints associated with the grid point (example: "234", "123456",
    "135")."""

    seid: int | None = None
    """Superelement identification number."""

    @classmethod
    def from_file_content(cls, file_content: list[str]) -> Grid:
        """Construct a Grid from the entry in a nastran file."""
        return Grid(
            id=int(file_content[1]),
            cp=cls._read_optional_field(file_content, 2, int, None),
            x1=cls._read_optional_field(file_content, 3, float, 0.0),
            x2=cls._read_optional_field(file_content, 4, float, 0.0),
            x3=cls._read_optional_field(file_content, 5, float, 0.0),
            cd=cls._read_optional_field(file_content, 6, int, None),
            ps=cls._read_optional_field(file_content, 7, str, None),
            seid=cls._read_optional_field(file_content, 8, int, None),
        )

    def to_file_content(self) -> str:
        """Export this entry into a line for saving to a nastran file."""
        return "GRID    " + self._fields_to_line(
            [self.id, self.cp, self.x1, self.x2, self.x3, self.cd, self.ps, self.seid]
        )

    def __hash__(self) -> int:
        """Return a hash of this instance."""
        attributes = tuple(sorted(vars(self).items()))
        return hash(attributes)
