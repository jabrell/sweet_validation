from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from frictionless import Schema

from sweet_validation.items import ValidatedValues
from sweet_validation.storage import Storage

# Define a type variable for allowed schemas currently bound to only allow for
# frictionless schemas
AllowedSchema = TypeVar("AllowedSchema", bound=Schema)


class Registry(ABC, Generic[AllowedSchema]):
    """Abstract class for data registry

    A registry provides access to data and schemas that describe the data and
    can be used to validate the data. For this the registry uses two separate
    storage backends, one for the data and one for the schemas. The registry
    maintains the link between data and respective schemas and allows to get
    data with the schema but also single columns together with their description.

    The registry enforces a schema standard and currently we only support the
    frictionless schema standard.

    Attributes:
        schema_storage (Storage): A storage backend for schemas.
        data_storage (Storage): A storage backend for data.
        schemas (list): A list of schema keys.

    """

    @property
    @abstractmethod
    def schemas(self) -> list[Any]:
        """Return a list of schema keys."""

    @property
    @abstractmethod
    def schema_storage(self) -> Storage:
        """Return the schema storage backend."""
        raise NotImplementedError

    @property
    @abstractmethod
    def data_storage(self) -> Storage:
        """Return the data storage backend."""
        raise NotImplementedError

    @abstractmethod
    def get_schema(self, key: Any) -> AllowedSchema:
        """Return a schema object by key.

        Args:
            key (Any): The key of the schema.

        Returns:
            AllowedSchema: The schema object.
        """
        raise NotImplementedError

    @abstractmethod
    def save_schema(self, key: Any, schema: AllowedSchema) -> None:
        """Save a schema object by key.

        Args:
            key (Any): The key of the schema.
            schema (Schema): The schema object.

        Raises:
            KeyError: If the schema already exists.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_schema(self, key: Any) -> None:
        """Delete a schema object by key.

        Args:
            key (Any): The key of the schema.

        Raises:
            KeyError: If the schema does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def update_schema(self, key: Any, schema: AllowedSchema) -> None:
        """Update a schema object by key.

        Note that updating a schema object must trigger a re-validation of all
        data objects that are linked to this schema to ensure consistency.

        Args:
            key (Any): The key of the schema.
            schema (AllowedSchema): The schema object.

        Raises:
            KeyError: If the schema does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def get_data(self, key: Any) -> ValidatedValues:
        """Return a data object by key.

        Args:
            key (Any): The key of the data.

        Returns:
            ValidatedValues: The data object.

        Raises:
            KeyError: If the data does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def save_data(self, key: Any, data: ValidatedValues) -> None:
        """Save a data object by key.

        Args:
            key (Any): The key of the data.
            data (ValidatedValues): The data object.

        Raises:
            KeyError: If the data already exists.
        """
        raise NotImplementedError

    def delete_data(self, key: Any) -> None:
        """Delete a data object by key.

        Args:
            key (Any): The key of the data.

        Raises:
            KeyError: If the data does not exist.
        """
        raise NotImplementedError

    def update_data(self, key: Any, data: ValidatedValues) -> None:
        """Update a data object by key.

        Args:
            key (Any): The key of the data.
            data (ValidatedValues): The data object.

        Raises:
            KeyError: If the data does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def get_column_data(self, data: Any, column: Any) -> ValidatedValues:
        """Return a column object by key.

        Args:
            data (Any): The key of the data source object
            column (Any): The key of the column.

        Returns:
            ValidatedValues: The column object.

        Raises:
            KeyError: If the column does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def get_data_schema(self, key: Any) -> AllowedSchema:
        """Return the schema object for a data object by key.

        Args:
            key (Any): The key of the data.

        Returns:
            AllowedSchema: The schema object.

        Raises:
            KeyError: If the data does not exist.
        """
        raise NotImplementedError
