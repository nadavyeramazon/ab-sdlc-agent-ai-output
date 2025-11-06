from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Greeting API", version="1.0.0")

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
def read_root():
    """Root endpoint"""
    return {"message": "Welcome to the Greeting API"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/greet", response_model=GreetingResponse)
def greet_user(request: GreetingRequest):
    """Greet a user by their name"""
    greeting_message = f"Hello, {request.name}! Welcome to our green-themed application!"
    return GreetingResponse(message=greeting_message, name=request.name)

@app.get("/greet/{name}", response_model=GreetingResponse)
def greet_user_get(name: str):
    """Greet a user by their name via GET request"""
    greeting_message = f"Hello, {name}! Welcome to our green-themed application!"
    return GreetingResponse(message=greeting_message, name=name)
