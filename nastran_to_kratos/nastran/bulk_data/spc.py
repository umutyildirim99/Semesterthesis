from __future__ import annotations

from dataclasses import dataclass

from ._nastran_entry import _NastranEntry


@dataclass
class Spc(_NastranEntry):
    """Defines a set of single-point constraints and enforced motion."""

    sid: int
    "Identification number of the single-point constraint set."

    g1: int
    "Grid or scalar point identification number."

    c1: int
    "Component number."

    d1: float
    "Value of enforced motion for components g1 at grid c1."

    g2: int | None
    "Grid or scalar point identification number."

    c2: int | None
    "Component number."

    d2: float | None
    "Value of enforced motion for components g2 at grid c2."

    @classmethod
    def read(cls, raw_entry: list[str]) -> Spc:
        """Construct a Spc from the entry in a nastran file."""
        return Spc(
            sid=int(raw_entry[1]),
            g1=int(raw_entry[2]),
            c1=int(raw_entry[3]),
            d1=cls._read_optional_field(raw_entry, 4, float, 0.0),
            g2=cls._read_optional_field(raw_entry, 5, int, None),
            c2=cls._read_optional_field(raw_entry, 6, int, None),
            d2=cls._read_optional_field(raw_entry, 7, float, None),
        )
