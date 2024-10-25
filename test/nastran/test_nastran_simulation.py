from nastran_to_kratos.nastran.nastran_simulation import (
    NastranSimulation,
    EntryIdentifyerNotSupportedError,
)
from nastran_to_kratos.nastran.grid import Grid
from nastran_to_kratos.nastran.crod import Crod

import pytest


def test_from_file_content__multiple_entries():
    file_content = [
        "GRID           2          1000.0     0.0     0.0",
        "GRID           2       5  1000.0     0.0     2.0       3     123       7",
    ]

    actual = NastranSimulation.from_file_content(file_content)
    assert len(actual.entries) == 2


def test_from_file_content__unsupported_entry():
    file_content = ["BADWORD "]

    with pytest.raises(EntryIdentifyerNotSupportedError):
        NastranSimulation.from_file_content(file_content)


def test_from_file_content__grid_entry():
    file_content = ["GRID           2          1000.0     0.0     0.0"]

    actual = NastranSimulation.from_file_content(file_content)
    assert actual.entries == [
        Grid.read(["GRID    ", "       2", "        ", "  1000.0", "     0.0", "     0.0"])
    ]


def test_from_file_content__crod_entry():
    file_content = ["CROD          12      13      21      23"]

    actual = NastranSimulation.from_file_content(file_content)
    assert actual.entries == [
        Crod.read(["CROD    ", "      12", "      13", "      21", "      23"])
    ]


def test_from_file_content__ignore_dollar_signs():
    file_content = ["$GRID          2          1000.0     0.0     0.0"]

    actual = NastranSimulation.from_file_content(file_content)
    assert actual == NastranSimulation.empty()


def test_from_file_content__ignore_empty_lines():
    file_content = [""]

    actual = NastranSimulation.from_file_content(file_content)
    assert actual == NastranSimulation.empty()


def test_from_file_content__ignore_sol():
    file_content = ["SOL 101"]

    actual = NastranSimulation.from_file_content(file_content)
    assert actual == NastranSimulation.empty()


def test_from_file_content__ignore_cend():
    file_content = ["CEND"]

    actual = NastranSimulation.from_file_content(file_content)
    assert actual == NastranSimulation.empty()


def test_from_file_content__ignore_begin():
    file_content = ["BEGIN"]

    actual = NastranSimulation.from_file_content(file_content)
    assert actual == NastranSimulation.empty()


def test_from_file_content__ignore_enddata():
    file_content = ["ENDDATA"]

    actual = NastranSimulation.from_file_content(file_content)
    assert actual == NastranSimulation.empty()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
