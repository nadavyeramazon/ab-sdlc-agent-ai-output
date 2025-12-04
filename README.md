# Task Manager Application

A full-stack task management application with a React frontend and Python FastAPI backend, orchestrated with Docker Compose for local development. Create, view, update, and delete tasks with persistent storage.

## 🎯 Overview

This project is a complete CRUD application for managing tasks with:
- **Frontend**: React 18 + Vite with responsive UI
- **Backend**: Python FastAPI with RESTful API
- **Data Persistence**: JSON file-based storage with in-memory caching
- **Testing**: Comprehensive test suite with property-based testing (Hypothesis & fast-check)
- **Orchestration**: Docker Compose for local development
- **Hot Reload**: Live updates during development for both frontend and backend

## 📁 Project Structure

```
project-root/
├── frontend/                      # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx               # Main task manager component
│   │   ├── App.test.jsx          # Comprehensive test suite with property tests
│   │   ├── App.css               # Task manager styling
│   │   ├── main.jsx              # React entry point
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
│   ├── task_repository.py        # Data persistence layer
│   ├── test_main.py              # API endpoint tests with property tests
│   ├── test_task_repository.py   # Repository tests with property tests
│   ├── requirements.txt          # Backend dependencies (includes hypothesis)
│   ├── pytest.ini                # Pytest configuration
│   ├── README_TESTS.md           # Backend testing documentation
│   ├── data/                     # Persistent storage directory
│   │   └── tasks.json            # Task data (created automatically)
│   └── Dockerfile                # Backend Docker image
├── .kiro/                         # Kiro spec-driven development
│   └── specs/
│       └── task-manager-app/
│           ├── requirements.md   # Feature requirements
│           ├── design.md         # Design document with correctness properties
│           └── tasks.md          # Implementation plan
├── docker-compose.yml             # Docker Compose orchestration
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
- ✅ **Delete All Tasks**: Remove all tasks at once with a single operation
- ✅ **Toggle Completion**: Mark tasks as complete or incomplete
- ✅ **Data Persistence**: Tasks persist across application restarts
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

### Backend Features
- ✅ RESTful API with FastAPI
- ✅ Full CRUD operations for tasks
- ✅ Bulk delete operation for clearing all tasks
- ✅ Pydantic models for request/response validation
- ✅ JSON file-based persistence with in-memory caching
- ✅ Automatic data directory and file creation
- ✅ Proper HTTP status codes (200, 201, 204, 404, 422)
- ✅ CORS enabled for frontend communication
- ✅ Auto-reload during development
- ✅ Comprehensive test coverage with property-based testing

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
Delete all tasks at once (bulk delete operation).

**Response (204 No Content):**
No response body.

**Example:**
```bash
# Delete all tasks
curl -X DELETE http://localhost:8000/api/tasks

# Response: 204 No Content (no body)
```

**Notes:**
- This is a destructive operation that removes all tasks from storage
- No confirmation is required - the operation executes immediately
- The operation is idempotent - calling it multiple times is safe
- Returns 204 status code even when no tasks exist
- Useful for testing, development, or clearing all data

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
- ✅ Request validation (empty titles, length limits)
- ✅ HTTP status codes (200, 201, 204, 404, 422)
- ✅ Task repository CRUD operations
- ✅ Bulk delete operations (delete_all)
- ✅ File persistence and data loading
- ✅ Error handling for missing files and invalid data

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
- ✅ **Property 11**: Bulk delete completeness - delete_all removes all tasks from repository
- ✅ **Property 12**: Bulk delete persistence - empty state persists after repository restart
- ✅ **Property 13**: Bulk delete completeness (API) - DELETE /api/tasks removes all tasks

For detailed backend testing documentation, see [backend/README_TESTS.md](backend/README_TESTS.md).

### Frontend Test Coverage

The frontend test suite includes:

**Integration Tests:**
- ✅ Task creation flow (form → API → list update)
- ✅ Task editing flow (edit button → form → update → display)
- ✅ Task deletion flow (delete button → removal)
- ✅ Task completion toggle
- ✅ Error handling for failed API calls
- ✅ Loading states for all operations
- ✅ Empty state display

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

**Bulk Task Deletion:**
- [ ] DELETE /api/tasks removes all tasks
- [ ] Operation works when no tasks exist (idempotent)
- [ ] All tasks are immediately removed from UI
- [ ] Empty state persists after page refresh
- [ ] Individual task endpoints return 404 after bulk delete

**Error Handling:**
- [ ] Validation errors display clearly
- [ ] Network errors show user-friendly messages
- [ ] Loading indicators show during operations

**Data Persistence:**
- [ ] Tasks persist after browser refresh
- [ ] Tasks persist after backend restart
- [ ] Tasks persist after full Docker restart
- [ ] Bulk delete persists after restart

**Integration:**
- [ ] Services start with `docker compose up` within 10 seconds
- [ ] No CORS errors in browser console
- [ ] Hot reload works for both frontend and backend
- [ ] API documentation accessible at /docs

### CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow that automatically:
- Tests backend code with pytest (including property-based tests)
- Tests frontend code with Vitest (including property-based tests)
- Verifies Docker image builds
- Validates Docker Compose configuration
- Performs health checks on running services

The CI pipeline runs on:
- All pull requests
- Pushes to main/master branch

All property-based tests run with 100+ iterations in CI to ensure comprehensive coverage.

## 🔧 Development

### Development Workflow

This project follows a spec-driven development approach. All features are documented in `.kiro/specs/task-manager-app/`:

1. **requirements.md**: Feature requirements with acceptance criteria
2. **design.md**: Architecture, data models, and correctness properties
3. **tasks.md**: Implementation plan with task checklist

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

The application uses a simple JSON file-based persistence strategy:

**Storage Location:**
- File: `backend/data/tasks.json`
- Format: JSON array of task objects
- Created automatically on first run

**Architecture:**
- **In-Memory Cache**: Tasks loaded into memory on startup
- **Write-Through**: All modifications immediately written to disk
- **Lazy Loading**: Data loaded on first API request

**Benefits:**
- ✅ No external database required
- ✅ Easy to inspect and debug (human-readable JSON)
- ✅ Simple backup and restore (copy the file)
- ✅ Suitable for single-instance deployment
- ✅ Fast reads from in-memory cache

**Docker Volume:**
The `backend/data` directory is mounted as a Docker volume, ensuring:
- Tasks persist across container restarts
- Data survives `docker compose down`
- Hot reload doesn't affect data

**Future Scalability:**
The repository pattern allows easy migration to a database (PostgreSQL, MongoDB, etc.) without changing the API interface.

### Backup and Restore

**Backup:**
```bash
# Copy the tasks file
cp backend/data/tasks.json backup-tasks-$(date +%Y%m%d).json
```

**Restore:**
```bash
# Replace with backup
cp backup-tasks-20240115.json backend/data/tasks.json

