# Hello World Service

A production-grade Hello World service implementing a RESTful API with comprehensive testing, logging, and error handling.

## Features

- FastAPI-based REST API
- Comprehensive error handling and validation
- Request/response logging middleware
- Configuration management
- Complete test suite
- Docker support

## Getting Started

### Prerequisites

- Python 3.13+
- pip

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Set environment variables (optional):
- `APP_NAME`: Service name (default: "Hello World Service")
- `DEBUG`: Enable debug mode (default: false)
- `LOG_LEVEL`: Logging level (default: INFO)
- `API_PREFIX`: API URL prefix (default: /api/v1)

### Running the Service

```bash
uvicorn src.app:app --reload
```

### Running Tests

```bash
pytest
```

### Docker

Build and run with Docker:

```bash
docker build -t hello-world-service .
docker run -p 8000:8000 hello-world-service
```

## API Endpoints

### POST /api/v1/hello
Generate a greeting message.

Request body:
```json
{
  "name": "string"  // optional, defaults to "World"
}
```

### GET /api/v1/stats
Get service statistics.

## Development

- Code style follows Google Python Style Guide
- Full test coverage required
- Type hints required