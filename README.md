# Green Theme Hello World Fullstack Application

A simple fullstack "Hello World" application featuring a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose.

## Features

- 🎨 React 18+ frontend with green theme styling
- 🚀 FastAPI backend with REST endpoints
- 🐳 Docker Compose orchestration for local development
- 🔄 Frontend-backend API integration with user interaction
- 🔥 Hot reload development environment
- ✅ Comprehensive test coverage
- 🤖 GitHub Actions CI/CD pipeline

## Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Running with Docker Compose

1. Clone the repository:
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
git checkout feature/JIRA-777/fullstack-app
```

2. Start the application:
```bash
docker compose up
```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. Stop the application:
```bash
docker compose down
```

## API Endpoints

### Get Hello Message
- **Method:** GET
- **Path:** `/api/hello`
- **Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Health Check
- **Method:** GET
- **Path:** `/health`
- **Response:**
```json
{
  "status": "healthy"
}
```

## Development

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Backend Development

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Testing

### Backend Tests

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm install
npm test
```

## Project Structure

```
project-root/
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── App.jsx        # Main application component
│   │   ├── App.css        # Application styles
│   │   ├── main.jsx       # Entry point
│   │   ├── components/    # Reusable components
│   │   └── hooks/         # Custom React hooks
│   ├── tests/             # Frontend tests
│   ├── Dockerfile         # Frontend Docker configuration
│   └── package.json       # Frontend dependencies
├── backend/               # FastAPI backend application
│   ├── app/
│   │   ├── main.py        # FastAPI application
│   │   ├── models.py      # Pydantic models
│   │   └── routes.py      # API routes
│   ├── tests/             # Backend tests
│   ├── Dockerfile         # Backend Docker configuration
│   └── requirements.txt   # Python dependencies
├── .github/
│   └── workflows/
│       └── ci.yml         # CI/CD pipeline
├── docker-compose.yml     # Docker orchestration
└── README.md              # This file
```

## Technology Stack

### Frontend
- React 18+
- Vite 4+
- Modern CSS with green theme (#2ecc71, #27ae60)
- Vitest & React Testing Library

### Backend
- Python 3.11+
- FastAPI 0.100+
- Uvicorn ASGI server
- Pytest for testing

### DevOps
- Docker & Docker Compose
- GitHub Actions for CI/CD
- Multi-stage Docker builds

## Performance Requirements

- API response time: < 100ms
- Frontend load time: < 2 seconds
- Bundle size: < 500KB
- Memory usage: Backend < 128MB, Frontend < 64MB

## Success Criteria

✅ Frontend application loads with green theme  
✅ Static "Hello World" message displays correctly  
✅ Button successfully triggers backend API call  
✅ Backend response displays within 200ms  
✅ Health check endpoint responds with healthy status  
✅ Docker Compose starts both services without errors  
✅ All tests pass in CI/CD pipeline  

## License

Apache License 2.0 - see LICENSE file for details
