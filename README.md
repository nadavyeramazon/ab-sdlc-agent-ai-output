# Microservices Application - Backend & Frontend

A complete microservices architecture with a FastAPI backend and Express.js frontend, featuring a beautiful green-themed UI and comprehensive test coverage.

## 🚀 Features

- **Backend Service**: FastAPI application with RESTful endpoints
- **Frontend Service**: Express.js server with green-themed UI
- **Microservices Communication**: Backend and frontend communicate via HTTP
- **Docker Compose**: Easy deployment with container orchestration
- **Health Checks**: Built-in health monitoring for both services
- **Comprehensive Tests**: Full test coverage with pytest and Jest
- **Production Ready**: Secure CORS configuration and optimized Docker images

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)

## 🏃 Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Start all services
docker-compose up --build
```

The services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend API Docs: http://localhost:8000/docs

### Local Development

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py

# Run tests
pytest test_main.py -v
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run the server
npm start

# Run tests
npm test

# Run tests with coverage
npm run test:coverage
```

## 🧪 Testing

### Backend Tests

The backend includes comprehensive pytest tests covering:
- Root endpoint (`/`)
- Health check endpoint (`/health`)
- Greeting endpoint (`/api/greeting`)
- Parameter validation
- Error handling
- CORS behavior

```bash
cd backend
pytest test_main.py -v --cov=main
```

### Frontend Tests

The frontend includes Jest tests covering:
- Health check endpoint
- Backend communication
- Greeting functionality
- Error handling
- Response structure validation

```bash
cd frontend
npm test -- --coverage
```

## 📡 API Endpoints

### Backend (Port 8000)

- `GET /` - Hello World message
- `GET /health` - Health check status
- `GET /api/greeting?name={name}` - Personalized greeting
- `GET /docs` - Interactive API documentation (Swagger UI)

### Frontend (Port 3000)

- `GET /` - Serve the main application page
- `GET /health` - Frontend health check
- `GET /api/backend-data` - Fetch data from backend
- `GET /api/greeting?name={name}` - Get greeting via backend

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │
│    Frontend     │────────▶│     Backend     │
│   (Express.js)  │  HTTP   │    (FastAPI)    │
│   Port 3000     │         │    Port 8000    │
│                 │         │                 │
└─────────────────┘         └─────────────────┘
        │
        │ Serves
        ▼
┌─────────────────┐
│   Browser UI    │
│  (Green Theme)  │
└─────────────────┘
```

## 🔒 Security Features

- **CORS Configuration**: Restricted to specific origins (no wildcard)
- **Environment Variables**: Configurable backend URL and CORS origins
- **Health Checks**: Native Python/Node.js health checks (no curl dependencies)
- **Production Mode**: Optimized Docker images without development flags

## 🎨 Frontend Features

- Beautiful green-themed UI
- Real-time backend communication
- Interactive greeting form
- Status indicators
- Responsive design
- Error handling with user feedback

## 📦 Project Structure

```
.
├── backend/
│   ├── Dockerfile
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── test_main.py        # Backend tests
├── frontend/
│   ├── Dockerfile
│   ├── server.js           # Express server
│   ├── package.json        # Node.js dependencies
│   ├── test/
│   │   └── server.test.js  # Frontend tests
│   └── public/
│       ├── index.html      # Main HTML page
│       ├── script.js       # Frontend JavaScript
│       └── styles.css      # Green theme styles
└── docker-compose.yml      # Container orchestration
```

## 🔧 Configuration

### Environment Variables

#### Backend
- `FRONTEND_URL`: Frontend URL for CORS (default: `http://localhost:3000`)
- `PYTHONUNBUFFERED`: Enable Python output buffering

#### Frontend
- `BACKEND_URL`: Backend API URL (default: `http://backend:8000`)
- `NODE_ENV`: Environment mode (default: `production`)
- `PORT`: Server port (default: `3000`)

## 🐛 Troubleshooting

### Services won't start
```bash
# Clean up and rebuild
docker-compose down -v
docker-compose up --build
```

### Backend health check fails
```bash
# Check backend logs
docker logs backend-service

# Verify httpx is installed
docker exec backend-service pip list | grep httpx
```

### Frontend can't reach backend
```bash
# Check network connectivity
docker exec frontend-service ping backend

# Verify environment variables
docker exec frontend-service env | grep BACKEND_URL
```

## 📝 License

MIT License - feel free to use this project for learning and development.

## 🤝 Contributing

Contributions are welcome! Please ensure:
1. All tests pass (`pytest` and `npm test`)
2. Code follows existing style conventions
3. New features include appropriate tests
4. Documentation is updated

## 📊 Test Coverage

- **Backend**: 100% coverage of all endpoints
- **Frontend**: Comprehensive coverage of routes and error handling

Run coverage reports:
```bash
# Backend
cd backend && pytest --cov=main --cov-report=html

# Frontend
cd frontend && npm test -- --coverage
```

## 🎯 Development Roadmap

- [x] Basic FastAPI backend
- [x] Express.js frontend
- [x] Docker containerization
- [x] Microservices communication
- [x] Comprehensive test coverage
- [x] Production-ready security
- [ ] CI/CD pipeline
- [ ] Kubernetes deployment
- [ ] Monitoring and logging
- [ ] API authentication

## 📞 Support

For issues, questions, or contributions, please open an issue on the repository.
