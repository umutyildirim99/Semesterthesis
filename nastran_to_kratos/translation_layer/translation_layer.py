from __future__ import annotations

from dataclasses import dataclass

from .elements import Element


@dataclass
class TranslationLayer:
    """A representation of a simulation used as a translation between nastran and kratos."""

    elements: list[Element] | None = None
