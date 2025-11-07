# AB SDLC Agent AI Backend

A comprehensive FastAPI backend service for the SDLC Agent AI system.

## Features

- ✅ **RESTful API**: Clean and intuitive REST endpoints
- ✅ **Task Management**: Full CRUD operations for tasks with filtering and pagination
- ✅ **User Management**: User creation, retrieval, and soft deletion
- ✅ **Data Validation**: Robust validation using Pydantic models
- ✅ **Health Checks**: Built-in health check endpoint
- ✅ **Statistics**: Task and user statistics endpoints
- ✅ **CORS Support**: Configured CORS middleware
- ✅ **Auto Documentation**: Interactive API docs (Swagger UI and ReDoc)
- ✅ **Error Handling**: Comprehensive error handling with custom responses
- ✅ **Type Safety**: Full type hints throughout the codebase

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

2. Install dependencies:
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

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Root & Health

- `GET /` - API information
- `GET /health` - Health check

### Tasks

- `POST /api/v1/tasks` - Create a new task
- `GET /api/v1/tasks` - Get all tasks (with filtering & pagination)
- `GET /api/v1/tasks/{task_id}` - Get a specific task
- `PUT /api/v1/tasks/{task_id}` - Update a task
- `PATCH /api/v1/tasks/{task_id}/status` - Update task status
- `DELETE /api/v1/tasks/{task_id}` - Delete a task

### Users

- `POST /api/v1/users` - Create a new user
- `GET /api/v1/users` - Get all users (with filtering & pagination)
- `GET /api/v1/users/{user_id}` - Get a specific user
- `DELETE /api/v1/users/{user_id}` - Delete a user (soft delete)

### Statistics

- `GET /api/v1/stats/tasks` - Get task statistics
- `GET /api/v1/stats/users` - Get user statistics

## Example Usage

### Create a Task

```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implement authentication",
    "description": "Add JWT-based authentication",
    "priority": "high",
    "assignee": "john.doe",
    "tags": ["backend", "security"]
  }'
```

### Get All Tasks

```bash
curl -X GET "http://localhost:8000/api/v1/tasks?status=pending&priority=high"
```

### Create a User

```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john.doe@example.com",
    "full_name": "John Doe",
    "password": "securepassword123"
  }'
```

### Get Task Statistics

```bash
curl -X GET "http://localhost:8000/api/v1/stats/tasks"
```

## Data Models

### Task

- **id**: Integer (auto-generated)
- **title**: String (required, 1-200 chars)
- **description**: String (optional, max 1000 chars)
- **status**: Enum (pending, in_progress, completed, failed)
- **priority**: Enum (low, medium, high, critical)
- **assignee**: String (optional, max 100 chars)
- **tags**: List of strings (optional, max 10 tags)
- **created_at**: DateTime (auto-generated)
- **updated_at**: DateTime (auto-updated)

### User

- **id**: Integer (auto-generated)
- **username**: String (required, 3-50 chars, unique)
- **email**: Email (required, unique)
- **full_name**: String (optional, max 100 chars)
- **is_active**: Boolean (default: true)
- **created_at**: DateTime (auto-generated)

## Features in Detail

### Filtering and Pagination

All list endpoints support filtering and pagination:

- **skip**: Number of records to skip (default: 0)
- **limit**: Maximum number of records to return (default: 100, max: 1000)
- Additional filters based on entity type (status, priority, assignee, etc.)

### Error Handling

The API returns consistent error responses:

```json
{
  "detail": "Error message",
  "timestamp": "2024-01-01T12:00:00",
  "path": "/api/v1/tasks/999"
}
```

### Data Validation

All input data is validated using Pydantic models:

- Type checking
- Length constraints
- Format validation (emails, etc.)
- Custom validators
- Automatic error messages

## Project Structure

```
ab-sdlc-agent-ai-backend/
├── app.py              # Main application file with all endpoints
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── LICENSE            # License file
```

## Development Notes

- The application currently uses in-memory storage. For production, integrate a proper database (PostgreSQL, MongoDB, etc.)
- Password hashing is not implemented in this version. Use proper password hashing (bcrypt, argon2) in production
- Configure CORS `allow_origins` appropriately for production environments
- Add authentication and authorization middleware for production use
- Consider adding rate limiting for production deployments

## Testing

You can test the API using:

1. **Interactive docs**: Visit `/docs` for Swagger UI
2. **curl**: Use the command-line examples above
3. **Postman**: Import the OpenAPI spec from `/openapi.json`
4. **Python requests**:

```python
import requests

# Create a task
response = requests.post(
    "http://localhost:8000/api/v1/tasks",
    json={
        "title": "Test task",
        "description": "This is a test",
        "priority": "high"
    }
)
print(response.json())
```

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
