"""FastAPI Backend for Hello World Application.

This module provides a simple REST API with hello and health check endpoints.
Designed to work with a React frontend on http://localhost:3000.
"""

from datetime import datetime, timezone
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI application
app = FastAPI(
    title="Hello World API",
    description="A simple FastAPI backend for fullstack Hello World application",
    version="1.0.0",
)

# Configure CORS middleware
# Allow requests from the React frontend running on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/api/hello", response_model=Dict[str, str])
async def hello() -> Dict[str, str]:
    """Return a hello message with current timestamp.
    
    This endpoint returns a greeting message along with the current server time
    in ISO 8601 format with UTC timezone.
    
    Returns:
        Dict[str, str]: A dictionary containing:
            - message: The greeting message
            - timestamp: Current UTC time in ISO 8601 format
    
    Example:
        GET /api/hello
        Response: {
            "message": "Hello World from Backend!",
            "timestamp": "2024-01-15T10:30:00.000Z"
        }
    """
    # Generate current timestamp in ISO 8601 format with UTC timezone
    current_time = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    
    return {
        "message": "Hello World from Backend!",
        "timestamp": current_time
    }


@app.get("/health", response_model=Dict[str, str])
async def health() -> Dict[str, str]:
    """Health check endpoint.
    
    This endpoint is used to verify that the API is running and responsive.
    Useful for container orchestration health checks and monitoring systems.
    
    Returns:
        Dict[str, str]: A dictionary containing the health status
    
    Example:
        GET /health
        Response: {
            "status": "healthy"
        }
    """
    return {"status": "healthy"}


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint with API information.
    
    Returns:
        Dict[str, str]: Basic API information and available endpoints
    """
    return {
        "name": "Hello World API",
        "version": "1.0.0",
        "endpoints": "/api/hello, /health"
    }


if __name__ == "__main__":
    # This allows running the app directly with: python main.py
    # For development purposes only
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
