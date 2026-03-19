from fastapi import HTTPException
from typing import Any, Dict, Optional
from app.schemas.error import ErrorResponse, ErrorCodes


def create_http_exception(
    status_code: int, error_code: str, message: str, details: Optional[Dict[str, Any]] = None
) -> HTTPException:
    """Helper function to create standardized HTTP exceptions."""
    error_response = ErrorResponse(error_code=error_code, message=message, details=details)
    return HTTPException(status_code=status_code, detail=error_response.model_dump())


def not_found_error(resource: str, identifier: Any) -> HTTPException:
    """Create a 404 error for when resource is not found."""
    return create_http_exception(
        status_code=404,
        error_code=ErrorCodes.NOT_FOUND,
        message=f"The requested {resource.title()} was not found.",
        details={"resource": resource, "id": identifier},
    )


def validation_error(field: str, value: Any, constraint: str) -> HTTPException:
    """Create a 400 error for validation failures."""
    return create_http_exception(
        status_code=400,
        error_code=ErrorCodes.VALIDATION_ERROR,
        message=f"Validation failed for field '{field}'.",
        details={"field": field, "value": value, "constraint": constraint},
    )


def unproccessable_entity_error(field: str, value: Any, constraint: str) -> HTTPException:
    """Create a 422 error for unprocessable entity."""
    return create_http_exception(
        status_code=422,
        error_code=ErrorCodes.VALIDATION_ERROR,
        message=f"Unprocessable entity: '{field}' contains semantically invalid data.",
        details={"field": field, "value": value, "constraint": constraint},
    )


def database_error(message: str) -> HTTPException:
    """Create a 500 error for database-related issues."""
    return create_http_exception(
        status_code=500,
        error_code=ErrorCodes.DATABASE_ERROR,
        message=f"Database operation error: {message}",
    )


def conflict_error(resource: str, reason: str) -> HTTPException:
    """Create a 409 error for conflict situations."""
    return create_http_exception(
        status_code=409,
        error_code=ErrorCodes.CONFLICT,
        message=f"Conflict with existing {resource}: {reason}",
        details={"resource": resource, "reason": reason},
    )
