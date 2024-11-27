import pytest

from nastran_to_kratos.kratos.model import Node


def test_to_mdpa():
    node = Node(1000.0, 2000.0, 3000.0)
    actual = node.to_mdpa(1)
    assert actual == "1 1000.0 2000.0 3000.0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
