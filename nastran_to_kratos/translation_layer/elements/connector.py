from __future__ import annotations

from abc import ABC
from dataclasses import dataclass

from quantio import Area

from nastran_to_kratos.nastran.bulk_data.entries import Crod, Prod


@dataclass
class Connector(ABC):
    """The base class of all connectors between two elements."""

    first_point_id: int
    seconds_point_id: int


@dataclass
class Truss(Connector):
    """A connector, which can only transfer forces along its primary axis."""

    cross_section: Area

    @classmethod
    def from_nastran(cls, crod: Crod, prod: Prod) -> Truss:
        """Construct this class from nastran."""
        if crod.pid != prod.pid:
            raise KeyError

        return Truss(
            first_point_id=crod.g1,
            seconds_point_id=crod.g2,
            cross_section=Area(square_millimeters=prod.a),
        )
