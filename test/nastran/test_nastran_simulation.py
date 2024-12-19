from pathlib import Path

import pytest

from nastran_to_kratos.nastran import NastranSimulation
from nastran_to_kratos.nastran.case_control import (
    Analysis,
    CaseControlSection,
    Displacement,
    Strain,
    Stress,
    Subcase,
)
from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Crod, Force, Grid, Mat1, Prod, Spc


@pytest.fixture
def x_movable_rod() -> NastranSimulation:
    return NastranSimulation(
        case_control=CaseControlSection(
            general=Subcase(
                analysis=Analysis.STATICS,
                displacement=Displacement.ALL,
                strain=Strain.ALL,
                stress=Stress.ALL,
            ),
            subcases={
                1: Subcase(
                    subtitle="LS_xForce",
                    label="LS_xForce",
                    spc=2,
                    load=1,
                    analysis=Analysis.STATICS,
                )
            },
        ),
        bulk_data=BulkDataSection(
            entries=[
                Grid(id=1, cp=None, x1=0.0, x2=0.0, x3=0.0),
                Grid(id=2, cp=None, x1=1000.0, x2=0.0, x3=0.0),
                Crod(eid=1, pid=1, g1=1, g2=2),
                Prod(pid=1, mid=1, a=350.0),
                Mat1(mid=1, e=210000.0, g=0.3),
                Spc(sid=2, g1=1, c1=12345, d1=0.0, g2=None, c2=None, d2=None),
                Spc(sid=2, g1=2, c1=2345, d1=0.0, g2=None, c2=None, d2=None),
                Force(sid=1, g=2, cid=0, f=40000.0, n1=1.0, n2=0.0, n3=0.0),
            ]
        ),
    )


@pytest.fixture
def x_movable_rod_path() -> Path:
    return Path(__file__).parent.parent.parent / "examples" / "x_movable_rod.bdf"


def read_file(path: Path) -> list[str]:
    with path.open() as f:
        file_content = f.readlines()
    return file_content


def test_from_path__x_movable_rod(x_movable_rod, x_movable_rod_path):
    actual = NastranSimulation.from_path(x_movable_rod_path)
    assert actual == x_movable_rod


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
