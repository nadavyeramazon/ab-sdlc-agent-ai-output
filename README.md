# Microservices Application

A simple microservices application demonstrating communication between a FastAPI backend and an Express.js frontend using Docker Compose.

## Architecture

This application consists of two microservices:

- **Backend**: FastAPI Python application running on port 8000
- **Frontend**: Express.js application with a green-themed UI running on port 3000

## Features

✅ **FastAPI Backend**
- RESTful API endpoints
- Health check endpoint
- CORS configuration with environment variable support
- Structured logging
- Comprehensive test coverage

✅ **Express Frontend**
- Green-themed user interface
- Backend communication via REST API
- Health check endpoint
- Structured logging
- Comprehensive test coverage

✅ **Docker Compose**
- Orchestrates both services
- Networking between containers
- Health checks for both services
- Auto-restart policies

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd ab-sdlc-agent-ai-backend
```

2. Start the services:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend API Docs: http://localhost:8000/docs

### Local Development

#### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the backend:
```bash
python main.py
```

4. Run tests:
```bash
pytest
# With coverage:
pytest --cov=main --cov-report=html
```

#### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the frontend:
```bash
npm start
# For development with auto-reload:
npm run dev
```

4. Run tests:
```bash
npm test
# With coverage:
npm run test:coverage
```

## API Endpoints

### Backend (Port 8000)

- `GET /` - Root endpoint with welcome message
- `GET /health` - Health check endpoint
- `GET /api/hello` - API endpoint that returns greeting message
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /openapi.json` - OpenAPI schema

### Frontend (Port 3000)

- `GET /` - Main application page
- `GET /health` - Health check endpoint
- `GET /api/message` - Endpoint that communicates with backend

## Environment Variables

### Backend

- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins (default: `*`)
- `LOG_LEVEL`: Logging level - DEBUG, INFO, WARNING, ERROR (default: `INFO`)

### Frontend

- `PORT`: Server port (default: `3000`)
- `BACKEND_URL`: Backend service URL (default: `http://backend:8000`)
- `NODE_ENV`: Environment mode (default: `development`)

## Testing

### Backend Tests

The backend includes comprehensive unit tests covering:
- All API endpoints (root, health, api/hello)
- CORS configuration
- Error handling
- OpenAPI documentation

Run tests:
```bash
cd backend
pytest -v
```

Run with coverage:
```bash
pytest --cov=main --cov-report=html
```

### Frontend Tests

The frontend includes comprehensive unit tests covering:
- All server endpoints
- Backend communication
- Error handling
- Environment configuration

Run tests:
```bash
cd frontend
npm test
```

Run with coverage:
```bash
npm run test:coverage
```

## Health Checks

Both services include health check endpoints and Docker health checks:

- Backend health check: Uses Python's built-in urllib to avoid dependency on curl
- Frontend health check: Uses Node.js http module to avoid dependency on wget

## Production Considerations

1. **CORS Configuration**: Update `ALLOWED_ORIGINS` in docker-compose.yml to restrict origins in production
2. **Logging**: Set appropriate `LOG_LEVEL` for production (INFO or WARNING)
3. **Secrets Management**: Use Docker secrets or environment files for sensitive data
4. **Resource Limits**: Add resource limits in docker-compose.yml for production deployments
5. **Monitoring**: Integrate with monitoring solutions using the health check endpoints

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── test_main.py         # Backend unit tests
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Backend container configuration
│   ├── pytest.ini          # Pytest configuration
│   └── .coveragerc         # Coverage configuration
├── frontend/
│   ├── server.js           # Express server
│   ├── package.json        # Node.js dependencies
│   ├── Dockerfile          # Frontend container configuration
│   ├── test/
│   │   └── server.test.js  # Frontend unit tests
│   └── public/
│       ├── index.html      # Main HTML page
│       ├── styles.css      # Green-themed styles
│       └── app.js          # Frontend JavaScript
├── docker-compose.yml      # Service orchestration
└── README.md              # This file
```

## Troubleshooting

### Services won't start

1. Ensure Docker and Docker Compose are installed and running
2. Check if ports 3000 and 8000 are available
3. View logs: `docker-compose logs`

### Frontend can't reach backend

1. Verify both services are running: `docker-compose ps`
2. Check service logs: `docker-compose logs backend` and `docker-compose logs frontend`
3. Ensure services are on the same network (app-network)

### Tests failing

1. Ensure all dependencies are installed
2. Check that you're in the correct directory (backend/ or frontend/)
3. For frontend tests, ensure NODE_ENV is not set to 'production'

## License

MIT License - see LICENSE file for details
