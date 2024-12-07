from abc import ABC
from dataclasses import dataclass

from quantio import Area


@dataclass
class Connector(ABC):
    """The base class of all connectors between two elements."""

    first_point_id: int
    seconds_point_id: int


@dataclass
class Truss(Connector):
    """A connector, which can only transfer forces along its primary axis."""

    cross_section: Area
