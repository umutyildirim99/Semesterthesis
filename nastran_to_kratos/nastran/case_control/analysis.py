from enum import Enum


class Analysis(Enum):
    """Specifies the type of analysis being performed for the current SUBCASE/STEP/SUBSTEP."""

    STATICS = "STATICS"
