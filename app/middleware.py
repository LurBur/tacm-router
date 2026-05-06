"""Middleware for request tracking and monitoring."""

import uuid
import time
import logging
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.logger import get_logger

logger = get_logger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Middleware to add unique request ID to all requests."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add request ID and tracking."""
        request_id = str(uuid.uuid4())
        
        # Store request ID in state for access in endpoints
        request.state.request_id = request_id
        
        # Log request
        logger.info(
            f"📬 Incoming {request.method} {request.url.path}",
            extra={"request_id": request_id}
        )
        
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            
            # Log response
            logger.info(
                f"✅ Response {response.status_code} for {request.method} {request.url.path}",
                extra={"request_id": request_id}
            )
            
            return response
        except Exception as e:
            logger.error(
                f"❌ Error processing request: {str(e)}",
                extra={"request_id": request_id},
                exc_info=True
            )
            raise


class TimingMiddleware(BaseHTTPMiddleware):
    """Middleware to track request processing time."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Track request timing."""
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        response.headers["X-Process-Time"] = str(process_time)
        
        request_id = getattr(request.state, "request_id", "unknown")
        logger.debug(
            f"⏱️ Request processed in {process_time:.2f}s",
            extra={"request_id": request_id}
        )
        
        return response
