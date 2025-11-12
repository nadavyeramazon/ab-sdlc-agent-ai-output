# CI/CD Pipeline - Green Theme Hello World Fullstack

## 🚀 Overview

Comprehensive GitHub Actions CI/CD pipeline for the Green Theme Hello World Fullstack Application, featuring parallel testing, comprehensive validation, and deployment readiness checks.

## 📋 Workflow Structure

### Trigger Events
- **Push**: `main`, `develop`, `feature/**` branches
- **Pull Request**: targeting `main` or `develop`
- **Manual**: `workflow_dispatch` for manual runs

### Concurrency Control
Automatically cancels in-progress runs for the same workflow and branch to save resources.

## 🔧 Jobs

### 1. Backend Tests (Python 3.11 + FastAPI + pytest)
**Duration:** ~5-10 minutes

**Steps:**
- ✅ Checkout code
- ✅ Setup Python 3.11 with pip caching
- ✅ Install dependencies from `backend/requirements.txt`
- ✅ Run pytest with coverage
- ✅ Upload coverage to Codecov
- ✅ Generate test artifacts

**Key Features:**
- Uses pip caching for faster dependency installation
- Comprehensive test coverage reporting
- JUnit XML test results for GitHub Actions
- HTML coverage reports as artifacts

**Commands:**
```bash
cd backend
pip install -r requirements.txt
pytest -v --cov=. --cov-report=xml --cov-report=html
```

### 2. Frontend Tests (Node 18 + React + Vitest)
**Duration:** ~5-10 minutes

**Steps:**
- ✅ Checkout code
- ✅ Setup Node.js 18 with npm caching
- ✅ Install dependencies from `frontend/package.json`
- ✅ Run ESLint for code quality
- ✅ Run Vitest with coverage
- ✅ Build production bundle
- ✅ Upload artifacts

**Key Features:**
- npm dependency caching for speed
- ESLint validation (must pass)
- Vitest test runner with coverage
- Production build verification

**Commands:**
```bash
cd frontend
npm ci
npm run lint
npm run test:coverage
npm run build
```

### 3. Integration Tests (Docker Compose)
**Duration:** ~10-15 minutes

**Dependencies:** Requires `backend-tests` and `frontend-tests` to pass

**Steps:**
- ✅ Build Docker images for backend and frontend
- ✅ Start services with `docker-compose up`
- ✅ Wait for backend health check (port 8000)
- ✅ Wait for frontend to be ready (port 3000)
- ✅ Test backend endpoints:
  - `/health` - Health check
  - `/` - Root endpoint
  - `/api/hello` - API endpoint
- ✅ Test frontend accessibility
- ✅ Collect logs on failure

**Key Features:**
- Full stack integration testing
- Health check validation with timeouts
- Comprehensive API endpoint testing
- Automatic log collection on failure
- Resource cleanup

### 4. Security & Quality Checks
**Duration:** ~5-10 minutes

**Runs in Parallel:** Doesn't block other tests

**Steps:**
- ✅ Trivy filesystem vulnerability scanner
- ✅ Python Safety dependency checker
- ✅ npm audit for Node.js packages
- ✅ Upload results to GitHub Security

**Key Features:**
- Identifies CRITICAL and HIGH severity vulnerabilities
- Integrates with GitHub Security tab
- Non-blocking (continue-on-error for warnings)

### 5. Deployment Readiness
**Duration:** ~2-3 minutes

**Dependencies:** Requires all previous jobs to pass

**Steps:**
- ✅ Download build artifacts
- ✅ Verify essential files exist
- ✅ Generate deployment summary
- ✅ Create status badge

**Key Features:**
- Validates production build artifacts
- Comprehensive deployment summary
- GitHub Actions summary dashboard

### 6. Notifications
**Duration:** ~1 minute

**Triggers:**
- Success notification on `main` branch
- Failure notification on any branch

## 🎯 Test Coverage

### Backend Coverage
- **Framework:** pytest with pytest-cov
- **Reports:** XML (Codecov), HTML (artifacts), Terminal
- **Location:** `backend/htmlcov/index.html`

### Frontend Coverage
- **Framework:** Vitest with @vitest/coverage-v8
- **Reports:** lcov (Codecov), HTML (artifacts)
- **Location:** `frontend/coverage/index.html`

## 🐳 Docker Compose Configuration

### Development Mode (Default)
```bash
docker-compose up
```

**Features:**
- **Backend:** Hot reload with `--reload` flag
- **Frontend:** Vite HMR (Hot Module Replacement)
- **Volumes:** Source code mounted for live updates
- **Ports:** Backend (8000), Frontend (3000)

### Production Mode
```bash
docker-compose --profile prod up
```

**Features:**
- Optimized production builds
- Nginx serving static frontend
- No source code volumes
- Port 3001 for production frontend

## 📊 Artifacts

### Backend Test Results
- Path: `backend/htmlcov/`
- Retention: 7 days
- Files: Coverage HTML reports, XML, JUnit reports

### Frontend Build
- Path: `frontend/dist/`
- Retention: 7 days
- Files: Production-ready static assets

## ⚡ Performance Optimizations

### Caching Strategy
1. **pip cache:** Python dependencies (~200MB)
2. **npm cache:** Node.js dependencies (~500MB)
3. **Docker layer cache:** Build optimization

### Parallel Execution
- Frontend and Backend tests run simultaneously
- Security checks run in parallel
- Reduces total CI time by ~50%

### Timeouts
- Backend tests: 15 minutes
- Frontend tests: 15 minutes
- Integration tests: 20 minutes
- Security checks: 10 minutes

## 🔍 Debugging Failed Builds

### Backend Test Failures
```bash
# Local testing
cd backend
pytest -v --tb=short
```

### Frontend Test Failures
```bash
# Local testing
cd frontend
npm run test
```

### Integration Test Failures
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Test services locally
docker-compose up
curl http://localhost:8000/health
curl http://localhost:3000
```

## 🎨 Status Badges

Add to your README:

```markdown
![CI Pipeline](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/workflows/CI%20Pipeline%20-%20Green%20Theme%20Hello%20World%20Fullstack/badge.svg)
```

## 🚀 Deployment Pipeline

### Success Criteria
All jobs must pass:
- ✅ Backend tests pass (100% of tests)
- ✅ Frontend tests pass (100% of tests)
- ✅ Integration tests pass
- ✅ Security scans complete
- ✅ Build artifacts verified

### Next Steps After CI Success
1. Merge PR to main branch
2. Automatic deployment triggers (if configured)
3. Production deployment

## 📝 Environment Variables

### CI Environment
```yaml
PYTHON_VERSION: '3.11'
NODE_VERSION: '18'
BACKEND_PORT: 8000
FRONTEND_PORT: 3000
```

### Local Development
See `backend/.env.example` for backend configuration

## 🛠️ Maintenance

### Updating Dependencies

**Backend:**
```bash
cd backend
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

**Frontend:**
```bash
cd frontend
npm update
npm audit fix
```

### Updating GitHub Actions
- Actions are pinned to major versions (v4, v5)
- Check for updates quarterly
- Test in feature branch before updating

## 📞 Support

For issues with the CI pipeline:
1. Check GitHub Actions logs
2. Review this documentation
3. Test locally with Docker Compose
4. Contact DevOps team

---

**Last Updated:** 2024
**Pipeline Version:** 1.0
**Status:** ✅ Production Ready
