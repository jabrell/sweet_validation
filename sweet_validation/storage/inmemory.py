from copy import deepcopy
from typing import Any

__all__ = ["InMemoryStorage"]


class InMemoryStorage:
    """A storage backend that stores data in memory.

    This storage uses a dictionary to store data in memory given a key under which
    the data are stored.

    """

    _data: dict[str, Any]

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        """Initialize the storage backend

        Args:
            data (dict[str, Any], optional): A dictionary of data to initialize
                the storage with. Defaults to None.
        """
        super().__init__()
        self._data = deepcopy(data) if data else {}

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

    def replace(self, key: str, value: Any) -> None:
        """Replace a value in the storage

        Args:
            key (str): The key of the value
            value (Any): The new value

        Raises:
            KeyError: If the key does not exist
        """
        self.delete(key)
        self.save(key, value)


# class MemorySchemaStorage(InMemoryStorage):
#     """A schema storage backend that stores schemas in memory.

#     This storage uses a dictionary to store schemas in memory given a key under
#     which the schema is stored. Another dictionary is used to to store the
#     relation between data and schemas.

#     """

#     _relations: dict[str, list[Any]]

#     def __init__(
#         self,
#         data: dict[str, Any] | None = None,
#         relations: dict[str, Any] | None = None,
#     ) -> None:
#         """Initialize the storage backend

#         Args:
#             data (dict[str, Any], optional): A dictionary schemas to initialize.
#                 Defaults to None.
#             relations (dict[str, Any], optional): A dictionary of relations between
#                 data and schema keys. Defaults to None.
#         """
#         super().__init__(data=data)
#         relations = (
#             deepcopy(relations) if relations else {k: [] for k in self._data.keys()}
#         )
#         # check that relations have lists as values
#         for key, value in relations.items():
#             if not isinstance(value, list):
#                 raise TypeError(
#                     f"Relations must be a dictionary with lists as values: Key '{key}' has value '{value}'"  # noqa: E501
#                 )

#         # check that relations are consistent with the schemas provided in the
#         # data dictionary: Keys in relations must be in the schema data
#         for key in relations:
#             if key not in self._data:
#                 raise KeyError(
#                     f"Schema data and relation are not consistent: Key '{key}' not found in data"  # noqa: E501
#                 )
#         # and the other way around
#         for key in self._data:
#             if key not in relations:
#                 raise KeyError(
#                     f"Schema data and relation are not consistent: Key '{key}' not found in relations"  # noqa: E501
#                 )
#         self._relations = deepcopy(relations) if relations else {}

#     @property
#     def relations(self) -> dict[str, list[Any]]:
#         """Return the relations between schemas and data."""
#         return deepcopy(self._relations)

#     def save(self, key: str, value: Any) -> None:
#         """Save a schema to the storage

#         Args:
#             key (str): The key of the schema
#             value (Any): The schema to save

#         Raises:
#             KeyError: If the key already exists
#         """
#         super().save(key, value)
#         self._relations[key] = []

#     def delete(self, key: str) -> None:
#         """Delete a schema from the storage

#         Args:
#             key (str): The key of the schema

#         Raises:
#             KeyError: If the key does not exist
#         """
#         if key in self._relations and len(self._relations[key]) > 0:
#             raise KeyError(f"Cannot delete key '{key}' since it has relations")
#         super().delete(key)
#         del self._relations[key]

#     # ignore mypy error since we overload the parent method signature
#     def replace(  # type: ignore[override]
#         self,
#         key: str,
#         value: Any,
#         raise_exception: bool = True,
#     ) -> list[str]:
#         """Replace a schema in the storage

#         Args:
#             key (str): The key of the schema
#             value (Any): The new schema
#             raise_exception (bool, optional): Whether to raise an exception if
#                 the schema has associated data items. Defaults to True.
#             **kwargs: Additional keyword arguments are ignored

#         Returns:
#             list[str]: A list of keys for the associated data items that are
#                 affected by the replacement

#         Raises:
#             KeyError: If the key does not exist
#         """
#         if raise_exception and len(self._relations[key]) > 0:
#             raise KeyError(f"Key '{key}' has relations")
#         self._data[key] = value
#         return self._relations[key]

#     def get_key_for_data(self, data_key: str) -> str:
#         """Return the schema key for a data key.

#         Args:
#             data_key (str): The key of the data

#         Returns:
#             str: The key of the schema

#         Raises:
#             KeyError: If the data key does not exist
#         """
#         for key, value in self._relations.items():
#             if data_key in value:
#                 # one data item has exactly one schema key so directly return
#                 return key
#         raise KeyError(f"Data key '{data_key}' not found")

#     def get_schema_for_data(self, data_key: str) -> Any:
#         """Return the schema for a data key.

#         Args:
#             data_key (str): The key of the data

#         Returns:
#             Any: The schema for the data key

#         Raises:
#             KeyError: If the data or schema key does not exist
#         """
#         return self.load(self.get_key_for_data(data_key))

#     def list_data_for_schema(self, schema_key: str) -> list[Any]:
#         """List all data keys for a schema key.

#         Args:
#             schema_key (Astr): The key of the schema

#         Returns:
#             list[Any]: A list of data keys associated with the schema key

#         Raises:
#             KeyError: If the schema key does not exist
#         """
#         return self._relations[schema_key]

#     def delete_relation(self, schema_key: str, data_key: str) -> None:
#         """Delete a relation between schema and data.

#         Args:
#             schema_key (str): The key of the schema
#             data_key (str): The key of the data

#         Raises:
#             KeyError: If the schema or data key does not exist
#         """
#         try:
#             self._relations[schema_key].remove(data_key)
#         except ValueError:
#             raise KeyError(
#                 f"Data key '{data_key}' not found in schema '{schema_key}'"
#             ) from None

#     def add_relation(self, schema_key: str, data_key: str) -> None:
#         """Add a relation between schema and data. The schema has to exist before
#         a relation can be added.

#         Args:
#             schema_key (str): The key of the schema
#             data_key (str): The key of the data

#         Raises:
#             KeyError: If the schema or data key does not exist
#         """
#         self._relations[schema_key].append(data_key)
