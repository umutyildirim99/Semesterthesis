from nastran_to_kratos.nastran.bulk_data.entries import Force

import pytest


def test_read__all_fields_have_values():
    raw_entry = ["FORCE", "2", "5", "6", "2.9", "0.0", "1.0", "0.0"]

    actual = Force.from_file_content(raw_entry)
    assert actual == Force(sid=2, g=5, cid=6, f=2.9, n1=0.0, n2=1.0, n3=0.0)


def test_read__optionale_fields():
    raw_entry = ["FORCE", "2", "5", "        ", "2.9", "0.0", "1.0", "0.0"]

    actual = Force.from_file_content(raw_entry)
    assert actual == Force(sid=2, g=5, cid=0, f=2.9, n1=0.0, n2=1.0, n3=0.0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
