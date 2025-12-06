# Task Manager Application

> A production-ready task management application with comprehensive linting, testing, and security configurations.

A full-stack task management application with a React frontend and Python FastAPI backend, orchestrated with Docker Compose for local development. Create, view, update, and delete tasks with persistent MySQL storage.

## 🎯 Overview

This project is a complete CRUD application for managing tasks with:
- **Frontend**: React 18 + Vite with responsive UI and custom hooks
- **Backend**: Python FastAPI with clean architecture (repository pattern, dependency injection)
- **Database**: MySQL 8.0 for persistent data storage with connection pooling
- **Testing**: Comprehensive test suite with property-based testing (Hypothesis & fast-check)
- **Code Quality**: Pre-commit hooks with Black, isort, flake8, Bandit, Prettier, ESLint
- **CI/CD**: GitHub Actions pipeline with sequential quality gates
- **Orchestration**: Docker Compose for local development
- **Hot Reload**: Live updates during development for both frontend and backend

## 📁 Project Structure

```
project-root/
├── .github/
│   └── workflows/
│       └── ci.yml                # CI/CD pipeline with sequential stages
├── backend/                       # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # Application factory with FastAPI app
│   │   ├── config.py             # Centralized configuration with Pydantic
│   │   ├── dependencies.py       # Dependency injection providers
│   │   ├── models/
│   │   │   └── task.py           # Pydantic models (Task, TaskCreate, TaskUpdate)
│   │   ├── repositories/
│   │   │   └── task_repository.py # MySQL data access layer
│   │   ├── routes/
│   │   │   ├── health.py         # Health check endpoint
│   │   │   └── tasks.py          # Task CRUD endpoints
│   │   └── services/
│   │       └── task_service.py   # Business logic layer
│   ├── tests/
│   │   ├── test_main.py          # API endpoint tests with Hypothesis
│   │   └── test_task_repository.py # Repository tests with Hypothesis
│   ├── data/
│   │   └── .gitkeep              # Placeholder for data directory
│   ├── Dockerfile                # Backend container image
│   ├── pyproject.toml            # Python project configuration
│   ├── requirements.txt          # Production dependencies
│   ├── requirements-dev.txt      # Development dependencies
│   ├── .env.example              # Environment variable template
│   ├── .flake8                   # Flake8 linting configuration
│   └── pytest.ini                # Pytest configuration (optional)
├── frontend/                      # React + Vite frontend
│   ├── src/
│   │   ├── __tests__/
│   │   │   └── App.test.jsx      # React component tests with fast-check
│   │   ├── assets/
│   │   │   └── logo.png          # Application logo
│   │   ├── components/
│   │   │   ├── TaskForm.jsx      # Task creation/edit form component
│   │   │   ├── TaskItem.jsx      # Individual task display component
│   │   │   └── TaskList.jsx      # Task list container component
│   │   ├── hooks/
│   │   │   ├── useTasks.js       # Custom hook for task management
│   │   │   └── useTasks.test.js  # Hook tests
│   │   ├── services/
│   │   │   ├── api.js            # API client with fetch wrapper
│   │   │   └── api.test.js       # API service tests
│   │   ├── test/
│   │   │   └── setup.js          # Test environment setup
│   │   ├── utils/
│   │   │   └── constants.js      # Shared constants
│   │   ├── App.jsx               # Main application component
│   │   ├── App.css               # Application styles
│   │   └── main.jsx              # React entry point
│   ├── index.html                # HTML template
│   ├── package.json              # Frontend dependencies (includes fast-check)
│   ├── vite.config.js            # Vite configuration with test setup
│   ├── .env.example              # Environment variable template
│   ├── .eslintrc.json            # ESLint configuration
│   ├── TEST_GUIDE.md             # Comprehensive testing documentation
│   └── Dockerfile                # Frontend container image
├── .gitignore                    # Git ignore rules
├── .pre-commit-config.yaml       # Pre-commit hooks configuration
├── docker-compose.yml            # Multi-service orchestration
├── LICENSE                       # License file
└── README.md                     # This file
```

