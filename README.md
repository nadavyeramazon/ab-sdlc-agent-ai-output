# Green Theme Hello World Fullstack Application

A simple fullstack "Hello World" application with a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose.

## 🎨 Features

### Frontend (React)
- **Green-themed UI** with modern, responsive design
- **React 18+** with functional components and hooks
- **Vite** for fast development and hot module replacement (HMR)
- **Interactive button** to fetch data from backend
- **Loading states** and error handling
- **Accessible** with proper ARIA labels

### Backend (FastAPI)
- **FastAPI** REST API with two endpoints:
  - `GET /api/hello` - Returns hello message with timestamp
  - `GET /health` - Health check endpoint
- **CORS enabled** for frontend communication
- **Fast response times** (<100ms)
- **Python 3.11+** with modern async/await patterns

### DevOps
- **Docker Compose** orchestration for easy local development
- **GitHub Actions CI/CD** pipeline with automated tests
- **Comprehensive test suite** for both frontend and backend
- **Hot reload** enabled for rapid development

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

### Running with Docker Compose (Recommended)

```bash
# Start both frontend and backend services
docker compose up

# Or run in detached mode
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Running Locally (Development)

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pip install -r requirements.txt
pytest test_main.py -v
```

### Frontend Tests
```bash
cd frontend
npm install
npm test

# Watch mode
npm run test:watch
```

### Run All Tests (CI)
The GitHub Actions workflow automatically runs all tests on push and pull requests:
- Backend tests with pytest
- Frontend tests with Vitest
- Docker build verification
- Integration tests with Docker Compose

## 📁 Project Structure

```
project-root/
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── App.css           # Green theme styles
│   │   ├── App.test.jsx      # Component tests
│   │   ├── main.jsx          # React entry point
│   │   ├── index.css         # Global styles
│   │   └── setupTests.js     # Test configuration
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js        # Vite configuration
│   ├── Dockerfile            # Production build
│   ├── Dockerfile.dev        # Development with HMR
│   └── nginx.conf            # Nginx configuration
├── backend/
│   ├── main.py               # FastAPI application
│   ├── test_main.py          # Backend tests
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile            # Backend container
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI/CD
├── docker-compose.yml        # Docker orchestration
└── README.md
```

## 🎯 API Endpoints

### GET /api/hello
Returns a hello message with timestamp.

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-01T12:00:00.000000"
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

## 🎨 Design

### Color Theme
- **Primary Green:** `#2ecc71`
- **Secondary Green:** `#27ae60`
- **Background:** Linear gradient from primary to secondary
- **Card Background:** White with shadow
- **Success Messages:** Light green background
- **Error Messages:** Light red background

### Responsive Design
- Mobile-first approach
- Breakpoints at 768px and 480px
- Centered layout with padding adjustments
- Touch-friendly button sizes

## 🐳 Docker Configuration

### Service Names
In Docker Compose, services communicate using service names:
- Backend service: `backend`
- Frontend service: `frontend`

### Environment Variables
- **Frontend:** `VITE_API_URL=http://backend:8000` (set in docker-compose.yml)
- **Backend:** `PYTHONUNBUFFERED=1` for real-time logs

### Networking
Both services are on the same Docker network (`app-network`) and can communicate using service names.

## 🔧 Development

### Hot Reload
- **Frontend:** Vite HMR automatically enabled
- **Backend:** Uvicorn `--reload` flag enabled

### Adding Features
1. Implement feature in respective directory (frontend/backend)
2. Write tests for the feature
3. Update this README if needed
4. Submit a pull request

## 📊 CI/CD Pipeline

The GitHub Actions workflow includes:
1. **Backend Tests** - Runs pytest on all backend tests
2. **Frontend Tests** - Runs Vitest on all component tests
3. **Docker Build** - Verifies Docker images build successfully
4. **Integration Tests** - Tests the full application with Docker Compose

**Workflow triggers on:**
- Push to `main` branch
- Push to `feature/**` branches
- Pull requests to `main` branch

## 🎓 Technical Highlights

### Docker Networking
- ✅ Frontend uses backend **service name** (`http://backend:8000`) not localhost
- ✅ Fallback to localhost for local development outside Docker
- ✅ CORS configured for both service name and localhost origins

### Best Practices
- **Clean Code:** Well-commented and maintainable
- **Error Handling:** Comprehensive error boundaries
- **Testing:** High test coverage with unit and integration tests
- **Accessibility:** Proper ARIA labels and semantic HTML
- **Performance:** Optimized with caching and lazy loading
- **Security:** Security headers in Nginx configuration

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚡ Performance

- **API Response Time:** <100ms (as per requirements)
- **Service Startup:** <10 seconds (as per requirements)
- **Frontend Load Time:** <2 seconds on modern browsers

## 🔍 Troubleshooting

### Port Already in Use
```bash
# Check what's using the port
lsof -i :3000  # Frontend
lsof -i :8000  # Backend

# Kill the process or use different ports in docker-compose.yml
```

### Docker Compose Issues
```bash
# Rebuild containers
docker compose build --no-cache

# Remove all containers and volumes
docker compose down -v

# View logs
docker compose logs -f backend
docker compose logs -f frontend
```

### Frontend Cannot Connect to Backend
- Ensure both services are running: `docker compose ps`
- Check backend health: `curl http://localhost:8000/health`
- Verify CORS configuration in `backend/main.py`
- Check environment variable: `VITE_API_URL` should be set to `http://backend:8000` in Docker

---

**Built with ❤️ using React, FastAPI, and Docker**
