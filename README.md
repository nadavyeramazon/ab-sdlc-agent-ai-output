# Purple Theme Hello World Fullstack Application

![CI Status](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/workflows/CI%20-%20Test%20Backend%20and%20Frontend/badge.svg?branch=feature/testing-react-frontend-v1)

A simple fullstack "Hello World" application with a purple-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose.

## 🚀 Features

- **React Frontend** (Vite + React 18)
  - Purple-themed responsive UI
  - User greet input with personalized greeting from backend
  - Interactive button to fetch data from backend API
  - Loading states and error handling
  - Comprehensive test coverage with React Testing Library

- **FastAPI Backend** (Python 3.11)
  - RESTful API with `/api/hello`, `/api/greet`, and `/health` endpoints
  - POST /api/greet endpoint for personalized greetings
  - Input validation and error handling
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
│   │   ├── App.css         # Purple theme styles
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

### POST /api/greet
Returns a personalized greeting for the provided name.

**Request:**
```json
{
  "name": "John"
}
```

**Success Response (200):**
```json
{
  "greeting": "Hello, John! Welcome to our purple-themed app!",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Error Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "name"],
      "msg": "Value error, Name cannot be empty",
      "input": "",
      "ctx": {"error": {}}
    }
  ]
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

- **Purple Theme**: Primary color #9b59b6, secondary #8e44ad
- **User Greet**: Input field to enter name and receive personalized greeting
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages
- **Accessibility**: ARIA labels and semantic HTML
- **Keyboard Support**: Enter key support for form submission

## ✅ Acceptance Criteria Met

### Story 1: Purple Theme Update ✓
- ✅ All green colors replaced with purple (#9b59b6 primary, #8e44ad secondary)
- ✅ Page background, buttons, and accents use purple theme
- ✅ Text remains readable with good contrast
- ✅ Existing "Hello World" functionality unchanged

### Story 2: User Greet API Endpoint ✓
- ✅ POST /api/greet endpoint accepts JSON with "name" field
- ✅ Returns personalized greeting: "Hello, [name]! Welcome to our purple-themed app!"
- ✅ Validates that name is not empty
- ✅ Returns 422 Unprocessable Entity for validation errors (Pydantic default)
- ✅ CORS enabled for frontend access

### Story 3: Frontend User Greet Integration ✓
- ✅ Input field for entering name
- ✅ Button labeled "Greet Me"
- ✅ On click, sends name to /api/greet endpoint
- ✅ Displays personalized greeting from backend
- ✅ Shows validation error if name is empty
- ✅ Shows loading state during API call
- ✅ Handles network errors gracefully
- ✅ Enter key support for form submission

### Story 4: Maintain Existing Functionality ✓
- ✅ Original "Get Message from Backend" button still works
- ✅ /api/hello endpoint still functional
- ✅ /health endpoint still functional
- ✅ Docker compose still works
- ✅ All existing tests pass

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

### Backend Tests (50+ tests)
- Health endpoint tests
- Hello endpoint tests
- Greet endpoint tests (valid input, empty name, whitespace validation)
- CORS configuration tests
- API performance tests
- Response structure validation
- Timestamp validation

### Frontend Tests (60+ tests)
- Component rendering tests
- User interaction tests (button clicks, input changes, Enter key)
- API integration tests
- Loading state tests
- Error handling tests
- Accessibility tests
- Form validation tests
- Greet functionality tests

### Integration Tests
- Docker Compose startup
- Service health checks
- API endpoint validation
- Frontend accessibility
- End-to-end workflow
- Cross-service communication

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
