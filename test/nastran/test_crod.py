from nastran_to_kratos.nastran.crod import Crod

import pytest


def test_from_file__all_fields_have_values():
    raw_entry = ["CROD    ", "      12", "      13", "      21", "      23"]

    actual = Crod.read(raw_entry)
    assert actual == Crod(eid=12, pid=13, g1=21, g2=23)


def test_from_file__optional_fields():
    raw_entry = ["CROD    ", "      12", "        ", "      21", "      23"]

    actual = Crod.read(raw_entry)
    assert actual == Crod(eid=12, pid=None, g1=21, g2=23)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
