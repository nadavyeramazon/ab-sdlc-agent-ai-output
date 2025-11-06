# Full-Stack Greeting Application

A simple full-stack application with a green-themed frontend and FastAPI backend.

## Features

- **Frontend**: JavaScript-based UI with green theme
- **Backend**: FastAPI application that greets users by name
- **Docker**: Containerized with Docker Compose

## Quick Start

1. Clone the repository
2. Run with Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Project Structure

```
├── frontend/          # JavaScript frontend application
├── backend/           # FastAPI backend application
├── docker-compose.yml # Docker Compose configuration
└── README.md         # This file
```

## API Endpoints

- `GET /`: Welcome message
- `POST /greet`: Greet user by name
- `GET /health`: Health check

## Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```