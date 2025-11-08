"""FastAPI Backend Application for Greeting Users"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from typing import Optional
import uvicorn

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


class GreetRequest(BaseModel):
    """Request model for greeting endpoint"""
    name: str
    language: Optional[str] = "en"
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    @validator('language')
    def language_must_be_valid(cls, v):
        valid_languages = ['en', 'es', 'fr', 'de', 'it']
        if v not in valid_languages:
            raise ValueError(f'Language must be one of: {", ".join(valid_languages)}')
        return v


class GreetResponse(BaseModel):
    """Response model for greeting endpoint"""
    message: str
    name: str
    language: str


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to the Greeting API",
        "version": "1.0.0",
        "endpoints": {
            "/greet": "POST - Greet a user by name",
            "/health": "GET - Health check endpoint"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "greeting-api"}


@app.post("/greet", response_model=GreetResponse)
async def greet_user(request: GreetRequest):
    """Greet a user with a personalized message
    
    Args:
        request: GreetRequest containing name and optional language
        
    Returns:
        GreetResponse with personalized greeting message
    """
    # Greeting templates by language
    greetings = {
        "en": f"Hello, {request.name}! Welcome to our application!",
        "es": f"¡Hola, {request.name}! ¡Bienvenido a nuestra aplicación!",
        "fr": f"Bonjour, {request.name}! Bienvenue dans notre application!",
        "de": f"Hallo, {request.name}! Willkommen in unserer Anwendung!",
        "it": f"Ciao, {request.name}! Benvenuto nella nostra applicazione!"
    }
    
    message = greetings.get(request.language, greetings["en"])
    
    return GreetResponse(
        message=message,
        name=request.name,
        language=request.language
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
