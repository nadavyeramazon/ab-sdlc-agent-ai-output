# AB SDLC Agent AI Backend

A FastAPI-based backend application for the AB SDLC Agent AI system.

## Features

- **FastAPI Framework**: Modern, fast (high-performance) web framework for building APIs
- **Auto-generated Documentation**: Interactive API docs at `/docs` and `/redoc`
- **Data Validation**: Request/response validation using Pydantic models
- **CORS Support**: Cross-Origin Resource Sharing enabled
- **RESTful API**: Complete CRUD operations for items
- **Error Handling**: Comprehensive error handling and custom error responses
- **Health Check**: Health check endpoint for monitoring

## Prerequisites

- Python 3.8+
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

### Development Mode

Run the application with auto-reload enabled:

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

For production deployment:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the application is running, you can access:

- **Interactive API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## API Endpoints

### Root
- `GET /` - Welcome message and links to documentation

### Health
- `GET /health` - Health check endpoint

### Items (CRUD Operations)
- `GET /items` - Get all items (with pagination and filtering)
- `GET /items/{item_id}` - Get a specific item by ID
- `POST /items` - Create a new item
- `PUT /items/{item_id}` - Update an existing item
- `PATCH /items/{item_id}` - Partially update an item
- `DELETE /items/{item_id}` - Delete an item
- `GET /items/search/by-name` - Search items by name

## Example Usage

### Health Check
```bash
curl http://localhost:8000/health
```

### Get All Items
```bash
curl http://localhost:8000/items
```

### Get Specific Item
```bash
curl http://localhost:8000/items/1
```

### Create New Item
```bash
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Monitor",
    "description": "27-inch 4K monitor",
    "price": 399.99,
    "in_stock": true,
    "tags": ["electronics", "displays"]
  }'
```

### Update Item
```bash
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Laptop",
    "price": 1099.99
  }'
```

### Delete Item
```bash
curl -X DELETE http://localhost:8000/items/1
```

### Search Items
```bash
curl http://localhost:8000/items/search/by-name?query=laptop
```

## Project Structure

```
ab-sdlc-agent-ai-backend/
│
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── LICENSE            # License file
```

## Technology Stack

- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server for running the application
- **Pydantic**: Data validation using Python type annotations
- **Python 3.8+**: Programming language

## Development

### Code Structure

The `app.py` file is organized into sections:

1. **Imports and App Initialization**: FastAPI setup and middleware configuration
2. **Pydantic Models**: Data models for request/response validation
3. **Data Store**: In-memory database (for demonstration)
4. **Exception Handlers**: Custom error handling
5. **API Endpoints**: RESTful API routes
6. **Lifecycle Events**: Startup and shutdown handlers
7. **Main Entry Point**: Application runner

### Adding New Endpoints

To add a new endpoint:

1. Define Pydantic models for request/response if needed
2. Add the endpoint function with appropriate decorators
3. Add proper documentation and type hints
4. Test using the interactive docs at `/docs`

### Error Handling

The application includes:
- Custom HTTP exception handler
- General exception handler for unexpected errors
- Validation errors are automatically handled by FastAPI

## Testing

You can test the API using:

1. **Interactive Documentation**: Visit http://localhost:8000/docs and try out endpoints
2. **cURL**: Use command-line cURL commands (examples above)
3. **Postman**: Import the OpenAPI schema from http://localhost:8000/openapi.json
4. **Python Requests**: Write test scripts using the `requests` library

## Environment Variables

For production deployment, consider using environment variables for configuration:

- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `WORKERS`: Number of worker processes (default: 1)
- `LOG_LEVEL`: Logging level (default: info)

## Security Considerations

⚠️ **Note**: This is a basic implementation for demonstration purposes. For production use, consider:

- Implementing authentication and authorization
- Using a proper database instead of in-memory storage
- Configuring CORS properly (not allowing all origins)
- Adding rate limiting
- Implementing input sanitization
- Using HTTPS
- Adding request logging and monitoring
- Implementing proper secret management

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please open an issue on GitHub.
