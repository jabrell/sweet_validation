from typing import Any, cast

__all__ = ["TweakedValidator"]


class TweakedValidator:
    """The TweakedValidator is a validator that serves test cases. It allows
    to specify the response of the validator for a given schema and data. In that
    it ensures that the schema is loaded but does not perform any validation.
    But returns the expected response. It also serves as a blue print for the
    implementation of the Validator class.
    """

    # TODO how to we implement validation reports?
    def validate(
        self, data: Any, schema: dict[str, Any], response: bool = True
    ) -> dict[str, Any]:
        """Validate the data against the schema

        Args:
            data (Any): Data to be validated
            schema (dict[str, Any]): Schema to validate against
            response (bool, optional): Expected response. Defaults to True.

        Returns:
            dict[str, Any]: Validation report
        """
        return {"valid": response}

    def is_valid(
        self, data: Any, schema: dict[str, Any], response: bool = True
    ) -> bool:
        """Check if the data is valid against the schema

        Args:
            data (Any): Data to be validated
            schema (dict[str, Any]): Schema to validate against
            response (bool, optional): Expected response. Defaults to True.

        Returns:
            bool: True if valid else False
        """
        if self.validate(data, schema, response=response)["valid"]:
            return True
        return False
