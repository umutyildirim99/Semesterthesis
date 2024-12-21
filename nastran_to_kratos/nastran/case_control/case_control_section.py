from __future__ import annotations

from dataclasses import dataclass

from .subcase import Subcase


@dataclass
class CaseControlSection:
    """The Case Control Section has several basic functions.

    Specifically it:
        - Selects loads and constraints.
        - Requests printing, plotting, and/or punching of input and out data.
        - Defines the subcase structure for the analysis.
    """

    general: Subcase
    subcases: dict[int, Subcase]

    @classmethod
    def empty(cls) -> CaseControlSection:
        """Construct a minimal instance of this class."""
        return CaseControlSection(general=Subcase.empty(), subcases={})

    @classmethod
    def from_file_content(cls, file_content: list[str]) -> CaseControlSection:
        """Construct this class from the contents of a nastran file."""
        case_control_section = CaseControlSection.empty()

        subcase_lines_with_general: dict[int, list[str]] = {0: []}
        current_subcase_id = 0
        for line in file_content:
            if line.startswith("SUBCASE"):
                current_subcase_id = int(line.split(" ")[-1].strip())
                subcase_lines_with_general[current_subcase_id] = []
                continue

            subcase_lines_with_general[current_subcase_id].append(line)

        for subcase_id, subcase in subcase_lines_with_general.items():
            if subcase_id == 0:
                case_control_section.general = Subcase.from_file_content(subcase)
            else:
                case_control_section.subcases[subcase_id] = Subcase.from_file_content(subcase)

        return case_control_section

    def to_file_content(self) -> list[str]:
        """Export this section into lines for saving to a nastran file."""
        file_content = self.general.to_file_content()
        for case_id, case in self.subcases.items():
            file_content.append(f"SUBCASE{_leftpad8(case_id)}")
            file_content.extend(case.to_file_content())
        return file_content


def _leftpad8(s: str | int) -> str:
    return str(s).rjust(8, " ")
