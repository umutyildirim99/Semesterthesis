from __future__ import annotations

from dataclasses import dataclass

from .entries import Crod, Force, Grid, Mat1, Prod, Spc, _BulkDataEntry


@dataclass
class BulkDataSection:
    """The bulk data section containing the model and loads."""

    entries: list[_BulkDataEntry]

    @classmethod
    def empty(cls) -> BulkDataSection:
        """Construct a minimal instance of this class."""
        return BulkDataSection(entries=[])

    @classmethod
    def from_file_content(cls, file_content: list[str]) -> BulkDataSection:
        """Construct this class from the contents of a nastran file."""
        bulk_data = BulkDataSection.empty()

        for line in file_content:
            entry_identifyer = line.strip().split(" ")[0].split(",")[0].strip()

            processed_entry: _BulkDataEntry | None = None
            match entry_identifyer:
                case "CROD":
                    processed_entry = Crod.from_file_content(_split_short_line(line))
                case "FORCE":
                    processed_entry = Force.from_file_content(_split_short_line(line))
                case "GRID":
                    processed_entry = Grid.from_file_content(_split_short_line(line))
                case "MAT1":
                    processed_entry = Mat1.from_file_content(_split_short_line(line))
                case "PROD":
                    processed_entry = Prod.from_file_content(_split_short_line(line))
                case "SPC":
                    processed_entry = Spc.from_file_content(_split_short_line(line))

                case "SOL" | "CEND" | "BEGIN" | "ENDDATA" | "PARAM":
                    pass
                case _:
                    raise EntryIdentifyerNotSupportedError(entry_identifyer)

            if processed_entry is not None:
                bulk_data.entries.append(processed_entry)

        return bulk_data


def _split_short_line(line: str) -> list[str]:
    return [line[i : i + 8] for i in range(0, len(line), 8)]


class EntryIdentifyerNotSupportedError(Exception):
    """Raised when a line starts with an identifyer, that is not in ENTRY_CLASS_MAPPING."""

    def __init__(self, entry_identifyer: str) -> None:
        super().__init__(f"{entry_identifyer} is not a supported entry type.")
