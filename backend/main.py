"""FastAPI Backend for Hello World Application

Provides REST API endpoints for the green-themed Hello World frontend.
Endpoints:
- GET /api/hello: Returns greeting message with timestamp
- GET /health: Health check endpoint
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict

app = FastAPI(
    title="Hello World API",
    description="Backend API for Green Theme Hello World Application",
    version="1.0.0"
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint to verify service is running.
    
    Returns:
        Dict containing health status
    """
    return {"status": "healthy"}
