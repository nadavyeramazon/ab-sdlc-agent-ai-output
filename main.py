import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AB SDLC Agent AI Backend")

# CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    repo: str
    branch: str
    requirements: str

class GenerateResponse(BaseModel):
    status: str
    message: str
    files_changed: list[str] = []

@app.get("/")
def root():
    return {"status": "ok", "message": "AB SDLC Agent AI Backend"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """Generate code based on requirements"""
    
    # Validate inputs
    if not request.repo or not request.branch or not request.requirements:
        raise HTTPException(status_code=400, detail="repo, branch, and requirements are required")
    
    # Call LLM service (Claude via Bedrock or OpenAI)
    llm_url = os.getenv("LLM_SERVICE_URL", "http://localhost:8001/generate")
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                llm_url,
                json={
                    "repo": request.repo,
                    "branch": request.branch,
                    "requirements": request.requirements
                }
            )
            response.raise_for_status()
            data = response.json()
            
            return GenerateResponse(
                status="success",
                message=data.get("message", "Code generated successfully"),
                files_changed=data.get("files_changed", [])
            )
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"LLM service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)