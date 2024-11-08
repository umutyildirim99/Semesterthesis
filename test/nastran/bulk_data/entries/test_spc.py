from nastran_to_kratos.nastran.bulk_data.entries import Spc

import pytest


def test_read__all_fields_have_values():
    raw_entry = ["SPC", "2", "32", "3", "-2.6", "33", "4", "-1.6"]

    actual = Spc.from_file_content(raw_entry)
    assert actual == Spc(sid=2, g1=32, c1=3, d1=-2.6, g2=33, c2=4, d2=-1.6)


def test_read__optional_fields():
    raw_entry = ["SPC", "2", "32", "3"]

    actual = Spc.from_file_content(raw_entry)
    assert actual == Spc(sid=2, g1=32, c1=3, d1=0.0, g2=None, c2=None, d2=None)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
