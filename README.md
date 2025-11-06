# Green Greeting Application

A full-stack application with a green-themed frontend and a FastAPI backend that greets users.

## Features

- **Frontend**: Green-themed JavaScript UI with smooth animations
- **Backend**: FastAPI application that greets users by name
- **Containerized**: Both services run in Docker containers
- **Docker Compose**: Easy orchestration of frontend and backend services

## Project Structure

```
.
├── backend/
│   ├── main.py           # FastAPI application
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Backend Docker configuration
├── frontend/
│   ├── index.html        # Main HTML file
│   ├── styles.css        # Green-themed CSS styles
│   ├── app.js           # JavaScript application logic
│   ├── nginx.conf       # Nginx configuration
│   └── Dockerfile       # Frontend Docker configuration
├── docker-compose.yml    # Docker Compose configuration
└── README.md            # This file
```

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd ab-sdlc-agent-ai-backend
```

2. Start the application:
```bash
docker-compose up --build
```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. Stop the application:
```bash
docker-compose down
```

### Running Locally (Without Docker)

#### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the FastAPI server:
```bash
uvicorn main:app --reload
```

The backend will be available at http://localhost:8000

#### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Serve the files using any static file server. For example, with Python:
```bash
python -m http.server 3000
```

The frontend will be available at http://localhost:3000

## API Endpoints

### POST /greet
Greets a user by name.

**Request Body:**
```json
{
  "name": "John"
}
```

**Response:**
```json
{
  "message": "Hello, John! Welcome to our green-themed application! 🌿"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Features

### Frontend
- Beautiful green gradient background
- Smooth animations and transitions
- Responsive design for mobile and desktop
- Form validation
- Error handling with user-friendly messages
- Clean and modern UI

### Backend
- RESTful API with FastAPI
- CORS enabled for frontend communication
- Input validation with Pydantic
- Health check endpoint
- Automatic API documentation (Swagger UI)

## Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Nginx
- **Backend**: Python, FastAPI, Uvicorn
- **Containerization**: Docker, Docker Compose

## Development

### Backend Development

The FastAPI backend includes automatic reload during development. Any changes to `main.py` will automatically restart the server.

### Frontend Development

For frontend changes, simply modify the HTML, CSS, or JavaScript files. If using Docker, rebuild the frontend container:

```bash
docker-compose up --build frontend
```

## Troubleshooting

### Backend not accessible from frontend

Make sure both services are running and connected to the same Docker network. The docker-compose.yml file handles this automatically.

### CORS errors

The backend is configured to allow all origins in development. For production, update the `allow_origins` in `backend/main.py` to specific domains.

## License

See LICENSE file for details.
