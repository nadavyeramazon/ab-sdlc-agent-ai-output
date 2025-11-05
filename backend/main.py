"""FastAPI Backend Application

A simple Hello World microservice backend that provides:
- Root endpoint with welcome message
- Health check endpoint for monitoring
- API endpoint for frontend communication

Environment Variables:
    ALLOWED_ORIGINS: Comma-separated list of allowed CORS origins (default: "*")
    LOG_LEVEL: Logging level (default: "INFO")
"""

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Configure structured logging
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Hello World Backend API")

# Configure CORS with environment variable support
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins == "*":
    origins = ["*"]
    logger.warning("CORS is configured to allow all origins. Consider restricting in production.")
else:
    origins = [origin.strip() for origin in allowed_origins.split(",")]
    logger.info(f"CORS configured for origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("FastAPI application initialized")


@app.get("/")
async def root():
    """Root endpoint
    
    Returns:
        dict: Welcome message from the backend
    """
    logger.info("Root endpoint accessed")
    return {"message": "How is the weather from FastAPI Backend!"}


@app.get("/health")
async def health():
    """Health check endpoint
    
    Returns:
        dict: Health status of the service
    """
    logger.debug("Health check endpoint accessed")
    return {"status": "healthy"}


@app.get("/api/hello")
async def hello():
    """Hello endpoint for frontend to call
    
    Returns:
        dict: Greeting message with service information
    """
    logger.info("API hello endpoint accessed")
    return {
        "message": "How is the weather from the backend!",
        "status": "success",
        "service": "FastAPI Backend"
    }


if __name__ == "__main__":
    logger.info("Starting FastAPI server on 0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
