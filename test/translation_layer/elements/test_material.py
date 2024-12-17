from pathlib import Path

import pytest
from quantio import Pressure

from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Mat1
from nastran_to_kratos.translation_layer import Material, materials_from_nastran
from nastran_to_kratos.kratos.material import KratosMaterial


def test_from_nastran():
    mat1 = Mat1(mid=1, e=210_000)

    actual = Material.from_nastran(mat1)
    assert actual == Material(name="Mat1_1", young_modulus=Pressure(gigapascal=210))


def test_materials_from_nastran__two_consecutive_materials():
    mat1 = Mat1(mid=1, e=210_000)
    mat2 = Mat1(mid=2, e=210_000)

    actual = materials_from_nastran(BulkDataSection(entries=[mat1, mat2]))
    assert actual == [Material.from_nastran(mat1), Material.from_nastran(mat2)]


def test_materials_from_nastran__wrong_order():
    mat1 = Mat1(mid=2, e=210_000)
    mat2 = Mat1(mid=1, e=210_000)

    actual = materials_from_nastran(BulkDataSection(entries=[mat1, mat2]))
    assert actual == [Material.from_nastran(mat2), Material.from_nastran(mat1)]


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