# Restart backend to reload
docker compose restart backend
```

**Reset Data:**
```bash
# Option 1: Delete all tasks via API
curl -X DELETE http://localhost:8000/api/tasks

# Option 2: Delete file and restart
rm backend/data/tasks.json
docker compose restart backend
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
  - FastAPI 0.100.0 - Web framework
  - Uvicorn[standard] 0.23.0 - ASGI server
  - Pydantic 2.0+ - Data validation
  
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
- Verify data directory is mounted: `docker compose config`
- Check file permissions: `ls -la backend/data/`
- Verify tasks.json exists: `cat backend/data/tasks.json`
- Check backend logs for file I/O errors: `docker compose logs backend`

### CORS errors
- Verify backend CORS is configured for `http://localhost:3000`
- Check that frontend is accessing correct API URL via VITE_API_URL
- Ensure environment variables are loaded (restart dev server)

### API returns 404 for tasks
- Verify backend is running: `curl http://localhost:8000/health`
- Check API endpoint: `curl http://localhost:8000/api/tasks`
- Review backend logs: `docker compose logs backend`
- Verify tasks.json is readable: `cat backend/data/tasks.json`

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

**File-Based Storage:**
- Chosen for simplicity and ease of debugging
- No external database setup required
- Suitable for single-user or low-traffic scenarios
- Easy migration path to database via repository pattern

**No Authentication:**
- MVP scope focuses on core CRUD functionality
- Authentication can be added later without major refactoring
- All tasks are currently shared (no user isolation)

**Bulk Delete Operation:**
- Provides efficient way to clear all tasks with single API call
- Avoids N+1 problem (no need to delete tasks one by one)
- Useful for testing, development, and data management
- Idempotent design ensures safe repeated calls

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
- Single-instance deployment (no horizontal scaling)
- File-based storage (not suitable for high concurrency)
- No authentication or authorization
- No real-time updates (polling required)
- No task sharing or collaboration features
- Bulk delete has no confirmation (destructive operation)

## 🤝 Contributing

### Development Process

1. **Review Specifications**:
   - Read `.kiro/specs/task-manager-app/requirements.md`
   - Review `.kiro/specs/task-manager-app/design.md`
   - Check `.kiro/specs/task-manager-app/tasks.md` for implementation plan

2. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Implement Changes**:
   - Follow the spec-driven development approach
   - Write implementation first
   - Add property-based tests for correctness properties
   - Add unit tests for specific cases

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

### Project Documentation
- [Requirements Document](.kiro/specs/task-manager-app/requirements.md)
- [Design Document](.kiro/specs/task-manager-app/design.md)
- [Implementation Tasks](.kiro/specs/task-manager-app/tasks.md)
- [Backend Testing Guide](backend/README_TESTS.md)
- [Frontend Testing Guide](frontend/TEST_GUIDE.md)

---

**Built with ❤️ using spec-driven development 📋**

**Tested with ✅ Property-Based Testing (Hypothesis & fast-check)**
