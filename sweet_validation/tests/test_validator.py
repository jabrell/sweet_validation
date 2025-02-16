import pandas as pd

from sweet_validation.validator import (
    DefaultValidator,
    DummyValidator,
    ValidationReport,
)

FRICTIONLESS_SCHEMA = {
    "fields": [
        {
            "name": "column_1",
            "type": "integer",
            "constraints": {"minimum": 10, "maximum": 99},
        },
        {
            "name": "column_2",
            "type": "string",
            "constraints": {"maxLength": 10, "pattern": "\\S+"},
        },
    ],
    "primaryKey": "column_1",
}


def test_validation_report():
    report = ValidationReport(valid=True, errors={})
    assert report.valid
    assert not report.errors
    assert report == ValidationReport(valid=True, errors={})
    assert report != ValidationReport(valid=False, errors={})
    assert report != ValidationReport(valid=True, errors={"a": "b"})
    assert report != []


def test_dummy_validator():
    validator = DummyValidator()
    assert validator.validate("data", {}) == ValidationReport(valid=True, errors={})
    assert validator.validate("data", {}, response=False) == ValidationReport(
        valid=False, errors={}
    )
    assert validator.is_valid("data", {})
    assert not validator.is_valid("data", {}, response=False)


def test_validation_error():
    from sweet_validation.exceptions import DataValidationError

    errors = {"column1": "an error"}
    report = ValidationReport(valid=False, errors=errors)
    error = DataValidationError("msg", report=report)
    assert str(error) == "msg" + f"\n{errors}"
    assert error.report == report


def test_default_validator_valid():
    schema = FRICTIONLESS_SCHEMA

    df_valid = pd.DataFrame(
        {
            "column_1": [10, 20, 30, 40, 50, 60],
            "column_2": ["a", "b", "c", "d", "e", "f"],
        }
    )
    report = DefaultValidator.validate(data=df_valid, schema=schema)
    assert report.valid
    assert not report.errors
    assert DefaultValidator.is_valid(data=df_valid, schema=schema)


def test_default_validator_invalid():
    schema = FRICTIONLESS_SCHEMA

    df_invalid = pd.DataFrame(
        {
            "column_1": [10, 20, 30, 40, 50, 999],
            "column_2": ["a", "b", "c", "d", "e", "f"],
            "column_3": [1, 2, 3, 4, 5, 6],
        }
    )
    report = DefaultValidator.validate(df_invalid, schema)
    assert not report.valid
    assert report.errors
    assert not DefaultValidator.is_valid(df_invalid, schema)
