"""FastAPI Backend for Green Theme Hello World Application

This module provides a simple REST API with two endpoints:
- /api/hello: Returns a hello message with timestamp
- /health: Returns health status
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict
import uvicorn

app = FastAPI(
    title="Green Theme Hello World API",
    description="Simple backend API for Hello World fullstack application",
    version="1.0.0"
)

# CORS middleware configuration to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/hello")
async def get_hello() -> Dict[str, str]:
    """Return hello message with timestamp.
    
    Returns:
        Dict with 'message' and 'timestamp' fields
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint.
    
    Returns:
        Dict with 'status' field indicating service health
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
