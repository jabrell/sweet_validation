from typing import Any


class DataValidationError(Exception):
    report: dict[str, Any] | None

    def __init__(
        self, message: str | None = None, report: dict[str, Any] | None = None
    ):
        message = message or "Validation failed."
        if report:
            message += f"\n{report}"
        self.report = report
        super().__init__(message)
