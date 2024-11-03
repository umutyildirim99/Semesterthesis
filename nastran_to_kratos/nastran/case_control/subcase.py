from __future__ import annotations

from dataclasses import dataclass

from .analysis import Analysis
from .displacement import Displacement
from .strain import Strain
from .stress import Stress


@dataclass
class Subcase:
    """Description needed."""

    subtitle: str
    label: str
    analysis: Analysis
    displacement: Displacement | None
    spc: int | None
    load: int | None
    strain: Strain | None
    stress: Stress | None
