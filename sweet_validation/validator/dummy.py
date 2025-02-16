from typing import Any

from .validation_report import ValidationReport

__all__ = ["DummyValidator"]


class DummyValidator:
    """The DummyValidator is a validator that serves test cases. It allows
    to specify the response of the validator for a given schema and data. In that
    it ensures that the schema is loaded but does not perform any validation.
    But returns the expected response. It also serves as a blue print for the
    implementation of the Validator class.
    """

    response: bool

    def __init__(self, response: bool = True) -> None:
        """Initialize the DummyValidator

        Args:
            response (bool | None): Expected response of the validator
        """
        self.response = response

    def validate(
        self, data: Any, schema: dict[str, Any], response: bool | None = None
    ) -> ValidationReport:
        """Validate the data against the schema

        Args:
            data (Any): Data to be validated
            schema (dict[str, Any]): Schema to validate against
            response (bool, optional): Expected response. Defaults to True.

        Returns:
            ValidationReport: Validation report
        """
        response = response if response is not None else self.response
        return ValidationReport(valid=response, errors={})

    def is_valid(
        self, data: Any, schema: dict[str, Any], response: bool | None = None
    ) -> bool:
        """Check if the data is valid against the schema

        Args:
            data (Any): Data to be validated
            schema (dict[str, Any]): Schema to validate against
            response (bool, optional): Expected response. Defaults to None which
                uses the response provided during initialization.

        Returns:
            bool: True if valid else False
        """
        return self.validate(data, schema, response=response).valid
