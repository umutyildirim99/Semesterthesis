from nastran_to_kratos.nastran.bulk_data.entries import Mat1

import pytest


def test_read__all_fields_have_values():
    raw_entry = [
        "MAT1",
        "17",
        "3e7",
        "0.5",
        "0.33",
        "4.28",
        "6.5e-6",
        "5.37e2",
        "0.23",
        "20e4",
        "15e4",
        "12e4",
        "1003",
    ]

    actual = Mat1.from_file_content(raw_entry)
    assert actual == Mat1(
        mid=17,
        e=3e7,
        g=0.5,
        nu=0.33,
        rho=4.28,
        a=6.5e-6,
        tref=5.37e2,
        ge=0.23,
        st=20e4,
        sc=15e4,
        ss=12e4,
        mcsid=1003,
    )


def test_read__optional_fields():
    raw_entry = ["MAT1", "17"]

    actual = Mat1.from_file_content(raw_entry)
    assert actual == Mat1(
        mid=17,
        e=None,
        g=None,
        nu=None,
        rho=None,
        a=None,
        tref=0.0,
        ge=None,
        st=None,
        sc=None,
        ss=None,
        mcsid=None,
    )


def test_to_file_content__all_fields_have_values():
    mat1 = Mat1(
        mid=17,
        e=3e7,
        g=0.5,
        nu=0.33,
        rho=4.28,
        a=6.5e-6,
        tref=5.37e2,
        ge=0.23,
        st=20e4,
        sc=15e4,
        ss=12e4,
        mcsid=1003,
    )

    actual = mat1.to_file_content()
    assert (
        actual
        == "MAT1          1730000000     0.5    0.33    4.28 6.5e-06     537    0.23  200000  150000  120000    1003"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
