# AB-SDLC Agent AI Backend

A FastAPI-based backend service for the AB-SDLC Agent AI system.

## Features

- ✅ RESTful API with FastAPI
- ✅ CRUD operations for items
- ✅ Request validation with Pydantic
- ✅ Health check endpoint
- ✅ CORS middleware
- ✅ Comprehensive logging
- ✅ Interactive API documentation (Swagger UI & ReDoc)
- ✅ Pagination support
- ✅ Statistics endpoint
- ✅ Exception handling

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
   cd ab-sdlc-agent-ai-backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Development Mode

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Root
- `GET /` - Welcome message with API information

### Health
- `GET /health` - Health check endpoint

### Items
- `GET /items` - List all items (with pagination and filtering)
  - Query Parameters:
    - `skip` (int, default=0): Number of items to skip
    - `limit` (int, default=10): Maximum items to return
    - `tag` (string, optional): Filter by tag
- `POST /items` - Create a new item
- `GET /items/{item_id}` - Get a specific item
- `PUT /items/{item_id}` - Update an item
- `DELETE /items/{item_id}` - Delete an item

### Statistics
- `GET /stats` - Get statistics about items

## API Documentation

Once the application is running, you can access:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Example Usage

### Create an Item

```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Product",
    "description": "A great product",
    "price": 29.99,
    "tags": ["new", "featured"]
  }'
```

### List Items

```bash
curl "http://localhost:8000/items?skip=0&limit=10"
```

### Get Item by ID

```bash
curl "http://localhost:8000/items/1"
```

### Update an Item

```bash
curl -X PUT "http://localhost:8000/items/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Product",
    "description": "Updated description",
    "price": 39.99,
    "tags": ["updated"]
  }'
```

### Delete an Item

```bash
curl -X DELETE "http://localhost:8000/items/1"
```

### Get Statistics

```bash
curl "http://localhost:8000/stats"
```

## Project Structure

```
ab-sdlc-agent-ai-backend/
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── LICENSE            # License file
```

## Development

### Code Quality

The code follows Python best practices:
- Type hints for better IDE support
- Comprehensive docstrings
- Proper error handling
- Logging for debugging
- Pydantic models for validation

### In-Memory Storage

This implementation uses in-memory storage for simplicity. For production use, consider:
- PostgreSQL/MySQL for relational data
- MongoDB for document storage
- Redis for caching

## Docker Support (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t ab-sdlc-backend .
docker run -p 8000:8000 ab-sdlc-backend
```

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
