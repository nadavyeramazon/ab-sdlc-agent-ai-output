from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Hello from Green Themed Backend'}

@app.get('/healthz')
def healthz():
    return {'status': 'ok'}