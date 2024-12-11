from pathlib import Path

import pytest

from nastran_to_kratos.nastran import NastranSimulation
from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Mat1, Grid, Crod, Prod
from nastran_to_kratos.translation_layer import TranslationLayer
from nastran_to_kratos.translation_layer.elements import (
    elements_from_nastran,
)


def test_from_nastran__elements():
    mat1 = Mat1(mid=1)
    grid1 = Grid(id=2)
    grid2 = Grid(id=3)
    crod = Crod(eid=4, pid=5, g1=2, g2=3)
    prod = Prod(pid=5, mid=1, a=350.0)
    nastran = NastranSimulation(BulkDataSection([mat1, grid1, grid2, crod, prod]))

    actual = TranslationLayer.from_nastran(nastran)
    assert actual == TranslationLayer(elements=elements_from_nastran(nastran.bulk_data))


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
