from nastran_to_kratos.nastran.bulk_data import (
    BulkDataSection,
    EntryIdentifyerNotSupportedError,
)
from nastran_to_kratos.nastran.bulk_data.entries import Grid, Crod, Prod, Force, Spc

import pytest


def test_from_file_content__multiple_entries():
    file_content = [
        "GRID           2          1000.0     0.0     0.0",
        "GRID           2       5  1000.0     0.0     2.0       3     123       7",
    ]

    actual = BulkDataSection.from_file_content(file_content)
    assert len(actual.entries) == 2


def test_from_file_content__unsupported_entry():
    file_content = ["BADWORD "]

    with pytest.raises(EntryIdentifyerNotSupportedError):
        BulkDataSection.from_file_content(file_content)


def test_from_file_content__grid_entry():
    file_content = ["GRID           2          1000.0     0.0     0.0"]

    actual = BulkDataSection.from_file_content(file_content)
    assert actual.entries == [
        Grid.from_file_content(
            ["GRID    ", "       2", "        ", "  1000.0", "     0.0", "     0.0"]
        )
    ]


def test_from_file_content__crod_entry():
    file_content = ["CROD          12      13      21      23"]

    actual = BulkDataSection.from_file_content(file_content)
    assert actual.entries == [
        Crod.from_file_content(["CROD    ", "      12", "      13", "      21", "      23"])
    ]


def test_from_file_content__prod_entry():
    file_content = ["PROD          17      23    42.6   17.92  4.2356     0.5"]

    actual = BulkDataSection.from_file_content(file_content)
    assert actual.entries == [
        Prod.from_file_content(["PROD", "17", "23", "42.6", "17.92", "4.2356", "0.5"])
    ]


def test_from_file_content__force_entry():
    file_content = ["FORCE       2       5       6     2.9     0.0     1.0     0.0"]

    actual = BulkDataSection.from_file_content(file_content)
    assert actual.entries == [
        Force.from_file_content(["FORCE", "2", "5", "6", "2.9", "0.0", "1.0", "0.0"])
    ]


def test_from_file_content__spc_entry():
    file_content = ["SPC            2      32       3    -2.6      33       4    -1.6"]

    actual = BulkDataSection.from_file_content(file_content)
    assert actual.entries == [
        Spc.from_file_content(["SPC", "2", "32", "3", "-2.6", "33", "4", "-1.6"])
    ]


def test_from_file_content__ignore_sol():
    file_content = ["SOL 101"]

    actual = BulkDataSection.from_file_content(file_content)
    assert actual == BulkDataSection.empty()


def test_from_file_content__ignore_cend():
    file_content = ["CEND"]

    actual = BulkDataSection.from_file_content(file_content)
    assert actual == BulkDataSection.empty()


def test_from_file_content__ignore_begin():
    file_content = ["BEGIN"]

    actual = BulkDataSection.from_file_content(file_content)
    assert actual == BulkDataSection.empty()


def test_from_file_content__ignore_enddata():
    file_content = ["ENDDATA"]

    actual = BulkDataSection.from_file_content(file_content)
    assert actual == BulkDataSection.empty()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
