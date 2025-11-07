# Hello World API - FastAPI

A simple Hello World API built with FastAPI Python framework.

## Features

- **Root Endpoint** (`/`): Returns a simple "Hello World" message
- **Health Check** (`/health`): Verifies the API is running
- **Personalized Greeting** (`/hello/{name}`): Returns a personalized greeting
- **API Info** (`/info`): Provides information about the API and available endpoints

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

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

### Method 1: Using Python directly

```bash
python main.py
```

### Method 2: Using Uvicorn

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Root Endpoint

**GET** `/`

Returns a simple Hello World message.

**Example:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "message": "Hello World!"
}
```

### 2. Health Check

**GET** `/health`

Verifies that the API is running and healthy.

**Example:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Service is up and running"
}
```

### 3. Personalized Greeting

**GET** `/hello/{name}`

Returns a personalized greeting message.

**Example:**
```bash
curl http://localhost:8000/hello/John
```

**Response:**
```json
{
  "message": "Hello, John!"
}
```

### 4. API Information

**GET** `/info`

Provides information about the API and its available endpoints.

**Example:**
```bash
curl http://localhost:8000/info
```

**Response:**
```json
{
  "name": "Hello World API",
  "version": "1.0.0",
  "description": "A simple FastAPI Hello World application",
  "endpoints": [
    "/",
    "/health",
    "/hello/{name}",
    "/info"
  ]
}
```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Project Structure

```
.
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── LICENSE             # License file
```

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs with Python
- **Uvicorn**: ASGI server implementation for running the application
- **Pydantic**: Data validation using Python type annotations

## Development

The application runs with auto-reload enabled in development mode, so changes to the code will automatically restart the server.

## License

See LICENSE file for details.
