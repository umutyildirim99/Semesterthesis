from __future__ import annotations

from dataclasses import dataclass

from ._bulk_data_entry import _BulkDataEntry


@dataclass
class Mat1(_BulkDataEntry):
    """Defines the material properties for linear isotropic materials."""

    mid: int
    "Material identification number."

    e: float | None = None
    "Young's modulus."

    g: float | None = None
    "Shear modulus."

    nu: float | None = None
    "Poisson's ratio."

    rho: float | None = None
    "Mass density."

    a: float | None = None
    "Thermal expansion coefficient."

    tref: float = 0.0
    """Reference temperature for the calculation of thermal loads, or a
    temperature-dependent thermal expansion coefficient."""

    ge: float | None = None
    "Structural element damping coefficient."

    st: float | None = None
    "Stress limit for tension."

    sc: float | None = None
    "Stress limit for compression."

    ss: float | None = None
    "Stress limit for shear."

    mcsid: int | None = None
    "Material coordinate system identification number."

    @classmethod
    def from_file_content(cls, file_content: list[str]) -> Mat1:
        """Construct a Mat1 from the entry in a nastran file."""
        return Mat1(
            mid=int(file_content[1]),
            e=cls._read_optional_field(file_content, 2, float, None),
            g=cls._read_optional_field(file_content, 3, float, None),
            nu=cls._read_optional_field(file_content, 4, float, None),
            rho=cls._read_optional_field(file_content, 5, float, None),
            a=cls._read_optional_field(file_content, 6, float, None),
            tref=cls._read_optional_field(file_content, 7, float, 0.0),
            ge=cls._read_optional_field(file_content, 8, float, None),
            st=cls._read_optional_field(file_content, 9, float, None),
            sc=cls._read_optional_field(file_content, 10, float, None),
            ss=cls._read_optional_field(file_content, 11, float, None),
            mcsid=cls._read_optional_field(file_content, 12, int, None),
        )

    def to_file_content(self) -> str:
        """Export this Mat1 into a line for saving to a nastran file."""
        return "MAT1    " + self._fields_to_line(
            [
                self.mid,
                self.e,
                self.g,
                self.nu,
                self.rho,
                self.a,
                self.tref,
                self.ge,
                self.st,
                self.sc,
                self.ss,
                self.mcsid,
            ]
        )

    def __hash__(self) -> int:
        """Return a hash of this instance."""
        attributes = tuple(sorted(vars(self).items()))
        return hash(attributes)
