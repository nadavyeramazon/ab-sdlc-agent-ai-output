"""Main FastAPI application entry point.

This module initializes and configures the FastAPI application
with all routes and middleware.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .config import settings
from .middleware import RequestLoggingMiddleware

def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="Production-grade Hello World API",
        version="1.0.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Add custom logging middleware
    app.add_middleware(RequestLoggingMiddleware)

    # Include routers
    app.include_router(router, prefix="/api/v1")

    return app

app = create_app()
