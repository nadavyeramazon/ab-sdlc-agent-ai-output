from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Greeting User API",
    description="A simple API to greet users with personalized messages",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GreetingRequest(BaseModel):
    """Request model for greeting endpoint"""
    name: str = Field(..., min_length=1, max_length=100, description="User's name")
    language: Optional[str] = Field("en", description="Language code (en, es, fr, de)")


class GreetingResponse(BaseModel):
    """Response model for greeting endpoint"""
    message: str
    name: str
    language: str


# Greeting messages in different languages
GREETINGS = {
    "en": "Hello, {name}! Welcome to our application!",
    "es": "¡Hola, {name}! ¡Bienvenido a nuestra aplicación!",
    "fr": "Bonjour, {name}! Bienvenue dans notre application!",
    "de": "Hallo, {name}! Willkommen in unserer Anwendung!"
}


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Greeting User API",
        "version": "1.0.0",
        "endpoints": {
            "/greet": "POST - Greet a user",
            "/greet/{name}": "GET - Greet a user by name",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "greeting-api"}


@app.post("/greet", response_model=GreetingResponse)
async def greet_user(request: GreetingRequest):
    """
    Greet a user with a personalized message.
    
    Args:
        request: GreetingRequest containing name and optional language
    
    Returns:
        GreetingResponse with personalized greeting message
    
    Raises:
        HTTPException: If language is not supported
    """
    language = request.language.lower() if request.language else "en"
    
    if language not in GREETINGS:
        logger.warning(f"Unsupported language requested: {language}")
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {language}. Supported languages: {', '.join(GREETINGS.keys())}"
        )
    
    message = GREETINGS[language].format(name=request.name)
    logger.info(f"Greeting generated for {request.name} in {language}")
    
    return GreetingResponse(
        message=message,
        name=request.name,
        language=language
    )


@app.get("/greet/{name}", response_model=GreetingResponse)
async def greet_user_by_name(name: str, language: Optional[str] = "en"):
    """
    Greet a user by name via GET request.
    
    Args:
        name: User's name from path parameter
        language: Optional language code (query parameter)
    
    Returns:
        GreetingResponse with personalized greeting message
    
    Raises:
        HTTPException: If name is empty or language is not supported
    """
    if not name or len(name.strip()) == 0:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    if len(name) > 100:
        raise HTTPException(status_code=400, detail="Name is too long (max 100 characters)")
    
    language = language.lower() if language else "en"
    
    if language not in GREETINGS:
        logger.warning(f"Unsupported language requested: {language}")
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {language}. Supported languages: {', '.join(GREETINGS.keys())}"
        )
    
    message = GREETINGS[language].format(name=name)
    logger.info(f"Greeting generated for {name} in {language}")
    
    return GreetingResponse(
        message=message,
        name=name,
        language=language
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
