from nastran_to_kratos.nastran.bulk_data.entries import Crod

import pytest


def test_read__all_fields_have_values():
    raw_entry = ["CROD    ", "      12", "      13", "      21", "      23"]

    actual = Crod.from_file_content(raw_entry)
    assert actual == Crod(eid=12, pid=13, g1=21, g2=23)


def test_to_file_content():
    crod = Crod(eid=12, pid=13, g1=21, g2=23)

    actual = crod.to_file_content()
    assert actual == "CROD          12      13      21      23"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
