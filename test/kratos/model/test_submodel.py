import pytest

from nastran_to_kratos.kratos.model import Condition, Element, Model, Node, SubModel


def test_to_mdpa__submodels_empty():
    submodel = SubModel(sub_models={"SubTruss": SubModel()})

    actual = submodel.to_mdpa()
    assert actual == [
        "    Begin SubModelPart SubTruss",
        "    End SubModelPart",
    ]


def test_to_mdpa__submodelpart_properties():
    submodel = SubModel(properties=[1, 2])

    actual = submodel.to_mdpa()
    assert actual == [
        "    Begin SubModelPartProperties",
        "        1",
        "        2",
        "    End SubModelPartProperties",
    ]


def test_to_mdpa__submodelpart_nodes():
    submodel = SubModel(nodes=[1, 2])

    actual = submodel.to_mdpa()
    assert actual == [
        "    Begin SubModelPartNodes",
        "        1",
        "        2",
        "    End SubModelPartNodes",
    ]


def test_to_mdpa__submodelpart_elements():
    submodel = SubModel(elements=[1, 2])

    actual = submodel.to_mdpa()
    assert actual == [
        "    Begin SubModelPartElements",
        "        1",
        "        2",
        "    End SubModelPartElements",
    ]


def test_to_mdpa__submodelpart_conditions():
    submodel = SubModel(conditions=[1, 2])

    actual = submodel.to_mdpa()
    assert actual == [
        "    Begin SubModelPartConditions",
        "        1",
        "        2",
        "    End SubModelPartConditions",
    ]


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
