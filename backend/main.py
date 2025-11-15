from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from typing import Dict

# Create FastAPI application instance
app = FastAPI(
    title="Green Theme Hello World API",
    description="Backend API for the Green Theme Hello World fullstack application",
    version="1.0.0"
)

# Configure CORS middleware to allow frontend access
# Allow specific frontend origin as per technical specification
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["GET"],  # Only GET methods needed
    allow_headers=["*"],  # Allow all headers for flexibility
)


@app.get("/api/hello", response_model=Dict[str, str])
async def get_hello_message() -> Dict[str, str]:
    """
    Returns a greeting message with current timestamp.
    
    Returns:
        dict: Contains 'message' and 'timestamp' in ISO 8601 format
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")  # ISO 8601 format with Z suffix
    }


@app.get("/health", response_model=Dict[str, str])
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint to verify service status.
    
    Returns:
        dict: Contains 'status' field indicating service health
    """
    return {"status": "healthy"}
