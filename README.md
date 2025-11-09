# ❤️ Red Greeting Fullstack Application

A modern, vibrant red-themed fullstack web application featuring a FastAPI backend and vanilla JavaScript frontend, fully containerized with Docker.

## 🚀 Features

### Backend (FastAPI)
- ✅ **Health Check Endpoint** (`/health`) - Monitor service status
- ✅ **Greeting Endpoints** (`/greet`, `/howdy`) - Personalized user greetings
- ✅ **RESTful API Design** - Clean and well-documented endpoints
- ✅ **CORS Support** - Frontend-backend communication enabled
- ✅ **Input Validation** - Pydantic models for request validation
- ✅ **Comprehensive Logging** - Track all API interactions
- ✅ **Interactive API Docs** - Swagger UI and ReDoc available

### Frontend (Vanilla JavaScript)
- ✅ **Red Theme** - Bold, vibrant red color palette
- ✅ **Real-time Health Monitoring** - Live backend status checks
- ✅ **Interactive Greeting Interface** - User-friendly name input
- ✅ **Multiple Greeting Styles** - Regular greetings and "Howdy" western style
- ✅ **Responsive Design** - Mobile and desktop friendly
- ✅ **Error Handling** - Graceful error messages
- ✅ **Pure JavaScript** - No frameworks, lightweight and fast

### DevOps & Testing
- ✅ **Docker Integration** - Containerized services
- ✅ **Docker Compose** - Single-command deployment
- ✅ **GitHub Actions CI** - Automated testing and builds
- ✅ **Comprehensive Tests** - pytest test suite with 50+ tests
- ✅ **E2E Tests** - Full stack testing with curl and docker-compose
- ✅ **Security Scanning** - Trivy vulnerability checks

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Git
- Bash (for running e2e tests)

## 🏃 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Start the application:**
   ```bash
   docker compose up -d
   ```

3. **Access the application:**
   - Frontend: http://localhost:80
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Stop the application:**
   ```bash
   docker compose down
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

### Run Backend Unit Tests

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

### Run Backend Tests with Coverage

```bash
cd backend
pip install pytest-cov
pytest tests/ --cov=. --cov-report=html --cov-report=term
```

### Run E2E Tests

End-to-end tests verify the complete integration using Docker Compose and curl:

```bash
# Make script executable
chmod +x tests/e2e/test_e2e.sh

# Run e2e tests
./tests/e2e/test_e2e.sh
```

The e2e test suite includes:
- 9 Backend API tests (health, greet, howdy endpoints)
- 6 Frontend tests (accessibility, files, content)
- 5 Integration tests (CORS, documentation, theme consistency)

See [E2E Test Documentation](tests/e2e/README.md) for details.

## 📚 API Documentation

### Endpoints

#### GET `/`
Root endpoint with API information.

**Response:**
```json
{
  "message": "Welcome to Red Greeting API",
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
  "service": "red-greeting-api",
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
  "message": "Hello, Alice! Welcome to our red-themed application! ❤️",
  "name": "Alice"
}
```

#### GET `/greet/{name}`
Greet a user by name (GET variant).

**Response:**
```json
{
  "message": "Hello, Bob! Welcome to our red-themed application! ❤️",
  "name": "Bob"
}
```

#### POST `/howdy`
Greet a user with a western-style howdy message.

**Request Body:**
```json
{
  "name": "Charlie"
}
```

**Response:**
```json
{
  "message": "Howdy, Charlie! Welcome partner to our red-themed application! 🤠",
  "name": "Charlie"
}
```

#### GET `/howdy/{name}`
Greet a user with howdy (GET variant).

**Response:**
```json
{
  "message": "Howdy, Dave! Welcome partner to our red-themed application! 🤠",
  "name": "Dave"
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
│       ├── test_main.py    # Comprehensive unit tests
│       ├── test_integration.py  # Integration tests
│       ├── test_color_theme.py  # Red theme verification tests
│       └── pytest.ini      # Pytest configuration
├── frontend/
│   ├── index.html          # Main HTML page
│   ├── styles.css          # Red theme styles
│   ├── app.js              # Frontend logic
│   ├── nginx.conf          # Nginx configuration
│   └── Dockerfile          # Frontend container config
├── tests/
│   └── e2e/
│       ├── test_e2e.sh     # E2E test script
│       └── README.md       # E2E test documentation
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
4. **E2E Testing** - Full stack tests with Docker Compose and curl
5. **Integration Testing** - Test service communication
6. **Security Scanning** - Trivy vulnerability scan

## 🎨 Frontend Features

### Red Theme
- Primary color: `#8b0000` (Dark red)
- Secondary color: `#b22222` (Firebrick)
- Accent color: `#dc143c` (Crimson)
- Light background: `#ffe8e8` (Light pink-red)
- Responsive and accessible design

### User Experience
- Real-time service health status with visual indicators
- Instant feedback on user actions
- Smooth animations and transitions
- Clear error messages
- Mobile-friendly interface
- Two greeting styles (regular and "howdy" western style)

## 🔒 Security

- Input validation with Pydantic
- CORS configuration for controlled access
- Security headers in nginx
- Regular vulnerability scanning
- No hardcoded secrets
- Rate limiting ready (can be added)

## 🐛 Troubleshooting

### Backend not responding
```bash
# Check backend logs
docker compose logs backend

# Restart backend
docker compose restart backend
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

### E2E tests failing
```bash
# Clean docker environment
docker compose down -v
docker system prune -f

# Rebuild and test
docker compose up -d --build
./tests/e2e/test_e2e.sh
```

## 📊 Test Coverage

- **Backend Unit Tests**: 30+ tests covering all endpoints and edge cases
- **Integration Tests**: 10+ tests for service interactions
- **Color Theme Tests**: 10+ tests verifying red theme consistency
- **E2E Tests**: 20 comprehensive tests for full stack validation
- **Total**: 70+ automated tests

## 📝 License

This project is licensed under the Apache License 2.0.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run all tests (unit, integration, and e2e)
5. Submit a pull request

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Built with ❤️ using FastAPI and Vanilla JavaScript**
