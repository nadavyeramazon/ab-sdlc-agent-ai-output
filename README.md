# Task Manager Application

A production-ready full-stack task management application with comprehensive linting, security scanning, and best practices. Features a React frontend and Python FastAPI backend, orchestrated with Docker Compose for local development.

## 🎯 Overview

This project is a complete CRUD application for managing tasks with:
- **Frontend**: React 18 + Vite with responsive UI
- **Backend**: Python FastAPI with RESTful API
- **Data Persistence**: JSON file-based storage with in-memory caching
- **Testing**: Comprehensive test suite with property-based testing (Hypothesis & fast-check)
- **Linting**: ESLint, Prettier, Black, Flake8, isort for code quality
- **Security**: CodeQL, Bandit, Safety, npm audit, Trivy, TruffleHog
- **Automation**: GitHub Actions CI/CD with security scanning
- **Dependency Management**: Dependabot for automated updates
- **Orchestration**: Docker Compose V2 for local development
- **Hot Reload**: Live updates during development for both frontend and backend

## 📁 Project Structure

```
project-root/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                # CI/CD pipeline with linting & tests
│   │   └── security.yml          # Security scanning workflow
│   └── dependabot.yml            # Automated dependency updates
├── frontend/                      # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx               # Main task manager component
│   │   ├── App.test.jsx          # Comprehensive test suite
│   │   ├── App.css               # Task manager styling
│   │   ├── main.jsx              # React entry point
│   │   └── test/
│   │       └── setup.js          # Test configuration
│   ├── .eslintrc.json            # ESLint configuration
│   ├── .prettierrc.json          # Prettier configuration
│   ├── index.html                # HTML template
│   ├── package.json              # Frontend dependencies
│   ├── vite.config.js            # Vite configuration
│   ├── .env.example              # Environment variable template
│   ├── TEST_GUIDE.md             # Testing documentation
│   └── Dockerfile                # Frontend Docker image
├── backend/                       # Python FastAPI backend
│   ├── main.py                   # FastAPI application
│   ├── task_repository.py        # Data persistence layer
│   ├── requirements.txt          # Backend dependencies
│   ├── pyproject.toml            # Python tooling configuration
│   ├── .flake8                   # Flake8 linting configuration
│   ├── pytest.ini                # Pytest configuration
│   ├── README_TESTS.md           # Backend testing documentation
│   ├── data/
│   │   └── .gitkeep              # Preserve data directory
│   ├── tests/                    # Test suite
│   └── Dockerfile                # Backend Docker image
├── docker-compose.yml             # Docker Compose V2 orchestration
├── .gitignore                    # Enhanced git ignore rules
├── LICENSE                       # Project license
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites
- Docker 20.10+ with Docker Compose V2 installed
- Git installed
- Node.js 18+ (for local development without Docker)
- Python 3.11+ (for local development without Docker)

### Run with Docker Compose (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output.git
   cd ab-sdlc-agent-ai-output
   ```

2. **Start the application** (using Docker Compose V2 syntax):
   ```bash
   docker compose up
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Health: http://localhost:8000/health
   - API Docs: http://localhost:8000/docs (Interactive Swagger UI)

4. **Stop the application**:
   ```bash
   docker compose down
   ```

### Docker Compose Commands (V2 Syntax)

This project uses Docker Compose V2 syntax (with space, not hyphen):

```bash
# Start services
docker compose up

# Start in detached mode
docker compose up -d

# View logs
docker compose logs -f

# Check service status
docker compose ps

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# Rebuild images
docker compose build

# Validate configuration
docker compose config
```

### Run Locally (Without Docker)

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install    # Use 'npm install' NOT 'npm ci'
npm run dev
```

## 🔧 Development

### Code Quality Tools

#### Backend (Python)
```bash
cd backend

# Format code with Black
black .

# Sort imports with isort
isort .

# Lint code with Flake8
flake8 .

# Run all quality checks
black --check . && isort --check-only . && flake8 .

# Security scanning
bandit -r .
safety check
```

#### Frontend (JavaScript)
```bash
cd frontend

# Lint code with ESLint
npm run lint

# Fix linting issues
npm run lint:fix

# Format code with Prettier
npm run format

# Check formatting
npm run format:check
```

### Running Tests

**Backend Tests:**
```bash
cd backend

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_main.py
```

**Frontend Tests:**
```bash
cd frontend

# Run all tests
npm test

# Run in watch mode
npm run test:watch

# Run with coverage
npm run test:coverage
```

