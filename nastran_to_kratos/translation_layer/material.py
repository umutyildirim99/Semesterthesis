from __future__ import annotations

from dataclasses import dataclass

from quantio import Pressure

from nastran_to_kratos.kratos.material import KratosMaterial
from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Mat1


@dataclass
class Material:
    """The material an element is made out of."""

    name: str = ""
    young_modulus: Pressure | None = None

    @classmethod
    def from_nastran(cls, mat1: Mat1) -> Material:
        """Construct this class from nastran."""
        return Material(
            name=f"MAT1_{mat1.mid}",
            young_modulus=Pressure(megapascal=mat1.e) if mat1.e is not None else None,
        )

    @classmethod
    def from_kratos(cls, kratos: KratosMaterial) -> Material:
        """Construct this class from kratos."""
        return Material(
            name=kratos.material_name,
            young_modulus=Pressure(megapascal=kratos.variables["YOUNG_MODULUS"]),
        )


def materials_from_nastran(bulk_data: BulkDataSection) -> list[Material]:
    """Construct all materials from the nastran mat1s."""
    return [Material.from_nastran(mat1) for mat1 in _sort_by_mat1_id(bulk_data.mat1s)]


def _sort_by_mat1_id(mat1s: list[Mat1]) -> list[Mat1]:
    return sorted(mat1s, key=lambda mat1: mat1.mid)
