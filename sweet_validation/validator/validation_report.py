from typing import Any

__all__ = ["ValidationReport"]


class ValidationReport:
    """Validation report class.

    It provides two main properties:

    - `valid` - a boolean flag indicating whether the validation was successful
    - `errors` - a list of validation errors
    """

    valid: bool
    errors: dict[Any, Any]

    def __init__(self, valid: bool, errors: dict[Any, Any]) -> None:
        self.valid = valid
        self.errors = errors

    def __eq__(self, value: object) -> bool:
        if self.valid == value.valid and self.errors == value.errors:
            return True
        return False
        return self.valid == value.valid and self.errors == value.errors
