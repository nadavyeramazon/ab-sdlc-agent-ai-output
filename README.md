# Green Theme Hello World Fullstack Application

A simple fullstack "Hello World" application demonstrating frontend-backend integration with a green-themed React frontend and Python FastAPI backend, orchestrated via Docker Compose for local development.

## 🎯 Features

- **Green-themed (#2ecc71) responsive UI** - Beautiful, modern interface
- **Dynamic data fetching from backend** - Real-time API integration
- **Hot module replacement (HMR)** - Rapid development with instant updates
- **Health check endpoint** - Service monitoring and status verification
- **Comprehensive test coverage** - Backend pytest and frontend React Testing Library tests
- **CI/CD pipeline** - Automated testing with GitHub Actions

## 🏗️ Architecture

```
├── frontend/                 # React + Vite frontend application
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Green theme styling
│   │   ├── App.test.jsx     # Frontend tests
│   │   ├── main.jsx         # React entry point
│   │   └── test/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js       # Vite configuration
│   ├── Dockerfile           # Production build
│   └── Dockerfile.dev       # Development build with HMR
├── backend/                  # FastAPI backend application
│   ├── main.py              # FastAPI application
│   ├── test_main.py         # Backend tests
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD pipeline
├── docker-compose.yml       # Orchestration configuration
└── README.md               # This file
```

## 📋 Prerequisites

Before running this application, ensure you have the following installed:

- **Docker** (version 20.10+)
- **Docker Compose** (version 2.x)

Optional for local development:
- **Node.js** (version 18+)
- **Python** (version 3.11+)

## 🚀 Quick Start

### Start the Application

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Start both frontend and backend services:
   ```bash
   docker compose up --build
   ```

3. Wait for services to start (typically 10-15 seconds)

4. Access the application:
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health

### Stop the Application

```bash
docker compose down
```

## 🧪 Running Tests

### Backend Tests (pytest)

```bash
# Using Docker
docker compose exec backend pytest test_main.py -v

# Or locally (requires Python 3.11+)
cd backend
pip install -r requirements.txt
pytest test_main.py -v
```

### Frontend Tests (Vitest + React Testing Library)

```bash
# Using Docker
docker compose exec frontend npm test

# Or locally (requires Node.js 18+)
cd frontend
npm install
npm test
```

### All Tests via CI/CD

The GitHub Actions workflow automatically runs all tests on push and pull requests. Check the `.github/workflows/ci.yml` file for details.

## 📡 API Endpoints

### GET /api/hello

Returns a greeting message with timestamp.

**Request:**
```bash
curl http://localhost:8000/api/hello
```

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:45.123Z"
}
```

### GET /health

Health check endpoint for service monitoring.

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy"
}
```

## 🎨 User Interface

### Features

- **Static "Hello World" heading** - Prominent H1 with green theme
- **Interactive button** - "Get Message from Backend" triggers API call
- **Loading state** - Visual feedback during API requests
- **Response display** - Shows backend message and timestamp
- **Error handling** - User-friendly error messages
- **Responsive design** - Works on mobile (320px+), tablet, and desktop

### Color Palette

- **Primary Green**: #2ecc71
- **Secondary Green**: #27ae60
- **Text**: #2c3e50
- **Background**: #ecf0f1
- **Error Red**: #e74c3c

## 🔧 Development

### Hot Module Replacement (HMR)

The frontend supports HMR for rapid development. Edit any file in `frontend/src/` and see changes instantly without page refresh.

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
```

### Rebuild Services

```bash
# Rebuild all
docker compose up --build

# Rebuild specific service
docker compose up --build backend
```

## 🐛 Troubleshooting

### Backend not responding

1. Check if backend container is running:
   ```bash
   docker compose ps
   ```

2. Check backend logs:
   ```bash
   docker compose logs backend
   ```

3. Verify health endpoint:
   ```bash
   curl http://localhost:8000/health
   ```

### Frontend shows "Failed to fetch data"

1. Ensure backend is running and healthy
2. Check CORS configuration in `backend/main.py`
3. Verify network connectivity:
   ```bash
   docker compose exec frontend ping backend
   ```

### Port already in use

If ports 3000 or 8000 are already in use:

1. Stop conflicting services
2. Or modify ports in `docker-compose.yml`

### Docker Compose fails to start

1. Ensure Docker daemon is running
2. Check Docker Compose version: `docker compose version`
3. Try cleaning up: `docker system prune`

### HMR not working

1. Ensure volumes are properly mounted in `docker-compose.yml`
2. Check that polling is enabled in `vite.config.js`
3. Restart frontend service: `docker compose restart frontend`

## 📊 Performance Requirements

- **Frontend initial load**: < 2 seconds
- **Backend API response**: < 100ms (95th percentile)
- **Docker services startup**: < 10 seconds
- **Vite HMR updates**: < 500ms

## ✅ Success Criteria

The application meets all success criteria:

- ✅ User can access frontend at http://localhost:3000
- ✅ Page displays "Hello World" with green theme
- ✅ Button fetches data from backend
- ✅ Backend response is displayed with timestamp
- ✅ Health endpoint returns healthy status
- ✅ Loading indicator during API requests
- ✅ Error handling for failed requests
- ✅ `docker compose up` starts both services
- ✅ Services communicate via Docker network
- ✅ Vite HMR enables live code updates
- ✅ CORS properly configured
- ✅ Comprehensive test coverage
- ✅ Responsive on all viewport sizes

## 🧪 Test Coverage

### Backend Tests

- ✅ GET /api/hello returns correct JSON structure
- ✅ Timestamp is valid ISO 8601 format
- ✅ GET /health returns healthy status
- ✅ CORS headers present in responses
- ✅ Response time within acceptable range
- ✅ Multiple requests return different timestamps

### Frontend Tests

- ✅ Hello World heading renders
- ✅ Button renders and is clickable
- ✅ Loading state displays during API call
- ✅ Backend response displays correctly
- ✅ Error messages display on failure
- ✅ Timeout error handling
- ✅ State management (clearing previous messages/errors)
- ✅ Accessibility (ARIA labels, live regions)

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please ensure:

1. All tests pass: `pytest` and `npm test`
2. Code follows style guidelines (PEP 8 for Python, ESLint for JavaScript)
3. Add tests for new features
4. Update documentation as needed

## 📞 Support

For issues and questions:

1. Check the Troubleshooting section above
2. Review Docker logs: `docker compose logs`
3. Open an issue on GitHub

---

**Built with ❤️ using React, FastAPI, and Docker**
