from pathlib import Path
import json

import pytest

from nastran_to_kratos.kratos import KratosSimulation
from nastran_to_kratos.kratos.model import Model, Node, Element, Condition, SubModel
from nastran_to_kratos.kratos.material import Material


def test_write_to_directory__x_movable_rod__model(tmp_path):
    output_dir = tmp_path / "x_movable_rod"
    ground_truth_path = Path(__file__).parent.parent.parent / "examples" / "truss.mdpa"

    kratos_simulation = KratosSimulation(
        model=Model(
            properties={0: {}},
            nodes={1: Node(0.0, 0.0, 0.0), 2: Node(1000.0, 0.0, 0.0)},
            elements={"TrussLinearElement3D2N": {1: Element(0, [1, 2])}},
            conditions={"PointLoadCondition2D1N": {1: Condition(0, [2])}},
            sub_models={
                "Truss": SubModel(nodes=[1, 2], elements=[1]),
                "SPC_Group_Node1": SubModel(nodes=[1]),
                "SPC_Group_Node2": SubModel(nodes=[2]),
                "xForce_Node2": SubModel(nodes=[2], conditions=[1]),
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
    ground_truth_path = Path(__file__).parent.parent.parent / "examples" / "Materials.json"

    kratos_simulation = KratosSimulation(
        materials=[
            Material(
                model_part_name="Structure.Truss",
                properties_id=0,
                material_name="MAT1_1",
                constitutive_law="TrussConstitutiveLaw",
                variables={"YOUNG_MODULUS": 210000.0, "DENSITY": 7850, "CROSS_AREA": 350},
            )
        ]
    )

    kratos_simulation.write_to_directory(output_dir)
    with (output_dir / "materials.json").open() as f:
        actual = json.load(f)

    with ground_truth_path.open() as f:
        ground_truth = json.load(f)

    assert actual == ground_truth


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