### Making Changes

**Frontend Changes:**
1. Edit files in `frontend/src/`
2. Changes auto-reflect with HMR
3. Run linting: `npm run lint`
4. Run tests: `npm test`
5. Verify in browser: http://localhost:3000

**Backend Changes:**
1. Edit files in `backend/`
2. FastAPI auto-reloads
3. Run linting: `black . && flake8 .`
4. Run tests: `pytest`
5. Check API docs: http://localhost:8000/docs

## 🤖 CI/CD Pipeline

### Overview

The project includes a comprehensive CI/CD pipeline that automatically runs on every pull request and push to main/master branches. The pipeline ensures code quality, security, and functionality before merging changes.

### Main CI Pipeline (`.github/workflows/ci.yml`)

**Triggers:**
- Pull request events (opened, synchronize, reopened)
- Pushes to main/master branches

**Pipeline Jobs:**

#### 1. Backend Tests (15 min timeout)
Validates Python backend code quality and functionality:

**Steps:**
- ✅ Python 3.11 environment setup
- ✅ Pip dependency caching for faster builds
- ✅ Install dependencies from `requirements.txt`
- ✅ Verify backend imports
- ✅ Code formatting checks (Black, isort)
- ✅ Linting checks (Flake8)
- ✅ Run test suite with pytest
- ✅ Generate coverage reports
- ✅ Upload coverage to Codecov

**Commands executed:**
```bash
black --check .
isort --check-only .
flake8 .
pytest tests/ -v --tb=short
pytest tests/ --cov=. --cov-report=term --cov-report=xml
```

#### 2. Frontend Tests (15 min timeout)
Validates React frontend code quality and functionality:

**Steps:**
- ✅ Node.js 18 environment setup
- ✅ npm dependency caching for faster builds
- ✅ Install dependencies with `npm install` (NOT `npm ci`)
- ✅ ESLint code linting
- ✅ Prettier format checking
- ✅ Run test suite with Vitest
- ✅ Generate coverage reports
- ✅ Production build verification

**Commands executed:**
```bash
npm install          # CRITICAL: Use 'npm install' NOT 'npm ci'
npm run lint
npm run format:check
npm test             # Run tests, NOT 'npm run dev'
npm run test:coverage
npm run build
```

#### 3. Docker Build Verification (20 min timeout)
Validates that Docker images can be built successfully:

**Steps:**
- ✅ Docker Buildx setup
- ✅ Build backend Docker image
- ✅ Build frontend Docker image
- ✅ Verify image creation
- ✅ Inspect image sizes
- ✅ List built images

**Images built:**
- `task-manager-backend:${{ github.sha }}`
- `task-manager-frontend:${{ github.sha }}`

#### 4. Docker Compose Validation (20 min timeout)
Validates multi-service orchestration and integration:

**Dependencies:** Requires successful completion of backend-tests, frontend-tests, and docker-build

**Steps:**
- ✅ Validate docker-compose.yml syntax using V2 syntax
- ✅ Start services with `docker compose up -d`
- ✅ Wait for services to initialize (15 seconds)
- ✅ Check service status with `docker compose ps`
- ✅ Verify backend container logs
- ✅ Verify frontend container logs
- ✅ Test backend health endpoint (retry logic with 10 attempts)
- ✅ Test frontend accessibility (retry logic with 10 attempts)
- ✅ Test backend API endpoints (/, /tasks)
- ✅ Show complete logs on failure
- ✅ Cleanup with `docker compose down -v`

**Health checks with retry logic:**
```bash
# Backend health check (10 retries, 3 second intervals)
curl -f http://localhost:8000/health

# Frontend accessibility check (10 retries, 3 second intervals)
curl -f http://localhost:3000

# API endpoint tests
curl -f http://localhost:8000/
curl -f http://localhost:8000/tasks
```

#### 5. CI Pipeline Success Summary
Provides overall pipeline status and success message when all jobs pass.

### CI/CD Best Practices Implemented

**Performance Optimizations:**
- ✅ Dependency caching (npm, pip) for faster builds
- ✅ Parallel job execution where possible
- ✅ Reasonable timeout limits (15-20 minutes)
- ✅ Conditional step execution

**Error Handling:**
- ✅ Retry logic for health checks
- ✅ Complete log output on failures
- ✅ Always-run cleanup steps
- ✅ Clear error messages and warnings

