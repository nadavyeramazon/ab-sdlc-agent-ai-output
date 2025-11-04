# Hello World FastAPI Application

A simple FastAPI backend application for a Hello World service.

## Features

- FastAPI backend with CORS middleware
- `/api/hello` endpoint returning a hello world message
- `/health` endpoint for health checks
- Comprehensive unit tests
- GitHub Actions CI/CD pipeline

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at:
- http://localhost:8000/api/hello
- http://localhost:8000/health
- http://localhost:8000/docs (Swagger UI)

## Running Tests

```bash
pytest -v
```

## API Endpoints

### GET /api/hello
Returns: `{"message": "Hello World"}`

### GET /health
Returns: `{"status": "healthy"}`
