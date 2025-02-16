import pytest

from sweet_validation.exceptions import DataValidationError
from sweet_validation.registry import InMemoryRegistry
from sweet_validation.schema_manager import SchemaManager
from sweet_validation.validator.dummy import DummyValidator

from .schemas import valid_schema, valid_schema2


def test_add_schema():
    registry = InMemoryRegistry(
        validator=DummyValidator(), schema_manager=SchemaManager()
    )
    registry.add_schema("key", valid_schema)
    assert registry.schemas == ["key"]
    assert registry.get_schema("key") == valid_schema
    # already exists so KeyError is raised
    with pytest.raises(KeyError):
        registry.add_schema("key", valid_schema)


def test_add_data():
    registry = InMemoryRegistry(
        validator=DummyValidator(), schema_manager=SchemaManager()
    )
    # raise KeyError if schema does not exist
    with pytest.raises(KeyError):
        registry.add_data("dkey", "lkey", data="data")

    registry.add_schema("skey", valid_schema)
    registry.add_data("dkey", "skey", data="data")
    assert registry.list_data() == [("dkey", "skey")]
    assert registry.get_data("dkey") == "data"
    # Schema does not exist so KeyError is raised
    with pytest.raises(KeyError):
        registry.add_data("dkey", "skey2", data="data")
    # Data already exists so KeyError is raised
    with pytest.raises(KeyError):
        registry.add_data("dkey", "skey", data="data")


def test_add_data_raises_validation_error():
    registry = InMemoryRegistry(
        validator=DummyValidator(response=False), schema_manager=SchemaManager()
    )
    registry.add_schema("skey", valid_schema)
    with pytest.raises(DataValidationError):
        registry.add_data("dkey", "skey", data="data")


def test_delete_schema():
    registry = InMemoryRegistry(
        validator=DummyValidator(), schema_manager=SchemaManager()
    )
    # raise KeyError if schema does not exist
    with pytest.raises(KeyError):
        registry.delete_schema("key")

    # raise ValueError if data associated with schema still exist
    registry.add_schema("skey", valid_schema)
    registry.add_data("dkey", "skey", data="data")
    with pytest.raises(ValueError):
        registry.delete_schema("skey")

    # deleting data allows to delete schema and schema list is empty
    registry.delete_data("dkey")
    registry.delete_schema("skey")
    assert registry.schemas == []


def test_delete_data():
    registry = InMemoryRegistry(
        validator=DummyValidator(), schema_manager=SchemaManager()
    )
    # raise KeyError if data does not exist
    with pytest.raises(KeyError):
        registry.delete_data("key")

    registry.add_schema("skey", valid_schema)
    registry.add_data("dkey", "skey", data="data")
    registry.delete_data("dkey")
    assert registry.data == []


def test_replace_schema():
    registry = InMemoryRegistry(
        validator=DummyValidator(), schema_manager=SchemaManager()
    )
    # raise IntegrityError if schema does not exist
    with pytest.raises(KeyError):
        registry.replace_schema("key", valid_schema)
    registry.add_schema("skey", valid_schema)
    registry.add_data("dkey", "skey", data="data")
    registry.replace_schema("skey", valid_schema2)
    assert registry.get_schema("skey") == valid_schema2


def test_replace_schema_raise_validation_error():
    registry = InMemoryRegistry(
        validator=DummyValidator(response=True), schema_manager=SchemaManager()
    )
    registry.add_schema("skey", valid_schema)
    registry.add_data("dkey", "skey", data="data")
    registry._validator.response = False
    with pytest.raises(DataValidationError):
        registry.replace_schema("skey", valid_schema2)


def test_replace_data():
    registry = InMemoryRegistry(
        validator=DummyValidator(), schema_manager=SchemaManager()
    )
    # raise KeyError if data does not exist
    with pytest.raises(KeyError):
        registry.replace_data("key", "data")

    registry.add_schema("skey", valid_schema)
    registry.add_data("dkey", "skey", data="data")
    registry.replace_data("dkey", "new_data")
    assert registry.get_data("dkey") == "new_data"


def test_replace_data_raise_validation_error():
    registry = InMemoryRegistry(
        validator=DummyValidator(response=True), schema_manager=SchemaManager()
    )
    registry.add_schema("skey", valid_schema)
    registry.add_data("dkey", "skey", data="data")
    registry._validator.response = False
    with pytest.raises(DataValidationError):
        registry.replace_data("dkey", "new_data")
