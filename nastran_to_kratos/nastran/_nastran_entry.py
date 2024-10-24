from abc import ABC, abstractmethod


class _NastranEntry(ABC):
    """The template for any single nastran element.

    This class should not be used directly."""

    @classmethod
    @abstractmethod
    def read(cls, raw_entry: list[str]) -> "_NastranEntry":
        """Create this class from the relevant entry in a nastran file."""
