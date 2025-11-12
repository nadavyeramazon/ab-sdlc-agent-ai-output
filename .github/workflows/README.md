# GitHub Actions CI/CD Workflows

## 📋 Overview

This directory contains GitHub Actions workflows for the Green Theme Hello World Fullstack Application.

## 🚀 Workflows

### CI/CD Pipeline (`ci.yml`)

**Triggers:**
- Push to `main` branch
- Push to `feature/**` branches
- Pull requests targeting `main` branch

**Jobs:**

#### 1. Frontend CI (`frontend-ci`)
- **Runtime:** Ubuntu Latest with Node.js 18.x
- **Timeout:** 15 minutes
- **Steps:**
  - ✅ Checkout code
  - ✅ Setup Node.js with npm caching
  - ✅ Install dependencies (`npm ci`)
  - ✅ Run linting (if available)
  - ✅ Run tests with coverage (`npm run test:coverage`)
  - ✅ Check coverage threshold (80%)
  - ✅ Build application (`npm run build`)
  - ✅ Upload coverage and build artifacts

#### 2. Backend CI (`backend-ci`)
- **Runtime:** Ubuntu Latest with Python 3.11
- **Timeout:** 15 minutes
- **Steps:**
  - ✅ Checkout code
  - ✅ Setup Python with pip caching
  - ✅ Install dependencies
  - ✅ Run flake8 linting
  - ✅ Run mypy type checking
  - ✅ Run pytest with coverage
  - ✅ Check coverage threshold (80%)
  - ✅ Run code quality checks (isort, black)
  - ✅ Upload coverage artifacts

#### 3. Docker Build & Integration Test (`docker-build`)
- **Runtime:** Ubuntu Latest with Docker
- **Timeout:** 20 minutes
- **Dependencies:** Runs after `frontend-ci` and `backend-ci` complete
- **Steps:**
  - ✅ Checkout code
  - ✅ Setup Docker Buildx
  - ✅ Build frontend Docker image
  - ✅ Build backend Docker image
  - ✅ Start services with docker-compose
  - ✅ Wait for health checks
  - ✅ Test backend API endpoints
  - ✅ Test frontend accessibility
  - ✅ Test inter-service communication
  - ✅ Display service status
  - ✅ Cleanup containers

#### 4. CI Status Report (`ci-status`)
- **Runtime:** Ubuntu Latest
- **Dependencies:** Runs after all jobs complete
- **Steps:**
  - ✅ Generate comprehensive CI summary
  - ✅ Display job status table
  - ✅ Fail pipeline if any job failed

## 🎯 Success Criteria

✅ **Frontend:**
- All tests pass
- Code coverage ≥ 80%
- Build succeeds
- Artifacts uploaded

✅ **Backend:**
- All tests pass
- Code coverage ≥ 80%
- Linting passes (flake8)
- Type checking passes (mypy)
- Code quality checks pass
- Artifacts uploaded

✅ **Docker:**
- Frontend image builds successfully
- Backend image builds successfully
- Both services start and become healthy
- API endpoints respond correctly
- Frontend is accessible
- Inter-service communication works

## 🚀 Optimization Features

### Caching Strategy
- **npm packages:** Cached using `actions/setup-node@v4` with `cache: 'npm'`
- **pip packages:** Cached using `actions/setup-python@v5` with `cache: 'pip'`

### Parallel Execution
- Frontend and Backend CI jobs run in parallel
- Docker build waits for both CI jobs to complete
- Reduces total pipeline time

### Timeout Limits
- Frontend CI: 15 minutes
- Backend CI: 15 minutes
- Docker Build: 20 minutes
- Prevents hanging jobs from consuming resources

### Artifact Management
- **Coverage reports:** Retained for 30 days
- **Build artifacts:** Retained for 7 days
- Automatic cleanup after retention period

## 📊 Coverage Reports

Coverage reports are uploaded as artifacts and can be downloaded from the workflow run:

1. Navigate to Actions tab
2. Select the workflow run
3. Scroll to "Artifacts" section
4. Download:
   - `frontend-coverage` - Frontend test coverage
   - `backend-coverage` - Backend test coverage
   - `frontend-build` - Production build

## 🔍 Monitoring & Debugging

### View Workflow Status
```bash
gh workflow view "CI/CD Pipeline - Green Theme Hello World"
```

### View Recent Runs
```bash
gh run list --workflow=ci.yml
```

### View Specific Run Details
```bash
gh run view <run-id>
```

### Download Artifacts
```bash
gh run download <run-id>
```

### Re-run Failed Jobs
```bash
gh run rerun <run-id> --failed
```

## 🐛 Troubleshooting

### Frontend Tests Failing
1. Check test logs in the workflow output
2. Verify all dependencies are installed correctly
3. Ensure test scripts are properly configured in `package.json`
4. Check if environment variables are needed

### Backend Tests Failing
1. Check pytest output in the workflow logs
2. Verify Python version compatibility
3. Ensure all requirements are installed
4. Check for missing environment variables

### Docker Build Failing
1. Review Docker build logs
2. Check Dockerfile syntax
3. Verify base images are accessible
4. Ensure all required files are present in build context

### Health Checks Timeout
1. Check service logs in the workflow output
2. Verify health check endpoints are correct
3. Increase timeout values if services need more startup time
4. Check for port conflicts or networking issues

### Coverage Below Threshold
1. Review uncovered code in coverage reports
2. Add tests for missing coverage
3. Adjust threshold if needed (in workflow file)

## 🔧 Configuration

### Environment Variables
Defined at the workflow level:
```yaml
env:
  NODE_VERSION: '18.x'      # Node.js version for frontend
  PYTHON_VERSION: '3.11'    # Python version for backend
  COVERAGE_THRESHOLD: 80    # Minimum code coverage percentage
```

### Modifying Coverage Threshold
Edit the `COVERAGE_THRESHOLD` value in `.github/workflows/ci.yml`:
```yaml
env:
  COVERAGE_THRESHOLD: 85  # Change to desired percentage
```

### Adding New Test Commands
Add steps in the respective CI job:
```yaml
- name: 🧪 Run integration tests
  run: npm run test:integration
```

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Node.js Testing with Vitest](https://vitest.dev/)
- [Python Testing with pytest](https://docs.pytest.org/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [GitHub Actions Cache](https://github.com/actions/cache)

## 🎉 Badge

Add this badge to your README to show CI status:

```markdown
[![CI/CD Pipeline](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml)
```

## 🤝 Contributing

When modifying workflows:
1. Test changes in a feature branch
2. Verify all jobs complete successfully
3. Check artifact uploads work correctly
4. Update this README if adding new features
5. Document any new environment variables or secrets
