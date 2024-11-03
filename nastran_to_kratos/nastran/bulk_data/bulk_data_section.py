from __future__ import annotations

from dataclasses import dataclass

from .entries import Crod, Force, Grid, Prod, Spc, _BulkDataEntry

ENTRY_CLASS_MAPPING: dict[str, type[_BulkDataEntry]] = {
    "GRID": Grid,
    "CROD": Crod,
    "PROD": Prod,
    "FORCE": Force,
    "SPC": Spc,
}


@dataclass
class BulkDataSection:
    """The bulk data section containing the model and loads."""

    entries: list[_BulkDataEntry]

    @classmethod
    def empty(cls) -> BulkDataSection:
        """Construct an empty NastranSimulation instance."""
        return BulkDataSection(entries=[])

    @classmethod
    def from_file_content(cls, file_content: list[str]) -> BulkDataSection:
        """Construct this class from the contents of a nastran file."""
        bulk_data = BulkDataSection.empty()

        for line in file_content:
            if _line_should_be_ignored(line):
                continue

            line_split_into_fields = [line[i : i + 8] for i in range(0, len(line), 8)]
            entry_class = _get_entry_class(line_split_into_fields)
            bulk_data.entries.append(entry_class.read(line_split_into_fields))

        return bulk_data


def _line_should_be_ignored(line: str) -> bool:
    """Return wether a given line should be skipped (e.g. if it is a comment)."""
    if line == "":
        return True

    if line.startswith(("$", "SOL", "CEND", "BEGIN", "ENDDATA")):
        return True

    return False


def _get_entry_class(line_split_into_fields: list[str]) -> type[_BulkDataEntry]:
    entry_identifyer = line_split_into_fields[0].strip()
    try:
        return ENTRY_CLASS_MAPPING[entry_identifyer]
    except KeyError:
        raise EntryIdentifyerNotSupportedError(entry_identifyer) from None


class EntryIdentifyerNotSupportedError(Exception):
    """Raised when a line starts with an identifyer, that is not in ENTRY_CLASS_MAPPING."""

    def __init__(self, entry_identifyer: str) -> None:
        super().__init__(f"{entry_identifyer} is not a supported entry type.")
