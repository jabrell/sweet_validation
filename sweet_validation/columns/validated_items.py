from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any


class ValidatedItems(ABC):
    """Abstract class for class holding a list of items that are always validated
    if changed.

    Attributes:
        items: A list of items that are validated.
            Items are immutable and can only be replaced by reassigning the items
            attribute which triggers the validation process.

    Methods:
        validate_items: Validate items
        is_valid: Check if items are valid. It allows also allows for testing
            an item object against the validation used in the class.
    """

    _items: Any

    def __init__(self, items: Any):
        if self.is_valid(items=items, raise_exception=True):
            self._items = items

    @property
    def items(self) -> Any:
        """Return the items of the column."""
        return deepcopy(self._items)

    @items.setter
    def items(self, items: Any) -> None:
        """Set the items of the column."""
        self.is_valid(items=items, raise_exception=True)
        self._items = items

    @abstractmethod
    def is_valid(self, items: Any, raise_exception: bool = True) -> bool:
        """Raise a ValidationError if the items are not valid.

        Args:
            items (Any): A list of items. If None, the column items are used.
            raise_exception (bool): If True, raise an error if the items
                are not valid. If False returns False if validation fails.

        Raises:
            ValidationError: If the items are not valid. The validation error
                should contain a report of the validation.
        """
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def validate_items(self, items: Any) -> Any:
        """Validate a list of items against the Field object.

        Args:
            items (Any): A list of items.

        Returns:
            Any: Should return a validation report.
        """
        raise NotImplementedError  # pragma: no cover
