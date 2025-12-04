# Task Manager Application

> A production-ready task management application with comprehensive linting, testing, and security configurations.

A full-stack task management application with a React frontend and Python FastAPI backend, orchestrated with Docker Compose for local development. Create, view, update, and delete tasks with persistent storage.

## 🎯 Overview

This project is a complete CRUD application for managing tasks with:
- **Frontend**: React 18 + Vite with responsive green-themed UI
- **Backend**: Python FastAPI with RESTful API
- **Database**: MySQL 8.0 for persistent data storage
- **Testing**: Comprehensive test suite with property-based testing (Hypothesis & fast-check)
- **Orchestration**: Docker Compose for local development
- **Hot Reload**: Live updates during development for both frontend and backend

## 🎨 UI Theme and Branding

The application features a modern green color scheme with the SwiftPay branding:

**Color Palette:**
- **Primary Green**: `#38a169` (green-500) - Main UI elements, buttons, focus states
- **Secondary Green**: `#2f855a` (green-600) - Hover states, gradients
- **Light Green**: `#48bb78` (green-400) - Edit buttons, accents
- **Background Gradient**: Linear gradient from green-500 to green-600

**Logo:**
- **Brand**: SwiftPay
- **File**: `frontend/src/assets/logo-swiftpay.png`
- **Usage**: Displayed in the application header alongside the "Task Manager" title

The green theme provides a fresh, professional appearance while maintaining excellent readability and accessibility.

## 📁 Project Structure

```
project-root/
├── frontend/                      # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx               # Main task manager component
│   │   ├── App.test.jsx          # Comprehensive test suite with property tests
│   │   ├── App.css               # Task manager styling (green theme)
│   │   ├── main.jsx              # React entry point
│   │   ├── assets/
│   │   │   └── logo-swiftpay.png # SwiftPay logo
│   │   └── test/
│   │       └── setup.js          # Test configuration
│   ├── index.html                # HTML template
│   ├── package.json              # Frontend dependencies (includes fast-check)
│   ├── vite.config.js            # Vite configuration with test setup
│   ├── .env.example              # Environment variable template
│   ├── TEST_GUIDE.md             # Comprehensive testing documentation
│   └── Dockerfile                # Frontend Docker image
├── backend/                       # Python FastAPI backend
│   ├── main.py                   # FastAPI application with task endpoints
│   ├── task_repository.py        # Data persistence layer (MySQL)
│   ├── test_main.py              # API endpoint tests with property tests
│   ├── test_task_repository.py   # Repository tests with property tests
│   ├── requirements.txt          # Backend dependencies (includes mysql-connector-python)
│   ├── pytest.ini                # Pytest configuration
│   ├── README_TESTS.md           # Backend testing documentation
│   ├── .env.example              # Environment variable template
│   └── Dockerfile                # Backend Docker image
├── .github/
│   └── workflows/
│       └── ci.yml                # CI/CD pipeline
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git installed
- Node.js 18+ (for local development without Docker)

### Run with Docker Compose (Recommended)

1. **Clone the repository and checkout the feature branch**:
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output.git
   cd ab-sdlc-agent-ai-output
   git checkout feature/JIRA-777/fullstack-app
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
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

#### Run Tests
```bash
cd frontend
npm test
```

## 🎨 Features

### Task Management Features
- ✅ **Create Tasks**: Add new tasks with title and description
- ✅ **View Tasks**: Display all tasks ordered by creation date (newest first)
- ✅ **Edit Tasks**: Update task title and description
- ✅ **Delete Tasks**: Remove individual tasks from the list
- ✅ **Delete All Tasks**: Clear all tasks at once with confirmation prompt
- ✅ **Toggle Completion**: Mark tasks as complete or incomplete
- ✅ **Data Persistence**: Tasks persist across application restarts
- ✅ **Input Validation**: Client and server-side validation for data integrity
- ✅ **Error Handling**: User-friendly error messages for all operations

### Frontend Features
- ✅ Modern green-themed responsive UI with SwiftPay branding
- ✅ Task creation form with validation
- ✅ Inline task editing
- ✅ Visual distinction for completed tasks (strikethrough)
- ✅ Delete All button with task count display
- ✅ Confirmation dialog for bulk operations
- ✅ Loading state indicators for all operations
- ✅ Error handling with user-friendly messages
- ✅ Empty state messaging
- ✅ Hot Module Replacement (HMR) for development
- ✅ Environment-based API URL configuration
- ✅ Comprehensive test coverage with property-based testing

### Backend Features
- ✅ RESTful API with FastAPI
- ✅ Full CRUD operations for tasks
- ✅ Bulk delete operation for all tasks
- ✅ Pydantic models for request/response validation
- ✅ MySQL database with connection pooling
- ✅ Automatic database schema creation
- ✅ Proper HTTP status codes (200, 201, 204, 404, 422)
- ✅ CORS enabled for frontend communication
- ✅ Auto-reload during development
- ✅ Comprehensive test coverage with property-based testing

## 🎨 User Interface Components

### Delete All Tasks Button

The Delete All feature provides a convenient way to clear all tasks at once:

**Location**: Above the task list in the "Task List" section

**Appearance**:
- Red button with white text
- Displays current task count: "Delete All (N)"
- Disabled state when no tasks exist
- Loading state: "Deleting..." during operation

**Behavior**:
1. Click the "Delete All (N)" button
2. Confirmation dialog appears: "Are you sure you want to delete all N task(s)? This action cannot be undone."
3. If confirmed:
   - All tasks are deleted via API call
   - Task list updates to show empty state
   - Button becomes disabled
4. If canceled:
   - No action taken
   - Tasks remain unchanged

**Safety Features**:
- Confirmation dialog prevents accidental deletion
- Disabled when no tasks exist
- Loading indicator during operation
- Error handling with rollback on failure
- Shows clear task count before deletion

**Code Example**:
```jsx
// Button is rendered in TaskList component
<button
  className="btn-delete-all"
  onClick={handleDeleteAll}
  disabled={taskCount === 0 || deleteAllLoading}