## 🏗️ Architecture

### Backend Architecture

The backend follows a clean, layered architecture with clear separation of concerns:

```
Request → Routes → Services → Repositories → Database
          ↓         ↓           ↓
       FastAPI   Business    Data Access
                  Logic       Layer
```

**Layers:**

1. **Routes Layer** (`app/routes/`):
   - HTTP endpoints and request/response handling
   - Request validation via Pydantic models
   - HTTP status code management
   - Error handling and exception mapping

2. **Services Layer** (`app/services/`):
   - Business logic and orchestration
   - Coordinates between routes and repositories
   - Transaction boundaries (if needed)
   - Domain rules enforcement

3. **Repository Layer** (`app/repositories/`):
   - Database access abstraction
   - CRUD operations
   - Query construction
   - Connection management with context managers

4. **Models Layer** (`app/models/`):
   - Pydantic models for validation
   - Data transfer objects (DTOs)
   - Request/response schemas

5. **Configuration** (`app/config.py`):
   - Centralized settings management
   - Environment variable loading
   - Type-safe configuration with Pydantic

6. **Dependency Injection** (`app/dependencies.py`):
   - FastAPI Depends() providers
   - Service and repository instantiation
   - Enables easy testing and mocking

**Benefits:**
- ✅ Easy to test each layer independently
- ✅ Clear separation of concerns
- ✅ Easier to swap implementations (e.g., switch from MySQL to PostgreSQL)
- ✅ Follows SOLID principles
- ✅ Scalable architecture for growing applications

### Frontend Architecture

The frontend uses a component-based architecture with custom hooks:

```
App.jsx
  ├── useTasks hook (state management)
  │   └── api.js (HTTP client)
  ├── TaskForm component (create/edit)
  ├── TaskList component (list container)
  │   └── TaskItem component (individual task)
  └── CSS styles
```

**Key Patterns:**
- **Custom Hooks**: `useTasks` encapsulates all task-related state and API calls
- **Component Composition**: Small, focused components with single responsibilities
- **Props Down, Events Up**: Data flows down via props, events bubble up
- **Separation of Concerns**: API logic separated from UI components

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git installed
- Node.js 18+ (for local development without Docker)
- Python 3.11+ (for local development without Docker)

### Run with Docker Compose (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output.git
   cd ab-sdlc-agent-ai-output
   ```

2. **Start the application**:
   ```bash
   docker compose up
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Health: http://localhost:8000/health
   - API Docs: http://localhost:8000/docs (Interactive Swagger UI)
   - MySQL: localhost:3306 (user: taskuser, password: taskpassword, database: taskmanager)

4. **Stop the application**:
   ```bash
   docker compose down
   ```

### Run Locally (Without Docker)

#### Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configure environment (copy and edit .env)
cp .env.example .env

# Ensure MySQL is running and configured
# Update DB_HOST, DB_PORT, etc. in .env if needed

# Run the application
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment (copy and edit .env)
cp .env.example .env

# Run the application
npm run dev
```

#### Run Tests
```bash
# Backend tests
cd backend
pytest -v --cov=app --cov-report=term-missing

