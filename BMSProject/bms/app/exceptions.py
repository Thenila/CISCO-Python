"""Custom exceptions for Banking Management System (BMS)."""

class BMSException(Exception):
    """Base exception class for the BMS project."""
    pass

class NotFoundException(BMSException):
    """Raised when a requested resource (e.g., account) is not found."""

    def __init__(self, resource_name: str, resource_id: int = None):
        self.resource_name = resource_name
        self.resource_id = resource_id
        message = f"{resource_name}"
        if resource_id is not None:
            message += f" with ID {resource_id}"
        message += " not found."
        super().__init__(message)

class IntegrityException(BMSException):
    """Raised when there is a database integrity error (e.g., unique constraint violation)."""

    def __init__(self, message="Database integrity error occurred."):
        super().__init__(message)