**Test Execution:**
- ✅ Run test commands (`pytest`, `npm test`) NOT server commands
- ✅ Coverage reporting and upload
- ✅ Multiple test types (unit, integration, property-based)
- ✅ Build verification before deployment

**Docker Integration:**
- ✅ Docker Compose V2 syntax (`docker compose` with space)
- ✅ Service health validation
- ✅ Multi-service integration testing
- ✅ Proper cleanup and volume removal

**Package Management:**
- ✅ Use `npm install` (NOT `npm ci`) to avoid lock file issues
- ✅ Use `pip install -r requirements.txt` (NOT poetry/pipenv)
- ✅ Lock files excluded from git (.gitignore)

### Required GitHub Secrets

None currently required. Future deployment workflows may need:
- `AWS_ACCESS_KEY_ID` - AWS credentials for deployment
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub password

### Viewing Pipeline Results

1. **GitHub Actions Tab**: View all workflow runs
2. **Pull Request Checks**: See status checks on PRs
3. **Commit Status**: See pipeline status on commits
4. **Coverage Reports**: View on Codecov (if configured)

### Security Pipeline (`.github/workflows/security.yml`)

Runs on PRs, pushes, and weekly schedule (Mondays 8:00 AM UTC):

1. **Python Security Analysis**
   - Bandit security scanning
   - Safety vulnerability checking
   - Uploads security reports

2. **JavaScript Security Analysis**
   - ESLint security plugin
   - npm audit for dependencies
   - Uploads audit reports

3. **CodeQL Analysis**
   - Semantic code analysis for Python and JavaScript
   - Security-extended query suite
   - Uploads results to GitHub Security tab

4. **Dependency Review** (PRs only)
   - Blocks PRs with vulnerable dependencies
   - License compliance checking (denies GPL-3.0, AGPL-3.0)
   - Fails on moderate+ severity issues

5. **Secret Scanning**
   - TruffleHog for exposed credentials
   - Scans entire git history
   - Only verified secrets reported

6. **Docker Security**
   - Trivy container scanning
   - CRITICAL and HIGH severity detection
   - SARIF results uploaded to GitHub

### Dependabot Configuration (`.github/dependabot.yml`)

Automated dependency updates:
- **Python packages**: Weekly updates (Monday 8:00 AM)
- **npm packages**: Weekly updates (Monday 8:00 AM)
- **GitHub Actions**: Weekly updates (Monday 8:00 AM)
- **Docker base images**: Weekly updates (Monday 8:00 AM)
- Grouped minor/patch updates
- Automatic security updates
- Proper labeling for easy review

## 🔒 Security

### Security Scanning Workflow

The project includes comprehensive security scanning via GitHub Actions (`.github/workflows/security.yml`):

**Python Security:**
- **Bandit**: Static security analysis for Python code
- **Safety**: Checks dependencies for known vulnerabilities

**JavaScript Security:**
- **ESLint Security Plugin**: Detects security issues in code
- **npm audit**: Scans dependencies for vulnerabilities

**Code Analysis:**
- **CodeQL**: GitHub's semantic code analysis engine
- **TruffleHog**: Secret scanning for exposed credentials

**Container Security:**
- **Trivy**: Vulnerability scanner for container images

**Dependency Management:**
- **Dependabot**: Automated dependency updates (`.github/dependabot.yml`)
- **Dependency Review**: Blocks PRs with vulnerable dependencies

### Security Features

✅ **Input Validation**: Pydantic models validate all API inputs  
✅ **CORS Configuration**: Restricted to localhost during development  
✅ **No SQL Injection**: JSON file-based storage (no SQL)  
✅ **Secrets Management**: `.env` files excluded from git  
✅ **Dependency Scanning**: Weekly automated scans via Dependabot  
✅ **Code Scanning**: Security-focused static analysis with CodeQL  
✅ **Container Scanning**: Image vulnerability detection with Trivy  
✅ **Secret Detection**: Prevents credential exposure with TruffleHog  

### Best Practices Implemented

**Code Quality:**
- ✅ Consistent code formatting (Black, Prettier)
- ✅ Import organization (isort)
- ✅ Linting rules enforced (Flake8, ESLint)
- ✅ Type hints in Python code
- ✅ Comprehensive error handling
- ✅ Maximum line length: 120 characters
- ✅ Complexity limits enforced

**Security:**
- ✅ Environment variables for configuration
- ✅ No hardcoded secrets or credentials
- ✅ Input validation on all endpoints
- ✅ Proper HTTP status codes
- ✅ Security headers (via FastAPI)
- ✅ Regular security audits via CI/CD

