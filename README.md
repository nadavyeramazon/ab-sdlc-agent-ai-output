# FastAPI Backend Application

A minimal FastAPI backend application with CORS support and automated testing.

## Installation

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

- `GET /api/hello` - Returns a hello world message

## Running Tests

```bash
pytest test_app.py -v
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
