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
    title="Green Hello World API",
    description="A simple hello world API with green theme support and timestamp tracking",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS to allow frontend to communicate with backend
# In production, specify exact origins for security
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
    """Response model for hello endpoint."""
    message: str = Field(..., description="The hello message")
    timestamp: str = Field(..., description="ISO 8601 formatted timestamp")
    status: str = Field(default="success", description="Response status")
    theme: str = Field(default="green", description="Application theme")


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str = Field(..., description="Service health status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    timestamp: str = Field(..., description="ISO 8601 formatted timestamp")
    theme: str = Field(default="green", description="Application theme")


class RootResponse(BaseModel):
    """Response model for root endpoint."""
    message: str = Field(..., description="Welcome message")
    docs: str = Field(..., description="Documentation URL")
    health: str = Field(..., description="Health check URL")
    hello: str = Field(..., description="Hello endpoint URL")
    theme: str = Field(default="green", description="Application theme")
    timestamp: str = Field(..., description="ISO 8601 formatted timestamp")


def get_current_timestamp() -> str:
    """Get current timestamp in ISO 8601 format with UTC timezone."""
    return datetime.now(timezone.utc).isoformat()


@app.get("/", response_model=RootResponse, tags=["Root"])
async def root() -> RootResponse:
    """Root endpoint providing API information.
    
    Returns:
        RootResponse: API information and navigation links
    """
    logger.info("Root endpoint accessed")
    return RootResponse(
        message="Welcome to Green Hello World API",
        docs="/docs",
        health="/health",
        hello="/api/hello",
        theme="green",
        timestamp=get_current_timestamp()
    )


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Health check endpoint to verify service is running.
    
    Returns:
        HealthResponse: Service health status information with timestamp
    """
    logger.info("Health check requested")
    return HealthResponse(
        status="healthy",
        service="green-hello-world-api",
        version="1.0.0",
        timestamp=get_current_timestamp(),
        theme="green"
    )


@app.get("/api/hello", response_model=HelloResponse, tags=["Hello"])
async def hello_world() -> HelloResponse:
    """Hello World endpoint that returns a green-themed greeting with timestamp.
    
    Returns:
        HelloResponse: Hello world message with green theme and current timestamp
    """
    logger.info("Hello world endpoint accessed")
    
    return HelloResponse(
        message="Hello World! 🌱 Welcome to our beautiful green-themed fullstack application! Built with React, Vite, and FastAPI. 🚀",
        timestamp=get_current_timestamp(),
        status="success",
        theme="green"
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
        message=f"Hello, {clean_name}! 🌱 Welcome to our green-themed fullstack application! 🚀",
        timestamp=get_current_timestamp(),
        status="success",
        theme="green"
    )


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 error handler."""
    logger.warning(f"404 error for path: {request.url.path}")
    return {"detail": "Endpoint not found"}


@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    """Custom 500 error handler."""
    logger.error(f"Internal server error for path: {request.url.path}: {exc}")
    return {"detail": "Internal server error"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )