# 🌟 Yellow Theme Hello World Fullstack Application

A minimal, production-ready fullstack application demonstrating modern web development practices with a vibrant yellow-themed UI. This project showcases the integration of a React frontend with a FastAPI backend, containerized with Docker and automated with CI/CD pipelines.

![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=flat&logo=react&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=flat&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=flat&logo=github-actions&logoColor=white)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [API Endpoints](#-api-endpoints)
- [Development](#-development)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Technology Stack](#-technology-stack)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- 🎨 **Yellow-Themed React Frontend** - Modern, responsive UI with vibrant yellow color scheme
- ⚡ **FastAPI Backend** - High-performance Python REST API with automatic documentation
- 🐳 **Docker Compose Orchestration** - One-command deployment with service networking
- 🔄 **Hot Reload Development** - Instant feedback with live code reloading for both frontend and backend
- 🚀 **CI/CD Pipeline** - Automated testing and validation with GitHub Actions
- 📝 **API Documentation** - Interactive Swagger/OpenAPI documentation at `/docs`
- 💚 **Health Checks** - Built-in health monitoring endpoints
- 🔧 **CORS Enabled** - Properly configured cross-origin resource sharing

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Compose Network                   │
│                                                              │
│  ┌──────────────────┐         ┌─────────────────────┐      │
│  │                  │         │                     │      │
│  │    Frontend      │────────▶│      Backend        │      │
│  │  (React + Vite)  │  HTTP   │  (FastAPI + Python) │      │
│  │                  │         │                     │      │
│  │   Port: 3000     │         │    Port: 8000       │      │
│  │                  │         │                     │      │
│  └──────────────────┘         └─────────────────────┘      │
│          │                              │                   │
└──────────┼──────────────────────────────┼───────────────────┘
           │                              │
           ▼                              ▼
    http://localhost:3000          http://localhost:8000
    (User Interface)               (REST API + Docs)
```

### Component Overview:

- **Frontend**: React 18 with Vite bundler, serving the yellow-themed UI
- **Backend**: FastAPI REST API with automatic OpenAPI documentation
- **Communication**: Frontend makes HTTP requests to backend API endpoints
- **Networking**: Docker Compose internal network for service-to-service communication
- **Development**: Both services support hot reload for rapid development

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker** (version 20.10 or higher)
  - [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** (version 2.0 or higher)
  - Usually included with Docker Desktop
  - [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Git** (for cloning the repository)
  - [Install Git](https://git-scm.com/downloads)
- **Available Ports**:
  - Port 3000 (Frontend)
  - Port 8000 (Backend)

### Optional (for local development without Docker):

- **Node.js** 18+ and npm
- **Python** 3.11+ and pip

---

## 🚀 Quick Start

Get the application running in less than 2 minutes!

### 1. Clone the Repository

```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output.git
cd ab-sdlc-agent-ai-output
git checkout feature/JIRA-888/fullstack-app
```

### 2. Start All Services

```bash
docker compose up
```

This single command will:
- Build Docker images for frontend and backend
- Start both services with hot reload enabled
- Set up networking between services
- Make the application accessible on your localhost

### 3. Access the Application

Once the services are running (you'll see logs indicating successful startup), open your browser:

| Service | URL | Description |
|---------|-----|-------------|
| 🎨 **Frontend** | http://localhost:3000 | Yellow-themed React UI |
| 🔧 **Backend API** | http://localhost:8000 | REST API endpoints |
| 📖 **API Docs** | http://localhost:8000/docs | Interactive Swagger UI |
| 📋 **Alternative Docs** | http://localhost:8000/redoc | ReDoc API documentation |

### 4. Stop the Application

```bash
# Press Ctrl+C in the terminal, then:
docker compose down
```

---

## 🔌 API Endpoints

### `GET /api/hello`

Returns a greeting message with the current UTC timestamp.

**Request:**
```bash
curl http://localhost:8000/api/hello
```

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:45.123456Z"
}
```

**Response Fields:**
- `message` (string): Greeting message from the backend
- `timestamp` (string): Current UTC time in ISO-8601 format

---

### `GET /health`

Health check endpoint for monitoring service status.

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy"
}
```

**Response Fields:**
- `status` (string): Health status of the service (always "healthy" when responding)

**Use Cases:**
- Docker health checks
- Load balancer health probes
- Monitoring systems
- Deployment verification

---

## 💻 Development

### Running Without Docker

Sometimes you may want to run services locally without Docker for debugging or development.

#### Backend Development

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at http://localhost:8000 with auto-reload enabled.

#### Frontend Development

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at http://localhost:3000 with hot module replacement (HMR).

#### Environment Variables

**Backend** (`backend/.env`):
```env
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

**Frontend** (`frontend/.env`):
```env
VITE_API_URL=http://localhost:8000
```

### Hot Reload

Both frontend and backend support hot reload in development mode:

- **Frontend**: Vite HMR updates the browser instantly when you save changes to React components
- **Backend**: Uvicorn auto-reloads the server when you modify Python files

### Code Formatting and Linting

**Frontend:**
```bash
cd frontend
npm run lint          # Check for linting errors
```

**Backend:**
```bash
cd backend
# Add your preferred linting tools (flake8, black, etc.)
```

---

## 📁 Project Structure

```
ab-sdlc-agent-ai-output/
├── frontend/                      # React frontend application
│   ├── src/
│   │   ├── App.jsx               # Main React component
│   │   ├── App.css               # Yellow theme styles
│   │   ├── main.jsx              # React entry point
│   │   └── index.css             # Global styles
│   ├── index.html                # HTML template
│   ├── package.json              # Node.js dependencies
│   ├── vite.config.js            # Vite configuration
│   ├── Dockerfile                # Frontend container image
│   └── .eslintrc.cjs             # ESLint configuration
│
├── backend/                       # FastAPI backend application
│   ├── main.py                   # FastAPI application & routes
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile                # Backend container image
│
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions CI/CD pipeline
│
├── docker-compose.yml            # Multi-container orchestration
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
└── README.md                     # This file
```

### Key Files Explained

| File | Purpose |
|------|---------|
| `frontend/src/App.jsx` | Main React component with yellow theme and API integration |
| `frontend/vite.config.js` | Vite bundler configuration with dev server settings |
| `backend/main.py` | FastAPI application with API routes and CORS configuration |
| `docker-compose.yml` | Defines services, networks, and volumes for local development |
| `.github/workflows/ci.yml` | Automated testing and validation pipeline |

---

## 🧪 Testing

### Manual Testing

#### 1. Verify Frontend

1. Open http://localhost:3000 in your browser
2. Check that the yellow-themed UI loads
3. Click the "Fetch Message from Backend" button
4. Verify that the greeting message and timestamp appear

#### 2. Test Backend API

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected: {"status":"healthy"}

# Test hello endpoint
curl http://localhost:8000/api/hello

# Expected: {"message":"Hello World from Backend!","timestamp":"..."}
```

#### 3. Test API Documentation

Visit http://localhost:8000/docs and:
1. Expand the `/api/hello` endpoint
2. Click "Try it out"
3. Click "Execute"
4. Verify the response

### Integration Testing

Test the full stack integration:

```bash
# Start all services
docker compose up -d

# Wait for services to be ready
sleep 5

# Test backend health
curl -f http://localhost:8000/health || echo "Backend health check failed"

# Test backend API
curl -f http://localhost:8000/api/hello || echo "Backend API failed"

# Test frontend (should return HTML)
curl -f http://localhost:3000 || echo "Frontend failed"

# Cleanup
docker compose down
```

### Automated Testing

The CI/CD pipeline automatically runs tests on every pull request. See [CI/CD Pipeline](#-cicd-pipeline) section for details.

---

## 🚀 CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment.

### Pipeline Overview

**Workflow File:** `.github/workflows/ci.yml`

**Triggers:**
- Pull requests to `main` or `master` branch
- Pushes to `main` or `master` branch

### Pipeline Stages

```
┌─────────────────────────────────────────────────────────┐
│  1. Backend Validation                                   │
│     - Check Python syntax                               │
│     - Verify FastAPI application                        │
│     - Validate requirements.txt                         │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  2. Frontend Build                                       │
│     - Install Node.js dependencies                      │
│     - Build production bundle                           │
│     - Verify build artifacts                            │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  3. Docker Build Validation                              │
│     - Build backend Docker image                        │
│     - Build frontend Docker image                       │
│     - Verify successful builds                          │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  4. Docker Compose Validation                            │
│     - Validate docker-compose.yml syntax                │
│     - Test service startup                              │
│     - Verify service health                             │
└─────────────────────────────────────────────────────────┘
```

### Viewing Pipeline Results

1. Go to the repository on GitHub
2. Click the "Actions" tab
3. Select a workflow run to see detailed logs
4. Each job shows individual step results

### Pipeline Badge

Add this to your pull request or documentation to show build status:

```markdown
![CI Pipeline](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output/actions/workflows/ci.yml/badge.svg?branch=feature/JIRA-888/fullstack-app)
```

---

## 🛠️ Technology Stack

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.2.0 | UI framework for building interactive interfaces |
| **Vite** | 5.0.0 | Next-generation frontend build tool and dev server |
| **@vitejs/plugin-react** | 4.2.0 | Official React plugin for Vite |

**Key Features:**
- Component-based architecture
- Virtual DOM for efficient updates
- JSX syntax for declarative UI
- Hot Module Replacement (HMR)

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11 | Programming language |
| **FastAPI** | 0.109.0 | Modern, fast web framework for building APIs |
| **Uvicorn** | 0.27.0 | Lightning-fast ASGI server |

**Key Features:**
- Automatic OpenAPI documentation
- Type hints for validation
- Async/await support
- High performance (comparable to Node.js)

### Infrastructure

| Technology | Purpose |
|------------|---------|
| **Docker** | Containerization platform |
| **Docker Compose** | Multi-container orchestration |
| **GitHub Actions** | CI/CD automation |
| **Node.js** 20 Alpine | Lightweight base image for frontend |
| **Python** 3.11 Slim | Minimal base image for backend |

### Development Tools

- **ESLint** - JavaScript linting
- **Git** - Version control
- **npm** - Node package manager
- **pip** - Python package manager

---

## 🔧 Troubleshooting

### Port Already in Use

**Problem:** `Error: bind: address already in use`

**Solution:**
```bash
# Find process using the port (Linux/Mac)
lsof -i :3000  # or :8000
kill -9 <PID>

# Find process using the port (Windows)
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use different ports in docker-compose.yml:
ports:
  - "3001:3000"  # Frontend
  - "8001:8000"  # Backend
```

### Docker Build Failures

**Problem:** Docker build fails with dependency errors

**Solution:**
```bash
# Clear Docker cache and rebuild
docker compose down
docker system prune -a
docker compose build --no-cache
docker compose up
```

### CORS Errors

**Problem:** Frontend shows CORS errors in browser console

**Solution:**
1. Verify backend CORS configuration in `backend/main.py`:
   ```python
   allow_origins=["http://localhost:3000"]
   ```
2. Ensure frontend is accessing the correct backend URL
3. Check that both services are running
4. Clear browser cache and reload

### Frontend Can't Connect to Backend

**Problem:** Frontend shows "Failed to fetch" or connection errors

**Solution:**
1. Verify backend is running:
   ```bash
   curl http://localhost:8000/health
   ```
2. Check Docker Compose logs:
   ```bash
   docker compose logs backend
   ```
3. Ensure services are on the same Docker network
4. Verify API URL in frontend code matches backend port

### Hot Reload Not Working

**Problem:** Changes to code don't reflect in the browser/app

**Solution:**

**Frontend:**
```bash
# Ensure volume mounts are correct in docker-compose.yml
volumes:
  - ./frontend:/app
  - /app/node_modules  # This line is crucial
```

**Backend:**
```bash
# Verify uvicorn reload flag in Dockerfile
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
```

### Container Exits Immediately

**Problem:** Service container starts then exits

**Solution:**
```bash
# Check container logs
docker compose logs <service-name>

# Common issues:
# - Missing dependencies
# - Syntax errors in code
# - Port conflicts
# - Missing environment variables

# Rebuild with verbose output
docker compose up --build
```

### Permission Denied Errors

**Problem:** Permission errors when mounting volumes

**Solution (Linux/Mac):**
```bash
# Fix ownership of project files
sudo chown -R $USER:$USER .

# Or run Docker with user permissions
docker compose run --user $(id -u):$(id -g) <service>
```

### Getting Help

If you encounter issues not covered here:

1. Check Docker Compose logs: `docker compose logs`
2. Check individual service logs: `docker compose logs <service-name>`
3. Review the GitHub Actions CI/CD logs for similar errors
4. Verify your Docker and Docker Compose versions meet requirements
5. Check for open issues in the repository

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Workflow

1. **Fork the Repository**
   ```bash
   # Fork via GitHub UI, then clone your fork
   git clone https://github.com/YOUR-USERNAME/ab-sdlc-agent-ai-output.git
   cd ab-sdlc-agent-ai-output
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. **Make Your Changes**
   - Write clean, readable code
   - Follow existing code style
   - Add comments where necessary
   - Test your changes locally

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: Add your feature description"
   ```

   **Commit Message Convention:**
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Code style changes (formatting, etc.)
   - `refactor:` - Code refactoring
   - `test:` - Adding or updating tests
   - `chore:` - Maintenance tasks

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a PR via GitHub UI.

### Pull Request Guidelines

- ✅ Provide clear description of changes
- ✅ Reference any related issues
- ✅ Ensure CI pipeline passes
- ✅ Update documentation if needed
- ✅ Keep PRs focused and atomic

### Code Review Process

1. Automated CI checks must pass
2. At least one maintainer review required
3. Address review feedback
4. Maintainer merges approved PRs

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

```
Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🌟 Acknowledgments

- Built with modern web development best practices
- Inspired by microservices architecture patterns
- Thanks to the React, FastAPI, and Docker communities

---

## 📞 Support & Contact

- **Issues:** [GitHub Issues](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output/issues)
- **Pull Requests:** [GitHub PRs](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output/pulls)
- **Documentation:** [Project Wiki](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output/wiki)

---

<div align="center">

**Made with ❤️ and ☕**

⭐ **Star this repository if you find it helpful!** ⭐

</div>
