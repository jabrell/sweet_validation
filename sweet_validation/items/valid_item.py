from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Generic, Protocol, TypeVar, runtime_checkable

T = TypeVar("T")

__all__ = ["ValidItem", "ValidItemProtocol"]


class ValidItem(ABC, Generic[T]):
    """Abstract class for class holding an value object that are always validated
    if changed.

    The class implements the logic of item validation and ensures that items cannot
    be changed without validation.

    Attributes:
        item: An objects that contains values that are validated.
            The item is immutable and can only be replaced by reassigning
            the item which triggers the validation process.

    Methods:
        validate: Validate items
        is_valid: Check if items are valid. It allows also allows for testing
            an item object against the validation used in the class.
    """

    _item: T

    def __init__(self, item: T):
        if self.is_valid(item=item, raise_exception=True):
            self._item = deepcopy(item)

    @property
    def item(self) -> T:
        """Return the items of the column."""
        return deepcopy(self._item)

    @item.setter
    def item(self, item: T) -> None:
        """Set the items of the column."""
        self.is_valid(item=item, raise_exception=True)
        self._item = item

    @abstractmethod
    def is_valid(self, item: T, raise_exception: bool = True) -> bool:
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
    def validate(self, item: T) -> Any:
        """Validate values.

        Args:
            values (Any): Value object

        Returns:
            Any: Should return a validation report.
        """
        raise NotImplementedError  # pragma: no cover


@runtime_checkable
class ValidItemProtocol(Protocol):
    @property
    def values(self) -> Any: ...
    def is_valid(self, value: Any) -> bool: ...
    def validate(self, value: Any) -> Any: ...
