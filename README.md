# Green Theme Hello World Fullstack Application

A minimal fullstack "Hello World" application with a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose for local development.

## 🎯 Overview

This project demonstrates a simple fullstack application with:
- **Frontend**: React 18 + Vite with green theme (#2ecc71)
- **Backend**: Python FastAPI with REST API
- **Orchestration**: Docker Compose for local development
- **Hot Reload**: Live updates during development for both frontend and backend

## 📁 Project Structure

```
project-root/
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Green theme styling
│   │   └── main.jsx         # React entry point
│   ├── index.html           # HTML template
│   ├── package.json         # Frontend dependencies
│   ├── vite.config.js       # Vite configuration
│   └── Dockerfile           # Frontend Docker image
├── backend/                  # Python FastAPI backend
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Backend dependencies
│   └── Dockerfile           # Backend Docker image
├── docker-compose.yml        # Docker Compose orchestration
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD pipeline
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git installed

### Run with Docker Compose (Recommended)

1. **Clone the repository and checkout the feature branch**:
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output.git
   cd ab-sdlc-agent-ai-output
   git checkout feature/JIRA-777/fullstack-app
   ```

2. **Start the application**:
   ```bash
   docker compose up
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Health: http://localhost:8000/health
   - API Hello: http://localhost:8000/api/hello

4. **Stop the application**:
   ```bash
   docker compose down
   ```

### Run Locally (Without Docker)

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🎨 Features

### Frontend Features
- ✅ Green-themed UI with gradient background (#2ecc71)
- ✅ "Hello World" heading display
- ✅ Interactive button to fetch backend data
- ✅ Loading state indicator
- ✅ Error handling with user-friendly messages
- ✅ Responsive design with centered layout
- ✅ Hot Module Replacement (HMR) for development

### Backend Features
- ✅ RESTful API with FastAPI
- ✅ `/api/hello` endpoint returning message with timestamp
- ✅ `/health` endpoint for health checks
- ✅ CORS enabled for frontend communication
- ✅ Auto-reload during development

## 📡 API Endpoints

### GET /api/hello
Returns a hello message with timestamp.

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### GET /health
Returns the health status of the backend.

**Response:**
```json
{
  "status": "healthy"
}
```

## 🧪 Testing

### Manual Testing Checklist

**Frontend:**
- [ ] Page loads at localhost:3000 with green theme
- [ ] "Hello World" heading is visible
- [ ] "Get Message from Backend" button is displayed
- [ ] Clicking button shows "Loading..." state
- [ ] Backend message displays after fetch completes
- [ ] Error message displays when backend is unavailable

**Backend:**
- [ ] API accessible at localhost:8000
- [ ] GET /api/hello returns correct JSON structure
- [ ] GET /health returns healthy status
- [ ] Timestamp in ISO-8601 format

**Integration:**
- [ ] Services start with `docker compose up` within 10 seconds
- [ ] Frontend successfully fetches data from backend
- [ ] No CORS errors in browser console
- [ ] Hot reload works for both frontend and backend

### CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow that automatically:
- Tests backend code and dependencies
- Builds and tests frontend code
- Verifies Docker image builds
- Validates Docker Compose configuration
- Performs health checks on running services

The CI pipeline runs on:
- All pull requests
- Pushes to main/master branch

## 🔧 Development

### Making Changes

**Frontend Changes:**
1. Edit files in `frontend/src/`
2. Changes are automatically reflected (HMR enabled)
3. No restart needed

**Backend Changes:**
1. Edit `backend/main.py`
2. FastAPI auto-reloads with `--reload` flag
3. No restart needed

### Viewing Logs

```bash
# All services
docker compose logs -f

# Frontend only
docker compose logs -f frontend

# Backend only
docker compose logs -f backend
```

### Rebuilding Images

```bash
# Rebuild all images
docker compose build

# Rebuild specific service
docker compose build frontend
docker compose build backend
```

## 🎨 Color Palette

The frontend uses a consistent green theme:
- **Primary Green**: `#2ecc71` - Main brand color
- **Secondary Green**: `#27ae60` - Hover states and accents
- **Background**: White (`#ffffff`)
- **Text**: Dark gray (`#2c3e50`) on light backgrounds
- **Text**: White (`#ffffff`) on dark backgrounds

## 📦 Dependencies

### Frontend
- React 18.2.0 - UI library
- React-DOM 18.2.0 - React rendering
- Vite 4.3.0 - Build tool and dev server
- @vitejs/plugin-react 4.0.0 - React plugin for Vite

### Backend
- FastAPI 0.100.0 - Web framework
- Uvicorn[standard] 0.23.0 - ASGI server

## 🐛 Troubleshooting

### Frontend not loading
- Ensure port 3000 is not in use: `lsof -i :3000`
- Check frontend logs: `docker compose logs frontend`
- Verify frontend container is running: `docker compose ps`

### Backend not responding
- Ensure port 8000 is not in use: `lsof -i :8000`
- Check backend logs: `docker compose logs backend`
- Verify backend health: `curl http://localhost:8000/health`

### CORS errors
- Verify backend CORS is configured for `http://localhost:3000`
- Check that frontend is accessing `http://localhost:8000` (not 127.0.0.1)

### Docker Compose issues
- Validate configuration: `docker compose config`
- Rebuild images: `docker compose build --no-cache`
- Remove volumes: `docker compose down -v`

## 📝 Notes

### Package Management
- Uses `npm install` (not `npm ci`) for flexibility
- Lock files are gitignored (package-lock.json, yarn.lock)
- Keeps dependencies minimal and simple

### Development Focus
- Optimized for local development, not production
- Hot reload enabled for rapid iteration
- Minimal complexity and dependencies
- No authentication, database, or advanced features

## 🤝 Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Ensure all manual tests pass
4. Submit a pull request
5. CI pipeline will automatically run tests

## 📄 License

This is a demonstration project for educational purposes.

## 🔗 Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

**Built with ❤️ and green theme 🍀**
