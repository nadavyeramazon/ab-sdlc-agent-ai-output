# Green Theme Hello World Fullstack Application

## Overview

A modern fullstack web application with a green-themed React frontend and FastAPI backend. This application demonstrates:

- **Green Theme UI**: Modern, accessible design with green color palette (#2ecc71, #27ae60)
- **RESTful API**: FastAPI backend with comprehensive validation
- **Comprehensive Testing**: Pytest backend tests and GitHub Actions CI
- **Docker Support**: Full containerization with Docker Compose

## Features

### Frontend (React + Vite)
- Green-themed responsive UI
- "Get Message from Backend" feature
- Loading states and error handling
- Keyboard navigation support
- Smooth animations and transitions

### Backend (FastAPI)
- `GET /api/hello` - Returns hello message with timestamp
- `GET /health` - Health check endpoint
- CORS configuration for frontend
- Comprehensive error handling

## Technical Stack

- **Frontend**: React 18, Vite 5, CSS3
- **Backend**: FastAPI 0.109, Python 3.11
- **Testing**: Pytest 7.4, FastAPI TestClient
- **CI/CD**: GitHub Actions
- **Containerization**: Docker, Docker Compose V2

## Quick Start

### Prerequisites
- Docker and Docker Compose V2
- Ports 3000 and 8000 available

### Running the Application

```bash
# Clone the repository
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend

# Checkout the feature branch
git checkout feature/JIRA-777/fullstack-app

# Start all services
docker compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Running Tests

#### Backend Tests
```bash
cd backend
pip install -r requirements.txt
pytest test_main.py -v
```

#### CI Pipeline
GitHub Actions automatically runs:
- Backend pytest suite (26 tests)
- Frontend build validation
- Docker image builds
- Integration tests

## API Endpoints

### GET /api/hello
Returns a hello message with timestamp.

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T14:30:00.123456Z"
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

## Testing

### Backend Test Suite
Located in `backend/test_main.py`:

- **Health Endpoint Tests** (3 tests)
  - Status code validation
  - JSON response format
  - Health status content

- **Hello Endpoint Tests** (5 tests)
  - Response structure
  - Message content
  - Timestamp format (ISO 8601)

- **CORS Tests** (2 tests)
  - Header validation
  - Origin allowance

- **Performance Tests** (2 tests)
  - Response time <100ms requirement

### Running Tests Locally

```bash
# Backend tests
cd backend
pytest test_main.py -v --cov=main --cov-report=term-missing

# Run specific test class
pytest test_main.py::TestHelloEndpoint -v

# Run with detailed output
pytest test_main.py -v --tb=long
```

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI pipeline
├── backend/
│   ├── Dockerfile             # Backend Docker configuration
│   ├── main.py                # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── test_main.py           # Pytest test suite
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── App.css           # Green theme styles
│   │   └── main.jsx          # React entry point
│   ├── Dockerfile            # Frontend Docker configuration
│   ├── index.html            # HTML template
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite configuration
├── docker-compose.yml        # Service orchestration
├── .gitignore               # Git ignore patterns
└── README.md                # This file
```

## Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) includes:

1. **Backend Tests**: Runs pytest suite with coverage
2. **Frontend Build**: Validates Vite build process
3. **Docker Build**: Validates Docker image creation
4. **Integration Tests**: Tests full stack with Docker Compose
   - Health endpoint validation
   - API functionality tests
   - Frontend accessibility check

## Success Criteria

This implementation meets all success criteria:

✅ User can access frontend at localhost:3000  
✅ Frontend displays green-themed page with "Hello World" heading  
✅ User can click button to fetch data from backend  
✅ Backend API responds with correct JSON message including timestamp  
✅ Both services start successfully with `docker compose up`  
✅ Frontend-backend integration works without errors  
✅ Vite HMR provides instant updates during development  
✅ README.md includes clear setup and run instructions  
✅ All acceptance criteria from user stories are met

## Color Palette

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| Primary Green | #2ecc71 | Primary buttons, headings |
| Secondary Green | #27ae60 | Borders, secondary elements |
| Success Background | #d5f4e6 | Success message backgrounds |
| Success Text | #1e7e34 | Success message text |

## License

Apache License 2.0

## Contributing

Contributions are welcome! Please ensure:
1. All tests pass
2. Code follows existing style
3. New features include tests
4. Documentation is updated

## Support

For issues or questions, please open an issue on GitHub.
