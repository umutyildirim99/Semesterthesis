import json
from pathlib import Path

import pytest

from nastran_to_kratos import nastran_to_kratos


def read_json(path: Path) -> dict:
    with path.open() as f:
        json_content = json.load(f)
    return json_content


def read_file(path: Path) -> list[str]:
    with path.open() as f:
        file_content = f.readlines()
    return file_content


def test_integration__x_movable_rod(tmp_path):
    output_dir = tmp_path / "x_movable_rod"
    ground_truth_dir = Path(__file__).parent.parent / "examples"
    nastran_input = ground_truth_dir / "x_movable_rod.bdf"

    nastran_to_kratos(nastran_input, output_dir)

    assert read_json(output_dir / "simulation_parameters.json") == read_json(
        ground_truth_dir / "simulation_parameters.json"
    )
    assert read_json(output_dir / "materials.json") == read_json(ground_truth_dir / "materials.json")
    assert read_file(output_dir / "model.mdpa") == read_file(ground_truth_dir / "model.mdpa")


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
