# Hello World FastAPI Service

A simple FastAPI service that returns a hello world message.

## Endpoints

- `GET /` - Returns hello world message
- `GET /health` - Health check endpoint

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Running with Docker

```bash
# Build the image
docker build -t hello-world-api .

# Run the container
docker run -p 8000:8000 hello-world-api
```

## API Documentation

Once running, access the auto-generated documentation at:
- `/docs` for Swagger UI
- `/redoc` for ReDoc