# Hello World Service

A production-grade Hello World API service built with FastAPI.

## Features

- FastAPI-based REST API
- Comprehensive error handling
- Request logging middleware
- Configuration management
- Docker support
- Complete test suite

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `pytest`
4. Start server: `uvicorn src.app:app --reload`

## API Documentation

Once running, access the OpenAPI documentation at:
- http://localhost:8000/docs
- http://localhost:8000/redoc

## Docker

Build: `docker build -t hello-world-service .`
Run: `docker run -p 8000:8000 hello-world-service`