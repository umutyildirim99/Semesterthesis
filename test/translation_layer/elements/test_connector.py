from pathlib import Path

import pytest

from nastran_to_kratos.nastran.bulk_data import BulkDataSection
from nastran_to_kratos.nastran.bulk_data.entries import Crod, Prod, Mat1, Rbe2
from nastran_to_kratos.translation_layer import Truss, trusses_from_nastran, Material, RBE2Connector


def test_truss_from_nastran():
    crod = Crod(eid=1, pid=1, g1=2, g2=3)
    prod = Prod(pid=1, mid=0, a=350.0)
    mat1 = Mat1(mid=0, e=210_000)

    actual = Truss.from_nastran(crod, prod, mat1)
    assert actual == Truss(
        first_point_index=2,
        second_point_index=3,
        cross_section=350.0,
        material=Material(name="MAT1_0", young_modulus=210_000),
    )


def test_rbe2_connectors_from_nastran__basic():
    rbe2 = Rbe2(eid=100, gn=1, cm=123, gmi=[2, 3])
    bulk = BulkDataSection(entries=[rbe2])

    connectors = RBE2Connector.rbe2_connectors_from_nastran(bulk)

    assert connectors == [RBE2Connector(dependent_node=1, independent_nodes=[2, 3], cm=123)]


def test_truss_from_nastran__pid_does_not_match():
    crod = Crod(eid=1, pid=1, g1=2, g2=3)
    prod = Prod(pid=5, mid=0, a=350.0)
    mat1 = Mat1(mid=0, e=210_000)

    with pytest.raises(KeyError):
        Truss.from_nastran(crod, prod, mat1)


def test_truss_from_nastran__mid_does_not_match():
    crod = Crod(eid=1, pid=5, g1=2, g2=3)
    prod = Prod(pid=5, mid=0, a=350.0)
    mat1 = Mat1(mid=20, e=210_000)

    with pytest.raises(KeyError):
        Truss.from_nastran(crod, prod, mat1)


def test_trusses_from_nastran__two_trusses():
    crod1 = Crod(eid=1, pid=1, g1=5, g2=6)
    prod1 = Prod(pid=1, mid=0, a=400)
    crod2 = Crod(eid=2, pid=2, g1=7, g2=8)
    prod2 = Prod(pid=2, mid=0, a=900)
    mat1 = Mat1(mid=0, e=210_000)
    bulk_data = BulkDataSection(entries=[crod1, crod2, prod1, prod2, mat1])

    actual = trusses_from_nastran(bulk_data)
    assert actual == [
        Truss.from_nastran(crod1, prod1, mat1),
        Truss.from_nastran(crod2, prod2, mat1),
    ]


def test_trusses_from_nastran__ignore_leftover_prod():
    crod1 = Crod(eid=1, pid=1, g1=5, g2=6)
    prod1 = Prod(pid=1, mid=0, a=400)
    prod2 = Prod(pid=2, mid=0, a=900)
    mat1 = Mat1(mid=0, e=210_000)
    bulk_data = BulkDataSection(entries=[crod1, prod1, prod2, mat1])

    actual = trusses_from_nastran(bulk_data)
    assert actual == [Truss.from_nastran(crod1, prod1, mat1)]


def test_trusses_from_nastran__raise_error_for_missing_prod():
    crod1 = Crod(eid=1, pid=1, g1=5, g2=6)
    mat1 = Mat1(mid=0, e=210_000)
    bulk_data = BulkDataSection(entries=[crod1, mat1])

    with pytest.raises(KeyError):
        trusses_from_nastran(bulk_data)


def test_trusses_from_nastran__raise_error_for_missing_mat1():
    crod1 = Crod(eid=1, pid=1, g1=5, g2=6)
    prod1 = Prod(pid=1, mid=0, a=400)
    bulk_data = BulkDataSection(entries=[crod1, prod1])

    with pytest.raises(KeyError):
        trusses_from_nastran(bulk_data)


def test_rbe2_from_nastran():
    rbe2 = Rbe2(eid=100, gn=1, cm=123, gmi=[2, 3, 4])

    actual = RBE2Connector.from_nastran(rbe2)

    assert actual == RBE2Connector(dependent_node=1, independent_nodes=[2, 3, 4], cm=123)


def test_rbe2_from_nastran__many_dependents():
    rbe2 = Rbe2(eid=102, gn=10, cm=123, gmi=list(range(11, 21)))

    actual = RBE2Connector.from_nastran(rbe2)

    assert actual == RBE2Connector(dependent_node=10, independent_nodes=list(range(11, 21)), cm=123)


def test_rbe2_from_nastran__with_alpha_tref():
    rbe2 = Rbe2(eid=103, gn=5, cm=123, gmi=[6, 7, 8], alpha=1.5, tref=300.0)

    actual = RBE2Connector.from_nastran(rbe2)

    assert actual == RBE2Connector(dependent_node=5, independent_nodes=[6, 7, 8], cm=123)


def test_get_constrained_dofs():
    connector = RBE2Connector(dependent_node=1, independent_nodes=[2], cm=0b000111)
    dofs = connector.get_constrained_dofs()
    assert set(dofs) == {"DISPLACEMENT_X", "DISPLACEMENT_Y", "DISPLACEMENT_Z"}


def test_to_kratos_process():
    connector = RBE2Connector(dependent_node=1, independent_nodes=[2, 3], cm=0b000111)
    process = connector.to_kratos_process(model_part_name="Structure")

    assert process["python_module"] == "impose_rbe2_process"
    assert process["kratos_module"] == "StructuralMechanicsApplication"
    assert process["process_name"] == "ImposeRBE2Process"

    parameters = process["Parameters"]
    assert parameters["model_part_name"] == "Structure"
    assert parameters["dependent_node"] == 1
    assert parameters["independent_nodes"] == [2, 3]
    assert parameters["constrained_dofs"] == ["DISPLACEMENT_X", "DISPLACEMENT_Y", "DISPLACEMENT_Z"]
    assert parameters["interval"] == [0.0, "End"]


def test_to_kratos_process_empty_independent_nodes():
    connector = RBE2Connector(dependent_node=1, independent_nodes=[], cm=0b001111)
    with pytest.raises(ValueError, match="Independent nodes list cannot be empty."):
        connector.to_kratos_process(model_part_name="Structure")


def test_to_kratos_process_no_constrained_dofs():
    connector = RBE2Connector(dependent_node=1, independent_nodes=[2, 3], cm=0)
    with pytest.raises(ValueError, match="No constrained DOFs specified in CM bitmask."):
        connector.to_kratos_process(model_part_name="Structure")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
