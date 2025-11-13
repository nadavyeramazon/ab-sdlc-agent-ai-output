from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel

# Create FastAPI application instance
app = FastAPI(
    title="Hello World Backend API",
    description="Purple-themed fullstack application backend",
    version="1.0.0"
)

# Configure CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Response models
class HelloResponse(BaseModel):
    """Response model for hello endpoint"""
    message: str
    timestamp: str

class HealthResponse(BaseModel):
    """Response model for health endpoint"""
    status: str

# Request/Response models for greet endpoint
class GreetRequest(BaseModel):
    """Request model for greet endpoint"""
    name: str

class GreetResponse(BaseModel):
    """Response model for greet endpoint"""
    greeting: str
    timestamp: str

@app.get("/api/hello", response_model=HelloResponse)
async def get_hello() -> HelloResponse:
    """
    Return a greeting message with current timestamp.
    
    Returns:
        HelloResponse: JSON with message and ISO 8601 timestamp
    """
    return HelloResponse(
        message="Hello World from Backend!",
        timestamp=datetime.utcnow().isoformat() + "Z"
    )

@app.post("/api/greet", response_model=GreetResponse)
async def greet_user(request: GreetRequest) -> GreetResponse:
    """
    Return a personalized greeting message with timestamp.
    
    Args:
        request: GreetRequest containing the user's name
    
    Returns:
        GreetResponse: JSON with personalized greeting and ISO 8601 timestamp
    
    Raises:
        HTTPException: 400 if name is empty or whitespace-only
    
    Example:
        Request: {"name": "Alice"}
        Response: {
            "greeting": "Hello, Alice! Welcome to our purple-themed app!",
            "timestamp": "2024-01-15T14:32:10.123456Z"
        }
    """
    # Validate that name is not empty or whitespace-only
    if not request.name.strip():
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty"
        )
    
    # Trim whitespace from name
    clean_name = request.name.strip()
    
    # Generate personalized greeting
    greeting_message = f"Hello, {clean_name}! Welcome to our purple-themed app!"
    
    # Generate ISO-8601 timestamp
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    return GreetResponse(
        greeting=greeting_message,
        timestamp=timestamp
    )

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint for monitoring.
    
    Returns:
        HealthResponse: JSON with status "healthy"
    """
    return HealthResponse(status="healthy")

# Root endpoint for basic info
@app.get("/")
async def root():
    """
    Root endpoint providing API information.
    
    Returns:
        dict: API name and available endpoints
    """
    return {
        "name": "Hello World Backend API",
        "endpoints": [
            "/api/hello",
            "/api/greet",
            "/health"
        ]
    }
