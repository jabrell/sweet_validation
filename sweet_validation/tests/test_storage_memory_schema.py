import pytest

from sweet_validation.storage import MemorySchemaStorage


def test_init():
    storage = MemorySchemaStorage()
    assert storage._data == {}
    assert storage._relations == {}
    storage = MemorySchemaStorage(
        data={"key": "value"}, relations={"key": ["other_key"]}
    )
    assert storage._data == {"key": "value"}
    assert storage._relations == {"key": ["other_key"]}
    # empty dict is initialized with data keys
    storage = MemorySchemaStorage(data={"key": "value"}, relations={})
    assert storage._data == {"key": "value"}
    assert storage._relations == {"key": []}


def test_init_raises():
    with pytest.raises(KeyError):
        MemorySchemaStorage(data={"key": "value"}, relations={"key2": []})
    with pytest.raises(KeyError):
        MemorySchemaStorage(data={"key": "value"}, relations={"key": [], "key2": []})
    with pytest.raises(KeyError):
        MemorySchemaStorage(
            data={"key": "value", "key3": "value"}, relations={"key": ["key2"]}
        )
    with pytest.raises(TypeError):
        MemorySchemaStorage(data={"key": "value"}, relations={"key": "other_key"})


def test_save():
    storage = MemorySchemaStorage()
    storage.save("key", "value")
    assert storage._data == {"key": "value"}
    assert storage._relations == {"key": []}


def test_replace():
    storage = MemorySchemaStorage(data={"key": "value"})
    storage.replace("key", "new_value")
    assert storage._data == {"key": "new_value"}


def test_replace_raises():
    relations = {"key": ["other_key"]}
    storage = MemorySchemaStorage(data={"key": "value"}, relations=relations)
    with pytest.raises(KeyError):
        storage.replace("key", "value")
    # without raise_exception it should return the list of values to update
    to_update = storage.replace("key", "value", raise_exception=False)
    assert to_update == relations["key"]


def test_delete():
    storage = MemorySchemaStorage(data={"key": "value"})
    storage.delete("key")
    assert storage._data == {}
    assert storage._relations == {}


def test_delete_raises():
    storage = MemorySchemaStorage(
        data={"key": "value"}, relations={"key": ["other_key"]}
    )
    with pytest.raises(KeyError):
        storage.delete("key")


def test_get_key_for_data():
    storage = MemorySchemaStorage(
        data={"key": "value", "key2": "value2"},
        relations={
            "key": ["other_key", "other_key2"],
            "key2": ["other_key3", "other_key4"],
        },
    )
    assert storage.get_key_for_data("other_key3") == "key2"
    with pytest.raises(KeyError):
        storage.get_key_for_data("non_existing_key")


def test_get_schema_for_data():
    storage = MemorySchemaStorage(
        data={"key": "value", "key2": "value2"},
        relations={
            "key": ["other_key", "other_key2"],
            "key2": ["other_key3", "other_key4"],
        },
    )
    assert storage.get_schema_for_data("other_key3") == "value2"
    with pytest.raises(KeyError):
        storage.get_schema_for_data("non_existing_key")


def test_get_data_for_schema():
    storage = MemorySchemaStorage(
        data={"key": "value", "key2": "value2"},
        relations={
            "key": ["other_key", "other_key2"],
            "key2": ["other_key3", "other_key4"],
        },
    )
    assert storage.list_data_for_schema("key") == ["other_key", "other_key2"]
    with pytest.raises(KeyError):
        storage.list_data_for_schema("non_existing_key")


def test_relation_read_only():
    relations = {
        "key": ["other_key", "other_key2"],
        "key2": ["other_key3", "other_key4"],
    }
    storage = MemorySchemaStorage(
        data={"key": "value", "key2": "value2"},
        relations=relations,
    )
    rel = storage.relations
    rel["key"] = ["other_key3"]
    assert storage.relations == relations


def test_add_relation():
    storage = MemorySchemaStorage(
        data={"key": "value", "key2": "value2"},
        relations={
            "key": ["other_key", "other_key2"],
            "key2": ["other_key3", "other_key4"],
        },
    )
    storage.add_relation("key", "other_key3")
    assert storage._relations == {
        "key": ["other_key", "other_key2", "other_key3"],
        "key2": ["other_key3", "other_key4"],
    }
    with pytest.raises(KeyError):
        storage.add_relation("non_existing_key", "other_key3")


def test_delete_relation():
    storage = MemorySchemaStorage(
        data={"key": "value", "key2": "value2"},
        relations={
            "key": ["other_key", "other_key2"],
            "key2": ["other_key3", "other_key4"],
        },
    )
    storage.delete_relation("key", "other_key")
    assert storage._relations == {
        "key": ["other_key2"],
        "key2": ["other_key3", "other_key4"],
    }
    with pytest.raises(KeyError):
        storage.delete_relation("key", "non_existing_key")
    with pytest.raises(KeyError):
        storage.delete_relation("non_existing_key", "other_key")
