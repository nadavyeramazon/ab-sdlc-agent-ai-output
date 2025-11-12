# CI/CD Quick Reference Guide
## Green Theme Hello World Fullstack Application

> **Quick access guide for developers working with the CI/CD pipeline**

---

## 🚀 Quick Start

### Triggering CI Workflow

**Automatic Triggers:**
```bash
# Push to feature branch
git push origin feature/my-feature

# Create pull request
gh pr create --base main --head feature/my-feature

# Push to main/develop
git push origin main
```

**Manual Trigger:**
1. Go to: Actions → CI Pipeline → Run workflow
2. Select branch
3. Click "Run workflow"

---

## 🧪 Local Testing Cheat Sheet

### Backend Tests
```bash
cd backend
pip install -r requirements.txt
pytest -v                    # Run all tests
pytest -k test_name         # Run specific test
pytest --cov=.              # With coverage
pytest --tb=short           # Short traceback
```

### Frontend Tests
```bash
cd frontend
npm ci                      # Clean install
npm run lint               # Linting
npm run test               # Run tests
npm run test:ui            # With UI
npm run test:coverage      # With coverage
npm run build              # Production build
```

### Integration Tests
```bash
docker-compose up -d                          # Start services
curl http://localhost:8000/health            # Backend health
curl http://localhost:3000                   # Frontend
docker-compose logs -f backend               # View logs
docker-compose down -v                       # Stop & cleanup
```

### Security Checks
```bash
# Python dependencies
cd backend && pip install safety && safety check -r requirements.txt

# npm dependencies
cd frontend && npm audit

# Trivy scan (requires installation)
trivy fs .
```

---

## 📊 CI Pipeline Overview

### Job Flow
```
Push/PR Trigger
    ↓
┌───┴────┬──────────┬─────────────┐
│Backend │ Frontend │   Security  │ (Parallel)
│ Tests  │  Tests   │   Checks    │
└───┬────┴────┬─────┴─────┬───────┘
    └─────────┴───────────┘
              ↓
       Integration Tests
              ↓
     Deployment Readiness
              ↓
         ✅ Success / ❌ Failure
```

### Typical Timings
| Job | Duration |
|-----|----------|
| Backend Tests | 5-10 min |
| Frontend Tests | 5-10 min |
| Security Checks | 5-10 min |
| Integration Tests | 10-15 min |
| Deployment Readiness | 2-5 min |
| **Total** | **~20-25 min** |

---

## ✅ Interpreting CI Results

### All Green ✅
```
✅ Backend Tests
✅ Frontend Tests  
✅ Integration Tests
✅ Security Checks
✅ Deployment Readiness
```
**Action**: Ready to merge! 🎉

### Red X ❌
Check which job failed:

**Backend Tests Failed**
- Review pytest output in logs
- Run `pytest -v` locally
- Check for import errors

**Frontend Tests Failed**
- Review Vitest output in logs
- Run `npm run test` locally
- Check linting with `npm run lint`

**Integration Tests Failed**
- Check service startup logs
- Run `docker-compose up` locally
- Verify endpoints respond

**Security Checks Failed**
- Review Security tab findings
- Update vulnerable dependencies
- Run security tools locally

**Deployment Readiness Failed**
- Usually means a previous job failed
- Check all jobs passed first
- Verify build artifacts exist

---

## 🔧 Common Quick Fixes

### Fix 1: Linting Errors
```bash
cd frontend
npm run lint -- --fix
git add .
git commit -m "fix: lint errors"
git push
```

### Fix 2: Test Failures
```bash
# Backend
cd backend
pytest -v --tb=short
# Fix issues, then:
git add .
git commit -m "fix: backend tests"
git push

# Frontend
cd frontend
npm run test
# Fix issues, then:
git add .
git commit -m "fix: frontend tests"
git push
```

### Fix 3: Security Vulnerabilities
```bash
# Update Python deps
cd backend
pip install --upgrade <package>
pip freeze > requirements.txt

# Update npm deps
cd frontend
npm audit fix
npm update

# Commit updates
git add .
git commit -m "chore: update dependencies for security"
git push
```

### Fix 4: Docker Issues
```bash
# Clean Docker state
docker-compose down -v
docker system prune -f

# Rebuild and test
docker-compose build
docker-compose up
```

### Fix 5: Cache Issues
```bash
# Clear GitHub Actions cache
# Go to: Settings → Actions → Caches → Delete

# Or wait for cache to rebuild on next run
```

---

## 📦 Artifacts

