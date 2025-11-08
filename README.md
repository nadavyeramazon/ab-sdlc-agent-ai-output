# Hello World FastAPI with Green Themed UI

[![CI Pipeline](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml)

🌿 A beautiful green-themed web interface paired with a FastAPI backend, fully containerized with Docker Compose for seamless deployment.

## Features

- 🎨 **Green Themed UI**: Beautiful, responsive green-themed interface built with vanilla JavaScript
- 🚀 **FastAPI Backend**: Modern, fast web framework for building APIs
- 🐳 **Docker Compose**: One-command deployment of both frontend and backend
- ✅ **Comprehensive Tests**: Full test coverage with pytest including Docker integration tests
- 🔄 **CI/CD Pipeline**: Automated testing with GitHub Actions including Docker build tests
- 📚 **API Documentation**: Auto-generated OpenAPI/Swagger docs
- 🐍 **Python 3.9+**: Compatible with Python 3.9, 3.10, and 3.11
- 🌐 **Nginx Frontend**: Production-ready nginx server for static files

## Quick Start with Docker Compose

### Prerequisites
- Docker (20.10 or higher)
- Docker Compose (v2 or higher)

### Running the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
   cd ab-sdlc-agent-ai-backend
   ```

2. Start the application:
   ```bash
   docker compose up -d
   ```

3. Access the application:
   - **Frontend UI**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc

4. Stop the application:
   ```bash
   docker compose down
   ```

### Docker Services

- **Backend** (FastAPI): Runs on port 8000
  - Health check endpoint: `/health`
  - Auto-restart enabled
  - Built from project root `Dockerfile`

- **Frontend** (Nginx): Runs on port 3000
  - Serves green-themed UI
  - Auto-restart enabled
  - Built from `frontend/Dockerfile`

## API Endpoints

### Root Endpoint
- **GET** `/` - Returns a simple hello world message
  ```json
  {"message": "Hello World"}
  ```

### Health Check
- **GET** `/health` - Health check endpoint
  ```json
  {"status": "healthy"}
  ```

### Personalized Greeting
- **GET** `/hello/{name}` - Returns a personalized greeting
  ```json
  {"message": "Hello {name}!"}
  ```

## Development Setup (Without Docker)

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Backend Setup

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the backend:
   ```bash
   python main.py
   ```
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

For development, you can serve the frontend with any static file server:

```bash
cd frontend
python -m http.server 3000
```

Or use the provided Docker setup:
```bash
cd frontend
docker build -t green-frontend .
docker run -p 3000:80 green-frontend
```

## Running Tests

### Run all tests:
```bash
pytest tests/ -v
```

### Run only unit tests:
```bash
pytest tests/test_main.py -v
```

### Run only Docker integration tests:
```bash
pytest tests/test_docker_integration.py -v
```

### Run tests with coverage:
```bash
pytest tests/ --cov=. --cov-report=term-missing
```

### Skip integration tests (for environments without Docker):
```bash
pytest tests/ -v -m "not integration"
```

## Project Structure

```
.
├── main.py                     # FastAPI application
├── Dockerfile                  # Backend Docker configuration
├── docker-compose.yml          # Docker Compose orchestration
├── requirements.txt            # Python dependencies
├── frontend/
│   ├── index.html             # Green-themed UI
│   ├── styles.css             # Green color scheme styles
│   ├── app.js                 # Vanilla JavaScript for API calls
│   ├── nginx.conf             # Nginx configuration
│   └── Dockerfile             # Frontend Docker configuration
├── tests/
│   ├── __init__.py
│   ├── test_main.py           # Backend API tests
│   └── test_docker_integration.py  # Docker setup tests
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI pipeline
├── README.md                   # This file
└── LICENSE                     # License file
```

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration. The pipeline:

- ✅ Runs on every push and pull request
- 🔄 Tests against Python 3.9, 3.10, and 3.11
- 🐳 Builds and tests Docker images
- 📊 Generates code coverage reports
- 🔍 Performs code quality checks (flake8, black, isort)
- 📦 Caches dependencies for faster builds
- 🏥 Tests Docker Compose setup and health checks

## Technology Stack

### Backend
- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: Lightning-fast ASGI server
- **Python 3.11**: Latest Python features

### Frontend
- **Vanilla JavaScript**: No frameworks - pure JS for simplicity
- **HTML5 & CSS3**: Modern web standards
- **Nginx**: High-performance web server
- **Green Theme**: Carefully designed color palette

### DevOps
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container orchestration
- **GitHub Actions**: CI/CD automation
- **Pytest**: Testing framework

## Green Theme Color Palette

- **Primary Green**: `#2d5016` - Deep forest green
- **Secondary Green**: `#4a7c2c` - Rich medium green
- **Light Green**: `#6da83e` - Fresh grass green
- **Accent Green**: `#8bc34a` - Vibrant lime green
- **Pale Green**: `#c8e6c9` - Soft mint green
- **Background**: `#f1f8e9` - Light cream green

## Features of the Green UI

- 🎨 **Responsive Design**: Works on desktop, tablet, and mobile
- 🌊 **Smooth Animations**: Elegant transitions and effects
- 🔘 **Interactive Buttons**: Visual feedback on all interactions
- 📊 **Real-time API Results**: Display JSON responses beautifully
- ⚡ **Fast Loading**: Optimized CSS and JavaScript
- ♿ **Accessible**: Semantic HTML and proper contrast ratios
- 🌈 **Gradient Backgrounds**: Modern, eye-catching design

## Docker Commands

### Build images:
```bash
# Build all services
docker compose build

# Build specific service
docker compose build backend
docker compose build frontend
```

### View logs:
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
```

### Restart services:
```bash
docker compose restart
```

### Remove containers and volumes:
```bash
docker compose down -v
```

## Development

### Code Quality

The project follows Python best practices:
- PEP 8 style guide compliance
- Type hints for better code clarity
- Comprehensive docstrings
- Clean code principles

### Testing Philosophy

Tests are organized into classes by functionality:
- **TestRootEndpoint**: Tests for the root endpoint
- **TestHealthCheckEndpoint**: Health check tests
- **TestHelloNameEndpoint**: Personalized greeting tests
- **TestDockerfileExists**: Docker configuration validation
- **TestFrontendFiles**: Frontend file validation
- **TestGreenTheming**: Green theme verification

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Backend not responding
```bash
# Check backend logs
docker compose logs backend

# Verify backend is running
docker compose ps

# Check health endpoint
curl http://localhost:8000/health
```

### Frontend not loading
```bash
# Check frontend logs
docker compose logs frontend

# Verify nginx is running
docker compose ps

# Check frontend accessibility
curl http://localhost:3000
```

### Port conflicts
If ports 3000 or 8000 are already in use, modify `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # Change backend to port 8080
  - "3001:80"    # Change frontend to port 3001
```

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

Built with 💚 using FastAPI, Vanilla JavaScript, Docker, and GitHub Actions