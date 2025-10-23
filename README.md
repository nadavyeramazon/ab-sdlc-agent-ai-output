# Hello World API

A simple Hello World API with rate limiting, request tracking, and comprehensive testing.

## Features

- Hello World endpoint with rate limiting
- Health check endpoint
- Request ID tracking
- CORS support
- Comprehensive test coverage

## Configuration

The API can be configured using environment variables:

- `API_RATE_LIMIT_REQUESTS`: Number of requests allowed per time window (default: 5)
- `API_RATE_LIMIT_WINDOW`: Time window in seconds for rate limiting (default: 60)

Copy `.env.example` to `.env` and adjust the values as needed.

## Installation

```bash
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn src.main:app --reload
```

## Running Tests

```bash
pytest tests/
```

## API Documentation

Once running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

- `GET /`: Hello World message
- `GET /health`: Health check status

## Response Headers

- `X-Request-ID`: Unique identifier for each request
- `X-RateLimit-Limit`: Maximum requests allowed in the time window
- `X-RateLimit-Remaining`: Remaining requests in the current window
- `X-RateLimit-Reset`: Time when the rate limit window resets
