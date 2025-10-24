"""FastAPI Hello World Application.

This module implements a simple FastAPI application with two endpoints:
- Root endpoint: Returns a Hello World message
- Health check endpoint: Returns the service health status
"""

from typing import Dict
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="AB SDLC Agent AI Backend",
    description="A simple FastAPI Hello World application",
    version="1.0.0",
)


@app.get("/", status_code=status.HTTP_200_OK, response_model=Dict[str, str])
async def root() -> Dict[str, str]:
    """Root endpoint that returns a Hello World message.
    
    Returns:
        Dict[str, str]: A dictionary containing the Hello World message
        
    Example:
        >>> GET /
        {"message": "Hello World"}
    """
    return {"message": "Hello World"}


@app.get("/health", status_code=status.HTTP_200_OK, response_model=Dict[str, str])
async def health_check() -> Dict[str, str]:
    """Health check endpoint that returns the service status.
    
    Returns:
        Dict[str, str]: A dictionary containing the health status
        
    Example:
        >>> GET /health
        {"status": "healthy"}
    """
    return {"status": "healthy"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception) -> JSONResponse:
    """Global exception handler for unhandled exceptions.
    
    Args:
        request: The incoming request
        exc: The exception that was raised
        
    Returns:
        JSONResponse: A JSON response with error details
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
