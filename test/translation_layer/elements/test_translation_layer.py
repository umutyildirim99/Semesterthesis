from pathlib import Path

import pytest
from quantio import Area, Pressure, Length

from nastran_to_kratos.kratos.kratos_simulation import KratosSimulation
from nastran_to_kratos.kratos.material import KratosMaterial
from nastran_to_kratos.kratos.model import Model, Node, Condition, SubModel
from nastran_to_kratos.kratos.model import Element as KratosElement
from nastran_to_kratos.kratos.simulation_parameters import (
    KratosConstraint,
    KratosLoad,
    SimulationParameters,
)
from nastran_to_kratos.nastran import NastranSimulation
from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Spc, Mat1, Grid, Crod, Prod, Force
from nastran_to_kratos.translation_layer import (
    TranslationLayer,
    Constraint,
    Truss,
    Point,
    Load,
    nodes_from_nastran,
    trusses_from_nastran,
    Material,
)


def test_from_nastran__nodes():
    grid1 = Grid(id=1, x1=500, x2=1000, x3=2000)
    grid2 = Grid(id=2, x1=200, x2=400, x3=800)
    nastran = NastranSimulation(bulk_data=BulkDataSection([grid1, grid2]))

    actual = TranslationLayer.from_nastran(nastran)
    assert actual.nodes == nodes_from_nastran(nastran.bulk_data)


def test_from_nastran__connectors():
    grid1 = Grid(id=1)
    grid2 = Grid(id=2)
    grid3 = Grid(id=3)
    crod1 = Crod(eid=5, pid=1, g1=1, g2=2)
    crod2 = Crod(eid=6, pid=1, g1=2, g2=3)
    prod1 = Prod(pid=1, mid=1, a=350)
    mat1 = Mat1(mid=1, e=210_000)
    nastran = NastranSimulation(
        bulk_data=BulkDataSection([grid1, grid2, grid3, crod1, crod2, prod1, mat1])
    )

    actual = TranslationLayer.from_nastran(nastran)
    assert actual.connectors == trusses_from_nastran(nastran.bulk_data)


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


def test_to_kratos__model():
    translation_layer = TranslationLayer(
        nodes=[
            Point.origin(1),
            Point(2, Length(meters=1), Length.zero(), Length.zero()),
        ],
        connectors=[
            Truss(
                first_point_index=1,
                second_point_index=2,
                cross_section=Area.zero(),
                material=Material(),
            )
        ],
        constraints=[
            Constraint(
                node_id=1,
                translation_by_axis=(True, True, True),
                rotation_by_axis=(False, False, False),
            ),
            Constraint(
                node_id=2,
                translation_by_axis=(False, True, True),
                rotation_by_axis=(False, False, False),
            ),
        ],
        loads=[Load(node_id=1, modulus=40_000, direction=(1, 0, 0))],
    )

    actual = translation_layer.to_kratos()
    assert actual.model == Model(
        properties={0: {}},
        nodes={1: Node(0, 0, 0), 2: Node(1000, 0, 0)},
        elements={"TrussLinearElement3D2N": {1: KratosElement(property_id=0, node_ids=[1, 2])}},
        conditions={"PointLoadCondition2D1N": {1: Condition(property_id=0, node_ids=[1])}},
        sub_models={
            "truss_1": SubModel(nodes=[1, 2], elements=[1]),
            "constraint_1": SubModel(nodes=[1]),
            "constraint_2": SubModel(nodes=[2]),
            "load_1": SubModel(nodes=[1], conditions=[1]),
        },
    )


def test_to_kratos__materials():
    translation_layer = TranslationLayer(
        nodes=[Point.origin(1), Point.origin(2)],
        connectors=[
            Truss(
                first_point_index=1,
                second_point_index=2,
                cross_section=Area(square_millimeters=35),
                material=Material(name="Steel", young_modulus=Pressure(gigapascal=210)),
            ),
            Truss(
                first_point_index=1,
                second_point_index=2,
                cross_section=Area(square_millimeters=50),
                material=Material(name="Steel", young_modulus=Pressure(gigapascal=210)),
            ),
            Truss(
                first_point_index=1,
                second_point_index=1,
                cross_section=Area(square_millimeters=22),
                material=Material(name="Aluminum", young_modulus=Pressure(gigapascal=69)),
            ),
        ],
    )

    actual = translation_layer.to_kratos()
    assert actual.materials == [
        KratosMaterial(
            model_part_name="Structure.truss_1",
            properties_id=0,
            material_name="Steel",
            constitutive_law="TrussConstitutiveLaw",
            variables={
                "YOUNG_MODULUS": 210_000,
                "CROSS_AREA": 35,
                "DENSITY": 0,
            },
        ),
        KratosMaterial(
            model_part_name="Structure.truss_2",
            properties_id=0,
            material_name="Steel",
            constitutive_law="TrussConstitutiveLaw",
            variables={
                "YOUNG_MODULUS": 210_000,
                "CROSS_AREA": 50,
                "DENSITY": 0,
            },
        ),
        KratosMaterial(
            model_part_name="Structure.truss_3",
            properties_id=0,
            material_name="Aluminum",
            constitutive_law="TrussConstitutiveLaw",
            variables={
                "YOUNG_MODULUS": 69_000,
                "CROSS_AREA": 22,
                "DENSITY": 0,
            },
        ),
    ]


def test_to_kratos__simulation_parameters():
    translation_layer = TranslationLayer(
        nodes=[Point.origin(1)],
        constraints=[
            Constraint(
                node_id=1,
                translation_by_axis=(True, True, True),
                rotation_by_axis=(False, False, False),
            )
        ],
        loads=[Load(node_id=1, modulus=40_000, direction=(1, 0, 0))],
    )

    actual = translation_layer.to_kratos()
    assert actual.parameters == SimulationParameters(
        constraints=[
            KratosConstraint(
                model_part_name="Structure.constraint_1",
                constrained_per_axis=(True, True, True),
                value_per_axis=(0, 0, 0),
            )
        ],
        loads=[KratosLoad(model_part_name="Structure.load_1", modulus=40_000, direction=(1, 0, 0))],
    )


def test_from_kratos__nodes():
    kratos = KratosSimulation(
        model=Model(
            nodes={1: Node(0, 0, 0), 2: Node(1000, 0, 0)},
        )
    )

    actual = TranslationLayer.from_kratos(kratos)
    assert actual.nodes == [
        Point(
            id=1,
            x=Length(meters=0),
            y=Length(meters=0),
            z=Length(meters=0),
        ),
        Point(
            id=2,
            x=Length(meters=1),
            y=Length(meters=0),
            z=Length(meters=0),
        ),
    ]


def test_from_kratos__connectors():
    kratos = KratosSimulation(
        model=Model(
            elements={"TrussLinearElement3D2N": {1: KratosElement(property_id=0, node_ids=[1, 2])}},
        ),
        materials=[
            KratosMaterial(
                model_part_name="Structure.truss_1",
                properties_id=0,
                material_name="Steel",
                constitutive_law="TrussConstitutiveLaw",
                variables={
                    "YOUNG_MODULUS": 210_000,
                    "CROSS_AREA": 35,
                    "DENSITY": 0,
                },
            )
        ],
    )

    actual = TranslationLayer.from_kratos(kratos)
    assert actual.connectors == [
        Truss(
            first_point_index=1,
            second_point_index=2,
            cross_section=Area(square_millimeters=35),
            material=Material(name="Steel", young_modulus=Pressure(gigapascal=210)),
        )
    ]


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
