from pathlib import Path

import pytest

from nastran_to_kratos.kratos.kratos_simulation import KratosSimulation, SimulationParameters
from nastran_to_kratos.kratos.simulation_parameters import Constraint as KratosConstraint
from nastran_to_kratos.kratos.simulation_parameters import Load as KratosLoad
from nastran_to_kratos.nastran import NastranSimulation
from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Spc, Mat1, Grid, Crod, Prod, Force
from nastran_to_kratos.translation_layer import TranslationLayer
from nastran_to_kratos.translation_layer.constraints import Constraint
from nastran_to_kratos.translation_layer.loads import Load
from nastran_to_kratos.translation_layer.elements import Element, elements_from_nastran, Point


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


def test_from_nastran__loads():
    force1 = Force(sid=0, g=1, cid=1, f=40_000, n1=1.0, n2=0.0, n3=0.0)
    force2 = Force(sid=0, g=1, cid=1, f=20_000, n1=0.0, n2=1.0, n3=0.0)
    nastran = NastranSimulation(bulk_data=BulkDataSection([force1, force2]))

    actual = TranslationLayer.from_nastran(nastran)
    assert actual.loads == [Load.from_nastran(force1), Load.from_nastran(force2)]


def test_to_kratos__simulation_parameters():
    translation_layer = TranslationLayer(
        elements=[Element(nodes=[Point(0, 0, 0)])],
        constraints=[
            Constraint(
                node_id=0,
                translation_by_axis=(True, True, True),
                rotation_by_axis=(False, False, False),
            )
        ],
        loads=[Load(node_id=0, modulus=40_000, direction=(1, 0, 0))],
    )

    actual = translation_layer.to_kratos()
    assert actual.parameters == SimulationParameters(
        constraints=[
            KratosConstraint(
                model_part_name="element_0",
                constrained_per_axis=(True, True, True),
                value_per_axis=(0, 0, 0),
            )
        ],
        loads=[KratosLoad(model_part_name="element_0", modulus=40_000, direction=(1, 0, 0))],
    )


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
