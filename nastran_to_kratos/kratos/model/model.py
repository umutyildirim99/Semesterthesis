from __future__ import annotations

from dataclasses import dataclass, field

from .condition import Condition
from .element import Element
from .node import Node

INDENT = "    "


@dataclass
class Model:
    """The parameters defining the shape and properties of the model in kratos."""

    properties: dict[int, dict[str, float]] = field(default_factory=dict)
    nodes: dict[int, Node] = field(default_factory=dict)
    elements: dict[str, dict[int, Element]] = field(default_factory=dict)
    conditions: dict[str, dict[int, Condition]] = field(default_factory=dict)
    sub_models: dict[str, Model] = field(default_factory=dict)

    def to_mdpa(self, layer: int = 0) -> list[str]:
        """Export this model to a list of string compatible with the kratos .mdpa files."""
        mdpa_content = []

        if len(self.properties) != 0:
            mdpa_content.extend(_properties_to_mdpa(self.properties, layer))
            mdpa_content.append("")

        if len(self.nodes) != 0:
            mdpa_content.extend(_nodes_to_mdpa(self.nodes, layer))
            mdpa_content.append("")

        if len(self.elements) != 0:
            mdpa_content.extend(_elements_to_mdpa(self.elements, layer))
            mdpa_content.append("")

        if len(self.conditions) != 0:
            mdpa_content.extend(_conditions_to_mdpa(self.conditions, layer))
            mdpa_content.append("")

        if len(self.sub_models) != 0:
            mdpa_content.extend(_submodels_to_mdpa(self.sub_models, layer))
            mdpa_content.append("")

        return _remove_empty_last_row(mdpa_content)


def _properties_to_mdpa(properties: dict[int, dict[str, float]], layer: int) -> list[str]:
    section_name = "Properties" if layer == 0 else "SubModelPartProperties"
    mdpa_content = []

    for property_id, property_ in properties.items():
        mdpa_content.append(INDENT * layer + f"Begin {section_name} {property_id}")

        for key, value in property_.items():
            mdpa_content.append(INDENT * (layer + 1) + f"{key} {value}")

        mdpa_content.append(INDENT * layer + f"End {section_name}")
        mdpa_content.append("")

    return _remove_empty_last_row(mdpa_content)


def _nodes_to_mdpa(nodes: dict[int, Node], layer: int) -> list[str]:
    section_name = "Nodes" if layer == 0 else "SubModelPartNodes"
    mdpa_content = []
    mdpa_content.append(INDENT * layer + f"Begin {section_name}")

    for node_id, node in nodes.items():
        mdpa_content.append(INDENT * (layer + 1) + node.to_mdpa(node_id))

    mdpa_content.append(INDENT * layer + f"End {section_name}")
    return mdpa_content


def _elements_to_mdpa(elements: dict[str, dict[int, Element]], layer: int) -> list[str]:
    section_name = "Elements" if layer == 0 else "SubModelPartElements"
    mdpa_content = []

    for element_id, element in elements.items():
        mdpa_content.append(INDENT * layer + f"Begin {section_name} {element_id}")

        for subelement_id, sub_element in element.items():
            mdpa_content.append(INDENT * (layer + 1) + sub_element.to_mdpa(subelement_id))

        mdpa_content.append(INDENT * layer + f"End {section_name}")
        mdpa_content.append("")

    return _remove_empty_last_row(mdpa_content)


def _conditions_to_mdpa(conditions: dict[str, dict[int, Condition]], layer: int) -> list[str]:
    section_name = "Conditions" if layer == 0 else "SubModelPartConditions"
    mdpa_content = []

    for condition_id, condition in conditions.items():
        mdpa_content.append(INDENT * layer + f"Begin {section_name} {condition_id}")

        for subcondition_id, sub_condition in condition.items():
            mdpa_content.append(INDENT * (layer + 1) + sub_condition.to_mdpa(subcondition_id))

        mdpa_content.append(INDENT * layer + f"End {section_name}")
        mdpa_content.append("")

    return _remove_empty_last_row(mdpa_content)


def _submodels_to_mdpa(submodels: dict[str, Model], layer: int) -> list[str]:
    mdpa_content = []

    for submodel_id, submodel in submodels.items():
        mdpa_content.append(INDENT * layer + f"Begin SubModelPart {submodel_id}")

        mdpa_content.extend(submodel.to_mdpa(layer + 1))

        mdpa_content.append(INDENT * layer + "End SubModelPart")
        mdpa_content.append("")

    return _remove_empty_last_row(mdpa_content)


def _remove_empty_last_row(mdpa_content: list[str]) -> list[str]:
    if len(mdpa_content) != 0 and mdpa_content[-1] == "":
        return mdpa_content[:-1]
    return mdpa_content
