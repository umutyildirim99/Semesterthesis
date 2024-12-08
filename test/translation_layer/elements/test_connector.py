from pathlib import Path

import pytest
from quantio import Area

from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Crod, Prod
from nastran_to_kratos.translation_layer.elements import Truss


def test_truss_from_nastran():
    crod = Crod(eid=1, pid=1, g1=2, g2=3)
    prod = Prod(pid=1, mid=0, a=350.0)

    actual = Truss.from_nastran(crod, prod)
    assert actual == Truss(
        first_point_id=2, seconds_point_id=3, cross_section=Area(square_millimeters=350.0)
    )


def test_truss_from_nastran__pid_does_not_match():
    crod = Crod(eid=1, pid=1, g1=2, g2=3)
    prod = Prod(pid=5, mid=0, a=350.0)

    with pytest.raises(KeyError):
        Truss.from_nastran(crod, prod)


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
