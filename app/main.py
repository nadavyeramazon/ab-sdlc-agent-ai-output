from fastapi import FastAPI
from app.routes import root

app = FastAPI()

# Include routes
app.include_router(root.router)