"""FastAPI backend with user greeting endpoint."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Greeting API",
    description="A simple API to greet users with a blue-themed frontend",
    version="1.0.0"
)

# Configure CORS for frontend communication with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GreetRequest(BaseModel):
    """Request model for greeting."""
    name: str = Field(..., min_length=1, max_length=100, description="User's name")
    language: Optional[str] = Field("en", description="Language code (en, es, fr, de)")


class GreetResponse(BaseModel):
    """Response model for greeting."""
    message: str = Field(..., description="Greeting message")
    name: str = Field(..., description="User's name")
    language: str = Field(..., description="Language used")


class HowdyRequest(BaseModel):
    """Request model for howdy greeting."""
    name: str = Field(..., min_length=1, max_length=100, description="User's name")
    language: Optional[str] = Field("en", description="Language code (en, es, fr, de)")


class HowdyResponse(BaseModel):
    """Response model for howdy greeting."""
    message: str = Field(..., description="Howdy greeting message")
    name: str = Field(..., description="User's name")
    language: str = Field(..., description="Language used")
    greeting_type: str = Field(default="howdy", description="Type of greeting")


# Greeting messages in different languages
GREETINGS = {
    "en": "Hello",
    "es": "Hola",
    "fr": "Bonjour",
    "de": "Guten Tag",
}

# Casual howdy greetings in different languages
HOWDY_GREETINGS = {
    "en": "Howdy",
    "es": "Qué tal",
    "fr": "Salut",
    "de": "Moin",
}


def validate_language(language: str, greetings_dict: Dict[str, str]) -> str:
    """Validate that the language is supported.
    
    Args:
        language: Language code to validate
        greetings_dict: Dictionary of supported greetings
        
    Returns:
        Lowercase language code
        
    Raises:
        HTTPException: If language is not supported
    """
    language_lower = language.lower()
    if language_lower not in greetings_dict:
        raise HTTPException(
            status_code=400,
            detail=f"Language '{language}' not supported. Supported languages: {', '.join(greetings_dict.keys())}"
        )
    return language_lower


def handle_greeting_error(error: Exception, user_name: str, greeting_type: str = "greeting"):
    """Handle errors that occur during greeting operations.
    
    Args:
        error: The exception that was raised
        user_name: Name of the user being greeted
        greeting_type: Type of greeting (for logging)
        
    Raises:
        HTTPException: If not already an HTTPException, raises 500 error
    """
    if isinstance(error, HTTPException):
        raise
    logger.error(f"Error in {greeting_type} for user {user_name}: {str(error)}")
    raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to the Greeting API",
        "version": "1.0.0",
        "endpoints": {
            "greet": "/api/greet",
            "howdy": "/api/howdy",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "greeting-api"}


@app.post("/api/greet", response_model=GreetResponse)
async def greet_user(request: GreetRequest):
    """Greet a user by name.
    
    Args:
        request: GreetRequest containing user's name and optional language
        
    Returns:
        GreetResponse with personalized greeting message
        
    Raises:
        HTTPException: If language is not supported or internal error occurs
    """
    try:
        # Validate language using helper function
        language = validate_language(request.language, GREETINGS)
        
        # Generate greeting message
        greeting = GREETINGS[language]
        message = f"{greeting}, {request.name}! Welcome to our blue-themed application! 💙"
        
        logger.info(f"Greeted user: {request.name} in {language}")
        
        return GreetResponse(
            message=message,
            name=request.name,
            language=language
        )
    except Exception as e:
        handle_greeting_error(e, request.name, "greeting")


@app.post("/api/howdy", response_model=HowdyResponse)
async def howdy_user(request: HowdyRequest):
    """Give a casual howdy greeting to a user.
    
    Args:
        request: HowdyRequest containing user's name and optional language
        
    Returns:
        HowdyResponse with personalized casual howdy greeting
        
    Raises:
        HTTPException: If language is not supported or internal error occurs
    """
    try:
        # Validate language using helper function
        language = validate_language(request.language, HOWDY_GREETINGS)
        
        # Generate howdy greeting message
        howdy_greeting = HOWDY_GREETINGS[language]
        message = f"{howdy_greeting}, {request.name}! Hope you're having a great day! 🤠"
        
        logger.info(f"Howdy greeted user: {request.name} in {language}")
        
        return HowdyResponse(
            message=message,
            name=request.name,
            language=language,
            greeting_type="howdy"
        )
    except Exception as e:
        handle_greeting_error(e, request.name, "howdy greeting")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
