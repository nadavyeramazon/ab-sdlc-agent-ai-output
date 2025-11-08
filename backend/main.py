"""FastAPI backend with user greeting endpoint."""
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
    description="A simple API to greet users with a blue-themed frontend",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
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
        HTTPException: If language is not supported
    """
    try:
        # Validate language
        language = request.language.lower()
        if language not in GREETINGS:
            raise HTTPException(
                status_code=400,
                detail=f"Language '{language}' not supported. Supported languages: {', '.join(GREETINGS.keys())}"
            )
        
        # Generate greeting message
        greeting = GREETINGS[language]
        message = f"{greeting}, {request.name}! Welcome to our blue-themed application! 💙"
        
        logger.info(f"Greeted user: {request.name} in {language}")
        
        return GreetResponse(
            message=message,
            name=request.name,
            language=language
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error greeting user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/howdy", response_model=HowdyResponse)
async def howdy_user(request: HowdyRequest):
    """Give a casual howdy greeting to a user.
    
    Args:
        request: HowdyRequest containing user's name and optional language
        
    Returns:
        HowdyResponse with personalized casual howdy greeting
        
    Raises:
        HTTPException: If language is not supported
    """
    try:
        # Validate language
        language = request.language.lower()
        if language not in HOWDY_GREETINGS:
            raise HTTPException(
                status_code=400,
                detail=f"Language '{language}' not supported. Supported languages: {', '.join(HOWDY_GREETINGS.keys())}"
            )
        
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
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in howdy greeting: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
