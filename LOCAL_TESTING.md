# Local Testing Guide - Green Theme Hello World Fullstack

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Node.js 18+ (for local frontend dev)
- Python 3.11+ (for local backend dev)

## 🐳 Docker Compose (Recommended)

### Start Everything
```bash
# Start both frontend and backend with hot reload
docker-compose up

# Or run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Stop Services
```bash
# Stop and remove containers
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v
```

### Production Build
```bash
# Run production frontend build
docker-compose --profile prod up

# Access production frontend on http://localhost:3001
```

## 🐍 Backend Testing (Local)

### Setup
```bash
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
```

### Run Backend Server
```bash
# Development with hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or use the Makefile
make run
```

### Run Backend Tests
```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=. --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_main.py -v

# Run with detailed output
pytest -vv --tb=short

# Generate coverage report
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

### Backend Test Structure
```
backend/tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_main.py            # Main API tests
└── test_ac_compliance.py   # Acceptance criteria tests
```

## ⚛️ Frontend Testing (Local)

### Setup
```bash
cd frontend

# Install dependencies
npm install

# Or use clean install (recommended for CI)
npm ci
```

### Run Frontend Dev Server
```bash
# Start Vite dev server with HMR
npm run dev

# Access at http://localhost:3000
```

### Run Frontend Tests
```bash
# Run tests in watch mode
npm test

# Run tests once (CI mode)
npm run test:coverage

# Run with UI
npm run test:ui

# Run specific test file
npm test -- src/__tests__/App.test.jsx
```

### Run Linting
```bash
# Check for lint errors
npm run lint

# Fix auto-fixable issues
npm run lint -- --fix
```

### Build Frontend
```bash
# Create production build
npm run build

# Preview production build
npm run preview
```

### Frontend Test Structure
```
frontend/src/
├── __tests__/          # Component tests
│   └── App.test.jsx
├── components/
│   └── __tests__/     # Component-specific tests
└── test/
    └── setup.js       # Test configuration
```

## 🧪 Running Tests Like CI

### Complete CI Test Simulation
```bash
# 1. Backend Tests
cd backend
pip install -r requirements.txt
pytest -v --cov=. --cov-report=xml --cov-report=term-missing

# 2. Frontend Tests
cd ../frontend
npm ci
npm run lint
npm run test:coverage
npm run build

# 3. Integration Tests (requires Docker)
cd ..
docker-compose build
docker-compose up -d

# Wait for services to be ready
sleep 10

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/
curl http://localhost:8000/api/hello
curl http://localhost:3000

# Cleanup
docker-compose down -v
```

## 🔧 Hot Reload Configuration

### Backend Hot Reload
The backend uses uvicorn's `--reload` flag:
```bash
uvicorn main:app --reload
```

**In Docker:**
```yaml
command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
volumes:
  - ./backend:/app  # Source code mounted
```

Edit any `.py` file in `backend/` and the server will automatically restart.

### Frontend Hot Reload (HMR)
Vite provides Hot Module Replacement:
```bash
npm run dev
```

**In Docker:**
```yaml
environment:
  - CHOKIDAR_USEPOLLING=true  # For Docker file watching
volumes:
  - ./frontend:/app
  - /app/node_modules  # Prevent overwriting
```

Edit any `.jsx`, `.css`, or other frontend files and changes appear instantly in the browser.

## 🔍 Troubleshooting

### Backend Won't Start
```bash
# Check if port 8000 is in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or use a different port
uvicorn main:app --reload --port 8001
```

### Frontend Won't Start
```bash
# Clear npm cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check if port 3000 is in use
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows
```

### Tests Failing Locally But Pass in CI
```bash
# Ensure you're using the right versions
python --version  # Should be 3.11+
node --version    # Should be 18+

# Clear all caches
pip cache purge
npm cache clean --force

# Reinstall from scratch
cd backend && pip install -r requirements.txt
cd ../frontend && npm ci
```

### Docker Issues
```bash
# Remove all containers and volumes
docker-compose down -v

# Rebuild from scratch
docker-compose build --no-cache

# Check logs
docker-compose logs backend
docker-compose logs frontend

# Check running containers
docker ps

# Enter container for debugging
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Module Not Found Errors

**Backend:**
```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=.
pytest

# Or use pytest from the backend directory
cd backend
pytest
```

**Frontend:**
```bash
# Reinstall dependencies
rm -rf node_modules
npm install
```

## 📊 Coverage Reports

### View Backend Coverage
```bash
cd backend
pytest --cov=. --cov-report=html

# Open in browser
# macOS:
open htmlcov/index.html
# Linux:
xdg-open htmlcov/index.html
# Windows:
start htmlcov/index.html
```

### View Frontend Coverage
```bash
cd frontend
npm run test:coverage

# Open in browser
# macOS:
open coverage/index.html
# Linux:
xdg-open coverage/index.html
# Windows:
start coverage/index.html
```

## ⚙️ Environment Variables

### Backend (.env)
```bash
cp backend/.env.example backend/.env

# Edit backend/.env:
ENVIRONMENT=development
DEBUG=true
```

### Frontend
Vite automatically loads `.env` files:
```bash
# frontend/.env.local
VITE_API_URL=http://localhost:8000
```

## 🎯 Test Coverage Goals

- Backend: >80% coverage
- Frontend: >80% coverage
- Integration: All endpoints tested

## 📝 Quick Commands

```bash
# Complete local test run
make test-all  # If Makefile exists

# Or manually:
cd backend && pytest -v && cd ../frontend && npm test && cd ..

# Docker quick test
docker-compose up -d && sleep 10 && curl http://localhost:8000/health && curl http://localhost:3000 && docker-compose down

# Clean everything
docker-compose down -v
rm -rf backend/__pycache__ backend/.pytest_cache backend/htmlcov
rm -rf frontend/node_modules frontend/dist frontend/coverage
```

## 🚀 Next Steps

1. Start services: `docker-compose up`
2. Run tests locally before pushing
3. Push to feature branch
4. CI pipeline runs automatically
5. Review CI results in GitHub Actions
6. Merge when all checks pass

---

**Need Help?**
- Check `.github/README-CI.md` for CI/CD documentation
- Review `README.md` for project overview
- See GitHub Actions logs for detailed error messages
