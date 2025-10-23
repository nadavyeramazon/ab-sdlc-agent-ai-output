"""Custom middleware implementations.

Defines request/response middleware for logging and monitoring.
"""

import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging request/response metrics."""

    async def dispatch(self, request: Request, call_next):
        """Process the request and log metrics.

        Args:
            request (Request): The incoming request
            call_next (Callable): The next middleware/route handler

        Returns:
            Response: The response from the next handler
        """
        start_time = time.time()
        
        response = await call_next(request)
        
        # Log request details
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"Method: {request.method} Path: {request.url.path} "
            f"Status: {response.status_code} Duration: {process_time:.2f}ms"
        )
        
        return response
