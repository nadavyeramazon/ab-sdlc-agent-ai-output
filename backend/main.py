"""FastAPI Backend for Hello World Application

Provides REST API endpoints for the purple-themed Hello World frontend.
Endpoints:
- GET /api/hello: Returns greeting message with timestamp
- POST /api/greet: Returns personalized greeting with timestamp
- GET /health: Health check endpoint
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict
from pydantic import BaseModel, field_validator

app = FastAPI(
    title="Hello World API",
    description="Backend API for Purple Theme Hello World Application",
    version="2.0.0"
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GreetRequest(BaseModel):
    """Request model for personalized greeting.
    
    Attributes:
        name: User's name (required, non-empty after trim)
    """
    name: str
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate that name is non-empty after stripping whitespace.
        
        Args:
            v: Name value to validate
            
        Returns:
            Validated name
            
        Raises:
            ValueError: If name is empty after stripping whitespace
        """
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


class GreetResponse(BaseModel):
    """Response model for personalized greeting.
    
    Attributes:
        greeting: Personalized greeting message
        timestamp: ISO-8601 formatted timestamp
    """
    greeting: str
    timestamp: str


@app.get("/api/hello")
async def get_hello() -> Dict[str, str]:
    """Returns hello message with ISO-8601 timestamp.
    
    Returns:
        Dict containing message and timestamp in ISO-8601 format
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.post("/api/greet")
async def post_greet(request: GreetRequest) -> GreetResponse:
    """Returns personalized greeting with ISO-8601 timestamp.
    
    Args:
        request: GreetRequest containing user's name
        
    Returns:
        GreetResponse containing personalized greeting and timestamp
        
    Raises:
        HTTPException: 400 if name validation fails
        HTTPException: 422 if request body is invalid
    """
    try:
        greeting_message = f"Hello, {request.name}! Welcome to our purple-themed app!"
        return GreetResponse(
            greeting=greeting_message,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint to verify service is running.
    
    Returns:
        Dict containing health status
    """
    return {"status": "healthy"}
