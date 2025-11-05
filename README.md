# Backend API Service

Minimal FastAPI backend service for the frontend client.

## Features

- ✅ FastAPI with CORS support
- 🌍 Root endpoint with Hello World message
- 🏥 Health check endpoint
- 🧪 Comprehensive unit tests
- 🤖 GitHub Actions CI/CD
- 📝 Proper typing and documentation

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Testing

```bash
pytest test_main.py -v
```

## API Endpoints

- `GET /` - Returns Hello World message
- `GET /health` - Returns health status
- `GET /docs` - OpenAPI documentation

## License

MIT License