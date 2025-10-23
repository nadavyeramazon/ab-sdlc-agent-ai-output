"""Middleware components for request/response processing and logging."""
import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging and timing."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process and log request/response cycle.
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware in chain
            
        Returns:
            Response: HTTP response
        """
        start_time = time.time()
        
        # Log request
        logger.info(
            f'Request: {request.method} {request.url.path} '
            f'Client: {request.client.host if request.client else "unknown"}'
        )
        
        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            
            # Log response
            logger.info(
                f'Response: {response.status_code} '
                f'Duration: {process_time:.2f}ms'
            )
            
            # Add timing header
            response.headers['X-Process-Time'] = f'{process_time:.2f}ms'
            return response
            
        except Exception as e:
            logger.error(f'Request failed: {str(e)}')
            raise