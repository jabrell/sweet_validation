from typing import Any, Protocol, runtime_checkable

__all__ = [
    "StorageProtocol",
]


@runtime_checkable
class StorageProtocol(Protocol):
    """Protocol for storage backends

    Storage backends implement at the very least the following methods:

    Methods:
        save: Save a value to the storage backend.
        load: Load a value from the storage backend.
        delete: Delete a value from the storage backend.
        exists: Check if a value exists in the storage backend.
        list: List all keys in the storage backend.
        replace: Replace a value in the storage backend.
            This method is already implemented and calls delete and save.
    """

    def save(self, key: Any, value: Any, **kwargs: Any) -> None: ...
    def load(self, key: Any, **kwargs: Any) -> Any: ...
    def delete(self, key: Any, **kwargs: Any) -> Any: ...
    def exists(self, key: Any, **kwargs: Any) -> bool: ...
    def list(self) -> list[Any]: ...
    def replace(self, key: Any, value: Any, **kwargs: Any) -> Any: ...
