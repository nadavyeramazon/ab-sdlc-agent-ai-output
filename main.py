from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    # Added comment to trigger CI
    return {'message': 'Hello, World!'}