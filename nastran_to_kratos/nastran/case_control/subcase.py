from __future__ import annotations

from dataclasses import dataclass

from .analysis import Analysis
from .displacement import Displacement
from .strain import Strain
from .stress import Stress


@dataclass
class Subcase:
    """Description needed."""

    subtitle: str | None = None
    label: str | None = None
    analysis: Analysis | None = None
    displacement: Displacement | None = None
    spc: int | None = None
    load: int | None = None
    strain: Strain | None = None
    stress: Stress | None = None

    @classmethod
    def empty(cls) -> Subcase:
        """Construct a minimal instance of this class."""
        return Subcase()

    @classmethod
    def from_file_content(cls, _file_content: list[str]) -> Subcase:
        """Construct this class from the contents of a nastran file."""
        return cls.empty()
