# 🚀 CI/CD Quick Start Guide

## Overview

This guide helps you quickly understand and work with the CI/CD pipeline for the Green Theme Hello World Fullstack Application.

---

## 📝 What Happens When You Push Code?

```
1. You push code or create a PR
        ↓
2. GitHub Actions triggers CI workflow
        ↓
3. Frontend & Backend tests run in parallel (3-5 min)
        ↓
4. Docker images build (2-4 min)
        ↓
5. Integration tests verify full stack (2-3 min)
        ↓
6. Summary report generated
        ↓
7. ✅ Green checkmark (or ❌ red X) appears on your PR
```

**Total Time:** 8-13 minutes (with cache)

---

## ✅ Quick Checks Before Pushing

### Frontend Checks
```bash
cd frontend

# Run tests
npm test

# Check coverage
npm run test:coverage

# Build application
npm run build
```

### Backend Checks
```bash
cd backend

# Run tests
pytest

# Check coverage
pytest --cov=. --cov-report=term

# Run linting
flake8 .
mypy .
```

### Docker Checks
```bash
# Build and start services
docker-compose up --build

# In another terminal, test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/hello
curl http://localhost:80
```

---

## 🔍 Viewing CI Results

### GitHub Web UI

1. Go to your PR or commit
2. Click on "Details" next to the CI check
3. View individual job logs
4. Download artifacts (coverage reports, builds)

### GitHub CLI

```bash
# List recent runs
gh run list --workflow=ci.yml --limit 5

# View specific run
gh run view <run-id>

# Watch run in real-time
gh run watch

# Download artifacts
gh run download <run-id>
```

---

## 🐛 Common Issues & Quick Fixes

### ❌ Frontend Tests Failed

**Quick Fix:**
```bash
cd frontend
npm test
# Fix failing tests locally
npm test -- --coverage
# Ensure coverage is above 80%
```

### ❌ Backend Tests Failed

**Quick Fix:**
```bash
cd backend
pytest -v
# Fix failing tests locally
pytest --cov=. --cov-report=html
# Open htmlcov/index.html to see what needs coverage
```

### ❌ Docker Build Failed

**Quick Fix:**
```bash
# Test locally first
docker-compose build

# If that works, issue might be cache-related
# Delete workflow caches in Settings → Actions → Caches
```

### ❌ Integration Tests Failed

**Quick Fix:**
```bash
# Start services locally
docker-compose up

# In another terminal, test manually
curl http://localhost:8000/health
curl http://localhost:8000/api/hello
curl -I http://localhost:80

# Check logs
docker-compose logs backend
docker-compose logs frontend
```

---

## 📊 Understanding CI Jobs

### Job 1: Frontend CI (3-5 min)
- ✅ Installs Node.js dependencies
- ✅ Runs 30+ React tests
- ✅ Checks test coverage (80%+)
- ✅ Builds production bundle

**When it fails:** Check test output in job logs

### Job 2: Backend CI (2-4 min)
- ✅ Installs Python dependencies
- ✅ Runs pytest suite
- ✅ Checks code quality (flake8, mypy)
- ✅ Checks test coverage (80%+)

**When it fails:** Check test output and linting errors

### Job 3: Docker Build (2-4 min)
- ✅ Builds frontend Docker image
- ✅ Builds backend Docker image
- ✅ Validates docker-compose.yml

**When it fails:** Check Dockerfile syntax and build context

### Job 4: Integration Tests (2-3 min)
- ✅ Starts full stack with docker-compose
- ✅ Waits for services to be healthy
- ✅ Tests API endpoints
- ✅ Verifies inter-service communication

**When it fails:** Check service logs in job output

### Job 5: CI Summary (<1 min)
- ✅ Aggregates all job results
- ✅ Creates status report
- ✅ Fails if any job failed

---

## 💡 Pro Tips

### Speed Up CI Runs

1. **Ensure lock files are committed:**
   - `frontend/package-lock.json`
   - `backend/requirements.txt`
   
   This enables dependency caching!

2. **Fix tests locally first:**
   - Faster feedback loop
   - Saves CI minutes

