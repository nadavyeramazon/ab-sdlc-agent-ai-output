# AB SDLC Agent AI Backend

Minimal FastAPI backend for the AB SDLC Agent AI system.

## Features

- ✅ FastAPI framework with automatic OpenAPI documentation
- ✅ CORS middleware with configurable security
- ✅ Health check endpoint for monitoring
- ✅ Comprehensive unit tests with pytest
- ✅ GitHub Actions CI/CD pipeline
- ✅ Type hints and Pydantic models

## Requirements

- Python 3.11+
- pip

## Installation

1. Clone the repository:
```bash
git clone git@github.com:nadavyeramazon/ab-sdlc-agent-ai-backend.git
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

## Configuration

The application uses environment variables for configuration:

- `PORT`: Server port (default: 8000)
- `CORS_ORIGINS`: Comma-separated list of allowed origins (default: `http://localhost:3000,http://localhost:5173`)

Create a `.env` file (see `.env.example`) or export variables:
```bash
export PORT=8000
export CORS_ORIGINS="http://localhost:3000,https://yourdomain.com"
```

## Usage

### Development Server

Run the application:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Run Tests

```bash
pytest -v
```

With coverage:
```bash
pytest -v --cov=. --cov-report=html
```

## API Endpoints

### `GET /`
Returns service information.

**Response:**
```json
{
  "message": "AB SDLC Agent AI Backend"
}
```

### `GET /health`
Health check endpoint for monitoring and load balancers.

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

## Deployment

### Production Considerations

1. **Environment Variables**: Set appropriate CORS_ORIGINS for your frontend domain
2. **HTTPS**: Always use HTTPS in production
3. **Process Manager**: Use gunicorn or similar:
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Docker (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t ab-sdlc-backend .
docker run -p 8000:8000 -e CORS_ORIGINS="https://yourdomain.com" ab-sdlc-backend
```

## CI/CD

GitHub Actions automatically runs tests on:
- Push to `main` or `feature/*` branches
- Pull requests to `main`

The pipeline includes:
- Unit tests with pytest
- Code coverage reporting
- Security checks with safety

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── test.yml          # CI/CD pipeline
├── main.py                   # FastAPI application
├── test_main.py             # Unit tests
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore patterns
├── .env.example            # Environment variables example
└── README.md               # This file
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Ensure tests pass: `pytest -v`
4. Submit a pull request

## License

MIT