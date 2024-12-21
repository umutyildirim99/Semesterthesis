from nastran_to_kratos.nastran.bulk_data.entries import Prod

import pytest


def test_read__all_fields_have_values():
    raw_entry = ["PROD", "17", "23", "42.6", "17.92", "4.2356", "0.5"]

    actual = Prod.from_file_content(raw_entry)
    assert actual == Prod(pid=17, mid=23, a=42.6, j=17.92, c=4.2356, nsm=0.5)


def test_read__optional_fields():
    raw_entry = ["PROD", "17", "23", "42.6"]

    actual = Prod.from_file_content(raw_entry)
    assert actual == Prod(pid=17, mid=23, a=42.6, j=None, c=0.0, nsm=None)


def test_to_file_content__all_fields_have_values():
    prod = Prod(pid=17, mid=23, a=42.6, j=17.92, c=4.2356, nsm=0.5)

    actual = prod.to_file_content()
    assert actual == "PROD          17      23    42.6   17.92  4.2356     0.5"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
