from pathlib import Path
from typing import Any

import pytest

from sweet_validation.storage import SqlStorage

db_file = "test.db"


@pytest.fixture(autouse=True, scope="function")
def cleanup_db_file(db_file="test.db"):
    db_path = Path(db_file)
    if db_path.exists():
        db_path.unlink()

    yield

    db_path = Path(db_file)
    if db_path.exists():
        db_path.unlink()


@pytest.mark.parametrize(
    "schema, expected_exception",
    [
        ({"fields": [{"name": "username", "type": "string"}], "name": "test"}, None),
        # missing name
        ({"fields": [{"name": "username", "type": "string"}]}, ValueError),
        # missing fields
        ({"name": "test2"}, ValueError),
        # field misses type
        ({"fields": [{"name": "username"}], "name": "test2"}, ValueError),
        # field misses name
        ({"fields": [{"type": "string"}], "name": "test2"}, ValueError),
        # type is not supported
        (
            {"fields": [{"name": "username", "type": "unknown"}], "name": "test2"},
            ValueError,
        ),
    ],
)
def test_create_table(
    schema: dict[str, Any], expected_exception: Exception | None
) -> None:
    db_uri = f"sqlite:///{db_file}"
    storage = SqlStorage(db_uri)
    if expected_exception:
        with pytest.raises(expected_exception):
            storage.create_table(schema)
    else:
        storage.create_table(schema)
    storage._close_engine()


def test_create_table_already_exists() -> None:
    db_uri = f"sqlite:///{db_file}"
    storage = SqlStorage(db_uri)
    schema = {"fields": [{"name": "username", "type": "string"}], "name": "test"}
    storage.create_table(schema)
    with pytest.raises(ValueError):
        storage.create_table(schema)
    storage._close_engine()


def test_delete_table() -> None:
    db_uri = f"sqlite:///{db_file}"
    storage = SqlStorage(db_uri)
    schema = {"fields": [{"name": "username", "type": "string"}], "name": "test"}
    storage.create_table(schema)
    storage.delete_table("test")
    assert "test" not in storage.tables
    storage._close_engine()
    with pytest.raises(ValueError):
        storage.delete_table("test")


def test_db_reflection() -> None:
    db_uri = f"sqlite:///{db_file}"
    storage = SqlStorage(db_uri)
    schema = {"fields": [{"name": "username", "type": "string"}], "name": "test"}
    storage.create_table(schema)
    storage._close_engine()

    # reopen the storage
    storage2 = SqlStorage(db_uri)
    assert "test" in storage2.tables
    storage2._close_engine()
