import pytest
from sqlalchemy.exc import IntegrityError

from sweet_validation.registry import InMemoryRegistry


def test_add_schema():
    registry = InMemoryRegistry()
    registry.add_schema("key", "schema")
    assert registry.list_schemas() == ["key"]
    assert registry.get_schema("key") == "schema"
    # already exists so error is raised
    with pytest.raises(IntegrityError):
        registry.add_schema("key", "schema")


def test_add_data():
    registry = InMemoryRegistry()
    # raise IntegrityError if schema does not exist
    with pytest.raises(KeyError):
        registry.add_data("dkey", "lkey", data="data")

    registry.add_schema("skey", "schema")
    registry.add_data("dkey", "skey", data="data")
    assert registry.list_data() == [("dkey", "skey")]
    assert registry.get_data("dkey") == "data"
    # already exists so error is raised
    with pytest.raises(IntegrityError):
        registry.add_data("dkey", "skey", data="data")


def test_delete_schema():
    registry = InMemoryRegistry()
    # raise IntegrityError if schema does not exist
    with pytest.raises(KeyError):
        registry.delete_schema("key")

    # raise IntegrityError if data associated with schema still exist
    registry.add_schema("skey", "schema")
    registry.add_data("dkey", "skey", data="data")
    with pytest.raises(IntegrityError):
        registry.delete_schema("skey")

    # deleting data allows to delete schema and schema list is empty
    registry.delete_data("dkey")
    registry.delete_schema("skey")
    assert registry.list_schemas() == []


def test_delete_data():
    registry = InMemoryRegistry()
    # raise KeyError if data does not exist
    with pytest.raises(KeyError):
        registry.delete_data("key")

    registry.add_schema("skey", "schema")
    registry.add_data("dkey", "skey", data="data")
    registry.delete_data("dkey")
    assert registry.list_data() == []


def test_replace_schema():
    registry = InMemoryRegistry()
    # raise IntegrityError if schema does not exist
    with pytest.raises(KeyError):
        registry.replace_schema("key", "schema")
    registry.add_schema("skey", "schema")
    registry.add_data("dkey", "skey", data="data")
    registry.replace_schema("skey", "new_schema")
    assert registry.get_schema("skey") == "new_schema"


def test_replace_data():
    registry = InMemoryRegistry()
    # raise KeyError if data does not exist
    with pytest.raises(KeyError):
        registry.replace_data("key", "data")

    registry.add_schema("skey", "schema")
    registry.add_data("dkey", "skey", data="data")
    registry.replace_data("dkey", "new_data")
    assert registry.get_data("dkey") == "new_data"
