# Hello World FastAPI Application

A simple Hello World API built with FastAPI, a modern, fast (high-performance) web framework for building APIs with Python.

## Features

- ✅ Simple Hello World endpoint
- ✅ Personalized greeting endpoint
- ✅ Health check endpoint
- ✅ Auto-generated interactive API documentation
- ✅ Fast and async by default

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
   cd ab-sdlc-agent-ai-backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Option 1: Using Python directly

```bash
python main.py
```

### Option 2: Using Uvicorn command

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-reload on code changes (useful for development).

## API Endpoints

Once the application is running, you can access the following endpoints:

### 1. Root Endpoint
- **URL**: `http://localhost:8000/`
- **Method**: GET
- **Response**: 
  ```json
  {"message": "Hello World!"}
  ```

### 2. Hello Endpoint
- **URL**: `http://localhost:8000/hello`
- **Method**: GET
- **Response**: 
  ```json
  {"message": "Hello from FastAPI!"}
  ```

### 3. Personalized Hello
- **URL**: `http://localhost:8000/hello/{name}`
- **Method**: GET
- **Example**: `http://localhost:8000/hello/John`
- **Response**: 
  ```json
  {"message": "Hello, John!"}
  ```

### 4. Health Check
- **URL**: `http://localhost:8000/health`
- **Method**: GET
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

These provide an interactive interface to explore and test all API endpoints.

## Testing the API

### Using curl

```bash
# Test root endpoint
curl http://localhost:8000/

# Test hello endpoint
curl http://localhost:8000/hello

# Test personalized greeting
curl http://localhost:8000/hello/World

# Test health check
curl http://localhost:8000/health
```

### Using Python requests

```python
import requests

# Test root endpoint
response = requests.get("http://localhost:8000/")
print(response.json())

# Test personalized greeting
response = requests.get("http://localhost:8000/hello/FastAPI")
print(response.json())
```

## Project Structure

```
ab-sdlc-agent-ai-backend/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .gitignore          # Git ignore file
└── LICENSE             # License file
```

## Development

### Adding New Endpoints

To add a new endpoint, simply add a new function with a route decorator:

```python
@app.get("/new-endpoint")
async def new_endpoint():
    return {"message": "This is a new endpoint"}
```

### Running Tests

To run tests (when implemented), use:

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

COPY . .

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

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