# Frontend tests
cd frontend
npm test
```

## 🎨 Features

### Task Management Features
- ✅ **Create Tasks**: Add new tasks with title and description
- ✅ **View Tasks**: Display all tasks ordered by creation date (newest first)
- ✅ **Edit Tasks**: Update task title and description
- ✅ **Delete Tasks**: Remove tasks from the list
- ✅ **Toggle Completion**: Mark tasks as complete or incomplete
- ✅ **Data Persistence**: Tasks persist in MySQL database across restarts
- ✅ **Input Validation**: Client and server-side validation for data integrity
- ✅ **Error Handling**: User-friendly error messages for all operations

### Frontend Features
- ✅ Responsive task management UI
- ✅ Task creation form with validation
- ✅ Inline task editing
- ✅ Visual distinction for completed tasks (strikethrough)
- ✅ Loading state indicators for all operations
- ✅ Error handling with user-friendly messages
- ✅ Empty state messaging
- ✅ Hot Module Replacement (HMR) for development
- ✅ Environment-based API URL configuration
- ✅ Comprehensive test coverage with property-based testing
- ✅ Custom hooks for state management (`useTasks`)
- ✅ Reusable component architecture

### Backend Features
- ✅ RESTful API with FastAPI
- ✅ Full CRUD operations for tasks
- ✅ Pydantic models for request/response validation
- ✅ MySQL database persistence with connection pooling
- ✅ Repository pattern for data access abstraction
- ✅ Dependency injection for testability
- ✅ Centralized configuration management
- ✅ Proper HTTP status codes (200, 201, 204, 404, 422)
- ✅ CORS enabled for frontend communication
- ✅ Auto-reload during development
- ✅ Comprehensive test coverage with property-based testing
- ✅ Clean architecture with layered design

### Code Quality Features
- ✅ **Pre-commit Hooks**: Automatic code formatting and linting before commits
  - Black (Python code formatting)
  - isort (Python import sorting)
  - flake8 (Python linting)
  - Bandit (Python security checks)
  - Prettier (JavaScript/CSS formatting)
  - ESLint (JavaScript linting)
- ✅ **CI/CD Pipeline**: Sequential quality gates in GitHub Actions
- ✅ **Property-Based Testing**: Hypothesis (Python) and fast-check (JavaScript)
- ✅ **Security Scanning**: Bandit for Python security vulnerabilities

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
      "description": "Update README with API docs and examples",
      "completed": false,
      "created_at": "2024-01-15T10:30:00.000000Z",
      "updated_at": "2024-01-15T10:30:00.000000Z"
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
  "description": "Update README with API docs and examples"
}
```

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Complete project documentation",
  "description": "Update README with API docs and examples",
  "completed": false,
  "created_at": "2024-01-15T10:30:00.000000Z",
  "updated_at": "2024-01-15T10:30:00.000000Z"
}
```

**Validation Errors (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Title cannot be empty",
      "type": "value_error"
    }
  ]
}
```

### GET /api/tasks/{task_id}
Retrieve a specific task by ID.

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Complete project documentation",
  "description": "Update README with API docs and examples",
  "completed": false,
  "created_at": "2024-01-15T10:30:00.000000Z",
  "updated_at": "2024-01-15T10:30:00.000000Z"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Task not found"
}
```

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

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "created_at": "2024-01-15T10:30:00.000000Z",
  "updated_at": "2024-01-15T11:45:00.000000Z"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Task not found"
}
```

### DELETE /api/tasks/{task_id}
Delete a task.

**Response (204 No Content):**
No response body.

**Response (404 Not Found):**
```json
{
  "detail": "Task not found"
}
```

### GET /health
Returns the health status of the backend.

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

### Interactive API Documentation
FastAPI provides automatic interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## ⚙️ Environment Configuration

### Backend Environment Variables

The backend uses environment variables for database configuration. When running with Docker Compose, these are set automatically in `docker-compose.yml`:

**Available Variables:**

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | MySQL host | `mysql` |
| `DB_PORT` | MySQL port | `3306` |
| `DB_USER` | MySQL user | `taskuser` |
| `DB_PASSWORD` | MySQL password | `taskpassword` |
| `DB_NAME` | MySQL database | `taskmanager` |
| `TEST_DB_NAME` | Test database name | `taskmanager_test` |
| `ENV` | Application environment | `development` |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `http://localhost:3000` |

For local development without Docker, create a `.env` file in the `backend/` directory:

```bash
cd backend
cp .env.example .env
```

**Example `.env` file:**
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=taskuser
DB_PASSWORD=taskpassword
DB_NAME=taskmanager
TEST_DB_NAME=taskmanager_test
ENV=development
CORS_ORIGINS=http://localhost:3000
```

### Frontend Environment Variables

The frontend uses Vite's environment variable system. Create a `.env` file in the `frontend/` directory:

```bash
cd frontend
cp .env.example .env
```

**Available Variables:**

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000` |

