# Hello World FastAPI Application

A simple REST API built with FastAPI that demonstrates basic API functionality with hello world endpoints.

## Features

- 🚀 Fast and modern Python web framework (FastAPI)
- 📝 Automatic interactive API documentation
- ✅ Health check endpoint
- 👋 Multiple hello world endpoints including personalized greetings

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Using Python directly:
```bash
python main.py
```

### Using uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Root Endpoint
- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns a welcome message
- **Example Response**:
  ```json
  {
    "message": "Welcome to the Hello World API!",
    "status": "success"
  }
  ```

### Hello World
- **URL**: `/hello`
- **Method**: `GET`
- **Description**: Returns a hello world message
- **Example Response**:
  ```json
  {
    "message": "Hello, World!",
    "status": "success"
  }
  ```

### Personalized Hello
- **URL**: `/hello/{name}`
- **Method**: `GET`
- **Description**: Returns a personalized greeting
- **Parameters**: `name` (string) - The name to greet
- **Example**: `GET /hello/John`
- **Example Response**:
  ```json
  {
    "message": "Hello, John!",
    "name": "John",
    "status": "success"
  }
  ```

### Health Check
- **URL**: `/health`
- **Method**: `GET`
- **Description**: Check if the API is running
- **Example Response**:
  ```json
  {
    "status": "healthy",
    "service": "Hello World API"
  }
  ```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Testing the API

You can test the API using curl, Postman, or any HTTP client:

### Using curl:
```bash
# Test root endpoint
curl http://localhost:8000/

# Test hello world endpoint
curl http://localhost:8000/hello

# Test personalized greeting
curl http://localhost:8000/hello/YourName

# Test health check
curl http://localhost:8000/health
```

### Using Python requests:
```python
import requests

response = requests.get("http://localhost:8000/hello")
print(response.json())
```

## Project Structure

```
.
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── LICENSE             # License file
```

## Development

The application runs with auto-reload enabled by default, so any changes to the code will automatically restart the server.

## License

This project is licensed under the terms specified in the LICENSE file.
