# Green Theme Hello World Fullstack Application

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![React](https://img.shields.io/badge/React-18.2-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

A simple fullstack demonstration application featuring a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose. This application serves as a reference implementation for fullstack development patterns and containerized deployment.

## 🎯 Features

- **Modern React Frontend**: Built with React 18+ and Vite for fast development
- **Green Theme Design**: Beautiful, responsive UI with custom green color scheme
- **FastAPI Backend**: High-performance Python backend with RESTful API
- **Docker Compose**: One-command deployment for both services
- **Hot Module Replacement**: Instant updates during development
- **Comprehensive Testing**: Full test coverage with pytest and Vitest
- **CORS Configured**: Secure cross-origin communication
- **Responsive Design**: Works on all devices (320px - 1920px)

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Technology Stack](#technology-stack)

## 🔧 Prerequisites

Before running this application, ensure you have the following installed:

- **Docker**: Version 20.10 or higher ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose**: Version 2.0 or higher ([Install Docker Compose](https://docs.docker.com/compose/install/))
- **Git**: For cloning the repository

> **Note**: Docker Desktop includes Docker Compose, so separate installation may not be necessary.

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
git checkout feature/JIRA-777/fullstack-app
```

### 2. Start the Application

```bash
docker compose up --build
```

This command will:
- Build both frontend and backend Docker images
- Start both services
- Set up networking between containers
- Enable hot-reload for development

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 4. Stop the Application

```bash
docker compose down
```

## 📁 Project Structure

```
project-root/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── App.jsx          # Main application component
│   │   ├── App.css          # Green theme styles
│   │   ├── App.test.jsx     # Frontend tests
│   │   ├── main.jsx         # React entry point
│   │   └── setupTests.js    # Test configuration
│   ├── index.html           # HTML template
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   └── Dockerfile           # Frontend container config
├── backend/                  # FastAPI backend application
│   ├── main.py              # FastAPI application
│   ├── test_main.py         # Backend tests
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container config
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI/CD
├── docker-compose.yml       # Docker orchestration
└── README.md               # This file
```

## 📚 API Documentation

### Endpoints

#### 1. Get Hello Message

```http
GET /api/hello
```

**Response (200 OK)**:
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**Description**: Returns a greeting message with ISO 8601 formatted timestamp.

#### 2. Health Check

```http
GET /health
```

**Response (200 OK)**:
```json
{
  "status": "healthy"
}
```

**Description**: Health check endpoint for monitoring service availability.

### Interactive API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation where you can test all endpoints.

## 💻 Development

### Running Services Individually

#### Backend Only

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Only

```bash
cd frontend
npm install
npm run dev
```

### Development Features

- **Hot Module Replacement (HMR)**: Frontend updates automatically on code changes
- **Auto-reload**: Backend restarts automatically on code changes
- **Volume Mounts**: Code changes reflect immediately in containers
- **Logging**: View container logs with `docker compose logs -f`

### Environment Variables

#### Backend
- `PYTHONUNBUFFERED=1`: Ensures Python output is sent straight to terminal

#### Frontend
- API Base URL: `http://localhost:8000` (hardcoded in App.jsx)

## 🧪 Testing

### Backend Tests (pytest)

```bash
# Run tests in container
docker compose exec backend pytest

# Run tests locally
cd backend
pip install -r requirements.txt
pytest -v
```

**Test Coverage**:
- Health endpoint tests
- Hello endpoint tests
- CORS configuration tests
- Response format validation
- Performance tests (<100ms response time)
- Error handling tests

### Frontend Tests (Vitest)

```bash
# Run tests locally
cd frontend
npm install
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with UI
npm run test:ui
```

**Test Coverage**:
- Component rendering tests
- User interaction tests
- API integration tests
- Error handling tests
- Loading state tests
- Accessibility tests

### Running All Tests

The GitHub Actions CI pipeline automatically runs all tests on push and pull request events.

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use

**Error**: `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solution**: Stop the process using the port or change the port in docker-compose.yml

```bash
# Find process using port
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill the process or change docker-compose.yml ports
```

#### Backend Connection Refused

**Error**: `Unable to connect to backend`

**Solution**: Ensure backend service is running

```bash
# Check if backend is running
docker compose ps

# Check backend logs
docker compose logs backend

# Restart backend
docker compose restart backend
```

#### CORS Errors

**Error**: `Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution**: CORS is pre-configured. If issues persist, verify backend/main.py CORS settings.

#### Docker Build Fails

**Error**: Build failures or timeout errors

**Solution**: Clear Docker cache and rebuild

```bash
# Remove containers and volumes
docker compose down -v

# Remove images
docker rmi $(docker images -q green-hello-*)

# Rebuild
docker compose up --build
```

#### Hot Reload Not Working

**Solution**: Ensure volume mounts are configured correctly in docker-compose.yml

```bash
# Restart services
docker compose restart

# Check volume mounts
docker compose config
```

### Health Checks

```bash
# Check service health
docker compose ps

# Backend health check
curl http://localhost:8000/health

# Frontend health check
curl http://localhost:3000
```

### Viewing Logs

```bash
# All services
docker compose logs -f

# Backend only
docker compose logs -f backend

# Frontend only
docker compose logs -f frontend

# Last 100 lines
docker compose logs --tail=100
```

## 🛠 Technology Stack

### Frontend
- **React**: 18.2.0
- **Vite**: 5.0.8
- **Vitest**: 1.1.0
- **React Testing Library**: 14.1.2
- **Node**: 18-alpine (Docker)
- **Nginx**: alpine (Production server)

### Backend
- **Python**: 3.11
- **FastAPI**: 0.100+
- **Uvicorn**: 0.23.0+
- **pytest**: 7.4.0+
- **httpx**: 0.24.0+ (for testing)

### DevOps
- **Docker**: 20.10+
- **Docker Compose**: 3.8
- **GitHub Actions**: CI/CD pipeline

## 🎨 Design Specifications

### Color Theme
- **Primary Green**: #2ecc71
- **Secondary Green**: #27ae60
- **Text on Green**: #ffffff
- **Background**: #f0f0f0
- **Error Text**: #e74c3c

### Responsive Breakpoints
- **Mobile Portrait**: 320px - 479px
- **Mobile Landscape**: 480px - 767px
- **Tablet**: 768px - 1024px
- **Desktop**: 1025px - 1919px
- **Large Desktop**: 1920px+

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues, questions, or suggestions, please open an issue in the GitHub repository.

---

**Built with ❤️ using React, FastAPI, and Docker**
