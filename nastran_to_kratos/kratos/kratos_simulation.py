from dataclasses import dataclass
from pathlib import Path

from .model import Model


@dataclass
class KratosSimulation:
    """All data for writing kratos simulation files."""

    model: Model

    def write_to_directory(self, output_dir: Path) -> None:
        """Store the simulation as files in an output directory."""
        if not output_dir.is_dir():
            output_dir.mkdir()

        with (output_dir / "model.mdpa").open("w") as model_file:
            model_file.writelines(_add_line_break_to_every_line(self.model.to_mdpa()))


def _add_line_break_to_every_line(lines: list[str]) -> list[str]:
    for i in range(len(lines)):
        if lines[i].endswith("\n"):
            continue
        lines[i] += "\n"
    return lines
