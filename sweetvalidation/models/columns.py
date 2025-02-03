from collections.abc import Iterable
from typing import TypeVar

import numpy as np
from pydantic import BaseModel, Field, model_validator

from .exceptions import DuplicatedValueError, RequiredValueError

__all__ = ["BaseColumn"]
T = TypeVar("T")


class BaseColumn(BaseModel):
    """A column is defined by its name, type, and a human-understandable
       description of it. A column is assumed to one and exactly one type.

       A column behaves like a list that only allows a certain type and has
       additional metadata.

    Attributes:
        name (str): Name of the column
        ctype (Any): Type of the values in the column
        description (str): Description of the column content
        allow_duplicates (bool): Whether the column values are allowed to contain
            duplicates. Default is False. Note that null values are not considered
            duplicates.
        allow_null (bool): Whether null values are allowed in the column
        null_values (list): List of values that are considered null
    """

    name: str
    ctype: type[T]
    description: str
    items: list[T] | None = Field(default_factory=list)
    allow_duplicates: bool = Field(frozen=True, default=False)
    allow_null: bool = Field(frozen=True, default=False)
    # TODO allow for pandas null values
    null_values: list = [None, np.nan, ""]

    @model_validator(mode="after")
    def validate_items(self):
        for item in self.items:
            self._check_null(item)
            self._check_type(item)
        self._check_duplicates(self.items)

        return self

    def _check_type(self, value: T) -> None:
        """
        Check if the value is of the correct type and not in the list of null values.

        Args:
            value (Any): Value to be checked

        Raises:
            TypeError: If the value is not of the correct type
            RequiredValueError: If the value is in the list of null values
        """
        # exclude null values from type checking if allowed
        if self.allow_null and value in self.null_values:
            return
        if not isinstance(value, self.ctype):
            raise TypeError(f"Value must be of type {self.ctype.__name__}")

    def _check_null(self, value: T) -> None:
        """Check whether value is null and if null is allowed

        Args:
            value (Any): Value to be checked

        Raises:
            RequiredValueError: If the value is null and null is not allowed
        """
        if not self.allow_null and value in self.null_values:
            if not self.allow_null:
                raise RequiredValueError(self.name)

    def _check_duplicates(self, iterable: Iterable[T]) -> None:
        """Check if all values are unique

        Args:
            iterable (Iterable): Values to be checked

        Raises:
            DuplicatedValueError: If the values are not unique
        """
        if not self.allow_duplicates:
            # exclude null values from duplicates
            to_check = [item for item in iterable if item not in self.null_values]
            if len(set(to_check)) != len(to_check):
                raise DuplicatedValueError(self.name)

    def __getitem__(self, key: int) -> T:
        return self.items[key]

    def __delitem__(self, index):
        del self.items[index]

    def __iter__(self) -> Iterable[T]:
        return iter(self.items)

    def __contains__(self, item: type[T]) -> bool:
        return item in self.items

    def __len__(self) -> int:
        return len(self.items)

    def append(self, item: type[T]) -> None:
        self._check_null(item)
        self._check_type(item)
        if not self.allow_duplicates and item in self.items:
            raise DuplicatedValueError(self.name)
        self.items.append(item)

    def extend(self, iterable: Iterable[T]) -> None:
        for item in iterable:
            self._check_null(item)
            self._check_type(item)
        new_items = self.items + list(iterable)
        self._check_duplicates(new_items)
        self.items = new_items.copy()


class IntegerColumn(BaseColumn):
    """A column that only allows integers."""

    minimum: int | None = None
    maximum: int | None = None

    def __init__(self, name: str, description: str):
        super().__init__(name=name, ctype=int, description=description)
