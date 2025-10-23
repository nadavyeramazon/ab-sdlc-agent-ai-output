# Hello World API

A production-ready Hello World API with enhanced features including type hints, OpenAPI documentation, rate limiting, and comprehensive test coverage.

## Features

- Type-hinted Python code
- OpenAPI documentation (available at `/api/docs` and `/api/redoc`)
- Rate limiting (5 requests per minute)
- Health check endpoint
- Version headers
- CORS support
- Comprehensive test coverage

## Installation

```bash
pip install -r requirements.txt
```

## Running the API

```bash
python src/main.py
```

The API will be available at http://localhost:8000

## Running Tests

```bash
pytest tests/
```

## API Endpoints

- GET `/`: Returns hello world message
- GET `/health`: Health check endpoint
- GET `/api/docs`: OpenAPI documentation
- GET `/api/redoc`: ReDoc documentation

## Headers

All responses include an `X-API-Version` header with the current API version.

## Rate Limiting

Endpoints are rate-limited to 5 requests per minute per IP address.
