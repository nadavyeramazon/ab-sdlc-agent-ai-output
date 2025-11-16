from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from pydantic import BaseModel, Field, validator
import os

# Create FastAPI application instance
app = FastAPI(
    title="Hello World Backend API",
    description="Purple Theme Hello World Backend Service with Personalized Greeting",
    version="1.2.0"
)

# ═══════════════════════════════════════════════════════════════════════════════
# CORS MIDDLEWARE CONFIGURATION - SECURITY CRITICAL
# ═══════════════════════════════════════════════════════════════════════════════
# 
# ⚠️  SECURITY WARNING: NEVER USE WILDCARD '*' IN allow_origins ⚠️
#
# Using '*' wildcard in allow_origins creates CRITICAL security vulnerabilities:
#   1. XSS (Cross-Site Scripting) Attacks:
#      - ANY malicious website can make requests to this API
#      - Attackers can steal user data, session tokens, and credentials
#   
#   2. Data Theft:
#      - Unauthorized domains can access sensitive API endpoints
#      - User information and application data exposed to any website
#   
#   3. CSRF (Cross-Site Request Forgery) Attacks:
#      - Malicious sites can forge requests on behalf of legitimate users
#      - Can lead to unauthorized actions and data manipulation
#   
#   4. API Abuse:
#      - Any website can consume API resources
#      - No control over who accesses the backend
#
# ✅ SECURE CONFIGURATION (Current Implementation):
#   - Explicitly list ONLY trusted frontend domains
#   - Use specific origins: http://localhost:3000 for development
#   - Use environment variables for production domains
#   - NEVER add '*' to the allow_origins list
#
# This configuration allows the React frontend running on localhost:3000 to make
# API calls while blocking all other origins for security.
# ═══════════════════════════════════════════════════════════════════════════════

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend development server (local only)
        os.getenv("FRONTEND_URL", "http://localhost:3000"),  # Production override via environment
        # ⚠️  NEVER add '*' here - it's a critical security vulnerability
        # ⚠️  Only add specific, trusted domains that need API access
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allow common HTTP methods
    allow_headers=["*"],  # Allow all headers (validated by origin check)
    expose_headers=["*"]  # Expose all headers to the client
)


# Pydantic Models for Greet Endpoint
class GreetRequest(BaseModel):
    """Request model for greet endpoint with validation.
    
    Security features:
    - Max length validation (100 chars) prevents DoS attacks via large payloads
    - Whitespace validation ensures meaningful input
    - Input sanitization via Pydantic validation
    """
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=100,  # DoS prevention: Limit input size to prevent memory exhaustion
        description="User's name (1-100 characters)"
    )
    
    @validator('name')
    def name_must_not_be_whitespace(cls, v):
        """Validate that name is not empty or whitespace-only."""
        if not v or not v.strip():
            raise ValueError('Name cannot be empty or whitespace-only')
        return v.strip()


class GreetResponse(BaseModel):
    """Response model for greet endpoint."""
    greeting: str
    timestamp: str


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
async def greet_user(request: GreetRequest):
    """
    Generate personalized greeting for user.
    
    Accepts a name and returns a personalized greeting message with timestamp.
    Validates that the name is not empty, not whitespace-only, and within length limits (1-100 chars).
    
    Security:
    - Max length validation (100 chars) prevents DoS attacks
    - Whitespace validation prevents empty submissions
    - Input sanitization via Pydantic validation
    
    Args:
        request: GreetRequest containing user's name (validated by Pydantic)
    
    Returns:
        GreetResponse: Personalized greeting and timestamp
    
    Raises:
        HTTPException: 422 error if name validation fails (handled by Pydantic)
    """
    # Name is already validated and trimmed by Pydantic validator
    name = request.name
    
    # Generate personalized greeting
    greeting = f"Hello, {name}! Welcome to our purple-themed app!"
    
    # Generate timestamp in ISO 8601 format with Z suffix
    # Using modern timezone-aware datetime API instead of deprecated utcnow()
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    
    return GreetResponse(greeting=greeting, timestamp=timestamp)


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
        "version": "1.2.0",
        "theme": "purple",
        "endpoints": [
            "/api/hello - Get greeting message with timestamp",
            "/api/greet - Post name to receive personalized greeting",
            "/health - Health check endpoint"
        ]
    }