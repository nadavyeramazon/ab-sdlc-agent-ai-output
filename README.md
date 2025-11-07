# Hello World FastAPI Application

A simple Hello World API built with FastAPI in Python.

## Description

This is a minimal FastAPI application that demonstrates basic API functionality with multiple endpoints for greeting users.

## Features

- **Root endpoint** (`/`): Returns a simple "Hello World!" message
- **Hello endpoint** (`/hello`): Returns a greeting from FastAPI
- **Personalized greeting** (`/hello/{name}`): Returns a personalized greeting with the provided name
- **Health check** (`/health`): Returns the health status of the API

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Method 1: Using Python directly
```bash
python main.py
```

### Method 2: Using Uvicorn command
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Root Endpoint
```
GET /
```
Returns: `{"message": "Hello World!"}`

### Hello Endpoint
```
GET /hello
```
Returns: `{"message": "Hello from FastAPI!"}`

### Personalized Hello
```
GET /hello/{name}
```
Example: `GET /hello/John`
Returns: `{"message": "Hello, John!"}`

### Health Check
```
GET /health
```
Returns: `{"status": "healthy", "message": "API is running"}`

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Testing the API

### Using cURL
```bash
# Test root endpoint
curl http://localhost:8000/

# Test hello endpoint
curl http://localhost:8000/hello

# Test personalized greeting
curl http://localhost:8000/hello/John

# Test health check
curl http://localhost:8000/health
```

### Using a Browser
Simply navigate to any of the endpoints in your web browser:
- http://localhost:8000/
- http://localhost:8000/hello
- http://localhost:8000/hello/YourName
- http://localhost:8000/health

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

See LICENSE file for details.
