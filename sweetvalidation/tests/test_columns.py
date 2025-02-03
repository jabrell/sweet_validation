import numpy as np
import pytest

from sweetvalidation.models import BaseColumn
from sweetvalidation.models.exceptions import DuplicatedValueError, RequiredValueError


def test_column_create():
    col = BaseColumn(ctype=int, name="test", description="test column")
    assert col.name == "test"
    assert col.description == "test column"
    assert col.ctype.__name__ == "int"


def test_column_create_w_items():
    col = BaseColumn(ctype=int, name="test", description="test column", items=[1, 2, 3])
    assert col.name == "test"
    assert col.description == "test column"
    assert col.ctype.__name__ == "int"
    assert col.items == [1, 2, 3]

    # should raise an error as multiple types are not allowed
    with pytest.raises(TypeError):
        BaseColumn(ctype=int, name="test", description="test column", items=[1, 2, "3"])


def test_column_add_items():
    col = BaseColumn(ctype=int, name="test", description="test column")
    col.append(1)
    col.append(2)
    col.append(3)
    assert col.items == [1, 2, 3]

    # should raise an error as multiple types are not allowed
    with pytest.raises(TypeError):
        col.append("3")


def test_column_expand():
    col = BaseColumn(ctype=int, name="test", description="test column")
    col.extend([1, 2, 3])
    assert col.items == [1, 2, 3]

    # should raise an error as multiple types are not allowed
    with pytest.raises(TypeError):
        col.extend([1, 2, "3"])


def test_column_get_item():
    col = BaseColumn(ctype=int, name="test", description="test column", items=[1, 2, 3])
    assert col[0] == 1
    assert col[1] == 2
    assert col[2] == 3
    # should raise index error
    with pytest.raises(IndexError):
        col[3]


def test_column_del_item():
    col = BaseColumn(ctype=int, name="test", description="test column", items=[1, 2, 3])
    del col[0]
    assert col.items == [2, 3]
    # should raise index error
    with pytest.raises(IndexError):
        del col[2]
    assert len(col) == 2


def test_column_contains():
    col = BaseColumn(ctype=int, name="test", description="test column", items=[1, 2, 3])
    assert 1 in col
    assert 4 not in col


def test_column_iter():
    col = BaseColumn(ctype=int, name="test", description="test column", items=[1, 2, 3])
    for i, item in enumerate(col):
        assert item == i + 1


def test_column_unique():
    with pytest.raises(DuplicatedValueError):
        _ = BaseColumn(
            ctype=int,
            name="test",
            description="test column",
            allow_duplicates=False,
            items=[1, 2, 3, 3],
        )
    col = BaseColumn(
        ctype=int,
        name="test",
        description="test column",
        allow_duplicates=False,
        items=[1, 2, 3],
    )
    with pytest.raises(DuplicatedValueError):
        col.append(3)
    with pytest.raises(DuplicatedValueError):
        col.extend([3, 4, 5])


@pytest.mark.parametrize("null_value", [None, np.nan, ""])
def test_column_required(null_value):
    with pytest.raises(RequiredValueError):
        _ = BaseColumn(
            ctype=int,
            name="test",
            description="test column",
            allow_null=False,
            items=[1, 2, null_value],
        )
    col = BaseColumn(
        ctype=int,
        name="test",
        description="test column",
        allow_null=True,
        items=[1, 2, null_value],
    )
    assert col.items == [1, 2, null_value]
    col = BaseColumn(
        ctype=int,
        name="test",
        description="test column",
        allow_null=False,
        items=[1, 2, 3],
    )
    with pytest.raises(RequiredValueError):
        col.append(None)
    with pytest.raises(RequiredValueError):
        col.extend([None, 4, 5])
