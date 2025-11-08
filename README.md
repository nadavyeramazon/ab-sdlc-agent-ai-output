# Hello World FastAPI Application with Green UI

A modern, containerized Hello World API built with FastAPI and a beautiful green-themed frontend.

## 🌟 Features

- ✅ FastAPI backend with multiple endpoints
- ✅ Beautiful green-themed UI with vanilla JavaScript
- ✅ Docker Compose for easy deployment
- ✅ Comprehensive test coverage (backend, frontend, integration)
- ✅ GitHub Actions CI/CD pipeline
- ✅ Interactive API documentation (Swagger UI and ReDoc)
- ✅ Health check endpoints
- ✅ Nginx frontend server with optimization
- ✅ Type hints and comprehensive documentation

## 🚀 Quick Start with Docker Compose

### Prerequisites

- Docker and Docker Compose installed
- Git (to clone the repository)

### Running the Application

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ab-sdlc-agent-ai-backend
   ```

2. Start the services with Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Access the application:
   - **Frontend UI**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation (Swagger)**: http://localhost:8000/docs
   - **API Documentation (ReDoc)**: http://localhost:8000/redoc

4. Stop the services:
   ```bash
   docker-compose down
   ```

### Viewing Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
```

## 🎨 Frontend Features

The green-themed UI provides an interactive interface with:

- **API Status Indicator**: Real-time health monitoring
- **Welcome Message**: Get the API welcome message
- **Hello World**: Simple hello endpoint
- **Personalized Greeting**: Enter your name for a custom greeting
- **API Documentation Links**: Quick access to Swagger and ReDoc
- **Responsive Design**: Works on desktop and mobile devices
- **Modern Green Theme**: Beautiful green color palette
- **Smooth Animations**: Polished user experience

## 🔧 API Endpoints

### Root Endpoint
- **GET `/`** - Welcome message
  ```json
  {"message": "Welcome to the Hello World API"}
  ```

### Hello Endpoints
- **GET `/hello`** - Basic hello world message
  ```json
  {"message": "Hello, World!"}
  ```

- **GET `/hello/{name}`** - Personalized greeting
  ```json
  {"message": "Hello, {name}!"}
  ```

### Health Check
- **GET `/health`** - Service health status
  ```json
  {
    "status": "healthy",
    "service": "Hello World API",
    "version": "1.0.0"
  }
  ```

### Documentation
- **GET `/docs`** - Interactive API documentation (Swagger UI)
- **GET `/redoc`** - Alternative API documentation (ReDoc)
- **GET `/openapi.json`** - OpenAPI schema

## 💻 Local Development (Without Docker)

### Backend Setup

1. Create a virtual environment:
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
   Or with uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Development

For local frontend development, you can use any static file server:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 3000
```

Or use VS Code's Live Server extension.

## 🧪 Testing

### Run All Tests

```bash
pytest -v
```

### Run Specific Test Suites

```bash
# Backend tests
pytest test_main.py -v

# Frontend unit tests
pytest test_frontend_unit.py -v

# Docker Compose tests
pytest test_docker_compose.py -v
```

### Test Coverage

The test suite includes:
- ✅ Backend API endpoint tests
- ✅ Frontend HTML/CSS/JavaScript tests
- ✅ Docker configuration validation
- ✅ Integration readiness tests
- ✅ Health check tests
- ✅ Error handling tests
- ✅ Response structure validation

## 🏗️ Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI pipeline
├── frontend/
│   ├── index.html              # Main HTML file
│   ├── styles.css              # Green-themed CSS
│   ├── app.js                  # Vanilla JavaScript
│   ├── nginx.conf              # Nginx configuration
│   └── Dockerfile              # Frontend container
├── main.py                     # FastAPI application
├── test_main.py                # Backend tests
├── test_frontend_unit.py       # Frontend unit tests
├── test_docker_compose.py      # Docker integration tests
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Backend container
├── docker-compose.yml          # Multi-container setup
├── .gitignore                  # Git ignore file
├── README.md                   # This file
└── LICENSE                     # License file
```

