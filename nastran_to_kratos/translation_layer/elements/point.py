from __future__ import annotations

from dataclasses import dataclass

from quantio import Length


@dataclass
class Point:
    """A point in 3D space."""

    x: Length
    y: Length
    z: Length
