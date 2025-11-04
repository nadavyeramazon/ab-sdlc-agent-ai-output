from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Minimal FastAPI Backend", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/hello")
async def hello():
    """Simple hello world endpoint"""
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}