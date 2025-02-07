from typing import Any

from frictionless import Field, Report, Resource, Schema

from sweet_validation.exceptions import ValidationError

from .valid_item import ValidItem

__all__ = ["Column"]


class Column(ValidItem[list[Any]]):
    """A column is defined as a list of items and a frictionless Field object.

    The field object defines the type and constraints of the column and is based
    on the frictionless.Field object. Values are validated against this field
    every time they are appended or extended.

    For more information on the Field object, see:
    - [Field types](https://framework.frictionlessdata.io/docs/fields/any.html)
        under "Data Fields"
    - [Constraints](https://specs.frictionlessdata.io/table-schema/#constraints)
    - [Table and Field Scheme standard](https://datapackage.org/standard/table-schema/)

    Attributes:
        field (Field): A frictionless Field object.
            The field object defines the type and constraints of the column.
            It can only be modified during instantiation. Otherwise it is
            immutable.
        values (list): A list of items. The items are validated against the field
            object. values are immutable and can only be set during instantiation or by
            replacing the values (e.g., col.values = [1, 2, 3]) which triggers
            a validation check.

    Methods:
        is_valid: Raise a ValidationError if values are not valid. It can also
            be used to validate a list of items against the Field object.
        validate: Validate values against the Field object.
        get_resource: Return a frictionless Resource object with the values and
            meta-data.

    Raises:
        ValidationError: If the items are not valid given the Field object.
        AttributeError: If the fields are modified after instantiation.

    Examples:

        ```python
        from frictionless.fields import IntegerField
        field = IntegerField(name="test", constraints={"minimum": 1, "maximum": 3})
        col = Column(field=field, values=[1, 2, 3])
        ```

        The field property is immutable and values can only be replaced by a new list
        but are otherwise immutable. That means that you always receive a copy of
        values and fields and modifying these copies will not affect the original
        column object.

        ```python
        from frictionless.fields import IntegerField
        field = IntegerField(name="test")
        col = Column(field=field, values=[1, 2, 3])
        print(col.value)  # returns [1, 2, 3]
        new_items = col.values
        new_items.append(4)
        print(col.values)  # still returns [1, 2, 3]
        col.values = new_items
        print(col.values)  # returns [1, 2, 3, 4]
        new_field = IntegerField(name="another_test") # raises AttributeError
        ```
    """

    _item: list[Any] = []
    _field: Field

    def __init__(self, field: Field, values: list[Any] | None = None):
        values = values or []
        # first assign the field so the validation can be done, then call parent class
        self._field = field
        super().__init__(item=values)

    @property
    def field(self) -> Field:
        """Return the field object of the column."""
        return self._field

    @field.setter
    def field(self, field: Field) -> None:
        """Set the field object of the column."""
        raise AttributeError("Cannot reset the field. Create a new column instead.")

    def is_valid(
        self, item: list[Any] | None = None, raise_exception: bool = True
    ) -> bool:
        """Raise a ValidationError if values are not valid.

        Args:
            values (list): A list of items. If None, the column values are used.
            raise_exception (bool): If True, raise a ValidationError if values
                are not valid. If False returns False if validation fails.

        Returns:
            bool: True if values are valid. False otherwise.

        Raises:
            ValidationError: If the items are not valid.
        """
        item = item or self.item
        rep = self.validate(item=item)
        if not rep.valid:
            if raise_exception:
                raise ValidationError(report=rep)
            return False
        return True

    def validate(self, item: list[Any] | None = None) -> Report:
        """Validate a list of items against the Field object.

        Args:
            values (list): A list of items.

        Raises:
            ValueError: If the items are not valid.
        """
        item = item or self.item
        return self.get_resource(item=item).validate()

    def get_resource(self, item: list[Any] | None) -> Resource:
        """Return a Resource object with the column items.

        Args:
            values (list): A list of items. If None, the column items are used."""
        item = item or self.item
        data = [[self.field.name]] + [[i] for i in item]
        return Resource(data=data, schema=Schema(fields=[self.field]))
