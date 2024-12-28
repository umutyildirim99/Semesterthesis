from pathlib import Path
import json

import pytest

from nastran_to_kratos.kratos import KratosSimulation
from nastran_to_kratos.kratos.model import Model, Node, Element, Condition, SubModel
from nastran_to_kratos.kratos.material import KratosMaterial
from nastran_to_kratos.kratos.simulation_parameters import (
    KratosConstraint,
    KratosLoad,
    SimulationParameters,
)


@pytest.fixture
def x_movable_rod_path() -> Path:
    return Path(__file__).parent.parent.parent / "examples"


def test_write_to_directory__x_movable_rod__model(tmp_path):
    output_dir = tmp_path / "x_movable_rod"
    ground_truth_path = Path(__file__).parent.parent.parent / "examples" / "model.mdpa"

    kratos_simulation = KratosSimulation(
        model=Model(
            properties={0: {}},
            nodes={1: Node(0.0, 0.0, 0.0), 2: Node(1000.0, 0.0, 0.0)},
            elements={"TrussLinearElement3D2N": {1: Element(0, [1, 2])}},
            conditions={"PointLoadCondition2D1N": {1: Condition(0, [2])}},
            sub_models={
                "truss_1": SubModel(nodes=[1, 2], elements=[1]),
                "constraint_1": SubModel(nodes=[1]),
                "constraint_2": SubModel(nodes=[2]),
                "load_1": SubModel(nodes=[2], conditions=[1]),
            },
        )
    )

    kratos_simulation.write_to_directory(output_dir)
    with (output_dir / "model.mdpa").open() as f:
        actual = f.readlines()

    with ground_truth_path.open() as f:
        ground_truth = f.readlines()

    assert actual == ground_truth


def test_write_to_directory__x_movable_rod__materials(tmp_path):
    output_dir = tmp_path / "x_movable_rod"
    ground_truth_path = Path(__file__).parent.parent.parent / "examples" / "materials.json"

    kratos_simulation = KratosSimulation(
        materials=[
            KratosMaterial(
                model_part_name="Structure.truss_1",
                properties_id=0,
                material_name="MAT1_1",
                constitutive_law="TrussConstitutiveLaw",
                variables={"YOUNG_MODULUS": 210000.0, "DENSITY": 0, "CROSS_AREA": 350},
            )
        ]
    )

    kratos_simulation.write_to_directory(output_dir)
    with (output_dir / "materials.json").open() as f:
        actual = json.load(f)

    with ground_truth_path.open() as f:
        ground_truth = json.load(f)

    assert actual == ground_truth


def test_write_to_directory__x_movable_rod__parameters(tmp_path):
    output_dir = tmp_path / "x_movable_rod"
    ground_truth_path = (
        Path(__file__).parent.parent.parent / "examples" / "simulation_parameters.json"
    )

    kratos_simulation = KratosSimulation(
        parameters=SimulationParameters(
            constraints=[
                KratosConstraint(
                    model_part_name="Structure.constraint_1",
                    constrained_per_axis=(True, True, True),
                    value_per_axis=(0.0, 0.0, 0.0),
                ),
                KratosConstraint(
                    model_part_name="Structure.constraint_2",
                    constrained_per_axis=(False, True, True),
                    value_per_axis=(None, 0.0, 0.0),
                ),
            ],
            loads=[
                KratosLoad(
                    model_part_name="Structure.load_1",
                    modulus=40_000.0,
                    direction=(1.0, 0.0, 0.0),
                )
            ],
        )
    )

    kratos_simulation.write_to_directory(output_dir)
    with (output_dir / "simulation_parameters.json").open() as f:
        actual = json.load(f)

    with ground_truth_path.open() as f:
        ground_truth = json.load(f)

    assert actual == ground_truth


def test_from_directory__x_movable_rod__parameters(x_movable_rod_path):
    actual = KratosSimulation.from_directory(x_movable_rod_path)
    assert actual.parameters == SimulationParameters(
        constraints=[
            KratosConstraint(
                model_part_name="Structure.constraint_1",
                constrained_per_axis=(True, True, True),
                value_per_axis=(0.0, 0.0, 0.0),
            ),
            KratosConstraint(
                model_part_name="Structure.constraint_2",
                constrained_per_axis=(False, True, True),
                value_per_axis=(None, 0.0, 0.0),
            ),
        ],
        loads=[
            KratosLoad(
                model_part_name="Structure.load_1",
                modulus=40_000.0,
                direction=(1.0, 0.0, 0.0),
            )
        ],
    )


def test_from_directory__x_movable_rod__parameters(x_movable_rod_path):
    actual = KratosSimulation.from_directory(x_movable_rod_path)
    assert actual.parameters == SimulationParameters(
        constraints=[
            KratosConstraint(
                model_part_name="Structure.constraint_1",
                constrained_per_axis=(True, True, True),
                value_per_axis=(0.0, 0.0, 0.0),
            ),
            KratosConstraint(
                model_part_name="Structure.constraint_2",
                constrained_per_axis=(False, True, True),
                value_per_axis=(None, 0.0, 0.0),
            ),
        ],
        loads=[
            KratosLoad(
                model_part_name="Structure.load_1",
                modulus=40_000.0,
                direction=(1.0, 0.0, 0.0),
            )
        ],
    )


def test_from_directory__x_movable_rod__materials(x_movable_rod_path):
    actual = KratosSimulation.from_directory(x_movable_rod_path)
    assert actual.materials == [
        KratosMaterial(
            model_part_name="Structure.truss_1",
            properties_id=0,
            material_name="MAT1_1",
            constitutive_law="TrussConstitutiveLaw",
            variables={"YOUNG_MODULUS": 210000.0, "DENSITY": 0, "CROSS_AREA": 350},
        )
    ]


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
