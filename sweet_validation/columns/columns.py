from typing import Any

from frictionless import Field, Report, Resource, Schema

from sweet_validation.exceptions import ValidationError


class Column(list):
    """A column is defined as a list of items and a frictionless Field object.

    Columns behave like lists but the list is checked against the Field object.

    Attributes:
        field (Field): A frictionless Field object.
        items (list): A list of items.
    """

    field: Field
    items: list[Any] | None

    def __init__(self, field: Field, items: list[Any] = None):
        self.field = field
        self.items = items or []
        if items:
            rep = self.validate_items(items)
            if not rep.valid:
                raise ValidationError(report=rep)
        super().__init__(self.items)

    @property
    def name(self) -> str:
        """Return the name of the column defined in the field object"""
        return self.field.name

    @property
    def description(self) -> str | None:
        """Return the description of the column defined in the field object"""
        return self.field.description

    @property
    def type(self) -> str:
        """Return the type of the column defined in the field object"""
        return self.field.type

    def validate_items(self, items: list[Any] | None) -> Report:
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
