from enum import Enum


class _CaseControlEnum(Enum):
    """Parent class to all enumerations in the case control section."""

    def __str__(self) -> str:
        """Export this class into a nastran compatible string."""
        return self.value
