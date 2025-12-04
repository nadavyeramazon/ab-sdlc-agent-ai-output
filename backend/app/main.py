"""
FastAPI Task Manager Application Factory.

This module provides the application factory function for creating and
configuring the FastAPI application instance with all necessary middleware,
routers, and settings.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.health import router as health_router
from app.routes.tasks import router as tasks_router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    This factory function creates a new FastAPI instance and configures it with:
    - Application metadata (title, description, version)
    - CORS middleware for cross-origin requests
    - Health check router
    - Tasks router with /api prefix

    Returns:
        Configured FastAPI application instance
    """
    # Create FastAPI instance with metadata and configuration
    app = FastAPI(
        title="Task Manager API",
        description="A RESTful API for managing tasks",
        version="1.0.0",
        redirect_slashes=False,
    )

    # Configure CORS middleware using settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )

    # Include routers
    app.include_router(health_router)
    app.include_router(tasks_router, prefix="/api")

    return app


# Create app instance at module level for uvicorn
app = create_app()
