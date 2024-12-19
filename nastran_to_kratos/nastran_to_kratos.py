from pathlib import Path

from .nastran import NastranSimulation
from .translation_layer import TranslationLayer


def nastran_to_kratos(nastran_input: Path, output_dir: Path) -> None:
    """Convert a simulation in the nastran format into kratos."""
    with nastran_input.open() as nastran_file:
        nastran_file_content = nastran_file.readlines()

    nastran = NastranSimulation.from_file_content(nastran_file_content)
    translation_layer = TranslationLayer.from_nastran(nastran)
    kratos = translation_layer.to_kratos()

    kratos.write_to_directory(output_dir)
