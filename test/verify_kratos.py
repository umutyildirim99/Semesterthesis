"""Verify that all kratos simulations are executable."""

from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import json

import KratosMultiphysics as Kratos
from KratosMultiphysics.StructuralMechanicsApplication.structural_mechanics_analysis import (
    StructuralMechanicsAnalysis,
)


def verify_kratos():
    examples_dir = Path(__file__).parent.parent / "examples"
    kratos_paths = examples_dir.glob("**/simulation_parameters.json")

    with TemporaryDirectory() as tmp_dir_str:
        tmp_dir = Path(tmp_dir_str)

        for kratos_path in kratos_paths:
            temp_kratos_path = _copy_simulation_files(kratos_path, tmp_dir)
            with temp_kratos_path.open() as file_input:
                parameters = Kratos.Parameters(file_input.read())

            model = Kratos.Model()
            simulation = StructuralMechanicsAnalysis(model, parameters)
            simulation.Run()


def _copy_simulation_files(kratos_path: Path, tmp_dir: Path) -> None:
    # There is a bug in kratos that looks for the files referenced in simulation_parameters.json
    # in the root directory. This function here is necessary to circumvent this.
    example_dir = kratos_path.parent

    model_source_path = example_dir / "model.mdpa"
    materials_source_path = example_dir / "materials.json"

    model_target_path = tmp_dir / "model.mdpa"
    materials_target_path = tmp_dir / "materials.json"
    kratos_target_path = example_dir / "simulation_parameters.json"

    shutil.copyfile(model_source_path, model_target_path)
    shutil.copyfile(materials_source_path, materials_target_path)

    with kratos_path.open() as f:
        kratos_params = json.load(f)

    kratos_params["solver_settings"]["model_import_settings"]["input_filename"] = str(
        model_target_path.parent / model_target_path.stem
    )
    kratos_params["solver_settings"]["material_import_settings"]["materials_filename"] = str(
        materials_target_path
    )

    with kratos_target_path.open("w") as f:
        json.dump(kratos_params, f, indent=4)

    return kratos_target_path


if __name__ == "__main__":
    verify_kratos()
