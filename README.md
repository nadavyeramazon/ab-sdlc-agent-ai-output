# AB SDLC Agent AI Backend

A simple FastAPI application that provides a Hello World endpoint and health check functionality.

## Project Overview

This is a FastAPI-based backend service that demonstrates a basic REST API implementation with two endpoints:
- A root endpoint that returns a "Hello World" message
- A health check endpoint for monitoring service status

## Prerequisites

- Python 3.13 or higher
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
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Run

### Option 1: Run directly with Python
```bash
python main.py
```

### Option 2: Run with uvicorn (with auto-reload for development)
```bash
uvicorn main:app --reload
```

### Option 3: Run with Docker
```bash
docker build -t ab-sdlc-agent-ai-backend .
docker run -p 8000:8000 ab-sdlc-agent-ai-backend
```

The application will start on `http://localhost:8000`

## API Endpoints

### 1. Hello World Endpoint

**GET** `/`

Returns a simple Hello World message.

**Response:**
```json
{
  "message": "Hello World"
}
```

**Example:**
```bash
curl http://localhost:8000/
```

### 2. Health Check Endpoint

**GET** `/health`

Returns the health status of the service.

**Response:**
```json
{
  "status": "healthy"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

## API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

### Manual Testing

1. Start the application (see "How to Run" section)
2. Test the Hello World endpoint:
   ```bash
   curl http://localhost:8000/
   ```
   Expected output: `{"message":"Hello World"}`

3. Test the Health Check endpoint:
   ```bash
   curl http://localhost:8000/health
   ```
   Expected output: `{"status":"healthy"}`

## Project Structure

```
ab-sdlc-agent-ai-backend/
├── main.py              # Main application entry point
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
├── .gitignore          # Git ignore rules
├── Dockerfile          # Docker container configuration
├── .dockerignore       # Docker ignore rules
└── pyproject.toml      # Project metadata and configuration
```

## Technology Stack

- **Framework**: FastAPI 0.115.0
- **ASGI Server**: Uvicorn 0.30.0
- **Python Version**: 3.13+

## Deployment

This application is deployment-ready and can be deployed to:
- Cloud platforms (AWS, GCP, Azure)
- Container orchestration platforms (Kubernetes, Docker Swarm)
- Platform-as-a-Service providers (Heroku, Render, Railway)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
