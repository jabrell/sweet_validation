from typing import Any

from ..schema_manager import SchemaManager
from ..storage import InMemoryStorage


class InMemoryRegistry:
    _schema_manager: SchemaManager
    _data_store: InMemoryStorage
    _validator: Any

    def __init__(self, validator: Any, schema_manager: SchemaManager) -> None:
        """Initialize the registry with schema manager and storage

        Args:
            validator (Any): Validator to validate data against schema
            fn_schema_db (str | None, optional): Filename of schema database.
                Defaults to None.
        """
        self._schema_manager = schema_manager
        self._validator = validator
        self._data_store = InMemoryStorage()

    # -------- schema related methods
    def add_schema(self, key: str, schema: Any) -> None:
        """Add schema to the registry. The schema is validated against the metadata
        standard. If the schema already exists, a KeyError is raised.

        Args:
            key (str): Key of schema
            schema (Any): Schema to be added

        Raises:
            KeyError: If the schema already exists
        """
        # TODO check schema against metadata standard
        # --> Done by schema manager?
        self._schema_manager.add_schema(key=key, schema=schema)

    def get_schema(self, key: str) -> Any:
        """Given the key of schema, return the schema

        Args:
            key (str): Key of schema

        Returns:
            Any: Schema

        Raises:
            KeyError: If the schema does not exist
        """
        return self._schema_manager[key]

    def delete_schema(self, key: str) -> None:
        """Given the key of schema delete it

        Args:
            key (str): Key of schema to delete

        Raises:
            IntegrityError: If the schema does not exist or data associated with
                the schema still exist
        """
        self._schema_manager.delete_schema(key=key)

    def replace_schema(self, key: str, schema: Any) -> None:
        """Replace a schema in the registry

        Args:
            key (str): Key of schema
            schema (Any): New schema

        Raises:
            KeyError: If the schema does not exist
        """
        # ensure that new schema is valid
        self._schema_manager.validate_schema(schema)
        for data_key in self._schema_manager.list_data_for_schema(key):
            data = self.get_data(data_key)
            self._validate_data(data=data, schema=schema)
        # replacement
        self._schema_manager.replace_schema(key, schema)

    @property
    def schemas(self) -> list[str]:
        """List all schemas

        Returns:
            list[str]: List of schema keys
        """
        return self._schema_manager.schemas

    # -------- data related methods
    def add_data(self, key: str, schema_key: str, data: Any) -> None:
        """Add data to the registry. The data is validated given the schema.

        Args:
            key (str): Key of data
            schema_key (str): Key of schema
            data (Any): Data to be added

        Raises:
            KeyError: If the schema does not exist
        """
        if key in self._schema_manager.data:
            raise KeyError(f"Data {key} already exists")
        if schema_key not in self.schemas:
            raise KeyError(f"Schema {schema_key} does not exist")
        # validate data
        self._validate_data(data=data, schema=self.get_schema(schema_key))
        # add data
        self._schema_manager.add_data(key=key, key_schema=schema_key)
        self._data_store.save(key, data)

    def get_data(self, key: str) -> Any:
        """Given the key of data, return the data

        Args:
            key (str): Key of data

        Returns:
            Any: Data

        Raises:
            KeyError: If the data does not exist
        """
        return self._data_store.load(key)

    def delete_data(self, key: str) -> None:
        """Given the key of data delete it

        Args:
            key (str): Key of data to delete

        Raises:
            IntegrityError: If the data does not exist
        """
        self._schema_manager.delete_data(key=key)
        self._data_store.delete(key)

    def replace_data(self, key: str, data: Any) -> None:
        """Replace a data in the registry

        Args:
            key (str): Key of data
            data (Any): New data

        Raises:
            KeyError: If the data does not exist
            ValidationError: If the data does not conform to the schema
        """
        schema = self._schema_manager.get_data_schema(key)
        # check data against schema
        self._validate_data(data=data, schema=schema)
        # replacement
        self._data_store.replace(key, data)

    def list_data(self) -> list[tuple[str, str]]:
        """List all data

        Returns:
            list[tuple[str, str]]: List of data tuples (id, id_schema)

        Raises:
            IntegrityError: If the data does not exist
        """
        return self._schema_manager.list_data()

    def _validate_data(self, data: Any, schema: dict[str, Any]) -> None:
        """Validate data against schema

        Args:
            data (Any): Data to be validated
            schema (dict[str, Any]): Schema to validate against

        Raises:
            ValueError: If data does not conform to schema
        """
        # check data against schema
        if not self._validator.is_valid(data, schema):
            raise ValueError("Data does not conform to schema")

    @property
    def data(self) -> list[str]:
        """List all data keys

        Returns:
            list[str]: List of data keys
        """
        return self._schema_manager.data
