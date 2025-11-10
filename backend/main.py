"""FastAPI Backend Application

Provides RESTful API endpoints for the Hello World fullstack application.
Includes CORS middleware for frontend communication.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from datetime import datetime
import pytz

# Initialize FastAPI application
app = FastAPI(
    title="Hello World API",
    description="Backend API for Purple Theme Hello World Application",
    version="2.0.0"
)

# Configure CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# Pydantic models for /api/greet endpoint
class GreetRequest(BaseModel):
    """Request model for user greeting endpoint.
    
    Attributes:
        name: User's name for personalization (required, non-empty)
    """
    name: str
    
    @validator('name')
    def validate_name(cls, v):
        """Validate that name is not empty after trimming whitespace.
        
        Args:
            v: The name value to validate
            
        Returns:
            str: Trimmed name value
            
        Raises:
            ValueError: If name is empty after trimming
        """
        trimmed = v.strip()
        if not trimmed:
            raise ValueError('Name cannot be empty')
        return trimmed


class GreetResponse(BaseModel):
    """Response model for user greeting endpoint.
    
    Attributes:
        greeting: Personalized greeting message
        timestamp: ISO-8601 formatted UTC timestamp
    """
    greeting: str
    timestamp: str


@app.get("/api/hello")
async def get_hello():
    """Return hello message with current timestamp.
    
    Returns:
        dict: Contains message and ISO 8601 formatted timestamp
    """
    # Get current UTC time in ISO 8601 format
    current_time = datetime.now(pytz.UTC).isoformat()
    
    return {
        "message": "Hello World from Backend!",
        "timestamp": current_time
    }


@app.post("/api/greet", response_model=GreetResponse)
async def greet_user(request: GreetRequest):
    """Generate personalized greeting for user.
    
    Args:
        request: GreetRequest containing user's name
        
    Returns:
        GreetResponse: Personalized greeting with timestamp
        
    Raises:
        HTTPException: 400 Bad Request if name validation fails
    """
    try:
        # Get the validated (trimmed) name
        name = request.name
        
        # Generate personalized greeting
        greeting_message = f"Hello, {name}! Welcome to our purple-themed app!"
        
        # Generate ISO-8601 timestamp
        current_time = datetime.utcnow().isoformat() + "Z"
        
        return GreetResponse(
            greeting=greeting_message,
            timestamp=current_time
        )
    except ValueError as e:
        # Handle validation errors
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring service status.
    
    Returns:
        dict: Service health status
    """
    return {
        "status": "healthy"
    }


# Root endpoint for API documentation redirect
@app.get("/")
async def root():
    """Root endpoint providing API information.
    
    Returns:
        dict: API welcome message and documentation link
    """
    return {
        "message": "Welcome to Hello World API",
        "docs": "/docs",
        "health": "/health"
    }
