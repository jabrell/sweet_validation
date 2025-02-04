from abc import ABC, abstractmethod


class AbstractSchema(ABC):
    """Schema interface.
    A schema
    - is a description of the structure of data.
    - can be used to validate data and to serialize/deserialize data.
    - consists of three major parts
        - Metadata: Information that describe the data that follow the schema
        - Dimensions: Dimensions are columns that fix the domain of the data.
        - Value: A single value column that represent numerical values
    """

    # todo need to fix types here
    dimensions: list
    value: int
    metadata: dict


class AbstractSchemaRegistry(ABC):
    """Schema registry interface."""

    @abstractmethod
    def create(self, name: str):
        """Create a new schema."""
        raise NotImplementedError

    @abstractmethod
    def get(self, name: str) -> None:
        """Get a schema by name

        Args:
            name (str): The name of the schema.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, name: str) -> None:
        """Delete a schema by id.

        Args:
            name (str): The name of the schema.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, name: str) -> None:
        """Update a schema by name.

        Args:
            name (str): The name of the schema.
            schema (dict): The schema to update.
        """
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list:
        """List all schemas."""
        raise NotImplementedError
