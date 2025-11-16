from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel
import os

# Create FastAPI application instance
app = FastAPI(
    title="Hello World Backend API",
    description="Purple Theme Hello World Backend Service with Personalized Greeting",
    version="1.2.0"
)

# Configure CORS middleware to allow frontend communication
# This enables the React frontend running on localhost:3000 to make API calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend development server
        os.getenv("FRONTEND_URL", "http://localhost:3000")  # Allow environment override
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allow all common HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Pydantic Models for Greet Endpoint
class GreetRequest(BaseModel):
    """Request model for greet endpoint."""
    name: str


class GreetResponse(BaseModel):
    """Response model for greet endpoint."""
    greeting: str
    timestamp: str


@app.get("/api/hello")
async def get_hello():
    """
    Returns a greeting message with current timestamp.
    
    This endpoint provides dynamic content to demonstrate
    frontend-backend communication.
    
    Returns:
        dict: JSON object containing message and ISO8601 timestamp
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.utcnow().isoformat() + "Z"  # ISO8601 format with UTC timezone
    }


@app.post("/api/greet", response_model=GreetResponse)
async def greet_user(request: GreetRequest):
    """
    Generate personalized greeting for user.
    
    Accepts a name and returns a personalized greeting message with timestamp.
    Validates that the name is not empty or whitespace-only.
    
    Args:
        request: GreetRequest containing user's name
    
    Returns:
        GreetResponse: Personalized greeting and timestamp
    
    Raises:
        HTTPException: 400 error if name is empty or whitespace-only
    """
    # Extract and trim the name
    name = request.name.strip()
    
    # Validate name is not empty
    if len(name) == 0:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    # Generate personalized greeting
    greeting = f"Hello, {name}! Welcome to our purple-themed app!"
    
    # Generate timestamp in ISO 8601 format with Z suffix
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    return GreetResponse(greeting=greeting, timestamp=timestamp)


@app.get("/health")
async def health_check():
    """
    Health check endpoint for service monitoring.
    
    Used by Docker, Kubernetes, or monitoring tools to verify
    the service is running and responsive.
    
    Returns:
        dict: JSON object indicating service health status
    """
    return {"status": "healthy"}


# Root endpoint for basic service information
@app.get("/")
async def root():
    """
    Root endpoint providing basic API information.
    
    Returns:
        dict: API metadata and available endpoints
    """
    return {
        "service": "Hello World Backend API",
        "version": "1.2.0",
        "theme": "purple",
        "endpoints": [
            "/api/hello - Get greeting message with timestamp",
            "/api/greet - Post name to receive personalized greeting",
            "/health - Health check endpoint"
        ]
    }
