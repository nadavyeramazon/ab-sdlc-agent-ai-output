from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Greeting API")

# Get allowed origins from environment variable, default to frontend container
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:8080"
).split(",")

logger.info(f"Allowed CORS origins: {ALLOWED_ORIGINS}")

# Configure CORS with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

class GreetingRequest(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the person to greet"
    )
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        # Strip whitespace
        v = v.strip()
        
        # Check if empty after stripping
        if not v:
            raise ValueError('Name cannot be empty or only whitespace')
        
        # Check length
        if len(v) > 100:
            raise ValueError('Name is too long (maximum 100 characters)')
        
        # Basic sanitization - allow only alphanumeric, spaces, hyphens, and apostrophes
        if not all(c.isalnum() or c.isspace() or c in "-'" for c in v):
            raise ValueError('Name contains invalid characters')
        
        return v

class GreetingResponse(BaseModel):
    message: str

@app.get("/")
async def root():
    """Root endpoint returning API information"""
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Greeting API", "version": "1.0.0"}

@app.post("/greet", response_model=GreetingResponse)
async def greet_user(request: GreetingRequest):
    """
    Greet a user by their name with validation
    
    Args:
        request: GreetingRequest containing the name
    
    Returns:
        GreetingResponse with personalized greeting message
    
    Raises:
        HTTPException: 422 if validation fails
    """
    try:
        logger.info(f"Greeting request received for name: {request.name}")
        greeting_message = f"Hello, {request.name}! Welcome to our green-themed application! 🌿"
        logger.info(f"Greeting generated successfully for: {request.name}")
        return GreetingResponse(message=greeting_message)
    except Exception as e:
        logger.error(f"Error generating greeting: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration"""
    logger.debug("Health check endpoint accessed")
    return {"status": "healthy", "service": "greeting-api"}
