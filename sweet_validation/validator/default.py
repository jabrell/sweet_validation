from typing import Any

import pandas as pd
from pandera.errors import SchemaErrors
from pandera.io import from_frictionless_schema

from .validation_report import ValidationReport

__all__ = ["DefaultValidator"]


class DefaultValidator:
    """The DefaultValidator class checks pandas dataframes against a frictionless
    schema.
    """

    @staticmethod
    def validate(data: pd.DataFrame, schema: dict[str | Any]) -> ValidationReport:
        """Validate a pandas dataframe against a frictionless schema

        Args:
            data (pd.DataFrame): Data to validate

        Raises:
            ValidationError: If the data does not conform to the schema
        """
        # convert schema to pandera schema
        schema = from_frictionless_schema(schema)
        try:
            schema.validate(data, lazy=True)
            return ValidationReport(valid=True, errors={})
        except SchemaErrors as e:
            return ValidationReport(valid=False, errors=e.message)

    @staticmethod
    def is_valid(data: pd.DataFrame, schema: dict[str | Any]) -> bool:
        """Check if a pandas dataframe is valid against a frictionless schema

        Args:
            data (pd.DataFrame): Data to validate

        Returns:
            bool: True if the data is valid, False otherwise
        """
        return DefaultValidator.validate(data, schema).valid
