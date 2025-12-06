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
│   │   ├── test_task_repository.py # Repository tests with Hypothesis
│   │   └── test_delete_all_tasks.py # Delete all tasks tests
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
│   │   │   ├── logo.png          # Application logo
│   │   │   └── logo-swiftpay.png # SwiftPay branding logo
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
│   │   ├── App.css               # Application styles (emerald green theme)
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
- Easy to test each layer independently
-  Clear separation of concerns
-  Easier to swap implementations (e.g., switch from MySQL to PostgreSQL)
-  Follows SOLID principles
-  Scalable architecture for growing applications

### Frontend Architecture

The frontend uses a component-based architecture with custom hooks:

```
App.jsx
  ├── useTasks hook (state management)
  │   └── api.js (HTTP client)
  ├── TaskForm component (create/edit)
  ├── TaskList component (list container)
  │   └── TaskItem component (individual task)
  └── CSS styles (emerald green theme)
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
-  **Create Tasks**: Add new tasks with title and description
-  **View Tasks**: Display all tasks ordered by creation date (newest first)
-  **Edit Tasks**: Update task title and description
-  **Delete Tasks**: Remove individual tasks from the list
-  **Delete All Tasks**: Remove all tasks at once with confirmation dialog
-  **Toggle Completion**: Mark tasks as complete or incomplete
-  **Data Persistence**: Tasks persist in MySQL database across restarts
-  **Input Validation**: Client and server-side validation for data integrity
-  **Error Handling**: User-friendly error messages for all operations

### User Interface Features
-  **Modern Theme**: Clean emerald green color scheme (rebranded from purple)
-  **SwiftPay Branding**: Updated logo for professional appearance
-  **Responsive Design**: Works on desktop and mobile devices
-  **Visual Feedback**: Loading states and disabled buttons during operations
-  **Confirmation Dialogs**: Safety prompts for destructive actions (Delete All)
-  **Empty State Messages**: Helpful hints when no tasks exist
-  **Smooth Animations**: Hover effects and transitions for better UX

### Delete All Tasks Feature

The **Delete All Tasks** button provides a quick way to clear all tasks at once:

**Location**: Appears above the task list when tasks exist

**Behavior**:
- Only visible when there are tasks to delete
- Shows confirmation dialog before deletion
- Displays loading state ("Deleting...") during operation
- Button is disabled during deletion to prevent double-clicks
- Hides automatically after all tasks are deleted

**Safety Features**:
- Confirmation dialog with clear warning message
- Describes action as irreversible
- User must explicitly confirm to proceed
- Can cancel without making changes

**Usage Example**:
```javascript
// User clicks "Delete All Tasks" button
// → Confirmation dialog appears
// → User confirms or cancels
// → If confirmed, all tasks are deleted from database
// → UI updates to show empty state
```

### Frontend Features
-  Responsive task management UI with emerald green theme
-  Task creation form with validation
-  Inline task editing
-  Visual distinction for completed tasks (strikethrough)
-  Loading state indicators for all operations
-  Error handling with user-friendly messages
-  Empty state messaging
-  Hot Module Replacement (HMR) for development
-  Environment-based API URL configuration
-  Comprehensive test coverage with property-based testing
-  Custom hooks for state management (`useTasks`)
-  Reusable component architecture

### Backend Features
-  RESTful API with FastAPI
-  Full CRUD operations for tasks
-  Bulk delete operation for all tasks (DELETE /api/tasks)
-  Pydantic models for request/response validation
-  MySQL database persistence with connection pooling
-  Repository pattern for data access abstraction
-  Dependency injection for testability
-  Centralized configuration management
-  Proper HTTP status codes (200, 201, 204, 404, 422)
-  CORS enabled for frontend communication
-  Auto-reload during development
-  Comprehensive test coverage with property-based testing
-  Clean architecture with layered design

### Code Quality Features
-  **Pre-commit Hooks**: Automatic code formatting and linting before commits
  - Black (Python code formatting)
  - isort (Python import sorting)
  - flake8 (Python linting)
  - Bandit (Python security checks)
  - Prettier (JavaScript/CSS formatting)
  - ESLint (JavaScript linting)
-  **CI/CD Pipeline**: Sequential quality gates in GitHub Actions
-  **Property-Based Testing**: Hypothesis (Python) and fast-check (JavaScript)
-  **Security Scanning**: Bandit for Python security vulnerabilities

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

### DELETE /api/tasks
Delete all tasks at once (bulk delete operation).

**Response (204 No Content):**
No response body.

**Example Usage:**
```bash
# Delete all tasks via curl
curl -X DELETE http://localhost:8000/api/tasks

