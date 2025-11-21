# Yellow Theme Hello World Fullstack Application 🌟

A simple, cheerful fullstack application with a yellow theme featuring a React frontend and FastAPI backend.

## 🎯 Project Overview

This is a demonstration fullstack application that displays a "Hello World" greeting with a bright yellow theme. The application consists of:

- **Frontend**: React 18 + Vite with a responsive yellow-themed UI
- **Backend**: Python FastAPI with CORS-enabled REST API
- **Infrastructure**: Docker Compose for easy local development

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   Frontend      │────────▶│    Backend      │
│   React+Vite    │         │    FastAPI      │
│   Port: 3000    │         │    Port: 8000   │
└─────────────────┘         └─────────────────┘
```

## 📋 Prerequisites

Before running this application, ensure you have the following installed:

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher

To verify your installation:

```bash
docker --version
docker-compose --version
```

## 🚀 Quick Start

### Running with Docker Compose (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ab-sdlc-agent-ai-output
   git checkout feature/JIRA-888/fullstack-app
   ```

2. **Start the application**:
   ```bash
   docker-compose up
   ```

   This command will:
   - Build both frontend and backend Docker images
   - Start both services with hot reload enabled
   - Set up networking between services

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Stop the application**:
   ```bash
   docker-compose down
   ```

### Running in Development Mode (Manual)

#### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## 📡 API Endpoints

### Root Endpoint
- **URL**: `GET /`
- **Description**: Returns API information
- **Response**:
  ```json
  {
    "name": "Yellow Theme Hello World API",
    "version": "1.0.0",
    "description": "A simple FastAPI backend with yellow theme"
  }
  ```

### Greeting Endpoint
- **URL**: `GET /api/greeting`
- **Description**: Returns a yellow-themed greeting message
- **Response**:
  ```json
  {
    "message": "Hello World from Yellow Theme! 🌟",
    "theme": "yellow",
    "timestamp": "2024-01-15T10:30:45.123456"
  }
  ```

### Health Check
- **URL**: `GET /health`
- **Description**: Health check endpoint for monitoring
- **Response**:
  ```json
  {
    "status": "healthy",
    "service": "backend"
  }
  ```

## 🧪 Manual Testing

### Testing the Backend

1. **Test root endpoint**:
   ```bash
   curl http://localhost:8000/
   ```

2. **Test greeting endpoint**:
   ```bash
   curl http://localhost:8000/api/greeting
   ```

3. **Test health check**:
   ```bash
   curl http://localhost:8000/health
   ```

4. **Access Interactive API Docs**:
   Open http://localhost:8000/docs in your browser for Swagger UI

### Testing the Frontend

1. **Open in browser**: Navigate to http://localhost:3000
2. **Verify greeting display**: You should see the yellow-themed greeting
3. **Test refresh button**: Click "Refresh Greeting" to fetch new data
4. **Test error handling**: Stop the backend and verify error messages

### End-to-End Testing

1. Start both services with `docker-compose up`
2. Open http://localhost:3000
3. Verify the greeting loads automatically
4. Check that the timestamp updates when refreshing
5. Verify the yellow theme is applied correctly

## 🔧 Development Workflow

### Hot Reload

Both frontend and backend support hot reload:

- **Backend**: Change any `.py` file in `./backend` and the server will auto-reload
- **Frontend**: Change any file in `./frontend/src` and Vite will hot-reload the page

### Making Changes

1. **Backend changes**: Edit files in `./backend/`
2. **Frontend changes**: Edit files in `./frontend/src/`
3. **Docker changes**: Edit `Dockerfile` or `docker-compose.yml`
4. **Dependencies**:
   - Backend: Update `backend/requirements.txt`
   - Frontend: Update `frontend/package.json`

### Rebuilding Containers

If you change dependencies or Dockerfiles:

```bash
docker-compose up --build
```

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI pipeline
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # Backend container config
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── App.css            # Yellow theme styles
│   │   ├── main.jsx           # React entry point
│   │   └── index.css          # Global styles
│   ├── index.html             # HTML template
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite configuration
│   └── Dockerfile             # Frontend container config
├── docker-compose.yml         # Multi-container orchestration
├── .gitignore                 # Git ignore rules (includes lock files)
└── README.md                  # This file
```

## 🎨 Features

- ✨ Beautiful yellow-themed UI with gradient backgrounds
- 🔄 Auto-refresh greeting functionality
- 📱 Responsive design for mobile and desktop
- 🚀 Fast development with hot reload
- 🐳 Easy deployment with Docker Compose
- 📊 Health check endpoints for monitoring
- 🔌 CORS-enabled API for frontend integration
- 📝 Interactive API documentation (Swagger UI)

## 🛠️ Technology Stack

### Frontend
- **React 18**: Modern UI library
- **Vite**: Fast build tool and dev server
- **CSS3**: Custom yellow theme styling

### Backend
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server with auto-reload
- **Pydantic**: Data validation

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **GitHub Actions**: CI/CD pipeline

## 🔒 Environment Variables

### Frontend
- `VITE_API_URL`: Backend API URL (default: `http://backend:8000`)

### Backend
- `PYTHONUNBUFFERED`: Enable Python unbuffered mode (set to `1`)

## 🧹 Cleanup

To remove all containers, networks, and volumes:

```bash
docker-compose down -v
```

To also remove images:

```bash
docker-compose down -v --rmi all
```

## 🚨 Troubleshooting

### Port Already in Use

If ports 3000 or 8000 are already in use:

1. Stop the conflicting service
2. Or modify ports in `docker-compose.yml`:
   ```yaml
   ports:
     - "3001:3000"  # Change external port
   ```

### Backend Not Accessible

1. Check if backend container is running: `docker-compose ps`
2. Check backend logs: `docker-compose logs backend`
3. Verify health endpoint: `curl http://localhost:8000/health`

### Frontend Can't Connect to Backend

1. Ensure both services are running
2. Check network configuration in `docker-compose.yml`
3. Verify `VITE_API_URL` environment variable
4. Check browser console for CORS errors

### Hot Reload Not Working

1. Ensure volume mounts are correct in `docker-compose.yml`
2. For Windows/Mac: Enable file sharing in Docker Desktop settings
3. Restart containers: `docker-compose restart`

## 📝 CI/CD Pipeline

The project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

1. **Backend Tests**: Validates Python code and dependencies
2. **Frontend Tests**: Runs linting and validates Node.js setup
3. **Docker Build**: Builds both Docker images
4. **Docker Compose Validation**: Tests multi-container startup

The pipeline runs automatically on:
- Pull requests to `main` or `master`
- Pushes to `main` or `master`

## 🤝 Contributing

1. Create a new branch for your feature
2. Make your changes
3. Test locally with `docker-compose up`
4. Commit with clear messages
5. Push and create a pull request

## 📄 License

See LICENSE file for details.

## 🎉 Enjoy!

Have fun with this yellow-themed Hello World application! 🌟

For questions or issues, please open a GitHub issue.
