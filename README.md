# FastAPI Hello World API

A simple Hello World API built with FastAPI Python framework.

## Description

This is a basic FastAPI application that demonstrates how to create a simple REST API with multiple endpoints. The API provides hello world functionality with both generic and personalized greetings.

## Features

- ✨ Simple and clean FastAPI implementation
- 🚀 Multiple endpoints for different use cases
- 📝 Comprehensive documentation with OpenAPI/Swagger UI
- 🏥 Health check endpoint
- 🔄 Hot reload support for development

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
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

Run the application with hot reload:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Root Endpoint
- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns a welcome message with API information
- **Response**:
```json
{
  "message": "Hello World!",
  "status": "success",
  "api": "FastAPI Hello World"
}
```

### Hello Endpoint
- **URL**: `/hello`
- **Method**: `GET`
- **Description**: Returns a simple hello world message
- **Response**:
```json
{
  "message": "Hello World!"
}
```

### Personalized Hello Endpoint
- **URL**: `/hello/{name}`
- **Method**: `GET`
- **Description**: Returns a personalized greeting
- **Parameters**:
  - `name` (path parameter): The name to greet
- **Example**: `/hello/John`
- **Response**:
```json
{
  "message": "Hello John!",
  "name": "John"
}
```

### Health Check Endpoint
- **URL**: `/health`
- **Method**: `GET`
- **Description**: Returns the health status of the API
- **Response**:
```json
{
  "status": "healthy",
  "service": "Hello World API"
}
```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing the API

You can test the API using various methods:

### Using cURL

```bash
# Test root endpoint
curl http://localhost:8000/

# Test hello endpoint
curl http://localhost:8000/hello

# Test personalized hello
curl http://localhost:8000/hello/YourName

# Test health check
curl http://localhost:8000/health
```

### Using Python requests

```python
import requests

response = requests.get("http://localhost:8000/")
print(response.json())
```

### Using Browser

Simply open your browser and navigate to:
- http://localhost:8000/
- http://localhost:8000/hello
- http://localhost:8000/hello/YourName
- http://localhost:8000/health

## Project Structure

```
ab-sdlc-agent-ai-backend/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── LICENSE             # License file
```

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running the application
- **Pydantic**: Data validation using Python type annotations

## Error Handling

The API includes basic error handling. FastAPI automatically:
- Validates request parameters
- Returns appropriate HTTP status codes
- Provides detailed error messages in responses

## Development

### Code Quality

The code follows Python best practices:
- Type hints for better code clarity
- Docstrings for all functions
- Clean and readable code structure
- Async/await for better performance

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue in the repository.
