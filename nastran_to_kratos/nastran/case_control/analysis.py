from ._case_control_enum import _CaseControlEnum


class Analysis(_CaseControlEnum):
    """Specifies the type of analysis being performed for the current SUBCASE/STEP/SUBSTEP."""

    STATICS = "STATICS"
