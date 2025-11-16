# Green Theme Hello World Fullstack Application

[![CI/CD Pipeline](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml)

A simple fullstack "Hello World" application with a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose for local development.

## 🌟 Features

- **Green-Themed React Frontend**: Modern React 18+ application with a beautiful green color scheme
- **FastAPI Backend**: High-performance Python backend with RESTful API
- **Docker Compose Orchestration**: One-command setup for complete development environment
- **Hot Module Replacement**: Real-time code updates without container restart
- **Comprehensive Testing**: Full test coverage for both frontend and backend
- **CI/CD Pipeline**: Automated testing with GitHub Actions
- **CORS Enabled**: Seamless frontend-backend communication

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Compose                       │
│                                                         │
│  ┌──────────────────┐      ┌──────────────────┐      │
│  │   Frontend        │      │   Backend         │      │
│  │   React + Vite    │─────▶│   FastAPI         │      │
│  │   Port: 3000      │      │   Port: 8000      │      │
│  └──────────────────┘      └──────────────────┘      │
│         │                           │                  │
│         │    fullstack-network      │                  │
│         └───────────────────────────┘                  │
└─────────────────────────────────────────────────────────┘
         │                           │
         ▼                           ▼
   localhost:3000              localhost:8000
```

## 📋 Prerequisites

- **Docker**: Version 20.10 or higher
- **Docker Compose**: V2 (comes with Docker Desktop)
- For local development without Docker:
  - **Node.js**: 18.x or higher
  - **Python**: 3.11 or higher

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
   cd ab-sdlc-agent-ai-backend
   git checkout feature/JIRA-777/fullstack-app
   ```

2. **Start all services**:
   ```bash
   docker compose up --build
   ```
   
   This single command will:
   - Build both frontend and backend Docker images
   - Start the frontend on http://localhost:3000
   - Start the backend on http://localhost:8000
   - Enable hot reload for both services

3. **Access the application**:
   - **Frontend**: Open http://localhost:3000 in your browser
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs (Swagger UI)

4. **Stop all services**:
   ```bash
   docker compose down
   ```

### Local Development (Without Docker)

#### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testing

### Run All Tests

```bash
# Backend tests
cd backend
pytest -v

# Frontend tests
cd frontend
npm test

# Docker Compose integration test
docker compose up -d --build
curl http://localhost:8000/health
curl http://localhost:8000/api/hello
curl http://localhost:3000
docker compose down
```

### Test Coverage

- **Backend**: pytest with FastAPI TestClient
  - API endpoint testing
  - CORS configuration validation
  - Performance testing (response time < 100ms)
  - Error handling scenarios

- **Frontend**: Vitest with React Testing Library
  - Component rendering
  - User interactions
  - API integration
  - Loading and error states
  - Accessibility (a11y) testing

## 📡 API Endpoints

### Backend API

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/` | GET | Service information | JSON with service details |
| `/health` | GET | Health check | `{"status": "healthy"}` |
| `/api/hello` | GET | Greeting with timestamp | `{"message": "Hello World from Backend!", "timestamp": "ISO8601"}` |

### Example Requests

```bash
# Health check
curl http://localhost:8000/health

# Get hello message
curl http://localhost:8000/api/hello

# Response:
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00.123456Z"
}
```

## 🎨 Frontend Features

### Green Theme Color Palette

- **Primary Green**: `#2ecc71`
- **Secondary Green**: `#27ae60`
- **Accent Green**: `#1abc9c`
- **Light Background**: Linear gradient from `#a8e6cf` to `#2ecc71`

### User Interface Components

1. **Hello World Heading**: Large, prominent green heading
2. **Fetch Button**: Interactive button to trigger backend API call
3. **Loading Indicator**: Shows during API request
4. **Response Display**: Shows backend message with timestamp
5. **Error Handling**: User-friendly error messages
6. **Responsive Design**: Works on mobile, tablet, and desktop

## 🔧 Configuration

### Environment Variables

#### Backend (`backend/.env`)
```env
FRONTEND_URL=http://localhost:3000
```

#### Frontend (`frontend/.env`)
```env
VITE_API_URL=http://localhost:8000
```

### Docker Compose Configuration