**Testing:**
- ✅ Unit tests for all components
- ✅ Property-based testing for edge cases
- ✅ Integration tests for API endpoints
- ✅ Test coverage tracking
- ✅ CI/CD integration

**Documentation:**
- ✅ Comprehensive inline documentation
- ✅ API documentation (Swagger/OpenAPI)
- ✅ README with clear instructions
- ✅ Testing guides
- ✅ Configuration examples

## 🎨 Features

### Task Management Features
- ✅ **Create Tasks**: Add new tasks with title and description
- ✅ **View Tasks**: Display all tasks ordered by creation date (newest first)
- ✅ **Edit Tasks**: Update task title and description
- ✅ **Delete Tasks**: Remove individual tasks from the list
- ✅ **Delete All Tasks**: Remove all tasks at once (bulk deletion)
- ✅ **Toggle Completion**: Mark tasks as complete or incomplete
- ✅ **Data Persistence**: Tasks persist across application restarts
- ✅ **Input Validation**: Client and server-side validation
- ✅ **Error Handling**: User-friendly error messages

### Frontend Features
- ✅ Responsive task management UI
- ✅ Task creation form with validation
- ✅ Inline task editing
- ✅ Visual distinction for completed tasks
- ✅ Loading state indicators
- ✅ Error handling with user messages
- ✅ Empty state messaging
- ✅ Hot Module Replacement (HMR)
- ✅ Environment-based configuration
- ✅ ESLint + Prettier integration
- ✅ Comprehensive test coverage

### Backend Features
- ✅ RESTful API with FastAPI
- ✅ Full CRUD operations
- ✅ Bulk delete operations
- ✅ Pydantic model validation
- ✅ JSON file-based persistence
- ✅ In-memory caching
- ✅ Automatic data directory creation
- ✅ Proper HTTP status codes
- ✅ CORS configuration
- ✅ Auto-reload in development
- ✅ Black + Flake8 + isort integration
- ✅ Comprehensive test coverage

## 📡 API Endpoints

