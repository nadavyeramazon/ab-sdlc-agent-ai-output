"""FastAPI Backend Application for Greeting Users"""
import logging
import sys
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from typing import Optional
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Greeting API",
    description="A simple API to greet users with customizable messages",
    version="1.0.0"
)

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log all requests"""
    start_time = datetime.now()
    logger.info(f"Request: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"Status: {response.status_code} Duration: {duration:.3f}s"
        )
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise


class GreetRequest(BaseModel):
    """Request model for greeting endpoint"""
    name: str
    language: Optional[str] = "en"
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        """Validate that name is not empty or whitespace"""
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        # Limit name length for security
        if len(v.strip()) > 100:
            raise ValueError('Name is too long (max 100 characters)')
        return v.strip()
    
    @validator('language')
    def language_must_be_valid(cls, v):
        """Validate that language is supported"""
        valid_languages = ['en', 'es', 'fr', 'de', 'it']
        if v not in valid_languages:
            raise ValueError(f'Language must be one of: {", ".join(valid_languages)}')
        return v


class GreetResponse(BaseModel):
    """Response model for greeting endpoint"""
    message: str
    name: str
    language: str
    timestamp: str


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: str
    timestamp: str


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred. Please try again later.",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.get("/")
async def root():
    """Root endpoint with API information"""
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to the Greeting API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "/greet": "POST - Greet a user by name",
            "/health": "GET - Health check endpoint",
            "/docs": "GET - API documentation"
        },
        "supported_languages": ["en", "es", "fr", "de", "it"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "greeting-api",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/greet", response_model=GreetResponse)
async def greet_user(request: GreetRequest):
    """Greet a user with a personalized message
    
    Args:
        request: GreetRequest containing name and optional language
        
    Returns:
        GreetResponse with personalized greeting message
        
    Raises:
        HTTPException: If validation fails
    """
    logger.info(f"Greeting request for user: {request.name} in language: {request.language}")
    
    # Greeting templates by language
    greetings = {
        "en": f"Hello, {request.name}! Welcome to our application!",
        "es": f"¡Hola, {request.name}! ¡Bienvenido a nuestra aplicación!",
        "fr": f"Bonjour, {request.name}! Bienvenue dans notre application!",
        "de": f"Hallo, {request.name}! Willkommen in unserer Anwendung!",
        "it": f"Ciao, {request.name}! Benvenuto nella nostra applicazione!"
    }
    
    message = greetings.get(request.language, greetings["en"])
    
    response = GreetResponse(
        message=message,
        name=request.name,
        language=request.language,
        timestamp=datetime.utcnow().isoformat()
    )
    
    logger.info(f"Successfully generated greeting for {request.name}")
    return response


if __name__ == "__main__":
    logger.info("Starting Greeting API server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )