class DuplicatedValueError(Exception):
    def __init__(self, column_name: str):
        """Raised when a column contains duplicated values.

        Args:
            column_name (str): The name of the column.
        """
        message = f"Column {column_name} contains duplicated values."
        super().__init__(message)
        self.message = message


class RequiredValueError(Exception):
    def __init__(self, column_name: str):
        message = f"Column {column_name} contains Null values which are not allowed."
        super().__init__(message)
        self.message = message
