from pathlib import Path

import pytest
from quantio import Area

from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Force
from nastran_to_kratos.translation_layer.loads import Load


def test_from_nastran():
    force = Force(sid=0, g=1, cid=1, f=40_000, n1=1.0, n2=0.0, n3=0.0)

    actual = Load.from_nastran(force)
    assert actual == Load(
        node_id=1,
        modulus=40_000,
        direction=(1.0, 0.0, 0.0),
    )


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
