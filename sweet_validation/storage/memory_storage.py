from copy import deepcopy
from typing import Any

from .storage import Storage

__all__ = ["MemoryStorage"]


class MemoryStorage(Storage):
    """A storage backend that stores data in memory.

    This storage uses a dictionary to store data in memory given a key under which
    the data are stored.

    """

    _data: dict[str, Any]

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        """Initialize the storage backend

        Args:
            data (dict[str, Any], optional): A dictionary of data to initialize t
                he storage with. Defaults to None.
        """
        super().__init__()
        self._data = {}
        if data:
            self._data = deepcopy(data)

    def save(self, key: str, value: Any) -> None:
        """Save a value to the storage

        Args:
            key (str): The key of the value
            value (Any): The value to save

        Raises:
            KeyError: If the key already exists
        """
        if self.exists(key):
            raise KeyError(f"Key '{key}' already exists")
        self._data[key] = value

    def load(self, key: str) -> Any:
        """Load a value from the storage

        Args:
            key (str): The key of the value

        Returns:
            Any: The value stored at the key

        Raises:
            KeyError: If the key does not exist
        """
        return self._data[key]

    def delete(self, key: str) -> None:
        """Delete a value from the storage

        Args:
            key (str): The key of the value

        Raises:
            KeyError: If the key does not exist
        """
        del self._data[key]

    def exists(self, key: str) -> bool:
        """Check if a value exists in the storage

        Args:
            key (str): The key of the value

        Returns:
            bool: True if the key exists, False otherwise
        """
        return key in self._data

    def list(self) -> list[str]:
        """List all keys in the storage

        Returns:
            list[str]: A list of all keys in the storage
        """
        return list(self._data.keys())
