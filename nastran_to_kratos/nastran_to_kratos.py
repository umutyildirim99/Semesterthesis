from pathlib import Path

from .nastran import NastranSimulation
from .translation_layer import TranslationLayer


def nastran_to_kratos(nastran_input: Path | str, output_dir: Path | str) -> None:
    """Convert a simulation in the nastran format into kratos.

    Args:
        nastran_input : The path to the nastran file (usually ending with .bdf)
        output_dir : The path to the directory where the kratos files should be saved (must have
            write permission).

    Example:
    ```python
    from nastran_to_kratos import nastran_to_kratos

    nastran_to_kratos("/path/to/nastran.bdf", "/path/to/output/dir")
    ```
    """
    nastran_input = Path(nastran_input)
    output_dir = Path(output_dir)

    with nastran_input.open() as nastran_file:
        nastran_file_content = nastran_file.readlines()

    nastran = NastranSimulation.from_file_content(nastran_file_content)
    translation_layer = TranslationLayer.from_nastran(nastran)
    kratos = translation_layer.to_kratos()

    kratos.write_to_directory(output_dir)
