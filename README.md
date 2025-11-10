# Green Theme Hello World Fullstack Application

![CI Status](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/workflows/CI%20-%20Tests%20and%20Quality%20Checks/badge.svg)

A simple fullstack "Hello World" application with a green-themed frontend and Python FastAPI backend, orchestrated with Docker Compose.

## 📋 Overview

This project demonstrates a complete fullstack application with:
- **Frontend**: Vanilla JavaScript (no frameworks), HTML, CSS with green theme (#2ecc71)
- **Backend**: Python FastAPI REST API
- **Containerization**: Docker and Docker Compose
- **Testing**: Comprehensive pytest test suite
- **CI/CD**: GitHub Actions workflow for automated testing

## 🏗️ Project Structure

```
project-root/
├── frontend/
│   ├── index.html          # Main HTML page
│   ├── style.css           # Green-themed styles
│   ├── app.js              # Frontend JavaScript logic
│   ├── nginx.conf          # Nginx configuration
│   └── Dockerfile          # Frontend container configuration
├── backend/
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container configuration
├── tests/
│   └── test_backend.py     # Comprehensive backend tests
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI workflow
├── docker-compose.yml      # Service orchestration
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker (version 20.10 or later)
- Docker Compose (version 2.0 or later)

### Running the Application

1. **Clone the repository**
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
   cd ab-sdlc-agent-ai-backend
   ```

2. **Start all services**
   ```bash
   docker compose up
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Stop the services**
   ```bash
   docker compose down
   ```

## 🧪 Testing

### Running Tests Locally

1. **Install Python dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Run pytest tests**
   ```bash
   pytest tests/ -v
   ```

### Test Coverage

The test suite includes:
- ✅ Health endpoint validation
- ✅ API endpoint functionality tests
- ✅ Response structure validation
- ✅ CORS configuration tests
- ✅ Performance tests (response time < 100ms)
- ✅ Integration tests
- ✅ Error handling tests

## 📡 API Endpoints

### GET /api/hello
Returns a hello message with timestamp.

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

### GET /
Root endpoint with welcome message.

**Response:**
```json
{
  "message": "Welcome to Green Theme Hello World API"
}
```

## 🎨 Features

### Frontend Features
- ✨ Green-themed responsive design (#2ecc71 primary, #27ae60 secondary)
- 🔄 Dynamic content loading from backend
- ⏳ Loading indicator during API calls
- ❌ Graceful error handling with user feedback
- 📱 Fully responsive layout
- 🎭 Smooth animations and transitions

### Backend Features
- ⚡ FastAPI high-performance framework
- 🔌 CORS enabled for frontend communication
- 📊 JSON responses
- 🏥 Health check endpoint
- 📝 Auto-generated API documentation
- 🔥 Hot reload in development mode

## 🔧 Development

### Development Mode with Hot Reload

The Docker Compose configuration includes volume mounting for hot reload:

```bash
docker compose up
```

Changes to backend code will automatically reload the server.

### Manual Backend Development

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Manual Frontend Development

Serve frontend files with any HTTP server:

```bash
cd frontend
python -m http.server 3000
```

## 🐳 Docker Configuration

### Backend Dockerfile
- Base image: `python:3.11-slim`
- Runs on port 8000
- Uvicorn server with hot reload

### Frontend Dockerfile
- Base image: `nginx:alpine`
- Serves static files on port 3000
- Optimized nginx configuration

### Docker Compose
- Orchestrates both services
- Configures networking between containers
- Health checks for backend service
- Volume mounting for development

## 🔄 CI/CD Pipeline

GitHub Actions workflow includes:

1. **Backend Tests**
   - Runs on Python 3.11 and 3.12
   - Executes pytest test suite
   - Tests live endpoints

2. **Code Quality**
   - Flake8 linting
   - Black formatting checks

3. **Frontend Validation**
   - HTML/CSS/JS file validation
   - Theme color verification

4. **Docker Build Tests**
   - Builds both Docker images
   - Validates docker-compose configuration

5. **Integration Tests**
   - Starts services with docker-compose
   - Tests end-to-end functionality
   - Validates API responses

## 📊 Success Criteria

- ✅ Frontend accessible at localhost:3000
- ✅ Backend accessible at localhost:8000
- ✅ Green-themed UI (#2ecc71, #27ae60)
- ✅ Button to fetch backend data
- ✅ Loading state during fetch
- ✅ Error handling
- ✅ API response time < 100ms
- ✅ Services start within 10 seconds
- ✅ CORS enabled
- ✅ Comprehensive test coverage
- ✅ Automated CI/CD pipeline

## 🛠️ Technology Stack

- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Backend**: Python 3.11+, FastAPI, Uvicorn
- **Web Server**: Nginx (frontend)
- **Containerization**: Docker, Docker Compose
- **Testing**: pytest, httpx, FastAPI TestClient
- **CI/CD**: GitHub Actions

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions, please open an issue in the GitHub repository.

---

**Built with ❤️ and 💚 (green theme)**
