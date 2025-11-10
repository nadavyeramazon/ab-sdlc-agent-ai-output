# Green Theme Hello World Fullstack Application

![CI Status](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/workflows/CI%20-%20Test%20Backend%20and%20Frontend/badge.svg?branch=feature/testing-react-frontend-v1)

A simple fullstack "Hello World" application with a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose.

## 🚀 Features

- **React Frontend** (Vite + React 18)
  - Green-themed responsive UI
  - Interactive button to fetch data from backend
  - Loading states and error handling
  - Comprehensive test coverage with React Testing Library

- **FastAPI Backend** (Python 3.11)
  - RESTful API with `/api/hello` and `/health` endpoints
  - CORS enabled for frontend communication
  - Comprehensive test coverage with pytest

- **Docker Compose Orchestration**
  - Single command to start both services
  - Hot reload enabled for development
  - Health checks configured

- **CI/CD Pipeline**
  - GitHub Actions workflow for automated testing
  - Backend tests, frontend tests, and integration tests
  - Docker Compose integration testing

## 📋 Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for local frontend development)
- Python 3.11+ (for local backend development)

## 🛠️ Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
git checkout feature/testing-react-frontend-v1
```

2. Start all services:
```bash
docker-compose up --build
```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

4. Stop services:
```bash
docker-compose down
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

### Run Backend Tests

```bash
cd backend
pytest test_main.py -v
```

### Run Frontend Tests

```bash
cd frontend
npm test
```

### Run All Tests (CI)

The GitHub Actions CI workflow automatically runs:
- Backend unit tests
- Frontend unit tests
- Integration tests with Docker Compose
- End-to-end API validation

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── test_main.py         # Backend tests
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container configuration
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Green theme styles
│   │   ├── App.test.jsx    # Frontend tests
│   │   ├── main.jsx        # React entry point
│   │   └── test/
│   │       └── setup.js    # Test configuration
│   ├── index.html          # HTML template
│   ├── package.json        # Node dependencies
│   ├── vite.config.js      # Vite configuration
│   ├── nginx.conf          # Nginx configuration for production
│   └── Dockerfile          # Frontend container configuration
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI pipeline
├── docker-compose.yml       # Docker Compose orchestration
└── README.md               # This file
```

## 🔌 API Endpoints

### GET /api/hello
Returns a hello message with timestamp.

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-01T12:00:00.000Z"
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

## 🎨 UI Features

- **Green Theme**: Primary color #2ecc71, secondary #27ae60
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages
- **Accessibility**: ARIA labels and semantic HTML

## ✅ Acceptance Criteria Met

### Story 1: Frontend Display ✓
- ✅ Page displays "Hello World" heading
- ✅ Green-themed background (#2ecc71)
- ✅ Responsive and centered layout
- ✅ Accessible via http://localhost:3000
- ✅ Built with React functional components

### Story 2: Backend API ✓
- ✅ GET /api/hello returns "Hello World from Backend!"
- ✅ GET /health returns "healthy" status
- ✅ Backend runs on port 8000
- ✅ CORS enabled for frontend

### Story 3: Frontend-Backend Integration ✓
- ✅ Button labeled "Get Message from Backend"
- ✅ Fetches data using React hooks
- ✅ Displays backend response
- ✅ Shows loading state
- ✅ Handles errors gracefully

### Story 4: Docker Compose Orchestration ✓
- ✅ `docker-compose up` starts both services
- ✅ Frontend accessible at localhost:3000
- ✅ Backend accessible at localhost:8000
- ✅ Services communicate with each other
- ✅ Hot reload enabled (Vite HMR)

## 🔧 Development

### Hot Reload

- **Frontend**: Vite HMR is enabled - changes are reflected instantly
- **Backend**: Uvicorn reload is enabled - changes restart the server automatically

### Adding Dependencies

**Backend:**
```bash
cd backend
pip install <package>
pip freeze > requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install <package>
```

## 📊 Test Coverage

### Backend Tests
- Health endpoint tests
- Hello endpoint tests
- CORS configuration tests
- API performance tests
- Response structure validation

### Frontend Tests
- Component rendering tests
- User interaction tests
- API integration tests
- Loading state tests
- Error handling tests
- Accessibility tests

### Integration Tests
- Docker Compose startup
- Service health checks
- API endpoint validation
- Frontend accessibility
- End-to-end workflow

## 🚀 CI/CD Pipeline

The GitHub Actions workflow runs on every push and pull request:

1. **Backend Tests**: Runs pytest and validates API endpoints
2. **Frontend Tests**: Runs Vitest and validates React components
3. **Integration Tests**: Builds Docker containers and tests the full stack
4. **Summary**: Aggregates results and reports status

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please ensure all tests pass before submitting a PR.

## 📧 Support

For issues or questions, please open an issue on GitHub.
