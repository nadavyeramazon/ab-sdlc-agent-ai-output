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
import os

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
# Support both local development (localhost:3000) and Docker Compose deployment
allowed_origins = [
    "http://localhost:3000",      # Local development
    "http://frontend:3000",       # Docker Compose internal network
    "http://127.0.0.1:3000",      # Alternative localhost
]

# Allow environment variable override for additional origins
if env_origins := os.getenv("CORS_ORIGINS"):
    allowed_origins.extend(env_origins.split(","))

logger.info(f"CORS allowed origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
    # Generate ISO 8601 timestamp with milliseconds precision and Z suffix (UTC timezone)
    # Format: 2025-11-15T12:44:54.123Z
    now = datetime.now(timezone.utc)
    # Use isoformat() which includes microseconds, then format to milliseconds and add Z
    timestamp = now.isoformat(timespec='milliseconds').replace("+00:00", "Z")
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
