# Purple-Themed Greeting Application

## Overview

A full-stack React + FastAPI application with a purple theme and personalized greeting functionality.

## Features

### Existing Features (Preserved)
- ✅ Hello World display
- ✅ Backend message retrieval via `GET /api/hello`
- ✅ Health check endpoint `GET /health`
- ✅ Docker Compose deployment

### New Features (JIRA-777)
- ✅ Purple color theme (#9b59b6, #8e44ad, #7d3c98)
- ✅ Personalized greeting API `POST /api/greet`
- ✅ Interactive greeting UI with validation
- ✅ ISO 8601 timestamps
- ✅ Comprehensive error handling
- ✅ WCAG AA contrast compliance

## Technology Stack

- **Frontend**: React 18 + Vite
- **Backend**: Python FastAPI 0.104
- **Testing**: pytest with FastAPI TestClient
- **CI/CD**: GitHub Actions
- **Deployment**: Docker Compose

## Quick Start

### Prerequisites
- Docker and Docker Compose V2
- Ports 3000 and 8000 available

### Running the Application

```bash
# Start all services
docker compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Running Tests

```bash
# Backend tests
cd backend
pip install -r requirements.txt
pytest ../tests/ -v

# With coverage
pytest ../tests/ --cov=. --cov-report=term-missing
```

## API Endpoints

### GET /api/hello
Returns "Hello World from Backend!" message.

**Response:**
```json
{
  "message": "Hello World from Backend!"
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

### POST /api/greet
Generates personalized greeting with timestamp.

**Request:**
```json
{
  "name": "Alice"
}
```

**Response (200):**
```json
{
  "greeting": "Hello, Alice! Welcome to our purple-themed app!",
  "timestamp": "2024-01-15T14:30:00.123456Z"
}
```

**Error Response (400):**
```json
{
  "detail": "Name cannot be empty"
}
```

## Testing

### Test Coverage

- **Regression Tests (REG-001 to REG-010)**: Ensure existing functionality
- **API Tests (API-001 to API-007)**: Validate greet endpoint
- **Validation Tests**: Input validation and error handling
- **Integration Tests**: End-to-end functionality

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test class
pytest tests/test_backend.py::TestGreetingAPI -v

# With coverage
pytest tests/ --cov=backend --cov-report=html
```

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI pipeline
├── backend/
│   ├── Dockerfile
│   ├── main.py                 # FastAPI application
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # React main component
│   │   ├── App.css            # Purple theme styles
│   │   └── main.jsx           # React entry point
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── tests/
│   └── test_backend.py        # Comprehensive backend tests
├── docker-compose.yml
├── pytest.ini
└── README.md
```

## Success Criteria

### ✅ Critical Success Criteria (9/9)
- CSC-1: "Get Message from Backend" button functions identically
- CSC-2: `GET /api/hello` returns same response
- CSC-3: `GET /health` returns same response
- CSC-4: `docker compose up` starts without new errors
- CSC-5: Frontend-backend communication operational
- CSC-6: Zero new browser console errors
- CSC-7: Zero new backend log errors
- CSC-8: CORS functions for all endpoints
- CSC-9: All regression tests pass

### ✅ Feature Success Criteria (8/8)
- FSC-1: Purple theme applied throughout UI
- FSC-2: Text contrast meets WCAG AA
- FSC-3: User can enter name and receive greeting
- FSC-4: `POST /api/greet` returns correct format
- FSC-5: Empty name validation works
- FSC-6: Loading indicator displays
- FSC-7: Network errors display user-friendly messages
- FSC-8: All feature tests pass

### ✅ Integration Success Criteria (5/5)
- ISC-1: Old and new features coexist
- ISC-2: No breaking changes
- ISC-3: Docker lifecycle functions cleanly
- ISC-4: All E2E tests pass
- ISC-5: Code maintainability verified

## Color Palette

| Color | Hex | Usage | WCAG Ratio |
|-------|-----|-------|------------|
| Primary Purple | `#9b59b6` | Buttons, headings | 4.68:1 (AA) |
| Secondary Purple | `#8e44ad` | Borders, secondary | 5.94:1 (AA) |
| Dark Purple | `#7d3c98` | Hover states | 7.09:1 (AAA) |

## CI/CD Pipeline

GitHub Actions workflow includes:
1. Backend pytest tests
2. Frontend build verification
3. Docker image builds
4. Integration tests with docker-compose
5. Endpoint health checks

## Development

### Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

### Adding New Features

1. Create feature branch from `main`
2. Implement changes
3. Write tests
4. Run test suite: `pytest tests/ -v`
5. Update CI workflow if needed
6. Create pull request

## License

Apache License 2.0

## Contributing

Contributions welcome! Please ensure:
- All tests pass
- Code follows style guidelines
- Documentation is updated
- WCAG AA compliance maintained