"""FastAPI Backend for Green Theme Hello World Application.

This module provides a simple REST API with two endpoints:
- /api/hello: Returns a hello message with timestamp
- /health: Health check endpoint for monitoring

CORS is enabled for frontend communication on localhost:3000.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="Green Theme Hello World API",
    description="Backend API for the Green Theme Hello World Fullstack Application",
    version="1.0.0"
)

# Configure CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/api/hello")
async def get_hello():
    """Return hello message with current timestamp.
    
    Returns:
        dict: JSON response with message and ISO format timestamp
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for service monitoring.
    
    Returns:
        dict: JSON response with health status
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    # Run the application with uvicorn server
    # reload=True enables hot reload for development
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
