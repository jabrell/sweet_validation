from pathlib import Path

import pytest
from sqlalchemy.exc import IntegrityError

from ..schema_manager import SchemaManager

db_file = Path("tmp.db")


@pytest.fixture(autouse=True, scope="module")
def cleanup_db_file():
    yield
    db_path = Path(db_file)  # Use Pathlib to represent the file
    if db_path.exists():
        db_path.unlink()  # Delete the file if it exists


@pytest.mark.parametrize("fn", [None, db_file])
def test_insert_schema(fn: str):
    relation_manager = SchemaManager(fn_db=fn)
    assert relation_manager.schemas == []
    relation_manager.add_schema(key="test")
    assert relation_manager.schemas == ["test"]
    # raise IntegrityError due to unique constraint of primary key
    with pytest.raises(IntegrityError):
        relation_manager.add_schema("test")
    relation_manager.clear_and_close()


@pytest.mark.parametrize("fn", [None, db_file])
def test_insert_data(fn: str):
    relation_manager = SchemaManager(fn_db=fn)
    relation_manager.add_schema(key="test")
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
    relation_manager = SchemaManager(fn_db=fn)
    relation_manager.add_schema(key="test")
    assert relation_manager.schemas == ["test"]
    relation_manager.delete_schema(key="test")
    assert relation_manager.schemas == []
    # raise exception due to foreign key constraint
    relation_manager.add_schema(key="test")
    relation_manager.insert_data(id="test", id_schema="test")
    with pytest.raises(IntegrityError):
        relation_manager.delete_schema(key="test")
    relation_manager.clear_and_close()


@pytest.mark.parametrize("fn", [None, db_file])
def test_delete_data(fn: str):
    relation_manager = SchemaManager(fn_db=fn)
    relation_manager.add_schema(key="test")
    relation_manager.insert_data(id="test", id_schema="test")
    assert relation_manager.list_data() == [("test", "test")]
    relation_manager.delete_data(id="test")
    assert relation_manager.list_data() == []
    relation_manager.clear_and_close()


@pytest.mark.parametrize("fn", [None, db_file])
def test_get_data_schema(fn: str):
    relation_manager = SchemaManager(fn_db=fn)
    relation_manager.add_schema(key="s_test")
    relation_manager.insert_data(id="test", id_schema="s_test")
    assert relation_manager.get_data_schema(id="test") == "s_test"
    relation_manager.clear_and_close()


def test_init_from_existing_db():
    relation_manager = SchemaManager(fn_db=db_file)
    relation_manager.add_schema(key="s_test")
    relation_manager.insert_data(id="test", id_schema="s_test")
    relation_manager.close()
    relation_manager2 = SchemaManager(fn_db=db_file)
    assert relation_manager2.get_data_schema(id="test") == "s_test"
    assert relation_manager2.schemas == ["s_test"]
    assert relation_manager2.list_data() == [("test", "s_test")]
    relation_manager2.clear_and_close()
