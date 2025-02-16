from sweet_validation.validator.dummy import DummyValidator


def test_dummy_validator():
    validator = DummyValidator()
    assert validator.validate("data", {}) == {"valid": True}
    assert validator.validate("data", {}, response=False) == {"valid": False}
    assert validator.is_valid("data", {})
    assert not validator.is_valid("data", {}, response=False)


def test_validation_error():
    from sweet_validation.exceptions import DataValidationError

    report = {"errors": "None"}
    error = DataValidationError("msg", report)
    assert str(error) == "msg" + f"\n{report}"
    assert error.report == report
