from pathlib import Path

import pytest
from quantio import Area, Pressure

from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Crod, Prod, Mat1
from nastran_to_kratos.translation_layer.elements.connector import (
    Truss,
    trusses_from_nastran,
    Material,
)


def test_truss_from_nastran():
    crod = Crod(eid=1, pid=1, g1=2, g2=3)
    prod = Prod(pid=1, mid=0, a=350.0)
    mat1 = Mat1(mid=0, e=210_000)

    actual = Truss.from_nastran(crod, prod, mat1)
    assert actual == Truss(
        first_point_index=2,
        second_point_index=3,
        cross_section=Area(square_millimeters=350.0),
        material=Material(name="Mat1_0", young_modulus=Pressure(megapascal=210_000)),
    )


def test_truss_from_nastran__pid_does_not_match():
    crod = Crod(eid=1, pid=1, g1=2, g2=3)
    prod = Prod(pid=5, mid=0, a=350.0)
    mat1 = Mat1(mid=0, e=210_000)

    with pytest.raises(KeyError):
        Truss.from_nastran(crod, prod, mat1)


def test_truss_from_nastran__mid_does_not_match():
    crod = Crod(eid=1, pid=5, g1=2, g2=3)
    prod = Prod(pid=5, mid=0, a=350.0)
    mat1 = Mat1(mid=20, e=210_000)

    with pytest.raises(KeyError):
        Truss.from_nastran(crod, prod, mat1)


def test_trusses_from_nastran__two_trusses():
    crod1 = Crod(eid=1, pid=1, g1=5, g2=6)
    prod1 = Prod(pid=1, mid=0, a=400)
    crod2 = Crod(eid=2, pid=2, g1=7, g2=8)
    prod2 = Prod(pid=2, mid=0, a=900)
    mat1 = Mat1(mid=0, e=210_000)
    bulk_data = BulkDataSection(entries=[crod1, crod2, prod1, prod2, mat1])

    actual = trusses_from_nastran(bulk_data)
    assert actual == [
        Truss.from_nastran(crod1, prod1, mat1),
        Truss.from_nastran(crod2, prod2, mat1),
    ]


def test_trusses_from_nastran__ignore_leftover_prod():
    crod1 = Crod(eid=1, pid=1, g1=5, g2=6)
    prod1 = Prod(pid=1, mid=0, a=400)
    prod2 = Prod(pid=2, mid=0, a=900)
    mat1 = Mat1(mid=0, e=210_000)
    bulk_data = BulkDataSection(entries=[crod1, prod1, prod2, mat1])

    actual = trusses_from_nastran(bulk_data)
    assert actual == [Truss.from_nastran(crod1, prod1, mat1)]


def test_trusses_from_nastran__raise_error_for_missing_prod():
    crod1 = Crod(eid=1, pid=1, g1=5, g2=6)
    mat1 = Mat1(mid=0, e=210_000)
    bulk_data = BulkDataSection(entries=[crod1, mat1])

    with pytest.raises(KeyError):
        trusses_from_nastran(bulk_data)


def test_trusses_from_nastran__raise_error_for_missing_mat1():
    crod1 = Crod(eid=1, pid=1, g1=5, g2=6)
    prod1 = Prod(pid=1, mid=0, a=400)
    bulk_data = BulkDataSection(entries=[crod1, prod1])

    with pytest.raises(KeyError):
        trusses_from_nastran(bulk_data)


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
