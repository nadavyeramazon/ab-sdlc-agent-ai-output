"""FastAPI backend application for Hello World fullstack app.

This module provides a simple REST API with health check and hello endpoints.
It includes CORS middleware to allow requests from the React frontend.
"""

from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI application
app = FastAPI(
    title="Hello World Backend API",
    description="Backend API for Green Theme Hello World Application",
    version="1.0.0"
)

# Configure CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["GET"],  # Only GET requests needed
    allow_headers=["*"],
)


class HelloResponse(BaseModel):
    """Response model for hello endpoint."""
    message: str
    timestamp: str


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str


@app.get("/api/hello", response_model=HelloResponse)
async def get_hello() -> HelloResponse:
    """Return hello message with current timestamp.
    
    Returns:
        HelloResponse: JSON response with message and ISO8601 timestamp
    """
    return HelloResponse(
        message="Hello World from Backend!",
        timestamp=datetime.utcnow().isoformat() + "Z"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint to verify service is running.
    
    Returns:
        HealthResponse: JSON response with status
    """
    return HealthResponse(status="healthy")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
