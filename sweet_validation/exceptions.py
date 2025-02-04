from frictionless import Report


class ValidationError(Exception):
    report: Report | None

    def __init__(self, message: str | None = None, report: Report | None = None):
        message = message or "Frictionless validation failed."
        if report:
            message += f"{report.errors}"
        self.report = report
        super().__init__(message)
