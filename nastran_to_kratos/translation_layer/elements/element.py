from dataclasses import dataclass, field

from .connector import Connector
from .material import Material
from .point import Point


@dataclass
class Element:
    """An element in a model."""

    nodes: list[Point] = field(default_factory=list)
    connectors: list[Connector] = field(default_factory=list)
    material: Material | None = None
