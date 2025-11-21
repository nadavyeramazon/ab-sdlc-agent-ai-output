from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Dict

# Create FastAPI application instance
app = FastAPI()

# CORS configuration - allow frontend on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


# Pydantic models for greet endpoint
class GreetRequest(BaseModel):
    name: str


class GreetResponse(BaseModel):
    greeting: str
    timestamp: str


@app.get("/api/hello")
async def get_hello() -> Dict[str, str]:
    """
    Returns a hello world message with current timestamp.
    
    Returns:
        JSON with message and ISO-8601 formatted timestamp
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Simple health check endpoint.
    
    Returns:
        JSON with healthy status
    """
    return {"status": "healthy"}


@app.post("/api/greet", response_model=GreetResponse)
async def greet_user(request: GreetRequest):
    """
    Generate a personalized greeting for the user.
    
    Args:
        request: GreetRequest with name field
        
    Returns:
        GreetResponse with personalized greeting and timestamp
        
    Raises:
        HTTPException 400: If name is empty or whitespace-only
    """
    # Validate name is not empty or whitespace
    if not request.name or not request.name.strip():
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty"
        )
    
    # Generate personalized greeting
    name = request.name.strip()
    greeting_message = f"Hello, {name}! Welcome to our purple-themed app!"
    
    # Generate ISO-8601 timestamp
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    return GreetResponse(
        greeting=greeting_message,
        timestamp=timestamp
    )