**Example `.env` file:**
```
VITE_API_URL=http://localhost:8000
```

**For Production:**
```
VITE_API_URL=https://api.yourdomain.com
```

> **Note:** Changes to `.env` require restarting the development server.

## 🧪 Testing

### Testing Philosophy

This project uses a dual testing approach combining traditional unit tests with property-based testing:

- **Unit Tests**: Verify specific examples, edge cases, and integration points
- **Property-Based Tests**: Verify universal properties that should hold across all inputs

Property-based testing uses:
- **Backend**: Hypothesis library (Python)
- **Frontend**: fast-check library (JavaScript)

Each property test runs 100+ iterations with randomly generated inputs to catch edge cases that manual testing might miss.

### Running Tests

**Backend Tests:**
```bash
cd backend

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_main.py
pytest tests/test_task_repository.py

# Run with coverage
pytest --cov=app --cov-report=html
pytest --cov=app --cov-report=term-missing
```

**Frontend Tests:**
```bash
cd frontend

# Run all tests once
npm test

# Run tests in watch mode (for development)
npm run test:watch

# Run tests with coverage report
npm run test:coverage
```

### Test Coverage

**Backend Test Suite:**

*Unit Tests:*
- ✅ All API endpoints (GET, POST, PUT, DELETE)
- ✅ Request validation (empty titles, length limits)
- ✅ HTTP status codes (200, 201, 204, 404, 422)
- ✅ Task repository CRUD operations
- ✅ MySQL connection and persistence
- ✅ Error handling for database errors
- ✅ Service layer business logic
- ✅ Dependency injection

*Property-Based Tests:*
- ✅ Task creation persistence - any valid task should be retrievable after creation
- ✅ Empty title rejection - any whitespace-only title should be rejected
- ✅ Task retrieval completeness - all stored tasks should be returned
- ✅ Completion toggle idempotence - toggling twice returns to original state
- ✅ Delete operation removes task - deleted tasks should not be retrievable
- ✅ Update preserves identity - updates should not change ID or creation time
- ✅ Invalid update rejection - empty title updates should be rejected
- ✅ RESTful status codes - operations return correct HTTP status codes
- ✅ Persistence across restarts - tasks survive backend restarts

**Frontend Test Suite:**

*Integration Tests:*
- ✅ Task creation flow (form → API → list update)
- ✅ Task editing flow (edit button → form → update → display)
- ✅ Task deletion flow (delete button → removal)
- ✅ Task completion toggle
- ✅ Error handling for failed API calls
- ✅ Loading states for all operations
- ✅ Empty state display
- ✅ Component rendering and props
- ✅ Custom hooks (useTasks)
- ✅ API service layer

*Property-Based Tests:*
- ✅ Task ordering consistency - tasks always ordered by creation date (newest first)

For detailed testing documentation:
- Backend: See inline test documentation in `backend/tests/`
- Frontend: See `frontend/TEST_GUIDE.md`

## 🛠️ Pre-commit Hooks

This project uses pre-commit hooks to automatically enforce code quality standards before commits.

### Setup Pre-commit Hooks

```bash
# Install pre-commit (if not already installed)
pip install pre-commit

# Install the git hooks
pre-commit install
```

### Configured Hooks

**Python (Backend):**
- **Black**: Automatic code formatting (PEP 8 compliant)
- **isort**: Import statement sorting and organization
- **flake8**: Linting for style and potential errors
- **Bandit**: Security vulnerability scanning

**JavaScript (Frontend):**
- **Prettier**: Automatic code formatting
- **ESLint**: Linting for React and JavaScript code

**General:**
- Trailing whitespace removal
- End-of-file fixer
- YAML/JSON validation
- Large file detection
- Merge conflict detection
- Private key detection

### Manual Hook Execution

```bash
# Run hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
pre-commit run eslint --all-files

# Update hook versions
pre-commit autoupdate
```

## 🔄 CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow that implements a sequential, fail-fast approach to quality assurance.

