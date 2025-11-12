# Backend Quick Start Guide

🚀 **Get up and running with the Green Theme Backend in 2 minutes!**

---

## ⚡ Instant Setup (Docker)

```bash
# From project root
docker-compose up backend

# Backend will be available at http://localhost:8000
```

**That's it!** ✨

---

## 💻 Local Development Setup

### Prerequisites
- Python 3.11+
- pip

### Steps

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server with hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Server running at**: http://localhost:8000

---

## ✅ Verify Installation

### 1. Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456+00:00",
  "service": "green-theme-backend"
}
```

### 2. Hello Endpoint
```bash
curl http://localhost:8000/api/hello
```

**Expected Response**:
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:45.123456+00:00",
  "status": "success"
}
```

### 3. API Documentation
Open in browser: http://localhost:8000/docs

---

## 🧪 Run Tests

```bash
cd backend

# Run all tests
pytest -v

# Run with coverage
pytest --cov=. --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_main.py -v

# Run AC compliance tests
pytest tests/test_ac_compliance.py -v
```

**Expected**: 60+ tests passing, 85%+ coverage

---

## 📦 Available Endpoints

| Endpoint | Method | Description | Response Time |
|----------|--------|-------------|---------------|
| `/` | GET | API information | ~5ms |
| `/health` | GET | Health check | ~5ms |
| `/api/hello` | GET | Hello World message | ~10ms |
| `/api/hello/{name}` | GET | Personalized greeting | ~12ms |
| `/docs` | GET | Swagger UI documentation | ~15ms |
| `/redoc` | GET | ReDoc documentation | ~15ms |

---

## 🔧 Common Commands

### Development
```bash
# Start with hot reload
uvicorn main:app --reload --port 8000

# Start with custom host
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run directly
python main.py
```

### Testing
```bash
# All tests
pytest -v

# With coverage
pytest --cov=. --cov-report=html

# Watch mode (requires pytest-watch)
ptw -- -v

# Performance tests only
pytest tests/test_main.py::TestPerformanceRequirements -v
```

### Docker
```bash
# Build image
docker build -t green-backend .

# Run container
docker run -p 8000:8000 green-backend

# With Docker Compose
docker-compose up backend

# View logs
docker-compose logs -f backend

# Stop
docker-compose down
```

---

## 📝 Environment Variables

```bash
# Optional - defaults work out of the box
PYTHONUNBUFFERED=1          # Enable Python output buffering
ENVIRONMENT=development      # Environment mode
PYTHONDONTWRITEBYTECODE=1  # Disable .pyc files
```

---

## 🐛 Troubleshooting

### Port already in use
```bash
# Find process using port 8000
lsof -ti:8000

# Kill process
kill -9 $(lsof -ti:8000)

# Or use different port
uvicorn main:app --reload --port 8001
```

### Dependencies issue
```bash
# Upgrade pip
pip install --upgrade pip

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear pip cache
pip cache purge
```

### Docker issues
```bash
# Rebuild without cache
docker-compose build --no-cache backend

# Remove all containers and volumes
docker-compose down -v

# Clean Docker system
docker system prune -a
```

### Tests failing
```bash
# Clear pytest cache
rm -rf .pytest_cache __pycache__

# Run tests in verbose mode
pytest -vv

# Run specific failing test
pytest tests/test_main.py::TestHelloEndpoint::test_hello_world_exact_format -vv
```

---

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs (when running)
- **Implementation Summary**: `BACKEND_IMPLEMENTATION_SUMMARY.md`
- **Testing Guide**: `TESTING_GUIDE.md`
- **AC Compliance**: `AC_COMPLIANCE.md`
- **Production Guide**: `PRODUCTION_READINESS.md`

---

## 🏃 Next Steps

1. ✅ Start the backend server
2. ✅ Test endpoints with curl or browser
3. ✅ Run the test suite
4. ✅ Explore API documentation at /docs
5. ✅ Start frontend to see full integration

---

## 🔗 Quick Links

- **Backend Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Hello Endpoint**: http://localhost:8000/api/hello

---

## 💡 Pro Tips

1. **Hot Reload**: Changes to `main.py` auto-reload the server
2. **Interactive API Docs**: Use `/docs` to test endpoints in browser
3. **Test Coverage**: Open `htmlcov/index.html` after coverage report
4. **Performance**: Response times are typically 5-25ms
5. **CORS**: Frontend at localhost:3000 is pre-configured

---

## ✅ Success Indicators

- ✅ Server starts without errors
- ✅ Health check returns `{"status": "healthy"}`
- ✅ All 60+ tests pass
- ✅ Coverage > 80%
- ✅ API docs accessible at /docs
- ✅ Response times < 100ms

---

**Need more help?** Check the comprehensive `BACKEND_IMPLEMENTATION_SUMMARY.md` 📚

**Happy coding!** 🚀💚
