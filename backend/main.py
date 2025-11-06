from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="Greeting API")

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GreetingRequest(BaseModel):
    name: str

class GreetingResponse(BaseModel):
    message: str

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to the Greeting API"}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/greet", response_model=GreetingResponse)
async def greet_user(request: GreetingRequest):
    """Greet user based on their name input"""
    if not request.name or request.name.strip() == "":
        greeting = "Hello! Please tell me your name."
    else:
        name = request.name.strip()
        greeting = f"Hello, {name}! Welcome to our green-themed greeting service. Have a wonderful day!"
    
    return GreetingResponse(message=greeting)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
