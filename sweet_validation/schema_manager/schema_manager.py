from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from .models import Base, Data, Schema  # Import your models

__all__ = ["SchemaManager"]


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
    The database has two tables: Schema and Data. Schema

    Attributes:
        engine (Engine): SQLAlchemy engine
        SessionLocal (sessionmaker): Session factory

    Methods:
        get_session: Provides a context-managed database session
        close_engine: Close the database engine
        insert_schema: Insert a schema into the database
        insert_data: Insert data into the database
        list_schemas: Fetch all schema keys
        list_data: Fetch all data
        delete_schema: Delete a schema given the key
        delete_data: Delete data given the key
        get_data_schema: Get the schema key associated with the data key
        close: Close the database engine
        clear_all: Clear all data in the database
        clear_and_close: Clear all data and close the database engine
    """

    _conn_str: str

    def __init__(self, fn: str | None = None) -> None:
        """Initialize the database engine and session factory
        Args:
            fn (str | None): Filename of the sqlite database
                Defaults to None, which uses an in-memory database
        """
        if fn:
            self._conn_str = f"sqlite:///{fn}"
        else:
            self._conn_str = "sqlite:///:memory:"

        self.engine = create_engine(self._conn_str)
        Base.metadata.create_all(self.engine)  # Create tables if they don't exist
        self.SessionLocal = sessionmaker(bind=self.engine)  # Create session factory

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Provides a context-managed database session."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e  # Re-raise after rollback
        finally:
            session.close()

    def close_engine(self) -> None:
        """Close the database engine."""
        self.engine.dispose()

    def insert_schema(self, id: str) -> None:
        """Insert a schema into the database given the key

        Args:
            id (str): Schema key

        Raises:
            IntegrityError: If the primary key is violated
        """
        with self.get_session() as session:
            session.add(Schema(id=id))
            session.commit()

    def insert_data(self, id: str, id_schema: str) -> None:
        """Insert data into the database given the key and key of associated schema

        Args:
            id (str): Data key
            id_schema (str): Schema key

        Raises:
            IntegrityError: If the primary key or foreign constraint is violated
        """
        with self.get_session() as session:
            session.add(Data(id=id, id_schema=id_schema))
            session.commit()

    def list_schemas(self) -> list[str]:
        """Fetch all schema keys

        Returns:
            list[str]: List of schema keys
        """
        with self.get_session() as session:
            return [schema.id for schema in session.query(Schema).all()]

    def list_data(self) -> list[tuple[str, str]]:
        """Fetch all data

        Returns:
            list[tuple[str, str]]: List of data tuples (id, id_schema)
        """
        with self.get_session() as session:
            return [(data.id, data.id_schema) for data in session.query(Data).all()]

    def delete_schema(self, id: str) -> None:
        """Delete a schema given the key

        Args:
            id (str): Schema key

        Raises:
            IntegrityError: If the foreign key constraint of data is violated,
                i.e. data associated with the schema still exist
        """
        with self.get_session() as session:
            session.query(Schema).filter(Schema.id == id).delete()
            session.commit()

    def delete_data(self, id: str) -> None:
        """Delete data given the key

        Args:
            id (str): Data key
        """
        with self.get_session() as session:
            session.query(Data).filter(Data.id == id).delete()
            session.commit()

    def get_data_schema(self, id: str) -> str:
        """Get the schema key associated with the data key

        Args:
            id (str): Data key

        raises:
            KeyError: If the data key does not exist

        Returns:
            str: Schema key
        """
        with self.get_session() as session:
            data = session.query(Data).filter(Data.id == id).first()
            if not data:
                raise KeyError(f"Data key '{id}' not found")
            return str(data.id_schema)

    def list_data_for_schema(self, id_schema: str) -> list[str]:
        """Get the data keys associated with the schema key

        Args:
            id_schema (str): Schema key

        Returns:
            list[str]: List of data keys
        """
        with self.get_session() as session:
            data = session.query(Data).filter(Data.id_schema == id_schema).all()
            return [str(d.id) for d in data]

    def close(self) -> None:
        self.close_engine()

    def clear_all(self) -> None:
        """Clear all data in the database"""
        with self.get_session() as session:
            session.query(Data).delete()
            session.query(Schema).delete()
            session.commit()

    def clear_and_close(self) -> None:
        self.clear_all()
        self.close()