### GET /api/tasks
Retrieve all tasks ordered by creation date (newest first).

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Complete project documentation",
      "description": "Update README with API docs",
      "completed": false,
      "created_at": "2024-01-15T10:30:00.000Z",
      "updated_at": "2024-01-15T10:30:00.000Z"
    }
  ]
}
```

### POST /api/tasks
Create a new task.

**Request Body:**
```json
{
  "title": "Complete project documentation",
  "description": "Update README with API docs"
}
```

**Response (201 Created):** Returns created task object

**Error Responses:**
- 422 Unprocessable Entity: Invalid input (empty title, too long, etc.)

### GET /api/tasks/{task_id}
Retrieve a single task by ID.

**Response (200 OK):** Returns task object

**Error Responses:**
- 404 Not Found: Task with given ID not found

### PUT /api/tasks/{task_id}
Update an existing task.

**Request Body (all fields optional):**
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

**Response (200 OK):** Returns updated task object

**Error Responses:**
- 404 Not Found: Task with given ID not found
- 422 Unprocessable Entity: Invalid input (empty title, too long, etc.)

### DELETE /api/tasks/{task_id}
Delete a specific task by ID.

**Response (204 No Content):** No response body

**Error Responses:**
- 404 Not Found: Task with given ID not found

### DELETE /api/tasks
Delete all tasks (bulk deletion).

**Description:** Remove all tasks from the system in a single operation.

**Request:** No request body required

**Response (204 No Content):** No response body

**Success Conditions:**
- Returns 204 status code with empty response body
- All tasks are removed from storage
- Operation persists across application restarts
- Safe to call on empty task list (idempotent)

**Example curl command:**
```bash
curl -X DELETE http://localhost:8000/api/tasks
```

**Use Cases:**
- Reset application to clean state
- Clear all tasks during testing
- Quick cleanup before starting fresh
- Bulk task management

**Notes:**
- This endpoint is distinct from `DELETE /api/tasks/{task_id}` (single task deletion)
- Operation is idempotent - can be called multiple times safely
- No undo functionality - deleted tasks cannot be recovered
- Works correctly even when task list is empty

### GET /health
Health check endpoint.

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

## 📦 Dependencies

### Frontend
**Production:**
- React 18.2.0 - UI library
- React-DOM 18.2.0 - React rendering

**Development:**
- Vite 4.3.0 - Build tool and dev server
- @vitejs/plugin-react 4.0.0 - React plugin
- Vitest 1.0.4 - Test framework
- @testing-library/react 14.1.2 - Testing utilities
- @testing-library/user-event 14.5.1 - User interaction
- @testing-library/jest-dom 6.1.5 - DOM matchers
- jsdom 23.0.1 - DOM implementation
- fast-check 4.3.0 - Property-based testing
- **ESLint 8.55.0** - Code linting
- **eslint-plugin-react 7.33.2** - React linting
- **eslint-plugin-react-hooks 4.6.0** - Hooks linting
- **eslint-plugin-security 2.1.0** - Security linting
- **Prettier 3.1.1** - Code formatting

### Backend
**Production:**
- FastAPI 0.104.1 - Web framework
- Uvicorn[standard] 0.24.0 - ASGI server
- Pydantic 2.5.0 - Data validation
- python-multipart 0.0.6 - File upload support

**Development & Testing:**
- pytest 7.4.3 - Test framework
- pytest-cov 4.1.0 - Coverage reporting
- httpx 0.25.2 - HTTP client for tests
- hypothesis 6.148.2 - Property-based testing
- **black 24.8.0** - Code formatting
- **flake8 7.0.0** - Code linting
- **isort 5.13.2** - Import sorting
- **ruff 0.1.9** - Fast linting
- **bandit 1.7.6** - Security linting
- **safety 3.2.7** - Dependency scanning

## ⚙️ Configuration Files

### Linting Configurations

**Backend:**
- `.flake8` - Flake8 linting rules (max line length 120, complexity limit 10)
- `pyproject.toml` - Black, isort, Bandit, pytest configurations
- `.gitignore` - Enhanced security-focused ignore rules

**Frontend:**
- `.eslintrc.json` - ESLint rules with React and security plugins
- `.prettierrc.json` - Prettier formatting rules (120 char line length)
- `.gitignore` - Comprehensive ignore patterns

### CI/CD Configurations

- `.github/workflows/ci.yml` - Main CI/CD pipeline
- `.github/workflows/security.yml` - Security scanning workflow
- `.github/dependabot.yml` - Automated dependency updates

## 🧪 Testing

### Testing Philosophy

This project uses comprehensive testing including:
- **Unit Tests**: Verify specific functionality
- **Integration Tests**: Test component interactions
- **Property-Based Tests**: Verify universal properties (100+ iterations)

### Backend Test Coverage

**Unit Tests:**
- ✅ All API endpoints (GET, POST, PUT, DELETE)
- ✅ Bulk delete operations (DELETE /api/tasks)
- ✅ Request validation and error handling
- ✅ HTTP status codes (200, 201, 204, 404, 422)
- ✅ Task repository CRUD operations
- ✅ File persistence and data loading

**Property-Based Tests:**
- ✅ Task creation and persistence
- ✅ Empty title rejection
- ✅ Task retrieval completeness
- ✅ Completion toggle idempotence
- ✅ Delete operation correctness
- ✅ Delete all operations
- ✅ Update identity preservation
- ✅ RESTful status codes

See [backend/README_TESTS.md](backend/README_TESTS.md) for details.

### Frontend Test Coverage

**Integration Tests:**
- ✅ Task creation flow
- ✅ Task editing flow
- ✅ Task deletion flow
- ✅ Task completion toggle
- ✅ Error handling
- ✅ Loading states
- ✅ Empty state display

**Property-Based Tests:**
- ✅ Task ordering consistency

See [frontend/TEST_GUIDE.md](frontend/TEST_GUIDE.md) for details.

## 💾 Data Persistence

### Storage Approach

- **File**: `backend/data/tasks.json`
- **Format**: JSON array of task objects
- **Architecture**: In-memory cache with write-through
- **Docker Volume**: Mounted for persistence across restarts

### Backup and Restore

**Backup:**
```bash
cp backend/data/tasks.json backup-tasks-$(date +%Y%m%d).json
```

**Restore:**
```bash
cp backup-tasks-20240115.json backend/data/tasks.json
docker compose restart backend
```

**Reset (Delete All Tasks):**
```bash
# Using API endpoint
curl -X DELETE http://localhost:8000/api/tasks

