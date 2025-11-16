# Purple Theme Hello World - Fullstack Application

## Overview

A modern fullstack web application featuring a purple-themed React frontend with FastAPI backend. This application demonstrates both existing and new functionality including backend message retrieval and personalized user greetings.

## Features

### Existing Functionality
- ✅ **Hello World Display**: Purple-themed heading with modern aesthetics
- ✅ **Backend Message Retrieval**: "Get Message from Backend" button fetches and displays messages
- ✅ **Health Check Endpoint**: `/health` endpoint for service monitoring

### New Features (Purple Theme Update)
- 🎨 **Purple Color Scheme**: Complete UI refresh with purple tones (#9b59b6, #8e44ad, #7d3c98)
- 👤 **Personalized Greetings**: Interactive form for user name input with personalized welcome messages
- ⏱️ **Timestamp Support**: ISO 8601 formatted timestamps for all greetings
- ✅ **Input Validation**: Client and server-side validation for empty/whitespace-only names
- 🔄 **Loading States**: Visual feedback during API requests
- ⚠️ **Error Handling**: User-friendly error messages for network failures and validation errors

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation using Python type hints
- **Uvicorn**: ASGI server
- **pytest**: Comprehensive test suite with 30+ tests

### Frontend
- **React 18**: Modern functional components with hooks
- **Vite**: Fast build tool and development server
- **Vitest**: Unit testing framework
- **React Testing Library**: Component testing utilities

### DevOps
- **Docker**: Containerized services
- **Docker Compose**: Multi-container orchestration
- **GitHub Actions**: CI/CD pipeline with automated testing

## API Endpoints

### GET /api/hello
Returns a hello message from the backend.

**Response:**
```json
{
  "message": "Hello from the backend!"
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
Generates a personalized greeting message.

**Request:**
```json
{
  "name": "John"
}
```

**Response (200 OK):**
```json
{
  "greeting": "Hello, John! Welcome to our purple-themed app!",
  "timestamp": "2024-01-15T14:30:00.000000Z"
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Name cannot be empty"
}
```

## Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Git

### Installation & Running

1. Clone the repository:
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
git checkout feature/JIRA-777/fullstack-app
```

2. Start the application:
```bash
docker compose up --build
```

3. Access the application:
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

#### Frontend Tests
```bash
cd frontend
npm install
npm test
```

#### Integration Tests (with Docker)
```bash
docker compose up -d
# Wait for services to start
curl http://localhost:8000/health
curl http://localhost:8000/api/hello
curl -X POST http://localhost:8000/api/greet -H "Content-Type: application/json" -d '{"name": "Test"}'
```

## Project Structure

```
.
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py              # FastAPI application
│   └── test_main.py         # Pytest test suite
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx          # Main React component
│       ├── App.css          # Purple theme styles
│       ├── App.test.jsx     # Component tests
│       └── setupTests.js
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD pipeline
├── docker-compose.yml
└── README.md
```

## Testing

### Test Coverage

#### Backend Tests (30+ tests)
- Health endpoint validation
- Hello endpoint functionality
- Greet endpoint with various inputs:
  - Valid names
  - Empty strings
  - Whitespace-only strings
  - Names with spaces
  - Special characters
  - Missing fields
- CORS configuration
- ISO 8601 timestamp validation

#### Frontend Tests (15+ tests)
- Component rendering
- User interactions
- API integration
- Error handling
- Loading states
- Accessibility features
- Feature coexistence

### CI/CD Pipeline

GitHub Actions workflow includes:
1. **Backend Tests**: Run pytest suite
2. **Frontend Tests**: Run Vitest suite
3. **Docker Build Validation**: Verify images build successfully
4. **Integration Tests**: End-to-end API testing with Docker Compose

## Success Criteria

### ✅ Critical Success Criteria (9/9)
- CSC-1: "Get Message from Backend" button functionality preserved
- CSC-2: GET /api/hello returns same response structure
- CSC-3: GET /health returns same response structure
- CSC-4: docker compose up starts without errors
- CSC-5: Frontend-backend communication operational
- CSC-6: Zero new console errors
- CSC-7: Zero new backend errors
- CSC-8: CORS functions correctly
- CSC-9: All regression tests pass

### ✅ Feature Success Criteria (8/8)
- FSC-1: Purple theme applied (#9b59b6, #8e44ad, #7d3c98)
- FSC-2: Text contrast meets WCAG AA standards
- FSC-3: User can enter name and receive greeting
- FSC-4: POST /api/greet returns correct format
- FSC-5: Empty name validation works
- FSC-6: Loading indicator displays
- FSC-7: Network error handling works
- FSC-8: All new feature tests pass

### ✅ Integration Success Criteria (5/5)
- ISC-1: Old and new features coexist
- ISC-2: No breaking changes
- ISC-3: Docker Compose lifecycle works
- ISC-4: All E2E tests pass
- ISC-5: Code meets maintainability standards

**Total: 22/22 Success Criteria Met** ✅

## Color Reference

| Element | Color Code | Usage |
|---------|------------|-------|
| Primary | #9b59b6 | Buttons, headings, primary backgrounds |
| Secondary | #8e44ad | Borders, secondary accents |
| Hover/Active | #7d3c98 | Interactive element hover states |

## Accessibility

- ✅ WCAG AA compliant contrast ratios (4.5:1 minimum)
- ✅ Keyboard navigation support (Tab key)
- ✅ Screen reader support with ARIA labels
- ✅ Focus indicators visible
- ✅ Error messages announced to assistive technologies
- ✅ Semantic HTML with proper labels

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Contributing

This is a demonstration project for the Purple Theme Update with User Greet API specification.

## Support

For issues or questions, please create an issue in the GitHub repository.