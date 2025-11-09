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
    title="Green Greeting API",
    description="A simple greeting API with health check",
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


class GreetRequest(BaseModel):
    """Request model for greeting endpoint."""
    name: str = Field(..., min_length=1, max_length=100, description="Name to greet")


class GreetResponse(BaseModel):
    """Response model for greeting endpoint."""
    message: str
    name: str


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    service: str
    version: str


@app.get("/", tags=["Root"])
async def root() -> Dict[str, str]:
    """Root endpoint providing API information."""
    return {
        "message": "Welcome to Green Greeting API",
        "docs": "/docs",
        "health": "/health"
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
        service="green-greeting-api",
        version="1.0.0"
    )


@app.post("/greet", response_model=GreetResponse, tags=["Greeting"])
async def greet_user(request: GreetRequest) -> GreetResponse:
    """Greet a user by name.
    
    Args:
        request: GreetRequest containing the name to greet
    
    Returns:
        GreetResponse: Personalized greeting message
    
    Raises:
        HTTPException: If name is invalid
    """
    if not request.name.strip():
        logger.warning(f"Invalid greet request with empty name")
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty or contain only whitespace"
        )
    
    logger.info(f"Greeting user: {request.name}")
    
    return GreetResponse(
        message=f"Hello, {request.name}! Welcome to our green-themed application! 🌿",
        name=request.name
    )


@app.get("/greet/{name}", response_model=GreetResponse, tags=["Greeting"])
async def greet_user_get(name: str) -> GreetResponse:
    """Greet a user by name using GET request.
    
    Args:
        name: Name to greet (path parameter)
    
    Returns:
        GreetResponse: Personalized greeting message
    
    Raises:
        HTTPException: If name is invalid
    """
    if not name or not name.strip():
        logger.warning(f"Invalid greet request with empty name")
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty or contain only whitespace"
        )
    
    if len(name) > 100:
        raise HTTPException(
            status_code=400,
            detail="Name is too long (maximum 100 characters)"
        )
    
    logger.info(f"Greeting user via GET: {name}")
    
    return GreetResponse(
        message=f"Hello, {name}! Welcome to our green-themed application! 🌿",
        name=name
    )
