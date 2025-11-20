"""FastAPI Backend for Hello World Application

This module implements a simple FastAPI backend with the following endpoints:
- GET /api/hello: Returns a greeting message with timestamp
- GET /health: Returns the health status of the service

The API is configured with CORS to allow requests from the frontend running on localhost:3000.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="Hello World API",
    description="A simple FastAPI backend that returns hello world messages",
    version="1.0.0"
)

# CORS configuration to allow frontend access
# This enables the frontend running on localhost:3000 to make requests to this API
origins = [
    "http://localhost:3000",  # React/Frontend development server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies to be included in requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/api/hello")
async def get_hello():
    """
    Returns a hello world message with the current timestamp.
    
    Returns:
        dict: JSON response containing:
            - message (str): Hello world greeting message
            - timestamp (str): Current time in ISO 8601 format
    
    Example Response:
        {
            "message": "Hello World from Backend!",
            "timestamp": "2024-01-15T10:30:45.123456"
        }
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.
    
    Returns:
        dict: JSON response containing:
            - status (str): Health status of the service
    
    Example Response:
        {
            "status": "healthy"
        }
    """
    return {
        "status": "healthy"
    }


# Development server configuration
if __name__ == "__main__":
    # Run the application with uvicorn
    # - host="0.0.0.0": Makes the server accessible externally
    # - port=8000: Default port for the API
    # - reload=True: Auto-reload on code changes (development only)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
