from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Purple Theme Backend API",
    description="Backend API for Purple Theme Hello World Fullstack Application",
    version="1.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)


class GreetRequest(BaseModel):
    """Request model for the greet endpoint.
    
    Attributes:
        name: User's name for personalized greeting
    """
    name: str


class GreetResponse(BaseModel):
    """Response model for the greet endpoint.
    
    Attributes:
        greeting: Personalized greeting message
        timestamp: ISO 8601 formatted UTC timestamp
    """
    greeting: str
    timestamp: str


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
    timestamp = datetime.utcnow().isoformat(timespec="milliseconds") + "Z"
    logger.info(f"Hello endpoint called at {timestamp}")

    return {"message": "Hello World from Backend!", "timestamp": timestamp}


@app.post("/api/greet", response_model=GreetResponse)
async def greet_user(request: GreetRequest):
    """Generate personalized greeting for user.
    
    Accepts a user's name and returns a personalized greeting message
    with a timestamp. Validates that the name is not empty.
    
    Args:
        request: GreetRequest containing the user's name
        
    Returns:
        GreetResponse with personalized greeting and ISO 8601 timestamp
        
    Raises:
        HTTPException: 400 Bad Request if name is empty or whitespace-only
        
    Example:
        Request: {"name": "Alice"}
        Response: {
            "greeting": "Hello, Alice! Welcome to our purple-themed app!",
            "timestamp": "2024-01-15T14:30:00.123456Z"
        }
    """
    # Trim whitespace and validate
    name = request.name.strip()
    if len(name) == 0:
        logger.warning("Greet endpoint called with empty name")
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty"
        )
    
    # Generate personalized greeting
    greeting = f"Hello, {name}! Welcome to our purple-themed app!"
    
    # Generate ISO 8601 timestamp with UTC indicator
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    logger.info(f"Greet endpoint called for user: {name} at {timestamp}")
    
    return GreetResponse(greeting=greeting, timestamp=timestamp)


@app.on_event("startup")
async def startup_event():
    """Log application startup."""
    logger.info("Application startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Log application shutdown."""
    logger.info("Application shutdown")
