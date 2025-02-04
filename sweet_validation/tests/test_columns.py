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


def test_len():
    field = IntegerField(name="test")
    items = [1, 2, 3]
    col = Column(field=field, items=items)
    assert len(col) == 3


def test_getattr():
    field = IntegerField(name="test", description="A test column")
    items = [1, 2, 3]
    col = Column(field=field, items=items)
    # attributes from the Field object
    assert col.name == "test"
    assert col.type == "integer"
    assert col.description == "A test column"
    # attributes from the Column object
    assert col.items == items
    assert col.field == field
    with pytest.raises(AttributeError):
        _ = col.not_an_attribute
