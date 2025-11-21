from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from datetime import datetime, timezone

# Create FastAPI app instance
app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# Pydantic models for request/response validation
class GreetRequest(BaseModel):
    """Request model for the greet endpoint"""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the user to greet")
    
    @validator('name')
    def name_must_not_be_whitespace(cls, v):
        """Validate that name is not empty or whitespace-only"""
        if not v or not v.strip():
            raise ValueError('Name cannot be empty or whitespace-only')
        return v.strip()

class GreetResponse(BaseModel):
    """Response model for the greet endpoint"""
    greeting: str
    timestamp: str

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/api/hello")
def hello():
    """Hello endpoint with timestamp"""
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/api/greet", response_model=GreetResponse)
async def greet_user(request: GreetRequest):
    """
    Personalized greeting endpoint that accepts a name and returns a greeting.
    
    Request body:
    {
        "name": "John"
    }
    
    Returns:
    {
        "greeting": "Hello, [name]! Welcome to our purple-themed app!",
        "timestamp": "2024-01-15T14:30:00.123456Z"
    }
    """
    # Generate personalized greeting (name is already validated and stripped by Pydantic)
    greeting_message = f"Hello, {request.name}! Welcome to our purple-themed app!"
    
    # Get current timestamp in ISO-8601 format with UTC timezone
    current_timestamp = datetime.now(timezone.utc).isoformat()
    
    return GreetResponse(
        greeting=greeting_message,
        timestamp=current_timestamp
    )
