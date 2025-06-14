from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .bulk_data import BulkDataSection
from .case_control import CaseControlSection


@dataclass
class NastranSimulation:
    """All data contained in a nastran file."""

    case_control: CaseControlSection = field(default_factory=CaseControlSection.empty)
    bulk_data: BulkDataSection = field(default_factory=BulkDataSection.empty)

    @classmethod
    def from_file_content(cls, file_content: list[str]) -> NastranSimulation:
        """Construct this class from the contents of a nastran file."""
        lines_sorted_by_section: dict[str, list[str]] = {"unassigned": []}

        current_section_id = "unassigned"
        for line in _remove_linebreak_from_file_content(file_content):
            if "Case Control Cards" in line:
                current_section_id = "case_control"
                lines_sorted_by_section[current_section_id] = []

            if "Bulk Data Cards" in line:
                current_section_id = "bulk_data"
                lines_sorted_by_section[current_section_id] = []

            if not _line_should_be_skipped(line):
                lines_sorted_by_section[current_section_id].append(line)

        return NastranSimulation(
            case_control=CaseControlSection.from_file_content(
                lines_sorted_by_section["case_control"]
            ),
            bulk_data=BulkDataSection.from_file_content(lines_sorted_by_section["bulk_data"]),
        )

    @classmethod
    def from_path(cls, path: Path) -> NastranSimulation:
        """Read the contents of a path pointing to a file and construct this class from it."""
        with path.open() as nastran_file:
            return NastranSimulation.from_file_content(nastran_file.readlines())

    def to_file_content(self) -> list[str]:
        """Export this simulation to lines that can be stored in a nastran file."""
        file_content = ["SOL 101", "CEND"]
        file_content.extend(self.case_control.to_file_content())
        file_content.append("BEGIN BULK")
        file_content.extend(self.bulk_data.to_file_content())
        file_content.append("ENDDATA")
        return _add_linebreaks_to_file_content(file_content)


def _remove_linebreak_from_file_content(file_content: list[str]) -> list[str]:
    stripped_file_content = []
    for line in file_content:
        if line.endswith("\n"):
            stripped_file_content.append(line[:-1])
        else:
            stripped_file_content.append(line)

    return stripped_file_content


def _add_linebreaks_to_file_content(file_content: list[str]) -> list[str]:
    return [line + "\n" for line in file_content]


def _line_should_be_skipped(line: str) -> bool:
    line_is_empty = line == ""
    line_is_a_comment = line.startswith("$")

    return line_is_empty or line_is_a_comment
