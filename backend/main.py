"""FastAPI Backend Application

This module implements a simple FastAPI backend with CORS support,
health check endpoint, and a hello world endpoint with timestamp.
"""

import logging
from datetime import datetime, timezone
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="Backend API",
    description="FastAPI backend with CORS support",
    version="1.0.0"
)

# Configure CORS middleware
# This allows the frontend (running on localhost:3000) to make requests to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React/Next.js development server
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

logger.info("FastAPI application initialized with CORS support")


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint.
    
    Returns:
        Dict[str, str]: Status indicating the service is healthy
        
    Example:
        >>> GET /health
        {"status": "healthy"}
    """
    logger.debug("Health check endpoint called")
    return {"status": "healthy"}


@app.get("/api/hello")
async def hello_world() -> Dict[str, str]:
    """Hello World endpoint with current timestamp.
    
    Returns:
        Dict[str, str]: A greeting message with ISO-8601 formatted timestamp
        
    Example:
        >>> GET /api/hello
        {
            "message": "Hello World from Backend!",
            "timestamp": "2024-01-15T10:30:00.123456Z"
        }
    """
    # Get current UTC time and format as ISO-8601 with timezone
    current_time = datetime.now(timezone.utc)
    iso_timestamp = current_time.isoformat().replace("+00:00", "Z")
    
    logger.info(f"Hello endpoint called at {iso_timestamp}")
    
    return {
        "message": "Hello World from Backend!",
        "timestamp": iso_timestamp
    }


# Application startup event
@app.on_event("startup")
async def startup_event():
    """Log application startup."""
    logger.info("Application startup complete - Server ready to accept requests")
    logger.info("Listening on http://0.0.0.0:8000")
    logger.info("API documentation available at http://localhost:8000/docs")


# Application shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Log application shutdown."""
    logger.info("Application shutting down")


if __name__ == "__main__":
    # This block is used for local development without Docker
    import uvicorn
    
    logger.info("Starting uvicorn server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
