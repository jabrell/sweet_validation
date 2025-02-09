# import pytest  # noqa

# from ..registry import MemoryRegistry


# def test_schema_store():
#     registry = MemoryRegistry()
#     assert registry.schemas == []
#     registry.save_schema("test", {"type": "object"})
#     assert registry.schemas == ["test"]
#     assert registry.get_schema("test") == {"type": "object"}
#     registry.replace_schema("test", {"type": "string"})
#     assert registry.get_schema("test") == {"type": "string"}
#     registry.delete_schema("test")
#     assert registry.schemas == []


# def test_data_store():
#     registry = MemoryRegistry()
#     assert registry.data == []
#     registry.save_data("test", {"key": "value"})
#     assert registry.get_data("test") == {"key": "value"}
#     registry.replace_data("test", {"key": "new value"})
#     assert registry.get_data("test") == {"key": "new value"}
#     registry.delete_data("test")
#     assert registry.data == []
