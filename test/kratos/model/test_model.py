import pytest

from nastran_to_kratos.kratos.model import Condition, Element, Model, Node


def test_to_mdpa__empty():
    model = Model()

    actual = model.to_mdpa()
    assert actual == []


def test_to_mdpa__one_property_two_values():
    model = Model(
        properties={
            0: {
                "DENSITY": 1.0,
                "THICKNESS": 2.0,
            }
        }
    )

    actual = model.to_mdpa()
    assert actual == [
        "Begin Properties 0",
        "    DENSITY 1.0",
        "    THICKNESS 2.0",
        "End Properties",
    ]


def test_to_mdpa__two_properties_one_value_each():
    model = Model(
        properties={
            0: {
                "DENSITY": 1.0,
            },
            1: {
                "DENSITY": 3.0,
            },
        }
    )

    actual = model.to_mdpa()
    assert actual == [
        "Begin Properties 0",
        "    DENSITY 1.0",
        "End Properties",
        "",
        "Begin Properties 1",
        "    DENSITY 3.0",
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


def test_to_mdpa__one_element_two_values():
    model = Model(
        elements={
            "TrussLinearElement3D2N": {
                1: Element(
                    property_id=0,
                    node_ids=[1, 2],
                ),
                2: Element(
                    property_id=1,
                    node_ids=[2, 3],
                ),
            },
        }
    )

    actual = model.to_mdpa()
    assert actual == [
        "Begin Elements TrussLinearElement3D2N",
        "    1 0 1 2",
        "    2 1 2 3",
        "End Elements",
    ]


def test_to_mdpa__two_elements_one_value_each():
    model = Model(
        elements={
            "TrussLinearElement3D2N": {
                1: Element(
                    property_id=0,
                    node_ids=[1, 2],
                ),
            },
            "Element2D3N": {
                1: Element(
                    property_id=0,
                    node_ids=[1, 4],
                ),
            },
        }
    )

    actual = model.to_mdpa()
    assert actual == [
        "Begin Elements TrussLinearElement3D2N",
        "    1 0 1 2",
        "End Elements",
        "",
        "Begin Elements Element2D3N",
        "    1 0 1 4",
        "End Elements",
    ]


def test_to_mdpa__one_condition_two_values():
    model = Model(
        conditions={
            "PointLoadCondition2D1N": {
                1: Condition(
                    property_id=0,
                    node_ids=[1, 2],
                ),
                2: Condition(
                    property_id=1,
                    node_ids=[2, 3],
                ),
            },
        }
    )

    actual = model.to_mdpa()
    assert actual == [
        "Begin Conditions PointLoadCondition2D1N",
        "    1 0 1 2",
        "    2 1 2 3",
        "End Conditions",
    ]


def test_to_mdpa__two_conditions_one_value_each():
    model = Model(
        conditions={
            "PointLoadCondition2D1N": {
                1: Condition(
                    property_id=0,
                    node_ids=[1, 2],
                ),
            },
            "Condition2D": {
                1: Condition(
                    property_id=0,
                    node_ids=[1, 4],
                ),
            },
        }
    )

    actual = model.to_mdpa()
    assert actual == [
        "Begin Conditions PointLoadCondition2D1N",
        "    1 0 1 2",
        "End Conditions",
        "",
        "Begin Conditions Condition2D",
        "    1 0 1 4",
        "End Conditions",
    ]


def test_to_mdpa__submodels_empty_one_layer():
    model = Model(sub_models={"Truss": Model()})

    actual = model.to_mdpa()
    assert actual == [
        "Begin SubModelPart Truss",
        "End SubModelPart",
    ]


def test_to_mdpa__submodels_empty_two_layers():
    model = Model(sub_models={"Truss": Model(sub_models={"SubTruss": Model()})})

    actual = model.to_mdpa()
    assert actual == [
        "Begin SubModelPart Truss",
        "    Begin SubModelPart SubTruss",
        "    End SubModelPart",
        "End SubModelPart",
    ]


def test_to_mdpa__submodel_sub_fields():
    model = Model(
        sub_models={
            "Truss": Model(
                nodes={
                    1: Node(1.0, 2.0, 3.0),
                }
            )
        }
    )

    actual = model.to_mdpa()
    assert actual == [
        "Begin SubModelPart Truss",
        "    Begin SubModelPartNodes",
        "        1 1.0 2.0 3.0",
        "    End SubModelPartNodes",
        "End SubModelPart",
    ]


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
