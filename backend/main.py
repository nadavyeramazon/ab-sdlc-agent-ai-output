from fastapi import FastAPI

app = FastAPI()

@app.get("/greet")
async def greet():
    return {"message": "Hello, user!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)