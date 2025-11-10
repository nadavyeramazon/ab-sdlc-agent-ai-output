"""FastAPI Backend for Green Theme Hello World Application

Provides REST API endpoints for frontend integration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import uvicorn

app = FastAPI(
    title="Green Theme Hello World API",
    description="Backend API for fullstack Hello World application",
    version="1.0.0"
)

# Configure CORS to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/hello")
async def get_hello():
    """Return hello message with timestamp.
    
    Returns:
        dict: JSON object with message and timestamp
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/health")
async def health_check():
    """Health check endpoint.
    
    Returns:
        dict: JSON object with status
    """
    return {"status": "healthy"}


@app.get("/")
async def root():
    """Root endpoint.
    
    Returns:
        dict: Welcome message
    """
    return {"message": "Welcome to Green Theme Hello World API"}


if __name__ == "__main__":
    # Run with uvicorn when executed directly
    uvicorn.run(app, host="0.0.0.0", port=8000)
