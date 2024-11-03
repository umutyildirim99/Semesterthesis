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
                case "SUBTITLE":
                    subcase.subtitle = value
                case _:
                    raise UnsupportedSubcaseFieldError(key)

        return subcase


class UnsupportedSubcaseFieldError(Exception):
    """Raised when a subcase field is not (yet) supported."""

    def __init__(self, field_name: str) -> None:
        super().__init__(f"{field_name} is not a supported field for the subcases.")
