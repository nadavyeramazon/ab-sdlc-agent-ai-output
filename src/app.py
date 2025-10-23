"""Main FastAPI application module."""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routes import router
from .middleware import LoggingMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def create_app() -> FastAPI:
    """Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    settings = get_settings()
    
    # Initialize FastAPI
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug_mode,
        docs_url=f'{settings.api_prefix}/docs',
        redoc_url=f'{settings.api_prefix}/redoc'
    )
    
    # Add middleware
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*']
    )
    
    # Include routes
    app.include_router(router, prefix=settings.api_prefix)
    
    return app

app = create_app()