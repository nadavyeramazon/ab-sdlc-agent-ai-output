"""FastAPI Backend Application with Greeting API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn

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
    name: str = Field(..., min_length=1, description="Name must not be empty")
    language: Optional[str] = "en"

class GreetingResponse(BaseModel):
    """Response model for greeting endpoint."""
    message: str
    name: str
    language: str

# Greeting templates in different languages
GREETINGS = {
    "en": "Hello, {name}! Welcome to our green-themed application!",
    "es": "¡Hola, {name}! ¡Bienvenido a nuestra aplicación con tema verde!",
    "fr": "Bonjour, {name}! Bienvenue dans notre application au thème vert!",
    "de": "Hallo, {name}! Willkommen in unserer grün gestalteten Anwendung!",
    "it": "Ciao, {name}! Benvenuto nella nostra applicazione a tema verde!",
}

@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "status": "healthy",
        "message": "Greeting API is running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/api/greet", response_model=GreetingResponse)
async def greet_user(request: GreetingRequest):
    """Greet a user with a personalized message.
    
    Args:
        request: GreetingRequest containing name and optional language
        
    Returns:
        GreetingResponse with personalized greeting message
    """
    language = request.language.lower() if request.language else "en"
    
    # Default to English if language not supported
    if language not in GREETINGS:
        language = "en"
    
    greeting_template = GREETINGS[language]
    message = greeting_template.format(name=request.name)
    
    return GreetingResponse(
        message=message,
        name=request.name,
        language=language
    )

@app.get("/api/languages")
async def get_supported_languages():
    """Get list of supported languages.
    
    Returns:
        List of supported language codes
    """
    return {
        "languages": list(GREETINGS.keys()),
        "count": len(GREETINGS)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)