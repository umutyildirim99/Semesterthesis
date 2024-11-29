import json
from dataclasses import dataclass
from pathlib import Path

from .material import Material
from .model import Model


@dataclass
class KratosSimulation:
    """All data for writing kratos simulation files."""

    model: Model | None = None
    "The model used in the simulation."

    materials: list[Material] | None = None
    "The materials for each model part."

    def write_to_directory(self, output_dir: Path) -> None:
        """Store the simulation as files in an output directory."""
        if not output_dir.is_dir():
            output_dir.mkdir()

        _write_model_file(self.model, output_dir / "model.mdpa")
        _write_materials_file(self.materials, output_dir / "materials.json")


def _write_model_file(model: Model | None, path: Path) -> None:
    if model is None:
        return
    with path.open("w") as model_file:
        model_file.writelines(_add_line_break_to_every_line(model.to_mdpa()))


def _write_materials_file(materials: list[Material] | None, path: Path) -> None:
    if materials is None:
        return

    materials_dict = {"properties": [material.to_json() for material in materials]}

    with path.open("w") as materials_file:
        json.dump(materials_dict, materials_file)


def _add_line_break_to_every_line(lines: list[str]) -> list[str]:
    for i in range(len(lines)):
        if lines[i].endswith("\n"):
            continue
        lines[i] += "\n"
    return lines
