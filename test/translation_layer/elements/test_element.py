from pathlib import Path

import pytest
from quantio import Pressure

from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Mat1, Grid, Crod, Prod
from nastran_to_kratos.translation_layer.elements import (
    Element,
    Point,
    Material,
    Truss,
    elements_from_nastran,
)


def test_from_nastran__one_rod_two_grids():
    mat1 = Mat1(mid=1)
    grid1 = Grid(id=2)
    grid2 = Grid(id=3)
    crod = Crod(eid=4, pid=5, g1=2, g2=3)
    prod = Prod(pid=5, mid=1, a=350.0)

    actual = Element.from_nastran([mat1, grid1, grid2, crod, prod])
    assert actual == Element(
        nodes=[Point.from_nastran(grid1), Point.from_nastran(grid2)],
        connectors=[Truss.from_nastran(crod, prod)],
        material=Material.from_nastran(mat1),
    )


def test_elements_from_data__one_element():
    mat1 = Mat1(mid=1)
    grid1 = Grid(id=2)
    grid2 = Grid(id=3)
    crod = Crod(eid=4, pid=5, g1=2, g2=3)
    prod = Prod(pid=5, mid=1, a=350.0)
    entries = [mat1, grid1, grid2, crod, prod]

    actual = elements_from_nastran(BulkDataSection(entries))
    assert actual == [Element.from_nastran(entries)]


def test_elements_from_data__two_elements():
    mat1 = Mat1(mid=1)

    grid2 = Grid(id=2)
    grid3 = Grid(id=3)
    crod4 = Crod(eid=4, pid=5, g1=2, g2=3)
    prod5 = Prod(pid=5, mid=1, a=350.0)

    grid6 = Grid(id=6)
    grid7 = Grid(id=7)
    crod8 = Crod(eid=8, pid=9, g1=6, g2=7)
    prod9 = Prod(pid=9, mid=1, a=350.0)

    entries_element1 = [mat1, grid2, grid3, crod4, prod5]
    entries_element2 = [mat1, grid6, grid7, crod8, prod9]
    all_entries = entries_element1 + entries_element2

    actual = elements_from_nastran(BulkDataSection(all_entries))
    assert actual == [
        Element.from_nastran(entries_element1),
        Element.from_nastran(entries_element2),
    ]


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
