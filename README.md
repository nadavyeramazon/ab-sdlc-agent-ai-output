# Hello World Fullstack Application

> A minimal fullstack demonstration featuring a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose.

## Overview

This is a **DEMO MODE** application showcasing:
- ✅ React 18+ frontend with green theme
- ✅ Python FastAPI backend with REST endpoints
- ✅ Docker Compose orchestration
- ✅ Frontend-backend integration
- ✅ Hot reload for development

**Technology Stack:**
- **Frontend**: React 18 + Vite
- **Backend**: Python 3.11 + FastAPI
- **Deployment**: Docker Compose

## Features

### Frontend Features
- 🎨 **Green Theme**: Clean, modern UI with #2ecc71 primary color
- 📱 **Responsive Design**: Works on desktop and mobile
- 🔄 **Dynamic Content**: Fetch data from backend API
- ⏳ **Loading States**: Visual feedback during API calls
- ❌ **Error Handling**: User-friendly error messages

### Backend Features
- 🚀 **Fast API**: High-performance REST endpoints
- 📡 **Health Check**: Monitor backend status
- 🕒 **Timestamps**: ISO-8601 formatted timestamps
- 🔓 **CORS Enabled**: Frontend can communicate with backend

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Ports 3000 and 8000 available

### Run the Application

1. **Clone the repository**:
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output.git
   cd ab-sdlc-agent-ai-output
   git checkout feature/JIRA-777/fullstack-app
   ```

2. **Start both services**:
   ```bash
   docker compose up
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Stop the application**:
   ```bash
   docker compose down
   ```

## API Endpoints

### GET /api/hello
Returns a greeting message with timestamp.

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00.123456"
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

### GET /
Root endpoint status.

**Response:**
```json
{
  "message": "Backend API is running"
}
```

## Project Structure

```
.
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Green theme styles
│   │   └── main.jsx         # React entry point
│   ├── index.html           # HTML template
│   ├── package.json         # NPM dependencies
│   ├── vite.config.js       # Vite configuration
│   └── Dockerfile           # Frontend container
├── backend/                  # FastAPI backend application
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD pipeline
├── docker-compose.yml       # Docker Compose configuration
└── README.md                # This file
```

## Development

### Run Frontend Locally

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at http://localhost:3000

### Run Backend Locally

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend will be available at http://localhost:8000

### Hot Reload

Both services support hot reload in Docker Compose:
- **Frontend**: Source files are mounted, changes reflect immediately
- **Backend**: Code directory is mounted, uvicorn reloads on changes

## Testing

### Manual Testing Checklist

1. **Frontend Static Content**:
   - [ ] "Hello World" heading displays correctly
   - [ ] Green theme applied consistently
   - [ ] Page loads at http://localhost:3000

2. **Backend API**:
   ```bash
   curl http://localhost:8000/api/hello
   curl http://localhost:8000/health
   ```

3. **Integration**:
   - [ ] Click "Get Message from Backend" button
   - [ ] Loading state appears during fetch
   - [ ] Backend message displays successfully
   - [ ] Error message shows when backend is stopped

4. **Docker Compose**:
   - [ ] Both services start within 10 seconds
   - [ ] No port conflicts
   - [ ] Services communicate without CORS errors

## CI/CD Pipeline

The repository includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:
- ✅ Runs backend validation
- ✅ Builds frontend application
- ✅ Validates Docker Compose configuration
- ✅ Builds Docker images

Workflow triggers on:
- Pull requests to any branch
- Push to main/master branches

## Troubleshooting

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check CORS configuration in `backend/main.py`
- Verify Docker network connectivity

### Port already in use
```bash
# Find and stop the process using the port
lsof -ti:3000 | xargs kill -9  # Frontend
lsof -ti:8000 | xargs kill -9  # Backend
```

### Docker build fails
```bash
# Clean Docker cache and rebuild
docker compose down -v
docker system prune -f
docker compose build --no-cache
docker compose up
```

## Design Decisions

This is a **DEMO MODE** application with the following principles:

- ✅ **Simplicity over optimization**: Focus on working functionality
- ✅ **Minimal dependencies**: Only essential packages included
- ✅ **No lock files**: Uses `npm install` and `pip install` directly
- ✅ **Basic error handling**: Sufficient for demonstration purposes
- ✅ **Development-focused**: Hot reload and easy debugging
- ✅ **No production optimization**: Suitable for local demonstration only

## Out of Scope

The following are **NOT** included:
- ❌ Authentication or authorization
- ❌ Database integration
- ❌ Unit tests or integration tests
- ❌ Production optimizations (minification, caching)
- ❌ Extensive logging or monitoring
- ❌ Advanced error handling
- ❌ Lock files (package-lock.json, poetry.lock)

## Success Criteria

- ✅ Frontend accessible at http://localhost:3000 with green theme
- ✅ Backend accessible at http://localhost:8000 with working endpoints
- ✅ Button triggers API call and displays response
- ✅ Loading state visible during fetch
- ✅ Error message displays when backend unavailable
- ✅ `docker compose up` successfully starts both services
- ✅ No CORS errors during frontend-backend communication

## License

This is a demonstration project for educational purposes.

## Author

Created for JIRA-777 fullstack application demonstration.