The `docker-compose.yml` configures:
- **Networking**: Bridge network for inter-service communication
- **Volume Mounts**: For hot reload during development
- **Port Mapping**: 3000 (frontend), 8000 (backend)
- **Health Checks**: Ensures backend is ready before frontend starts

## 📁 Project Structure

```
project-root/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Green theme styles
│   │   ├── main.jsx         # React entry point
│   │   ├── test/
│   │   │   └── setup.js     # Test configuration
│   │   └── App.test.jsx     # Component tests
│   ├── index.html           # HTML template
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   └── Dockerfile           # Frontend container
├── backend/                  # FastAPI backend application
│   ├── main.py              # FastAPI application
│   ├── test_main.py         # Backend tests
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI/CD
├── docker-compose.yml       # Docker orchestration
└── README.md                # This file
```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Backend Tests**: Runs pytest suite, validates API endpoints
2. **Frontend Tests**: Runs Vitest suite, validates component behavior
3. **Docker Compose Test**: Validates full-stack integration
4. **Performance Checks**: Ensures response times meet requirements

### Workflow Triggers

- Push to any branch
- Pull request to `main`
- Manual workflow dispatch

## 🎯 User Stories & Acceptance Criteria

### ✅ Story 1: Frontend Display
- [x] Page displays "Hello World" heading
- [x] Green theme (#2ecc71) applied
- [x] Responsive and centered content
- [x] Accessible via http://localhost:3000
- [x] Built with React 18+ functional components

### ✅ Story 2: Backend API
- [x] GET /api/hello returns message with timestamp
- [x] GET /health returns healthy status
- [x] Backend runs on port 8000
- [x] CORS enabled for http://localhost:3000
- [x] Response time < 100ms

### ✅ Story 3: Frontend-Backend Integration
- [x] Button "Get Message from Backend" visible
- [x] Button fetches data using React hooks
- [x] Displays backend response
- [x] Shows loading indicator
- [x] Displays error messages on failure
- [x] Button disabled while loading

### ✅ Story 4: Docker Compose Orchestration
- [x] `docker compose up` starts both services
- [x] Frontend accessible at http://localhost:3000
- [x] Backend accessible at http://localhost:8000
- [x] Services communicate via Docker network
- [x] Vite HMR enabled
- [x] Services start within 10 seconds
- [x] `docker compose down` cleanly stops services

## 🐛 Troubleshooting

### Services won't start

```bash
# Check if ports are already in use
lsof -i :3000
lsof -i :8000

# View service logs
docker compose logs frontend
docker compose logs backend
```

### Frontend can't connect to backend

1. Verify backend is running: `curl http://localhost:8000/health`
2. Check CORS configuration in `backend/main.py`
3. Ensure `VITE_API_URL` is set correctly

### Hot reload not working

1. Ensure volume mounts are correct in `docker-compose.yml`
2. For Docker Desktop on Windows/Mac, enable file sharing
3. Try rebuilding: `docker compose up --build`

## 📝 Development Notes

- **Backend**: Uses uvicorn with `--reload` flag for auto-reload
- **Frontend**: Vite provides instant HMR without full page reload
- **Testing**: Run tests before committing to ensure quality
- **Docker**: Uses multi-stage builds for optimization (future enhancement)

## 🤝 Contributing

1. Create a feature branch from `main`
2. Implement your changes
3. Write tests for new functionality
4. Ensure all tests pass: `pytest` and `npm test`
5. Create a Pull Request

## 📄 License

See LICENSE file for details.

## 🆘 Support

For issues and questions:
- Create an issue in the GitHub repository
- Check existing documentation
- Review CI/CD pipeline logs for detailed error messages

## 🎉 Success Criteria

All acceptance criteria have been met:

- ✅ User can access frontend at http://localhost:3000
- ✅ Frontend displays green-themed "Hello World" using React
- ✅ User can click button to fetch backend data
- ✅ Backend responds with correct JSON message including timestamp
- ✅ GET /health endpoint returns healthy status
- ✅ All services start successfully with `docker compose up`
- ✅ Vite HMR works when editing frontend code
- ✅ README includes setup instructions, run commands, and architecture overview
- ✅ All acceptance criteria from user stories are met
- ✅ Error states are handled gracefully in the UI
- ✅ Comprehensive tests for both frontend and backend
- ✅ GitHub Actions CI workflow configured and working

---

**Built with ❤️ using React 18, Vite, FastAPI, and Docker**
