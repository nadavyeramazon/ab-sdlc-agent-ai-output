# 🌿 Greeting Application - Full Stack Implementation

[![CI Pipeline](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml)

A full-stack web application that greets users in multiple languages with a beautiful green-themed interface.

## 🚀 Features

- **FastAPI Backend**: RESTful API with comprehensive validation
- **Vanilla JavaScript Frontend**: No frameworks, pure JavaScript with green theme
- **Multi-language Support**: English, Spanish, French, German, and Italian
- **Docker Compose**: Easy deployment and orchestration
- **Comprehensive Testing**: pytest with FastAPI TestClient
- **CI/CD Pipeline**: GitHub Actions with automated testing
- **Health Checks**: Built-in health monitoring
- **CORS Support**: Cross-origin resource sharing enabled
- **Responsive Design**: Mobile-friendly green-themed UI

## 📋 Prerequisites

- Docker and Docker Compose (for containerized deployment)
- Python 3.11+ (for local development)
- Node.js/npm (optional, for frontend development)

## 🏃‍♂️ Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

2. Start the application:
```bash
docker-compose up -d
```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. Stop the application:
```bash
docker-compose down
```

### Local Development

#### Backend

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
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

2. Open `index.html` in your browser or use a simple HTTP server:
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
pytest tests/ --cov=. --cov-report=html
```

View coverage report: `backend/htmlcov/index.html`

### Test Specific Module

```bash
cd backend
pytest tests/test_main.py::TestGreetEndpoint -v
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
  "endpoints": {
    "/greet": "POST - Greet a user by name",
    "/health": "GET - Health check endpoint"
  }
}
```

#### GET `/health`
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "service": "greeting-api"
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
  "language": "en"
}
```

**Supported Languages:**
- `en` - English
- `es` - Spanish (Español)
- `fr` - French (Français)
- `de` - German (Deutsch)
- `it` - Italian (Italiano)

### Interactive API Documentation

Visit http://localhost:8000/docs for Swagger UI documentation.

## 🏗️ Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Backend container definition
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py     # pytest configuration
│       └── test_main.py    # Comprehensive test suite
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── styles.css          # Green-themed CSS
│   ├── app.js              # Vanilla JavaScript
│   ├── nginx.conf          # Nginx configuration
│   └── Dockerfile          # Frontend container definition
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI pipeline
├── docker-compose.yml       # Multi-service orchestration
└── README.md               # This file
```

## 🔄 CI/CD Pipeline

The project includes a comprehensive GitHub Actions CI pipeline that:

1. **Tests Backend**: Runs pytest with coverage reporting
2. **Lints Code**: Checks code quality with flake8 and black
3. **Builds Docker Images**: Builds and tests Docker containers
4. **Integration Tests**: Tests the full stack with Docker Compose
5. **Security Scan**: Checks dependencies for vulnerabilities

### Triggers

- Push to `main` branch
- Push to any `feature/**` or `test-*` branch
- Pull requests to `main`

## 🎨 Frontend Features

- **Green Theme**: Calming and professional green color scheme
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Form Validation**: Client-side input validation
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages
- **Multi-language Support**: Dropdown for language selection

## 🔒 Security

- Input validation on both client and server
- CORS configuration for secure cross-origin requests
- Health check endpoints for monitoring
- Container security with minimal base images
- Dependency scanning in CI pipeline

## 🐳 Docker Configuration

### Backend Container
- Base: `python:3.11-slim`
- Port: 8000
- Health checks enabled

### Frontend Container
- Base: `nginx:alpine`
- Port: 80 (mapped to 3000)
- Static file serving with Nginx

### Networks
- Isolated bridge network for service communication

## 📝 Development Workflow

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make changes and test locally:
```bash
docker-compose up --build
```

3. Run tests:
```bash
cd backend && pytest tests/ -v
```

4. Commit and push:
```bash
git add .
git commit -m "Description of changes"
git push origin feature/your-feature-name
```

5. Create a Pull Request on GitHub

6. CI pipeline will automatically run tests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

See LICENSE file for details.

## 🙏 Acknowledgments

- Built with FastAPI and Vanilla JavaScript
- Containerized with Docker
- Tested with pytest
- Automated with GitHub Actions

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

Made with ❤️ and 🌿
