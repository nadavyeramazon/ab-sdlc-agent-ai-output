"""FastAPI Backend for Hello World Application.

Provides REST API endpoints for the frontend to fetch greeting messages
with timestamps and health check functionality.
"""

from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="Hello World API",
    description="Backend API for Yellow Theme Hello World Application",
    version="1.0.0"
)

# Configure CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/api/hello")
async def get_hello():
    """Return greeting message with ISO-8601 timestamp.
    
    Returns:
        dict: JSON response with message and timestamp
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring service availability.
    
    Returns:
        dict: JSON response with health status
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    # Run the application with Uvicorn server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload for development
    )
