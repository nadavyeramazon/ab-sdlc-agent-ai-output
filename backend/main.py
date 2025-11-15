"""FastAPI backend for Green Theme Hello World application.

Provides two main endpoints:
- /api/hello: Returns a greeting message with timestamp
- /health: Health check endpoint
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timezone
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application instance
app = FastAPI(
    title="Green Theme Hello World API",
    description="Backend API for Green Theme Hello World fullstack application",
    version="1.0.0"
)

# Configure CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend development server
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


# Pydantic models for response validation
class HelloResponse(BaseModel):
    """Response model for /api/hello endpoint."""
    message: str
    timestamp: str


class HealthResponse(BaseModel):
    """Response model for /health endpoint."""
    status: str


@app.get("/api/hello", response_model=HelloResponse)
async def get_hello() -> HelloResponse:
    """Return a hello world message with current timestamp.
    
    Returns:
        HelloResponse: JSON response with message and ISO 8601 timestamp
    """
    logger.info("GET /api/hello endpoint called")
    # Generate ISO 8601 timestamp with Z suffix (UTC timezone)
    # Use replace(microsecond=0) for cleaner timestamps, then manually add Z
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return HelloResponse(
        message="Hello World from Backend!",
        timestamp=timestamp
    )


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint to verify service is running.
    
    Returns:
        HealthResponse: JSON response with health status
    """
    logger.info("GET /health endpoint called")
    return HealthResponse(status="healthy")


if __name__ == "__main__":
    import uvicorn
    # Run the application with Uvicorn server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
