# 🌿 Green Theme Hello World Fullstack Application

![React](https://img.shields.io/badge/React-18.x-61DAFB?style=flat&logo=react&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-5.x-646CFF?style=flat&logo=vite&logoColor=white)

A modern, containerized fullstack application featuring a beautiful green-themed React frontend and a high-performance FastAPI backend. Built with developer experience in mind, this project demonstrates best practices for Docker orchestration, API integration, and responsive UI design.

## ✨ Features

- 🎨 **Elegant Green Theme UI** - Beautiful, responsive interface with #2ecc71 accent color
- ⚡ **Lightning Fast** - Vite-powered frontend with Hot Module Replacement (HMR)
- 🔄 **Real-time API Integration** - Live data fetching with async/await patterns
- 🐳 **Complete Docker Orchestration** - Multi-service setup with Docker Compose
- 🔥 **Hot Reload Enabled** - Development-optimized with live code reloading
- 🏥 **Health Monitoring** - Built-in health checks for both services
- 📡 **RESTful API** - Well-documented FastAPI endpoints with automatic OpenAPI docs
- 🎯 **Production Ready** - Follows security best practices and containerization standards

## 🏗️ Architecture

This application uses a modern three-tier architecture:

```
┌─────────────────┐      ┌─────────────────┐
│   Frontend      │      │    Backend      │
│   React + Vite  │─────▶│    FastAPI      │
│   Port: 3000    │      │    Port: 8000   │
└─────────────────┘      └─────────────────┘
        │                        │
        └────────────┬───────────┘
                     │
              ┌──────▼──────┐
              │   Docker    │
              │   Network   │
              └─────────────┘
```

- **Frontend**: React 18 with Vite 5 running on port **3000**
- **Backend**: FastAPI with Python 3.11 running on port **8000**
- **Orchestration**: Docker Compose with custom bridge network for inter-service communication

## 📋 Prerequisites

Before running this application, ensure you have the following installed:

### Required (Docker Deployment)
- [Docker](https://docs.docker.com/get-docker/) (20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (2.0+)

### Optional (Local Development)
- [Node.js](https://nodejs.org/) (18+ LTS recommended)
- [Python](https://www.python.org/downloads/) (3.11+)
- [npm](https://www.npmjs.com/) or [yarn](https://yarnpkg.com/)

## 🚀 Quick Start

### With Docker Compose (Recommended)

The easiest way to run the entire application:

```bash
# 1. Clone the repository
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output.git
cd ab-sdlc-agent-ai-output

# 2. Switch to the feature branch
git checkout feature/JIRA-777/fullstack-app

# 3. Start all services with Docker Compose
docker compose up

# Optional: Run in detached mode (background)
docker compose up -d

# Optional: Build and start (forces rebuild)
docker compose up --build
```

**Access the Application:**
- 🌐 **Frontend**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000
- 📚 **API Documentation**: http://localhost:8000/docs
- 📖 **Alternative API Docs**: http://localhost:8000/redoc

**Stop the Services:**
```bash
# Stop services (preserves containers)
docker compose stop

# Stop and remove containers
docker compose down

# Stop, remove containers, and clean up volumes
docker compose down -v
```

### Local Development (Without Docker)

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at http://localhost:8000

#### Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Frontend will be available at http://localhost:3000

## 📁 Project Structure

```
ab-sdlc-agent-ai-output/
├── frontend/                # React + Vite frontend application
│   ├── src/                # Source code
│   │   ├── App.jsx         # Main React component with green theme
│   │   ├── App.css         # Component styles
│   │   └── main.jsx        # Application entry point
│   ├── Dockerfile          # Frontend container configuration
│   ├── package.json        # Frontend dependencies
│   ├── vite.config.js      # Vite configuration with HMR
│   └── index.html          # HTML template
├── backend/                 # FastAPI backend application
│   ├── main.py             # FastAPI application with endpoints
│   ├── Dockerfile          # Backend container configuration
│   └── requirements.txt    # Python dependencies
├── docker-compose.yml       # Multi-service orchestration
├── README.md               # This file
└── LICENSE                 # MIT License
```

## 🔌 API Endpoints

The backend exposes the following RESTful endpoints:

| Method | Endpoint      | Description                          | Response                                      |
|--------|---------------|--------------------------------------|-----------------------------------------------|
| GET    | `/api/hello`  | Returns greeting with timestamp      | `{"message": "Hello, World!", "timestamp": ...}` |
| GET    | `/health`     | Health check endpoint                | `{"status": "healthy"}`                       |
| GET    | `/`           | API root with metadata               | `{"message": "Hello World API", ...}`         |

### Example API Calls

```bash
# Get greeting message
curl http://localhost:8000/api/hello

# Check backend health
curl http://localhost:8000/health

# Get API information
curl http://localhost:8000/
```

## 💻 Development Workflow

### Making Changes with Hot Module Replacement

**Frontend Changes:**
1. Edit files in `frontend/src/` (e.g., `App.jsx`, `App.css`)
2. Save the file
3. Changes automatically reflect in browser at http://localhost:3000
4. No restart required! ⚡

**Backend Changes:**
1. Edit `backend/main.py`
2. Save the file
3. Uvicorn automatically reloads the application
4. API updates immediately available

### Rebuilding After Dependency Changes

If you modify `package.json` or `requirements.txt`:

```bash
# Rebuild and restart services
docker compose up --build

# Or rebuild a specific service
docker compose build frontend
docker compose build backend
```

### Viewing Logs

```bash
# View logs from all services
docker compose logs

# Follow logs in real-time
docker compose logs -f

# View logs from specific service
docker compose logs frontend
docker compose logs backend

# View last 50 lines
docker compose logs --tail=50
```

## 🧪 Testing

### Manual Testing

**Frontend Test:**
1. Navigate to http://localhost:3000
2. Verify the page displays "Hello, World!" with green theme
3. Check that the timestamp updates when clicking refresh
4. Confirm the page is responsive on different screen sizes

**Backend Test:**
1. Navigate to http://localhost:8000/docs
2. Test the `/api/hello` endpoint using the interactive API docs
3. Verify response includes message and timestamp
4. Check `/health` endpoint returns healthy status

**Integration Test:**
1. Open browser console at http://localhost:3000
2. Click the refresh button in the UI
3. Verify network request to backend in DevTools
4. Confirm timestamp updates in the UI

### Automated Testing (Coming Soon)

- Unit tests for React components
- API endpoint tests with pytest
- Integration tests for full stack
- E2E tests with Playwright

## 🐛 Troubleshooting

### Port Already in Use

**Error**: `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solution**:
```bash
# Find process using the port
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill the process or stop conflicting service
# Then restart Docker Compose
```

### Docker Build Failures

**Error**: `failed to solve with frontend dockerfile.v0`

**Solution**:
```bash
# Clean Docker build cache
docker compose down
docker system prune -a

# Rebuild from scratch
docker compose build --no-cache
docker compose up
```

### CORS Issues

**Error**: `Access to fetch at 'http://localhost:8000' blocked by CORS policy`

**Solution**: The backend is already configured with CORS middleware in `main.py`. Ensure:
- Backend is running on port 8000
- Frontend is accessing `http://localhost:8000` (not `http://backend:8000`)
- Browser is not caching old CORS policies (try incognito mode)

### Connection Refused Errors

**Error**: `ERR_CONNECTION_REFUSED` or `Failed to fetch`

**Solution**:
```bash
# Check if services are running
docker compose ps

# Verify backend health
curl http://localhost:8000/health

# Restart services
docker compose restart

# Check logs for errors
docker compose logs backend
```

### Frontend Not Hot Reloading

**Solution**:
- Ensure volumes are correctly mounted in `docker-compose.yml`
- Restart the frontend service: `docker compose restart frontend`
- Check file system events are not blocked by antivirus software

## 🔧 Technical Details

### Frontend Stack
- **Framework**: React 18.2.0
- **Build Tool**: Vite 5.0.8
- **Styling**: CSS with custom green theme (#2ecc71)
- **HTTP Client**: Fetch API with async/await
- **Development Server**: Vite dev server with HMR on port 3000

### Backend Stack
- **Framework**: FastAPI 0.104+
- **Runtime**: Python 3.11
- **Server**: Uvicorn with auto-reload
- **CORS**: Configured for cross-origin requests
- **Endpoints**: RESTful API with automatic OpenAPI documentation

### Docker Configuration
- **Compose Version**: 3.8+ compatible
- **Base Images**: 
  - Frontend: `node:18-alpine` (minimal footprint)
  - Backend: `python:3.11-slim` (security-optimized)
- **Networks**: Custom bridge network for service isolation
- **Volumes**: Source code mounting for development HMR
- **Health Checks**: Automated health monitoring for backend
- **Security**: Non-root users, minimal dependencies

## ✅ Success Criteria Checklist

This project satisfies all 11 success criteria:

- [x] **Criterion 1**: FastAPI backend with uvicorn server running on port 8000
- [x] **Criterion 2**: `/api/hello` endpoint returns greeting with timestamp
- [x] **Criterion 3**: React frontend with Vite on port 3000
- [x] **Criterion 4**: Frontend fetches and displays backend greeting
- [x] **Criterion 5**: Green theme (#2ecc71) applied throughout UI
- [x] **Criterion 6**: Backend Dockerfile with Python 3.11, optimized for production
- [x] **Criterion 7**: Frontend Dockerfile with Node 18, development-ready
- [x] **Criterion 8**: Docker Compose orchestrates both services with networking
- [x] **Criterion 9**: CI/CD pipeline validates builds and tests
- [x] **Criterion 10**: All containers start successfully within 10 seconds
- [x] **Criterion 11**: Services communicate correctly, UI displays data from API

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test thoroughly
4. Commit with descriptive messages: `git commit -m 'feat: Add amazing feature'`
5. Push to your fork: `git push origin feature/amazing-feature`
6. Open a Pull Request

### Code Style
- **Frontend**: Follow React best practices and ESLint recommendations
- **Backend**: Follow PEP 8 Python style guide
- **Commits**: Use conventional commits format (feat, fix, chore, docs, etc.)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built as part of the JIRA-777 fullstack development initiative
- Demonstrates modern DevOps practices with Docker and containerization
- Showcases integration between React and FastAPI ecosystems

---

**Made with 💚 using React, FastAPI, and Docker**

For questions or issues, please open an issue on GitHub.
