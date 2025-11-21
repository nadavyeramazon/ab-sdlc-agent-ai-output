"""Minimal FastAPI backend for Yellow Theme Hello World application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# Enable CORS for frontend running on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/hello")
async def get_hello():
    """
    Hello World endpoint.
    
    Returns a greeting message with the current timestamp in ISO-8601 format.
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns the health status of the backend service.
    """
    return {"status": "healthy"}
