from collections.abc import Iterable
from typing import TypeVar

from pydantic import BaseModel, Field, model_validator

__all__ = ["Column"]
T = TypeVar("T")


class Column(BaseModel):
    """A column is defined by its name, type, and a human-understandable
       description of it. A column is assumed to one and exactly one type.

       A column behaves like a list that only allows a certain type and has
       additional metadata.

    Attributes:
        name (str): Name of the column
        ctype (Any): Type of the values in the column
        description (str): Description of the column content
    """

    name: str
    ctype: type[T]
    description: str
    items: list[T] | None = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_items(self):
        for i, item in enumerate(self.items):
            if not isinstance(item, self.ctype):
                raise TypeError(
                    f"Item at index {i} must be of type {self.ctype.__name__}, but found {type(item).__name__}"  # noqa
                )
        return self

    def _check_type(self, value: T):
        if not isinstance(value, self.ctype):
            raise TypeError(f"Value must be of type {self.ctype.__name__}")

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
        self._check_type(item)
        self.items.append(item)

    def extend(self, iterable: Iterable[T]) -> None:
        if not all(isinstance(item, self.ctype) for item in iterable):
            raise TypeError(f"All elements must be of type {self.ctype.__name__}")
        self.items.extend(iterable)