### Pipeline Triggers
- All pull requests to main/master branches
- Direct pushes to main/master branches

### Pipeline Stages

The CI pipeline executes in three distinct stages, each acting as a quality gate:

**Stage 1: Linting (Parallel Execution)**
- **Backend Linting**: Runs flake8 on Python code
- **Frontend Linting**: Runs ESLint on JavaScript/React code
- **Purpose**: Catch code style and syntax issues immediately
- **Duration**: ~1-2 minutes
- **Fail-Fast**: If linting fails, subsequent stages are skipped

**Stage 2: Testing (Parallel Execution, After Linting)**
- **Backend Tests**: Runs pytest with coverage reporting
  - Unit tests for API endpoints and repository operations
  - Property-based tests using Hypothesis (100+ iterations)
- **Frontend Tests**: Runs Vitest with React Testing Library
  - Integration tests for UI components
  - Property-based tests using fast-check (100+ iterations)
  - Production build verification
- **Purpose**: Verify functionality and correctness
- **Duration**: ~2-3 minutes
- **Fail-Fast**: If tests fail, Docker validation is skipped

**Stage 3: Docker Integration (Sequential Execution, After Tests)**
- **Docker Compose Validation**: 
  - Validates docker-compose.yml syntax
  - Starts all services (MySQL, backend, frontend)
  - Performs health checks on backend and frontend
  - Displays logs on failure
  - Cleans up containers and volumes
- **Purpose**: Verify complete system integration
- **Duration**: ~3-5 minutes
- **Fail-Fast**: Stops immediately on any failure

### Dependency Graph

```
┌─────────────────┐     ┌─────────────────┐
│ Backend Linting │     │Frontend Linting │  ← Stage 1: Linting (Parallel)
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  Backend Tests  │     │ Frontend Tests  │  ← Stage 2: Testing (Parallel)
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │Docker Compose Validate│           ← Stage 3: Integration
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │    CI Success Summary │           ← Final confirmation
         └───────────────────────┘
```

### Key Features
- ✅ Sequential execution with explicit job dependencies
- ✅ Fail-fast approach - stops at first failure
- ✅ Parallel execution within stages for efficiency
- ✅ Comprehensive testing including property-based tests (100+ iterations)
- ✅ Full system integration validation with Docker Compose
- ✅ Intelligent caching for faster subsequent runs (pip, npm)

### Typical Execution Times
- **Linting Stage**: 1-2 minutes (parallel)
- **Testing Stage**: 2-3 minutes (parallel, after linting)
- **Docker Stage**: 3-5 minutes (sequential, after tests)
- **Total Duration**: 6-10 minutes (with caching)
- **First Run**: 10-15 minutes (without cache)

## 🔧 Development

### Development Workflow

1. **Setup Development Environment**:
   ```bash
   # Install pre-commit hooks
   pre-commit install
   
   # Start services
   docker compose up
   ```

2. **Make Changes**:
   - Edit files in `frontend/src/` or `backend/app/`
   - Changes automatically reload (HMR enabled)

3. **Test Changes**:
   ```bash
   # Run backend tests
   cd backend && pytest -v
   
   # Run frontend tests
   cd frontend && npm test
   ```

4. **Commit Changes**:
   ```bash
   git add .
   git commit -m "Your message"
   # Pre-commit hooks run automatically
   ```

5. **Push Changes**:
   ```bash
   git push
   # CI/CD pipeline runs automatically
   ```

### Making Backend Changes

**File Locations:**
- Routes: `backend/app/routes/`
- Services: `backend/app/services/`
- Repositories: `backend/app/repositories/`
- Models: `backend/app/models/`
- Configuration: `backend/app/config.py`
- Dependencies: `backend/app/dependencies.py`

**Testing:**
```bash
cd backend
pytest -v
pytest --cov=app --cov-report=term-missing
```

**Access API Docs:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Making Frontend Changes

