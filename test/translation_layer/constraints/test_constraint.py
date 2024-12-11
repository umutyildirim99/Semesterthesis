from pathlib import Path

import pytest
from quantio import Area

from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Spc
from nastran_to_kratos.translation_layer.constraints import Constraint


def test_from_nastran__all_movement_constraint():
    spc = Spc(sid=1, g1=2, c1=123456)

    actual = Constraint.from_nastran(spc)
    assert actual == Constraint(
        node_id=2,
        translation_by_axis=(True, True, True),
        rotation_by_axis=(True, True, True),
    )


def test_from_nastran__not_all_movement_constraint():
    spc = Spc(sid=1, g1=2, c1=246)

    actual = Constraint.from_nastran(spc)
    assert actual == Constraint(
        node_id=2,
        translation_by_axis=(False, True, False),
        rotation_by_axis=(True, False, True),
    )


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
