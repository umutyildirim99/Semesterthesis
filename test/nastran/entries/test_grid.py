from nastran_to_kratos.nastran.bulk_data import Grid

import pytest


def test_read__all_fields_have_values():
    raw_entry = [
        "GRID    ",
        "       2",
        "       5",
        "  1000.0",
        "     0.0",
        "     2.0",
        "       3",
        "     123",
        "       7",
    ]

    actual = Grid.read(raw_entry)
    assert actual == Grid(id=2, cp=5, x1=1000.0, x2=0.0, x3=2.0, cd=3, ps="123", seid=7)


def test_read__optional_fields():
    raw_entry = ["GRID    ", "       2", "        ", "  1000.0", "     0.0", "     0.0"]

    actual = Grid.read(raw_entry)
    assert actual == Grid(id=2, cp=None, x1=1000.0, x2=0.0, x3=0.0, cd=None, ps=None, seid=0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
