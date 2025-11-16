from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

app = FastAPI(title="Hello World API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GreetRequest(BaseModel):
    """Request model for the greet endpoint.
    
    Attributes:
        name: The user's name to personalize the greeting.
    """
    name: str


class GreetResponse(BaseModel):
    """Response model for the greet endpoint.
    
    Attributes:
        greeting: Personalized greeting message.
        timestamp: ISO 8601 formatted timestamp of when the greeting was generated.
    """
    greeting: str
    timestamp: str


class HelloResponse(BaseModel):
    """Response model for the hello endpoint."""
    message: str


class HealthResponse(BaseModel):
    """Response model for the health check endpoint."""
    status: str


@app.get("/api/hello", response_model=HelloResponse)
async def get_hello() -> HelloResponse:
    """Return a hello message from the backend.
    
    Returns:
        HelloResponse with a greeting message.
    """
    return HelloResponse(message="Hello from the backend!")


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint to verify the service is running.
    
    Returns:
        HealthResponse indicating the service is healthy.
    """
    return HealthResponse(status="healthy")


@app.post("/api/greet", response_model=GreetResponse)
async def greet_user(request: GreetRequest) -> GreetResponse:
    """Generate a personalized greeting for the user.
    
    This endpoint accepts a user's name and returns a personalized greeting
    message along with a timestamp. The name is validated to ensure it's not
    empty or whitespace-only.
    
    Args:
        request: GreetRequest containing the user's name.
    
    Returns:
        GreetResponse with personalized greeting and ISO 8601 timestamp.
    
    Raises:
        HTTPException: 400 error if name is empty or whitespace-only.
    """
    # Validate name is not empty after stripping whitespace
    name = request.name.strip()
    
    if not name:
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty"
        )
    
    # Generate personalized greeting
    greeting = f"Hello, {name}! Welcome to our purple-themed app!"
    
    # Generate ISO 8601 timestamp
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    return GreetResponse(greeting=greeting, timestamp=timestamp)