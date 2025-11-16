from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import os

# Create FastAPI application instance
app = FastAPI(
    title="Purple Theme Greeting API",
    description="Purple-themed Hello World Backend with Personalized Greetings",
    version="1.0.0"
)

# ═══════════════════════════════════════════════════════════════════════════════
# CORS MIDDLEWARE CONFIGURATION - SECURITY CRITICAL
# ═══════════════════════════════════════════════════════════════════════════════
# ⚠️  SECURITY WARNING: Never use '*' wildcard in allow_origins!
#
# Using '*' wildcard creates CRITICAL security vulnerabilities:
#   - Enables XSS attacks from malicious domains
#   - Allows unauthorized data theft from any website  
#   - Permits CSRF attacks against your API
#   - Exposes sensitive user data to untrusted origins
#
# ✅ SECURE CONFIGURATION: Explicitly whitelist only trusted origins
# ═══════════════════════════════════════════════════════════════════════════════

app.add_middleware(
    CORSMiddleware,
    # Explicitly whitelist origins - NO wildcards for production security
    allow_origins=[
        "http://localhost:3000",  # Frontend development server
        os.getenv("FRONTEND_URL", "http://localhost:3000")  # Production frontend from environment
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Only methods we actually use
    allow_headers=["Content-Type", "Authorization"],  # Specific headers only
    expose_headers=[]
)


# ═══════════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class GreetRequest(BaseModel):
    """Request model for greeting endpoint with security validations."""
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,  # Prevent DoS attacks via large payloads
        description="User's name for personalized greeting"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alice"
            }
        }


class GreetResponse(BaseModel):
    """Response model for greeting endpoint."""
    greeting: str
    timestamp: str

    class Config:
        json_schema_extra = {
            "example": {
                "greeting": "Hello, Alice! Welcome to our purple-themed app!",
                "timestamp": "2024-01-15T14:30:00.000Z"
            }
        }


# ═══════════════════════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

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
        # Using modern timezone-aware datetime API (not deprecated utcnow())
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }


@app.post("/api/greet", response_model=GreetResponse)
async def create_greeting(request: GreetRequest):
    """
    Creates a personalized greeting message.
    
    Validates input and returns a customized greeting with timestamp.
    Max length validation prevents DoS attacks via large payloads.
    
    Args:
        request: GreetRequest with user's name
        
    Returns:
        GreetResponse: Personalized greeting with timestamp
        
    Raises:
        HTTPException: 400 if name is empty or only whitespace
    """
    # Validate name is not empty or only whitespace
    if not request.name or not request.name.strip():
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty"
        )
    
    # Generate personalized greeting
    greeting_message = f"Hello, {request.name.strip()}! Welcome to our purple-themed app!"
    
    # Generate ISO 8601 timestamp using modern timezone-aware API
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    
    return GreetResponse(
        greeting=greeting_message,
        timestamp=timestamp
    )


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


@app.get("/")
async def root():
    """
    Root endpoint providing basic API information.
    
    Returns:
        dict: API metadata and available endpoints
    """
    return {
        "service": "Purple Theme Greeting API",
        "version": "1.0.0",
        "theme": "purple",
        "endpoints": [
            "/api/hello - GET greeting message with timestamp",
            "/api/greet - POST personalized greeting",
            "/health - Health check endpoint"
        ]
    }
