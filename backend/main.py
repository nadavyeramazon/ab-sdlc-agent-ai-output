"""FastAPI backend application with greeting endpoint."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Greeting API",
    description="A simple API to greet users",
    version="1.0.0"
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GreetingRequest(BaseModel):
    """Request model for greeting endpoint."""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the user to greet")
    language: Optional[str] = Field("en", description="Language code (en, es, fr)")


class GreetingResponse(BaseModel):
    """Response model for greeting endpoint."""
    message: str = Field(..., description="Greeting message")
    name: str = Field(..., description="Name of the greeted user")
    language: str = Field(..., description="Language used for greeting")


# Greeting messages in different languages
GREETINGS = {
    "en": "Hello, {name}! Welcome to our application!",
    "es": "¡Hola, {name}! ¡Bienvenido a nuestra aplicación!",
    "fr": "Bonjour, {name}! Bienvenue dans notre application!",
    "de": "Hallo, {name}! Willkommen in unserer Anwendung!",
    "it": "Ciao, {name}! Benvenuto nella nostra applicazione!",
}


@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Greeting API",
        "version": "1.0.0",
        "endpoints": {
            "/api/greet": "POST - Greet a user",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "greeting-api"}


@app.post("/api/greet", response_model=GreetingResponse)
async def greet_user(request: GreetingRequest):
    """Greet a user in the specified language.
    
    Args:
        request: GreetingRequest containing user name and optional language
    
    Returns:
        GreetingResponse with personalized greeting message
    
    Raises:
        HTTPException: If language is not supported
    """
    try:
        # Validate language
        language = request.language.lower() if request.language else "en"
        
        if language not in GREETINGS:
            logger.warning(f"Unsupported language requested: {language}")
            raise HTTPException(
                status_code=400,
                detail=f"Language '{language}' is not supported. Available languages: {', '.join(GREETINGS.keys())}"
            )
        
        # Generate greeting message
        message = GREETINGS[language].format(name=request.name)
        
        logger.info(f"Greeting generated for {request.name} in {language}")
        
        return GreetingResponse(
            message=message,
            name=request.name,
            language=language
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating greeting: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)