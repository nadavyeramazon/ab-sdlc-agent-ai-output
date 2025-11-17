# Yellow Theme Hello World Fullstack Application

A simple fullstack "Hello World" application demonstrating modern web architecture with a yellow-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose.

## 🎯 Features

- **React Frontend**: Modern React 18+ with Vite for fast development and HMR
- **FastAPI Backend**: High-performance Python backend with async support
- **Yellow Theme**: Beautiful green/yellow color scheme (#2ecc71, #27ae60)
- **Docker Compose**: Single-command orchestration for both services
- **Comprehensive Tests**: Full test coverage for frontend and backend
- **CI/CD**: GitHub Actions workflow for automated testing
- **Responsive Design**: Works on all screen sizes

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐
│  React Frontend │  HTTP   │ FastAPI Backend │
│   (Port 3000)   │◄───────►│   (Port 8000)   │
└─────────────────┘         └─────────────────┘
```

## 📋 Prerequisites

- Docker (v24.0+)
- Docker Compose (v2.0+)
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
   cd ab-sdlc-agent-ai-backend
   git checkout feature/JIRA-888/fullstack-app
   ```

2. Start all services:
   ```bash
   docker compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Backend Docs: http://localhost:8000/docs

4. Stop the services:
   ```bash
   docker compose down
   ```

### Local Development

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

### Backend Tests

```bash
cd backend
pytest test_main.py -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Integration Tests (Docker Compose)

The CI workflow includes comprehensive integration tests that verify:
- Both services start successfully
- Backend API endpoints return correct responses
- Frontend is accessible
- Services communicate correctly

## 📚 API Documentation

### Endpoints

#### `GET /api/hello`
Returns a hello world message with timestamp.

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## 🎨 User Interface

The frontend features:
- Prominent "Hello World" heading with yellow theme
- Button to fetch data from backend
- Loading indicator during API calls
- Error handling with user-friendly messages
- Responsive design for all screen sizes

## 🏗️ Project Structure

```
project-root/
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   ├── App.css              # Yellow theme styles
│   │   ├── main.jsx             # React entry point
│   │   ├── App.test.jsx         # Component tests
│   │   └── test/
│   │       └── setup.js         # Test configuration
│   ├── index.html               # HTML template
│   ├── package.json             # Node dependencies
│   ├── vite.config.js           # Vite configuration
│   ├── Dockerfile               # Production build
│   ├── Dockerfile.dev           # Development build
│   └── nginx.conf               # Nginx config for production
├── backend/
│   ├── main.py                  # FastAPI application
│   ├── test_main.py             # Backend tests
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile               # Backend container
├── docker-compose.yml           # Service orchestration
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions workflow
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables

#### Frontend
- `VITE_BACKEND_URL`: Backend API URL (default: http://localhost:8000)

#### Backend
- `PYTHONUNBUFFERED`: Enable Python output buffering (set to 1)

## 🚀 CI/CD Pipeline

The GitHub Actions workflow runs on every push and includes:

1. **Backend Tests**: pytest with FastAPI TestClient
2. **Frontend Tests**: Vitest with React Testing Library
3. **Docker Compose Integration Tests**: End-to-end service verification

All tests must pass before merging to main.

## 📊 Success Criteria

- ✅ Frontend accessible at http://localhost:3000
- ✅ Backend accessible at http://localhost:8000
- ✅ Yellow theme properly applied
- ✅ Button successfully fetches backend data
- ✅ Loading states and error handling work correctly
- ✅ All tests pass
- ✅ Docker Compose starts services within 10 seconds
- ✅ No errors in console or logs

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Ensure all tests pass
4. Submit a pull request

## 📝 License

See LICENSE file for details.

## 🐛 Troubleshooting

### Services not starting
- Check Docker is running: `docker ps`
- Check ports 3000 and 8000 are available
- View logs: `docker compose logs`

### Frontend can't reach backend
- Ensure backend is running: `curl http://localhost:8000/health`
- Check CORS configuration in backend/main.py
- Verify VITE_BACKEND_URL is correct

### Tests failing
- Ensure dependencies are installed
- Check Node.js and Python versions
- Review test logs for specific errors

## 📧 Support

For issues or questions, please open an issue on GitHub.
