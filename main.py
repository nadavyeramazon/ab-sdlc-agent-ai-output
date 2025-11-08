from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hello, World!</title>
    </head>
    <body>
        <h1>Hello, World!</h1>
        <p>This is a simple UI integrated with FastAPI backend.</p>
    </body>
    </html>
    """

@app.get("/api/hello")
async def hello():
    return {"message": "Hello, World!"}