# OR manually delete file
rm backend/data/tasks.json
docker compose restart backend
```

## 🐛 Troubleshooting

### CI/CD Pipeline Issues

**Pipeline Failures:**
1. Check the specific job that failed in GitHub Actions tab
2. Review the job logs for detailed error messages
3. Run the same commands locally to reproduce
4. Fix the issues and push again

**Common CI Failures:**

**Linting Failures:**
```bash
# Backend
cd backend
black --check . && isort --check-only . && flake8 .

# Frontend
cd frontend
npm run lint && npm run format:check
```

**Test Failures:**
```bash
# Backend
cd backend
pytest tests/ -v

# Frontend
cd frontend
npm test
```

**Docker Build Failures:**
```bash
# Test Docker builds locally
docker build -t backend:test ./backend
docker build -t frontend:test ./frontend
```

**Docker Compose Failures:**
```bash
# Validate configuration
docker compose config

# Test locally
docker compose up -d
docker compose ps
docker compose logs
docker compose down -v
```

### Linting Errors

**Python:**
```bash
cd backend
black --check .  # Check formatting
black .          # Fix formatting
isort --check .  # Check imports
isort .          # Fix imports
flake8 .         # Check linting
```

**JavaScript:**
```bash
cd frontend
npm run lint           # Check linting
npm run lint:fix       # Fix linting
npm run format:check   # Check formatting
npm run format         # Fix formatting
```

### Security Scan Failures

1. Check GitHub Security tab for detailed findings
2. Review security reports in CI artifacts
3. Update vulnerable dependencies:
   - Backend: `cd backend && pip install --upgrade -r requirements.txt`
   - Frontend: `cd frontend && npm update`
4. Fix code issues identified by scanners
5. Re-run security workflow

### Common Issues

**Frontend not loading:**
- Ensure port 3000 is available: `lsof -i :3000`
- Check frontend logs: `docker compose logs frontend`
- Clear browser cache and reload

**Backend not responding:**
- Ensure port 8000 is available: `lsof -i :8000`
- Verify health endpoint: `curl http://localhost:8000/health`
- Check backend logs: `docker compose logs backend`

**Docker issues:**
- Validate configuration: `docker compose config`
- Rebuild images: `docker compose build --no-cache`
- Clean up: `docker compose down -v`

**Tests failing:**
- Check linting first
- Verify all dependencies installed
- Review test output carefully

## 📝 Contributing

### Development Workflow

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**:
   - Write code following project standards
   - Run linting: `black . && flake8 .` or `npm run lint`
   - Write tests for new functionality
   - Run tests: `pytest` or `npm test`

3. **Pre-Commit Checks**:
   ```bash
   # Backend
   cd backend
   black --check . && isort --check-only . && flake8 . && pytest
   
   # Frontend
   cd frontend
   npm run lint && npm run format:check && npm test
   ```

4. **Commit Changes**:
   ```bash
   git add .
   git commit -m "feat: description of changes"
   ```

5. **Push and Create PR**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Wait for CI/CD Pipeline**:
   - All CI jobs must pass (backend-tests, frontend-tests, docker-build, docker-compose-validation)
   - Security scans must pass
   - Address any failures before requesting review

### Pull Request Requirements

- ✅ All linting checks pass (Black, Flake8, isort, ESLint, Prettier)
- ✅ All tests pass (unit + property-based + integration)
- ✅ No security vulnerabilities introduced
- ✅ Code coverage maintained or improved
- ✅ Documentation updated if needed
- ✅ **CI/CD pipeline succeeds (all 4 jobs green)**
- ✅ Security scans pass
- ✅ Docker builds successful
- ✅ Docker Compose validation passes

### Code Style Guidelines

**Python:**
- Follow PEP 8 standards
- Use Black for formatting (120 char lines)
- Sort imports with isort
- Add type hints where appropriate
- Write docstrings for functions/classes
- Keep complexity under 10 (Flake8 check)

**JavaScript:**
- Follow ESLint recommendations
- Use Prettier for formatting (120 char lines)
- Use functional components with hooks
- Add prop-types or TypeScript types
- Write clear, descriptive variable names
- Handle errors gracefully

## 🔗 Resources

### Documentation
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

### Testing
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [pytest Documentation](https://docs.pytest.org/)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [fast-check Documentation](https://fast-check.dev/)

### Code Quality & Security
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [ESLint Documentation](https://eslint.org/)
- [Prettier Documentation](https://prettier.io/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [CodeQL Documentation](https://codeql.github.com/docs/)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)

### CI/CD
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)

---

**Last Updated**: December 2025  
**Maintained by**: nadavyeramazon  
**License**: Educational/Demonstration Project
