from sweet_validation.validator.tweaked_validator import TweakedValidator


def test_validation():
    validator = TweakedValidator()
    assert validator.validate("data", {}) == {"valid": True}
    assert validator.validate("data", {}, response=False) == {"valid": False}
    assert validator.is_valid("data", {})
    assert not validator.is_valid("data", {}, response=False)
