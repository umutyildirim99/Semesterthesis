from enum import Enum, auto


class Analysis(Enum):
    """Specifies the type of analysis being performed for the current SUBCASE/STEP/SUBSTEP."""

    STATICS = auto()
