from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class ValidatedValues(ABC, Generic[T]):
    """Abstract class for class holding a value object that are always validated
    if changed.

    Attributes:
        values: An objects that contains values that are validated.
            Values are immutable and can only be replaced by reassigning the values
            attribute which triggers the validation process.

    Methods:
        validate: Validate items
        is_valid: Check if items are valid. It allows also allows for testing
            an item object against the validation used in the class.
    """

    _values: T

    def __init__(self, values: T):
        if self.is_valid(values=values, raise_exception=True):
            self._values = values

    @property
    def values(self) -> T:
        """Return the items of the column."""
        return deepcopy(self._values)

    @values.setter
    def values(self, values: T) -> None:
        """Set the items of the column."""
        self.is_valid(values=values, raise_exception=True)
        self._values = values

    @abstractmethod
    def is_valid(self, values: T, raise_exception: bool = True) -> bool:
        """Check if values are not valid

        Args:
            values (T): A values object.
            raise_exception (bool): If True, raise an error if the values
                are not valid. If False returns False if validation fails.

        Raises:
            ValidationError: If the values are not valid. The validation error
                should contain a report of the validation.
        """
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def validate(self, values: T) -> Any:
        """Validate values.

        Args:
            values (Any): Value object

        Returns:
            Any: Should return a validation report.
        """
        raise NotImplementedError  # pragma: no cover
