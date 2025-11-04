from fastapi import APIRouter
from app.api.routes import hello, health

api_router = APIRouter()

# Include route modules
api_router.include_router(
    hello.router,
    prefix="/hello",
    tags=["Hello"]
)

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"]
)