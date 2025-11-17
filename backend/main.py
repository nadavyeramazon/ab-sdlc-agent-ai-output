"""FastAPI backend for Yellow Theme Hello World application.

Provides endpoints for:
- /api/hello: Returns hello world message with timestamp
- /health: Health check endpoint for monitoring
"""

from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Yellow Theme Hello World API",
    description="Backend API for fullstack Hello World application",
    version="1.0.0"
)

# CORS middleware configuration
# Allow requests from frontend running on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://frontend:3000",  # Docker network hostname
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HelloResponse(BaseModel):
    """Response model for /api/hello endpoint."""
    message: str
    timestamp: str


class HealthResponse(BaseModel):
    """Response model for /health endpoint."""
    status: str


@app.get("/api/hello", response_model=HelloResponse)
async def get_hello() -> HelloResponse:
    """Return hello world message with current timestamp.
    
    Returns:
        HelloResponse: JSON with message and ISO-8601 timestamp
        
    Raises:
        HTTPException: 500 if timestamp generation fails
    """
    try:
        # Generate ISO-8601 formatted timestamp
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        logger.info(f"Hello endpoint called at {timestamp}")
        
        return HelloResponse(
            message="Hello World from Backend!",
            timestamp=timestamp
        )
    except Exception as e:
        logger.error(f"Error in /api/hello endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint for service monitoring.
    
    Returns:
        HealthResponse: JSON with status "healthy"
    """
    logger.info("Health check endpoint called")
    return HealthResponse(status="healthy")


@app.get("/")
async def root():
    """Root endpoint - provides API information."""
    return {
        "name": "Yellow Theme Hello World API",
        "version": "1.0.0",
        "endpoints": {
            "/api/hello": "Get hello world message with timestamp",
            "/health": "Health check endpoint",
            "/docs": "Interactive API documentation"
        }
    }
