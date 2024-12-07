from __future__ import annotations

from dataclasses import dataclass

from quantio import Pressure


@dataclass
class Material:
    """The material an element is made out of."""

    name: str = ""
    young_modulus: Pressure | None = None
