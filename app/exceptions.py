"""Custom exceptions for Siphon MVP service."""

from typing import Optional, Any
from fastapi import HTTPException, status


class SiphonException(HTTPException):
    """Base exception for Siphon service."""
    
    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str = "SIPHON_ERROR",
        context: Optional[dict] = None,
    ):
        """Initialize Siphon exception.
        
        Args:
            detail: Human-readable error message
            status_code: HTTP status code
            error_code: Machine-readable error identifier
            context: Additional error context
        """
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.context = context or {}


class InvalidInputException(SiphonException):
    """Raised when input validation fails."""
    
    def __init__(self, detail: str, context: Optional[dict] = None):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="INVALID_INPUT",
            context=context,
        )


class ProcessingException(SiphonException):
    """Raised when pipeline processing fails."""
    
    def __init__(self, detail: str, stage: str, context: Optional[dict] = None):
        if context is None:
            context = {}
        context["stage"] = stage
        super().__init__(
            detail=detail,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="PROCESSING_ERROR",
            context=context,
        )


class RateLimitException(SiphonException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, retry_after_seconds: int = 60):
        super().__init__(
            detail=f"Rate limit exceeded. Retry after {retry_after_seconds} seconds.",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED",
            context={"retry_after": retry_after_seconds},
        )


class TimeoutException(SiphonException):
    """Raised when operation times out."""
    
    def __init__(self, operation: str = "processing"):
        super().__init__(
            detail=f"Request timeout during {operation}. Please try again.",
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            error_code="REQUEST_TIMEOUT",
            context={"operation": operation},
        )
