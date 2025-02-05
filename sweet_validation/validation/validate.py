from frictionless import Resource

__all__ = ["validate_csv_file"]


def validate_csv_file(fn_csv: str, fn_schema: str) -> bool:
    """Validate a CSV file against a schema file.

    Args:
        fn_csv (str): The path to the CSV file.
        fn_schema (str): The path to the schema file.

    Returns:
        bool: True if the CSV file is valid, False otherwise.
    """
    r = Resource(source=fn_csv, schema=fn_schema)
    valid = r.validate()
    return bool(valid.valid)
