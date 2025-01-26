from pathlib import Path

from .kratos import KratosSimulation
from .translation_layer import TranslationLayer


def kratos_to_nastran(kratos_directory: Path | str, output_file: Path | str) -> None:
    """Convert a simulation in the kratos format into nastran.

    Args:
        kratos_directory : Directory containing the kratos simulation files. The directory must
            contain the files `material.json`, `model.mdpa` and `simulation_parameters.json`
        output_file : The path to the target file of the nastran simulation.

    Example:
    ```python
    from nastran_to_kratos import kratos_to_nastran

    kratos_to_nastran("/path/to/kratos", "/path/to/output/file.bdf")
    ```
    """
    kratos_directory = Path(kratos_directory)
    output_file = Path(output_file)

    kratos = KratosSimulation.from_directory(kratos_directory)
    translation_layer = TranslationLayer.from_kratos(kratos)
    nastran = translation_layer.to_nastran()

    with output_file.open("w") as file_:
        file_.writelines(nastran.to_file_content())
