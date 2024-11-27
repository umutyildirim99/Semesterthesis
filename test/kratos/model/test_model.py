import pytest

from nastran_to_kratos.kratos.model import Model, Node


def test_to_mdpa__empty():
    model = Model()

    actual = model.to_mdpa()
    assert actual == []


def test_to_mdpa__properties():
    model = Model(
        properties={
            0: {
                "DENSITY": 1.0,
                "THICKNESS": 2.0,
            },
            1: {
                "DENSITY": 3.0,
                "THICKNESS": 4.0,
            },
        }
    )

    actual = model.to_mdpa()
    assert actual == [
        "Begin Properties 0",
        "    DENSITY 1.0",
        "    THICKNESS 2.0",
        "End Properties",
        "",
        "Begin Properties 1",
        "    DENSITY 3.0",
        "    THICKNESS 4.0",
        "End Properties",
    ]


def test_to_mdpa__nodes():
    model = Model(
        nodes={
            1: Node(1.0, 2.0, 3.0),
            2: Node(4.0, 5.0, 6.0),
        }
    )

    actual = model.to_mdpa()
    assert actual == [
        "Begin Nodes",
        "    1 1.0 2.0 3.0",
        "    2 4.0 5.0 6.0",
        "End Nodes",
    ]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
