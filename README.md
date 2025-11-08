# Hello World FastAPI Application

A simple, well-tested Hello World API built with FastAPI framework.

## Features

- ✅ Simple REST API with multiple endpoints
- ✅ Comprehensive test coverage
- ✅ GitHub Actions CI/CD pipeline
- ✅ Interactive API documentation (Swagger UI and ReDoc)
- ✅ Health check endpoint
- ✅ Type hints and documentation

## API Endpoints

### Root Endpoint
- **GET `/`** - Welcome message
  ```json
  {"message": "Welcome to the Hello World API"}
  ```

### Hello Endpoints
- **GET `/hello`** - Basic hello world message
  ```json
  {"message": "Hello, World!"}
  ```

- **GET `/hello/{name}`** - Personalized greeting
  ```json
  {"message": "Hello, {name}!"}
  ```

### Health Check
- **GET `/health`** - Service health status
  ```json
  {
    "status": "healthy",
    "service": "Hello World API",
    "version": "1.0.0"
  }
  ```

### Documentation
- **GET `/docs`** - Interactive API documentation (Swagger UI)
- **GET `/redoc`** - Alternative API documentation (ReDoc)
- **GET `/openapi.json`** - OpenAPI schema

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ab-sdlc-agent-ai-backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Development Server

Run the application with uvicorn:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Access Documentation

Once the server is running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run the comprehensive test suite:

```bash
pytest test_main.py -v
```

Run tests with detailed output:

```bash
pytest test_main.py -v -s
```

### Test Coverage

The test suite includes:
- ✅ Root endpoint tests
- ✅ Hello endpoint tests
- ✅ Personalized greeting tests
- ✅ Health check tests
- ✅ API documentation tests
- ✅ Error handling tests
- ✅ Response structure validation
- ✅ Integration tests

## CI/CD Pipeline

The project includes a GitHub Actions workflow that:
- Runs on every push and pull request
- Tests the application with pytest
- Performs code quality checks with flake8
- Validates code formatting with black
- Verifies the application can start
- Checks that all required endpoints exist

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI pipeline
├── main.py                  # FastAPI application
├── test_main.py             # Comprehensive test suite
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore file
├── README.md               # This file
└── LICENSE                 # License file
```

## Dependencies

- **FastAPI** (0.115.5) - Modern web framework for building APIs
- **Uvicorn** (0.34.0) - ASGI server implementation
- **Pytest** (8.3.4) - Testing framework
- **HTTPX** (0.28.1) - HTTP client for testing
- **Pydantic** (2.10.3) - Data validation

## Development

### Code Quality

The project follows Python best practices:
- PEP 8 style guide
- Type hints
- Comprehensive documentation
- Error handling
- Clean, readable code

### Adding New Endpoints

1. Add the endpoint in `main.py`:
   ```python
   @app.get("/new-endpoint")
   async def new_endpoint():
       return {"message": "New endpoint"}
   ```

2. Add tests in `test_main.py`:
   ```python
   def test_new_endpoint():
       response = client.get("/new-endpoint")
       assert response.status_code == 200
   ```

3. Run tests to verify:
   ```bash
   pytest test_main.py -v
   ```

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please ensure:
- All tests pass
- Code follows PEP 8 style guide
- New features include tests
- Documentation is updated
