"""FastAPI Backend for Green Theme Hello World Application

Provides RESTful API endpoints for health checks and message retrieval.
Configured with CORS middleware for frontend communication.
"""

from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Green Theme Hello World API",
    description="Backend API for the Green Theme Hello World fullstack application",
    version="1.0.0"
)

# CORS middleware configuration for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint for container and service monitoring.
    
    Returns:
        dict: Status indicating service health
    """
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}


@app.get("/api/hello")
async def get_hello_message():
    """Get hello message with current timestamp.
    
    Returns:
        dict: Message and ISO 8601 formatted timestamp
    """
    # Generate ISO 8601 formatted timestamp
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    logger.info(f"Hello endpoint accessed at {timestamp}")
    
    return {
        "message": "Hello World from Backend!",
        "timestamp": timestamp
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
