# Yellow Theme Hello World Fullstack Application

![Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A modern fullstack web application featuring a yellow-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose. This project demonstrates best practices in web development, containerization, and API integration.

## 🌟 Features

- **Yellow-themed React frontend** with responsive design
- **FastAPI backend** with RESTful API endpoints
- **Docker Compose orchestration** for easy development
- **Hot Module Replacement (HMR)** for instant code updates
- **Comprehensive test coverage** for both frontend and backend
- **CORS configuration** for secure cross-origin requests
- **Health check endpoints** for monitoring
- **Loading states and error handling** for better UX

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   Frontend      │         │    Backend      │
│   React+Vite    │ ◄─────► │    FastAPI      │
│   Port 3000     │   HTTP  │    Port 8000    │
└─────────────────┘         └─────────────────┘
        │                           │
        └───────────┬───────────────┘
                    │
            Docker Network
```

## 📁 Project Structure

```
.
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Yellow theme styling
│   │   ├── main.jsx         # Entry point
│   │   ├── App.test.jsx     # Component tests
│   │   └── test/
│   │       └── setup.js     # Test configuration
│   ├── index.html           # HTML template
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   ├── Dockerfile           # Frontend container
│   └── .dockerignore
│
├── backend/                  # FastAPI backend application
│   ├── main.py              # FastAPI app with endpoints
│   ├── test_main.py         # Backend tests
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Backend container
│   └── .dockerignore
│
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI pipeline
│
├── docker-compose.yml       # Docker orchestration
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker (v20.10+)
- Docker Compose (v2.0+)

### Running the Application

1. **Clone the repository**
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
   cd ab-sdlc-agent-ai-backend
   git checkout feature/JIRA-888/fullstack-app
   ```

2. **Start the application**
   ```bash
   docker compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Stop the application**
   ```bash
   docker compose down
   ```

## 🧪 Testing

### Backend Tests

Run backend tests with pytest:

```bash
cd backend
pip install -r requirements.txt
pytest test_main.py -v
```

Test coverage:
- ✅ GET /api/hello endpoint
- ✅ GET /health endpoint
- ✅ CORS headers validation
- ✅ Response time requirements (<100ms)
- ✅ ISO-8601 timestamp format
- ✅ Error handling

### Frontend Tests

Run frontend tests with Vitest:

```bash
cd frontend
npm install
npm test
```

Test coverage:
- ✅ Component rendering
- ✅ Button click functionality
- ✅ API integration
- ✅ Loading states
- ✅ Error handling
- ✅ Yellow theme styling

### CI/CD Pipeline

GitHub Actions automatically runs tests on every push and pull request:
- Backend tests with pytest
- Frontend tests with Vitest
- Docker build validation

## 📡 API Endpoints

### GET /api/hello

Returns a hello world message with timestamp.

**Response (200 OK):**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### GET /health

Health check endpoint for service monitoring.

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

### GET /

Root endpoint providing API information.

**Response (200 OK):**
```json
{
  "name": "Yellow Theme Hello World API",
  "version": "1.0.0",
  "endpoints": {
    "/api/hello": "Get hello world message with timestamp",
    "/health": "Health check endpoint",
    "/docs": "Interactive API documentation"
  }
}
```

## 🎨 Color Theme

The application uses a bright yellow color scheme:

- **Primary**: `#FFEB3B` (bright yellow)
- **Secondary**: `#FDD835` (darker yellow)
- **Text**: `#212121` (dark gray)
- **Background**: Gradient from primary to secondary

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 18+
- **Build Tool**: Vite 5+
- **Testing**: Vitest + React Testing Library
- **Styling**: CSS3 with responsive design

### Backend
- **Framework**: FastAPI 0.109+
- **Server**: Uvicorn
- **Testing**: pytest + httpx
- **Python**: 3.11+

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **CI/CD**: GitHub Actions

## 🔧 Development

### Hot Reload

Both frontend and backend support hot reload during development:

- **Frontend**: Vite HMR automatically refreshes the browser on code changes
- **Backend**: Uvicorn `--reload` flag restarts the server on code changes

Code changes are reflected immediately without rebuilding containers.

### Environment Variables

**Frontend** (`.env`):
```env
VITE_API_URL=http://localhost:8000
```

**Backend**:
```env
PYTHONUNBUFFERED=1
```

### Adding New Features

1. Create a new branch: `git checkout -b feature/my-feature`
2. Make changes to frontend or backend
3. Write tests for new functionality
4. Run tests locally: `pytest` (backend) or `npm test` (frontend)
5. Commit and push: `git push origin feature/my-feature`
6. Create a Pull Request

## 📊 Performance

- **API Response Time**: <100ms for all endpoints
- **Container Startup**: <10 seconds
- **Frontend Build**: Vite optimized builds
- **Docker Image Sizes**: Optimized with Alpine Linux

## 🐛 Troubleshooting

### Port Already in Use

If ports 3000 or 8000 are already in use:

```bash
# Find and kill process using port 3000
lsof -ti:3000 | xargs kill -9

# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

### Docker Build Issues

Clear Docker cache and rebuild:

```bash
docker compose down -v
docker system prune -a
docker compose up --build
```

### CORS Errors

Ensure backend CORS middleware includes your frontend URL:

```python
allow_origins=[
    "http://localhost:3000",
    "http://frontend:3000",
]
```

## 📝 User Stories

### Story 1: Frontend Display ✅
- Page displays "Hello World" as prominent heading
- Yellow theme background (#FFEB3B, #FDD835)
- Text centered and responsive
- Accessible via http://localhost:3000

### Story 2: Backend API ✅
- GET /api/hello returns JSON with message and timestamp
- GET /health returns healthy status
- Backend runs on port 8000
- CORS configured for localhost:3000
- Response time <100ms

### Story 3: Frontend-Backend Integration ✅
- Button labeled "Get Message from Backend"
- Fetches data from /api/hello on click
- Displays backend message and timestamp
- Shows loading indicator during fetch
- Displays error message on failure
- Button disabled during loading

### Story 4: Docker Compose Orchestration ✅
- `docker compose up` starts both services
- Frontend accessible at http://localhost:3000
- Backend accessible at http://localhost:8000
- Services communicate via Docker network
- Vite HMR enabled for development
- Services start within 10 seconds
- `docker compose down` cleanly stops services

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Ensure all tests pass
6. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Initial Implementation**: AI-powered SDLC Agent
- **Repository**: nadavyeramazon/ab-sdlc-agent-ai-backend

## 🙏 Acknowledgments

- FastAPI for the excellent Python web framework
- React and Vite teams for modern frontend tooling
- Docker for containerization technology

---

**Built with ❤️ and ☕ using modern web technologies**
