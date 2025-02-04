from collections.abc import Iterable
from typing import Any

from frictionless import Field, Report, Resource, Schema

from sweet_validation.exceptions import ValidationError

__all__ = ["Column"]


class Column:
    """A column is defined as a list of items and a frictionless Field object.

    Columns roughly behave like lists but is checked against the Field object.

    Attributes:
        field (Field): A frictionless Field object.
        items (list): A list of items.
    """

    _items: list[Any]

    def __init__(self, field: Field, items: list[Any] | None = None):
        self.field = field
        if items:
            self._raise_on_validation(items=items)
        self._items = items or []

    @property
    def items(self) -> list[Any]:
        """Return the items of the column."""
        return self._items

    @items.setter
    def items(self, items: list[Any]) -> None:
        """Set the items of the column."""
        raise AttributeError("Cannot set the items of a column. Use append or extend")

    @property
    def name(self) -> str:
        """Return the name of the column defined in the field object"""
        return self.field.name

    @name.setter
    def name(self, name: str) -> None:
        raise AttributeError(
            "Cannot set the name of a column. Set the name of the field object instead."
        )

    @property
    def description(self) -> str | None:
        """Return the description of the column defined in the field object"""
        return self.field.description

    @description.setter
    def description(self, description: str) -> None:
        raise AttributeError(
            "Cannot set the description of a column. Set the description of the field object instead."  # noqa
        )

    @property
    def type(self) -> str:
        """Return the type of the column defined in the field object"""
        return self.field.type

    @type.setter
    def type(self, type: str) -> None:
        """Set the type of the column defined in the field object"""
        raise AttributeError(
            "Cannot set the type of a column. Set the type of the field object instead."
        )

    def append(self, item: Any) -> None:
        """Append an item to the column items.

        Args:
            item (Any): An item to append to the column items.

        Raises:
            ValidationError: If the item is not valid.
        """
        new_items = self.items + [item]
        self._raise_on_validation(items=new_items)
        self._items = new_items

    def extend(self, items: Iterable[Any]) -> None:
        """Extend the column items with a list of items.

        Args:
            items (list): A list of items to extend the column items.

        Raises:
            ValidationError: If the items are not valid.
        """
        new_items = self.items + list(items)
        self._raise_on_validation(items=new_items)
        self._items = new_items

    def _raise_on_validation(self, items: list[Any] | None = None) -> None:
        """Raise a ValidationError if the items are not valid.

        Args:
            items (list): A list of items. If None, the column items are used.

        Raises:
            ValidationError: If the items are not valid.
        """
        items = items or self.items
        rep = self.validate_items(items=items)
        if not rep.valid:
            raise ValidationError(report=rep)

    def validate_items(self, items: list[Any] | None = None) -> Report:
        """Validate a list of items against the Field object.

        Args:
            items (list): A list of items.

        Raises:
            ValueError: If the items are not valid.
        """
        items = items or self.items
        return self.get_resource(items=items).validate()

    def get_resource(self, items: list[Any] | None) -> Resource:
        """Return a Resource object with the column items.

        Args:
            items (list): A list of items. If None, the column items are used."""
        items = items or self.items
        data = [[self.field.name]] + [[i] for i in items]
        return Resource(data=data, schema=Schema(fields=[self.field]))

    def __len__(self) -> int:
        """Returns the number of items"""
        return len(self.items)
