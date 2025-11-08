# 🌿 Greeting Application - Full Stack Implementation

[![CI Pipeline](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready full-stack web application that greets users in multiple languages with a beautiful green-themed interface, comprehensive testing, and automated CI/CD.

## 🚀 Features

### Backend (FastAPI)
- ✅ **RESTful API** with comprehensive validation
- ✅ **Multi-language Support**: English, Spanish, French, German, and Italian
- ✅ **Request Logging** for monitoring and debugging
- ✅ **Error Handling** with custom exception handlers
- ✅ **Input Validation** with Pydantic models
- ✅ **CORS Support** for cross-origin requests
- ✅ **Health Check Endpoints** for monitoring
- ✅ **OpenAPI Documentation** (Swagger UI)

### Frontend (Vanilla JavaScript)
- ✅ **Green-Themed Responsive UI** 
- ✅ **Pure JavaScript** (no frameworks)
- ✅ **Accessibility Features** (ARIA labels, screen reader support)
- ✅ **Form Validation** and error handling
- ✅ **Loading States** with spinner
- ✅ **Retry Logic** for API calls
- ✅ **Environment-Aware** API URL configuration
- ✅ **Mobile-Responsive** design

### DevOps & Infrastructure
- ✅ **Docker Compose** orchestration
- ✅ **Multi-stage Docker builds** with security best practices
- ✅ **Health Checks** for all services
- ✅ **Resource Limits** and auto-restart policies
- ✅ **CI/CD Pipeline** with GitHub Actions
- ✅ **Automated Testing** (60+ test cases)
- ✅ **Code Coverage** reporting
- ✅ **Security Scanning** with Trivy and Safety
- ✅ **Code Linting** (flake8, black, isort)

## 📋 Prerequisites

- Docker and Docker Compose (for containerized deployment)
- Python 3.11+ (for local development)
- curl (for health checks)

## 🏃‍♂️ Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

2. **Start the application:**
```bash
docker-compose up -d
```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

4. **View logs:**
```bash
docker-compose logs -f
```

5. **Stop the application:**
```bash
docker-compose down
```

### Local Development

#### Backend

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python main.py
```

The API will be available at http://localhost:8000

#### Frontend

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Serve with a simple HTTP server:
```bash
python -m http.server 3000
```

The frontend will be available at http://localhost:3000

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Run Tests with Coverage

```bash
cd backend
pytest tests/ --cov=. --cov-report=html --cov-report=term
```

View coverage report: `backend/htmlcov/index.html`

### Run Specific Test Class

```bash
cd backend
pytest tests/test_main.py::TestGreetEndpoint -v
```

### Run Tests in Docker

```bash
docker-compose up -d
docker exec greeting-backend pytest tests/ -v
```

## 📚 API Documentation

### Endpoints

#### GET `/`
Returns API information and available endpoints.

**Response:**
```json
{
  "message": "Welcome to the Greeting API",
  "version": "1.0.0",
  "status": "operational",
  "endpoints": {
    "/greet": "POST - Greet a user by name",
    "/health": "GET - Health check endpoint",
    "/docs": "GET - API documentation"
  },
  "supported_languages": ["en", "es", "fr", "de", "it"]
}
```

#### GET `/health`
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "service": "greeting-api",
  "version": "1.0.0",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### POST `/greet`
Greet a user with a personalized message.

**Request Body:**
```json
{
  "name": "Alice",
  "language": "en"
}
```

**Response:**
```json
{
  "message": "Hello, Alice! Welcome to our application!",
  "name": "Alice",
  "language": "en",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Supported Languages:**
- `en` - English
- `es` - Spanish (Español)
- `fr` - French (Français)
- `de` - German (Deutsch)
- `it` - Italian (Italiano)

**Validation Rules:**
- Name: Required, 1-100 characters, cannot be empty or whitespace only
- Language: Optional (defaults to "en"), must be one of supported languages

### Interactive API Documentation

Visit http://localhost:8000/docs for Swagger UI documentation with interactive API testing.

## 🏗️ Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application with logging
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Backend container with security
│   ├── .dockerignore       # Docker ignore patterns
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py     # pytest configuration
│       └── test_main.py    # Comprehensive test suite (60+ tests)
├── frontend/
│   ├── index.html          # Accessible HTML with ARIA
│   ├── styles.css          # Green-themed responsive CSS
│   ├── app.js              # Vanilla JavaScript with retry logic
│   ├── nginx.conf          # Nginx configuration
│   ├── Dockerfile          # Frontend container
│   └── .dockerignore       # Docker ignore patterns
├── .github/
│   └── workflows/
│       └── ci.yml          # Comprehensive CI/CD pipeline
├── docker-compose.yml       # Multi-service orchestration
├── README.md               # This file
├── LICENSE                 # MIT License
└── .gitignore             # Git ignore patterns
```

## 🔄 CI/CD Pipeline

The project includes a comprehensive GitHub Actions CI/CD pipeline that runs on every push and pull request:

### Pipeline Jobs

1. **Test Backend**
   - Runs pytest with 60+ test cases
   - Generates coverage reports (HTML and XML)
   - Uploads coverage to Codecov

2. **Lint Backend**
   - Checks code with flake8 (errors and warnings)
   - Validates code formatting with black
   - Checks import ordering with isort

3. **Build Docker**
   - Builds backend and frontend Docker images
   - Tests container health checks
   - Validates service startup

4. **Integration Tests**
   - Starts full stack with Docker Compose
   - Tests all API endpoints
   - Validates multi-language support
   - Tests frontend accessibility

5. **Security Scan**
   - Scans dependencies with Safety
   - Scans Docker images with Trivy
   - Checks for known vulnerabilities

### Triggers

- Push to `main` branch
- Push to `feature/**` branches
- Push to `test-*` branches
- Pull requests to `main`

## 🎨 Frontend Features

### Green Theme
- Professional and calming color palette
- Gradient backgrounds
- Smooth animations and transitions

### Accessibility
- ARIA labels for screen readers
- Semantic HTML structure
- Keyboard navigation support
- High contrast mode support
- Reduced motion support
- Screen reader announcements

### User Experience
- Form validation with helpful error messages
- Loading states with spinner
- Retry logic for failed requests
- Mobile-responsive design
- Focus management for better navigation

## 🔒 Security Features

### Backend Security
- Input validation with Pydantic
- Request logging for audit trails
- Error handling without exposing internals
- CORS configuration
- Non-root user in Docker container
- Health check endpoints

### Frontend Security
- XSS prevention with text sanitization
- Input length limits
- Request timeout handling
- Environment-aware API URLs

### Infrastructure Security
- Minimal Docker base images
- .dockerignore to exclude sensitive files
- Resource limits in Docker Compose
- Automated security scanning in CI
- Dependency vulnerability checks

## 🐳 Docker Configuration

### Backend Container
- **Base**: `python:3.11-slim`
- **Port**: 8000
- **User**: Non-root (appuser)
- **Health Check**: curl to /health endpoint
- **Resources**: CPU 0.25-1.0, Memory 128-512MB

### Frontend Container
- **Base**: `nginx:alpine`
- **Port**: 80 (mapped to 3000)
- **Static Serving**: Nginx with gzip compression
- **Resources**: CPU 0.1-0.5, Memory 64-256MB

### Networks
- Isolated bridge network for service communication
- Services communicate via service names

## 📝 Development Workflow

1. **Create a feature branch:**
```bash
git checkout -b feature/your-feature-name
```

2. **Make changes and test locally:**
```bash
docker-compose up --build
```

3. **Run tests:**
```bash
cd backend && pytest tests/ -v
```

4. **Commit and push:**
```bash
git add .
git commit -m "Description of changes"
git push origin feature/your-feature-name
```

5. **Create a Pull Request** on GitHub

6. **CI pipeline will automatically:**
   - Run all tests
   - Check code quality
   - Build Docker images
   - Run integration tests
   - Scan for security vulnerabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Ensure code follows style guidelines
7. Submit a pull request

### Code Style Guidelines

- **Python**: Follow PEP 8, use type hints
- **JavaScript**: Use ES6+ features, clear variable names
- **Comments**: Explain complex logic, use docstrings
- **Tests**: Write descriptive test names, test edge cases

## 🐛 Troubleshooting

### Backend not starting
```bash
# Check logs
docker-compose logs backend

# Restart service
docker-compose restart backend
```

### Frontend cannot connect to backend
```bash
# Ensure backend is healthy
curl http://localhost:8000/health

# Check network connectivity
docker-compose ps
```

### Tests failing locally
```bash
# Ensure dependencies are updated
cd backend
pip install -r requirements.txt

# Run tests with verbose output
pytest tests/ -v --tb=short
```

## 📊 Performance

- Backend response time: < 50ms (average)
- Frontend load time: < 1s
- Docker image sizes:
  - Backend: ~200MB
  - Frontend: ~25MB

## 🔮 Future Enhancements

- [ ] Add authentication and authorization
- [ ] Database integration for storing greetings
- [ ] Rate limiting for API endpoints
- [ ] WebSocket support for real-time updates
- [ ] Additional language support
- [ ] User preferences and customization
- [ ] Analytics and usage tracking
- [ ] Internationalization (i18n) for UI
- [ ] Dark mode theme option
- [ ] Progressive Web App (PWA) support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for Python
- Containerized with [Docker](https://www.docker.com/) - Platform for developing, shipping, and running applications
- Tested with [pytest](https://pytest.org/) - Testing framework for Python
- Automated with [GitHub Actions](https://github.com/features/actions) - CI/CD platform

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ and 🌿**

*This project demonstrates best practices in full-stack development, containerization, testing, and CI/CD automation.*