import pytest

from nastran_to_kratos.nastran.case_control.case_control_section import CaseControlSection


def test_from_file_content__empty():
    file_content = []

    actual = CaseControlSection.from_file_content(file_content)
    assert actual == CaseControlSection.empty()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
