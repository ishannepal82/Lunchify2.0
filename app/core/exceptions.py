"""Application-wide exception definitions."""


class ApplicationException(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = 500) -> None:
        """Initialize application exception.
        
        Args:
            message: Human-readable error message.
            code: Error code for client handling.
            status_code: HTTP status code.
        """
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class ResourceNotFoundError(ApplicationException):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found") -> None:
        """Initialize resource not found error."""
        super().__init__(message, code="NOT_FOUND", status_code=404)


class ValidationError(ApplicationException):
    """Raised when validation fails."""

    def __init__(self, message: str = "Validation failed") -> None:
        """Initialize validation error."""
        super().__init__(message, code="VALIDATION_ERROR", status_code=422)


class ConflictError(ApplicationException):
    """Raised when a conflict occurs (e.g., duplicate resource)."""

    def __init__(self, message: str = "Resource conflict") -> None:
        """Initialize conflict error."""
        super().__init__(message, code="CONFLICT", status_code=409)


class RateLimitExceededError(ApplicationException):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        """Initialize rate limit error."""
        super().__init__(message, code="RATE_LIMIT_EXCEEDED", status_code=429)
