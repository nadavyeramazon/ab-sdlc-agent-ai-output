# FastAPI Hello World API

A simple Hello World REST API built with FastAPI framework in Python.

## Features

- 🚀 Fast and modern API built with FastAPI
- 👋 Multiple greeting endpoints
- 🌍 Multi-language support
- 📚 Auto-generated interactive API documentation
- ✅ Health check endpoint
- 🔄 Path and query parameter support
- 📝 Request body validation with Pydantic
- 🎨 Clean and well-documented code

## Requirements

- Python 3.7 or higher
- FastAPI
- Uvicorn (ASGI server)
- Pydantic

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

2. Switch to the feature branch:
```bash
git checkout feature/test-18
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the API

Start the development server:
```bash
python3 app.py
```

Or use uvicorn directly:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Root Endpoint
**GET** `/`

Returns a basic Hello World message.

```bash
curl http://localhost:8000/
```

Response:
```json
{
  "message": "Hello World!",
  "status": "success",
  "api": "FastAPI Hello World API"
}
```

### 2. Health Check
**GET** `/health`

Check if the API is running.

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "message": "API is running smoothly"
}
```

### 3. Greet User by Name
**GET** `/hello/{name}`

Greet a specific user.

```bash
curl http://localhost:8000/hello/Alice
```

Response:
```json
{
  "message": "Hello, Alice!",
  "name": "Alice"
}
```

### 4. Customizable Greeting (Query Parameters)
**GET** `/greet?name=John&greeting=Hi`

Customize both the greeting and name.

```bash
curl "http://localhost:8000/greet?name=John&greeting=Hi"
```

Response:
```json
{
  "message": "Hi, John!",
  "greeting": "Hi",
  "name": "John"
}
```

### 5. Multi-language Greeting (POST)
**POST** `/greet`

Create greetings in different languages.

```bash
curl -X POST http://localhost:8000/greet \
  -H "Content-Type: application/json" \
  -d '{"name": "Maria", "language": "es"}'
```

Response:
```json
{
  "message": "Hola, Maria!",
  "name": "Maria",
  "language": "es",
  "greeting": "Hola"
}
```

Supported languages:
- `en` - English (Hello)
- `es` - Spanish (Hola)
- `fr` - French (Bonjour)
- `de` - German (Hallo)
- `it` - Italian (Ciao)
- `pt` - Portuguese (Olá)
- `ru` - Russian (Привет)
- `ja` - Japanese (こんにちは)
- `zh` - Chinese (你好)

### 6. API Information
**GET** `/info`

Get information about the API and available endpoints.

```bash
curl http://localhost:8000/info
```

## Code Structure

```
ab-sdlc-agent-ai-backend/
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── LICENSE            # License file
└── .gitignore         # Git ignore rules
```

## Development

### Running in Development Mode

The application includes auto-reload enabled by default, so any changes to the code will automatically restart the server.

### Testing with curl

Test all endpoints:

```bash
# Root endpoint
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health

# Greet by name
curl http://localhost:8000/hello/Alice

# Custom greeting with query params
curl "http://localhost:8000/greet?name=Bob&greeting=Hey"

# Multi-language greeting
curl -X POST http://localhost:8000/greet \
  -H "Content-Type: application/json" \
  -d '{"name": "Pierre", "language": "fr"}'

# API info
curl http://localhost:8000/info
```

### Testing with Python requests

```python
import requests

# GET request
response = requests.get("http://localhost:8000/")
print(response.json())

# POST request
response = requests.post(
    "http://localhost:8000/greet",
    json={"name": "Alice", "language": "es"}
)
print(response.json())
```

## Features of FastAPI

This simple API demonstrates several key features of FastAPI:

1. **Fast Performance**: Built on Starlette and Pydantic for high performance
2. **Type Hints**: Full Python type hints for better IDE support
3. **Automatic Documentation**: Swagger UI and ReDoc generated automatically
4. **Data Validation**: Automatic request validation with Pydantic
5. **Async Support**: Native async/await support for concurrent requests
6. **Standards-based**: Based on OpenAPI and JSON Schema

## Error Handling

The API includes automatic error handling:
- 422 Validation Error: When request data doesn't match expected schema
- 404 Not Found: When accessing non-existent endpoints

## License

See the LICENSE file in the repository root.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created as a simple demonstration of FastAPI framework for building REST APIs in Python.
