"""FastAPI main application module.

This module initializes the FastAPI application with CORS middleware
and includes all route handlers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
import os

# Initialize FastAPI application
app = FastAPI(
    title="Hello World API",
    description="Green Theme Hello World Fullstack Application Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Include routers
app.include_router(router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Hello World API",
        "docs": "/docs",
        "health": "/health"
    }
