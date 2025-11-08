from fastapi import FastAPI

app = FastAPI()

@app.get("/")
defsgr root():
    return {"message": "Hello World"}
