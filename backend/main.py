from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Hello World Backend API")

# Configure CORS to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Hello World from FastAPI Backend!"}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/api/hello")
async def hello():
    """Hello endpoint for frontend to call"""
    return {
        "message": "Hello from the backend!",
        "status": "success",
        "service": "FastAPI Backend"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