# Delete all tasks via JavaScript
await fetch('http://localhost:8000/api/tasks', { method: 'DELETE' });
```

**Use Cases:**
This endpoint is useful for:
- Clearing all completed tasks after a milestone
- Resetting the task list for a new project
- Bulk cleanup operations during development
- Testing and demo purposes
- Removing all tasks before archiving

**Frontend Integration:**
The Delete All Tasks button in the UI:
1. Displays only when tasks exist
2. Shows confirmation dialog before deletion
3. Calls this endpoint on confirmation
4. Updates UI to show empty state after successful deletion
5. Shows error message if operation fails

**Note:** This operation is idempotent - calling it multiple times will always result in an empty task list and return 204.

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
Delete a specific task by ID.

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
pytest tests/test_delete_all_tasks.py

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
-  All API endpoints (GET, POST, PUT, DELETE)
-  DELETE /api/tasks endpoint (delete all tasks)
-  Request validation (empty titles, length limits)
-  HTTP status codes (200, 201, 204, 404, 422)
-  Task repository CRUD operations
-  Repository delete_all method
-  MySQL connection and persistence
-  Error handling for database errors
-  Service layer business logic
-  Dependency injection

*Property-Based Tests:*
-  Task creation persistence - any valid task should be retrievable after creation
-  Empty title rejection - any whitespace-only title should be rejected
-  Task retrieval completeness - all stored tasks should be returned
-  Completion toggle idempotence - toggling twice returns to original state
-  Delete operation removes task - deleted tasks should not be retrievable
-  Delete all removes N tasks - deleting all tasks results in empty list
-  Delete all idempotence - calling delete_all multiple times succeeds
-  Update preserves identity - updates should not change ID or creation time
-  Invalid update rejection - empty title updates should be rejected
-  RESTful status codes - operations return correct HTTP status codes
-  Persistence across restarts - tasks survive backend restarts

**Frontend Test Suite:**

*Integration Tests:*
-  Task creation flow (form → API → list update)
-  Task editing flow (edit button → form → update → display)
-  Task deletion flow (delete button → removal)
-  Delete all tasks flow (button → confirmation → removal)
-  Task completion toggle
-  Error handling for failed API calls
-  Loading states for all operations
-  Empty state display
-  Component rendering and props
-  Custom hooks (useTasks)
-  API service layer

*Delete All Tasks Tests:*
-  Button visibility (only shown when tasks exist)
-  Confirmation dialog display
-  User cancellation handling
-  Successful bulk deletion
-  Loading state during operation
-  Button disabled state during operation
-  Error handling for failed deletion
-  Empty state after deletion

*Property-Based Tests:*
-  Task ordering consistency - tasks always ordered by creation date (newest first)

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
-  Sequential execution with explicit job dependencies
-  Fail-fast approach - stops at first failure
-  Parallel execution within stages for efficiency
-  Comprehensive testing including property-based tests (100+ iterations)
-  Full system integration validation with Docker Compose
-  Intelligent caching for faster subsequent runs (pip, npm)

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
-  ACID compliance for data integrity
-  Concurrent access support
-  Standard SQL queries
-  Scalable storage
-  Production-ready database engine
-  Easy backup and restore with MySQL tools
-  Docker volume persistence across container restarts

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
  - python-multipart 0.0.6 - Form data parsing
  - mysql-connector-python 8.2.0 - MySQL database driver
  
- **Development & Testing:**
  - pytest 7.4.3 - Test framework
  - pytest-cov 4.1.0 - Coverage reporting
  - httpx 0.25.2 - HTTP client for testing
  - hypothesis 6.148.2 - Property-based testing library

### Frontend
- **Production:**
  - React 18.2.0 - UI library
  - React-DOM 18.2.0 - React rendering
  
- **Development & Testing:**
  - Vite 4.3.0 - Build tool and dev server
  - @vitejs/plugin-react 4.0.0 - React plugin for Vite
  - Vitest 1.0.4 - Test framework
  - @testing-library/react 14.1.2 - React testing utilities
  - @testing-library/user-event 14.5.1 - User interaction testing
  - @testing-library/jest-dom 6.1.5 - DOM matchers
  - jsdom 23.0.1 - DOM implementation for testing
  - fast-check 4.3.0 - Property-based testing library
  - ESLint 8.55.0 - JavaScript linting
  - eslint-plugin-react 7.33.2 - React-specific linting rules
  - eslint-plugin-react-hooks 4.6.0 - React Hooks linting rules
  - eslint-plugin-vitest 0.3.10 - Vitest-specific linting rules

## 🐛 Troubleshooting

### Frontend not loading
- Ensure port 3000 is not in use: `lsof -i :3000` (macOS/Linux) or `netstat -ano | findstr :3000` (Windows)
- Check frontend logs: `docker compose logs frontend`
- Verify frontend container is running: `docker compose ps`
- Clear browser cache and reload
- Check VITE_API_URL environment variable is set correctly
- Verify Node modules are installed: `cd frontend && npm install`

### Backend not responding
- Ensure port 8000 is not in use: `lsof -i :8000` (macOS/Linux) or `netstat -ano | findstr :8000` (Windows)
- Check backend logs: `docker compose logs backend`
- Verify backend health: `curl http://localhost:8000/health`
- Check MySQL connection: `docker compose logs mysql`
- Verify environment variables are set correctly

