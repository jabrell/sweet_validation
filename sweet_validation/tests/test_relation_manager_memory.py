from pathlib import Path

import pytest
from sqlalchemy.exc import IntegrityError

from ..relation_manager import RelationManager

db_file = Path("tmp.db")


@pytest.fixture(autouse=True, scope="module")
def cleanup_db_file():
    yield
    db_path = Path(db_file)  # Use Pathlib to represent the file
    if db_path.exists():
        db_path.unlink()  # Delete the file if it exists


@pytest.mark.parametrize("fn", [None, db_file])
def test_insert_schema(fn: str):
    relation_manager = RelationManager(fn=fn)
    assert relation_manager.list_schemas() == []
    relation_manager.insert_schema(id="test")
    assert relation_manager.list_schemas() == ["test"]
    # raise IntegrityError due to unique constraint of primary key
    with pytest.raises(IntegrityError):
        relation_manager.insert_schema("test")
    relation_manager.clear_and_close()


@pytest.mark.parametrize("fn", [None, db_file])
def test_insert_data(fn: str):
    relation_manager = RelationManager(fn=fn)
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


@pytest.mark.parametrize("fn", [None, db_file])
def test_delete_schema(fn: str):
    relation_manager = RelationManager(fn=fn)
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


@pytest.mark.parametrize("fn", [None, db_file])
def test_delete_data(fn: str):
    relation_manager = RelationManager(fn=fn)
    relation_manager.insert_schema(id="test")
    relation_manager.insert_data(id="test", id_schema="test")
    assert relation_manager.list_data() == [("test", "test")]
    relation_manager.delete_data(id="test")
    assert relation_manager.list_data() == []
    relation_manager.clear_and_close()


@pytest.mark.parametrize("fn", [None, db_file])
def test_get_data_schema(fn: str):
    relation_manager = RelationManager(fn=fn)
    relation_manager.insert_schema(id="s_test")
    relation_manager.insert_data(id="test", id_schema="s_test")
    assert relation_manager.get_data_schema(id="test") == "s_test"
    relation_manager.clear_and_close()


def init_from_existing_db():
    relation_manager = RelationManager(fn=db_file)
    relation_manager.insert_schema(id="s_test")
    relation_manager.insert_data(id="test", id_schema="s_test")
    relation_manager.close()
    relation_manager2 = RelationManager(fn=db_file)
    assert relation_manager2.get_data_schema(id="test") == "s_test"
    assert relation_manager2.list_schemas() == ["s_test"]
    assert relation_manager2.list_data() == [("test", "s_test")]
    relation_manager2.clear_and_close()
