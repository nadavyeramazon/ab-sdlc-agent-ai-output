"""FastAPI backend application with greeting endpoint.

This module provides a RESTful API for greeting users in multiple languages.
It includes comprehensive error handling, logging, and CORS support.
"""
import os
import logging
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Application metadata
APP_NAME = "Greeting API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A multi-language greeting API built with FastAPI"

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
# In production, replace ["*"] with specific origins
allowed_origins = os.getenv('ALLOWED_ORIGINS', '*').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allowed_origins == ['*'] else allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS configured with origins: {allowed_origins}")


class GreetingRequest(BaseModel):
    """Request model for greeting endpoint.
    
    Attributes:
        name: User's name (1-100 characters)
        language: Language code (optional, defaults to 'en')
    """
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=100, 
        description="Name of the user to greet",
        example="John Doe"
    )
    language: Optional[str] = Field(
        "en", 
        description="Language code (en, es, fr, de, it)",
        example="en"
    )
    
    @validator('name')
    def validate_name(cls, v):
        """Validate that name is not just whitespace."""
        if not v or not v.strip():
            raise ValueError('Name cannot be empty or just whitespace')
        return v.strip()
    
    @validator('language')
    def validate_language(cls, v):
        """Convert language to lowercase."""
        return v.lower() if v else 'en'


class GreetingResponse(BaseModel):
    """Response model for greeting endpoint.
    
    Attributes:
        message: Personalized greeting message
        name: User's name that was greeted
        language: Language used for the greeting
    """
    message: str = Field(..., description="Greeting message")
    name: str = Field(..., description="Name of the greeted user")
    language: str = Field(..., description="Language used for greeting")


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="API version")


class ErrorResponse(BaseModel):
    """Response model for errors."""
    detail: str = Field(..., description="Error detail message")
    error_code: Optional[str] = Field(None, description="Error code")


# Greeting messages in different languages
GREETINGS = {
    "en": "Hello, {name}! Welcome to our application!",
    "es": "¡Hola, {name}! ¡Bienvenido a nuestra aplicación!",
    "fr": "Bonjour, {name}! Bienvenue dans notre application!",
    "de": "Hallo, {name}! Willkommen in unserer Anwendung!",
    "it": "Ciao, {name}! Benvenuto nella nostra applicazione!",
}

SUPPORTED_LANGUAGES = list(GREETINGS.keys())


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error_code": "INTERNAL_ERROR"}
    )


@app.get("/", tags=["Info"])
async def root():
    """Root endpoint returning API information.
    
    Returns:
        dict: API metadata including name, version, and available endpoints
    """
    logger.debug("Root endpoint accessed")
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "description": APP_DESCRIPTION,
        "endpoints": {
            "/": "GET - API information",
            "/health": "GET - Health check",
            "/api/greet": "POST - Greet a user",
            "/docs": "GET - Interactive API documentation",
            "/redoc": "GET - Alternative API documentation"
        },
        "supported_languages": SUPPORTED_LANGUAGES
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint.
    
    Returns:
        HealthResponse: Service health status
    """
    logger.debug("Health check endpoint accessed")
    return HealthResponse(
        status="healthy",
        service="greeting-api",
        version=APP_VERSION
    )


@app.post(
    "/api/greet", 
    response_model=GreetingResponse,
    responses={
        200: {"description": "Successful greeting"},
        400: {"description": "Invalid language or input", "model": ErrorResponse},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error", "model": ErrorResponse}
    },
    tags=["Greetings"]
)
async def greet_user(request: GreetingRequest):
    """Greet a user in the specified language.
    
    Args:
        request: GreetingRequest containing user name and optional language
    
    Returns:
        GreetingResponse: Personalized greeting message
    
    Raises:
        HTTPException: If language is not supported or other errors occur
    
    Example:
        ```python
        POST /api/greet
        {
            "name": "John",
            "language": "en"
        }
        ```
    """
    try:
        # Validate language
        language = request.language.lower() if request.language else "en"
        
        if language not in GREETINGS:
            logger.warning(
                f"Unsupported language requested: {language} for user: {request.name}"
            )
            raise HTTPException(
                status_code=400,
                detail=f"Language '{language}' is not supported. "
                       f"Available languages: {', '.join(SUPPORTED_LANGUAGES)}"
            )
        
        # Generate greeting message
        message = GREETINGS[language].format(name=request.name)
        
        logger.info(
            f"Greeting generated: user={request.name}, language={language}"
        )
        
        return GreetingResponse(
            message=message,
            name=request.name,
            language=language
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating greeting: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while processing greeting"
        )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0')
    
    logger.info(f"Starting {APP_NAME} v{APP_VERSION} on {host}:{port}")
    
    uvicorn.run(
        app, 
        host=host, 
        port=port,
        log_level=log_level.lower()
    )