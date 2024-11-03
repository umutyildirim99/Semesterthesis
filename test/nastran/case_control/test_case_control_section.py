import pytest

from nastran_to_kratos.nastran.case_control.case_control_section import CaseControlSection, Subcase


def test_from_file_content__empty():
    file_content = []

    actual = CaseControlSection.from_file_content(file_content)
    assert actual == CaseControlSection.empty()


def test_from_file_content__only_general():
    file_content = [
        "  ANALYSIS = STATICS",
        "  DISPLACEMENT = ALL",
        "  STRAIN = ALL",
        "  STRESS = ALL",
    ]

    actual = CaseControlSection.from_file_content(file_content)
    assert actual == CaseControlSection(
        general=Subcase.from_file_content(file_content),
        subcases={},
    )


def test_from_file_content__subcases():
    file_content = [
        "SUBCASE       1",
        "  SUBTITLE  = LS_xForce",
        "  LABEL= LS_xForce",
        "SUBCASE       2",
        "  SUBTITLE  = LS_yForce",
        "  LABEL= LS_yForce",
    ]

    actual = CaseControlSection.from_file_content(file_content)
    assert actual == CaseControlSection(
        general=Subcase.empty(),
        subcases={
            1: Subcase.from_file_content(
                [
                    "  SUBTITLE  = LS_xForce",
                    "  LABEL= LS_xForce",
                ]
            ),
            2: Subcase.from_file_content(
                [
                    "  SUBTITLE  = LS_yForce",
                    "  LABEL= LS_yForce",
                ]
            ),
        },
    )


def test_from_file_content__general_and_subcase():
    file_content = [
        "  ANALYSIS = STATICS",
        "  DISPLACEMENT = ALL",
        "  STRAIN = ALL",
        "  STRESS = ALL",
        "SUBCASE       1",
        "  SUBTITLE  = LS_xForce",
        "  LABEL= LS_xForce",
        "  SPC =        2",
        "  LOAD =        1",
        "  ANALYSIS = STATICS",
    ]

    actual = CaseControlSection.from_file_content(file_content)
    assert actual == CaseControlSection(
        general=Subcase.from_file_content(
            [
                "  ANALYSIS = STATICS",
                "  DISPLACEMENT = ALL",
                "  STRAIN = ALL",
                "  STRESS = ALL",
            ]
        ),
        subcases={
            1: Subcase.from_file_content(
                [
                    "  SUBTITLE  = LS_xForce",
                    "  LABEL= LS_xForce",
                    "  SPC =        2",
                    "  LOAD =        1",
                    "  ANALYSIS = STATICS",
                ]
            )
        },
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
