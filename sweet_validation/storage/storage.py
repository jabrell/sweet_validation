from abc import ABC, abstractmethod
from copy import deepcopy
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
        replace: Replace a value in the storage backend.
            This method is already implemented and calls delete and save.
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

    def replace(self, key: Any, value: Any, **kwargs: Any) -> Any:
        """Update a value in the storage backend."""
        self.delete(key)
        self.save(key, value)


class SchemaStorage(Storage):
    """Abstract class for schema storage backends

    The SchemaStorage is a standard storage that in additionally stores information
    about the relation between schemas and data, i.e., which schema is associated
    with which data. To work with this relation, the SchemaStorage must implement
    additional methods:

    - get_key_for_data: Return the schema key for a data key.
    - get_schema_for_data: Return the schema object for a data key.
    - list_data_for_schema: List all data keys for a schema key.
    - add_schema_for_data: Add a data schema relation.
    - delete_relation: Delete a data schema relation.

    The relations are stored in an additional attribute which is readonly

    Attributes:
        relations


    Methods:
        save: Save a schema to the storage backend.
        load: Load a schema from the storage backend.
        delete: Delete a schema from the storage backend.
        exists: Check if a schema exists in the storage backend.
        list: List all schema keys in the storage backend.
        replace: Replace a value in the storage backend.
            This method is already implemented and calls delete and save.
        get_key_for_data: Return the schema key for a data key.
        get_schema_for_data: Return the schema object for a data key.
        list_data_for_schema: List all data keys for a schema key.
        add_schema_for_data: Add a data schema relation.
    """

    _relations: Any

    @property
    @abstractmethod
    def relations(self) -> Any:
        """Return the relations between schemas and data."""
        return deepcopy(self._relations)

    @abstractmethod
    def get_key_for_data(self, data_key: Any) -> Any:
        """Return the schema key for a data key."""
        raise NotImplementedError

    @abstractmethod
    def get_schema_for_data(self, data_key: Any) -> Any:
        """Return the schema for a data key."""
        # TODO Should we add an explicit return type here? It could frictionless
        # TODO schema or a more generic schema object.
        raise NotImplementedError

    @abstractmethod
    def list_data_for_schema(self, schema_key: Any) -> list[Any]:
        """List all data keys for a schema key."""
        raise NotImplementedError

    @abstractmethod
    def add_relation(self, schema_key: Any, data_key: Any) -> None:
        """Add a data schema relation."""
        raise NotImplementedError

    @abstractmethod
    def delete_relation(self, schema_key: Any, data_key: Any) -> None:
        """Delete a data schema relation."""
        raise NotImplementedError
