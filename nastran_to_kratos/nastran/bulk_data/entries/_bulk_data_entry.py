from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class _BulkDataEntry(ABC):
    """The template for any single nastran element.

    This class should not be used directly.
    """

    @classmethod
    @abstractmethod
    def from_file_content(cls, file_content: list[str]) -> _BulkDataEntry:
        """Create this class from the relevant entry in a nastran file."""

    @classmethod
    def _read_optional_field(
        cls,
        raw_entry: list[str],
        field_index: int,
        target_class: type[T],
        default_value: T,
    ) -> T:
        """Read an optional field from a nastran entry.

        Most fields in nastran are optional. In that case they are either not present at all or just
        entirely blank spaces. If a field exists and has content, this function strips the raw field
        string of all blank spaces and converts it to the respective class (like int, float, str,
        ...). If not, a default value is returned (like None, 0.0, ...).

        Args:
            raw_entry: entire list of fields in the entry, that is also passed to read()
            field_index: index of the relevant field in the raw entry
            target_class: class this entry should be parsed into if it is present
            default_value (T): default value to be returned if the field is not present

        Returns:
            either the string parsed into the target class or the default value

        """
        try:
            field_is_empty = raw_entry[field_index] == " " * 8
        except IndexError:
            field_is_empty = True

        if field_is_empty:
            return default_value
        return target_class(raw_entry[field_index].strip())

    # @abstractmethod
    def to_file_content(self) -> str:
        """Export this entry into a line for saving to a nastran file."""
        raise NotImplementedError

    def _fill(self, field: str | float | None) -> str:
        """Fill a string with spaces of length 8."""
        if field is None:
            return ""
        return str(field).rjust(8)

    @abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError
