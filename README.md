# Green Theme Hello World Fullstack Application

[![CI/CD](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml/badge.svg?branch=feature/JIRA-777/fullstack-app)](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml)

A modern fullstack "Hello World" application featuring a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose for local development.

## 🎯 Overview

This application demonstrates:
- **Frontend-Backend Integration**: React frontend communicating with FastAPI backend
- **Modern Web Technologies**: React 18, Vite, FastAPI, Docker
- **Green Theme UI**: Beautiful emerald green (#2ecc71) themed interface
- **Containerization**: Docker Compose orchestration with hot reload
- **API Communication**: RESTful API with proper CORS configuration
- **Error Handling**: Graceful error handling and user feedback
- **Comprehensive Testing**: Backend tests with pytest and frontend tests with Vitest
- **CI/CD**: Automated testing with GitHub Actions

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                             │
│                   http://localhost:3000                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ API Calls
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose                           │
│                                                             │
│  ┌─────────────────────┐      ┌──────────────────────┐    │
│  │   Frontend          │      │   Backend            │    │
│  │   React + Vite      │◄────►│   FastAPI            │    │
│  │   Port: 3000        │      │   Port: 8000         │    │
│  └─────────────────────┘      └──────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Technology Stack

### Frontend
- **React 18.2.0**: Modern UI library with hooks
- **Vite 5.0**: Lightning-fast build tool and dev server
- **CSS3**: Custom styling with responsive design
- **Vitest**: Unit testing framework
- **React Testing Library**: Component testing utilities

### Backend
- **FastAPI 0.109.0**: Modern Python web framework
- **Uvicorn 0.27.0**: ASGI server with auto-reload
- **Python 3.11**: Latest Python features
- **pytest**: Comprehensive testing framework

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **GitHub Actions**: CI/CD automation
- **Hot Module Replacement**: Fast development workflow

## 📋 Prerequisites

Before running the application, ensure you have:

- **Docker**: Version 20.x or higher
- **Docker Compose**: Version 2.x or higher
- **Git**: For cloning the repository

Check versions:
```bash
docker --version
docker compose version
git --version
```

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

### 2. Checkout the Feature Branch

```bash
git checkout feature/JIRA-777/fullstack-app
```

### 3. Start the Application

```bash
docker compose up --build
```

This command will:
- Build Docker images for frontend and backend
- Start both services
- Enable hot reload for development
- Display logs from both containers

**Expected startup time**: < 15 seconds

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Health Check**: http://localhost:8000/health

### 5. Stop the Application

```bash
docker compose down
```

To also remove volumes:
```bash
docker compose down -v
```

## 🎮 Usage

### Using the Frontend

1. Open http://localhost:3000 in your browser
2. You'll see a green-themed page with "Hello World" heading
3. Click the **"Get Message from Backend"** button
4. Watch the loading indicator appear
5. See the message "Hello World from Backend!" display

### Testing the Backend API

#### Using curl:

```bash
# Get hello message
curl http://localhost:8000/api/hello

# Check health
curl http://localhost:8000/health
```

#### Using browser:

Navigate to:
- http://localhost:8000/api/hello
- http://localhost:8000/health

#### Expected Responses:

**GET /api/hello**:
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**GET /health**:
```json
{
  "status": "healthy"
}
```

## 🧪 Running Tests

### Backend Tests (pytest)

```bash
# Run all backend tests
cd backend
python -m pytest

# Run with verbose output
python -m pytest -v

# Run with coverage
python -m pytest --cov=main --cov-report=html
```

**Test Coverage**:
- Health endpoint tests
- Hello endpoint tests
- CORS configuration tests
- Response format validation
- Performance tests (< 100ms response time)
- Timestamp format validation

### Frontend Tests (Vitest)

```bash
# Run all frontend tests
cd frontend
npm test

# Run tests in watch mode
npm run test:watch

# Run with UI
npm run test -- --ui
```

**Test Coverage**:
- Component rendering tests
- Button interaction tests
- API call mocking and validation
- Loading state tests
- Error handling tests
- Accessibility tests

### Running Tests in Docker

```bash
# Backend tests
docker compose exec backend pytest

# Frontend tests
docker compose exec frontend npm test
```

## 📁 Project Structure

```
project-root/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── test_main.py         # Backend tests
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container config
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Styling
│   │   ├── App.test.jsx     # Frontend tests
│   │   ├── main.jsx         # React entry point
│   │   └── test/
│   │       └── setup.js     # Test configuration
│   ├── index.html           # HTML template
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   └── Dockerfile           # Frontend container config
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI workflow
├── docker-compose.yml       # Docker Compose orchestration
└── README.md               # This file
```

## 🎨 Features

### Frontend Features
- ✅ Green-themed responsive UI (#2ecc71)
- ✅ Centered content layout
- ✅ Interactive button with hover effects
- ✅ Loading indicator with spinner animation
- ✅ Success message display
- ✅ Error handling with user-friendly messages
- ✅ Disabled button state during API calls
- ✅ Mobile-responsive design
- ✅ Accessibility attributes (ARIA labels)
- ✅ Smooth animations and transitions

### Backend Features
- ✅ RESTful API with FastAPI
- ✅ CORS enabled for localhost:3000
- ✅ ISO 8601 timestamp format
- ✅ Health check endpoint
- ✅ Auto-reload on code changes
- ✅ Comprehensive logging
- ✅ API documentation (Swagger UI)
- ✅ < 100ms response time

### DevOps Features
- ✅ Docker Compose orchestration
- ✅ Hot Module Replacement (HMR)
- ✅ Volume mounts for live code sync
- ✅ Health checks for services
- ✅ Custom bridge network
- ✅ Clean startup and shutdown
- ✅ GitHub Actions CI workflow
- ✅ Automated testing on push/PR

## 🔧 Development

### Hot Reload

Both frontend and backend support hot reload:

**Frontend**: Vite HMR automatically reloads on file changes
```bash
# Edit files in frontend/src/
# Browser updates automatically
```

**Backend**: Uvicorn auto-reload restarts on file changes
```bash
# Edit backend/main.py
# Server restarts automatically
```

### Viewing Logs

```bash
# All services
docker compose logs -f

# Backend only
docker compose logs -f backend

# Frontend only
docker compose logs -f frontend
```

### Rebuilding Services

```bash
# Rebuild all services
docker compose up --build

# Rebuild specific service
docker compose build backend
docker compose build frontend
```

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use

**Problem**: `Error: Port 3000/8000 is already allocated`

**Solution**:
```bash
# Find process using the port
lsof -i :3000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change ports in docker-compose.yml
```

#### Backend Not Responding

**Problem**: Frontend shows "Failed to fetch message from backend"

**Solution**:
```bash
# Check backend is running
docker compose ps

# Check backend logs
docker compose logs backend

# Test backend directly
curl http://localhost:8000/health

# Restart backend
docker compose restart backend
```

#### Frontend Not Loading

**Problem**: Browser shows "Cannot connect" or white page

**Solution**:
```bash
# Check frontend is running
docker compose ps

# Check frontend logs
docker compose logs frontend

# Rebuild and restart
docker compose up --build frontend
```

#### CORS Errors

**Problem**: Browser console shows CORS policy errors

**Solution**:
- Ensure backend CORS middleware includes `http://localhost:3000`
- Check browser is accessing `http://localhost:3000` (not `127.0.0.1`)
- Verify frontend API URL is correct in `App.jsx`

#### Docker Build Failures

**Problem**: `docker compose up --build` fails

**Solution**:
```bash
# Clean Docker cache
docker system prune -a

# Remove all containers and volumes
docker compose down -v

# Rebuild from scratch
docker compose up --build
```

#### Hot Reload Not Working

**Problem**: Changes don't reflect automatically

**Solution**:
```bash
# Check volumes are mounted correctly
docker compose config

# Restart with clean state
docker compose down
docker compose up
```

## 📊 Performance

### Metrics

- **Frontend Load Time**: < 2 seconds
- **API Response Time**: < 100ms
- **Docker Startup Time**: < 15 seconds
- **Hot Reload Update**: < 1 second

### Optimization Tips

1. **Docker**: Use BuildKit for faster builds
   ```bash
   DOCKER_BUILDKIT=1 docker compose build
   ```

2. **Frontend**: Vite already optimized for development

3. **Backend**: Uvicorn with `--reload` is optimized for dev

## 🔒 Security Notes

This is a **development application** with minimal security:

- ⚠️ HTTP only (no HTTPS)
- ⚠️ No authentication/authorization
- ⚠️ CORS open for localhost
- ⚠️ Debug mode enabled
- ⚠️ Not production-ready

**Do NOT use in production without proper security hardening.**

## 🤝 Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

### Code Style

- **Python**: Follow PEP 8
- **JavaScript**: Use ESLint with React config
- **Commits**: Use conventional commits format

## 📝 API Documentation

### Endpoints

#### GET /api/hello

Returns greeting message with timestamp.

**Response**:
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**Status Codes**:
- `200 OK`: Success
- `500 Internal Server Error`: Server error

#### GET /health

Health check endpoint.

**Response**:
```json
{
  "status": "healthy"
}
```

**Status Codes**:
- `200 OK`: Service is healthy

### CORS Configuration

- **Allowed Origins**: `http://localhost:3000`, `http://127.0.0.1:3000`
- **Allowed Methods**: GET, POST, OPTIONS
- **Allowed Headers**: Content-Type
- **Credentials**: False

## 🧪 Testing Strategy

### Backend Tests

1. **Health Endpoint Tests**: Verify health check works
2. **Hello Endpoint Tests**: Validate response structure
3. **CORS Tests**: Ensure CORS headers are correct
4. **Performance Tests**: Check response times < 100ms
5. **Timestamp Tests**: Validate ISO 8601 format

### Frontend Tests

1. **Rendering Tests**: Component displays correctly
2. **Interaction Tests**: Button clicks work
3. **API Tests**: Mock fetch calls
4. **Loading Tests**: Loading state shows correctly
5. **Error Tests**: Error handling works
6. **Accessibility Tests**: ARIA attributes present

## 🚦 CI/CD Pipeline

GitHub Actions workflow runs on every push and pull request:

1. **Backend Tests**:
   - Setup Python 3.11
   - Install dependencies
   - Run pytest

2. **Frontend Tests**:
   - Setup Node.js 18
   - Install dependencies
   - Run Vitest

3. **Docker Build Test**:
   - Build both services
   - Verify containers start

View workflow status in Actions tab.

## 📄 License

See [LICENSE](LICENSE) file for details.

## 👥 Authors

- Development Team - Initial implementation

## 🙏 Acknowledgments

- FastAPI for the amazing Python web framework
- React team for the excellent UI library
- Vite team for the blazing-fast build tool
- Docker for containerization technology

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review existing GitHub Issues
3. Create a new issue with detailed information

---

**Built with ❤️ using React, FastAPI, and Docker**
