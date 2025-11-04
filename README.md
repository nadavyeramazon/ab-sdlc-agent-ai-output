# Minimal FastAPI Backend

A minimal FastAPI backend service providing basic endpoints.

## Features

- ✅ FastAPI framework
- ✅ CORS middleware enabled
- ✅ Hello World endpoint
- ✅ Health check endpoint
- ✅ Unit tests with pytest
- ✅ GitHub Actions CI/CD

## Endpoints

### GET /api/hello
Returns a simple hello world message.

**Response:**
```json
{
  "message": "Hello World"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Running Tests

```bash
pytest -v
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc