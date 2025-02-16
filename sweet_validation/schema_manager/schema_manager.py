from __future__ import annotations

import json
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Any, cast

import jsonschema
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from ..utils import read_schema_from_file
from .models import Base
from .models import Data as DataTable
from .models import Schema as SchemaTable

__all__ = ["SchemaManager"]


BASE_SCHEMA = Path(__file__).parent / "meta_schemas" / "frictionlessv1.json"


@event.listens_for(Engine, "connect")  # type: ignore
def set_sqlite_pragma(dbapi_connection: Any, connection_record: Any) -> None:
    """Enable foreign key support for SQLite connections

    Only needed for sqlite connections

    see: https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#foreign-key-support"""
    if (
        dbapi_connection.__class__.__module__ == "sqlite3"
    ):  # Check if it's an SQLite connection
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


__all__ = ["SchemaManager"]


class SchemaManager:
    """A simple relation manager based on SQLite

    The underlying database is in-memory if no filename is provided.
    If a filename is provided, the database is stored in the file.
    The database has two tables: Schema and Data. The schema table stores the
    schema key and the schema itself. The data table stores the data key and the
    schema key associated with the data. Note that data table does not store data
    but only the key to access the data.

    Attributes:
        schemas: List of schema keys

    Methods:
        # schema management methods
        add_schema: Insert a schema into the database
        delete_schema: Delete a schema given the key
        replace_schema: Replace a schema in the database
        list_data_for_schema: Get the data keys associated with the schema key

        # data management methods
        add_data: Insert data into the database
        list_data: Fetch all data keys
        delete_data: Delete data given the key
        get_data_schema: Get the schema key associated with the data key

        # db management methods
        get_session: Provides a context-managed database session
        close_engine: Close the database engine
        close: Close the database engine
        clear: Clear all tables in the database
        clear_and_close: Clear all data and close the database engine
    """

    key_meta_schema = "__meta_schema__"

    def __init__(
        self,
        fn_db: str | None = None,
        meta_schema: str | Path | dict[str, Any] | None = None,
    ) -> None:
        """Initialize the database engine and session factory
        Args:
            fn (str | None): Filename of the sqlite database
                Defaults to None, which uses an in-memory database
            meta_schema (str | Schema | None): Metadata schema for the database
                Defaults to None, which uses the default schema. If a string is
                provided it is assumed to be a path to a schema file in yaml format.
        """
        # create the meta-data schema
        # TODO allow for extensions of the base schema
        meta_schema = meta_schema or BASE_SCHEMA
        self._meta_schema: dict[str, Any] = read_schema_from_file(meta_schema)

        # self._meta_schema = self._create_schema_from_file(meta_schema)
        # create the engine and the tables
        conn_str = f"sqlite:///{fn_db}" if fn_db else "sqlite:///:memory:"
        self._init_db(conn_str)

        # check whether the meta-schema is in the database else create it
        try:
            self._meta_schema = self[self.key_meta_schema]
        except KeyError:
            self._write_schema_to_db(self.key_meta_schema, self._meta_schema)

    def _create_and_check_schema(
        self, schema: str | Path | dict[str, Any]
    ) -> dict[str, Any]:
        """Create a schema from file and return the scheme itself it is already a
        schema

        Args:
            schema (str | Path | dict[str, Any]): Schema
                If a string or pathlib.Path is provided, it is assumed to be the
                path to a schema file in json or yaml format

        Returns:
            dict[str, Any]: Schema
        """
        schema = read_schema_from_file(schema)
        self.validate_schema(schema)
        return schema

    # --------- schema management methods
    @property
    def schemas(self) -> list[str]:
        """Fetch all schema keys

        Returns:
            list[str]: List of schema keys
        """
        with self.get_session() as session:
            return [
                schema.id
                for schema in session.query(SchemaTable).all()
                if schema.id != self.key_meta_schema
            ]

    def __getitem__(self, key: str) -> dict[str, Any]:
        """Get the schema given the key

        Args:
            key (str): Schema key

        Raises:
            KeyError: If the schema key does not exist

        Returns:
            str: Schema
        """
        with self.get_session() as session:
            schema = session.query(SchemaTable).filter(SchemaTable.id == key).first()
            if not schema:
                raise KeyError(f"Schema key '{key}' not found")
            return cast(dict[str, Any], json.loads(schema.schema))

    def add_schema(self, key: str, schema: str | Path | dict[str, Any]) -> None:
        """Insert a schema into the database given the key

        Args:
            key (str): Schema key
            schema (str | Path | dict[str, Any]): Schema
                If a string or pathlib.Path is provided, it is assumed to be the
                path to a schema file in json or yaml format.

        Raises:
            KeyError: If the schema key already exists
        """
        if key in self.schemas:
            raise KeyError(f"Schema key '{key}' already exists")

        schema = self._create_and_check_schema(schema)

        # convert schema to json string and store in database
        self._write_schema_to_db(key, schema)

    def delete_schema(self, key: str) -> None:
        """Delete a schema given the key

        Args:
            key (str): Schema key

        Raises:
            KeyError: If schema does not exist
            ValueError: If some data is still associated with the schema
        """
        if key not in self.schemas:
            raise KeyError(f"Schema key '{key}' not found")
        if self.list_data_for_schema(key):
            raise ValueError(f"Data associated with schema key '{key}' still exists")
        with self.get_session() as session:
            session.query(SchemaTable).filter(SchemaTable.id == key).delete()
            session.commit()

    def replace_schema(self, key: str, schema: str | Path | dict[str, Any]) -> None:
        """Replace a schema in the database

        Args:
            key (str): Schema key
            schema (str | Schema): New schema

        Raises:
            KeyError: If the schema key does not exist
        """
        if key not in self.schemas:
            raise KeyError(f"Schema key '{key}' not found")

        schema = self._create_and_check_schema(schema)

        schema = json.dumps(schema)
        with self.get_session() as session:
            session.query(SchemaTable).filter(SchemaTable.id == key).update(
                {"schema": schema}
            )
            session.commit()

    def list_data_for_schema(self, key: str) -> list[str]:
        """Get the data keys associated with the schema key

        Args:
            key (str): Schema key

        Returns:
            list[str]: List of data keys
        """
        with self.get_session() as session:
            data = session.query(DataTable).filter(DataTable.id_schema == key).all()
            return [str(d.id) for d in data]

    def validate_schema(self, schema: str | Path | dict[str, Any]) -> None:
        """Check if a schema is valid given the metadata schema

        Args:
            schema (str | Path | dict[str, Any]): Schema to check
                If a string or pathlib.Path is provided, it is assumed to be the
                path to a schema file in json or yaml format.

        Raises:
            jsonschema.exceptions.ValidationError: If the schema is not valid
        """
        if isinstance(schema, str | Path):
            schema = read_schema_from_file(schema)
        jsonschema.validate(instance=schema, schema=self._meta_schema)

    def _write_schema_to_db(self, key: str, schema: dict[str, Any]) -> None:
        """Write a schema to the database

        Args:
            key (str): Schema key
            schema (dict[str, Any]): Schema
        """
        my_schema = json.dumps(schema)
        with self.get_session() as session:
            session.add(SchemaTable(id=key, schema=my_schema))
            session.commit()

    # --------- data management methods
    @property
    def data(self) -> list[str]:
        """List of all data keys

        Returns:
            list[str]: List of data keys
        """
        return [d[0] for d in self.list_data()]

    def add_data(self, key: str, key_schema: str) -> None:
        """Insert data into the database given the key and key of associated schema

        Args:
            key (str): Data key
            key_schema (str): Schema key

        Raises:
            KeyError: If the primary key or foreign constraint is violated
        """
        if key in self.data:
            raise KeyError(f"Data key '{key}' already exists")
        if key_schema not in self.schemas:
            raise KeyError(f"Schema key '{key_schema}' not found")
        with self.get_session() as session:
            session.add(DataTable(id=key, id_schema=key_schema))
            session.commit()

    def list_data(self) -> list[tuple[str, str]]:
        """Fetch all data

        Returns:
            list[tuple[str, str]]: List of data tuples (id, id_schema)
        """
        with self.get_session() as session:
            return [
                (data.id, data.id_schema) for data in session.query(DataTable).all()
            ]

    def delete_data(self, key: str) -> None:
        """Delete data given the key

        Args:
            key (str): Data key

        Raises:
            KeyError: If the data key does not exist
        """
        if key not in [d[0] for d in self.list_data()]:
            raise KeyError(f"Data key '{key}' not found")
        with self.get_session() as session:
            session.query(DataTable).filter(DataTable.id == key).delete()
            session.commit()

    def get_data_schema(self, key: str) -> dict[str, Any]:
        """Get the schema key associated with the data key

        Args:
            key (str): Data key

        raises:
            KeyError: If the data key does not exist

        Returns:
            str: Schema
        """
        key_schema = self.get_data_schema_key(key)
        return self[key_schema]

    def get_data_schema_key(self, key: str) -> str:
        """Get the schema key associated with the data key

        Args:
            key (str): Data key

        raises:
            KeyError: If the data key does not exist

        Returns:
            str: Schema key
        """
        with self.get_session() as session:
            data = session.query(DataTable).filter(DataTable.id == key).first()
            if not data:
                raise KeyError(f"Data key '{key}' not found")
            return str(data.id_schema)

    # --------- db management methods
    def _init_db(self, conn_str: str) -> None:
        """Initialize the database with the metadata schema

        Args:
            conn_str (str): Connection string to the database
        """
        self._conn_str = conn_str
        self._engine = create_engine(self._conn_str)
        Base.metadata.create_all(self._engine)  # Create tables if they don't exist
        self._SessionLocal = sessionmaker(bind=self._engine)  # Create session factory

    def _close_engine(self) -> None:
        """Close the database engine."""
        self._engine.dispose()
        self._engine = None

    def close(self) -> None:
        self._close_engine()

    def clear(self) -> None:
        """Clear all data in the database"""
        with self.get_session() as session:
            session.query(DataTable).delete()
            session.query(SchemaTable).delete()
            session.commit()

    def clear_and_close(self) -> None:
        self.clear()
        self.close()

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Provides a context-managed database session."""
        session = self._SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e  # Re-raise after rollback
        finally:
            session.close()
