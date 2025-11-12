"""FastAPI Backend Application for Green Theme Hello World.

This module implements a production-ready FastAPI application with:
- Health check endpoint
- Hello World API endpoint with timestamp
- CORS middleware for frontend communication
- Proper error handling and logging
"""

from datetime import datetime
from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class HelloResponse(BaseModel):
    """Response model for hello endpoint."""
    
    message: str = Field(
        ...,
        description="Hello message from backend",
        example="Hello World from Backend!"
    )
    timestamp: str = Field(
        ...,
        description="ISO 8601 formatted timestamp",
        example="2024-01-01T12:00:00.000Z"
    )


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = Field(
        ...,
        description="Health status of the service",
        example="healthy"
    )


class ErrorResponse(BaseModel):
    """Response model for error responses."""
    
    detail: str = Field(
        ...,
        description="Error message",
        example="Internal server error"
    )


# Initialize FastAPI application
app = FastAPI(
    title="Green Theme Hello World Backend",
    description="Production-ready FastAPI backend for Hello World application",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS middleware
# Frontend runs in browser and connects to localhost, not Docker service names
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend on Docker (port 3000)
        "http://localhost:5173",  # Vite dev server alternative port
        "http://localhost:80",    # Alternative frontend port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    tags=["Health"],
    summary="Health Check",
    description="Check if the service is running and healthy",
    responses={
        200: {
            "description": "Service is healthy",
            "model": HealthResponse,
        },
        503: {
            "description": "Service is unavailable",
            "model": ErrorResponse,
        },
    },
)
async def health_check() -> Dict[str, str]:
    """Health check endpoint.
    
    Returns:
        Dict containing health status
        
    Raises:
        HTTPException: If service is unhealthy
    """
    try:
        # In a real application, you might check database connections,
        # external services, etc.
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unhealthy: {str(e)}"
        )


@app.get(
    "/api/hello",
    response_model=HelloResponse,
    status_code=status.HTTP_200_OK,
    tags=["API"],
    summary="Hello World",
    description="Get a hello world message with current timestamp",
    responses={
        200: {
            "description": "Successful response with message and timestamp",
            "model": HelloResponse,
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse,
        },
    },
)
async def hello() -> Dict[str, str]:
    """Hello World endpoint with timestamp.
    
    Returns:
        Dict containing message and ISO 8601 formatted timestamp
        
    Raises:
        HTTPException: If an error occurs generating the response
    """
    try:
        # Generate ISO 8601 formatted timestamp
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        
        return {
            "message": "Hello World from Backend!",
            "timestamp": timestamp
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response: {str(e)}"
        )


@app.get(
    "/",
    include_in_schema=False
)
async def root() -> Dict[str, Any]:
    """Root endpoint - redirects to API documentation.
    
    Returns:
        Dict with service information and documentation links
    """
    return {
        "service": "Green Theme Hello World Backend",
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs",
        "health": "/health",
        "api": "/api/hello"
    }


if __name__ == "__main__":
    # Run the application with Uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Set to True for development
        log_level="info"
    )
