# Backend - FastAPI Hello World

A simple FastAPI backend application that provides a hello world API.

## Endpoints

- `GET /` - Root endpoint with hello world message
- `GET /api/hello` - API endpoint for frontend communication
- `GET /health` - Health check endpoint

## Running Locally

```bash
pip install -r requirements.txt
python main.py
```

The API will be available at http://localhost:8000

## Running with Docker

```bash
docker build -t backend .
docker run -p 8000:8000 backend
```
