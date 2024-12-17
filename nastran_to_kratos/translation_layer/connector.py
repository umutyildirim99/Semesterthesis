from __future__ import annotations

from abc import ABC
from dataclasses import dataclass

from quantio import Area

from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Crod, Mat1, Prod

from .material import Material


@dataclass
class Connector(ABC):
    """The base class of all connectors between two elements."""

    first_point_index: int
    second_point_index: int
    material: Material


@dataclass
class Truss(Connector):
    """A connector, which can only transfer forces along its primary axis."""

    cross_section: Area

    @classmethod
    def from_nastran(cls, crod: Crod, prod: Prod, mat1: Mat1) -> Truss:
        """Construct this class from nastran."""
        if crod.pid != prod.pid:
            raise KeyError

        if prod.mid != mat1.mid:
            raise KeyError

        return Truss(
            first_point_index=crod.g1,
            second_point_index=crod.g2,
            cross_section=Area(square_millimeters=prod.a),
            material=Material.from_nastran(mat1),
        )


def trusses_from_nastran(bulk_data: BulkDataSection) -> list[Connector]:
    """Construct all materials from the nastran Crods and Prods."""
    prods_by_pid = {prod.pid: prod for prod in bulk_data.prods}
    mat1s_by_mid = {mat1.mid: mat1 for mat1 in bulk_data.mat1s}
    return [
        Truss.from_nastran(crod, prods_by_pid[crod.pid], mat1s_by_mid[prods_by_pid[crod.pid].mid])
        for crod in bulk_data.crods
    ]
