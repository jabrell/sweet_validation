import json
from pathlib import Path

import pytest

from ..schema_manager import SchemaManager
from .schemas import valid_schema

db_file = Path("tmp.db")
dir_schema = Path(__file__).parent
valid_schema_file = dir_schema / "valid_schema.json"


@pytest.fixture(autouse=True, scope="module")
def cleanup_db_file():
    db_path = Path(db_file)
    if db_path.exists():
        db_path.unlink()

    yield

    db_path = Path(db_file)
    if db_path.exists():
        db_path.unlink()


@pytest.mark.parametrize("fn", [None, db_file])
def test_add_schema(fn: str):
    relation_manager = SchemaManager(fn_db=fn)
    assert relation_manager.schemas == []
    relation_manager.add_schema(key="test", schema=valid_schema)
    assert relation_manager.schemas == ["test"]
    assert relation_manager["test"] == valid_schema
    # raise KeyError due to unique constraint of primary key
    with pytest.raises(KeyError):
        relation_manager.add_schema("test", schema="content")
    relation_manager.clear_and_close()


@pytest.mark.parametrize("fn", [None, db_file])
def test_add_schema_from_file(fn: str):
    relation_manager = SchemaManager(fn_db=fn)
    with open(valid_schema_file, "w") as f:
        json.dump(valid_schema, f)
    relation_manager.add_schema(key="test", schema=valid_schema_file)
    assert relation_manager.schemas == ["test"]
    assert relation_manager["test"] == valid_schema
    valid_schema_file.unlink()
    relation_manager.clear_and_close()


@pytest.mark.parametrize("fn", [None, db_file])
def test_get_schema(fn: str):
    relation_manager = SchemaManager(fn_db=fn)
    relation_manager.add_schema(key="test", schema=valid_schema)
    assert relation_manager["test"] == valid_schema
    # raise KeyError if schema key does not exist
    with pytest.raises(KeyError):
        relation_manager["test2"]
    relation_manager.clear_and_close()


@pytest.mark.parametrize("fn", [None, db_file])
def test_delete_schema(fn: str):
    relation_manager = SchemaManager(fn_db=fn)
    relation_manager.add_schema(key="test", schema=valid_schema)
    assert relation_manager.schemas == ["test"]
    relation_manager.delete_schema(key="test")
    assert relation_manager.schemas == []
    # raise exception due to foreign key constraint
    relation_manager.add_schema(key="test", schema=valid_schema)
    relation_manager.add_data(key="test", key_schema="test")
    with pytest.raises(ValueError):
        relation_manager.delete_schema(key="test")
    # raise if schema key does not exist
    with pytest.raises(KeyError):
        relation_manager.delete_schema("test2")
    relation_manager.clear_and_close()


@pytest.mark.parametrize("fn", [None, db_file])
def test_get_data_schema(fn: str):
    relation_manager = SchemaManager(fn_db=fn)
    relation_manager.add_schema(key="s_test", schema=valid_schema)
    relation_manager.add_data(key="test", key_schema="s_test")
    assert relation_manager.get_data_schema(key="test") == valid_schema
    # raise KeyError if data key does not exist
    with pytest.raises(KeyError):
        relation_manager.get_data_schema("test2")
    relation_manager.clear_and_close()


@pytest.mark.parametrize("fn", [None, db_file])
def test_insert_data(fn: str):
    relation_manager = SchemaManager(fn_db=fn)
    relation_manager.add_schema(key="test", schema=valid_schema)
    relation_manager.add_data(key="test", key_schema="test")
    assert relation_manager.list_data() == [("test", "test")]
    # raise IntegrityError due to unique constraint of primary key
    with pytest.raises(KeyError):
        relation_manager.add_data("test", "test")
    # raise exception due to foreign key constraint
    with pytest.raises(KeyError):
        relation_manager.add_data("test2", "test2")
    relation_manager.clear_and_close()


@pytest.mark.parametrize("fn", [None, db_file])
def test_delete_data(fn: str):
    relation_manager = SchemaManager(fn_db=fn)
    relation_manager.add_schema(key="test", schema=valid_schema)
    relation_manager.add_data(key="test", key_schema="test")
    assert relation_manager.list_data() == [("test", "test")]
    relation_manager.delete_data(key="test")
    assert relation_manager.list_data() == []
    # raise if data key does not exist
    with pytest.raises(KeyError):
        relation_manager.delete_data("test")
    relation_manager.clear_and_close()


# TODO that likely needs to be revised to be more robust in terms of database
# is consistent with schema
def test_init_from_existing_db():
    relation_manager = SchemaManager(fn_db=db_file)
    relation_manager.add_schema(key="s_test", schema=valid_schema)
    relation_manager.add_data(key="test", key_schema="s_test")
    relation_manager.close()
    relation_manager2 = SchemaManager(fn_db=db_file)
    assert relation_manager2.get_data_schema(key="test") == valid_schema
    assert relation_manager2.schemas == ["s_test"]
    assert relation_manager2.list_data() == [("test", "s_test")]
    relation_manager2.clear_and_close()