3. **Use draft PRs for WIP:**
   - CI still runs but marked as draft
   - Less pressure during development

### Debugging Failed Runs

1. **Check the summary first:**
   - Scroll down on the Actions page
   - Summary shows which tests failed

2. **Expand failed steps:**
   - Click on red X steps
   - Read error messages carefully

3. **Download artifacts:**
   - Coverage reports show untested code
   - Build artifacts help debug build issues

4. **Check environment variables:**
   - Ensure VITE_API_URL is set correctly
   - Verify PORT configurations

### Writing CI-Friendly Code

1. **Frontend:**
   - Write tests for all components
   - Use proper test IDs for elements
   - Mock API calls in tests
   - Keep coverage above 80%

2. **Backend:**
   - Write tests for all endpoints
   - Use fixtures for common test data
   - Test error cases
   - Keep coverage above 80%

3. **Docker:**
   - Test Dockerfiles locally
   - Use health checks
   - Set proper environment variables
   - Document service dependencies

---

## 🎯 Coverage Requirements

Both frontend and backend must maintain **80%+ code coverage**.

### Checking Coverage Locally

**Frontend:**
```bash
cd frontend
npm run test:coverage
# Opens coverage report in browser
```

**Backend:**
```bash
cd backend
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

### What If Coverage Drops?

1. Download coverage artifact from failed run
2. Open HTML report to see uncovered lines
3. Add tests for uncovered code
4. Re-run CI

---

## 📦 Artifacts Available

After each CI run, you can download:

### Frontend Coverage (30 days)
- HTML coverage report
- JSON coverage data
- Line-by-line coverage details

### Backend Coverage (30 days)
- HTML coverage report
- XML coverage data
- Per-file coverage breakdown

### Frontend Build (7 days)
- Production build files
- Static assets
- Ready for deployment

### How to Download

**Web UI:**
1. Go to Actions → Select run
2. Scroll to "Artifacts" section
3. Click artifact name to download

**CLI:**
```bash
gh run download <run-id>
```

---

## 🔄 Re-running Failed Jobs

### Web UI
1. Go to failed workflow run
2. Click "Re-run jobs" button
3. Choose "Re-run failed jobs" or "Re-run all jobs"

### CLI
```bash
# Re-run failed jobs only
gh run rerun <run-id> --failed

# Re-run all jobs
gh run rerun <run-id>
```

---

## 📞 Getting Help

### Self-Service
1. Check this guide first
2. Review detailed docs in `.github/workflows/README.md`
3. Check `CI_CD_IMPLEMENTATION.md` for technical details

### Escalation
1. Check workflow logs for errors
2. Try to reproduce locally
3. Check if issue is environment-specific
4. Create issue with:
   - Run ID
   - Error logs
   - Local test results

---

## ✨ Best Practices

### Before Pushing

✅ Run tests locally  
✅ Check coverage locally  
✅ Verify Docker builds locally  
✅ Test integration with docker-compose  
✅ Commit lock files  

### During Development

✅ Write tests as you code  
✅ Maintain coverage above 80%  
✅ Fix linting issues immediately  
✅ Test in Docker periodically  
✅ Monitor CI results  

### After CI Passes

✅ Review coverage reports  
✅ Check for warnings  
✅ Verify build artifacts  
✅ Request code review  
✅ Merge when approved  

---

## 🎓 Learning Resources

### CI/CD Concepts
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [CI/CD Best Practices](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions)

### Testing
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [pytest Documentation](https://docs.pytest.org/)

### Docker
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)

---

## 🎉 Success Checklist

Before considering your CI setup complete:

- [ ] All tests pass locally
- [ ] Coverage is above 80%
- [ ] Docker builds successfully
- [ ] Integration tests pass
- [ ] No linting errors
- [ ] Documentation updated
- [ ] Lock files committed
- [ ] CI passes on PR
- [ ] Code review approved
- [ ] Ready to merge! 🚀

---

**Last Updated:** 2025-11-12  
**Quick Help:** Check `.github/workflows/README.md` for detailed documentation  
**Technical Details:** See `CI_CD_IMPLEMENTATION.md`
