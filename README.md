# FastAPI Backend Application

A minimal FastAPI backend application with CORS support and automated testing.

## Features

- Clean and simple FastAPI backend
- CORS middleware with security restrictions
- Comprehensive unit tests with pytest
- GitHub Actions CI/CD pipeline
- Type hints and async endpoints

## Installation

### Prerequisites

- Python 3.12 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone git@github.com:nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install development dependencies (for testing):
```bash
pip install -r requirements-dev.txt
```

## Running the Application

### Development Mode

```bash
uvicorn main:app --reload
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### `GET /api/hello`

Returns a simple hello world message.

**Response:**
```json
{
  "message": "Hello World"
}
```

**Example:**
```bash
curl http://localhost:8000/api/hello
```

## Running Tests

### Run all tests:
```bash
pytest test_app.py -v
```

### Run with coverage:
```bash
pytest test_app.py -v --cov=main
```

## Project Structure

```
.
├── main.py                    # FastAPI application
├── test_app.py                # Unit tests
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── .github/
│   └── workflows/
│       └── test.yml          # GitHub Actions CI/CD
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## CI/CD

The project uses GitHub Actions for continuous integration:

- Tests run automatically on push to main/develop branches
- Tests run on all pull requests
- Uses Python 3.12
- Runs pytest with verbose output

## CORS Configuration

The backend allows requests from any origin but restricts:
- **Methods**: GET, POST, PUT, DELETE only
- **Headers**: Content-Type and Authorization only

For production, update the `allow_origins` in `main.py` to specific domains:

```python
allow_origins=["https://yourdomain.com"],
```

## Development

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Use async/await for all endpoints

### Adding New Endpoints

1. Add endpoint function in `main.py`
2. Add corresponding tests in `test_app.py`
3. Run tests to ensure they pass
4. Update this README with endpoint documentation

## Troubleshooting

**Port already in use:**
```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9
```

**Module not found:**
```bash
# Ensure you're in the correct directory and dependencies are installed
pip install -r requirements.txt
```

## License

MIT
