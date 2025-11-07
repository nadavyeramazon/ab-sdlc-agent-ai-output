# Hello World API - FastAPI

A simple Hello World API built with FastAPI.

## Features

- Simple Hello World endpoint
- Personalized greeting endpoint
- Health check endpoint
- Fast and async API powered by FastAPI
- Auto-generated interactive API documentation

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode

Run the application with auto-reload:

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

## API Endpoints

Once the application is running, you can access:

### Endpoints

- **GET /** - Root endpoint returning "Hello World!"
  ```
  curl http://localhost:8000/
  ```
  Response: `{"message": "Hello World!"}`

- **GET /hello** - Hello endpoint with structured greeting
  ```
  curl http://localhost:8000/hello
  ```
  Response: `{"greeting": "Hello", "target": "World"}`

- **GET /hello/{name}** - Personalized greeting endpoint
  ```
  curl http://localhost:8000/hello/John
  ```
  Response: `{"message": "Hello John!"}`

- **GET /health** - Health check endpoint
  ```
  curl http://localhost:8000/health
  ```
  Response: `{"status": "healthy", "service": "Hello World API"}`

### Interactive API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
.
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: Lightning-fast ASGI server
- **Pydantic**: Data validation using Python type annotations

## Development

### Testing the API

You can test the API using:

1. **curl** (command line):
   ```bash
   curl http://localhost:8000/
   ```

2. **Browser**: Navigate to http://localhost:8000/

3. **Interactive Docs**: Navigate to http://localhost:8000/docs

## License

See LICENSE file for details.
