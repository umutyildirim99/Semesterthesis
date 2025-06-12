from nastran_to_kratos.nastran.bulk_data.entries import Rbe2
import pytest


def test_read__minimal_required_fields():
    raw = ["RBE2    1 10 123 20"]
    actual = Rbe2.from_file_content(raw)
    expected = Rbe2(eid=1, gn=10, cm=123, gmi=[20])
    assert actual == expected


def test_read__all_fields_have_values():
    raw_entry = ["RBE2", "9", "8", "12", "10", "12", "14", "15", "16", "6.5", "-6.0"]

    actual = Rbe2.from_file_content(raw_entry)
    expected = Rbe2(
        eid=9,
        gn=8,
        cm=12,
        gmi=[10, 12, 14, 15, 16],
        alpha=6.5,
        tref=-6.0,
    )

    assert actual == expected


def test_read__multiple_gmi_no_optional_fields():
    raw = ["RBE2    2 5 3 10 11 12 13 14 15"]
    actual = Rbe2.from_file_content(raw)
    expected = Rbe2(eid=2, gn=5, cm=3, gmi=[10, 11, 12, 13, 14, 15])
    assert actual == expected


def test_read__with_alpha_only():
    raw = ["RBE2    3 7 6 21 22 23 0.75"]
    actual = Rbe2.from_file_content(raw)
    expected = Rbe2(eid=3, gn=7, cm=6, gmi=[21, 22, 23], alpha=0.75)
    assert actual == expected


def test_to_file_content__with_all_fields():
    rbe2 = Rbe2(eid=9, gn=8, cm=12, gmi=[10, 12, 14, 15, 16], alpha=6.5, tref=-6.0)
    actual = rbe2.to_file_content()
    expected = (
        "RBE2           9       8      12      10      12      14      15      16     6.5    -6.0"
    )

    print("\nExpected:", repr(expected))
    print("Actual:  ", repr(actual))

    assert actual == expected


def test_to_file_content__only_required_fields():
    rbe2 = Rbe2(eid=20, gn=100, cm=123, gmi=[200, 300])
    actual = rbe2.to_file_content()
    expected = "RBE2          20     100     123     200     300"

    assert actual == expected


def test_read__with_alpha_and_tref():
    raw = ["RBE2    4 8 2 30 31 32 1.23 -50.0"]
    actual = Rbe2.from_file_content(raw)
    expected = Rbe2(eid=4, gn=8, cm=2, gmi=[30, 31, 32], alpha=1.23, tref=-50.0)
    assert actual == expected


def test_read__all_fields_have_values():
    # Multiline RBE2 with GMI, alpha, tref
    raw_entry = ["RBE2    9 8 12 10 12 14 15 16", " 6.5 -6.0"]
    actual = Rbe2.from_file_content(raw_entry)
    expected = Rbe2(eid=9, gn=8, cm=12, gmi=[10, 12, 14, 15, 16], alpha=6.5, tref=-6.0)

    assert actual == expected


def test_round_trip():
    original = Rbe2(eid=7, gn=4, cm=6, gmi=[1, 2, 3, 4], alpha=0.0, tref=100.0)
    text = original.to_file_content()
    reconstructed = Rbe2.from_file_content(text.splitlines())
    assert reconstructed == original


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
