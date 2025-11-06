from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="Greeter API", description="A simple API to greet users")

# Enable CORS to allow frontend communication
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
    return {"message": "Greeter API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/greet", response_model=GreetingResponse)
async def greet_user(request: GreetingRequest):
    """
    Greet a user by their name
    """
    if not request.name or not request.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    greeting_message = f"Hello, {request.name.strip()}! Welcome to our green-themed application! 🌿"
    return GreetingResponse(message=greeting_message)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)