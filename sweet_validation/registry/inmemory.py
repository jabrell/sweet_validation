import logging
from typing import Any

from ..schema_manager import SchemaManager
from ..storage import InMemoryStorage


class InMemoryRegistry:
    manager: SchemaManager
    _schema_store: InMemoryStorage
    _data_store: InMemoryStorage

    def __init__(self) -> None:
        self.manager = SchemaManager()
        self._schema_store = InMemoryStorage()
        self._data_store = InMemoryStorage()

    def add_schema(self, key: str, schema: Any) -> None:
        """Add schema to the registry. The schema is validated against the metadata
        standard. If the schema already exists, an IntegrityError is raised.

        Args:
            key (str): Key of schema
            schema (Any): Schema to be added

        Raises:
            IntegrityError: If the schema already exists
        """
        # TODO check schema against metadata standard
        self.manager.add_schema(key=key, schema=schema)
        self._schema_store.save(key, schema)

    def get_schema(self, key: str) -> Any:
        """Given the key of schema, return the schema

        Args:
            key (str): Key of schema

        Returns:
            Any: Schema

        Raises:
            KeyError: If the schema does not exist
        """
        return self._schema_store.load(key)

    def delete_schema(self, key: str) -> None:
        """Given the key of schema delete it

        Args:
            key (str): Key of schema to delete

        Raises:
            IntegrityError: If the schema does not exist or data associated with
                the schema still exist
        """
        self.manager.delete_schema(key=key)
        self._schema_store.delete(key)

    def replace_schema(self, key: str, schema: Any) -> None:
        """Replace a schema in the registry

        Args:
            key (str): Key of schema
            schema (Any): New schema

        Raises:
            KeyError: If the schema does not exist
            ValidationError: If the schema does not conform to the metadata standard
        """
        # TODO check schema against metadata standard
        # TODO check data against schema
        for data_key in self.manager.list_data_for_schema(key):
            data = self.get_data(data_key)
            logging.info(f"Data: {data} Schema: {schema}")
        # TODO how to log schema changes. The old schema is not available after
        # replacement
        self._schema_store.replace(key, schema)

    def list_schemas(self) -> list[str]:
        """List all schemas

        Returns:
            list[str]: List of schema keys
        """
        return self.manager.schemas

    def add_data(self, key: str, schema_key: str, data: Any) -> None:
        """Add data to the registry. The data is validated given the schema.

        Args:
            key (str): Key of data
            schema_key (str): Key of schema
            data (Any): Data to be added

        Raises:
            IntegrityError: If the schema does not exist
            ValidationError: If the data does not conform to the schema
        """
        schema = self.get_schema(schema_key)
        # TODO check data against schema
        logging.info(f"Data: {data} Schema: {schema}")
        self.manager.insert_data(key=key, key_schema=schema_key)
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
        self.manager.delete_data(key=key)
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
        # TODO check data against schema
        # TODO how to log data changes. The old data is not available after
        schema = self.manager.get_data_schema(key)
        logging.info(f"Validating Data: {data} Schema: {schema}")
        # replacement
        self._data_store.replace(key, data)

    def list_data(self) -> list[tuple[str, str]]:
        """List all data

        Returns:
            list[tuple[str, str]]: List of data tuples (id, id_schema)

        Raises:
            IntegrityError: If the data does not exist
        """
        return self.manager.list_data()
