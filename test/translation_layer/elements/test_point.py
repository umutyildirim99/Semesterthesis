from pathlib import Path

import pytest
from quantio import Length

from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Grid
from nastran_to_kratos.translation_layer import Point, nodes_from_nastran


def test_from_nastran():
    grid = Grid(id=1, x1=1000, x2=2000, x3=3000)

    actual = Point.from_nastran(grid)
    assert actual == Point(id=1, x=Length(meters=1), y=Length(meters=2), z=Length(meters=3))


def test_nodes_from_nastran__two_consecutive_points():
    grid1 = Grid(id=1, x1=1000, x2=2000, x3=3000)
    grid2 = Grid(id=2, x1=1100, x2=2100, x3=3100)
    bulk_data = BulkDataSection(entries=[grid1, grid2])

    actual = nodes_from_nastran(bulk_data)
    assert actual == [Point.from_nastran(grid1), Point.from_nastran(grid2)]


def test_nodes_from_nastran__wrong_order():
    grid1 = Grid(id=2, x1=1000, x2=2000, x3=3000)
    grid2 = Grid(id=1, x1=1100, x2=2100, x3=3100)
    bulk_data = BulkDataSection(entries=[grid1, grid2])

    actual = nodes_from_nastran(bulk_data)
    assert actual == [Point.from_nastran(grid2), Point.from_nastran(grid1)]


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
