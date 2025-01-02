from pathlib import Path

from .kratos import KratosSimulation
from .translation_layer import TranslationLayer


def kratos_to_nastran(kratos_directory: Path, output_file: Path) -> None:
    """Convert a simulation in the kratos format into nastran."""
    kratos = KratosSimulation.from_directory(kratos_directory)
    translation_layer = TranslationLayer.from_kratos(kratos)
    nastran = translation_layer.to_nastran()

    with output_file.open("w") as file_:
        file_.writelines(nastran.to_file_content())
