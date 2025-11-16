"""FastAPI backend application with health and greeting endpoints."""

from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Purple Greeting API",
    description="A Hello World API with personalized greeting support",
    version="1.0.0"
)

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GreetRequest(BaseModel):
    """Request model for greet endpoint."""
    name: str


class GreetResponse(BaseModel):
    """Response model for greet endpoint."""
    greeting: str
    timestamp: str


class HelloResponse(BaseModel):
    """Response model for hello endpoint."""
    message: str


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str


@app.get("/api/hello", response_model=HelloResponse, tags=["Hello"])
async def hello() -> HelloResponse:
    """Hello World endpoint.
    
    Returns:
        HelloResponse: Hello World message
    """
    logger.info("Hello endpoint called")
    return HelloResponse(message="Hello World from Backend!")


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Health check endpoint to verify service is running.
    
    Returns:
        HealthResponse: Service health status
    """
    logger.info("Health check requested")
    return HealthResponse(status="healthy")


@app.post("/api/greet", response_model=GreetResponse, tags=["Greeting"])
async def greet_user(request: GreetRequest) -> GreetResponse:
    """Generate personalized greeting.
    
    Args:
        request: GreetRequest containing the name to greet
    
    Returns:
        GreetResponse: Personalized greeting with timestamp
    
    Raises:
        HTTPException: If name is empty or contains only whitespace
    """
    name = request.name.strip()
    
    if len(name) == 0:
        logger.warning("Greet request with empty name")
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    logger.info(f"Greeting user: {name}")
    
    greeting = f"Hello, {name}! Welcome to our purple-themed app!"
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    return GreetResponse(greeting=greeting, timestamp=timestamp)