### Tasks not persisting
- Verify MySQL is running: `docker compose ps mysql`
- Check MySQL logs for errors: `docker compose logs mysql`
- Verify database connection: `docker compose exec mysql mysql -u taskuser -ptaskpassword taskmanager -e "SELECT COUNT(*) FROM tasks;"`
- Check backend logs for database errors: `docker compose logs backend`
- Ensure MySQL is healthy before backend starts (check healthcheck in docker-compose.yml)
- Verify MySQL volume exists: `docker volume ls | grep mysql-data`

### CORS errors
- Verify backend CORS is configured for `http://localhost:3000`
- Check CORS_ORIGINS environment variable in backend
- Ensure frontend is accessing correct API URL via VITE_API_URL
- Check browser console for specific CORS error messages
- Restart both frontend and backend after environment changes

### API returns 404 for tasks
- Verify backend is running: `curl http://localhost:8000/health`
- Check API endpoint: `curl http://localhost:8000/api/tasks`
- Review backend logs: `docker compose logs backend`
- Check routes are registered: Visit http://localhost:8000/docs
- Verify MySQL connection and table exists
- Ensure correct API prefix (/api) is used in frontend

### Tests failing
**Backend:**
- Clear pytest cache: `rm -rf .pytest_cache __pycache__`
- Reinstall dependencies: `pip install -r requirements.txt -r requirements-dev.txt`
- Run with verbose output: `pytest -v`
- Check hypothesis examples: `ls -la .hypothesis/examples/`
- Ensure MySQL is running for integration tests

