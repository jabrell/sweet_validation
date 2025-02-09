from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from .models import Base, Data, Schema  # Import your models

__all__ = ["MemoryRelationManager"]


@event.listens_for(Engine, "connect")  # type: ignore
def set_sqlite_pragma(dbapi_connection: Any) -> None:
    """Enable foreign key support for SQLite connections

    Only needed for sqlite connections

    see: https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#foreign-key-support"""
    if (
        dbapi_connection.__class__.__module__ == "sqlite3"
    ):  # Check if it's an SQLite connection
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


class MemoryRelationManager:
    _conn_str: str = "sqlite:///:memory:"  # Or your connection string

    def __init__(self) -> None:
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

        Returns:
            str: Schema key
        """
        with self.get_session() as session:
            data = session.query(Data).filter(Data.id == id).first()
            return str(data.id_schema)

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
