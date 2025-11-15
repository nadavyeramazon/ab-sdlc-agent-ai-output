# Green Theme Hello World Fullstack Application

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-teal.svg)

A simple fullstack "Hello World" application demonstrating modern web development practices with a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose for local development.

## 🌟 Features

- **Modern React Frontend**: Built with React 18+ and Vite for fast development
- **FastAPI Backend**: High-performance Python API with automatic documentation
- **Green Theme UI**: Beautiful, responsive design with custom color palette
- **Docker Compose**: One-command setup for both services
- **Hot Module Reload**: Instant updates during development
- **CORS Configured**: Seamless frontend-backend communication
- **Comprehensive Tests**: pytest suite for backend API validation
- **CI/CD Ready**: GitHub Actions workflow for automated testing

## 📋 Prerequisites

Before running this application, ensure you have the following installed:

- **Docker**: Version 20.10 or higher ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose**: Version 2.0 or higher (usually included with Docker Desktop)

### Verify Installation

```bash
docker --version
docker compose version
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
git checkout feature/JIRA-777/fullstack-app
```

### 2. Start the Application

```bash
docker compose up --build
```

This single command will:
- Build Docker images for frontend and backend
- Start both services with proper networking
- Enable hot module reload for development
- Display logs from both services

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative API Docs**: http://localhost:8000/redoc (ReDoc)

### 4. Stop the Application

```bash
docker compose down
```

## 🏗️ Project Structure

```
project-root/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Green theme styles
│   │   └── main.jsx         # React entry point
│   ├── index.html           # HTML template
│   ├── package.json         # npm dependencies
│   ├── vite.config.js       # Vite configuration
│   └── Dockerfile           # Frontend container
│
├── backend/                 # FastAPI backend application
│   ├── main.py             # FastAPI app with routes
│   ├── requirements.txt    # Python dependencies
│   ├── test_main.py        # pytest test suite
│   └── Dockerfile          # Backend container
│
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI pipeline
│
├── docker-compose.yml      # Multi-service orchestration
└── README.md              # This file
```

## 🎨 User Stories Implementation

### Story 1: Static Frontend Display ✅
- Green-themed page with "Hello World" heading
- Responsive design for all screen sizes
- Centered layout using modern CSS
- Accessible at http://localhost:3000

### Story 2: Backend API Endpoints ✅
- `GET /api/hello`: Returns message with ISO 8601 timestamp
- `GET /health`: Health check endpoint
- CORS configured for frontend communication
- Fast response times (<100ms)

### Story 3: Frontend-Backend Integration ✅
- Interactive "Get Message from Backend" button
- Loading indicator during API calls
- Success message display with timestamp
- User-friendly error handling
- Button disabled during loading

### Story 4: Docker Compose Orchestration ✅
- Single `docker compose up` command starts all services
- Hot module reload for rapid development
- Services communicate via Docker network
- Clean shutdown with `docker compose down`

## 🧪 Testing

### Run Backend Tests

The backend includes a comprehensive pytest test suite that validates all API endpoints.

#### Option 1: Run Tests in Docker

```bash
# Start the backend service
docker compose up -d backend

# Run tests inside the container
docker compose exec backend pytest test_main.py -v

# Or run with coverage
docker compose exec backend pytest test_main.py -v --cov=main
```

#### Option 2: Run Tests Locally

```bash
cd backend
pip install -r requirements.txt
pytest test_main.py -v
```

### Test Coverage

The test suite includes:
- ✅ API endpoint functionality tests
- ✅ Response format validation
- ✅ ISO 8601 timestamp verification
- ✅ CORS configuration tests
- ✅ Performance benchmarks
- ✅ Error handling validation

### CI/CD Pipeline

GitHub Actions automatically runs tests on every push and pull request:
- Backend pytest suite
- Code quality checks
- Test results displayed in PR

## 🔧 Development

### Hot Module Reload

Both frontend and backend support hot reload:

**Frontend (Vite HMR)**:
- Edit files in `frontend/src/`
- Changes appear instantly in browser
- No page refresh needed

**Backend (Uvicorn reload)**:
- Edit `backend/main.py`
- Server automatically restarts
- API changes available immediately

### Environment Variables

**Frontend** (`frontend/`):
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)

**Backend** (`backend/`):
- `PYTHONUNBUFFERED`: Enable real-time logging (set to 1)

### Port Configuration

- Frontend: `3000` (configured in `vite.config.js`)
- Backend: `8000` (configured in `main.py` and `Dockerfile`)

To change ports, update:
1. `docker-compose.yml` port mappings
2. `vite.config.js` server.port (frontend)
3. CORS origins in `backend/main.py`

## 🌈 Color Theme

The application uses a beautiful green color palette:

- **Primary Green**: `#2ecc71`
- **Secondary Green**: `#27ae60`
- **White Text**: `#ffffff`
- **Error Red**: `#e74c3c`

## 📚 API Documentation

### GET /api/hello

**Description**: Returns a hello world message with current timestamp

**Response** (200 OK):
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00.123456Z"
}
```

### GET /health

**Description**: Health check endpoint for monitoring

**Response** (200 OK):
```json
{
  "status": "healthy"
}
```

### Interactive API Documentation

FastAPI provides automatic interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐛 Troubleshooting

### Services Won't Start

**Issue**: Port already in use
```
Error: Bind for 0.0.0.0:3000 failed: port is already allocated
```

**Solution**: Stop other services using ports 3000 or 8000
```bash
# Find process using port
lsof -i :3000  # or :8000

# Kill the process
kill -9 <PID>
```

### Frontend Can't Connect to Backend

**Issue**: CORS errors or connection refused

**Solution**:
1. Ensure backend is running: `docker compose ps`
2. Check backend logs: `docker compose logs backend`
3. Verify CORS origins in `backend/main.py` include your frontend URL
4. Try accessing backend directly: http://localhost:8000/health

### Docker Build Fails

**Issue**: Build errors or dependency issues

**Solution**:
```bash
# Clean Docker cache and rebuild
docker compose down -v
docker system prune -f
docker compose up --build --force-recreate
```

### Hot Reload Not Working

**Issue**: Changes not reflected automatically

**Solution**:
- Ensure volumes are properly mounted in `docker-compose.yml`
- Try restarting services: `docker compose restart`
- Check file permissions on mounted volumes

### Backend Tests Fail

**Issue**: pytest failures

**Solution**:
1. Check backend is running: `docker compose up -d backend`
2. View backend logs: `docker compose logs backend`
3. Run tests with verbose output: `docker compose exec backend pytest -v`

## 📦 Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🎯 Success Criteria

- ✅ Frontend accessible at http://localhost:3000
- ✅ Backend accessible at http://localhost:8000
- ✅ API returns correct JSON format
- ✅ Health check returns healthy status
- ✅ Interactive button fetches backend data
- ✅ Error handling displays user-friendly messages
- ✅ Docker Compose orchestrates both services
- ✅ Hot reload works for development
- ✅ CORS properly configured
- ✅ Responsive design works on all screen sizes
- ✅ Comprehensive test suite with pytest
- ✅ CI/CD pipeline with GitHub Actions

## 📞 Support

For issues, questions, or contributions:
- Open an issue in this repository
- Check existing documentation
- Review the troubleshooting section above

## 🚀 Next Steps

This is a demonstration application. For production deployment, consider:
- Add authentication and authorization
- Implement database integration
- Add comprehensive logging and monitoring
- Configure production-grade CORS settings
- Set up HTTPS/TLS
- Implement rate limiting
- Add end-to-end tests
- Configure environment-specific settings

---

**Built with ❤️ using React, FastAPI, and Docker**