**File Locations:**
- Components: `frontend/src/components/`
- Hooks: `frontend/src/hooks/`
- Services: `frontend/src/services/`
- Main App: `frontend/src/App.jsx`
- Styles: `frontend/src/App.css`

**Testing:**
```bash
cd frontend
npm test
npm run test:watch  # Watch mode
```

**Access Frontend:**
- Development: http://localhost:3000

### Viewing Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f frontend
docker compose logs -f backend
docker compose logs -f mysql
```

### Rebuilding Images

```bash
# Rebuild all images
docker compose build

# Rebuild specific service
docker compose build frontend
docker compose build backend

# Rebuild without cache
docker compose build --no-cache
```

## 💾 Data Persistence

### MySQL Database

The application uses MySQL 8.0 for persistent data storage with the following architecture:

**Database Schema:**
- **Database**: `taskmanager`
- **Table**: `tasks`
- **Columns**:
  - `id` VARCHAR(36) PRIMARY KEY - UUID
  - `title` VARCHAR(200) NOT NULL - Task title
  - `description` TEXT - Task description
  - `completed` BOOLEAN DEFAULT FALSE - Completion status
  - `created_at` VARCHAR(30) NOT NULL - ISO timestamp
  - `updated_at` VARCHAR(30) NOT NULL - ISO timestamp

**Architecture Features:**
- **Connection Pooling**: Context manager for efficient connection handling
- **Auto-Initialization**: Database schema created automatically on startup
- **Transaction Safety**: All writes committed immediately
- **Error Handling**: Graceful handling of connection and query errors
- **Repository Pattern**: Data access abstraction for easy testing and swapping

**Benefits:**
- ✅ ACID compliance for data integrity
- ✅ Concurrent access support
- ✅ Standard SQL queries
- ✅ Scalable storage
- ✅ Production-ready database engine
- ✅ Easy backup and restore with MySQL tools
- ✅ Docker volume persistence across container restarts

**Docker Volume:**
MySQL data is stored in a Docker volume (`mysql-data`), ensuring:
- Data persists across container restarts
- Data survives `docker compose down`
- Can be backed up using Docker volume commands

**Database Connection:**
The backend connects to MySQL using:
- Host: `mysql` (Docker service name) or `localhost` (local dev)
- Port: 3306
- Credentials configured via environment variables

### Backup and Restore

**Backup Database:**
```bash
# Backup using mysqldump
docker compose exec mysql mysqldump -u taskuser -ptaskpassword taskmanager > backup-$(date +%Y%m%d).sql

# Or backup the entire volume
docker run --rm -v ab-sdlc-agent-ai-output_mysql-data:/data -v $(pwd):/backup ubuntu tar czf /backup/mysql-backup-$(date +%Y%m%d).tar.gz /data
```

**Restore Database:**
```bash
# Restore from SQL dump
docker compose exec -T mysql mysql -u taskuser -ptaskpassword taskmanager < backup-20240115.sql

# Or restore from volume backup
docker run --rm -v ab-sdlc-agent-ai-output_mysql-data:/data -v $(pwd):/backup ubuntu tar xzf /backup/mysql-backup-20240115.tar.gz -C /
docker compose restart mysql
```

**Reset Data:**
```bash
# Connect to MySQL and delete all tasks
docker compose exec mysql mysql -u taskuser -ptaskpassword taskmanager -e "DELETE FROM tasks;"

# Or drop and recreate the database
docker compose exec mysql mysql -u root -prootpassword -e "DROP DATABASE taskmanager; CREATE DATABASE taskmanager;"
docker compose restart backend
```

**Access MySQL CLI:**
```bash
# Connect to MySQL command line
docker compose exec mysql mysql -u taskuser -ptaskpassword taskmanager

# Then you can run SQL commands:
# SELECT * FROM tasks;
# DESCRIBE tasks;
# etc.
```

## 📦 Dependencies

### Backend
- **Production:**
  - FastAPI 0.104.1 - Web framework
  - Uvicorn[standard] 0.24.0 - ASGI server
  - Pydantic 2.5.0 - Data validation
  - mysql-connector-python
