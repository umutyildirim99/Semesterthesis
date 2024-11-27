from dataclasses import dataclass, field

from ._util import _indent, _remove_empty_last_row
from .condition import Condition
from .element import Element
from .node import Node
from .submodel import SubModel


@dataclass
class Model:
    """The parameters defining the shape and properties of the model in kratos."""

    properties: dict[int, dict[str, float]] = field(default_factory=dict)
    nodes: dict[int, Node] = field(default_factory=dict)
    elements: dict[str, dict[int, Element]] = field(default_factory=dict)
    conditions: dict[str, dict[int, Condition]] = field(default_factory=dict)
    sub_models: dict[str, SubModel] = field(default_factory=dict)

    def to_mdpa(self) -> list[str]:
        """Export this model to a list of string compatible with the kratos .mdpa files."""
        mdpa_content = []

        if len(self.properties) != 0:
            mdpa_content.extend(_properties_to_mdpa(self.properties))
            mdpa_content.append("")

        if len(self.nodes) != 0:
            mdpa_content.extend(_nodes_to_mdpa(self.nodes))
            mdpa_content.append("")

        if len(self.elements) != 0:
            mdpa_content.extend(_elements_to_mdpa(self.elements))
            mdpa_content.append("")

        if len(self.conditions) != 0:
            mdpa_content.extend(_conditions_to_mdpa(self.conditions))
            mdpa_content.append("")

        if len(self.sub_models) != 0:
            mdpa_content.extend(_submodels_to_mdpa(self.sub_models))
            mdpa_content.append("")

        return _remove_empty_last_row(mdpa_content)


def _properties_to_mdpa(properties: dict[int, dict[str, float]]) -> list[str]:
    mdpa_content = []

    for property_id, property_ in properties.items():
        mdpa_content.append(f"Begin Properties {property_id}")

        for key, value in property_.items():
            mdpa_content.append(_indent(f"{key} {value}", 1))

        mdpa_content.append("End Properties")
        mdpa_content.append("")

    return _remove_empty_last_row(mdpa_content)


def _nodes_to_mdpa(nodes: dict[int, Node]) -> list[str]:
    mdpa_content = []
    mdpa_content.append("Begin Nodes")

    for node_id, node in nodes.items():
        mdpa_content.append(_indent(node.to_mdpa(node_id), 1))

    mdpa_content.append("End Nodes")
    return mdpa_content


def _elements_to_mdpa(elements: dict[str, dict[int, Element]]) -> list[str]:
    mdpa_content = []
    for element_id, element in elements.items():
        mdpa_content.append(f"Begin Elements {element_id}")

        for subelement_id, sub_element in element.items():
            mdpa_content.append(_indent(sub_element.to_mdpa(subelement_id), 1))

        mdpa_content.append("End Elements")
        mdpa_content.append("")

    return _remove_empty_last_row(mdpa_content)


def _conditions_to_mdpa(conditions: dict[str, dict[int, Condition]]) -> list[str]:
    mdpa_content = []

    for condition_id, condition in conditions.items():
        mdpa_content.append(f"Begin Conditions {condition_id}")

        for subcondition_id, sub_condition in condition.items():
            mdpa_content.append(_indent(sub_condition.to_mdpa(subcondition_id), 1))

        mdpa_content.append("End Conditions")
        mdpa_content.append("")

    return _remove_empty_last_row(mdpa_content)


def _submodels_to_mdpa(submodels: dict[str, SubModel]) -> list[str]:
    mdpa_content = []

    for submodel_id, submodel in submodels.items():
        mdpa_content.append(f"Begin SubModelPart {submodel_id}")

        mdpa_content.extend(submodel.to_mdpa(1))

        mdpa_content.append("End SubModelPart")
        mdpa_content.append("")

    return _remove_empty_last_row(mdpa_content)