## 🐳 Docker Architecture

### Services

1. **Backend Service** (`backend`)
   - FastAPI application
   - Python 3.11
   - Port 8000
   - Health checks enabled

2. **Frontend Service** (`frontend`)
   - Nginx web server
   - Static files (HTML, CSS, JS)
   - Port 3000 (mapped to container port 80)
   - Depends on backend health

### Networks

- `app-network`: Bridge network for service communication

### Health Checks

Both services have health checks configured:
- Backend: HTTP check on `/health` endpoint
- Frontend: HTTP check on root `/` endpoint

## 🔄 CI/CD Pipeline

The GitHub Actions workflow includes:

1. **Test Job**
   - Backend API tests
   - Frontend unit tests
   - Docker configuration tests

2. **Lint Job**
   - Code quality checks with flake8
   - Code formatting validation with black

3. **Build Job**
   - Application import verification
   - Endpoint validation

4. **Docker Job**
   - Docker image builds
   - Docker Compose integration testing
   - Health check verification

5. **Frontend Validation Job**
   - HTML structure validation
   - CSS green theme verification
   - JavaScript function checks

## 🛠️ Technologies Used

### Backend
- **FastAPI** (0.115.5) - Modern web framework
- **Uvicorn** (0.34.0) - ASGI server
- **Pydantic** (2.10.3) - Data validation
- **Python** (3.11) - Programming language

### Frontend
- **Vanilla JavaScript** - No frameworks, pure JS
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with animations
- **Nginx** - Web server

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD automation
- **Pytest** (8.3.4) - Testing framework

## 📝 Environment Variables

The application uses environment-aware configuration:

- Frontend automatically detects backend URL based on hostname
- No manual configuration needed for Docker Compose setup
- Backend runs on `0.0.0.0:8000` in container

## 🔐 Security Features

- Nginx security headers configured
- CORS ready (can be easily added to FastAPI)
- Health check endpoints
- Input validation in backend
- XSS protection headers
- Content type sniffing prevention

## 🚀 Production Deployment

For production deployment:

1. Update API URLs in frontend if needed
2. Configure environment variables
3. Use production-ready web server (e.g., Gunicorn with Uvicorn workers)
4. Set up SSL/TLS certificates
5. Configure proper logging
6. Set up monitoring and alerting
7. Use container orchestration (Kubernetes, ECS, etc.)

## 🤝 Contributing

Contributions are welcome! Please ensure:
- All tests pass: `pytest -v`
- Code follows PEP 8 style guide
- Frontend uses vanilla JavaScript only
- New features include tests
- Documentation is updated
- Docker Compose setup works

## 📄 License

See LICENSE file for details.

## 🐛 Troubleshooting

### Docker Compose Issues

**Services not starting:**
```bash
docker-compose down
docker-compose up --build
```

**Port conflicts:**
- Check if ports 8000 or 3000 are already in use
- Modify port mappings in `docker-compose.yml`

**Health check failures:**
```bash
docker-compose logs backend
docker-compose logs frontend
```

### Frontend Issues

**API connection fails:**
- Ensure backend is running: `curl http://localhost:8000/health`
- Check browser console for errors
- Verify API_BASE_URL in app.js

### Backend Issues

**Import errors:**
```bash
pip install -r requirements.txt
```

**Port already in use:**
```bash
# Find process using port 8000
lsof -i :8000  # On Linux/Mac
netstat -ano | findstr :8000  # On Windows
```

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with detailed information

## 🎯 Future Enhancements

- [ ] Add user authentication
- [ ] Implement data persistence
- [ ] Add more interactive features
- [ ] Create additional themes
- [ ] Add WebSocket support for real-time updates
- [ ] Implement API rate limiting
- [ ] Add metrics and monitoring dashboard
- [ ] Create mobile app version

---

**Built with ❤️ using FastAPI and Vanilla JavaScript**