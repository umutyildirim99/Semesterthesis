import pytest

from nastran_to_kratos.nastran.case_control.subcase import (
    Subcase,
    UnsupportedSubcaseFieldError,
    Analysis,
)


def test_from_file_content__empty():
    file_content = []

    actual = Subcase.from_file_content(file_content)
    assert actual == Subcase.empty()


def test_from_file_content__invalid_key():
    file_content = ["  INVALID = 1"]

    with pytest.raises(UnsupportedSubcaseFieldError):
        Subcase.from_file_content(file_content)


def test_from_file_content__subtitle():
    file_content = ["  SUBTITLE = LS_xForce"]

    actual = Subcase.from_file_content(file_content)
    assert actual == Subcase(subtitle="LS_xForce")


def test_from_file_content__label():
    file_content = ["  LABEL = LS_yForce"]

    actual = Subcase.from_file_content(file_content)
    assert actual == Subcase(label="LS_yForce")


def test_from_file_content__analysis():
    file_content = ["  ANALYSIS = STATICS"]

    actual = Subcase.from_file_content(file_content)
    assert actual == Subcase(analysis=Analysis.STATICS)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
