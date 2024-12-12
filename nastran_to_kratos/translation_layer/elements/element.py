from __future__ import annotations

from dataclasses import dataclass, field

from nastran_to_kratos.kratos.material import KratosMaterial
from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import _BulkDataEntry

from .connector import Connector, trusses_from_nastran
from .material import Material
from .point import Point, nodes_from_nastran


@dataclass
class Element:
    """An element in a model."""

    nodes: list[Point] = field(default_factory=list)
    connectors: list[Connector] = field(default_factory=list)
    material: Material | None = None

    @classmethod
    def from_nastran(cls, entries: list[_BulkDataEntry]) -> Element:
        """Construct this class from nastran."""
        bulk_data = BulkDataSection(entries)
        return Element(
            nodes=nodes_from_nastran(bulk_data),
            connectors=trusses_from_nastran(bulk_data),
            material=Material.from_nastran(bulk_data.mat1s[0]),
        )

    def to_kratos_material(self, index: int) -> KratosMaterial:
        """Export this element as a kratos material."""
        if self.material is None:
            raise ValueError

        return KratosMaterial(
            model_part_name=f"element_{index}",
            properties_id=0,
            material_name=self.material.name,
            constitutive_law="TrussConstitutiveLaw",
            variables={
                "YOUNG_MODULUS": self.material.young_modulus.megapascal
                if self.material.young_modulus is not None
                else 0.0,
                "CROSS_AREA": self.connectors[0].cross_section.square_millimeters,  # type: ignore[attr-defined]
            },
        )


def elements_from_nastran(bulk_data: BulkDataSection) -> list[Element]:
    """Construct all elements from nastran."""
    grids_by_id = {grid.id: grid for grid in bulk_data.grids}
    crods = bulk_data.crods
    prods_by_pid = {prod.pid: prod for prod in bulk_data.prods}
    mat1s_by_mid = {mat1.mid: mat1 for mat1 in bulk_data.mat1s}

    nastran_elements: list[set[_BulkDataEntry]] = []
    for crod in crods:
        element_which_contains_grid1 = _which_element_is_entry_in(
            grids_by_id[crod.g1], nastran_elements
        )
        element_which_contains_grid2 = _which_element_is_entry_in(
            grids_by_id[crod.g2], nastran_elements
        )

        if element_which_contains_grid1 is None and element_which_contains_grid2 is None:
            nastran_elements.append(set())
            element_index = -1

        elif element_which_contains_grid1 is not None and element_which_contains_grid2 is None:
            element_index = element_which_contains_grid1

        elif element_which_contains_grid1 is None and element_which_contains_grid2 is not None:
            element_index = element_which_contains_grid2

        else:
            element_index = element_which_contains_grid1  # type: ignore[assignment]

        nastran_elements[element_index].update(
            [
                crod,
                prods_by_pid[crod.pid],
                mat1s_by_mid[prods_by_pid[crod.pid].mid],
                grids_by_id[crod.g1],
                grids_by_id[crod.g2],
            ]
        )

    return [Element.from_nastran(list(entries)) for entries in nastran_elements]


def _which_element_is_entry_in(
    entry: _BulkDataEntry, nastran_elements: list[set[_BulkDataEntry]]
) -> int | None:
    for i, nastran_element in enumerate(nastran_elements):
        if entry in nastran_element:
            return i
    return None
