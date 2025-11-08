"""FastAPI Backend Application for User Greeting Service.

This module provides a simple greeting API endpoint that accepts a user's name
and returns a personalized greeting message.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="User Greeting API",
    description="A simple API for greeting users with personalized messages",
    version="1.0.0"
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GreetingRequest(BaseModel):
    """Request model for greeting endpoint."""
    name: str = Field(..., min_length=1, max_length=100, description="User's name")
    title: Optional[str] = Field(None, max_length=50, description="Optional title (Mr., Ms., Dr., etc.)")
    
    @validator('name')
    def validate_name(cls, v):
        """Validate that name contains only valid characters."""
        if not v.strip():
            raise ValueError('Name cannot be empty or whitespace only')
        # Allow letters, spaces, hyphens, and apostrophes
        if not all(c.isalpha() or c in ' -\'' for c in v):
            raise ValueError('Name can only contain letters, spaces, hyphens, and apostrophes')
        return v.strip()
    
    @validator('title')
    def validate_title(cls, v):
        """Validate title if provided."""
        if v is not None:
            v = v.strip()
            if v and not v.replace('.', '').isalpha():
                raise ValueError('Title can only contain letters and periods')
            return v if v else None
        return v


class GreetingResponse(BaseModel):
    """Response model for greeting endpoint."""
    message: str = Field(..., description="Personalized greeting message")
    name: str = Field(..., description="User's name")
    success: bool = Field(True, description="Request success status")


@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "service": "User Greeting API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "greet": "/api/greet",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "greeting-api"
    }


@app.post("/api/greet", response_model=GreetingResponse)
async def greet_user(request: GreetingRequest):
    """Greet a user with a personalized message.
    
    Args:
        request: GreetingRequest containing user's name and optional title
        
    Returns:
        GreetingResponse with personalized greeting message
        
    Raises:
        HTTPException: If request validation fails
    """
    try:
        # Build the greeting message
        if request.title:
            full_name = f"{request.title} {request.name}"
        else:
            full_name = request.name
        
        greeting_message = f"Hello, {full_name}! Welcome to our service. We're delighted to greet you today!"
        
        logger.info(f"Greeting user: {full_name}")
        
        return GreetingResponse(
            message=greeting_message,
            name=request.name,
            success=True
        )
    except Exception as e:
        logger.error(f"Error greeting user: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your greeting request"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
