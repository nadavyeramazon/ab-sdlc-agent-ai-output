# Green Greeting Application

A full-stack web application with a beautiful green-themed UI that greets users by name. Built with FastAPI backend and vanilla JavaScript frontend, containerized with Docker.

## Features

- 🌿 Beautiful green-themed user interface
- ✅ Comprehensive input validation and sanitization
- 🔒 Secure CORS configuration
- 🧪 Full test coverage for backend and frontend
- 🐳 Docker containerization with health checks
- 📊 API proxy configuration for production deployments
- 🎨 Responsive design with smooth animations

## Architecture

- **Backend**: FastAPI (Python) - RESTful API with validation
- **Frontend**: Vanilla JavaScript with HTML/CSS
- **Reverse Proxy**: Nginx for serving static files and API proxying
- **Containerization**: Docker and Docker Compose

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development)
- Node.js (optional, for frontend testing)

### Running with Docker Compose

1. Clone the repository:
```bash
git clone <repository-url>
cd ab-sdlc-agent-ai-backend
```

2. Start the application:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Running Tests

#### Backend Tests

```bash
cd backend
pip install -r requirements.txt
pytest

# With coverage report
pytest --cov=. --cov-report=html
```

#### Frontend Tests

```bash
cd frontend
npm install
npm test

# With coverage
npm run test:coverage
```

## API Endpoints

### GET /
Returns welcome message and API version.

**Response:**
```json
{
  "message": "Welcome to the Greeting API",
  "version": "1.0.0"
}
```

### POST /greet
Greets a user by name with validation.

**Request:**
```json
{
  "name": "Alice"
}
```

**Response:**
```json
{
  "message": "Hello, Alice! Welcome to our green-themed application! 🌿"
}
```

**Validation Rules:**
- Name must be 1-100 characters
- Only alphanumeric characters, spaces, hyphens, and apostrophes allowed
- Leading/trailing whitespace is trimmed
- Empty or whitespace-only names are rejected

### GET /health
Health check endpoint for container orchestration.

**Response:**
```json
{
  "status": "healthy",
  "service": "greeting-api"
}
```

## Configuration

### Backend Environment Variables

- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins (default: `http://localhost:3000,http://localhost:8080`)
- `PYTHONUNBUFFERED`: Set to 1 for real-time logging

### Frontend Configuration

The frontend automatically detects the environment:
- **Local development**: Uses `http://localhost:8000` for API calls
- **Production/Docker**: Uses `/api` proxy path configured in nginx

## Security Features

1. **Input Validation**: Comprehensive validation with Pydantic models
2. **CORS Configuration**: Restricted to specific allowed origins
3. **Input Sanitization**: Prevents XSS and injection attacks
4. **Length Limits**: Prevents buffer overflow attacks
5. **Error Logging**: Detailed logging without exposing sensitive information

## Test Coverage

### Backend Tests
- ✅ Root endpoint functionality
- ✅ Greeting endpoint with valid inputs
- ✅ Input validation (empty, whitespace, length, special characters)
- ✅ Health check endpoint
- ✅ CORS configuration
- ✅ Error handling

### Frontend Tests
- ✅ API configuration for different environments
- ✅ Input validation logic
- ✅ Message display functions
- ✅ API call construction
- ✅ Error handling scenarios
- ✅ Form submission flow
- ✅ Response parsing

## Development

### Local Backend Development

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Local Frontend Development

Open `frontend/index.html` in a browser, or use a local server:

```bash
cd frontend
python -m http.server 8080
```

## Docker Health Checks

The backend container includes a Python-based health check that doesn't require curl:
- Checks every 30 seconds
- 10-second timeout
- 3 retries before marking unhealthy
- 40-second startup grace period

## Troubleshooting

### Backend not responding
- Check if the container is running: `docker ps`
- View logs: `docker-compose logs backend`
- Ensure port 8000 is not in use

### Frontend can't connect to backend
- Verify both containers are on the same network
- Check nginx configuration for API proxy
- Ensure CORS origins are properly configured

### Tests failing
- Ensure all dependencies are installed
- Check Python/Node.js versions
- Review test output for specific failures

## License

MIT License - see LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Support

For issues and questions, please open an issue on GitHub.
