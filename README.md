# Hello World API with FastAPI

A simple Hello World REST API built with FastAPI and Python.

## Overview

This project implements a basic REST API with multiple endpoints including:
- Root endpoint returning "Hello World"
- Health check endpoint
- Personalized greeting endpoint
- API information endpoint

## Features

- ✅ Fast and modern Python web framework (FastAPI)
- ✅ Automatic interactive API documentation (Swagger UI)
- ✅ Type hints and validation with Pydantic
- ✅ Asynchronous request handling
- ✅ Production-ready with uvicorn ASGI server

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode

Run the application with auto-reload enabled:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### 1. Root Endpoint
- **URL**: `/`
- **Method**: GET
- **Description**: Returns a simple Hello World message
- **Response**:
  ```json
  {
    "message": "Hello World!"
  }
  ```

### 2. Health Check
- **URL**: `/health`
- **Method**: GET
- **Description**: Check if the API is running
- **Response**:
  ```json
  {
    "status": "healthy"
  }
  ```

### 3. Personalized Greeting
- **URL**: `/hello/{name}`
- **Method**: GET
- **Description**: Returns a personalized greeting
- **Parameters**:
  - `name` (path parameter): The name to greet
- **Example**: `/hello/John`
- **Response**:
  ```json
  {
    "message": "Hello John!"
  }
  ```

### 4. API Information
- **URL**: `/api/info`
- **Method**: GET
- **Description**: Returns API metadata
- **Response**:
  ```json
  {
    "name": "Hello World API",
    "version": "1.0.0",
    "description": "A simple Hello World API built with FastAPI",
    "framework": "FastAPI"
  }
  ```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Testing the API

### Using cURL

```bash
# Test root endpoint
curl http://localhost:8000/

# Test health check
curl http://localhost:8000/health

# Test personalized greeting
curl http://localhost:8000/hello/Alice

# Test API info
curl http://localhost:8000/api/info
```

### Using Python requests

```python
import requests

response = requests.get("http://localhost:8000/")
print(response.json())
```

### Using httpie

```bash
http GET http://localhost:8000/
```

## Project Structure

```
.
├── main.py              # FastAPI application with endpoints
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Code Quality

- **Type Hints**: Full type annotations for better IDE support and error detection
- **Documentation**: Comprehensive docstrings for all functions
- **Error Handling**: Built-in FastAPI error handling
- **Async/Await**: Asynchronous endpoints for better performance

## Running Tests

```bash
pytest
```

## Deployment

### Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t hello-world-api .
docker run -p 8000:8000 hello-world-api
```

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: Lightning-fast ASGI server
- **Pydantic**: Data validation using Python type annotations
- **Python 3.8+**: Programming language

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue in the GitHub repository.
