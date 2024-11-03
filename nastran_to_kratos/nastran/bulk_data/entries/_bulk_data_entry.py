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
    def read(cls, raw_entry: list[str]) -> _BulkDataEntry:
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
