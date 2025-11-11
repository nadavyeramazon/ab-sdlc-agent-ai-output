"""FastAPI Backend Application

Provides a RESTful API for the Hello World fullstack application.
Includes health check and greeting endpoints with CORS support.

Endpoints:
    GET /health - Health check endpoint
    GET /api/hello - Returns greeting message with timestamp
    GET /docs - Swagger UI API documentation
    GET /redoc - ReDoc API documentation
"""

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application with metadata
app = FastAPI(
    title="Green Theme Hello World API",
    description="Backend API for fullstack Hello World application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware
# Allow requests from frontend running on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/hello", tags=["API"])
async def get_hello(response: Response) -> dict:
    """Return greeting message with current timestamp.
    
    Returns a JSON response containing a greeting message and the current
    server timestamp in ISO 8601 format (UTC).
    
    Args:
        response: FastAPI Response object for setting headers
    
    Returns:
        dict: JSON response with structure:
            {
                "message": "Hello World from Backend!",
                "timestamp": "2024-01-15T10:30:00.000000Z"
            }
    
    Example:
        >>> response = await get_hello()
        >>> print(response["message"])
        Hello World from Backend!
    """
    current_time = datetime.utcnow().isoformat() + "Z"
    logger.info(f"GET /api/hello - Returning greeting at {current_time}")
    
    # Set cache control headers for development
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    return {
        "message": "Hello World from Backend!",
        "timestamp": current_time
    }


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """Health check endpoint for service monitoring.
    
    Used by Docker health checks, load balancers, and monitoring systems
    to verify the service is running and responsive.
    
    Returns:
        dict: JSON response with structure:
            {
                "status": "healthy"
            }
    
    Example:
        >>> response = await health_check()
        >>> print(response["status"])
        healthy
    """
    logger.info("GET /health - Health check requested")
    return {"status": "healthy"}


# Root endpoint for basic service information
@app.get("/", tags=["Info"])
async def root() -> dict:
    """Root endpoint providing basic service information.
    
    Returns:
        dict: Service information including name and documentation links
    """
    return {
        "service": "Green Theme Hello World API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
