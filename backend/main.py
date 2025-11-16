"""FastAPI backend with hello world and personalized greeting endpoints."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Purple Theme Greeting API",
    description="A simple API with hello world and personalized greeting endpoints",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GreetRequest(BaseModel):
    """Request model for greeting endpoint."""
    name: str

    @validator('name')
    def validate_name(cls, v):
        """Validate that name is not empty or whitespace only."""
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


class GreetResponse(BaseModel):
    """Response model for greeting endpoint."""
    greeting: str
    timestamp: str


@app.get("/api/hello")
async def hello():
    """Hello world endpoint.
    
    Returns a simple hello message from the backend.
    This is the existing functionality that must remain unchanged.
    """
    logger.info("Hello endpoint called")
    return {"message": "Hello from FastAPI backend!"}


@app.get("/health")
async def health_check():
    """Health check endpoint.
    
    Returns the health status of the service.
    Used by Docker healthcheck and monitoring.
    """
    return {"status": "healthy"}


@app.post("/api/greet", response_model=GreetResponse)
async def greet_user(request: GreetRequest):
    """Personalized greeting endpoint.
    
    Args:
        request: GreetRequest containing user's name
        
    Returns:
        GreetResponse with personalized greeting and timestamp
        
    Raises:
        HTTPException: 400 if name is empty or validation fails
    """
    try:
        # Generate personalized greeting message
        greeting_message = f"Hello, {request.name}! Welcome to our purple-themed app!"
        
        # Generate ISO-8601 timestamp (UTC)
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        logger.info(f"Greeted user: {request.name}")
        
        return GreetResponse(
            greeting=greeting_message,
            timestamp=timestamp
        )
    except ValueError as e:
        # Handle validation errors from Pydantic
        logger.warning(f"Validation error for greet: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty"
        )
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Error in greet endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
