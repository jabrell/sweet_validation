from .validator import ValidationReport


class DataValidationError(Exception):
    report: ValidationReport | None

    def __init__(
        self, message: str | None = None, report: ValidationReport | None = None
    ):
        message = message or "Validation failed."
        if report:
            message += f"\n{report.errors}"
        self.report = report
        super().__init__(message)
