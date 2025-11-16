# Purple Theme Fullstack Application

A fullstack web application with a purple theme featuring React frontend and FastAPI backend.

## Features

- **Purple Theme**: Modern purple color scheme throughout the application
- **Get Message from Backend**: Fetch hello world message from API
- **Personalized Greeting**: Enter your name to receive a personalized greeting
- **Responsive Design**: Works on desktop and mobile devices
- **Comprehensive Testing**: Full test coverage with pytest
- **CI/CD Pipeline**: Automated testing with GitHub Actions

## Tech Stack

- **Frontend**: React 18, Vite, CSS3
- **Backend**: Python 3.11, FastAPI, Pydantic
- **Testing**: pytest, FastAPI TestClient
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

## Quick Start

### Prerequisites

- Docker and Docker Compose V2
- Or: Node.js 18+, Python 3.11+

### Running with Docker

```bash
# Start both frontend and backend
docker compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Running Locally (Development)

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### GET /api/hello
Returns a hello world message.

**Response:**
```json
{
  "message": "Hello from FastAPI backend!"
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
Returns a personalized greeting.

**Request:**
```json
{
  "name": "John"
}
```

**Response:**
```json
{
  "greeting": "Hello, John! Welcome to our purple-themed app!",
  "timestamp": "2024-01-15T14:30:00.000Z"
}
```

**Error Response (400):**
```json
{
  "detail": "Name cannot be empty"
}
```

## Testing

### Backend Tests

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

### Run All Tests

```bash
# From root directory
pytest tests/ -v --cov=backend --cov-report=html
```

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Backend container
│   └── tests/              # Backend tests
│       ├── __init__.py
│       └── test_api.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Purple theme styles
│   │   └── main.jsx        # React entry point
│   ├── index.html          # HTML template
│   ├── vite.config.js      # Vite configuration
│   ├── package.json        # Node dependencies
│   └── Dockerfile          # Frontend container
├── tests/
│   ├── __init__.py
│   └── test_integration.py # Integration tests
├── .github/
│   └── workflows/
│       └── ci.yml          # CI/CD pipeline
├── docker-compose.yml      # Docker services
├── pytest.ini             # Pytest configuration
└── README.md
```

## Color Palette

- **Primary Purple**: #9b59b6
- **Secondary Purple**: #8e44ad
- **Hover Purple**: #7d3c98
- **Background**: Linear gradient with purple tones
- **Text**: High contrast for accessibility (WCAG AA compliant)

## Development

### Adding New Features

1. Implement backend endpoint in `backend/main.py`
2. Add corresponding tests in `backend/tests/`
3. Update frontend in `frontend/src/App.jsx`
4. Run tests to ensure nothing breaks
5. Commit changes

### Running CI Locally

The CI pipeline runs automatically on push. To test locally:

```bash
# Run backend tests
pytest tests/ -v

# Build Docker images
docker compose build

# Start services
docker compose up
```

## License

Apache License 2.0 - See LICENSE file for details
