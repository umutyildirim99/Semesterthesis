from nastran_to_kratos.nastran.bulk_data.entries import Conrod
import pytest


def test_read__all_fields_have_values():
    raw_entry = ["CONROD", "2", "16", "17", "4", "2.69"]
    actual = Conrod.from_file_content(raw_entry)
    assert actual == Conrod(eid=2, g1=16, g2=17, mid=4, a=2.69)


def test_to_file_content():
    conrod = Conrod(eid=2, g1=16, g2=17, mid=4, a=2.69)
    actual = conrod.to_file_content()
    expected = "CONROD           2      16      17       4    2.69"

    print(f"\nExpected: {repr(expected)}")
    print(f"Actual:   {repr(actual)}")

    assert actual == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
