from nastran_to_kratos.nastran.nastran_simulation import NastranSimulation
from nastran_to_kratos.nastran.grid import Grid

import pytest


def test_from_file_content__one_grid_entry():
    file_content = ["GRID           2          1000.0     0.0     0.0"]

    actual = NastranSimulation.from_file_content(file_content)
    assert actual.entries == [
        Grid.read(["GRID    ", "       2", "        ", "  1000.0", "     0.0", "     0.0"])
    ]


def test_from_file_content__two_grid_entries():
    file_content = [
        "GRID           2          1000.0     0.0     0.0",
        "GRID           2       5  1000.0     0.0     2.0       3     123       7",
    ]

    actual = NastranSimulation.from_file_content(file_content)
    assert len(actual.entries) == 2


def test_from_file_content__ignore_dollar_signs():
    file_content = ["$GRID          2          1000.0     0.0     0.0"]

    actual = NastranSimulation.from_file_content(file_content)
    assert actual.entries == []


def test_from_file_content__ignore_empty_lines():
    file_content = [""]

    actual = NastranSimulation.from_file_content(file_content)
    assert actual.entries == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
