from __future__ import annotations

from dataclasses import dataclass, field

from ._util import _indent, _remove_empty_last_row


@dataclass
class SubModel:
    """The parameters defining the shape and properties of the model in kratos."""

    properties: list[int] = field(default_factory=list)
    nodes: list[int] = field(default_factory=list)
    elements: list[int] = field(default_factory=list)
    conditions: list[int] = field(default_factory=list)
    sub_models: dict[str, SubModel] = field(default_factory=dict)

    def to_mdpa(self, layer: int = 1) -> list[str]:
        """Export this model to a list of string compatible with the kratos .mdpa files."""
        mdpa_content = []

        mdpa_content.extend(_id_list_to_mdpa(self.properties, layer, "SubModelPartProperties"))
        mdpa_content.extend(_id_list_to_mdpa(self.nodes, layer, "SubModelPartNodes"))
        mdpa_content.extend(_id_list_to_mdpa(self.elements, layer, "SubModelPartElements"))
        mdpa_content.extend(_id_list_to_mdpa(self.conditions, layer, "SubModelPartConditions"))
        mdpa_content.extend(_submodels_to_mdpa(self.sub_models, layer))

        return _remove_empty_last_row(mdpa_content)


def _id_list_to_mdpa(id_list: list[int], layer: int, section_name: str) -> list[str]:
    if id_list == []:
        return []

    mdpa_content = []
    mdpa_content.append(_indent(f"Begin {section_name}", layer))

    mdpa_content.extend([_indent(str(id_), layer + 1) for id_ in id_list])

    mdpa_content.append(_indent(f"End {section_name}", layer))
    return mdpa_content


def _submodels_to_mdpa(submodels: dict[str, SubModel], layer: int) -> list[str]:
    if submodels == {}:
        return []

    mdpa_content = []

    for submodel_id, submodel in submodels.items():
        mdpa_content.append(_indent(f"Begin SubModelPart {submodel_id}", layer))

        mdpa_content.extend(submodel.to_mdpa(layer + 1))

        mdpa_content.append(_indent("End SubModelPart", layer))
        mdpa_content.append("")

    return _remove_empty_last_row(mdpa_content)
