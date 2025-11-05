# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Backend API",
        description="Backend API Service",
        version="1.0.0",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()


@app.get("/", tags=["General"])
async def root() -> dict[str, str]:
    """Root endpoint returning a welcome message."""
    return {"message": "Hello World from Backend"}


@app.get("/health", tags=["Health"])
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )