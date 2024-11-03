from nastran_to_kratos.nastran.bulk_data import Prod

import pytest


def test_read__all_fields_have_values():
    raw_entry = ["PROD", "17", "23", "42.6", "17.92", "4.2356", "0.5"]

    actual = Prod.read(raw_entry)
    assert actual == Prod(pid=17, mid=23, a=42.6, j=17.92, c=4.2356, nsm=0.5)


def test_read__optional_fields():
    raw_entry = ["PROD", "17", "23", "42.6", "17.92", "        ", "0.5"]

    actual = Prod.read(raw_entry)
    assert actual == Prod(pid=17, mid=23, a=42.6, j=17.92, c=0.0, nsm=0.5)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
