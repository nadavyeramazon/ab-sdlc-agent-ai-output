# Greeting Application

A full-stack application with a green-themed frontend and FastAPI backend that greets users by name.

## Features

- **Frontend**: JavaScript-based UI with a beautiful green theme
- **Backend**: FastAPI application that provides greeting functionality
- **Docker**: Fully containerized with Docker Compose for easy deployment

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container configuration
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── styles.css          # Green-themed CSS styles
│   ├── app.js              # JavaScript application logic
│   ├── nginx.conf          # Nginx configuration
│   └── Dockerfile          # Frontend container configuration
├── docker-compose.yml      # Docker Compose configuration
└── README.md              # This file
```

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ab-sdlc-agent-ai-backend
   ```

2. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - **Frontend**: Open your browser and navigate to `http://localhost:3000`
   - **Backend API**: `http://localhost:8000`
   - **API Documentation**: `http://localhost:8000/docs`

### Stopping the Application

```bash
docker-compose down
```

## API Endpoints

### Backend (FastAPI)

- `GET /` - Root endpoint
- `GET /health` - Health check endpoint
- `POST /greet` - Greet a user by name (accepts JSON body with `name` field)
- `GET /greet/{name}` - Greet a user by name via GET request

### Example API Request

```bash
curl -X POST "http://localhost:8000/greet" \
     -H "Content-Type: application/json" \
     -d '{"name": "John"}'
```

### Example API Response

```json
{
  "message": "Hello, John! Welcome to our green-themed application!",
  "name": "John"
}
```

## Development

### Running Backend Locally

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Running Frontend Locally

Simply open `frontend/index.html` in your browser, or use a local web server:

```bash
cd frontend
python -m http.server 3000
```

## Technologies Used

- **Frontend**:
  - HTML5
  - CSS3 (with green theme)
  - Vanilla JavaScript
  - Nginx (for serving static files in Docker)

- **Backend**:
  - Python 3.11
  - FastAPI
  - Uvicorn
  - Pydantic

- **DevOps**:
  - Docker
  - Docker Compose

## Features Implemented

✅ Green-themed UI with gradient backgrounds
✅ Responsive design for mobile and desktop
✅ FastAPI backend with CORS support
✅ RESTful API for greeting users
✅ Docker containerization for both frontend and backend
✅ Docker Compose for easy multi-container deployment
✅ Health check endpoints
✅ Error handling and validation
✅ Interactive user interface with real-time feedback

## License

See the LICENSE file for details.
