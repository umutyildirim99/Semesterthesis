import json
from dataclasses import dataclass
from pathlib import Path

from .material import KratosMaterial
from .model import Model
from .simulation_parameters import SimulationParameters


@dataclass
class KratosSimulation:
    """All data for writing kratos simulation files."""

    parameters: SimulationParameters | None = None
    "Main container of simulation configuration."

    model: Model | None = None
    "The model used in the simulation."

    materials: list[KratosMaterial] | None = None
    "The materials for each model part."

    def write_to_directory(self, output_dir: Path) -> None:
        """Store the simulation as files in an output directory."""
        if not output_dir.is_dir():
            output_dir.mkdir()

        _write_parameters_file(self.parameters, output_dir / "simulation_parameters.json")
        _write_model_file(self.model, output_dir / "model.mdpa")
        _write_materials_file(self.materials, output_dir / "materials.json")


def _write_model_file(model: Model | None, path: Path) -> None:
    if model is None:
        return
    with path.open("w") as model_file:
        model_file.writelines(_add_line_break_to_every_line(model.to_mdpa()))


def _write_materials_file(materials: list[KratosMaterial] | None, path: Path) -> None:
    if materials is None:
        return

    materials_dict = {"properties": [material.to_json() for material in materials]}

    with path.open("w") as materials_file:
        json.dump(materials_dict, materials_file)


def _write_parameters_file(parameters: SimulationParameters | None, path: Path) -> None:
    if parameters is None:
        return
    with path.open("w") as parameters_file:
        json.dump(parameters.to_json(), parameters_file)


def _add_line_break_to_every_line(lines: list[str]) -> list[str]:
    for i in range(len(lines)):
        if lines[i].endswith("\n"):
            continue
        lines[i] += "\n"
    return lines
