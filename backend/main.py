from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict

# Create FastAPI application instance
app = FastAPI()

# CORS configuration - allow frontend on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET"],
    allow_headers=["Content-Type"],
)


@app.get("/api/hello")
async def get_hello() -> Dict[str, str]:
    """
    Returns a hello world message with current timestamp.
    
    Returns:
        JSON with message and ISO-8601 formatted timestamp
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Simple health check endpoint.
    
    Returns:
        JSON with healthy status
    """
    return {"status": "healthy"}
