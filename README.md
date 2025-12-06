# SwiftPay Tasks Application

> A production-ready task management application with comprehensive linting, testing, and security configurations.

A full-stack task management application with a React frontend and Python FastAPI backend, orchestrated with Docker Compose for local development. Create, view, update, and delete tasks with persistent storage. Now featuring **SwiftPay** branding with a modern green color scheme.

## 🎯 Overview

This project is a complete CRUD application for managing tasks with:
- **Frontend**: React 18 + Vite with responsive UI and SwiftPay branding
- **Backend**: Python FastAPI with RESTful API
- **Database**: MySQL 8.0 for persistent data storage
- **Testing**: Comprehensive test suite with property-based testing (Hypothesis & fast-check)
- **Orchestration**: Docker Compose for local development
- **Hot Reload**: Live updates during development for both frontend and backend
- **Modern Design**: Green color theme with SwiftPay branding

## 🎨 Features

### Task Management Features
- ✅ **Create Tasks**: Add new tasks with title and description
- ✅ **View Tasks**: Display all tasks ordered by creation date (newest first)
- ✅ **Edit Tasks**: Update task title and description
- ✅ **Delete Tasks**: Remove individual tasks from the list
- ✅ **Delete All Tasks**: Remove all tasks at once with confirmation dialog
- ✅ **Toggle Completion**: Mark tasks as complete or incomplete
- ✅ **Data Persistence**: Tasks persist across application restarts
- ✅ **Input Validation**: Client and server-side validation for data integrity
- ✅ **Error Handling**: User-friendly error messages for all operations
- ✅ **SwiftPay Branding**: Professional branding with green color theme

### Delete All Tasks Feature

The application includes a powerful bulk deletion feature that allows users to clear all tasks at once:

**User Flow:**
1. When tasks exist, a "Delete All Tasks" button appears at the top-right of the task list
2. Clicking the button shows a confirmation dialog: "Are you sure you want to delete all tasks? This action cannot be undone."
3. Upon confirmation, all tasks are deleted from the database
4. The UI updates to show the empty state ("No tasks yet")
5. If the operation fails, an error message is displayed and tasks are restored (rollback)

**Technical Details:**
- **API Endpoint**: `DELETE /api/tasks/all`
- **Optimistic Updates**: Tasks are removed from the UI immediately
- **Error Rollback**: If deletion fails, tasks are restored to the UI
- **Auto-dismiss Errors**: Error messages automatically disappear after 5 seconds
- **Loading States**: Button shows "Deleting All..." during operation and is disabled
- **Conditional Rendering**: Button only appears when tasks exist

**Example Usage:**
```bash
# Using curl
curl -X DELETE http://localhost:8000/api/tasks/all

# Response when tasks exist
{"success": true, "deletedCount": 5}

# Response when no tasks exist
{"success": true, "deletedCount": 0}
```

### Frontend Features
- ✅ Responsive task management UI with SwiftPay branding
- ✅ Modern green color theme (emerald and teal accents)
- ✅ Task creation form with validation
- ✅ Inline task editing
- ✅ Bulk task deletion with confirmation
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
- ✅ Bulk delete operation for all tasks
- ✅ Pydantic models for request/response validation
- ✅ MySQL database persistence
- ✅ Automatic database schema initialization
- ✅ Proper HTTP status codes (200, 201, 204, 404, 422, 500)
- ✅ CORS enabled for frontend communication
- ✅ Auto-reload during development
- ✅ Comprehensive test coverage with property-based testing

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

## 💡 Color Theme

The application features a modern **green color theme** inspired by SwiftPay's branding:

| Element | Color | Usage |
|---------|-------|-------|
| **Primary Green** | `#10b981` (Emerald 500) | Gradient start, buttons, focus states, loading spinner, checkbox accent |
| **Dark Green** | `#047857` (Emerald 700) | Gradient end |
| **Hover Green** | `#059669` (Emerald 600) | Primary button hover state |
| **Teal** | `#14b8a6` (Teal 500) | Edit button background |
| **Dark Teal** | `#0d9488` (Teal 600) | Edit button hover state |

**Background Gradient:**
```css
background: linear-gradient(135deg, #10b981 0%, #047857 100%);
```

This creates a vibrant, professional appearance that aligns with modern design trends while maintaining excellent readability and accessibility.

## 📱 API Endpoints

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

### DELETE /api/tasks/all
Delete all tasks from the database.

**Response (200 OK):**
```json
{
  "success": true,
  "deletedCount": 5
}
```

**Response (500 Internal Server Error):**
```json
{
  "detail": "Failed to delete tasks"
}
```

**Example Usage:**
```bash
# Delete all tasks using curl
curl -X DELETE http://localhost:8000/api/tasks/all

# Response when tasks exist
{"success": true, "deletedCount": 3}

# Response when no tasks exist
{"success": true, "deletedCount": 0}
```

