import pytest

from sweet_validation.storage import MemoryStorage


def test_init():
    storage = MemoryStorage()
    assert storage._data == {}
    storage = MemoryStorage(data={"key": "value"})
    assert storage._data == {"key": "value"}


def test_load():
    storage = MemoryStorage(data={"key": "value"})
    assert storage.load("key") == "value"


def test_load_raises():
    storage = MemoryStorage()
    with pytest.raises(KeyError):
        storage.load("key")


def test_save():
    storage = MemoryStorage()
    storage.save("key", "value")
    assert storage._data == {"key": "value"}


def test_save_raises():
    storage = MemoryStorage(data={"key": "value"})
    with pytest.raises(KeyError):
        storage.save("key", "value")


def test_replace():
    storage = MemoryStorage(data={"key": "value"})
    storage.replace("key", "new_value")
    assert storage._data == {"key": "new_value"}


def test_replace_raises():
    storage = MemoryStorage()
    with pytest.raises(KeyError):
        storage.replace("key", "value")


def test_delete():
    storage = MemoryStorage(data={"key": "value"})
    storage.delete("key")
    assert storage._data == {}


def test_delete_raises():
    storage = MemoryStorage()
    with pytest.raises(KeyError):
        storage.delete("key")


def test_exists():
    storage = MemoryStorage(data={"key": "value"})
    assert storage.exists("key")
    assert not storage.exists("key2")


def test_list():
    storage = MemoryStorage(data={"key": "value", "key2": "value2"})
    assert storage.list() == ["key", "key2"]
