from __future__ import annotations

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

    @classmethod
    def from_mdpa(cls, mdpa_content: list[str]) -> Model:
        """Construct this class from an mdpa file."""
        model = Model()
        stripped_mdpa_content = _strip_all_lines(mdpa_content)

        for i, line in enumerate(stripped_mdpa_content):
            if line.startswith("Begin Properties"):
                model.properties = _properties_from_mdpa(stripped_mdpa_content[i:])
            if line.startswith("Begin Nodes"):
                model.nodes = _nodes_from_mdpa(stripped_mdpa_content[i:])
            if line.startswith("Begin Elements"):
                model.elements = _elements_from_mdpa(stripped_mdpa_content[i:])
            if line.startswith("Begin Conditions"):
                model.conditions = _conditions_from_mdpa(stripped_mdpa_content[i:])
            if line.startswith("Begin SubModelPart "):
                submodelpart_id = line.split(" ")[-1]
                model.sub_models[submodelpart_id] = _submodelpart_from_mdpa(
                    stripped_mdpa_content[i:]
                )

        return model

    def to_mdpa(self) -> list[str]:
        """Export this model to a list of string compatible with the kratos .mdpa files."""
        mdpa_content = []

        mdpa_content.extend(_properties_to_mdpa(self.properties))
        mdpa_content.extend(_nodes_to_mdpa(self.nodes))
        mdpa_content.extend(_elements_to_mdpa(self.elements))
        mdpa_content.extend(_conditions_to_mdpa(self.conditions))
        mdpa_content.extend(_submodels_to_mdpa(self.sub_models))

        return _remove_empty_last_row(mdpa_content)


def _properties_to_mdpa(properties: dict[int, dict[str, float]]) -> list[str]:
    if properties == {}:
        return []

    mdpa_content = []

    for property_id, property_ in properties.items():
        mdpa_content.append(f"Begin Properties {property_id}")

        for key, value in property_.items():
            mdpa_content.append(_indent(f"{key} {value}", 1))

        mdpa_content.append("End Properties")
        mdpa_content.append("")

    return mdpa_content


def _nodes_to_mdpa(nodes: dict[int, Node]) -> list[str]:
    if nodes == {}:
        return []

    mdpa_content = []
    mdpa_content.append("Begin Nodes")

    for node_id, node in nodes.items():
        mdpa_content.append(_indent(node.to_mdpa(node_id), 1))

    mdpa_content.append("End Nodes")
    mdpa_content.append("")
    return mdpa_content


def _elements_to_mdpa(elements: dict[str, dict[int, Element]]) -> list[str]:
    if elements == {}:
        return []

    mdpa_content = []
    for element_id, element in elements.items():
        mdpa_content.append(f"Begin Elements {element_id}")

        for subelement_id, sub_element in element.items():
            mdpa_content.append(_indent(sub_element.to_mdpa(subelement_id), 1))

        mdpa_content.append("End Elements")
        mdpa_content.append("")

    return mdpa_content


def _conditions_to_mdpa(conditions: dict[str, dict[int, Condition]]) -> list[str]:
    if conditions == {}:
        return []

    mdpa_content = []

    for condition_id, condition in conditions.items():
        mdpa_content.append(f"Begin Conditions {condition_id}")

        for subcondition_id, sub_condition in condition.items():
            mdpa_content.append(_indent(sub_condition.to_mdpa(subcondition_id), 1))

        mdpa_content.append("End Conditions")
        mdpa_content.append("")

    return mdpa_content


def _submodels_to_mdpa(submodels: dict[str, SubModel]) -> list[str]:
    if submodels == {}:
        return []

    mdpa_content = []

    for submodel_id, submodel in submodels.items():
        mdpa_content.append(f"Begin SubModelPart {submodel_id}")

        mdpa_content.extend(submodel.to_mdpa(1))

        mdpa_content.append("End SubModelPart")
        mdpa_content.append("")

    return mdpa_content


def _strip_all_lines(lines: list[str]) -> list[str]:
    return [line.strip() for line in lines]


def _properties_from_mdpa(lines: list[str]) -> dict[int, dict[str, float]]:
    property_id = int(lines[0].split(" ")[-1])
    return {property_id: {}}


def _nodes_from_mdpa(lines: list[str]) -> dict[int, Node]:
    nodes = {}
    for line in lines[1:]:
        if line.startswith("End Nodes"):
            break

        node_id = int(line.split(" ")[0])
        x = float(line.split(" ")[1])
        y = float(line.split(" ")[2])
        z = float(line.split(" ")[3])

        nodes[node_id] = Node(x, y, z)

    return nodes


def _elements_from_mdpa(lines: list[str]) -> dict[str, dict[int, Element]]:
    element_id = lines[0].split(" ")[-1]
    elements: dict[str, dict[int, Element]] = {element_id: {}}
    for line in lines[1:]:
        if line.startswith("End Elements"):
            break

        sub_id = int(line.split(" ")[0])
        property_id = int(line.split(" ")[1])
        node_ids = [int(n) for n in line.split(" ")[2:]]
        elements[element_id][sub_id] = Element(property_id, node_ids)

    return elements


def _conditions_from_mdpa(lines: list[str]) -> dict[str, dict[int, Condition]]:
    condition_id = lines[0].split(" ")[-1]
    conditions: dict[str, dict[int, Condition]] = {condition_id: {}}
    for line in lines[1:]:
        if line.startswith("End Conditions"):
            break

        sub_id = int(line.split(" ")[0])
        property_id = int(line.split(" ")[1])
        node_ids = [int(n) for n in line.split(" ")[2:]]
        conditions[condition_id][sub_id] = Condition(property_id, node_ids)

    return conditions


def _submodelpart_from_mdpa(lines: list[str]) -> SubModel:
    submodel = SubModel()
    for i, line in enumerate(lines):
        if line == "End SubModelPart":
            break

        if line.startswith("Begin SubModelPartNodes"):
            submodel.nodes = _read_consecutive_numbers(lines[i + 1 :])
        if line.startswith("Begin SubModelPartElements"):
            submodel.elements = _read_consecutive_numbers(lines[i + 1 :])
        if line.startswith("Begin SubModelPartConditions"):
            submodel.conditions = _read_consecutive_numbers(lines[i + 1 :])

    return submodel


def _read_consecutive_numbers(lines: list[str]) -> list[int]:
    numbers = []
    for line in lines:
        if line.startswith("End"):
            break
        numbers.append(int(line))

    return numbers
