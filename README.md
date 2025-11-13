# Green Theme Hello World Fullstack Application

<div align="center">

![React](https://img.shields.io/badge/React-18.2.0-61dafb?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11-3776ab?logo=python)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ed?logo=docker)

</div>

A modern fullstack "Hello World" application featuring a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose. This project demonstrates best practices in web development, containerization, and API integration.

## 🌟 Features

- **Green-themed React Frontend**: Beautiful, responsive UI with gradient backgrounds
- **FastAPI Backend**: High-performance API with automatic documentation
- **Docker Compose Orchestration**: One-command deployment for both services
- **Hot Module Replacement**: Instant feedback during development
- **Comprehensive Testing**: Full test coverage for both frontend and backend
- **CI/CD Pipeline**: Automated testing with GitHub Actions
- **CORS Configuration**: Secure cross-origin resource sharing
- **Health Checks**: Monitor service availability

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)
- **Git** (for cloning the repository)

Verify your installation:

```bash
docker --version
docker compose version
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
git checkout feature/JIRA-777/fullstack-app
```

### 2. Start the Application

```bash
docker compose up
```

This single command will:
- Build both frontend and backend Docker images
- Start all services
- Set up networking between containers
- Mount volumes for hot reload

Wait for the services to start (typically 10-15 seconds). You'll see logs from both services in your terminal.

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Backend API Docs**: http://localhost:8000/docs (Swagger UI)
- **Backend Health Check**: http://localhost:8000/health

### 4. Test the Application

1. Open your browser to http://localhost:3000
2. You should see a green-themed page with "Hello World" heading
3. Click the "Get Message from Backend" button
4. The backend message will appear below the button

## 🏗️ Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── test_main.py         # Backend tests
│   └── Dockerfile           # Backend container definition
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Component styling
│   │   ├── App.test.jsx     # Frontend tests
│   │   ├── main.jsx         # React entry point
│   │   ├── index.css        # Global styles
│   │   └── setupTests.js    # Test configuration
│   ├── public/              # Static assets
│   ├── index.html           # HTML template
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   ├── .eslintrc.cjs        # ESLint configuration
│   └── Dockerfile           # Frontend container definition
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD pipeline
├── docker-compose.yml       # Service orchestration
└── README.md               # This file
```

## 🔧 Development

### Running Tests

#### Backend Tests

```bash
cd backend
pip install -r requirements.txt
pytest -v
```

#### Frontend Tests

```bash
cd frontend
npm install
npm test
```

### Hot Reload

Both services support hot reload:

- **Frontend**: Edit files in `frontend/src/` and see changes instantly
- **Backend**: Edit `backend/main.py` and the server will auto-reload

### Stopping Services

```bash
# Stop and remove containers
docker compose down

# Stop, remove containers, and delete volumes
docker compose down -v
```

### Viewing Logs

```bash
# All services
docker compose logs

# Specific service
docker compose logs backend
docker compose logs frontend

# Follow logs in real-time
docker compose logs -f
```

### Restarting Services

```bash
# Restart all services
docker compose restart

# Restart specific service
docker compose restart backend
```

## 🧪 Testing

### Backend Test Coverage

The backend includes comprehensive tests covering:
- ✅ Health check endpoint
- ✅ Hello endpoint with message and timestamp
- ✅ CORS configuration
- ✅ Response time performance
- ✅ JSON response structure
- ✅ ISO 8601 timestamp format

Run with coverage:

```bash
cd backend
pip install pytest-cov
pytest --cov=main --cov-report=html
```

### Frontend Test Coverage

The frontend includes comprehensive tests covering:
- ✅ Initial render and UI elements
- ✅ Button click interactions
- ✅ Loading state management
- ✅ Successful API calls
- ✅ Error handling
- ✅ Multiple interactions

Run with UI:

```bash
cd frontend
npm run test:ui
```

## 🌐 API Documentation

### Endpoints

#### GET /api/hello

Returns a greeting message with timestamp.

**Response (200 OK):**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00.123456Z"
}
```

#### GET /health

Health check endpoint for monitoring.

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

### Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎨 Design Specifications

### Color Palette

- **Primary Green**: `#2ecc71`
- **Secondary Green**: `#27ae60`
- **Light Green**: `#a8e6cf`
- **Dark Green**: `#1e8449`
- **White**: `#ffffff`
- **Error Red**: `#e74c3c`

### Responsive Design

The application is fully responsive:
- **Desktop**: Full-size layout (> 768px)
- **Tablet**: Adjusted spacing and font sizes (768px)
- **Mobile**: Compact layout (< 375px)

## 🔒 Security

- **CORS**: Configured to allow requests only from `http://localhost:3000`
- **No Hardcoded Credentials**: Environment-based configuration
- **Input Validation**: Pydantic models for request/response validation

## 📊 Performance

- **Frontend Load Time**: < 2 seconds
- **API Response Time**: < 100ms
- **Docker Startup Time**: < 10 seconds

## 🐛 Troubleshooting

### Port Conflicts

**Problem**: Error: "port is already allocated"

**Solution**:
```bash
# Check what's using the port
lsof -i :3000
lsof -i :8000

# Stop the conflicting service or modify docker-compose.yml
```

### Services Not Starting

**Problem**: Containers fail to start

**Solution**:
```bash
# Check logs
docker compose logs

# Rebuild images
docker compose build --no-cache
docker compose up
```

### CORS Errors

**Problem**: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Solution**:
- Ensure backend is running on port 8000
- Check CORS configuration in `backend/main.py`
- Verify frontend is accessing `http://localhost:8000`

### Hot Reload Not Working

**Problem**: Changes don't reflect automatically

**Solution**:
- Check volume mounts in `docker-compose.yml`
- Restart services: `docker compose restart`
- For Windows/Mac: Ensure Docker Desktop file sharing is enabled

### Network Issues

**Problem**: Frontend can't reach backend

**Solution**:
```bash
# Check network
docker network ls

# Inspect network
docker network inspect ab-sdlc-agent-ai-backend_app-network

# Recreate network
docker compose down
docker compose up
```

## 🔄 CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow that:

1. **Backend Tests**: Runs pytest with coverage reporting
2. **Frontend Tests**: Runs Vitest tests and ESLint
3. **Docker Build**: Tests Docker image builds
4. **Integration Tests**: Validates full stack with Docker Compose

Workflow is triggered on:
- Push to `main` or `feature/**` branches
- Pull requests to `main`

## 📝 Development Notes

### Technology Choices

- **React 18**: Latest stable version with concurrent features
- **Vite**: Fast build tool with excellent HMR
- **FastAPI**: Modern Python framework with automatic docs
- **Docker Compose**: Simple multi-container orchestration
- **Vitest**: Fast unit test framework for Vite projects
- **pytest**: Comprehensive Python testing framework

### Best Practices Implemented

- ✅ Functional React components with hooks
- ✅ Async/await for API calls
- ✅ Error boundaries and error handling
- ✅ Loading states for better UX
- ✅ Type hints in Python code
- ✅ Pydantic models for validation
- ✅ Comprehensive test coverage
- ✅ Clean code with comments
- ✅ Semantic HTML with ARIA attributes
- ✅ Mobile-first responsive design

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for excellent API framework and documentation
- React team for the amazing frontend library
- Docker for containerization platform
- Vite for blazing-fast build tooling

## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

<div align="center">

**Built with ❤️ using React, FastAPI, and Docker**

</div>
