import pytest

from nastran_to_kratos.kratos.material import Material


def test_to_json():
    material = Material(
        model_part_name="Structure.Bar",
        properties_id=0,
        material_name="Steel",
        constitutive_law="BarConstitutiveLaw",
        variables={"YOUNG_MODULUS": 210000.0, "DENSITY": 7850, "CROSS_AREA": 350},
    )

    actual = material.to_json()
    assert actual == {
        "model_part_name": "Structure.Bar",
        "properties_id": 0,
        "Material": {
            "name": "Steel",
            "constitutive_law": {"name": "BarConstitutiveLaw"},
            "Variables": {"YOUNG_MODULUS": 210000.0, "DENSITY": 7850, "CROSS_AREA": 350},
            "tables": {},
        },
    }


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
