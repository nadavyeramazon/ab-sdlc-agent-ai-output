from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

# Create FastAPI application instance
app = FastAPI(
    title="Hello World Backend API",
    description="Green Theme Hello World Backend Service",
    version="1.0.0"
)

# ═══════════════════════════════════════════════════════════════════════════════
# CORS MIDDLEWARE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
# Allow frontend running on localhost:3000 to make API calls
# In production, replace with specific frontend domain
# ═══════════════════════════════════════════════════════════════════════════════

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend development server
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)


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
        "version": "1.0.0",
        "theme": "green",
        "endpoints": [
            "/api/hello - Get greeting message with timestamp",
            "/health - Health check endpoint"
        ]
    }
