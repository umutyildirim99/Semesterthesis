from pathlib import Path

import pytest

from nastran_to_kratos.nastran import NastranSimulation
from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Spc, Mat1, Grid, Crod, Prod
from nastran_to_kratos.translation_layer import TranslationLayer
from nastran_to_kratos.translation_layer.constraints import Constraint
from nastran_to_kratos.translation_layer.elements import Element, elements_from_nastran


def test_from_nastran__elements():
    mat1 = Mat1(mid=1)
    grid1 = Grid(id=2)
    grid2 = Grid(id=3)
    crod = Crod(eid=4, pid=5, g1=2, g2=3)
    prod = Prod(pid=5, mid=1, a=350.0)
    nastran = NastranSimulation(bulk_data=BulkDataSection([mat1, grid1, grid2, crod, prod]))

    actual = TranslationLayer.from_nastran(nastran)
    assert actual.elements == elements_from_nastran(nastran.bulk_data)


def test_from_nastran__constraints():
    spc1 = Spc(sid=1, g1=2, c1=123456)
    spc2 = Spc(sid=2, g1=2, c1=246)
    nastran = NastranSimulation(bulk_data=BulkDataSection([spc1, spc2]))

    actual = TranslationLayer.from_nastran(nastran)
    assert actual.constraints == [Constraint.from_nastran(spc1), Constraint.from_nastran(spc2)]


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
