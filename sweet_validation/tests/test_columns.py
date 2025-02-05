import pytest
from frictionless.fields import IntegerField

from sweet_validation.columns.columns import Column
from sweet_validation.exceptions import ValidationError


def test_init():
    field = IntegerField(name="test")
    items = [1, 2, 3]
    col = Column(field=field, items=items)
    assert col.field == field
    assert col.items == [1, 2, 3]


def test_init_wrong_types():
    field = IntegerField(name="test")
    items = [1, "b", "c"]
    with pytest.raises(ValidationError):
        _ = Column(field=field, items=items)


def test_init_constraints():
    field = IntegerField(name="test", constraints={"minimum": 1, "maximum": 3})
    items = [0, 2, 3, 5]
    with pytest.raises(ValidationError):
        _ = Column(field=field, items=items)


def test_immutable_field():
    field = IntegerField(name="test")
    items = [1, 2, 3]
    col = Column(field=field, items=items)
    with pytest.raises(AttributeError):
        col.field = IntegerField(name="another_test")


def test_immutable_items():
    field = IntegerField(name="test")
    items = [1, 2, 3]
    col = Column(field=field, items=items)
    new_items = col.items
    new_items.append(4)
    assert col.items == [1, 2, 3]
    col.items = new_items
    assert col.items == [1, 2, 3, 4]


def test_is_valid():
    field = IntegerField(name="test", constraints={"minimum": 1, "maximum": 3})
    items = [1, 2, 3]
    col = Column(field=field, items=items)
    assert col.is_valid()
    items = [0, 2, 3, 5]
    with pytest.raises(ValidationError):
        col.is_valid(items=items)
    assert not col.is_valid(items=items, raise_exception=False)
