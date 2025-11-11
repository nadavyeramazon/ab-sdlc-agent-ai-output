"""FastAPI Backend Application

Provides a RESTful API for the Hello World fullstack application.
Includes health check and greeting endpoints with CORS support.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="Green Theme Hello World API",
    description="Backend API for fullstack Hello World application",
    version="1.0.0"
)

# Configure CORS middleware
# Allow requests from frontend running on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/hello")
async def get_hello():
    """Return greeting message with current timestamp.
    
    Returns:
        dict: JSON response with message and ISO 8601 formatted timestamp
    """
    current_time = datetime.utcnow().isoformat() + "Z"
    logger.info(f"GET /api/hello - Returning greeting at {current_time}")
    
    return {
        "message": "Hello World from Backend!",
        "timestamp": current_time
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for service monitoring.
    
    Returns:
        dict: JSON response indicating service health status
    """
    logger.info("GET /health - Health check requested")
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
