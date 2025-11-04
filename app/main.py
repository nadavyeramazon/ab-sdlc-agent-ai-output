from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.router import api_router


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Backend API for AB SDLC Agent AI Application",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API router
    application.include_router(api_router, prefix="/api/v1")
    
    return application


app = create_application()


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return JSONResponse(
        content={
            "message": "Welcome to AB SDLC Agent AI Backend API",
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "health": "/api/v1/health"
        }
    )


@app.on_event("startup")
async def startup_event():
    """Execute on application startup"""
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug mode: {settings.DEBUG}")


@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown"""
    print(f"Shutting down {settings.APP_NAME}")