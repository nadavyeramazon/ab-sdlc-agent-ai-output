from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel

app = FastAPI(title="Yellow Theme Hello World API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HelloResponse(BaseModel):
    """Response model for the hello endpoint."""
    message: str
    timestamp: str


class HealthResponse(BaseModel):
    """Response model for the health endpoint."""
    status: str


@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Yellow Theme Hello World API",
        "version": "1.0.0",
        "description": "A simple FastAPI backend for the Hello World fullstack application"
    }


@app.get("/api/hello", response_model=HelloResponse)
async def get_hello():
    """
    Hello World endpoint.
    
    Returns a greeting message with the current timestamp in ISO-8601 format.
    """
    return HelloResponse(
        message="Hello World from Backend!",
        timestamp=datetime.utcnow().isoformat() + 'Z'
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns the health status of the backend service.
    """
    return HealthResponse(status="healthy")
