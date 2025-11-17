"""FastAPI Backend for Hello World Application

This module provides a simple REST API with two endpoints:
- /api/hello: Returns a greeting message with timestamp
- /health: Health check endpoint

CORS is configured to allow requests from the frontend running on localhost:3000.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="Hello World API",
    description="Simple backend API for Hello World fullstack application",
    version="1.0.0"
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/api/hello")
async def get_hello():
    """Return Hello World message with current timestamp.
    
    Returns:
        dict: JSON response with message and ISO 8601 timestamp
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint to verify service is running.
    
    Returns:
        dict: JSON response with health status
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    # Run the application with uvicorn server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload for development
    )
