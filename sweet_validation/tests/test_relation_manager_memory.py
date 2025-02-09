import pytest  # noqa

from sqlalchemy.exc import IntegrityError

from ..relation_manager import MemoryRelationManager


def test_insert_schema():
    relation_manager = MemoryRelationManager()
    assert relation_manager.list_schemas() == []
    relation_manager.insert_schema(id="test")
    assert relation_manager.list_schemas() == ["test"]
    # raise IntegrityError due to unique constraint of primary key
    with pytest.raises(IntegrityError):
        relation_manager.insert_schema("test")
    relation_manager.clear_and_close()


def test_insert_data():
    relation_manager = MemoryRelationManager()
    relation_manager.insert_schema(id="test")
    relation_manager.insert_data(id="test", id_schema="test")
    assert relation_manager.list_data() == [("test", "test")]
    # raise IntegrityError due to unique constraint of primary key
    with pytest.raises(IntegrityError):
        relation_manager.insert_data("test", "test")
    # raise exception due to foreign key constraint
    with pytest.raises(IntegrityError):
        relation_manager.insert_data("test2", "test2")
    relation_manager.clear_and_close()


def test_delete_schema():
    relation_manager = MemoryRelationManager()
    relation_manager.insert_schema(id="test")
    assert relation_manager.list_schemas() == ["test"]
    relation_manager.delete_schema(id="test")
    assert relation_manager.list_schemas() == []
    # raise exception due to foreign key constraint
    relation_manager.insert_schema(id="test")
    relation_manager.insert_data(id="test", id_schema="test")
    with pytest.raises(IntegrityError):
        relation_manager.delete_schema(id="test")
    relation_manager.clear_and_close()


def test_delete_data():
    relation_manager = MemoryRelationManager()
    relation_manager.insert_schema(id="test")
    relation_manager.insert_data(id="test", id_schema="test")
    assert relation_manager.list_data() == [("test", "test")]
    relation_manager.delete_data(id="test")
    assert relation_manager.list_data() == []
    relation_manager.clear_and_close()


def test_get_data_schema():
    relation_manager = MemoryRelationManager()
    relation_manager.insert_schema(id="s_test")
    relation_manager.insert_data(id="test", id_schema="s_test")
    assert relation_manager.get_data_schema(id="test") == "s_test"
    relation_manager.clear_and_close()
