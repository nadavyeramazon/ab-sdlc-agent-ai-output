# Microservices Application - FastAPI + JavaScript

A simple microservices application demonstrating communication between a FastAPI backend and a JavaScript frontend using Docker Compose.

## Architecture

This project consists of two microservices:

1. **Backend** - FastAPI Python application
   - Provides REST API endpoints
   - Runs on port 8000
   - Location: `./backend`

2. **Frontend** - JavaScript application with green theme
   - Static web application served by Nginx
   - Communicates with backend via REST API
   - Runs on port 3000 (mapped to port 80 in container)
   - Location: `./frontend`

## Prerequisites

- Docker
- Docker Compose

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd ab-sdlc-agent-ai-backend
```

2. Start all services:
```bash
docker-compose up --build
```

3. Access the applications:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. Stop all services:
```bash
docker-compose down
```

### Running Services Individually

#### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

#### Frontend
```bash
cd frontend
# Open index.html in a browser or use a simple HTTP server
python -m http.server 3000
```

## API Endpoints

### Backend Endpoints

- `GET /` - Root endpoint with hello world message
- `GET /api/hello` - API endpoint that returns a JSON response for the frontend
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)

## Features

### Backend
- FastAPI framework for high performance
- CORS enabled for frontend communication
- RESTful API design
- Health check endpoint
- Auto-generated API documentation

### Frontend
- Modern, responsive design
- Green-themed UI
- Async/await for API calls
- Error handling and loading states
- Containerized with Nginx

### Docker & Orchestration
- Multi-container setup with Docker Compose
- Isolated network for service communication
- Health checks for backend service
- Volume mounting for development
- Easy one-command deployment

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Backend container configuration
│   ├── .dockerignore       # Docker ignore file
│   └── README.md           # Backend documentation
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── styles.css          # Styling (green theme)
│   ├── app.js              # JavaScript application logic
│   ├── nginx.conf          # Nginx configuration
│   ├── Dockerfile          # Frontend container configuration
│   └── README.md           # Frontend documentation
├── docker-compose.yml      # Docker Compose configuration
├── README.md              # This file
└── LICENSE                # License file
```

## Development

### Making Changes

1. Make your changes to the backend or frontend code
2. Rebuild and restart the services:
```bash
docker-compose up --build
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Debugging

#### Check service status
```bash
docker-compose ps
```

#### Execute commands in containers
```bash
# Backend
docker-compose exec backend bash

# Frontend
docker-compose exec frontend sh
```

## Technology Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Nginx
- **Containerization**: Docker, Docker Compose

## License

See LICENSE file for details.

## Contributing

Feel free to submit issues and pull requests.
