from nastran_to_kratos.nastran_to_kratos import add

import pytest

def test_add():
    assert add(1, 1) == 2

if __name__ == "__main__":
    pytest.main([__file__, "-v"])