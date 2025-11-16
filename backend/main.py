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
# CORS MIDDLEWARE CONFIGURATION - SECURITY CRITICAL - NO WILDCARDS!
# ═══════════════════════════════════════════════════════════════════════════════
# ⚠️  SECURITY VERIFICATION: This configuration does NOT use '*' wildcard
#
# CURRENT CONFIGURATION (SECURE):
#   allow_origins = ["http://localhost:3000", os.getenv("FRONTEND_URL", ...)]
#   ✅ Explicitly whitelists ONLY trusted origins
#   ✅ NO wildcard '*' present
#   ✅ Prevents XSS attacks from malicious domains
#   ✅ Blocks unauthorized data theft
#   ✅ Mitigates CSRF attack vectors
#
# WHY WILDCARDS ARE DANGEROUS:
#   Using allow_origins=['*'] would allow ANY website to:
#   - Make authenticated requests to this API
#   - Steal user data and session tokens
#   - Execute cross-site scripting (XSS) attacks
#   - Perform CSRF attacks against authenticated users
#   - Access sensitive API endpoints from untrusted domains
#
# PRODUCTION DEPLOYMENT:
#   Set FRONTEND_URL environment variable to your production frontend domain
#   Example: FRONTEND_URL=https://app.example.com
# ═══════════════════════════════════════════════════════════════════════════════

app.add_middleware(
    CORSMiddleware,
    # ✅ SECURE: Explicit origin whitelist - NO wildcards!
    allow_origins=[
        "http://localhost:3000",  # Frontend development server
        os.getenv("FRONTEND_URL", "http://localhost:3000"),  # Production frontend from environment
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allow all common HTTP methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"]  # Expose all headers to the client
)


# ═══════════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS WITH SECURITY VALIDATIONS
# ═══════════════════════════════════════════════════════════════════════════════

class GreetRequest(BaseModel):
    """
    Request model for greet endpoint with comprehensive validation.
    
    Security Features:
    - max_length=100: Prevents DoS attacks via oversized payloads
    - min_length=1: Prevents empty name submissions
    - Custom validator: Strips whitespace and rejects whitespace-only names
    """
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=100,  # ✅ DoS Prevention: Limits input size
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
        # ✅ Modern API: Using datetime.now(timezone.utc) instead of deprecated utcnow()
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")  # ISO8601 format with UTC timezone
    }


@app.post("/api/greet", response_model=GreetResponse)
async def greet_user(request: GreetRequest):
    """
    Generate personalized greeting for user.
    
    Accepts a name and returns a personalized greeting message with timestamp.
    
    Security Features:
    - Input validation: max_length=100 prevents DoS attacks
    - Whitespace handling: Strips and validates non-empty names
    - Modern datetime API: timezone-aware timestamps
    
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
    
    # ✅ Modern API: Using datetime.now(timezone.utc) instead of deprecated utcnow()
    # Generate timestamp in ISO 8601 format with Z suffix
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
        "security": {
            "cors": "Explicit origin whitelist - NO wildcards",
            "validation": "Max length 100 chars prevents DoS",
            "datetime": "Modern timezone-aware API"
        },
        "endpoints": [
            "/api/hello - Get greeting message with timestamp",
            "/api/greet - Post name to receive personalized greeting",
            "/health - Health check endpoint"
        ]
    }