>
  {deleteAllLoading ? 'Deleting...' : `Delete All (${taskCount})`}
</button>
```

**Styling**:
```css
.btn-delete-all {
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #e53e3e;
  color: white;
}

.btn-delete-all:hover:not(:disabled) {
  background-color: #c53030;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(229, 62, 62, 0.4);
}

.btn-delete-all:disabled {
  background-color: #cbd5e0;
  cursor: not-allowed;
  opacity: 0.7;
}
```

**Testing**:
The Delete All feature includes comprehensive tests:
- Unit tests for API method
- Integration tests for user flow
- Tests for confirmation dialog
- Tests for disabled state
- Tests for loading state
- Tests for error handling with rollback

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
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T10:30:00.000Z"
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
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T10:30:00.000Z"
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
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T11:45:00.000Z"
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

### DELETE /api/tasks
Delete all tasks at once.

**Request Body:** None

**Response (200 OK):**
```json
{
  "message": "All tasks deleted",
  "deletedCount": 5
}
```

**Frontend Integration:**
```javascript
// API Service Method
async deleteAllTasks() {
  const response = await fetch(`${API_URL}/api/tasks`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

// Hook Usage
const deleteAllTasks = async () => {
  setError(null);
  const originalTasks = [...tasks];
  setTasks([]); // Optimistic update

  try {
    const result = await taskApi.deleteAllTasks();
    return { success: true, deletedCount: result.deletedCount };
  } catch (err) {
    setTasks(originalTasks); // Rollback on error
    setError(err.message);
    return { success: false, deletedCount: 0 };
  }
};
```

**Example Usage:**
```bash
# Delete all tasks using curl
curl -X DELETE http://localhost:8000/api/tasks

# Expected response
{
  "message": "All tasks deleted",
  "deletedCount": 5
}
```

**Use Cases:**
- Clear all test data during development
- Reset the task list quickly
- Bulk cleanup operations
- Starting fresh with an empty task list

**Safety Features:**
- Frontend confirmation dialog prevents accidental deletion
- Returns count of deleted tasks for verification
- Optimistic UI updates with rollback on error
- Clear error messages on failure

**Note:** This operation cannot be undone. All tasks are permanently deleted from the database. Always confirm the operation in the confirmation dialog.

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

For local development without Docker, create a `.env` file in the `backend/` directory:

```bash
cd backend
cp .env.example .env
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
pytest test_main.py
pytest test_task_repository.py

# Run with coverage
pytest --cov=. --cov-report=html
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

### Backend Test Coverage

The backend test suite includes:

**Unit Tests:**
- ✅ All API endpoints (GET, POST, PUT, DELETE)
- ✅ DELETE all tasks endpoint with empty list and existing tasks
- ✅ Request validation (empty titles, length limits)
- ✅ HTTP status codes (200, 201, 204, 404, 422)
- ✅ Task repository CRUD operations
- ✅ Database persistence and data loading
- ✅ Error handling for connection failures and invalid data

**Property-Based Tests:**
- ✅ **Property 1**: Task creation persistence - any valid task should be retrievable after creation
- ✅ **Property 2**: Empty title rejection - any whitespace-only title should be rejected
- ✅ **Property 3**: Task retrieval completeness - all stored tasks should be returned
- ✅ **Property 4**: Completion toggle idempotence - toggling twice returns to original state
- ✅ **Property 5**: Delete operation removes task - deleted tasks should not be retrievable
- ✅ **Property 6**: Update preserves identity - updates should not change ID or creation time
- ✅ **Property 7**: Invalid update rejection - empty title updates should be rejected
- ✅ **Property 8**: RESTful status codes - operations return correct HTTP status codes
- ✅ **Property 9**: Persistence across restarts - tasks survive backend restarts

For detailed backend testing documentation, see [backend/README_TESTS.md](backend/README_TESTS.md).

### Frontend Test Coverage

The frontend test suite includes:

**Integration Tests:**
- ✅ Task creation flow (form → API → list update)
- ✅ Task editing flow (edit button → form → update → display)
- ✅ Task deletion flow (delete button → removal)
- ✅ Delete all tasks flow (button → confirmation → deletion)
- ✅ Task completion toggle
- ✅ Error handling for failed API calls
- ✅ Loading states for all operations
- ✅ Empty state display

**Delete All Tasks Tests:**
- ✅ Render delete all button with task count
- ✅ Disable button when no tasks exist
- ✅ Show confirmation dialog when clicked
- ✅ Delete all tasks when confirmed
- ✅ Preserve tasks when confirmation is canceled
- ✅ Handle API errors with rollback
- ✅ Show loading state during operation

**Property-Based Tests:**
- ✅ **Property 10**: Task ordering consistency - tasks always ordered by creation date (newest first)

For detailed frontend testing documentation, see [frontend/TEST_GUIDE.md](frontend/TEST_GUIDE.md).

### Manual Testing Checklist

**Task Creation:**
- [ ] Can create task with title only
- [ ] Can create task with title and description
- [ ] Cannot create task with empty title
- [ ] Form clears after successful creation
- [ ] New task appears at top of list

**Task Display:**
- [ ] All tasks display with title, description, status
- [ ] Completed tasks show strikethrough styling
- [ ] Tasks ordered by creation date (newest first)
- [ ] Empty state message shows when no tasks exist
- [ ] Green theme is consistently applied
- [ ] SwiftPay logo is displayed in header

**Task Editing:**
- [ ] Edit button shows edit form with current data
- [ ] Can update title and description
- [ ] Cannot save with empty title
- [ ] Cancel button discards changes
- [ ] Updated task displays immediately

**Task Completion:**
- [ ] Can toggle task completion status
- [ ] Visual styling updates immediately
- [ ] Status persists after page refresh

**Task Deletion:**
- [ ] Delete button removes task from list
- [ ] Task removed immediately from UI
- [ ] Deletion persists after page refresh

**Delete All Tasks:**
- [ ] Delete All button displays with task count
- [ ] Button is disabled when no tasks exist
- [ ] Confirmation dialog shows correct task count
- [ ] All tasks are removed when confirmed
- [ ] Tasks are preserved when canceled
- [ ] Button shows "Deleting..." during operation
- [ ] Error handling works with rollback
- [ ] Empty state displays after successful deletion

**Error Handling:**
- [ ] Validation errors display clearly
- [ ] Network errors show user-friendly messages
- [ ] Loading indicators show during operations
- [ ] Delete all errors restore original task list

**Data Persistence:**
- [ ] Tasks persist after browser refresh
- [ ] Tasks persist after backend restart
- [ ] Tasks persist after full Docker restart

**Integration:**
- [ ] Services start with `docker compose up` within 10 seconds
- [ ] No CORS errors in browser console
- [ ] Hot reload works for both frontend and backend
- [ ] API documentation accessible at /docs

### CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow that implements a sequential, fail-fast approach to quality assurance. The pipeline is designed to catch simple issues early before investing time in more expensive operations.

**Pipeline Triggers:**
- All pull requests to main/master branches
- Direct pushes to main/master branches

**Key Features:**
- ✅ Sequential execution with explicit job dependencies
- ✅ Fail-fast approach - stops at first failure
- ✅ Parallel execution within stages for efficiency
- ✅ Comprehensive testing including property-based tests (100+ iterations)
- ✅ Full system integration validation with Docker Compose
- ✅ Intelligent caching for faster subsequent runs

#### Pipeline Stages

The CI pipeline executes in three distinct stages, each acting as a quality gate:

**Stage 1: Linting (Parallel Execution)**
- **Backend Linting**: Runs flake8 on Python code
- **Frontend Linting**: Runs ESLint on JavaScript/React code
- **Purpose**: Catch code style and syntax issues immediately
- **Duration**: ~1-2 minutes
- **Fail-Fast**: If linting fails, tests are skipped

**Stage 2: Testing (Parallel Execution, After Linting)**
- **Backend Tests**: Runs pytest with coverage reporting
  - Unit tests for API endpoints and repository operations
  - Property-based tests using Hypothesis (100+ iterations)
- **Frontend Tests**: Runs Vitest with React Testing Library
  - Integration tests for UI components
  - Property-based tests using fast-check (100+ iterations)
  - Delete All feature tests
- **Purpose**: Verify functionality and correctness
- **Duration**: ~2-3 minutes
- **Fail-Fast**: If tests fail, Docker validation is skipped

**Stage 3: Docker Validation (Sequential Execution, After Tests)**
- **Docker Build Verification**: Builds backend and frontend images
- **Docker Compose Validation**: 
  - Validates docker-compose.yml syntax
  - Starts all services (MySQL, backend, frontend)
  - Performs health checks on backend and frontend
  - Displays logs on failure
  - Cleans up containers and volumes
- **Purpose**: Verify complete system integration
- **Duration**: ~3-5 minutes
- **Fail-Fast**: Stops immediately on any failure

#### Dependency Graph

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
         ┌───────────▼───────────┐
         │  Docker Build Verify  │           ← Stage 3: Docker (Sequential)
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │Docker Compose Validate│
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │    CI Success Summary │           ← Final confirmation
         └───────────────────────┘
```

#### Execution Order and Fail-Fast Behavior

The pipeline enforces strict execution order using GitHub Actions' `needs` keyword:

1. **Linting runs first** (parallel):
   - `backend-linting` (no dependencies)
   - `frontend-linting` (no dependencies)
   - If either fails → entire pipeline stops

2. **Tests run after linting** (parallel):
   - `backend-tests` needs `backend-linting`
   - `frontend-tests` needs `frontend-linting`
   - If either fails → Docker validation is skipped

3. **Docker validation runs after tests** (sequential):
   - `docker-build` (runs in parallel with tests for efficiency)
   - `docker-compose-validation` needs `[backend-tests, frontend-tests, docker-build]`
   - If any dependency fails → validation is skipped

4. **Summary job confirms success**:
   - `ci-success` needs all previous jobs
   - Only runs if all checks pass

**Fail-Fast Configuration:**
- All critical steps use `continue-on-error: false` (or omit it, as false is default)
- Failed jobs immediately stop the pipeline
- Dependent jobs are automatically skipped
- Clear status indicators show which stage failed

#### Caching Strategy

The pipeline uses intelligent caching to speed up subsequent runs:

**Backend Cache:**
```yaml
key: ${{ runner.os }}-pip-${{ hashFiles('backend/requirements.txt', 'backend/requirements-dev.txt') }}
```
- Caches pip packages based on requirements file hashes
- Cache invalidates automatically when dependencies change
- Typical speedup: 30-60 seconds per run

**Frontend Cache:**
```yaml
key: ${{ runner.os }}-node-${{ hashFiles('frontend/package.json') }}
```
- Caches npm packages based on package.json hash
- Cache invalidates automatically when dependencies change
- Typical speedup: 45-90 seconds per run

#### Testing the Pipeline Locally

You can test the CI pipeline locally using [act](https://github.com/nektos/act), a tool that runs GitHub Actions locally:

**Install act:**
```bash
# macOS
brew install act

# Linux
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Windows (with Chocolatey)
choco install act-cli
```

**Run the entire pipeline:**
```bash
# Run all jobs
act pull_request

# Run with verbose output
act pull_request -v
```

**Run specific jobs:**
```bash
# Run only linting jobs
act pull_request -j backend-linting
act pull_request -j frontend-linting

# Run only test jobs
act pull_request -j backend-tests
act pull_request -j frontend-tests

# Run Docker validation
act pull_request -j docker-compose-validation
```

**Simulate different scenarios:**
```bash
# Test with a specific event
act push

# Test with environment variables
act pull_request --env NODE_VERSION=18 --env PYTHON_VERSION=3.11

# Use a specific Docker image for the runner
act pull_request -P ubuntu-latest=catthehacker/ubuntu:act-latest
```

**Limitations of local testing:**
- Some GitHub-specific features may not work identically
- Caching behavior may differ from GitHub's infrastructure
- Secrets and environment variables need to be provided manually
- Docker-in-Docker scenarios may require additional configuration

**Alternative: Manual validation**
```bash
# Validate workflow syntax
docker run --rm -v $(pwd):/repo ghcr.io/rhysd/actionlint:latest -color

# Or install actionlint locally
brew install actionlint  # macOS
actionlint .github/workflows/ci.yml
```

#### Monitoring Pipeline Execution

**In GitHub UI:**
1. Navigate to the "Actions" tab in your repository
2. Select a workflow run to see the execution graph
3. Click on individual jobs to see detailed logs
4. Failed jobs show clear error messages and logs

**Status Checks:**
- All jobs must pass before merging pull requests
- Branch protection rules enforce CI success
- Clear visual indicators show pipeline status

**Debugging Failed Runs:**
1. Check which stage failed (linting, tests, or Docker)
2. Review the job logs for specific error messages
3. For Docker failures, check the "Show Docker Compose logs" step
4. Reproduce locally using the same commands from the workflow
5. Use `act` to test fixes before pushing

#### Pipeline Performance

**Typical Execution Times:**
- **Linting Stage**: 1-2 minutes (parallel)
- **Testing Stage**: 2-3 minutes (parallel, after linting)
- **Docker Stage**: 3-5 minutes (sequential, after tests)
- **Total Duration**: 6-10 minutes (with caching)
- **First Run**: 10-15 minutes (without cache)

**Optimization Features:**
- Parallel execution within stages
- Dependency caching (pip, npm)
- Early termination on failures
- Efficient Docker layer caching

All property-based tests run with 100+ iterations in CI to ensure comprehensive coverage.

## 🔧 Development

**Recommended Workflow:**
1. Review requirements and design documents
2. Implement feature following tasks.md
3. Write tests (unit + property-based)
4. Verify tests pass
5. Manual testing
6. Commit when all tests pass

### Making Changes

**Frontend Changes:**
1. Edit files in `frontend/src/`
2. Changes are automatically reflected (HMR enabled)
3. No restart needed
4. Run tests: `cd frontend && npm test`
5. Verify in browser: http://localhost:3000

**Backend Changes:**
1. Edit files in `backend/`
2. FastAPI auto-reloads with `--reload` flag
3. No restart needed
4. Run tests: `cd backend && pytest`
5. Check API docs: http://localhost:8000/docs

**Adding New Features:**
1. Update requirements.md with acceptance criteria
2. Update design.md with correctness properties
3. Update tasks.md with implementation steps
4. Implement following the task list
5. Write property-based tests for correctness properties
6. Write unit tests for specific cases
7. Update README.md with feature documentation

### Viewing Logs

```bash
# All services
docker compose logs -f

# Frontend only
docker compose logs -f frontend

# Backend only
docker compose logs -f backend
```

### Rebuilding Images

```bash
# Rebuild all images
docker compose build

# Rebuild specific service
docker compose build frontend
docker compose build backend
```

## 💾 Data Persistence

### Storage Approach

The application uses MySQL 8.0 for persistent data storage:

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

**Architecture:**
- **Connection Pooling**: Context manager for efficient connection handling
- **Auto-Initialization**: Database schema created automatically on startup
- **Transaction Safety**: All writes committed immediately
- **Error Handling**: Graceful handling of connection and query errors

**Benefits:**
- ✅ ACID compliance for data integrity
- ✅ Concurrent access support
- ✅ Standard SQL queries
- ✅ Scalable storage
- ✅ Production-ready database engine
- ✅ Easy backup and restore with MySQL tools

**Docker Volume:**
MySQL data is stored in a Docker volume (`mysql-data`), ensuring:
- Data persists across container restarts
- Data survives `docker compose down`
- Can be backed up using Docker volume commands

**Database Connection:**
The backend connects to MySQL using:
- Host: `mysql` (Docker service name)
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
# Delete all tasks using the API
curl -X DELETE http://localhost:8000/api/tasks

# Or connect to MySQL and delete all tasks
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

### Frontend
- **Production:**
  - React 18.2.0 - UI library
  - React-DOM 18.2.0 - React rendering
  
- **Development:**
  - Vite 4.3.0 - Build tool and dev server
  - @vitejs/plugin-react 4.0.0 - React plugin for Vite
  - Vitest 1.0.4 - Test framework
  - @testing-library/react 14.1.2 - React testing utilities
  - @testing-library/user-event 14.5.1 - User interaction testing
  - @testing-library/jest-dom 6.1.5 - DOM matchers
  - jsdom 23.0.1 - DOM implementation for testing
  - fast-check 3.15.0 - Property-based testing library

### Backend
- **Production:**
  - FastAPI 0.104.1 - Web framework
  - Uvicorn[standard] 0.24.0 - ASGI server
  - Pydantic 2.5.0 - Data validation
  - mysql-connector-python 8.2.0 - MySQL database driver
  
- **Development:**
  - pytest 7.4.0 - Test framework
  - pytest-cov 4.1.0 - Coverage reporting
  - hypothesis 6.92.0 - Property-based testing library

## 🐛 Troubleshooting

### Frontend not loading
- Ensure port 3000 is not in use: `lsof -i :3000`
- Check frontend logs: `docker compose logs frontend`
- Verify frontend container is running: `docker compose ps`
- Clear browser cache and reload

### Backend not responding
- Ensure port 8000 is not in use: `lsof -i :8000`
- Check backend logs: `docker compose logs backend`
- Verify backend health: `curl http://localhost:8000/health`
- Check if data directory exists: `ls -la backend/data/`

### Tasks not persisting
- Verify MySQL is running: `docker compose ps mysql`
- Check MySQL logs: `docker compose logs mysql`
- Verify database connection: `docker compose exec mysql mysql -u taskuser -ptaskpassword taskmanager -e "SELECT COUNT(*) FROM tasks;"`
- Check backend logs for database errors: `docker compose logs backend`
- Ensure MySQL is healthy before backend starts: `docker compose config`

### CORS errors
- Verify backend CORS is configured for `http://localhost:3000`
- Check that frontend is accessing correct API URL via VITE_API_URL
- Ensure environment variables are loaded (restart dev server)

### API returns 404 for tasks
- Verify backend is running: `curl http://localhost:8000/health`
- Check API endpoint: `curl http://localhost:8000/api/tasks`
- Review backend logs: `docker compose logs backend`
- Check MySQL connection: `docker compose exec mysql mysql -u taskuser -ptaskpassword taskmanager -e "SELECT * FROM tasks;"`
- Verify MySQL service is healthy: `docker compose ps`

### Tests failing
**Frontend:**
- Clear node_modules: `rm -rf node_modules && npm install`
- Check test setup: Ensure `src/test/setup.js` exists
- Run with verbose: `npm test -- --reporter=verbose`

**Backend:**
- Clear pytest cache: `rm -rf .pytest_cache __pycache__`
- Reinstall dependencies: `pip install -r requirements.txt`
- Run with verbose: `pytest -v`
- Check hypothesis examples: `ls -la .hypothesis/examples/`

### Property-based tests failing
- Property tests use random data and may find edge cases
- Review the failing example in test output
- Check if the failure reveals a bug or incorrect test assumption
- Hypothesis stores failing examples in `.hypothesis/examples/`
- fast-check shows counterexamples in test output

### Docker Compose issues
- Validate configuration: `docker compose config`
- Rebuild images: `docker compose build --no-cache`
- Remove volumes: `docker compose down -v`
- Check disk space: `df -h`

## 📝 Notes

### Design Decisions

**Green Theme with SwiftPay Branding:**
- Professional green color scheme for modern appearance
- Consistent color usage throughout the application
- SwiftPay logo for brand identity
- Maintains excellent readability and accessibility
- Easy to customize for different brands

**MySQL Database:**
- Production-ready relational database
- ACID compliance for data integrity
- Supports concurrent access and transactions
- Standard SQL for queries
- Easy to scale and backup
- Repository pattern allows swapping to other databases

**Delete All Feature:**
- Confirmation dialog prevents accidental data loss
- Task count display for clarity
- Disabled state when no tasks exist
- Optimistic UI updates with error rollback
- Returns deleted count for verification

**No Authentication:**
- MVP scope focuses on core CRUD functionality
- Authentication can be added later without major refactoring
- All tasks are currently shared (no user isolation)

**Property-Based Testing:**
- Catches edge cases that manual testing misses
- Provides mathematical guarantees about correctness
- Each property runs 100+ iterations with random data
- Complements traditional unit tests

**Spec-Driven Development:**
- Requirements → Design → Tasks → Implementation
- Correctness properties defined before implementation
- Each property maps to specific acceptance criteria
- Ensures implementation matches specification

### Development Focus
- Optimized for local development with comprehensive testing
- Hot reload enabled for rapid iteration
- Minimal external dependencies
- Property-based testing for correctness guarantees
- Clear separation of concerns (repository pattern)

### Limitations
- No authentication or authorization
- No real-time updates (polling required)
- No task sharing or collaboration features
- Basic MySQL configuration (not optimized for high load)
- Single MySQL instance (no replication or clustering)

## 🤝 Contributing

### Development Process

2. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Implement Changes**:
   - Follow the spec-driven development approach
   - Write implementation first
   - Add property-based tests for correctness properties
   - Add unit tests for specific cases
   - Update documentation

4. **Run Tests**:
   ```bash
   # Backend tests
   cd backend && pytest -v
   
   # Frontend tests
   cd frontend && npm test
   ```

5. **Manual Testing**:
   - Complete the manual testing checklist
   - Verify data persistence
   - Test error scenarios

6. **Submit Pull Request**:
   - Ensure all tests pass
   - Update documentation if needed
   - Reference related requirements/tasks

**Pull Request Requirements:**
- ✅ All automated tests must pass (unit + property-based)
- ✅ Property-based tests run 100+ iterations
- ✅ No new linting errors
- ✅ Code coverage maintained or improved
- ✅ Manual testing checklist completed
- ✅ Documentation updated if API changes
- ✅ Correctness properties validated

## 📄 License

This is a demonstration project for educational purposes.

## 🔗 Resources

### Documentation
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

### Property-Based Testing
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/) - Python property-based testing
- [fast-check Documentation](https://fast-check.dev/) - JavaScript property-based testing
- [Property-Based Testing Guide](https://hypothesis.works/articles/what-is-property-based-testing/)

---

**Built with ❤️ using spec-driven development 📋**

**Tested with ✅ Property-Based Testing (Hypothesis & fast-check)**

**Styled with 🎨 Modern Green Theme & SwiftPay Branding**
