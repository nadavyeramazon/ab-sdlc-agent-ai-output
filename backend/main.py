from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

# Create FastAPI application instance
app = FastAPI(
    title="Hello World Backend API",
    description="Green Theme Hello World Backend Service",
    version="1.0.0"
)

# Configure CORS middleware to allow frontend communication
# This enables the React frontend running on localhost:3000 to make API calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend development server
        os.getenv("FRONTEND_URL", "http://localhost:3000")  # Allow environment override
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allow all common HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/api/hello")
async def get_hello():
    """
    Returns a greeting message with current timestamp.
    
    This endpoint provides dynamic content to demonstrate
    frontend-backend communication.
    
    Returns:
        dict: JSON object containing message and ISO8601 timestamp
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.utcnow().isoformat() + "Z"  # ISO8601 format with UTC timezone
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for service monitoring.
    
    Used by Docker, Kubernetes, or monitoring tools to verify
    the service is running and responsive.
    
    Returns:
        dict: JSON object indicating service health status
    """
    return {"status": "healthy"}


# Root endpoint for basic service information
@app.get("/")
async def root():
    """
    Root endpoint providing basic API information.
    
    Returns:
        dict: API metadata and available endpoints
    """
    return {
        "service": "Hello World Backend API",
        "version": "1.0.0",
        "endpoints": [
            "/api/hello - Get greeting message with timestamp",
            "/health - Health check endpoint"
        ]
    }
