from __future__ import annotations

from dataclasses import dataclass

from .subcase import Subcase


@dataclass
class CaseControlSection:
    """The Case Control Section has several basic functions.

    Specifically it:
        - Selects loads and constraints.
        - Requests printing, plotting, and/or punching of input and out data.
        - Defines the subcase structure for the analysis.
    """

    general: Subcase
    subcases: dict[int, Subcase]
