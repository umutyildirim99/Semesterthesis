from __future__ import annotations

from dataclasses import dataclass

from quantio import Pressure

from nastran_to_kratos.nastran.bulk_data.entries import Mat1


@dataclass
class Material:
    """The material an element is made out of."""

    name: str = ""
    young_modulus: Pressure | None = None

    @classmethod
    def from_nastran(cls, mat1: Mat1) -> Material:
        """Construct this class from nastran."""
        return Material(name=f"Mat1_{mat1.mid}", young_modulus=Pressure(megapascal=mat1.e))
