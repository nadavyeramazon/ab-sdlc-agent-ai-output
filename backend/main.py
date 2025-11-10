"""FastAPI Backend Application

Provides RESTful API endpoints for the Hello World fullstack application.
Includes CORS middleware for frontend communication.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz

# Initialize FastAPI application
app = FastAPI(
    title="Hello World API",
    description="Backend API for Green Theme Hello World Application",
    version="1.0.0"
)

# Configure CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/api/hello")
async def get_hello():
    """Return hello message with current timestamp.
    
    Returns:
        dict: Contains message and ISO 8601 formatted timestamp
    """
    # Get current UTC time in ISO 8601 format
    current_time = datetime.now(pytz.UTC).isoformat()
    
    return {
        "message": "Hello World from Backend!",
        "timestamp": current_time
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring service status.
    
    Returns:
        dict: Service health status
    """
    return {
        "status": "healthy"
    }


# Root endpoint for API documentation redirect
@app.get("/")
async def root():
    """Root endpoint providing API information.
    
    Returns:
        dict: API welcome message and documentation link
    """
    return {
        "message": "Welcome to Hello World API",
        "docs": "/docs",
        "health": "/health"
    }
