from pathlib import Path

import pytest
from quantio import Pressure

from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Mat1
from nastran_to_kratos.translation_layer.elements import Material


def test_from_nastran():
    mat1 = Mat1(mid=1, e=210_000)

    actual = Material.from_nastran(mat1)
    assert actual == Material(name="Mat1_1", young_modulus=Pressure(gigapascal=210))


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
