import pytest

from sweetvalidation.models import Column


def test_column_create():
    col = Column(ctype=int, name="test", description="test column")
    assert col.name == "test"
    assert col.description == "test column"
    assert col.ctype.__name__ == "int"


def test_column_create_w_items():
    col = Column(ctype=int, name="test", description="test column", items=[1, 2, 3])
    assert col.name == "test"
    assert col.description == "test column"
    assert col.ctype.__name__ == "int"
    assert col.items == [1, 2, 3]

    # should raise an error as multiple types are not allowed
    with pytest.raises(TypeError):
        Column(ctype=int, name="test", description="test column", items=[1, 2, "3"])


def test_column_add_items():
    col = Column(ctype=int, name="test", description="test column")
    col.append(1)
    col.append(2)
    col.append(3)
    assert col.items == [1, 2, 3]

    # should raise an error as multiple types are not allowed
    with pytest.raises(TypeError):
        col.append("3")


def test_column_expand():
    col = Column(ctype=int, name="test", description="test column")
    col.extend([1, 2, 3])
    assert col.items == [1, 2, 3]

    # should raise an error as multiple types are not allowed
    with pytest.raises(TypeError):
        col.extend([1, 2, "3"])


def test_column_get_item():
    col = Column(ctype=int, name="test", description="test column", items=[1, 2, 3])
    assert col[0] == 1
    assert col[1] == 2
    assert col[2] == 3
    # should raise index error
    with pytest.raises(IndexError):
        col[3]


def test_column_del_item():
    col = Column(ctype=int, name="test", description="test column", items=[1, 2, 3])
    del col[0]
    assert col.items == [2, 3]
    # should raise index error
    with pytest.raises(IndexError):
        del col[2]
    assert len(col) == 2


def test_column_contains():
    col = Column(ctype=int, name="test", description="test column", items=[1, 2, 3])
    assert 1 in col
    assert 4 not in col


def test_column_iter():
    col = Column(ctype=int, name="test", description="test column", items=[1, 2, 3])
    for i, item in enumerate(col):
        assert item == i + 1
