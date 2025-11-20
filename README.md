# Hello World Fullstack Application

[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2+-blue.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.0+-purple.svg)](https://vitejs.dev/)

A modern fullstack application demonstrating containerized development with Docker and Docker Compose. This project features a FastAPI backend and a Vite + React frontend, fully orchestrated for seamless local development.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [Development Workflow](#development-workflow)
- [API Documentation](#api-documentation)
- [Docker Configuration](#docker-configuration)
- [Success Criteria](#success-criteria)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This application demonstrates best practices for containerized fullstack development:

- **Backend**: FastAPI-based REST API with CORS support
- **Frontend**: React application built with Vite for fast HMR (Hot Module Replacement)
- **Orchestration**: Docker Compose for multi-container management
- **Development**: Hot reload enabled for both services for rapid development

## 📁 Project Structure

```
ab-sdlc-agent-ai-output/
├── backend/
│   ├── Dockerfile              # Backend container configuration
│   ├── main.py                 # FastAPI application
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── Dockerfile              # Frontend container configuration
│   ├── package.json            # Node.js dependencies
│   ├── vite.config.js          # Vite configuration
│   ├── index.html              # HTML entry point
│   └── src/                    # React source code
│       ├── main.jsx            # React entry point
│       ├── App.jsx             # Main App component
│       └── App.css             # Application styles
├── docker-compose.yml          # Multi-container orchestration
└── README.md                   # This file
```

## ✅ Prerequisites

Before running this application, ensure you have the following installed:

- **Docker**: Version 20.10 or higher
  - [Install Docker Desktop](https://www.docker.com/products/docker-desktop) (includes Docker Compose)
  - Verify installation: `docker --version`

- **Docker Compose**: Version 2.0 or higher
  - Included with Docker Desktop
  - Verify installation: `docker compose version`

- **Git**: For cloning the repository
  - Verify installation: `git --version`

### System Requirements

- **OS**: Windows 10/11, macOS 10.15+, or Linux
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: At least 2GB free

## 🛠️ Technology Stack

### Backend

- **Framework**: FastAPI 0.100+
- **Server**: Uvicorn with auto-reload
- **Language**: Python 3.11
- **API Style**: RESTful
- **CORS**: Configured for localhost:3000

### Frontend

- **Framework**: React 18.2+
- **Build Tool**: Vite 5.0+
- **Language**: JavaScript (ES6+)
- **Styling**: CSS3

### Infrastructure

- **Containerization**: Docker
- **Orchestration**: Docker Compose 3.8
- **Networking**: Bridge network (hello-network)
- **Volumes**: Bind mounts for hot reload

## 🚀 Quick Start

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
- Build Docker images for both services (first time only)
- Create containers for backend and frontend
- Set up networking between services
- Start both services with hot reload enabled

**Expected Output:**
```
✅ Network hello-network created
✅ Container hello-backend started
✅ Container hello-frontend started
```

**Services should start within 10 seconds.**

### 4. Access the Application

- **Frontend**: [http://localhost:3000](http://localhost:3000)
  - Interactive React UI
  - Hot reload enabled

- **Backend API**: [http://localhost:8000](http://localhost:8000)
  - FastAPI root endpoint
  - Returns API information

- **API Health Check**: [http://localhost:8000/health](http://localhost:8000/health)
  - Returns service health status
  - Used for container health monitoring

- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
  - Auto-generated Swagger UI
  - Interactive API testing

### 5. Stop the Application

```bash
# Stop and remove containers (keeps images)
docker compose down

# Stop, remove containers, and remove volumes
docker compose down -v

# Stop, remove everything including images
docker compose down --rmi all -v
```

## 💻 Development Workflow

### Hot Reload (Live Development)

Both services support hot reload for rapid development:

#### Backend Changes

1. Edit any Python file in `backend/`
2. Uvicorn automatically detects changes
3. Server reloads within 1-2 seconds
4. No need to restart containers

**Example:**
```python
# Edit backend/main.py
@app.get("/api/hello")
async def get_hello():
    return {
        "message": "Hello World - Updated!",  # Change this
        "timestamp": datetime.now().isoformat()
    }
```

#### Frontend Changes

1. Edit any file in `frontend/src/`
2. Vite HMR updates browser instantly
3. Changes reflect in < 1 second
4. Browser state preserved

**Example:**
```jsx
// Edit frontend/src/App.jsx
function App() {
  return (
    <div className="App">
      <h1>Hello World - Updated!</h1>  {/* Change this */}
    </div>
  )
}
```

### Container Management

```bash
# View running containers
docker compose ps

# View logs (all services)
docker compose logs

# View logs (specific service)
docker compose logs backend
docker compose logs frontend

# Follow logs in real-time
docker compose logs -f

# Restart a specific service
docker compose restart backend

# Rebuild after dependency changes
docker compose up --build

# Run in detached mode (background)
docker compose up -d
```

### Accessing Container Shell

```bash
# Backend shell
docker compose exec backend /bin/bash

# Frontend shell
docker compose exec frontend /bin/sh

# Run commands without entering shell
docker compose exec backend python -c "import sys; print(sys.version)"
docker compose exec frontend npm list
```

## 📚 API Documentation

### Endpoints

#### GET `/api/hello`

Returns a hello world message with timestamp.

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

**Status Codes:**
- `200 OK`: Success

#### GET `/health`

Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy"
}
```

**Status Codes:**
- `200 OK`: Service is healthy

#### GET `/`

Root endpoint with API information.

**Response:**
```json
{
  "title": "Hello World API",
  "version": "1.0.0",
  "description": "A simple FastAPI backend"
}
```

### CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000` (Frontend development server)

All HTTP methods and headers are allowed.

## 🐳 Docker Configuration

### Backend Dockerfile

**Key Features:**
- Base: `python:3.11-slim`
- Optimized layer caching
- Hot reload enabled
- Port: 8000

**Build Command:**
```bash
cd backend
docker build -t hello-backend .
```

### Frontend Dockerfile

**Key Features:**
- Base: `node:18-alpine`
- Vite dev server with HMR
- Host binding for Docker
- Port: 3000

**Build Command:**
```bash
cd frontend
docker build -t hello-frontend .
```

### Docker Compose Features

- **Networking**: Shared bridge network (`hello-network`)
- **Service Dependencies**: Frontend waits for backend
- **Volume Mounts**: 
  - `./backend:/app` - Backend hot reload
  - `./frontend:/app` - Frontend hot reload
  - `/app/node_modules` - Prevent overwriting node_modules
- **Environment Variables**: 
  - `VITE_API_URL`: Backend API URL
  - `PYTHONUNBUFFERED`: Python output to terminal
- **Health Checks**: Backend health monitoring
- **Restart Policy**: `unless-stopped` for reliability

## ✅ Success Criteria Checklist

Verify your setup meets all acceptance criteria:

- [ ] `docker compose up` starts both services successfully
- [ ] Services start within 10 seconds
- [ ] Frontend accessible at [http://localhost:3000](http://localhost:3000)
- [ ] Backend accessible at [http://localhost:8000](http://localhost:8000)
- [ ] Health check returns healthy at [http://localhost:8000/health](http://localhost:8000/health)
- [ ] Hot reload works for backend (edit `backend/main.py`)
- [ ] Hot reload works for frontend (edit `frontend/src/App.jsx`)
- [ ] Volume mounts configured correctly (changes persist)
- [ ] Frontend can communicate with backend API
- [ ] `docker compose down` stops services cleanly
- [ ] No port conflicts with existing services
- [ ] Container logs show no errors

## 🔧 Troubleshooting

### Port Already in Use

**Error:** `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solution:**
```bash
# Find process using the port
lsof -i :3000

# Kill the process (macOS/Linux)
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "3001:3000"  # Use port 3001 instead
```

### Containers Not Starting

**Solution:**
```bash
# Check container status
docker compose ps

# View detailed logs
docker compose logs backend
docker compose logs frontend

# Rebuild from scratch
docker compose down -v
docker compose build --no-cache
docker compose up
```

### Hot Reload Not Working

**Backend:**
- Ensure volume mount is correct in `docker-compose.yml`
- Check file permissions (especially on Linux)
- Verify uvicorn is running with `--reload` flag

**Frontend:**
- Ensure node_modules volume is set correctly
- Clear browser cache
- Check Vite config has proper host binding

### Cannot Connect to Backend from Frontend

**Solution:**
- Verify `VITE_API_URL` is set correctly
- Check both services are on same network
- Ensure CORS is configured in backend
- Use `docker compose logs backend` to check for errors

### Permission Denied Errors (Linux)

**Solution:**
```bash
# Fix ownership of mounted volumes
sudo chown -R $USER:$USER backend frontend

# Or run with sudo (not recommended)
sudo docker compose up
```

### Docker Compose Command Not Found

**Solution:**
- Update Docker Desktop to latest version
- Or use legacy command: `docker-compose up`

## 📝 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ using Docker, FastAPI, and React**