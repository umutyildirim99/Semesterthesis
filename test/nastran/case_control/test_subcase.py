import pytest

from nastran_to_kratos.nastran.case_control.subcase import Subcase


def test_from_file_content__empty():
    file_content = []  # file content is empty

    actual = Subcase.from_file_content(file_content)
    assert actual == Subcase.empty()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
