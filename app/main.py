from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.v1.router import api_router
from app.middleware.cors import setup_cors


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Setup CORS
    setup_cors(app)
    
    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    
    # Root endpoint
    @app.get("/")
    async def root():
        return JSONResponse(
            content={
                "message": f"Welcome to {settings.APP_NAME}",
                "version": settings.APP_VERSION,
                "docs": "/docs",
                "health": f"{settings.API_V1_PREFIX}/health"
            }
        )
    
    return app


app = create_application()