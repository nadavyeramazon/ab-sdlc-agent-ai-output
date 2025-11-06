# Simple Backend API

A simple FastAPI backend that provides REST endpoints for managing items.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /api/items` - Get all items
- `POST /api/items` - Create a new item
- `GET /api/items/{item_id}` - Get item by ID
- `PUT /api/items/{item_id}` - Update item by ID
- `DELETE /api/items/{item_id}` - Delete item by ID

The API documentation is available at `http://localhost:8000/docs`
