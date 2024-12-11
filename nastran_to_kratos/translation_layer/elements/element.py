from __future__ import annotations

from dataclasses import dataclass, field

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
