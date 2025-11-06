from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Greeting Service", description="A simple greeting API")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GreetingRequest(BaseModel):
    name: str

class GreetingResponse(BaseModel):
    message: str
    name: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Greeting Service API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/greet", response_model=GreetingResponse)
async def greet_user(request: GreetingRequest):
    """Greet a user by their name"""
    greeting_message = f"Hello, {request.name}! Welcome to our green-themed application!"
    return GreetingResponse(message=greeting_message, name=request.name)

@app.get("/greet/{name}", response_model=GreetingResponse)
async def greet_user_get(name: str):
    """Greet a user by their name via GET request"""
    greeting_message = f"Hello, {name}! Welcome to our green-themed application!"
    return GreetingResponse(message=greeting_message, name=name)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
