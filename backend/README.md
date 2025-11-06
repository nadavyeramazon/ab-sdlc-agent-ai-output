# FastAPI Greeting Backend

A simple FastAPI backend service that provides personalized greeting functionality.

## Features

- 🚀 **FastAPI Framework**: Modern, fast Python web framework
- 👋 **Greeting Endpoint**: POST endpoint to greet users by name
- ✅ **Health Check**: Monitor service health
- 🔄 **CORS Support**: Configured for frontend communication
- 📝 **API Documentation**: Auto-generated Swagger/OpenAPI docs
- 🔒 **Input Validation**: Using Pydantic models

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

### 1. Create a Virtual Environment (Recommended)

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Backend

### Development Mode

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: `http://localhost:8000`
- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Docker

If a Dockerfile is provided:

```bash
docker build -t greeting-backend .
docker run -p 8000:8000 greeting-backend
```

## API Endpoints

### 1. Root Endpoint

**GET** `/`

Returns a welcome message.

**Response:**
```json
{
  "message": "Welcome to the Greeting API"
}
```

### 2. Health Check

**GET** `/health`

Check if the service is running.

**Response:**
```json
{
  "status": "healthy"
}
```

### 3. Greet User

**POST** `/greet`

Greet a user based on their name.

**Request Body:**
```json
{
  "name": "John"
}
```

**Response:**
```json
{
  "message": "Hello, John! Welcome to our green-themed greeting service. Have a wonderful day!"
}
```

**Error Handling:**
- If name is empty or missing, returns a default greeting message
- Validates input using Pydantic models

## Project Structure

```
backend/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration (optional)
├── .dockerignore        # Docker ignore file
└── README.md            # This file
```

## Dependencies

Main dependencies (see requirements.txt):

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **pydantic**: Data validation

## Configuration

The backend can be configured using environment variables:

- `PORT`: Server port (default: 8000)

Example:
```bash
PORT=9000 python main.py
```

## CORS Configuration

The API is configured to accept requests from any origin (`allow_origins=["*"]`).

For production, update this in `main.py` to specific origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Greet endpoint
curl -X POST http://localhost:8000/greet \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'
```

### Using Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/greet",
    json={"name": "Alice"}
)
print(response.json())
```

### Using the Interactive Docs

1. Start the server
2. Open `http://localhost:8000/docs`
3. Try out the endpoints directly in the browser

## Development

### Adding New Endpoints

1. Define your endpoint in `main.py`:

```python
@app.get("/new-endpoint")
async def new_endpoint():
    return {"message": "Hello from new endpoint"}
```

2. Add Pydantic models for request/response validation as needed

### Auto-reload During Development

Use the `--reload` flag with uvicorn to auto-reload on code changes:

```bash
uvicorn main:app --reload
```

## Troubleshooting

### Port Already in Use

If port 8000 is already in use:

```bash
# Use a different port
uvicorn main:app --port 8001
```

### CORS Errors

If you see CORS errors in the browser:

1. Ensure the backend is running
2. Check that CORS middleware is properly configured
3. Verify the frontend is using the correct backend URL

### Module Not Found

If you see import errors:

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## License

See the main repository LICENSE file.