**Frontend:**
- Clear node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`
- Check test setup: Ensure `src/test/setup.js` exists
- Run with verbose output: `npm test -- --reporter=verbose`
- Clear Vitest cache: `rm -rf node_modules/.vitest`

### Property-based tests failing
- Property tests use random data and may find edge cases
- Review the failing example in test output
- Check if the failure reveals a bug or incorrect test assumption
- Hypothesis stores failing examples in `.hypothesis/examples/`
- fast-check shows counterexamples in test output
- Run tests multiple times to verify reproducibility

### Docker Compose issues
- Validate configuration: `docker compose config`
- Rebuild images: `docker compose build --no-cache`
- Remove volumes: `docker compose down -v` (⚠️ This deletes data!)
- Check disk space: `df -h` (Linux/macOS) or `wmic logicaldisk get` (Windows)
- Verify Docker daemon is running: `docker ps`
- Check for port conflicts: Ensure ports 3000, 8000, 3306 are available

### Pre-commit hooks failing
- Update hooks: `pre-commit autoupdate`
- Run manually: `pre-commit run --all-files`
- Check specific hook: `pre-commit run <hook-name> --all-files`
- Clear cache: `pre-commit clean`
- Reinstall hooks: `pre-commit uninstall && pre-commit install`

### MySQL connection errors
- Verify MySQL container is running: `docker compose ps mysql`
- Check MySQL is accepting connections: `docker compose exec mysql mysqladmin ping`
- Verify credentials match environment variables
- Check MySQL logs: `docker compose logs mysql`
- Ensure healthcheck passes before backend starts
- Wait 10-15 seconds after starting MySQL before running backend

## 📝 Design Decisions & Notes

### Architecture Decisions

**Clean Architecture with Layered Design:**
- Separates concerns into distinct layers (routes, services, repositories)
- Makes code easier to test, maintain, and scale
- Allows swapping implementations (e.g., different databases) without affecting business logic
- Follows SOLID principles and dependency inversion

**Repository Pattern:**
- Abstracts data access logic from business logic
- Makes it easy to swap MySQL for another database (PostgreSQL, MongoDB, etc.)
- Simplifies testing by allowing mock repositories
- Provides a clean interface for data operations

**Dependency Injection:**
- Uses FastAPI's Depends() for automatic dependency resolution
- Enables easy testing with mock services/repositories
- Promotes loose coupling between components
- Makes code more maintainable and testable

**MySQL Database:**
- Production-ready relational database with ACID guarantees
- Supports concurrent access and transactions
- Standard SQL for queries makes it familiar to developers
- Docker volume ensures data persistence
- Easy to backup and restore

**No Authentication:**
- MVP scope focuses on core CRUD functionality
- Authentication can be added later without major refactoring
- All tasks are currently shared (no user isolation)
- Simplifies development and testing

**Property-Based Testing:**
- Catches edge cases that manual testing misses
- Provides mathematical guarantees about correctness
- Each property runs 100+ iterations with random data
- Complements traditional unit tests
- Helps discover bugs early in development

**Component-Based Frontend:**
- Small, focused components with single responsibilities
- Custom hooks (`useTasks`) encapsulate state and API logic
- Props down, events up pattern for predictable data flow
- Makes components reusable and testable
- Separates concerns (UI, state, API)

**Emerald Green Theme:**
- Modern, professional appearance
- Rebranded from original purple/blue theme
- Consistent color palette across the application
- High contrast for accessibility
- Smooth hover effects and transitions for better UX

**SwiftPay Branding:**
- Updated logo for professional appearance
- Maintains brand consistency
- Easy to swap logos for different deployments
- Scalable SVG/PNG format

### Development Philosophy

**Code Quality First:**
- Pre-commit hooks enforce standards before code is committed
- CI/CD pipeline validates quality at multiple stages
- Property-based testing provides correctness guarantees
- Comprehensive test coverage for confidence in changes

**Developer Experience:**
- Hot reload for instant feedback during development
- Automatic API documentation with FastAPI
- Clear error messages and validation
- Comprehensive README and inline documentation

**Production Readiness:**
- MySQL for reliable data persistence
- Docker Compose for consistent environments
- Health checks for service monitoring
- Error handling throughout the application
- Security scanning with Bandit

### Limitations

- **No Authentication/Authorization**: All tasks are shared, no user isolation
- **No Real-time Updates**: Requires manual refresh or polling
- **No Collaboration**: No task sharing or multi-user features
- **Basic MySQL Configuration**: Not optimized for high load or replication
- **No Task Categories/Tags**: Simple flat task list structure
- **No Task Priorities**: All tasks treated equally
- **No Search/Filter**: Must scroll through all tasks
- **No Pagination**: All tasks loaded at once (could be issue with many tasks)
- **No Task Deadlines**: No due date tracking
- **Local Development Only**: Not configured for production deployment

### Future Enhancements

Potential improvements for future versions:

1. **Authentication & Authorization**:
   - User registration and login
   - JWT token-based authentication
   - Role-based access control
   - User-specific task lists

2. **Advanced Features**:
   - Task categories and tags
   - Priority levels
   - Due dates and reminders
   - Task search and filtering
   - Pagination for large task lists
   - Sorting options (priority, due date, etc.)

3. **Collaboration**:
   - Task sharing between users
   - Comments on tasks
   - Task assignment
   - Activity history

4. **Real-time Updates**:
   - WebSocket support
   - Live updates when others modify tasks
   - Notifications for changes

5. **Deployment**:
   - Production Docker configuration
   - Kubernetes manifests
   - CI/CD deployment pipeline
   - Environment-specific configurations
   - Database migrations

6. **Performance**:
   - Database indexing
   - Query optimization
   - Caching layer (Redis)
   - Connection pooling optimization

## 🤝 Contributing

### Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/ab-sdlc-agent-ai-output.git
   cd ab-sdlc-agent-ai-output
   ```

