"""FastAPI backend application for Yellow Theme Hello World.

Provides REST API endpoints for frontend integration with CORS support.
"""
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(
    title="Yellow Theme Hello World Backend",
    description="Simple FastAPI backend for fullstack demo",
    version="1.0.0"
)

# Configure CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://frontend:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/hello")
async def hello():
    """Return hello world message with ISO-8601 timestamp.
    
    Returns:
        dict: Message and timestamp in ISO-8601 format
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/health")
async def health():
    """Health check endpoint.
    
    Returns:
        dict: Service health status
    """
    return {"status": "healthy"}


@app.get("/")
async def root():
    """Root endpoint.
    
    Returns:
        dict: Welcome message
    """
    return {"message": "Yellow Theme Hello World Backend API"}
