from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel

# Create FastAPI application instance
app = FastAPI(
    title="Hello World Backend API",
    description="Green-themed fullstack application backend",
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
            "/health"
        ]
    }
