import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="ab-sdlc-agent-ai-backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str
    context: str = ""

class GenerateResponse(BaseModel):
    result: str
    status: str = "success"

@app.get("/")
def root():
    return {"status": "ok", "service": "ab-sdlc-agent-ai-backend"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    
    # Minimal AI response - replace with actual AI integration when ready
    result = f"Generated response for: {request.prompt}"
    if request.context:
        result += f" (with context: {request.context[:50]}...)"
    
    return GenerateResponse(result=result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))