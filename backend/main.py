from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Greeting API")

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

@app.get("/")
def read_root():
    return {"message": "Welcome to the Greeting API!"}

@app.post("/greet", response_model=GreetingResponse)
def greet_user(request: GreetingRequest):
    """Greet a user by their name"""
    greeting = f"Hello, {request.name}! Welcome to our green-themed application!"
    return GreetingResponse(message=greeting)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
