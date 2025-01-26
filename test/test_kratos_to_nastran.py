import json
from pathlib import Path

import pytest

from nastran_to_kratos import kratos_to_nastran


def read_json(path: Path) -> dict:
    with path.open() as f:
        json_content = json.load(f)
    return json_content


def read_file(path: Path) -> list[str]:
    with path.open() as f:
        file_content = f.readlines()
    return file_content


def remove_unimportant_lines(lines: list[str]) -> list[str]:
    important_lines = []
    for line in lines:
        if line in ("", "\n"):
            continue
        if line.startswith(("$", "PARAM")):
            continue
        important_lines.append(line)
    return important_lines


def test_integration__x_movable_rod(tmp_path):
    x_movable_rod_dir = Path(__file__).parent.parent / "examples" / "x_movable_rod"
    output_file = tmp_path / "x_movable_rod.bdf"

    kratos_to_nastran(x_movable_rod_dir / "kratos", output_file)

    ground_truth = remove_unimportant_lines(
        read_file(x_movable_rod_dir / "nastran" / "x_movable_rod.bdf")
    )
    actual = remove_unimportant_lines(read_file(output_file))
    p = str(tmp_path)
    assert actual


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
