# Hello World FastAPI

[![CI Pipeline](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml)

A simple Hello World API built with FastAPI, featuring comprehensive tests and CI/CD integration.

## Features

- 🚀 **FastAPI Framework**: Modern, fast web framework for building APIs
- ✅ **Comprehensive Tests**: Full test coverage with pytest
- 🔄 **CI/CD Pipeline**: Automated testing with GitHub Actions
- 📚 **API Documentation**: Auto-generated OpenAPI/Swagger docs
- 🐍 **Python 3.9+**: Compatible with Python 3.9, 3.10, and 3.11

## API Endpoints

### Root Endpoint
- **GET** `/` - Returns a simple hello world message
  ```json
  {"message": "Hello World"}
  ```

### Health Check
- **GET** `/health` - Health check endpoint
  ```json
  {"status": "healthy"}
  ```

### Personalized Greeting
- **GET** `/hello/{name}` - Returns a personalized greeting
  ```json
  {"message": "Hello {name}!"}
  ```

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
   cd ab-sdlc-agent-ai-backend
   ```

2. Create a virtual environment (optional but recommended):
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

Run the FastAPI application:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Running Tests

### Run all tests:
```bash
pytest tests/ -v
```

### Run tests with coverage:
```bash
pytest tests/ --cov=. --cov-report=term-missing
```

### Run specific test class:
```bash
pytest tests/test_main.py::TestRootEndpoint -v
```

## Project Structure

```
.
├── main.py                  # FastAPI application
├── tests/
│   ├── __init__.py
│   └── test_main.py        # Comprehensive test suite
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI pipeline
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── LICENSE                # License file
```

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration. The pipeline:

- ✅ Runs on every push and pull request
- 🔄 Tests against Python 3.9, 3.10, and 3.11
- 📊 Generates code coverage reports
- 🔍 Performs code quality checks (flake8, black, isort)
- 📦 Caches dependencies for faster builds

## Development

### Code Quality

The project follows Python best practices:
- PEP 8 style guide compliance
- Type hints for better code clarity
- Comprehensive docstrings
- Clean code principles

### Testing Philosophy

Tests are organized into classes by functionality:
- **TestRootEndpoint**: Tests for the root endpoint
- **TestHealthCheckEndpoint**: Health check tests
- **TestHelloNameEndpoint**: Personalized greeting tests
- **TestAPIMetadata**: API documentation tests
- **TestErrorHandling**: Error handling and edge cases
- **TestConcurrency**: Concurrent request handling

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Technologies Used

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pytest**: Testing framework
- **GitHub Actions**: CI/CD automation
- **Python 3.9+**: Programming language

## Support

For issues, questions, or contributions, please open an issue on GitHub.
