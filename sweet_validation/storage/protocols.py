from typing import Any, Protocol, runtime_checkable

__all__ = ["StorageProtocol", "SchemaRelationsProtocol", "SchemaStorageProtocol"]


# TODO - it would be better to have a more specific types for keys and values.
#        This would however require four type variables to specify the types of
#        the SchemaStorageProtocol.
# TODO should get rid SchemaStorage: All relations should be managed at the registry
#       level
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


@runtime_checkable
class SchemaRelationsProtocol(Protocol):
    """The SchemaStorageManagementProtocol defines the methods needed to manage
    the relations between schemas and data

    Attributes:
        relations: The relations between schemas and data

    Methods:
        get_key_for_data: Return the schema key for a data key.
        get_schema_for_data: Return the schema object for a data key.
        list_data_for_schema: List all data keys for a schema key.
        add_schema_for_data: Add a data schema relation.
        delete_relation: Delete a data schema relation.
    """

    relations: dict[Any, Any]

    def get_key_for_data(data_key: Any, **kwargs: Any) -> Any: ...
    def get_schema_for_data(data_key: Any, **kwargs: Any) -> Any: ...
    def list_data_for_schema(schema_key: Any, **kwargs: Any) -> list[Any]: ...
    def add_relation(schema_key: Any, data_key: Any, **kwargs: Any) -> None: ...
    def delete_relation(schema_key: Any, data_key: Any, **kwargs: Any) -> None: ...


@runtime_checkable
class SchemaStorageProtocol(StorageProtocol, SchemaRelationsProtocol, Protocol):
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
