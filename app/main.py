from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="Simple Hello World API",
    description="A basic FastAPI application with two endpoints",
    version="1.0.0"
)

@app.get("/", tags=["root"])
def root():
    return {
        "message": "Hello World",
        "description": "Welcome to the Simple Hello World API",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/info", tags=["info"])
def info():
    return {
        "app_name": "Simple Hello World API",
        "version": "1.0.0",
        "framework": "FastAPI",
        "author": "AI Agent"
    }
