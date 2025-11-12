# GitHub Actions CI/CD Workflows

This directory contains the GitHub Actions workflow configurations for the Green Theme Hello World Fullstack Application.

## 📋 Table of Contents

- [Available Workflows](#available-workflows)
- [CI Workflow Details](#ci-workflow-details)
- [Job Dependencies](#job-dependencies)
- [Caching Strategy](#caching-strategy)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

## 🚀 Available Workflows

### CI Workflow (`ci.yml`)

**Triggers:**
- Pull requests to `main`, `develop`, and `feature/**` branches
- Pushes to `main` and `develop` branches
- Manual workflow dispatch

**Purpose:** Comprehensive continuous integration testing for frontend, backend, and Docker builds with integration testing.

## 🔄 CI Workflow Details

The CI workflow consists of 5 parallel and sequential jobs:

### 1️⃣ Frontend CI (`frontend-ci`)

**Runs on:** Ubuntu Latest  
**Timeout:** 15 minutes  
**Working Directory:** `./frontend`

**Steps:**
1. **Checkout code** - Get latest code from repository
2. **Setup Node.js 18.x** - Install Node.js with npm cache
3. **Cache node_modules** - Cache dependencies for faster builds
4. **Install dependencies** - Run `npm ci` if cache miss
5. **Run linting** - Execute linter if configured (optional)
6. **Run tests with coverage** - Execute `npm run test:coverage` (Vitest)
7. **Check coverage threshold** - Verify coverage meets 80% threshold
8. **Upload coverage reports** - Save coverage artifacts (30 days retention)
9. **Build application** - Run `npm run build` for production
10. **Check build size** - Display build output size
11. **Upload build artifacts** - Save build files (7 days retention)

**Key Features:**
- ✅ 30+ React component tests using React Testing Library
- ✅ Vitest test runner with coverage reporting
- ✅ Dependency caching for faster subsequent runs
- ✅ Build artifact preservation
- ✅ Automatic coverage threshold checking

**Technologies:**
- React 18.2
- Vite 5.x
- Vitest with coverage
- React Testing Library

### 2️⃣ Backend CI (`backend-ci`)

**Runs on:** Ubuntu Latest  
**Timeout:** 15 minutes  
**Working Directory:** `./backend`

**Steps:**
1. **Checkout code** - Get latest code from repository
2. **Setup Python 3.11** - Install Python with pip cache
3. **Cache pip packages** - Cache dependencies for faster builds
4. **Install dependencies** - Install from requirements.txt
5. **Run flake8 linting** - Check code style and errors
6. **Run mypy type checking** - Verify type hints
7. **Run tests with coverage** - Execute pytest with multiple coverage formats
8. **Check coverage threshold** - Verify coverage meets 80% threshold
9. **Upload coverage reports** - Save coverage artifacts (30 days retention)
10. **Run code quality checks** - Check isort and black formatting

**Key Features:**
- ✅ Comprehensive FastAPI endpoint testing
- ✅ pytest with coverage reporting (XML, HTML, JSON)
- ✅ Code quality checks (flake8, mypy, isort, black)
- ✅ Dependency caching for faster subsequent runs
- ✅ Automatic coverage threshold checking

**Technologies:**
- Python 3.11
- FastAPI 0.104
- pytest with coverage
- Code quality tools (flake8, mypy, isort, black)

### 3️⃣ Docker Build Verification (`docker-build`)

**Runs on:** Ubuntu Latest  
**Timeout:** 20 minutes  
**Depends on:** `frontend-ci`, `backend-ci`

**Steps:**
1. **Checkout code** - Get latest code from repository
2. **Set up Docker Buildx** - Enable advanced Docker build features
3. **Cache Docker layers - Frontend** - Cache frontend image layers
4. **Cache Docker layers - Backend** - Cache backend image layers
5. **Build frontend Docker image** - Build with layer caching
6. **Build backend Docker image** - Build with layer caching
7. **Verify Docker Compose configuration** - Validate docker-compose.yml
8. **Verify required services** - Check for backend and frontend services
9. **Display built images** - Show image sizes
10. **Optimize Docker cache** - Clean up old cache layers

**Key Features:**
- ✅ Parallel Docker builds after CI passes
- ✅ Layer caching for faster builds
- ✅ Configuration validation
- ✅ Service verification
- ✅ Multi-stage build optimization

**Docker Configuration:**
- Frontend: Nginx-based production build
- Backend: Python FastAPI application
- Network: Bridge network (app-network)
- Health checks: Built-in for both services

### 4️⃣ Integration Tests (`integration-test`)

**Runs on:** Ubuntu Latest  
**Timeout:** 20 minutes  
**Depends on:** `docker-build`

**Steps:**
1. **Checkout code** - Get latest code from repository
2. **Start services with docker-compose** - Launch full stack
3. **Wait for backend health check** - Ensure backend is ready (120s timeout)
4. **Wait for frontend health check** - Ensure frontend is ready (90s timeout)
5. **Display service status** - Show running containers
6. **Test backend health endpoint** - Verify `/health` endpoint
7. **Test backend API endpoint** - Verify `/api/hello` endpoint
8. **Test frontend accessibility** - Verify HTTP 200 response
9. **Test inter-service communication** - Verify Docker network connectivity
10. **Integration test summary** - Display results
11. **Show service logs on failure** - Debug information if tests fail
12. **Cleanup** - Stop and remove containers

**Key Features:**
- ✅ Full stack integration testing
- ✅ Service health verification
- ✅ API endpoint testing
- ✅ Inter-service communication verification
- ✅ Docker network validation
- ✅ Automatic cleanup

**Tests Performed:**
- Backend health check (port 8000)
- Frontend accessibility (port 80)
- API endpoint functionality
- Container-to-container communication
- Network configuration

### 5️⃣ CI Summary (`ci-summary`)

**Runs on:** Ubuntu Latest  
**Depends on:** `frontend-ci`, `backend-ci`, `docker-build`, `integration-test`  
**Always runs:** Yes (even if previous jobs fail)

**Steps:**
1. **Generate comprehensive CI summary** - Create detailed status report

**Key Features:**
- ✅ Consolidated status report
- ✅ Detailed job results table
- ✅ Success/failure indicators
- ✅ Testing coverage summary
- ✅ Fails if any required job fails

## 📊 Job Dependencies

```
frontend-ci ────┐
                ├──> docker-build ──> integration-test ──> ci-summary
backend-ci ─────┘
```

**Execution Flow:**
1. `frontend-ci` and `backend-ci` run in **parallel** (fastest)
2. `docker-build` runs after both CI jobs succeed
3. `integration-test` runs after Docker build succeeds
4. `ci-summary` runs after all jobs complete (always)

## 💾 Caching Strategy

### Frontend Caching
- **npm cache**: Automatic via `setup-node` action
- **node_modules**: Manual cache with package-lock.json hash key
- **Restoration**: Falls back to latest cache if exact match not found

### Backend Caching
- **pip cache**: Automatic via `setup-python` action
- **~/.cache/pip**: Manual cache with requirements.txt hash key
- **Restoration**: Falls back to latest cache if exact match not found

### Docker Caching
- **Frontend layers**: Cached to `/tmp/.buildx-cache-frontend`
- **Backend layers**: Cached to `/tmp/.buildx-cache-backend`
- **Cache strategy**: `mode=max` for maximum layer caching
- **Optimization**: Old caches cleaned up after each build

**Cache Benefits:**
- ⚡ **Faster builds**: 50-80% faster on cache hits
- 💰 **Cost savings**: Reduced GitHub Actions minutes
- 🔄 **Efficiency**: Parallel job execution with cached dependencies

## 🔧 Environment Variables

Global environment variables used across all jobs:

| Variable | Value | Description |
|----------|-------|-------------|
| `NODE_VERSION` | `18.x` | Node.js version for frontend |
| `PYTHON_VERSION` | `3.11` | Python version for backend |
| `COVERAGE_THRESHOLD` | `80` | Minimum code coverage percentage |

### Job-Specific Environment Variables

**Frontend CI:**
- `CI=true` - Enables CI mode for testing
- `NODE_ENV=production` - Production build mode

**Backend CI:**
- No additional environment variables

**Integration Tests:**
- Inherits from docker-compose.yml:
  - `PORT=8000` (backend)
  - `NODE_ENV=production` (backend)
  - `VITE_API_URL=http://backend:8000` (frontend)

## 🐛 Troubleshooting

### Frontend Tests Failing

**Check:**
1. Verify all tests pass locally: `npm run test`
2. Check test coverage: `npm run test:coverage`
3. Review frontend CI job logs
4. Verify Node.js version matches (18.x)

**Common Issues:**
- Missing dependencies: Clear cache and re-run
- Test timeout: Increase test timeout in vitest.config.js
- Import errors: Check file paths and imports

### Backend Tests Failing

**Check:**
1. Verify all tests pass locally: `pytest`
2. Check test coverage: `pytest --cov=.`
3. Review backend CI job logs
4. Verify Python version matches (3.11)

**Common Issues:**
- Import errors: Check PYTHONPATH
- Async test issues: Verify pytest-asyncio configuration
- Coverage threshold: Review coverage reports

### Docker Build Failing

**Check:**
1. Verify Dockerfiles exist in frontend/ and backend/
2. Build images locally: `docker-compose build`
3. Review docker-build job logs
4. Check Dockerfile syntax

**Common Issues:**
- Layer cache corruption: Clear cache and rebuild
- Build context issues: Verify COPY paths
- Base image issues: Check internet connectivity

### Integration Tests Failing

**Check:**
1. Verify docker-compose works locally: `docker-compose up`
2. Check service health: `docker-compose ps`
3. Review integration-test job logs
4. Verify network configuration

**Common Issues:**
- Health check timeout: Services take too long to start
- Port conflicts: Check port availability
- Network issues: Verify Docker network configuration
- API endpoint changes: Update test assertions

### Cache Issues

**Solution:**
1. **Clear GitHub Actions cache**:
   - Go to repository Settings → Actions → Caches
   - Delete all caches or specific cache keys

2. **Force rebuild without cache**:
   - Trigger workflow dispatch manually
   - Or update cache keys in workflow file

### Viewing Detailed Logs

1. **Navigate to Actions tab** in GitHub repository
2. **Select the workflow run** you want to investigate
3. **Click on failed job** to see detailed logs
4. **Expand steps** to see command output
5. **Download artifacts** (coverage reports, build files) for local analysis

## 📈 Optimization Tips

### Reducing CI Time

1. **Use caching**: Already implemented for npm, pip, and Docker layers
2. **Parallel execution**: Frontend and backend CI run simultaneously
3. **Fail fast**: Jobs fail quickly on first error
4. **Conditional steps**: Lint only if script exists

### Improving Test Performance

1. **Frontend**: Use `--watchAll=false` in CI (already set)
2. **Backend**: Use pytest-xdist for parallel test execution
3. **Docker**: Multi-stage builds to reduce image size

### Monitoring Coverage

- Coverage reports uploaded to artifacts (30 days retention)
- Download from workflow run page
- View HTML reports locally for detailed analysis

## 🔐 Security Considerations

### Secrets Management

- **No secrets required** for current workflow
- If adding deployment: Use GitHub Secrets
- Never commit credentials to repository

### Dependency Security

- Regular dependency updates recommended
- Use dependabot for automated updates
- Review security advisories

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [React Testing Library](https://testing-library.com/react)
- [pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)

## 🎯 Success Criteria

A successful CI run requires:

- ✅ All frontend tests pass (30+ tests)
- ✅ Frontend build completes successfully
- ✅ All backend tests pass with coverage
- ✅ Backend linting and type checking pass
- ✅ Frontend Docker image builds
- ✅ Backend Docker image builds
- ✅ docker-compose.yml is valid
- ✅ Services start and pass health checks
- ✅ API endpoints respond correctly
- ✅ Inter-service communication works

## 📞 Support

For CI/CD issues:
1. Check this documentation first
2. Review workflow logs in Actions tab
3. Check for similar issues in repository discussions
4. Create an issue with detailed error logs

---

**Last Updated:** 2025-11-12  
**Workflow Version:** 2.0  
**Maintained by:** DevOps Team
