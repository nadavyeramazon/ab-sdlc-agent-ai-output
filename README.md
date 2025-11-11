# Green Theme Hello World Fullstack Application

A modern fullstack web application demonstrating React frontend with FastAPI backend integration, featuring a beautiful green theme and containerized development environment.

## 🎯 Project Overview

This project serves as a reference implementation for building fullstack applications with:
- **Frontend**: React 18+ with Vite for fast development
- **Backend**: Python FastAPI for high-performance RESTful APIs
- **Orchestration**: Docker Compose for seamless multi-service deployment
- **Development**: Hot Module Replacement (HMR) for instant feedback

## ✨ Key Features

- 🎨 Beautiful green-themed responsive UI
- ⚡ Lightning-fast development with Vite HMR
- 🔄 Real-time backend auto-reload with Uvicorn
- 🐳 Single-command Docker Compose orchestration
- 🧪 Comprehensive test coverage (frontend & backend)
- ♿ WCAG 2.1 Level A accessibility compliance
- 📱 Fully responsive design (mobile, tablet, desktop)

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Git**: For cloning the repository

### Installation Links
- [Docker Desktop](https://www.docker.com/products/docker-desktop) (includes Docker Compose)
- [Docker Engine](https://docs.docker.com/engine/install/) (Linux)

### Verify Installation

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
- Start both services with hot-reload enabled
- Set up networking between services
- Display logs in your terminal

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)

### 4. Stop the Application

```bash
# Stop services (Ctrl+C in terminal, then)
docker compose down

# Stop and remove volumes
docker compose down -v
```

## 📁 Project Structure

```
project-root/
├── frontend/                  # React frontend application
│   ├── src/
│   │   ├── App.jsx           # Main application component
│   │   ├── App.css           # Green theme styling
│   │   ├── App.test.jsx      # Frontend tests
│   │   ├── main.jsx          # Application entry point
│   │   └── setupTests.js     # Test configuration
│   ├── index.html            # HTML template
│   ├── package.json          # Node dependencies
│   ├── vite.config.js        # Vite configuration
│   └── Dockerfile            # Frontend container
├── backend/                   # FastAPI backend application
│   ├── main.py               # FastAPI application
│   ├── test_main.py          # Backend tests
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile            # Backend container
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI/CD
├── docker-compose.yml        # Service orchestration
└── README.md                 # This file
```

## 🔌 API Endpoints

### GET /api/hello

Returns a greeting message with server timestamp.

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**Example:**
```bash
curl http://localhost:8000/api/hello
```

### GET /health

Health check endpoint for service monitoring.

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

## 🛠️ Development Workflow

### Running with Hot Reload

Both frontend and backend support hot reload in development mode:

1. **Start services**:
   ```bash
   docker compose up
   ```

2. **Edit frontend code** in `frontend/src/`
   - Changes reflect instantly in browser (HMR)
   - No page refresh needed for most changes

3. **Edit backend code** in `backend/main.py`
   - Uvicorn automatically reloads the server
   - Changes take effect in ~1-2 seconds

### Running Tests

#### Backend Tests (pytest)

```bash
# Run tests in Docker container
docker compose exec backend pytest test_main.py -v

# Run tests locally (requires Python 3.11+)
cd backend
pip install -r requirements.txt
pytest test_main.py -v
```

#### Frontend Tests (Vitest)

```bash
# Run tests in Docker container
docker compose exec frontend npm test

# Run tests locally (requires Node 18+)
cd frontend
npm install
npm test
```

### Viewing Logs

```bash
# View all service logs
docker compose logs

# View specific service logs
docker compose logs backend
docker compose logs frontend

# Follow logs in real-time
docker compose logs -f
```

### Rebuilding Containers

```bash
# Rebuild all services
docker compose build

# Rebuild specific service
docker compose build backend

# Rebuild and restart
docker compose up --build
```

## 🧪 Testing

### Test Coverage

#### Backend Tests (`backend/test_main.py`)
- ✅ Health endpoint functionality
- ✅ Hello endpoint response structure
- ✅ ISO 8601 timestamp format validation
- ✅ Response time performance (<100ms)
- ✅ CORS configuration
- ✅ Error handling (404, 405)
- ✅ API documentation availability

#### Frontend Tests (`frontend/src/App.test.jsx`)
- ✅ Component rendering
- ✅ User interactions (button clicks)
- ✅ Loading states
- ✅ Successful API integration
- ✅ Error handling scenarios
- ✅ Timeout handling
- ✅ Accessibility (ARIA attributes)
- ✅ Button state management
- ✅ Multiple interactions

### Continuous Integration

GitHub Actions automatically runs tests on every push and pull request:

```yaml
# .github/workflows/ci.yml
- Backend tests with pytest
- Frontend tests with Vitest
- Linting and code quality checks
```

## 🎨 Design Specifications

### Color Palette

- **Primary Green**: `#2ecc71`
- **Secondary Green**: `#27ae60`
- **Text Dark**: `#2c3e50`
- **Text Light**: `#ffffff`
- **Error Red**: `#e74c3c`
- **Success Green**: `#d5f4e6`

### Responsive Breakpoints

- **Mobile**: 320px - 767px
- **Tablet**: 768px - 1023px
- **Desktop**: 1024px+

### Accessibility Features

- Semantic HTML5 elements
- ARIA labels and roles
- Keyboard navigation support
- Screen reader compatibility
- High contrast mode support
- Reduced motion preferences

## 🐛 Troubleshooting

### Port Already in Use

**Error**: `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solution**:
```bash
# Find process using the port
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill the process or change port in docker-compose.yml
```

### Backend Not Responding

**Issue**: Frontend shows "Unable to connect to backend"

**Solutions**:
1. Check backend is running: `docker compose ps`
2. Check backend logs: `docker compose logs backend`
3. Verify backend health: `curl http://localhost:8000/health`
4. Restart services: `docker compose restart`

### Frontend Not Updating

**Issue**: Code changes not reflecting in browser

**Solutions**:
1. Hard refresh browser: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (macOS)
2. Check frontend logs: `docker compose logs frontend`
3. Rebuild frontend: `docker compose build frontend && docker compose up`

### Docker Build Fails

**Error**: `failed to solve with frontend dockerfile.v0`

**Solutions**:
1. Clear Docker cache: `docker system prune -a`
2. Remove volumes: `docker compose down -v`
3. Rebuild from scratch: `docker compose build --no-cache`

### Tests Failing

**Issue**: Tests pass locally but fail in CI

**Solutions**:
1. Check Node/Python versions match CI
2. Ensure all dependencies are installed
3. Check for environment-specific issues
4. Review CI logs in GitHub Actions

## 🔧 Configuration

### Environment Variables

#### Backend
```bash
LOG_LEVEL=info          # Logging level (debug, info, warning, error)
```

#### Frontend
```bash
VITE_API_URL=http://localhost:8000  # Backend API URL
```

### Modifying Ports

Edit `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8080:8000"  # Change 8080 to desired port
  
  frontend:
    ports:
      - "3001:3000"  # Change 3001 to desired port
```

## 📚 Technology Stack

### Frontend
- **React**: 18.2.0 - UI library
- **Vite**: 5.0.8 - Build tool and dev server
- **Vitest**: 1.0.4 - Testing framework
- **React Testing Library**: 14.1.2 - Component testing

### Backend
- **FastAPI**: 0.104.1 - Web framework
- **Uvicorn**: 0.24.0 - ASGI server
- **Pydantic**: 2.5.0 - Data validation
- **pytest**: 7.4.3 - Testing framework

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **GitHub Actions**: CI/CD pipeline

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a pull request

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Repository**: nadavyeramazon/ab-sdlc-agent-ai-backend
- **Branch**: feature/JIRA-777/fullstack-app

## 🙏 Acknowledgments

- FastAPI documentation for excellent API framework guidance
- React team for comprehensive documentation
- Vite team for blazing-fast development experience
- Docker community for containerization best practices

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: ✅ Production Ready
