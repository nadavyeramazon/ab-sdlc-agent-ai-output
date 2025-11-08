"""FastAPI Backend Application with Greeting and Howdy APIs."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn

app = FastAPI(
    title="Greeting and Howdy API",
    description="A simple API to greet users with multiple greeting styles",
    version="1.1.0"
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

class HowdyRequest(BaseModel):
    """Request model for howdy endpoint."""
    name: str = Field(..., min_length=1, description="Name must not be empty")
    language: Optional[str] = "en"
    style: Optional[str] = "casual"  # casual, formal, friendly

class HowdyResponse(BaseModel):
    """Response model for howdy endpoint."""
    message: str
    name: str
    language: str
    style: str

# Greeting templates in different languages
GREETINGS = {
    "en": "Hello, {name}! Welcome to our blue-themed application!",
    "es": "¡Hola, {name}! ¡Bienvenido a nuestra aplicación con tema azul!",
    "fr": "Bonjour, {name}! Bienvenue dans notre application au thème bleu!",
    "de": "Hallo, {name}! Willkommen in unserer blau gestalteten Anwendung!",
    "it": "Ciao, {name}! Benvenuto nella nostra applicazione a tema blu!",
}

# Howdy templates in different languages and styles
HOWDY_TEMPLATES = {
    "en": {
        "casual": "Howdy, {name}! Great to see ya!",
        "formal": "Howdy, {name}. It's a pleasure to make your acquaintance.",
        "friendly": "Howdy there, {name}! Hope you're having a wonderful day!"
    },
    "es": {
        "casual": "¡Qué tal, {name}! ¡Qué gusto verte!",
        "formal": "Buenas, {name}. Es un placer conocerle.",
        "friendly": "¡Hola, {name}! ¡Espero que tengas un día maravilloso!"
    },
    "fr": {
        "casual": "Salut, {name}! Content de te voir!",
        "formal": "Bonjour, {name}. C'est un plaisir de faire votre connaissance.",
        "friendly": "Coucou, {name}! J'espère que tu passes une merveilleuse journée!"
    },
    "de": {
        "casual": "Servus, {name}! Schön dich zu sehen!",
        "formal": "Guten Tag, {name}. Es ist mir eine Freude, Sie kennenzulernen.",
        "friendly": "Hallo, {name}! Ich hoffe, du hast einen wunderbaren Tag!"
    },
    "it": {
        "casual": "Ciao, {name}! Che piacere vederti!",
        "formal": "Buongiorno, {name}. È un piacere conoscerla.",
        "friendly": "Ehi, {name}! Spero che tu stia passando una giornata meravigliosa!"
    }
}

@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "status": "healthy",
        "message": "Greeting and Howdy API is running",
        "version": "1.1.0"
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

@app.post("/api/howdy", response_model=HowdyResponse)
async def howdy_user(request: HowdyRequest):
    """Greet a user with a howdy-style message.
    
    This endpoint provides a more casual, Western-style greeting with different
    style options (casual, formal, friendly) and multi-language support.
    
    Args:
        request: HowdyRequest containing name, optional language, and optional style
        
    Returns:
        HowdyResponse with personalized howdy message
    """
    language = request.language.lower() if request.language else "en"
    style = request.style.lower() if request.style else "casual"
    
    # Default to English if language not supported
    if language not in HOWDY_TEMPLATES:
        language = "en"
    
    # Default to casual if style not supported
    if style not in ["casual", "formal", "friendly"]:
        style = "casual"
    
    howdy_template = HOWDY_TEMPLATES[language][style]
    message = howdy_template.format(name=request.name)
    
    return HowdyResponse(
        message=message,
        name=request.name,
        language=language,
        style=style
    )

@app.get("/api/languages")
async def get_supported_languages():
    """Get list of supported languages.
    
    Returns:
        List of supported language codes for both greeting and howdy endpoints
    """
    return {
        "languages": list(GREETINGS.keys()),
        "count": len(GREETINGS)
    }

@app.get("/api/howdy/styles")
async def get_howdy_styles():
    """Get list of supported howdy styles.
    
    Returns:
        List of supported style options for howdy endpoint
    """
    return {
        "styles": ["casual", "formal", "friendly"],
        "count": 3,
        "description": {
            "casual": "Relaxed and informal greeting",
            "formal": "Professional and polite greeting",
            "friendly": "Warm and enthusiastic greeting"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)