from __future__ import annotations

from dataclasses import dataclass

from ._nastran_entry import _NastranEntry
from .crod import Crod
from .grid import Grid

ENTRY_CLASS_MAPPING: dict[str, type[_NastranEntry]] = {
    "GRID": Grid,
    "CROD": Crod,
}


@dataclass
class NastranSimulation:
    """All relevant contents of a nastran file."""

    entries: list[_NastranEntry]

    @classmethod
    def empty(cls) -> NastranSimulation:
        """Construct an empty NastranSimulation instance."""
        return NastranSimulation(entries=[])

    @classmethod
    def from_file_content(cls, file_content: list[str]) -> NastranSimulation:
        """Construct this class from the contents of a nastran file."""
        simulation = NastranSimulation.empty()

        for line in file_content:
            if _line_should_be_ignored(line):
                continue

            line_split_into_fields = [line[i : i + 8] for i in range(0, len(line), 8)]

            entry_class = ENTRY_CLASS_MAPPING[line_split_into_fields[0].strip()]
            simulation.entries.append(entry_class.read(line_split_into_fields))

        return simulation


def _line_should_be_ignored(line: str) -> bool:
    """Return wether a given line should be skipped (e.g. if it is a comment)."""
    if line == "":
        return True

    if line.startswith(("$", "SOL", "CEND", "BEGIN", "ENDDATA")):
        return True

    return False