**UI Implementation:**
- Button appears only when tasks exist
- Confirmation dialog prevents accidental deletion
- Optimistic UI updates for instant feedback
- Error rollback restores tasks if operation fails
- Loading state disables button during operation
- Error messages auto-dismiss after 5 seconds

### DELETE /api/tasks/{task_id}
Delete a single task by ID.

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

## 📁 Project Structure

```
project-root/
├── frontend/                      # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx               # Main task manager component
│   │   ├── App.css               # Green theme styling
│   │   ├── assets/
│   │   │   └── logo.png          # SwiftPay logo
│   │   ├── __tests__/
│   │   │   ├── App.test.jsx     # Main component tests
│   │   │   └── DeleteAllTasks.test.jsx  # Delete all tests
│   │   ├── components/
│   │   │   ├── TaskList.jsx     # Task list with delete all button
│   │   │   ├── TaskForm.jsx     # Task creation/edit form
│   │   │   └── TaskItem.jsx     # Individual task display
│   │   ├── hooks/
│   │   │   └── useTasks.js      # Task state management hook
│   │   ├── services/
│   │   │   └── api.js           # API service with deleteAllTasks
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
pytest test_delete_all_tasks.py

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

### Frontend Test Coverage

The frontend test suite includes comprehensive tests for all features:

**Delete All Tasks Tests** (`DeleteAllTasks.test.jsx`):
- ✅ Delete all button rendering (only when tasks exist)
- ✅ Confirmation dialog behavior
- ✅ Complete delete all flow (button → confirm → API → empty state)
- ✅ Loading states during delete all operation
- ✅ Error handling and rollback on failure
- ✅ Auto-dismissing error messages after 5 seconds
- ✅ Edge cases (one task, many tasks)
- ✅ API integration (correct endpoint and method)

**Main App Tests** (`App.test.jsx`):
- ✅ Component rendering with SwiftPay branding
- ✅ Task creation flow
- ✅ Task editing flow
- ✅ Task deletion flow
- ✅ Task completion toggle
- ✅ Error handling for failed API calls
- ✅ Loading states for all operations
- ✅ Empty state display
- ✅ Property-based test for task ordering

For detailed frontend testing documentation, see [frontend/TEST_GUIDE.md](frontend/TEST_GUIDE.md).

### Backend Test Coverage

The backend test suite includes:

**Unit Tests:**
- ✅ All API endpoints (GET, POST, PUT, DELETE)
- ✅ Delete all tasks endpoint
- ✅ Request validation (empty titles, length limits)
- ✅ HTTP status codes (200, 201, 204, 404, 422, 500)
- ✅ Task repository CRUD operations
- ✅ Bulk delete operations
- ✅ MySQL database operations
- ✅ Error handling for database failures

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
- [ ] SwiftPay branding and green theme are visible

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
- [ ] Delete all button appears when tasks exist
- [ ] Delete all button hidden when no tasks exist
- [ ] Confirmation dialog appears on click
- [ ] Canceling confirmation keeps tasks intact
- [ ] Confirming deletes all tasks (including completed ones)
- [ ] UI updates to show empty state
- [ ] Button shows loading state during operation
- [ ] Error message appears if operation fails
- [ ] Error message auto-dismisses after 5 seconds
- [ ] Tasks are restored if deletion fails (rollback)

**Error Handling:**
- [ ] Validation errors display clearly
- [ ] Network errors show user-friendly messages
- [ ] Loading indicators show during operations

**Data Persistence:**
- [ ] Tasks persist after browser refresh
- [ ] Tasks persist after backend restart
- [ ] Tasks persist after full Docker restart

**Integration:**
- [ ] Services start with `docker compose up` within 10 seconds
- [ ] No CORS errors in browser console
- [ ] Hot reload works for both frontend and backend
- [ ] API documentation accessible at /docs

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

**SwiftPay Branding:**
- Modern, professional appearance with green color theme
- Emerald and teal color palette for accessibility and visual appeal
- Clean, minimalist design focused on usability
- Responsive layout optimized for all screen sizes

**Delete All Tasks Feature:**
- Confirmation dialog prevents accidental data loss
- Optimistic updates provide instant feedback
- Error rollback ensures data integrity
- Auto-dismissing errors reduce visual clutter
- Conditional rendering keeps UI clean when not needed

**MySQL Database:**
- Production-ready relational database
- ACID compliance for data integrity
- Supports concurrent access and transactions
- Standard SQL for queries
- Easy to scale and backup
- Repository pattern allows swapping to other databases

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

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Implement Changes**:
   - Follow the spec-driven development approach
   - Write implementation first
   - Add property-based tests for correctness properties
   - Add unit tests for specific cases

3. **Run Tests**:
   ```bash
   # Backend tests
   cd backend && pytest -v
   
   # Frontend tests
   cd frontend && npm test
   ```

4. **Manual Testing**:
   - Complete the manual testing checklist
   - Verify data persistence
   - Test error scenarios

5. **Submit Pull Request**:
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

## 📝 License

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

**Branded with 💳 SwiftPay Design**
