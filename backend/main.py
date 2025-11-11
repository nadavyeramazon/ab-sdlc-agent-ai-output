"""FastAPI backend for Hello World fullstack application.

Provides two endpoints:
- GET /api/hello: Returns hello message with timestamp
- GET /health: Health check endpoint
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

app = FastAPI(
    title="Hello World Backend",
    description="Green Theme Hello World Fullstack Application Backend",
    version="1.0.0"
)

# Configure CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/hello")
async def get_hello():
    """Return hello message with ISO timestamp.
    
    Returns:
        dict: JSON response with message and timestamp
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring.
    
    Returns:
        dict: JSON response with health status
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
