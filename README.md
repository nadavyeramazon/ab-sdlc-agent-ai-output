# 🌿 Green Greeting Fullstack Application

A modern, eco-friendly themed fullstack web application featuring a FastAPI backend and vanilla JavaScript frontend, fully containerized with Docker.

## 🚀 Features

### Backend (FastAPI)
- ✅ **Health Check Endpoint** (`/health`) - Monitor service status
- ✅ **Greeting Endpoint** (`/greet`) - Personalized user greetings
- ✅ **RESTful API Design** - Clean and well-documented endpoints
- ✅ **CORS Support** - Frontend-backend communication enabled
- ✅ **Input Validation** - Pydantic models for request validation
- ✅ **Comprehensive Logging** - Track all API interactions
- ✅ **Interactive API Docs** - Swagger UI and ReDoc available

### Frontend (Vanilla JavaScript)
- ✅ **Green Theme** - Eco-friendly color palette
- ✅ **Real-time Health Monitoring** - Live backend status checks
- ✅ **Interactive Greeting Interface** - User-friendly name input
- ✅ **Responsive Design** - Mobile and desktop friendly
- ✅ **Error Handling** - Graceful error messages
- ✅ **Pure JavaScript** - No frameworks, lightweight and fast

### DevOps
- ✅ **Docker Integration** - Containerized services
- ✅ **Docker Compose** - Single-command deployment
- ✅ **GitHub Actions CI** - Automated testing and builds
- ✅ **Comprehensive Tests** - pytest test suite with 30+ tests
- ✅ **Security Scanning** - Trivy vulnerability checks

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Git

## 🏃 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Start the application:**
   ```bash
   docker-compose up -d
   ```

3. **Access the application:**
   - Frontend: http://localhost:80
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

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
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Serve with any static file server, e.g.:
python -m http.server 8080

# Or use nginx, serve, etc.
```

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

### Run Tests with Coverage

```bash
cd backend
pip install pytest-cov
pytest tests/ --cov=. --cov-report=html --cov-report=term
```

### Integration Tests

Integration tests run automatically in the CI pipeline using Docker Compose.

## 📚 API Documentation

### Endpoints

#### GET `/`
Root endpoint with API information.

**Response:**
```json
{
  "message": "Welcome to Green Greeting API",
  "docs": "/docs",
  "health": "/health"
}
```

#### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "green-greeting-api",
  "version": "1.0.0"
}
```

#### POST `/greet`
Greet a user by name.

**Request Body:**
```json
{
  "name": "Alice"
}
```

**Response:**
```json
{
  "message": "Hello, Alice! Welcome to our green-themed application! 🌿",
  "name": "Alice"
}
```

#### GET `/greet/{name}`
Greet a user by name (GET variant).

**Response:**
```json
{
  "message": "Hello, Bob! Welcome to our green-themed application! 🌿",
  "name": "Bob"
}
```

## 🏗️ Architecture

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Backend container config
│   └── tests/
│       ├── __init__.py
│       ├── test_main.py    # Comprehensive test suite
│       └── pytest.ini      # Pytest configuration
├── frontend/
│   ├── index.html          # Main HTML page
│   ├── styles.css          # Green theme styles
│   ├── app.js              # Frontend logic
│   ├── nginx.conf          # Nginx configuration
│   └── Dockerfile          # Frontend container config
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI pipeline
├── docker-compose.yml      # Multi-container orchestration
└── README.md
```

## 🔄 CI/CD Pipeline

The GitHub Actions CI pipeline includes:

1. **Backend Testing** - Run pytest suite with coverage
2. **Backend Linting** - flake8 and black checks
3. **Docker Build** - Build backend and frontend images
4. **Integration Testing** - Test services with Docker Compose
5. **Security Scanning** - Trivy vulnerability scan

## 🎨 Frontend Features

### Green Theme
- Primary color: `#2d5016` (Dark green)
- Accent colors: Various shades of green
- Background: Light green gradient
- Responsive and accessible design

### User Experience
- Real-time service health status
- Instant feedback on user actions
- Smooth animations and transitions
- Clear error messages
- Mobile-friendly interface

## 🔒 Security

- Input validation with Pydantic
- CORS configuration for controlled access
- Security headers in nginx
- Regular vulnerability scanning
- No hardcoded secrets

## 🐛 Troubleshooting

### Backend not responding
```bash
# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

### Frontend can't connect to backend
1. Ensure backend is running: `curl http://localhost:8000/health`
2. Check CORS configuration in `backend/main.py`
3. Verify network connectivity in `docker-compose.yml`

### Tests failing
```bash
# Clean install dependencies
cd backend
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
```

## 📝 License

This project is licensed under the Apache License 2.0.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Built with ❤️ and 🌿 using FastAPI and Vanilla JavaScript**
