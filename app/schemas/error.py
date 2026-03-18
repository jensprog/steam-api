from typing import Optional, Any, Dict
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standardized error response schema for API endpoints."""

    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ValidationErrorDetail(BaseModel):
    """Details for validation errors."""

    field: str
    value: Any
    constraint: str


class ValidationErrorResponse(BaseModel):
    """Specific error response for validation failures."""

    error_code: str
    details: Optional[Dict[str, ValidationErrorDetail]] = None


# Pre-defined error types
class ErrorCodes:
    # Client errors (4xx)

    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    CONFLICT = "CONFLICT"

    # Server errors (5xx)
    DATABASE_ERROR = "DATABASE_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"


# Common error responses
GAME_NOT_FOUND = ErrorResponse(
    error_code=ErrorCodes.NOT_FOUND, message="The requested game was not found.", details={"resource": "game"}
)

DEVELOPER_NOT_FOUND = ErrorResponse(
    error_code=ErrorCodes.NOT_FOUND, message="The requested developer was not found.", details={"resource": "developer"}
)

GENRE_NOT_FOUND = ErrorResponse(
    error_code=ErrorCodes.NOT_FOUND, message="The requested genre was not found.", details={"resource": "genre"}
)
