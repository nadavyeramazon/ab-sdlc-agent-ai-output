"""FastAPI backend application with health and greeting endpoints."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Green Hello World API",
    description="A simple hello world API with green theme support",
    version="1.0.0"
)

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HelloResponse(BaseModel):
    """Response model for hello endpoint."""
    message: str
    status: str = "success"
    theme: str = "green"


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    service: str
    version: str
    theme: str = "green"


@app.get("/", tags=["Root"])
async def root() -> Dict[str, str]:
    """Root endpoint providing API information."""
    return {
        "message": "Welcome to Green Hello World API",
        "docs": "/docs",
        "health": "/health",
        "hello": "/api/hello",
        "theme": "green"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Health check endpoint to verify service is running.
    
    Returns:
        HealthResponse: Service health status information
    """
    logger.info("Health check requested")
    return HealthResponse(
        status="healthy",
        service="green-hello-world-api",
        version="1.0.0",
        theme="green"
    )


@app.get("/api/hello", response_model=HelloResponse, tags=["Hello"])
async def hello_world() -> HelloResponse:
    """Hello World endpoint that returns a green-themed greeting.
    
    Returns:
        HelloResponse: Hello world message with green theme
    """
    logger.info("Hello world endpoint accessed")
    
    return HelloResponse(
        message="Hello World! 🌱 Welcome to our beautiful green-themed fullstack application! Built with React, Vite, and FastAPI. 🚀",
        status="success",
        theme="green"
    )


@app.get("/api/hello/{name}", response_model=HelloResponse, tags=["Hello"])
async def hello_user(name: str) -> HelloResponse:
    """Personalized hello endpoint.
    
    Args:
        name: Name to greet (path parameter)
    
    Returns:
        HelloResponse: Personalized greeting message
    
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
        raise HTTPException(
            status_code=400,
            detail="Name is too long (maximum 100 characters)"
        )
    
    logger.info(f"Personalized hello for: {name}")
    
    return HelloResponse(
        message=f"Hello, {name}! 🌱 Welcome to our green-themed fullstack application! 🚀",
        status="success",
        theme="green"
    )