# Green Theme Hello World Fullstack Application

A minimal demonstration fullstack application featuring a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose for easy local development.

## Overview

This project showcases a simple yet complete fullstack application architecture with:

- **Frontend**: React 18+ with Vite for fast development and HMR (Hot Module Replacement)
- **Backend**: Python 3.11+ with FastAPI for modern async API development
- **Orchestration**: Docker Compose for seamless multi-service development
- **Theme**: Clean, centered green-themed UI design
- **Purpose**: Minimal demo application demonstrating fullstack architecture patterns

The application demonstrates client-server communication, containerization, and development best practices in a straightforward, easy-to-understand implementation.

## Features

✨ **Frontend Capabilities**:
- Green-themed React application with centered, responsive layout
- Interactive button to fetch data from backend
- Real-time message display with timestamps
- Vite-powered development with instant HMR
- Clean, modern CSS styling with custom green color scheme

🚀 **Backend Capabilities**:
- FastAPI REST API with two endpoints (`/api/hello`, `/health`)
- Automatic API documentation (Swagger UI)
- CORS configured for local development
- Uvicorn server with hot reload for rapid development
- Health check endpoint for monitoring

🐳 **Docker Integration**:
- Single-command startup with Docker Compose
- Hot reload enabled for both frontend and backend services
- Isolated service containers with proper networking
- Volume mounts for development workflow
- Easy service scaling and management

## Prerequisites

Before running this application, ensure you have the following installed:

