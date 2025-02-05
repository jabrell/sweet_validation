from typing import Any

from frictionless import Field, Report, Resource, Schema

from sweet_validation.exceptions import ValidationError

from .validated_items import ValidatedItems

__all__ = ["Column"]


class Column(ValidatedItems):
    """A column is defined as a list of items and a frictionless Field object.

    Columns roughly behave like lists but is checked against the Field object.

    Attributes:
        field (Field): A frictionless Field object.
            The field object defines the type and constraints of the column.
            It can only be modified during instantiation. Otherwise it is
            immutable.
        items (list): A list of items. The items are validated against the field object.
            items are immutable and can only be set during instantiation or by
            replacing the items (e.g., col.items = [1, 2, 3]) which triggers
            a validation check.

    Methods:
        is_valid: Raise a ValidationError if the items are not valid. It can also
            be used to validate a list of items against the Field object.
        validate_items: Validate a list of items against the Field object.
        get_resource: Return a frictionless Resource object with the column items.

    Raises:
        ValidationError: If the items are not valid given the Field object.
        AttributeError: If the fields are modified after instantiation.

    The field object defines the type and constraints of the column and is based
    on the frictionless.Field object. The items are validated against this field
    every time they are appended or extended.

    For more information on the Field object, see:
    - [Field types](https://framework.frictionlessdata.io/docs/fields/any.html)
        under "Data Fields"
    - [Constraints](https://specs.frictionlessdata.io/table-schema/#constraints)
    - [Table and Field Scheme standard](https://specs.frictionlessdata.io/table-schema/#constraints)

    Examples:

        ```python
        from frictionless.fields import IntegerField
        field = IntegerField(name="test", constraints={"minimum": 1, "maximum": 3})
        col = Column(field=field, items=[1, 2, 3])
        ```

        The field property is immutable and items can only be replaced by a new list.
        That means that you always receive a copy of items and fields and modifying
        these copies will not affect the original column.

        ```python
        from frictionless.fields import IntegerField
        field = IntegerField(name="test")
        col = Column(field=field, items=[1, 2, 3])
        print(col.items)  # returns [1, 2, 3]
        new_items = col.items
        new_items.append(4)
        print(col.items)  # still returns [1, 2, 3]
        col.items = new_items
        print(col.items)  # returns [1, 2, 3, 4]
        new_field = IntegerField(name="another_test") # raises AttributeError
        ```

    """

    _items: list[Any]
    _field: Field

    def __init__(self, field: Field, items: list[Any] | None = None):
        # first assign the field so the validation can be done, then call parent class
        self._field = field
        super().__init__(items=items)

    @property
    def field(self) -> Field:
        """Return the field object of the column."""
        return self._field

    @field.setter
    def field(self, field: Field) -> None:
        """Set the field object of the column."""
        raise AttributeError("Cannot reset the field. Create a new column instead.")

    def is_valid(
        self, items: list[Any] | None = None, raise_exception: bool = True
    ) -> bool:
        """Raise a ValidationError if the items are not valid.

        Args:
            items (list): A list of items. If None, the column items are used.
            raise_exception (bool): If True, raise a ValidationError if the items
                are not valid. If False returns False if validation fails.

        Returns:
            bool: True if the items are valid.

        Raises:
            ValidationError: If the items are not valid.
        """
        items = items or self.items
        rep = self.validate_items(items=items)
        if not rep.valid:
            if raise_exception:
                raise ValidationError(report=rep)
            return False
        return True

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
