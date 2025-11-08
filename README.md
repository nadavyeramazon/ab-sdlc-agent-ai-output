# Green Greeting App 🌿

[![CI Pipeline](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml)

A fullstack application with a green-themed JavaScript frontend and FastAPI Python backend that greets users in multiple languages.

## Features

- 🎨 **Green-themed UI**: Beautiful, responsive vanilla JavaScript frontend with a nature-inspired green color palette
- 🚀 **FastAPI Backend**: High-performance Python API with automatic documentation
- 🌍 **Multi-language Support**: Greet users in English, Spanish, French, and German
- 🐳 **Docker Compose**: Easy deployment with containerized services
- ✅ **Comprehensive Tests**: Full test coverage with pytest
- 🔄 **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions

## Technology Stack

### Backend
- Python 3.11
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Pydantic (data validation)

### Frontend
- Vanilla JavaScript (no frameworks)
- HTML5
- CSS3 with custom green theme
- Nginx (web server)

### DevOps
- Docker & Docker Compose
- pytest (testing framework)
- GitHub Actions (CI/CD)

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Python 3.11+ (for local development)

### Running with Docker Compose

1. Clone the repository:
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

2. Start the application:
```bash
docker compose up -d
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

4. Stop the application:
```bash
docker compose down
```

### Local Development

#### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

The API will be available at http://localhost:8000

#### Frontend

For local frontend development, simply open `frontend/index.html` in a web browser or use a local web server:

```bash
cd frontend
python -m http.server 3000
```

Then visit http://localhost:3000

## API Documentation

### Endpoints

#### `GET /`
Root endpoint with API information.

**Response:**
```json
{
  "message": "Welcome to the Greeting API",
  "version": "1.0.0",
  "endpoints": {
    "greet": "/api/greet",
    "health": "/health"
  }
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "greeting-api"
}
```

#### `POST /api/greet`
Greet a user by name in a specified language.

**Request Body:**
```json
{
  "name": "John",
  "language": "en"
}
```

**Supported Languages:**
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German

**Response:**
```json
{
  "message": "Hello, John! Welcome to our green-themed application! 🌿",
  "name": "John",
  "language": "en"
}
```

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=backend --cov-report=html
```

### Test Categories

- **Unit Tests**: Test individual components and functions
- **Integration Tests**: Test API endpoints and data flow
- **Docker Tests**: Test containerized deployment

## CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow that:

1. **Testing**: Runs all pytest tests with coverage reporting
2. **Linting**: Checks code quality with flake8, black, and isort
3. **Docker Build**: Builds and tests Docker images
4. **Integration**: Tests the full application stack

The pipeline runs automatically on:
- Push to `main` branch
- Push to `feature/**` branches
- Pull requests to `main`

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container configuration
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── styles.css          # Green theme styles
│   ├── app.js              # Vanilla JavaScript logic
│   ├── nginx.conf          # Nginx configuration
│   └── Dockerfile          # Frontend container configuration
├── tests/
│   ├── __init__.py
│   └── test_main.py        # Comprehensive test suite
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI/CD pipeline
├── docker-compose.yml      # Docker Compose configuration
├── pytest.ini              # Pytest configuration
└── README.md               # This file
```

## Features in Detail

### Green Theme

The frontend features a carefully crafted green color palette inspired by nature:
- Primary Green: `#2d6a4f` - Deep forest green
- Secondary Green: `#40916c` - Vibrant green
- Light Green: `#52b788` - Fresh spring green
- Background: `#d8f3dc` - Soft mint

### Form Validation

- Client-side validation for immediate feedback
- Server-side validation with Pydantic models
- Input length limits (1-100 characters)
- Case-insensitive language codes

### Error Handling

- Graceful error messages for unsupported languages
- Network error handling with user-friendly messages
- Validation errors with clear descriptions

### Responsive Design

- Mobile-first approach
- Adapts to different screen sizes
- Touch-friendly interface

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/JIRA-XXX/description`
3. Make your changes
4. Run tests: `pytest tests/`
5. Commit your changes: `git commit -am 'Add new feature'`
6. Push to the branch: `git push origin feature/JIRA-XXX/description`
7. Create a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with 💚 by the Green Team
- Powered by FastAPI and vanilla JavaScript
- Containerized with Docker
- Tested with pytest
- Deployed with GitHub Actions
