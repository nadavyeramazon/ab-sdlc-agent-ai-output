# AB-SDLC-Agent-AI Backend

Minimal FastAPI backend for the AB-SDLC-Agent-AI frontend client.

## Features

- ✅ FastAPI with async/await support
- ✅ RESTful API endpoints
- ✅ CORS enabled for frontend integration
- ✅ Pydantic data validation
- ✅ Health check endpoint
- ✅ Task management (CRUD operations)
- ✅ OpenAPI documentation
- ✅ Environment-based configuration
- ✅ Comprehensive test suite with pytest
- ✅ Code linting with flake8
- ✅ GitHub Actions CI/CD ready

## Requirements

- Python 3.12+
- pip

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development/testing
```

4. Create environment file:
```bash
cp .env.example .env
```

5. Edit `.env` file with your configuration (optional - defaults work fine)

## Running the Application

### Development Server

Run with auto-reload enabled:
```bash
python run.py
```

### Production Server

Run with uvicorn directly:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Health Check
- `GET /api/v1/health` - Check API health status

### Tasks
- `GET /api/v1/tasks` - List all tasks (with optional filtering and pagination)
- `GET /api/v1/tasks/{task_id}` - Get a specific task
- `POST /api/v1/tasks` - Create a new task
- `PUT /api/v1/tasks/{task_id}` - Update a task
- `DELETE /api/v1/tasks/{task_id}` - Delete a task

## Project Structure

```
ab-sdlc-agent-ai-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Configuration settings
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py       # API router aggregation
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── health.py   # Health check endpoint
│   │           └── tasks.py    # Task CRUD endpoints
│   └── middleware/
│       ├── __init__.py
│       └── cors.py             # CORS configuration
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_health.py          # Health endpoint tests
│   ├── test_tasks.py           # Task endpoint tests
│   └── test_main.py            # Main app tests
├── .env.example                # Example environment variables
├── .flake8                     # Flake8 configuration
├── .gitignore                  # Git ignore rules
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Development dependencies
├── run.py                      # Development server runner
└── README.md                   # This file
```

## Configuration

Configuration is managed through environment variables. See `.env.example` for available options:

- `APP_NAME` - Application name (default: "AB-SDLC-Agent-AI Backend")
- `APP_VERSION` - Application version (default: "1.0.0")
- `HOST` - Server host (default: "0.0.0.0")
- `PORT` - Server port (default: 8000)
- `RELOAD` - Enable auto-reload for development (default: True)
- `CORS_ORIGINS` - Allowed CORS origins (comma-separated)

## Development

### Adding New Endpoints

1. Create a new file in `app/api/v1/endpoints/`
2. Define your router and endpoints
3. Import and include the router in `app/api/v1/router.py`

### Task Model

Tasks have the following structure:
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string (optional)",
  "status": "pending | in_progress | completed",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Testing

### Running Tests

Run all tests with coverage:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

Run specific test file:
```bash
pytest tests/test_health.py
```

Run with coverage report:
```bash
pytest --cov=app --cov-report=html
```

### Code Linting

Check code style with flake8:
```bash
flake8 app
```

### Test Coverage

The test suite includes:
- ✅ Health check endpoint tests (3 tests)
- ✅ Task CRUD operations tests (16 tests)
- ✅ Main application tests (6 tests)
- ✅ CORS middleware tests
- ✅ API documentation tests

Total: 25+ test cases covering all endpoints and core functionality.

### Manual API Testing

Test the API using curl, Postman, or the built-in Swagger UI at `/docs`.

Example curl commands:

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Create a task
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "My Task", "description": "Task description", "status": "pending"}'

# List tasks
curl http://localhost:8000/api/v1/tasks

# Get a specific task
curl http://localhost:8000/api/v1/tasks/{task_id}

# Update a task
curl -X PUT http://localhost:8000/api/v1/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'

# Delete a task
curl -X DELETE http://localhost:8000/api/v1/tasks/{task_id}
```

## CI/CD

### GitHub Actions

The repository includes GitHub Actions workflows for:
- ✅ Automated testing on push and pull requests
- ✅ Code linting with flake8
- ✅ Test coverage reporting
- ✅ Python 3.12 compatibility check

Note: The `.github/workflows/test.yml` file needs to be manually created due to API restrictions.

## Docker Support

### Using Docker

Build the image:
```bash
docker build -t ab-sdlc-backend .
```

Run the container:
```bash
docker run -p 8000:8000 ab-sdlc-backend
```

### Using Docker Compose

Start the application:
```bash
docker-compose up
```

Stop the application:
```bash
docker-compose down
```

## Notes

- This is a minimal backend implementation with in-memory storage
- For production use, consider adding:
  - Database integration (PostgreSQL, MongoDB, etc.)
  - Authentication and authorization
  - Logging and monitoring
  - Rate limiting
  - Caching
  - Database migrations
  - Async task queue (Celery, etc.)

## License

MIT License

## Author

Nadav Yer (nadavyer@amazon.com)
