from typing import Any

from sqlalchemy import Column, MetaData, Table, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Boolean, Date, DateTime, Float, Integer, Text, Time

__all__ = ["SqlStorage"]

map_db_types = {
    "sqlite": {
        "any": Text,
        "boolean": Boolean,
        "date": Date,
        "datetime": DateTime,
        "integer": Integer,
        "number": Float,
        "string": Text,
        "time": Time,
        "year": Integer,
    }
}


class SqlStorage:
    """The SQL storage uses a database to store the data."""

    def __init__(self, db_uri: str, echo_sql: bool = False) -> None:
        """Initialize the SQL storage.

        Args:
            db_uri: The URI of the database.
            echo_sql: Whether to echo SQL queries.
        """
        self.db_uri = db_uri
        self._engine = create_engine(db_uri, echo=echo_sql)
        self.metadata = MetaData()
        with self._engine.connect() as conn:
            self.metadata.reflect(conn)
        self.Session = sessionmaker(bind=self._engine)
        self.metadata.create_all(self._engine)

    @property
    def tables(self) -> list[str]:
        """Return a list of table names in the database."""
        return list(self.metadata.tables.keys())

    def create_table(self, schema: dict[str, Any]) -> None:
        """Create a table in the database form a given schema.

        The schema must have a "name" key and a "fields" key. The "fields" are
        used to create the columns of the table. The "name" is used as the name
        of the table.

        Args:
            schema: The schema to create the table from. It has to be given as
                dictionary with a "name" key and a "fields" key.
        """
        tbl_name = schema.get("name")
        if not tbl_name:
            raise ValueError("The schema must have a 'name' key")
        fields = schema.get("fields")
        if not fields:
            raise ValueError(
                "The schema must have a 'fields' key with at least one field"
            )

        # check wether the table already exists
        if tbl_name in self.tables:
            raise ValueError(f"Table '{tbl_name}' already exists")

        # create columns
        # TODO include constraints here
        db_types = map_db_types[self._engine.dialect.name]
        cols = []
        for field in fields:
            name = field.get("name")
            if not name:
                raise ValueError("Each field must have a 'name' key")
            type_ = field.get("type")
            if not type_:
                raise ValueError(f"The field '{name}' must have a 'type' key")
            db_type = db_types.get(type_)
            if not db_type:
                raise ValueError(
                    f"Type '{type_}' not supported by database flavor '{self._engine.dialect.name}'"  # noqa
                )
            cols.append(Column(name=name, type_=db_type))

        # create the table object
        table = Table(tbl_name, self.metadata, *cols)
        with self._engine.begin() as conn:
            self.metadata.create_all(conn, tables=[table])

    def delete_table(self, table_name: str) -> None:
        """Delete a table from the database.

        Args:
            table_name: The name of the table to delete.
        """
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        table = self.metadata.tables[table_name]
        with self._engine.begin() as conn:
            self.metadata.drop_all(conn, tables=[table])
            self.metadata.remove(table)

    def _close_engine(self) -> None:
        """Close the database engine."""
        self._engine.dispose()
        self._engine = None