### Download Artifacts
```bash
# Via GitHub CLI
gh run list --limit 1
gh run download <run-id>

# Via Web UI
# Go to: Actions → Select run → Artifacts section → Download
```

### Available Artifacts
- `backend-test-results/` - Coverage HTML, XML, JUnit
- `frontend-build/` - Production build (dist/)

---

## 🔍 Debugging Tips

### View Detailed Logs
1. Go to: Actions → Select workflow run
2. Click failed job
3. Expand error step
4. Click "View raw logs" for full output

### Re-run Failed Jobs
1. Go to failed workflow run
2. Click "Re-run failed jobs"
3. Or "Re-run all jobs" to start fresh

### Enable Debug Logging
Add to commit message:
```
git commit -m "debug: enable debug logging" --allow-empty
```
Then add repository secret:
- `ACTIONS_STEP_DEBUG`: `true`
- `ACTIONS_RUNNER_DEBUG`: `true`

---

## 📋 Status Checks

### View CI Status

**Badge in README:**
```markdown
![CI](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/workflows/CI%20Pipeline%20-%20Green%20Theme%20Hello%20World%20Fullstack/badge.svg?branch=main)
```

**Command Line:**
```bash
gh run list --limit 5
gh run view <run-id>
gh run watch
```

**Pull Request:**
- Status checks appear at bottom of PR
- Click "Details" to view job logs
- Must pass before merge

---

## ⚡ Performance Tips

### Speed Up Local Testing

**Backend:**
```bash
# Use virtual environment
python -m venv venv
source venv/bin/activate

# Run specific test file
pytest tests/test_main.py -v

# Skip slow tests
pytest -m "not slow"
```

**Frontend:**
```bash
# Install once, reuse
npm ci  # Only when package-lock changes

# Run specific test file
npm run test -- src/__tests__/App.test.jsx

# Run tests in watch mode
npm run test -- --watch
```

### Speed Up CI

**Best Practices:**
- Don't commit unnecessary files
- Keep dependencies minimal
- Use `.dockerignore` and `.gitignore`
- Fix tests early (fail-fast)
- Run linting before commit

---

## 🎯 Pre-Push Checklist

Before pushing code:

```bash
# 1. Run linting
cd frontend && npm run lint

# 2. Run backend tests
cd backend && pytest -v

# 3. Run frontend tests
cd frontend && npm run test

# 4. Build frontend
cd frontend && npm run build

# 5. Test integration (optional)
docker-compose up -d
# Test endpoints
docker-compose down -v

# 6. Push!
git push origin feature/my-feature
```

---

## 🔗 Useful Links

### Repository
- **Actions**: https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions
- **Security**: https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/security
- **Settings**: https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/settings

### Documentation
- Full CI/CD Docs: `CI_CD_SETUP_SUMMARY.md`
- Backend Tests: `backend/TESTING_GUIDE.md`
- Frontend Tests: `frontend/TESTING_GUIDE.md`
- CI README: `.github/README-CI.md`

### External Resources
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [pytest Docs](https://docs.pytest.org/)
- [Vitest Docs](https://vitest.dev/)
- [Docker Compose Docs](https://docs.docker.com/compose/)

---

## 📞 Getting Help

### Self-Service
1. Check this quick reference
2. Review full documentation
3. Search repository issues
4. Test locally

### Ask for Help
1. Create GitHub issue with:
   - Error message
   - Job logs
   - Steps to reproduce
2. Tag relevant team members
3. Include workflow run link

---

## 🎓 Tips for Success

### Development Workflow
```bash
# 1. Create feature branch
git checkout -b feature/JIRA-123/new-feature

# 2. Make changes and test locally
# ... code changes ...
pytest -v  # backend
npm run test  # frontend

# 3. Commit with good message
git add .
git commit -m "feat: add new feature"

# 4. Push and watch CI
git push origin feature/JIRA-123/new-feature

# 5. Monitor workflow
gh run watch

# 6. Create PR when green
gh pr create

# 7. Respond to review feedback
# ... make changes ...
git add .
git commit -m "fix: address review comments"
git push

# 8. Merge when approved and green
gh pr merge
```

### Best Practices
✅ Test locally before pushing  
✅ Fix linting issues immediately  
✅ Keep commits small and focused  
✅ Write descriptive commit messages  
✅ Monitor CI results  
✅ Fix failures quickly  
✅ Update dependencies regularly  
✅ Review security alerts  

---

**Last Updated**: 2024-11-12  
**Version**: 1.0  
**Quick Help**: See `CI_CD_SETUP_SUMMARY.md` for detailed documentation
