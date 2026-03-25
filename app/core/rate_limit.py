from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse
from app.utils.errors import too_many_requests_error

""" Rate limiting configuration for the Steam Games API.
Provides centralized rate limiting using the slowapi library
"""

# Create a limiter instance with in-memory storage
limiter = Limiter(key_func=get_remote_address, storage_uri="memory://", default_limits=["100/hour"])


# Rate limit exception handler
def rate_limit_handler(request: Request, exc: Exception):
    rate_exc = exc if isinstance(exc, RateLimitExceeded) else None
    detail = rate_exc.detail if rate_exc else "Rate limit exceeded"

    # Use centralized error handling
    http_exception = too_many_requests_error(detail)
    return JSONResponse(status_code=http_exception.status_code, content=http_exception.detail)
