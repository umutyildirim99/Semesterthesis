import pytest

from nastran_to_kratos.nastran.case_control.subcase import (
    Subcase,
    UnsupportedSubcaseFieldError,
    Analysis,
    Displacement,
)


def test_from_file_content__empty():
    file_content = []

    actual = Subcase.from_file_content(file_content)
    assert actual == Subcase.empty()


def test_from_file_content__invalid_key():
    file_content = ["  INVALID = 1"]

    with pytest.raises(UnsupportedSubcaseFieldError):
        Subcase.from_file_content(file_content)


def test_from_file_content__analysis():
    file_content = ["  ANALYSIS = STATICS"]

    actual = Subcase.from_file_content(file_content)
    assert actual == Subcase(analysis=Analysis.STATICS)


def test_from_file_content__displacement():
    file_content = ["  DISPLACEMENT = ALL"]

    actual = Subcase.from_file_content(file_content)
    assert actual == Subcase(displacement=Displacement.ALL)


def test_from_file_content__label():
    file_content = ["  LABEL = LS_yForce"]

    actual = Subcase.from_file_content(file_content)
    assert actual == Subcase(label="LS_yForce")


def test_from_file_content__load():
    file_content = ["  LOAD = 1"]

    actual = Subcase.from_file_content(file_content)
    assert actual == Subcase(load=1)


def test_from_file_content__spc():
    file_content = ["  SPC = 2"]

    actual = Subcase.from_file_content(file_content)
    assert actual == Subcase(spc=2)


def test_from_file_content__subtitle():
    file_content = ["  SUBTITLE = LS_xForce"]

    actual = Subcase.from_file_content(file_content)
    assert actual == Subcase(subtitle="LS_xForce")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
