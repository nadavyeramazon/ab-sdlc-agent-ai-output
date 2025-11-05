# Microservices Application

This project demonstrates a simple microservices architecture with a FastAPI backend and a green-themed JavaScript frontend, orchestrated with Docker Compose.

## Architecture

- **Backend**: FastAPI Python application (Port 8000)
- **Frontend**: Node.js/Express application with green theme (Port 3000)
- **Orchestration**: Docker Compose

## Features

### Backend (FastAPI)
- RESTful API endpoints
- Health check endpoint
- CORS enabled for frontend communication
- Hello World API endpoint

### Frontend (JavaScript/Node.js)
- Green-themed responsive UI
- Real-time communication with backend
- Health check endpoint
- Modern, clean design

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Start the application using Docker Compose:
```bash
docker-compose up --build
```

3. Access the applications:
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **Backend API Docs**: http://localhost:8000/docs

## Development

### Running Backend Locally

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Running Frontend Locally

```bash
cd frontend
npm install
npm start
```

## API Endpoints

### Backend (Port 8000)

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/hello` - Hello endpoint for frontend communication
- `GET /docs` - Interactive API documentation (Swagger UI)

### Frontend (Port 3000)

- `GET /` - Main application page
- `GET /health` - Health check
- `GET /api/message` - Fetch message from backend

## Docker Commands

```bash
# Start services
docker-compose up

# Start services in detached mode
docker-compose up -d

# Build and start services
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Backend Docker configuration
│   └── .dockerignore       # Docker ignore file
├── frontend/
│   ├── server.js           # Express server
│   ├── package.json        # Node.js dependencies
│   ├── Dockerfile          # Frontend Docker configuration
│   ├── .dockerignore       # Docker ignore file
│   └── public/
│       ├── index.html      # Main HTML page
│       ├── styles.css      # Green theme styles
│       └── app.js          # Frontend JavaScript
├── docker-compose.yml      # Docker Compose configuration
└── README.md              # This file
```

## Technologies Used

### Backend
- Python 3.11
- FastAPI
- Uvicorn (ASGI server)
- Pydantic

### Frontend
- Node.js 18
- Express.js
- Axios (HTTP client)
- Vanilla JavaScript
- CSS3 (Green theme)

### DevOps
- Docker
- Docker Compose

## License

MIT License
