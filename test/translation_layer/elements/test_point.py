from pathlib import Path

import pytest
from quantio import Length

from nastran_to_kratos.nastran.bulk_data.entries import Grid
from nastran_to_kratos.translation_layer.elements import Point


def test_from_nastran():
    grid = Grid(id=1, x1=1000, x2=2000, x3=3000)

    actual = Point.from_nastran(grid)
    assert actual == Point(x=Length(meters=3), y=Length(meters=2), z=Length(meters=1))


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
