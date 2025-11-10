"""FastAPI Backend for Purple Theme Hello World Application

This module provides a simple REST API with three endpoints:
- /api/hello: Returns a hello message with timestamp
- /api/greet: Returns a personalized greeting for a given name
- /health: Returns health status
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict
from pydantic import BaseModel, field_validator
import uvicorn

app = FastAPI(
    title="Purple Theme Hello World API",
    description="Backend API for Hello World fullstack application with purple theme",
    version="2.0.0"
)

# CORS middleware configuration to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods including POST
    allow_headers=["*"],
)


class GreetRequest(BaseModel):
    """Request model for greet endpoint.
    
    Attributes:
        name: User's name (must not be empty or whitespace only)
    """
    name: str
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate that name is not empty or whitespace only.
        
        Args:
            v: Name value to validate
            
        Returns:
            Validated name
            
        Raises:
            ValueError: If name is empty or whitespace only
        """
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


@app.get("/api/hello")
async def get_hello() -> Dict[str, str]:
    """Return hello message with timestamp.
    
    Returns:
        Dict with 'message' and 'timestamp' fields
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/greet")
async def greet_user(request: GreetRequest) -> Dict[str, str]:
    """Return personalized greeting for user.
    
    Args:
        request: GreetRequest containing user's name
        
    Returns:
        Dict with 'greeting' and 'timestamp' fields
        
    Raises:
        HTTPException: 400 if name is invalid
    """
    try:
        # Pydantic validation will handle empty/whitespace check
        name = request.name
        return {
            "greeting": f"Hello, {name}! Welcome to our purple-themed app!",
            "timestamp": datetime.now().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint.
    
    Returns:
        Dict with 'status' field indicating service health
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
