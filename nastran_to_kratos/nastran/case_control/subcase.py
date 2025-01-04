from __future__ import annotations

from dataclasses import dataclass

from .analysis import Analysis
from .displacement import Displacement
from .strain import Strain
from .stress import Stress


@dataclass
class Subcase:
    """Description needed."""

    analysis: Analysis | None = None
    displacement: Displacement | None = None
    label: str | None = None
    load: int | None = None
    spc: int | None = None
    strain: Strain | None = None
    stress: Stress | None = None
    subtitle: str | None = None

    @classmethod
    def empty(cls) -> Subcase:
        """Construct a minimal instance of this class."""
        return Subcase()

    @classmethod
    def from_file_content(cls, file_content: list[str]) -> Subcase:
        """Construct this class from the contents of a nastran file."""
        subcase = Subcase.empty()

        for line in file_content:
            key = line.split("=")[0].strip()
            value = line.split("=")[1].strip()

            match key:
                case "ANALYSIS":
                    subcase.analysis = Analysis[value]
                case "DISPLACEMENT":
                    subcase.displacement = Displacement[value]
                case "LABEL":
                    subcase.label = value
                case "LOAD":
                    subcase.load = int(value)
                case "SPC":
                    subcase.spc = int(value)
                case "STRAIN":
                    subcase.strain = Strain[value]
                case "STRESS":
                    subcase.stress = Stress[value]
                case "SUBTITLE":
                    subcase.subtitle = value
                case _:
                    raise UnsupportedSubcaseFieldError(key)

        return subcase

    def to_file_content(self) -> list[str]:
        """Export this subcase into lines for saving to a nastran file."""
        lines = []
        if self.analysis is not None:
            lines.append(f"  ANALYSIS = {self.analysis}")
        if self.displacement is not None:
            lines.append(f"  DISPLACEMENT = {self.displacement}")
        if self.label is not None:
            lines.append(f"  LABEL = {self.label}")
        if self.load is not None:
            lines.append(f"  LOAD = {_leftpad8(self.load)}")
        if self.spc is not None:
            lines.append(f"  SPC = {_leftpad8(self.spc)}")
        if self.strain is not None:
            lines.append(f"  STRAIN = {self.strain}")
        if self.stress is not None:
            lines.append(f"  STRESS = {self.stress}")
        if self.subtitle is not None:
            lines.append(f"  SUBTITLE = {self.subtitle}")
        return lines


def _leftpad8(s: str | int) -> str:
    return str(s).rjust(8, " ")


class UnsupportedSubcaseFieldError(Exception):
    """Raised when a subcase field is not (yet) supported."""

    def __init__(self, field_name: str) -> None:
        super().__init__(f"{field_name} is not a supported field for the subcases.")
