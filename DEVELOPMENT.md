# Development Guide

This guide provides detailed information for developers working on the Green Theme Hello World Fullstack Application.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Development Setup](#development-setup)
- [Code Structure](#code-structure)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Debugging](#debugging)
- [Performance Optimization](#performance-optimization)
- [Common Issues](#common-issues)

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Docker Compose                         │
│                                                             │
│  ┌──────────────────────┐    ┌─────────────────────────┐  │
│  │  Frontend Container  │    │  Backend Container      │  │
│  │  (React + Vite)      │◄───┤  (Python + FastAPI)    │  │
│  │  Port: 3000          │    │  Port: 8000             │  │
│  │                      │    │                         │  │
│  │  - Hot Module        │    │  - Auto-reload          │  │
│  │    Replacement       │    │  - CORS enabled         │  │
│  │  - Dev server        │    │  - Health checks        │  │
│  └──────────────────────┘    └─────────────────────────┘  │
│           │                            │                    │
│           └────────────────────────────┘                    │
│                  app-network (bridge)                       │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
                   Host Machine
              http://localhost:3000
              http://localhost:8000
```

### Frontend Architecture (React)

- **Framework**: React 18 with functional components and hooks
- **Build Tool**: Vite for fast development and optimized builds
- **State Management**: Local component state using useState
- **Styling**: Pure CSS with responsive design and accessibility features
- **Testing**: Vitest with React Testing Library

### Backend Architecture (FastAPI)

- **Framework**: FastAPI for high-performance async API
- **Server**: Uvicorn ASGI server with auto-reload
- **CORS**: Configured middleware for cross-origin requests
- **Documentation**: Auto-generated Swagger UI and ReDoc
- **Testing**: pytest with FastAPI TestClient

## Development Setup

### Prerequisites

- **Docker Desktop**: 20.10+ (includes Docker Compose)
- **Git**: Any recent version
- **Code Editor**: VS Code recommended (with extensions)

### Recommended VS Code Extensions

- **Python**: ms-python.python
- **Pylance**: ms-python.vscode-pylance
- **ESLint**: dbaeumer.vscode-eslint
- **ES7+ React/Redux/React-Native snippets**: dsznajder.es7-react-js-snippets
- **Docker**: ms-azuretools.vscode-docker

### Initial Setup

```bash
# Clone repository
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
git checkout feature/JIRA-777/fullstack-app

# Start services
docker compose up

# Verify services are running
curl http://localhost:8000/health
curl http://localhost:3000
```

## Code Structure

### Backend Code Organization

```
backend/
├── main.py              # FastAPI application with routes
├── test_main.py         # Comprehensive test suite
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container configuration
└── .dockerignore        # Files to exclude from build
```

### Frontend Code Organization

```
frontend/
├── src/
│   ├── App.jsx          # Main React component
│   ├── App.css          # Styling with green theme
│   ├── App.test.jsx     # Component tests
│   ├── main.jsx         # Application entry point
│   └── setupTests.js    # Test configuration
├── index.html           # HTML template
├── package.json         # Dependencies and scripts
├── vite.config.js       # Vite configuration
├── Dockerfile           # Container configuration
└── .dockerignore        # Files to exclude from build
```

## Development Workflow

### Making Changes

#### Frontend Changes

1. Edit files in `frontend/src/`
2. Save the file
3. Vite HMR automatically updates browser (no refresh needed)
4. Check browser console for errors

#### Backend Changes

1. Edit `backend/main.py`
2. Save the file
3. Uvicorn automatically reloads server (~1-2 seconds)
4. Check Docker logs for errors: `docker compose logs backend`

### Hot Reload Verification

```bash
# Terminal 1: Watch logs
docker compose logs -f

# Terminal 2: Make code changes
echo "// Test change" >> frontend/src/App.jsx

# Observe HMR update in Terminal 1
```

## Testing

### Backend Testing

#### Run All Tests

```bash
docker compose exec backend pytest test_main.py -v
```

#### Run Specific Test

```bash
docker compose exec backend pytest test_main.py::TestHealthEndpoint::test_health_returns_200 -v
```

#### Run with Coverage

```bash
docker compose exec backend pytest test_main.py --cov=main --cov-report=html
```

#### Test Categories

- **Health Endpoint Tests**: Verify health check functionality
- **Hello Endpoint Tests**: Validate API response structure and content
- **CORS Tests**: Ensure cross-origin requests work correctly
- **Error Handling Tests**: Test 404 and 405 responses
- **Performance Tests**: Verify response time < 100ms

### Frontend Testing

#### Run All Tests

```bash
docker compose exec frontend npm test
```

#### Run Tests in Watch Mode

```bash
docker compose exec frontend npm test -- --watch
```

#### Run Tests with UI

```bash
docker compose exec frontend npm run test:ui
```

#### Test Categories

- **Rendering Tests**: Verify component structure
- **Interaction Tests**: Test button clicks and user events
- **API Integration Tests**: Mock fetch and test responses
- **Error Handling Tests**: Validate error states
- **Accessibility Tests**: Check ARIA attributes and roles

### Integration Testing

```bash
# Start all services
docker compose up -d

# Wait for services to be ready
sleep 10

# Test backend health
curl -f http://localhost:8000/health

# Test backend API
curl http://localhost:8000/api/hello

# Test frontend
curl -f http://localhost:3000

# Stop services
docker compose down
```

## Debugging

### Backend Debugging

#### View Logs

```bash
# All logs
docker compose logs backend

# Follow logs
docker compose logs -f backend

# Last 50 lines
docker compose logs --tail=50 backend
```

#### Interactive Python Shell

```bash
docker compose exec backend python
```

#### Test API Manually

```bash
# Health check
curl http://localhost:8000/health

# API endpoint
curl http://localhost:8000/api/hello

# OpenAPI documentation
open http://localhost:8000/docs
```

### Frontend Debugging

#### Browser DevTools

1. Open http://localhost:3000
2. Press F12 to open DevTools
3. Check Console tab for errors
4. Check Network tab for API calls

#### View Logs

```bash
docker compose logs -f frontend
```

#### Check Build Output

```bash
docker compose exec frontend npm run build
```

## Performance Optimization

### Docker Build Optimization

#### Use BuildKit

```bash
DOCKER_BUILDKIT=1 docker compose build
```

#### Clean Build

```bash
docker compose build --no-cache
```

#### Remove Unused Resources

```bash
docker system prune -a
```

### Vite Optimization

- Vite automatically optimizes in production builds
- Use `npm run build` to create optimized production bundle
- Check bundle size: `du -sh frontend/dist`

### FastAPI Optimization

- FastAPI is already highly optimized
- Use async/await for I/O operations
- Enable gzip compression in production

## Common Issues

### Port Already in Use

```bash
# Find process using port
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Change port in docker-compose.yml
ports:
  - "3001:3000"  # Use 3001 instead
```

### Hot Reload Not Working

```bash
# Rebuild containers
docker compose down
docker compose build --no-cache
docker compose up
```

### Backend Not Responding

```bash
# Check backend health
curl http://localhost:8000/health

# Check logs
docker compose logs backend

# Restart backend
docker compose restart backend
```

### Frontend Build Fails

```bash
# Clear node_modules
docker compose down
rm -rf frontend/node_modules
docker compose build --no-cache frontend
docker compose up
```

### Tests Failing

```bash
# Backend tests
docker compose exec backend pytest test_main.py -v --tb=short

# Frontend tests
docker compose exec frontend npm test -- --run

# Check for syntax errors
docker compose exec backend python -m py_compile main.py
docker compose exec frontend npm run lint
```

## Best Practices

### Code Style

- **Python**: Follow PEP 8 style guide
- **JavaScript**: Follow Airbnb style guide
- **Comments**: Write clear, concise comments for complex logic
- **Docstrings**: Document all functions and classes

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes and commit
git add .
git commit -m "feat: Add new feature"

# Push and create PR
git push origin feature/your-feature
```

### Commit Messages

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `style:` Code formatting
- `chore:` Maintenance

## Resources

### Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Docker Documentation](https://docs.docker.com/)

### Tools

- [Postman](https://www.postman.com/) - API testing
- [React DevTools](https://react.dev/learn/react-developer-tools) - React debugging
- [HTTPie](https://httpie.io/) - Command-line HTTP client

---

**Happy Coding! 🚀**
