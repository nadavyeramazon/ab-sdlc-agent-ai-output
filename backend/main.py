"""FastAPI backend application with health and greeting endpoints."""

from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Green Theme Backend API",
    description="Backend API for Green Theme Hello World Fullstack Application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS to allow frontend to communicate with backend
# AC-010: CORS properly configured to allow frontend communication
allowed_origins = [
    "http://localhost:3000",    # React development server
    "http://127.0.0.1:3000",   # Alternative localhost
    "http://0.0.0.0:3000",     # Docker container access
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


class HelloResponse(BaseModel):
    """Response model for hello endpoint - AC-007 specification."""
    message: str = Field(..., description="The hello message")
    timestamp: str = Field(..., description="ISO 8601 formatted timestamp")
    status: str = Field(..., description="Response status")


class HealthResponse(BaseModel):
    """Response model for health check endpoint - AC-008 specification."""
    status: str = Field(..., description="Service health status")
    timestamp: str = Field(..., description="ISO 8601 formatted timestamp")
    service: str = Field(..., description="Service name")


def get_current_timestamp() -> str:
    """Get current timestamp in ISO 8601 format with UTC timezone.
    
    Optimized for fast execution to meet AC-012 response time requirement.
    """
    return datetime.now(timezone.utc).isoformat()


@app.get("/", tags=["Root"])
async def root() -> Dict[str, str]:
    """Root endpoint providing API information.
    
    Returns:
        Dict: API information and navigation links
    """
    logger.info("Root endpoint accessed")
    return {
        "message": "Green Theme Backend API",
        "docs": "/docs",
        "health": "/health",
        "hello": "/api/hello",
        "timestamp": get_current_timestamp()
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Health check endpoint - AC-008: Returns health status as 'healthy'.
    
    Returns exactly the format specified in requirements:
    {
        "status": "healthy",
        "timestamp": "2024-01-15T10:30:00Z",
        "service": "green-theme-backend"
    }
    
    Returns:
        HealthResponse: Service health status with exact specification format
    """
    logger.info("Health check requested")
    return HealthResponse(
        status="healthy",
        timestamp=get_current_timestamp(),
        service="green-theme-backend"
    )


@app.get("/api/hello", response_model=HelloResponse, tags=["Hello"])
async def hello_world() -> HelloResponse:
    """Hello World endpoint - AC-007: Returns exact specified message.
    
    Returns exactly the format specified in requirements:
    {
        "message": "Hello World from Backend!",
        "timestamp": "2024-01-15T10:30:00Z",
        "status": "success"
    }
    
    Returns:
        HelloResponse: Hello world message with exact specification format
    """
    logger.info("Hello world endpoint accessed")
    
    return HelloResponse(
        message="Hello World from Backend!",
        timestamp=get_current_timestamp(),
        status="success"
    )


@app.get("/api/hello/{name}", response_model=HelloResponse, tags=["Hello"])
async def hello_user(name: str) -> HelloResponse:
    """Personalized hello endpoint with timestamp.
    
    Args:
        name: Name to greet (path parameter)
    
    Returns:
        HelloResponse: Personalized greeting message with timestamp
    
    Raises:
        HTTPException: If name is invalid
    """
    if not name or not name.strip():
        logger.warning("Invalid hello request with empty name")
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty or contain only whitespace"
        )
    
    if len(name) > 100:
        logger.warning(f"Name too long: {len(name)} characters")
        raise HTTPException(
            status_code=400,
            detail="Name is too long (maximum 100 characters)"
        )
    
    # Sanitize name to prevent potential issues
    clean_name = name.strip()
    
    logger.info(f"Personalized hello for: {clean_name}")
    
    return HelloResponse(
        message=f"Hello, {clean_name}! Welcome from Backend!",
        timestamp=get_current_timestamp(),
        status="success"
    )


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 error handler - AC-011: Proper HTTP status codes."""
    logger.warning(f"404 error for path: {request.url.path}")
    return {"detail": "Endpoint not found"}


@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    """Custom 500 error handler - AC-011: Proper HTTP status codes."""
    logger.error(f"Internal server error for path: {request.url.path}: {exc}")
    return {"detail": "Internal server error"}


if __name__ == "__main__":
    import uvicorn
    # AC-009: Backend service runs on port 8000 and accepts HTTP requests
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )