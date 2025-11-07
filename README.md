# Hello World FastAPI Application

A simple Hello World API built with FastAPI Python framework.

## Features

- 🚀 Fast and modern API built with FastAPI
- 📝 Multiple endpoints demonstrating different HTTP methods
- 🌍 Multi-language greeting support
- 📚 Automatic interactive API documentation
- ✅ Health check endpoint for monitoring
- 🔧 Type hints and validation with Pydantic

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Method 1: Using Python directly
```bash
python main.py
```

### Method 2: Using uvicorn
```bash
uvicorn main:app --reload
```

The application will start on `http://localhost:8000`

## API Endpoints

### 1. Root Endpoint
- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns a simple Hello World message
- **Example**:
  ```bash
  curl http://localhost:8000/
  ```

### 2. Health Check
- **URL**: `/health`
- **Method**: `GET`
- **Description**: Returns the health status of the application
- **Example**:
  ```bash
  curl http://localhost:8000/health
  ```

### 3. Personalized Greeting
- **URL**: `/hello/{name}`
- **Method**: `GET`
- **Description**: Returns a personalized greeting
- **Example**:
  ```bash
  curl http://localhost:8000/hello/John
  ```

### 4. Custom Greeting
- **URL**: `/greet`
- **Method**: `POST`
- **Description**: Returns a greeting in different languages
- **Request Body**:
  ```json
  {
    "name": "John",
    "language": "es"
  }
  ```
- **Supported Languages**: en, es, fr, de, it, pt, ja, zh, ko, ar
- **Example**:
  ```bash
  curl -X POST http://localhost:8000/greet \
    -H "Content-Type: application/json" \
    -d '{"name": "John", "language": "es"}'
  ```

### 5. API Information
- **URL**: `/info`
- **Method**: `GET`
- **Description**: Returns information about the API and available endpoints
- **Example**:
  ```bash
  curl http://localhost:8000/info
  ```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These interfaces allow you to test all endpoints directly from your browser.

## Project Structure

```
.
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── LICENSE             # License file
```

## Development

### Running Tests

To run tests (if test files are added):
```bash
pytest
```

### Code Style

The code follows PEP 8 style guidelines and includes:
- Type hints for better code clarity
- Docstrings for all functions
- Input validation using Pydantic models
- Error handling

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running the application
- **Pydantic**: Data validation using Python type annotations

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue in the GitHub repository.
