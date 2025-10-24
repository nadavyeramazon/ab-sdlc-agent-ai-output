# ab-sdlc-agent-ai-backend

A simple FastAPI "Hello World" service that serves as the backend for the AB SDLC Agent AI system.

## Features

- **FastAPI Framework**: Modern, fast (high-performance) web framework for building APIs
- **Health Check Endpoint**: Monitor service health
- **Hello World Endpoint**: Simple greeting endpoint
- **Service Info Endpoint**: Get service metadata and version
- **Docker Support**: Containerized deployment with multi-stage builds
- **Auto-generated API Documentation**: Interactive Swagger UI and ReDoc
- **CORS Enabled**: Cross-Origin Resource Sharing configured
- **Comprehensive Tests**: Full test coverage with pytest

## Prerequisites

- Python 3.13+
- Docker (optional, for containerized deployment)

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

2. Create a virtual environment:
```bash
python3.13 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Local Development

Run the application using uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The service will be available at `http://localhost:8000`

### Using Docker

1. Build the Docker image:
```bash
docker build -t ab-sdlc-agent-ai-backend .
```

2. Run the container:
```bash
docker run -p 8000:8000 ab-sdlc-agent-ai-backend
```

The service will be available at `http://localhost:8000`

## API Endpoints

### GET /
Returns service information including name, version, and status.

**Response:**
```json
{
  "service": "ab-sdlc-agent-ai-backend",
  "version": "1.0.0",
  "status": "running"
}
```

### GET /health
Health check endpoint for monitoring service availability.

**Response:**
```json
{
  "status": "healthy"
}
```

### GET /hello
Simple greeting endpoint that returns "Hello, World!".

**Response:**
```json
{
  "message": "Hello, World!"
}
```

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## Testing

This project includes comprehensive unit tests covering all endpoints, error cases, and edge cases.

### Running Tests

1. Install testing dependencies (if not already installed):
```bash
pip install -r requirements.txt
```

2. Run all tests:
```bash
pytest
```

3. Run tests with verbose output:
```bash
pytest -v
```

4. Run tests with coverage report:
```bash
pytest --cov=main --cov-report=html
```

5. Run specific test classes:
```bash
pytest test_main.py::TestHealthEndpoint -v
pytest test_main.py::TestHelloEndpoint -v
pytest test_main.py::TestErrorHandling -v
```

### Test Coverage

The test suite includes:

- **Endpoint Tests**: All API endpoints (/health, /hello, /)
- **Response Structure Tests**: Validates JSON response format
- **Error Handling Tests**: 404, 405 status codes
- **CORS Tests**: Cross-origin request handling
- **API Documentation Tests**: OpenAPI, Swagger UI, ReDoc
- **Concurrent Request Tests**: Async behavior validation
- **HTTP Method Tests**: GET, POST, PUT, DELETE behavior

### Continuous Integration

Tests should be run automatically in CI/CD pipelines before deployment:
```bash
# Example CI command
pytest --cov=main --cov-report=term-missing --cov-fail-under=80
```

## Development

### Project Structure

```
ab-sdlc-agent-ai-backend/
├── main.py              # FastAPI application entry point
├── test_main.py         # Comprehensive unit tests
├── requirements.txt     # Python dependencies (including test deps)
├── Dockerfile          # Docker image definition
├── .dockerignore       # Docker build exclusions
├── .gitignore          # Git exclusions
├── pyproject.toml      # Python project configuration
└── README.md           # This file
```

### Adding New Features

1. Add your endpoint in `main.py`
2. Write corresponding tests in `test_main.py`
3. Run tests to ensure everything works: `pytest -v`
4. Update this README with new endpoint documentation

## Environment Variables

Currently, the application doesn't require any environment variables. Future versions may include:

- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)
- `LOG_LEVEL`: Logging level (default: info)

## Performance

- **Async Support**: All endpoints use async handlers for optimal performance
- **Lightweight**: Minimal dependencies for fast startup
- **Production Ready**: Uses uvicorn with uvloop for high performance

## License

This project is part of the AB SDLC Agent AI system.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `pytest`
6. Submit a pull request

## Support

For issues and questions, please open an issue in the GitHub repository.