3. **Install pre-commit hooks**:
   ```bash
   pip install pre-commit
   pre-commit install
   ```

4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

5. **Make your changes**:
   - Follow existing code style and patterns
   - Add tests for new functionality
   - Update documentation as needed

6. **Run tests**:
   ```bash
   # Backend tests
   cd backend && pytest -v
   
   # Frontend tests
   cd frontend && npm test
   ```

7. **Run pre-commit hooks**:
   ```bash
   pre-commit run --all-files
   ```

8. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: Add your feature description"
   ```

9. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

10. **Create a Pull Request**

### Commit Message Guidelines

Follow conventional commits format:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

### Pull Request Requirements

-  All automated tests must pass (unit + property-based)
-  Property-based tests run 100+ iterations
-  No new linting errors
-  Code coverage maintained or improved
-  Documentation updated if needed
-  Pre-commit hooks pass
-  Descriptive PR title and description

### Code Style

**Python:**
- Follow PEP 8 style guide
- Use Black for formatting (line length: 100)
- Use type hints where appropriate
- Document functions and classes with docstrings

**JavaScript:**
- Use ESLint recommended rules
- Use Prettier for formatting
- Use meaningful variable and function names
- Add JSDoc comments for complex functions

## 📄 License

This is a demonstration project for educational purposes. See [LICENSE](LICENSE) file for details.

## 🔗 Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Backend framework
- [Pydantic Documentation](https://docs.pydantic.dev/) - Data validation
- [React Documentation](https://react.dev/) - Frontend framework
- [Vite Documentation](https://vitejs.dev/) - Build tool
- [Vitest Documentation](https://vitest.dev/) - Testing framework
- [React Testing Library](https://testing-library.com/react) - Component testing
- [Docker Compose Documentation](https://docs.docker.com/compose/) - Container orchestration
- [MySQL Documentation](https://dev.mysql.com/doc/) - Database

### Property-Based Testing
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/) - Python property-based testing
- [fast-check Documentation](https://fast-check.dev/) - JavaScript property-based testing
- [Property-Based Testing Guide](https://hypothesis.works/articles/what-is-property-based-testing/)

### Code Quality Tools
- [Black Documentation](https://black.readthedocs.io/) - Python code formatter
- [flake8 Documentation](https://flake8.pycqa.org/) - Python linting
- [ESLint Documentation](https://eslint.org/) - JavaScript linting
- [Prettier Documentation](https://prettier.io/) - Code formatter
- [pre-commit Documentation](https://pre-commit.com/) - Git hooks

### Testing Resources
- [pytest Documentation](https://docs.pytest.org/) - Python testing
- [Hypothesis Strategies](https://hypothesis.readthedocs.io/en/latest/data.html) - Data generation
- [Testing Library Queries](https://testing-library.com/docs/queries/about) - DOM queries
- [Vitest API](https://vitest.dev/api/) - Test API reference

---

**Built with ❤️ using Clean Architecture and Modern Development Practices**

**Tested with  Property-Based Testing (Hypothesis & fast-check)**
