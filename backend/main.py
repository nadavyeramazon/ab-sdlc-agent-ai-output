"""FastAPI Backend for Purple Theme Hello World Application.

This module provides a REST API with three endpoints:
- /api/hello: Returns a hello message with timestamp
- /api/greet: Accepts user name and returns personalized greeting
- /health: Health check endpoint for monitoring

CORS is enabled for frontend communication on localhost:3000.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from datetime import datetime
import uvicorn
import re

# Initialize FastAPI application
app = FastAPI(
    title="Purple Theme Hello World API",
    description="Backend API for the Purple Theme Hello World Fullstack Application",
    version="2.0.0"
)

# Configure CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Pydantic models for request/response validation
class GreetRequest(BaseModel):
    """Request model for /api/greet endpoint.
    
    Attributes:
        name (str): User's name for personalized greeting
    """
    name: str
    
    @validator('name')
    def validate_name(cls, v):
        """Validate that name is not empty or whitespace-only.
        
        Args:
            v (str): Name value to validate
            
        Returns:
            str: Validated and trimmed name
            
        Raises:
            ValueError: If name is empty or whitespace-only
        """
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


class GreetResponse(BaseModel):
    """Response model for /api/greet endpoint.
    
    Attributes:
        greeting (str): Personalized greeting message
        timestamp (str): ISO-8601 formatted UTC timestamp
    """
    greeting: str
    timestamp: str


@app.get("/api/hello")
async def get_hello():
    """Return hello message with current timestamp.
    
    This is the EXISTING endpoint - preserved unchanged for regression testing.
    
    Returns:
        dict: JSON response with message and ISO format timestamp
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.post("/api/greet", response_model=GreetResponse)
async def greet_user(request: GreetRequest):
    """Generate personalized greeting for the user.
    
    This is the NEW feature endpoint - implements personalized greetings.
    Validates input, sanitizes name, and returns personalized message.
    
    Args:
        request (GreetRequest): Request containing user's name
        
    Returns:
        GreetResponse: Personalized greeting with timestamp
        
    Raises:
        HTTPException: 400 error if name is empty or whitespace-only
        HTTPException: 422 error if validation fails (Pydantic)
    """
    # Name is already validated and trimmed by Pydantic validator
    name = request.name
    
    # Additional validation: check for reasonable length (optional security measure)
    if len(name) > 100:
        raise HTTPException(
            status_code=400,
            detail="Name is too long (maximum 100 characters)"
        )
    
    # Generate personalized greeting as per specification
    greeting_message = f"Hello, {name}! Welcome to our purple-themed app!"
    
    # Create response with current timestamp in ISO-8601 format
    return GreetResponse(
        greeting=greeting_message,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )


@app.get("/health")
async def health_check():
    """Health check endpoint for service monitoring.
    
    This is the EXISTING endpoint - preserved unchanged for regression testing.
    
    Returns:
        dict: JSON response with health status
    """
    return {"status": "healthy"}


# Exception handler for Pydantic validation errors
@app.exception_handler(ValueError)
async def validation_exception_handler(request, exc):
    """Handle validation errors from Pydantic models.
    
    Args:
        request: The request that caused the error
        exc: The ValueError exception
        
    Returns:
        HTTPException: 400 error with validation message
    """
    raise HTTPException(status_code=400, detail=str(exc))


if __name__ == "__main__":
    # Run the application with uvicorn server
    # reload=True enables hot reload for development
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
