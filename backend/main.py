from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Green Theme Backend API",
    description="Backend API for Green Theme Hello World Fullstack Application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    logger.info("Health check requested")
    return {"status": "healthy"}

@app.get("/api/hello")
async def hello():
    """
    Hello endpoint that returns a message with current UTC timestamp.
    
    Returns:
        dict: Message and ISO-8601 formatted timestamp
    """
    timestamp = datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
    logger.info(f"Hello endpoint called at {timestamp}")
    
    return {
        "message": "Hello World from Backend!",
        "timestamp": timestamp
    }

@app.on_event("startup")
async def startup_event():
    """Log application startup."""
    logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    """Log application shutdown."""
    logger.info("Application shutdown")