- **Docker**: Version 20.10 or higher ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose**: Version 2.0 or higher (usually included with Docker Desktop)
- **Git**: For cloning the repository ([Install Git](https://git-scm.com/downloads))
- **Available Ports**: Ensure ports 3000 (frontend) and 8000 (backend) are not in use

To verify your installations:
```bash
docker --version
docker compose version
git --version
```

## Project Structure

```
project-root/
├── frontend/              # React + Vite application
│   ├── src/              # React source code
│   │   ├── App.jsx       # Main application component
│   │   ├── App.css       # Green theme styling
│   │   └── main.jsx      # Application entry point
│   ├── public/           # Static assets
│   ├── index.html        # HTML template
│   ├── package.json      # Frontend dependencies
│   ├── vite.config.js    # Vite configuration
│   └── Dockerfile        # Frontend container definition
│
├── backend/              # FastAPI application
│   ├── main.py           # API endpoints and application logic
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Backend container definition
│
├── .github/
│   └── workflows/        # CI/CD pipeline configurations
│       └── ci.yml        # Continuous integration workflow
│
├── docker-compose.yml    # Multi-service orchestration
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
└── README.md            # This file
```

## Quick Start

Get the application running in just a few commands:

### 1. Clone the Repository

```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output.git
cd ab-sdlc-agent-ai-output
```

### 2. Checkout the Feature Branch

```bash
git checkout feature/JIRA-777/fullstack-app
```

### 3. Start the Application

```bash
docker compose up
```

This command will:
- Build Docker images for frontend and backend
- Start both services with hot reload enabled
- Set up networking between services
- Mount source code for development

### 4. Access the Application

- **Frontend**: Open your browser to [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)

You should see the green-themed frontend with a "Get Message from Backend" button.

## Usage Instructions

### Starting Services

Start all services in the foreground (with logs):
```bash
docker compose up
```

Start services in the background (detached mode):
```bash
docker compose up -d
```

### Stopping Services

Stop services gracefully (containers remain):
```bash
docker compose stop
```

Stop and remove containers:
```bash
docker compose down
```

Stop and remove containers, volumes, and images:
```bash
docker compose down --volumes --rmi all
```

### Viewing Logs

View logs for all services:
```bash
docker compose logs -f
```

View logs for a specific service:
```bash
docker compose logs -f frontend
docker compose logs -f backend
```

### Rebuilding Services

Rebuild and restart after code changes:
```bash
docker compose up --build
```

Rebuild specific service:
```bash
docker compose build frontend
docker compose up frontend
```

### Accessing Service Shells

Access backend container shell:
```bash
docker compose exec backend sh
```

Access frontend container shell:
```bash
docker compose exec frontend sh
```

## Manual Testing

### Testing the Frontend

1. Navigate to [http://localhost:3000](http://localhost:3000)
2. You should see:
   - Green-themed page with centered content
   - Application title
   - "Get Message from Backend" button
3. Click the button
4. Verify that a message with timestamp appears below the button
5. Click multiple times to verify new timestamps

### Testing the Backend Directly

Test the hello endpoint:
```bash
curl http://localhost:8000/api/hello
```

Expected response:
```json
{
  "message": "Hello from the backend!",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy"
}
```

### Testing with Browser DevTools

1. Open browser DevTools (F12)
2. Go to Network tab
3. Click "Get Message from Backend" button
4. Inspect the API call:
   - Request URL: `http://localhost:8000/api/hello`
   - Method: GET
   - Status: 200
   - Response: JSON with message and timestamp

## API Endpoints

### GET /api/hello

Returns a greeting message with current timestamp.

**Request:**
```bash
curl -X GET http://localhost:8000/api/hello
```

**Response:**
```json
{
  "message": "Hello from the backend!",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

**Status Codes:**
- `200 OK`: Successful response

---

### GET /health

Health check endpoint for monitoring service availability.

**Request:**
```bash
curl -X GET http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy"
}
```

**Status Codes:**
- `200 OK`: Service is healthy and operational

---

### Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

Use these interfaces to explore and test API endpoints directly in your browser.

## Development

### Hot Reload Configuration

Both frontend and backend are configured with hot reload for efficient development:

**Frontend (Vite)**:
- Changes to `.jsx`, `.css`, or `.html` files trigger instant HMR
- No page refresh required for most changes
- Fast rebuild times (<100ms typically)

**Backend (Uvicorn)**:
- Changes to `.py` files trigger automatic server restart
- Uvicorn runs with `--reload` flag
- Server restarts in ~1-2 seconds

### Making Code Changes

1. Edit files in `frontend/src/` or `backend/` directories
2. Save your changes
3. Watch the console for hot reload confirmation
4. Refresh browser if needed (frontend usually auto-updates)

### Installing Dependencies

**Frontend** (CRITICAL - Read Carefully):

⚠️ **IMPORTANT**: Always use `npm install` (NOT `npm ci`)

```bash
cd frontend
npm install <package-name>
```

This adds the package to `package.json`. Lock files (package-lock.json) are gitignored and should NOT be committed.

**Backend**:

```bash
cd backend
pip install <package-name>
pip freeze > requirements.txt  # Update requirements
```

### Running Tests Locally

**Frontend Tests**:
```bash
cd frontend
npm install
npm test
```

**Backend Tests**:
```bash
cd backend
pip install -r requirements.txt
pytest tests/
```

### Development Workflow Best Practices

1. **Always use `npm install`** (never `npm ci`) for frontend dependencies
2. **Never commit lock files** (package-lock.json, yarn.lock, etc.)
3. **Keep docker-compose running** during development for instant feedback
4. **Use browser DevTools** to debug API calls and React components
5. **Check logs** with `docker compose logs -f` if issues arise
6. **Rebuild images** after changing Dockerfiles or dependency files

## Troubleshooting

### Port Already in Use

**Problem**: Error message like "port 3000 is already allocated"

**Solution**:
```bash
# Find process using the port
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill the process or use different ports in docker-compose.yml
```

### CORS Errors

**Problem**: Browser console shows CORS policy errors

**Solution**:
- Verify backend CORS configuration in `backend/main.py`
- Ensure `http://localhost:3000` is in allowed origins
- Check that backend is running on port 8000
- Try hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

### Container Issues

**Problem**: Services won't start or behave unexpectedly

**Solution**:
```bash
# Complete reset
docker compose down --volumes
docker compose build --no-cache
docker compose up

# Check container status
docker compose ps

# Inspect specific service
docker compose logs backend
```

### Frontend Not Loading

**Problem**: Blank page or "Cannot connect" error

**Solution**:
1. Verify frontend container is running: `docker compose ps`
2. Check frontend logs: `docker compose logs frontend`
3. Ensure port 3000 is accessible
4. Try rebuilding: `docker compose up --build frontend`

### Backend API Not Responding

**Problem**: API calls fail or timeout

**Solution**:
1. Check backend is healthy: `curl http://localhost:8000/health`
2. Review backend logs: `docker compose logs backend`
3. Verify backend container is running: `docker compose ps`
4. Check Python errors in logs

### Hot Reload Not Working

**Problem**: Changes not reflected after saving files

**Solution**:
- **Frontend**: Ensure volume mounts are correct in docker-compose.yml
- **Backend**: Check that source files are in `/app` directory
- Try restarting services: `docker compose restart`
- Check file permissions on mounted volumes

### Build Failures

**Problem**: Docker build fails with dependency errors

**Solution**:
```bash
# Clean Docker cache
docker builder prune

# Rebuild without cache
docker compose build --no-cache

# Check Dockerfile syntax
docker compose config
```

### View All Container Logs

```bash
# Follow all logs
docker compose logs -f

# Get last 100 lines
docker compose logs --tail=100

# Export logs to file
docker compose logs > debug.log
```

### Get Help

If issues persist:
1. Review Docker Compose logs thoroughly
2. Check GitHub Issues for similar problems
3. Verify all prerequisites are met
4. Try on a fresh clone of the repository

## Tech Stack Details

### Frontend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.x | UI library for component-based development |
| **Vite** | 5.x | Next-generation frontend build tool with instant HMR |
| **Node.js** | 18.x | JavaScript runtime (development only) |
| **CSS3** | - | Styling with custom properties and flexbox |

**Key Libraries**:
- React DOM for rendering
- Vite for build tooling and dev server

**Color Scheme**:
- Primary Green: `#2ecc71` (vibrant green for buttons and highlights)
- Secondary Green: `#27ae60` (darker green for hover states)
- Background: `#f0f0f0` (light gray)
- Text: `#333` (dark gray)

### Backend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11+ | Programming language |
| **FastAPI** | latest | Modern async web framework for APIs |
| **Uvicorn** | latest | ASGI server with hot reload support |
| **Pydantic** | latest | Data validation (included with FastAPI) |

**Key Features**:
- Async/await support for high performance
- Automatic API documentation (OpenAPI/Swagger)
- Type hints with runtime validation
- CORS middleware for cross-origin requests

### Container Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Docker** | 20.10+ | Containerization platform |
| **Docker Compose** | 2.0+ | Multi-container orchestration |
| **Alpine Linux** | latest | Minimal base image for containers |

**Container Configuration**:
- Frontend: `node:18-alpine` base image
- Backend: `python:3.11-slim` base image
- Volume mounts for source code
- Network bridge for service communication

### Development Tools

- **Git**: Version control
- **npm**: Frontend package manager (use `npm install`, NOT `npm ci`)
- **pip**: Python package manager
- **curl**: API testing
- **Browser DevTools**: Frontend debugging

## Demo Mode Notes

This application is designed for **demonstration and learning purposes**:

### What This Application IS

✅ **Educational**: Demonstrates fullstack architecture patterns  
✅ **Minimal**: Focused on core functionality without complexity  
✅ **Development-Ready**: Hot reload and Docker Compose for fast iteration  
✅ **Well-Structured**: Clear separation of concerns (frontend/backend)  
✅ **Docker-First**: Containerized services for consistency  
✅ **API-Documented**: Automatic Swagger documentation  

### What This Application IS NOT

❌ **Production-Ready**: No security hardening, no optimization  
❌ **Feature-Complete**: Intentionally minimal feature set  
❌ **Authenticated**: No user authentication or authorization  
❌ **Persistent**: No database or data persistence  
❌ **Scalable**: Single-instance services, no load balancing  
❌ **Tested**: No comprehensive test suite (infrastructure only)  

### Intentional Limitations

- **No Database**: No data persistence layer (could add PostgreSQL/MongoDB)
- **No Authentication**: No user login or JWT tokens (could add Auth0/Passport)
- **No State Management**: No Redux/Context API (could add for complex state)
- **No Testing**: Minimal test coverage (could add Jest/Pytest)
- **No CI/CD**: Basic GitHub Actions only (could add deployment pipelines)
- **No Logging**: Basic console logging (could add Winston/structlog)
- **No Monitoring**: No APM or metrics (could add Prometheus/Grafana)

### Extending This Application

This demo serves as a foundation. Consider adding:

1. **Database Layer**: PostgreSQL, MongoDB, or Redis
2. **Authentication**: JWT tokens, OAuth 2.0, or session-based auth
3. **State Management**: Redux, Zustand, or React Context
4. **Testing**: Jest, React Testing Library, Pytest, pytest-cov
5. **Logging**: Structured logging with Winston or structlog
6. **Monitoring**: Health checks, metrics, and tracing
7. **Error Handling**: Global error boundaries and API error handling
8. **Validation**: Input validation and sanitization
9. **Security**: HTTPS, rate limiting, input sanitization
10. **Documentation**: API docs, architecture diagrams, ADRs

### Use Cases

Perfect for:
- Learning fullstack development patterns
- Testing Docker Compose workflows
- Demonstrating CI/CD pipelines
- Teaching React + FastAPI integration
- Quick prototyping and experimentation

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

Permission is hereby granted, free of charge, to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this software, subject to including the copyright notice and permission notice in all copies or substantial portions of the software.

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.**

---

## Additional Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## Support

For issues, questions, or contributions:

1. **Check Troubleshooting Section**: Most common issues are documented above
2. **Review Logs**: Use `docker compose logs` to diagnose problems
3. **GitHub Issues**: Report bugs or request features
4. **Documentation**: Refer to official docs for each technology

---

**Happy Coding! 🚀💚**

Built with ❤️ using React, FastAPI, and Docker