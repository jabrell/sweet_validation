from abc import ABC, abstractmethod
from typing import Any

__all__ = ["Storage"]


class Storage(ABC):
    """Abstract class for storage backends

    Storage backends implement at the very least the following methods:

    Methods:
        save: Save a value to the storage backend.
        load: Load a value from the storage backend.
        delete: Delete a value from the storage backend.
        exists: Check if a value exists in the storage backend.
        list: List all keys in the storage backend.
    """

    @abstractmethod
    def save(self, key: Any, value: Any) -> None:
        """Save a value to the storage backend."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def load(self, key: Any) -> Any:
        """Load a value from the storage backend."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def delete(self, key: Any) -> Any:
        """Delete a value from the storage backend."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def exists(self, key: Any) -> bool:
        """Check if a value exists in the storage backend."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def list(self) -> list[Any]:
        """List all keys in the storage backend."""
        raise NotImplementedError  # pragma: no cover
