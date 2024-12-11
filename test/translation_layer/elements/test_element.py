from pathlib import Path

import pytest
from quantio import Pressure

from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Mat1, Grid, Crod, Prod
from nastran_to_kratos.translation_layer.elements import Element, Point, Material, Truss


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


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
