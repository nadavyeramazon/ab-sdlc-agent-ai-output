# Task Manager Application

> A production-ready task management application with comprehensive linting, testing, and security configurations.

A full-stack task management application with a React frontend and Python FastAPI backend, orchestrated with Docker Compose for local development. Create, view, update, and delete tasks with persistent storage.

## 🎯 Overview

This project is a complete CRUD application for managing tasks with:
- **Frontend**: React 18 + Vite with responsive UI
- **Backend**: Python FastAPI with RESTful API
- **Database**: MySQL 8.0 for persistent data storage
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
│   │   ├── App.css               # Task manager styling (green theme)
│   │   ├── main.jsx              # React entry point
│   │   ├── assets/
│   │   │   └── logo-swiftpay.png # Application logo
│   │   └── test/
│   │       └── setup.js          # Test configuration
│   ├── index.html                # HTML template
│   ├── package.json              # Frontend dependencies (includes fast-check)
│   ├── vite.config.js            # Vite configuration with test setup
│   ├── .env.example              # Environment variable template
│   ├── TEST_GUIDE.md             # Comprehensive testing documentation
│   └── Dockerfile                # Frontend Docker image
├── backend/                       # Python FastAPI backend
│   ├── app/
│   │   ├── main.py               # FastAPI application factory
│   │   ├── routes/
│   │   │   └── tasks.py          # Task endpoints (includes DELETE /tasks/all)
│   │   ├── services/
│   │   │   └── task_service.py   # Business logic layer
│   │   ├── repositories/
│   │   │   └── task_repository.py # Data persistence layer (MySQL)
│   │   └── models/
│   │       └── task.py           # Pydantic models
│   ├── tests/
│   │   ├── test_main.py          # API endpoint tests
│   │   ├── test_task_repository.py # Repository tests
│   │   └── test_delete_all_tasks.py # DELETE /tasks/all endpoint tests
│   ├── requirements.txt          # Backend dependencies
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
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

#### Run Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🎨 Features

### Task Management Features
- ✅ **Create Tasks**: Add new tasks with title and description
- ✅ **View Tasks**: Display all tasks ordered by creation date (newest first)
- ✅ **Edit Tasks**: Update task title and description
- ✅ **Delete Tasks**: Remove individual tasks or delete all tasks at once
- ✅ **Toggle Completion**: Mark tasks as complete or incomplete
- ✅ **Data Persistence**: Tasks persist across application restarts
- ✅ **Input Validation**: Client and server-side validation for data integrity
- ✅ **Error Handling**: User-friendly error messages for all operations

### UI Design & Branding
- ✅ **Modern Green Theme**: Fresh emerald color scheme (#10B981) for a professional look
- ✅ **SwiftPay Branding**: Custom SwiftPay logo for brand identity
- ✅ **Responsive Design**: Mobile-friendly interface that adapts to screen size
- ✅ **Visual Feedback**: Smooth animations and hover effects
- ✅ **Accessible Colors**: High contrast ratios for readability

### Frontend Features
- ✅ Responsive task management UI with green theme
- ✅ Task creation form with validation
- ✅ Inline task editing
- ✅ Visual distinction for completed tasks (strikethrough)
- ✅ Loading state indicators for all operations
- ✅ Error handling with user-friendly messages
- ✅ Success messages for bulk operations
- ✅ Empty state messaging
- ✅ Hot Module Replacement (HMR) for development
- ✅ Environment-based API URL configuration
- ✅ Comprehensive test coverage with property-based testing
- ✅ **Delete All Tasks Button**: Bulk delete with confirmation dialog
  - Appears only when tasks are present
  - Native confirmation dialog before deletion
  - Shows success message with deleted count
  - Disabled during deletion operation
  - Automatic UI refresh after deletion

### Backend Features
- ✅ RESTful API with FastAPI
- ✅ Full CRUD operations for tasks
- ✅ Bulk deletion endpoint for clearing all tasks
- ✅ Pydantic models for request/response validation
- ✅ MySQL database persistence with connection pooling
- ✅ Automatic database schema initialization
- ✅ Proper HTTP status codes (200, 201, 204, 404, 422, 500)
- ✅ CORS enabled for frontend communication
- ✅ Auto-reload during development
- ✅ Comprehensive test coverage with property-based testing

## 🎨 UI Theme & Design

### Color Palette

The application uses a modern **green theme** with emerald colors:

| Element | Color | Hex Code | Usage |
|---------|-------|----------|--------|
| **Primary Green** | Emerald 500 | `#10B981` | Buttons, accents, hover states |
| **Dark Green** | Emerald 600 | `#059669` | Active buttons, focus states |
| **Light Green** | Emerald 100 | `#D1FAE5` | (Reserved for future use) |
| **Very Light Green** | Emerald 50 | `#ECFDF5` | Success messages background |
| **Background Gradient** | Green gradient | `#10B981 → #059669` | App background |

**Accessibility:**
- All color combinations meet WCAG AA contrast ratio requirements
- Interactive elements have clear visual feedback
- Focus states are clearly visible

### Branding

**Logo:**
- The application displays the **SwiftPay** logo in the header
- Logo file: `frontend/src/assets/logo-swiftpay.png`
- Size: 64x64px (desktop), 48x48px (mobile)
- Positioned alongside the "Task Manager" heading

### Delete All Tasks Button

The **Delete All Tasks** button provides a convenient way to clear all tasks at once:

**Visual Design:**
- **Color**: Red (#FC8181) to indicate destructive action
- **Position**: Top-right of task list, next to "Task List" heading
- **Responsive**: Full-width on mobile, compact on desktop
- **States**:
  - Normal: Red background, white text
  - Hover: Darker red (#F56565) with elevation effect
  - Disabled: Gray background (#CBD5E0) during operation
  - Loading: Shows "Deleting..." text

**Behavior:**
```javascript
// When clicked:
1. Shows confirmation dialog: "Are you sure you want to delete all tasks? 
   This action cannot be undone."
2. If user clicks "Cancel": No action taken
3. If user clicks "OK":
   - Button disabled and shows "Deleting..."
   - Calls DELETE /api/tasks/all endpoint
   - On success:
     * Refreshes task list
     * Shows success message: "Successfully deleted N task(s)"
     * Success message auto-dismisses after 5 seconds
   - On error:
     * Shows error message
     * Button re-enabled
```

**Visibility:**
- Button **only appears** when tasks are present
- Button **hidden** when task list is empty
- Button **disabled** while tasks are loading

**User Experience:**
- ✅ Clear visual warning (red color)
- ✅ Confirmation dialog prevents accidental deletion
- ✅ Loading state provides feedback during operation
- ✅ Success message confirms action completion
- ✅ Shows count of deleted tasks for transparency
- ✅ Proper error handling with user-friendly messages

**Code Example:**
```jsx
{tasks.length > 0 && (
  <button
    onClick={handleDeleteAllTasks}
    disabled={deleteAllLoading || loading}
    className="btn-delete-all"
  >
    {deleteAllLoading ? 'Deleting...' : 'Delete All Tasks'}
  </button>
)}
```

**CSS Styling:**
```css
.btn-delete-all {
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #fc8181; /* Red for destructive action */
  color: white;
  white-space: nowrap;
}

.btn-delete-all:hover:not(:disabled) {
  background-color: #f56565;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(252, 129, 129, 0.4);
}
```

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
Delete a single task.

**Response (204 No Content):**
No response body.

**Response (404 Not Found):**
```json
{
  "detail": "Task not found"
}
```

### DELETE /api/tasks/all
Delete all tasks at once (bulk delete operation).

**Description:**
This endpoint provides a convenient way to clear all tasks from the database. Useful for testing, resetting the application state, or bulk cleanup operations.

**HTTP Method:** `DELETE`

**Path:** `/api/tasks/all`

**Request Body:** None required

**Response (200 OK):**
```json
{
  "success": true,
  "message": "All tasks deleted",
  "deletedCount": 5
}
```

**Response Fields:**
- `success` (boolean): Always `true` for successful deletion
- `message` (string): Human-readable success message
- `deletedCount` (integer): Number of tasks deleted (0 if no tasks existed)

**Response (500 Internal Server Error):**
Returned when a database error occurs during the delete operation.

```json
{
  "detail": "Error deleting tasks: Database connection error"
}
```

**Error Scenarios:**
- **Database Connection Failure**: If MySQL is unavailable or connection fails
- **Query Execution Error**: If the DELETE query fails
- **General Exceptions**: Any unexpected errors during the operation

**Example Usage:**

```bash
# Using curl
curl -X DELETE http://localhost:8000/api/tasks/all

# Using httpie
http DELETE http://localhost:8000/api/tasks/all

# Using JavaScript fetch
fetch('http://localhost:8000/api/tasks/all', { method: 'DELETE' })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log(`Deleted ${data.deletedCount} task(s)`);
    console.log(`Success: ${data.success}`);
    console.log(`Message: ${data.message}`);
  })
  .catch(error => console.error('Error deleting tasks:', error));
```

**Frontend Integration Example:**
```jsx
const handleDeleteAllTasks = async () => {
  const confirmed = window.confirm(
    'Are you sure you want to delete all tasks? This action cannot be undone.'
  );
  
  if (!confirmed) return;
  
  setDeleteAllLoading(true);
  
  try {
    const response = await fetch(`${API_URL}/api/tasks/all`, {
      method: 'DELETE'
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    await fetchTasks(); // Refresh task list
    
    setSuccessMessage(
      `Successfully deleted ${data.deletedCount} task${data.deletedCount !== 1 ? 's' : ''}`
    );
    
    // Auto-dismiss success message after 5 seconds
    setTimeout(() => setSuccessMessage(''), 5000);
  } catch (err) {
    setError('Failed to delete all tasks: ' + err.message);
  } finally {
    setDeleteAllLoading(false);
  }
};
```

**Implementation Notes:**
- ✅ **Idempotent**: Calling the endpoint multiple times is safe and produces the same result
- ✅ **Returns count**: Always returns the number of tasks deleted, even if 0
- ✅ **Atomic operation**: All tasks are deleted in a single database transaction
- ✅ **Cannot be undone**: Ensure proper confirmation dialogs in client applications
- ✅ **Frontend confirmation**: UI shows native confirmation dialog before execution
- ✅ **Success feedback**: Frontend displays count of deleted tasks
- ✅ **Error handling**: HTTP 500 status returned on server errors (not error object in body)
- ✅ **Route ordering**: Defined before `/tasks/{task_id}` to prevent path conflicts

**Route Ordering Note:**
The `/tasks/all` route must be defined **before** the `/tasks/{task_id}` route in the FastAPI router to ensure FastAPI matches the specific path first, rather than treating "all" as a task ID parameter.

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
pytest tests/test_main.py
pytest tests/test_task_repository.py
pytest tests/test_delete_all_tasks.py

# Run with coverage
pytest --cov=app --cov-report=html
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

The frontend test suite includes comprehensive tests for the Delete All Tasks feature:

**Delete All Button Tests:**
- ✅ Button appears when tasks are present
- ✅ Button hidden when no tasks exist
- ✅ Shows confirmation dialog on click
- ✅ Does not delete when user cancels confirmation
- ✅ Deletes all tasks when user confirms
- ✅ Shows success message with deleted count
- ✅ Uses singular/plural correctly ("1 task" vs "2 tasks")
- ✅ Shows error message on API failure
- ✅ Disables button during deletion operation
- ✅ Shows loading state ("Deleting...")

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

**API Service Tests:**
- ✅ `deleteAllTasks()` returns success response with deletedCount
- ✅ `deleteAllTasks()` throws error on failure (consistent error handling)
- ✅ Error handling consistency across all API operations

For detailed frontend testing documentation, see [frontend/TEST_GUIDE.md](frontend/TEST_GUIDE.md).

### Backend Test Coverage

The backend test suite includes:

**Unit Tests:**
- ✅ All API endpoints (GET, POST, PUT, DELETE)
- ✅ Bulk delete endpoint (DELETE /api/tasks/all)
- ✅ Request validation (empty titles, length limits)
- ✅ HTTP status codes (200, 201, 204, 404, 422, 500)
- ✅ Task repository CRUD operations
- ✅ Database persistence and connection handling
- ✅ Error handling for database errors and invalid data

**Delete All Tasks Tests (`tests/test_delete_all_tasks.py`):**
- ✅ Delete multiple tasks (returns correct count)
- ✅ Delete with empty database (returns 0 count)
- ✅ Delete single task (returns count of 1)
- ✅ Response JSON structure validation (success, message, deletedCount)
- ✅ Idempotent behavior (can call multiple times safely)
- ✅ Delete and recreate tasks workflow
- ✅ Delete tasks with mixed completion states
- ✅ Content-Type header validation
- ✅ Accurate deleted count for various scenarios (0, 1, 3, 5, 10 tasks)
- ✅ Database error handling
- ✅ Wrong HTTP methods (GET, POST, PUT) return 405
- ✅ Integration with other endpoints (create, update, get)
- ✅ GET /api/tasks returns empty list after delete all

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

**UI Theme & Branding:**
- [ ] Green color theme applied throughout UI
- [ ] SwiftPay logo displays correctly in header
- [ ] Logo scales properly on mobile devices
- [ ] All interactive elements use green accent colors
- [ ] Hover states show darker green
- [ ] Focus states are clearly visible

**Delete All Tasks Feature:**
- [ ] Delete All button appears when tasks exist
- [ ] Delete All button hidden when no tasks exist
- [ ] Clicking button shows confirmation dialog
- [ ] Confirmation message is clear and warns about permanence
- [ ] Canceling confirmation does not delete tasks
- [ ] Confirming deletes all tasks
- [ ] Success message shows correct count
- [ ] Success message uses singular for 1 task
- [ ] Success message uses plural for multiple tasks
- [ ] Success message auto-dismisses after 5 seconds
- [ ] Button disabled during deletion
- [ ] Button shows "Deleting..." during operation
- [ ] Task list refreshes after deletion
- [ ] Empty state message appears after deletion
- [ ] Error message displays on API failure
- [ ] Button works on mobile devices
- [ ] Button responsive design on different screens

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
- [ ] Delete button removes individual task from list
- [ ] Task removed immediately from UI
- [ ] Deletion persists after page refresh

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

For detailed CI/CD documentation, see the **CI/CD Pipeline** section below.

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
1. Edit files in `backend/app/`
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
# Use the bulk delete endpoint (easiest method)
curl -X DELETE http://localhost:8000/api/tasks/all

# Or use the Delete All button in the UI

# Or connect to MySQL and delete all tasks manually
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
- Check if MySQL is running: `docker compose ps mysql`

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

### Delete All endpoint returns 404
- Verify route ordering: `/tasks/all` must be defined **before** `/tasks/{task_id}`
- Check backend logs: `docker compose logs backend`
- Test endpoint directly: `curl -X DELETE http://localhost:8000/api/tasks/all`
- Restart backend: `docker compose restart backend`

### Delete All button not working
- Check browser console for JavaScript errors
- Verify backend API is accessible: `curl -X DELETE http://localhost:8000/api/tasks/all`
- Check if tasks exist: `curl http://localhost:8000/api/tasks`
- Review frontend logs: `docker compose logs frontend`
- Test confirmation dialog: Ensure browser allows native dialogs
- Check network tab for API request/response

### Tests failing
**Frontend:**
- Clear node_modules: `rm -rf node_modules && npm install`
- Check test setup: Ensure `src/test/setup.js` exists
- Run with verbose: `npm test -- --reporter=verbose`
- Check for mock issues with `window.confirm`

**Backend:**
- Clear pytest cache: `rm -rf .pytest_cache __pycache__`
- Reinstall dependencies: `pip install -r requirements.txt`
- Run with verbose: `pytest -v`
- Check hypothesis examples: `ls -la .hypothesis/examples/`
- Verify test database: `docker compose exec mysql mysql -u taskuser -ptaskpassword taskmanager_test -e "SHOW TABLES;"`

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

**UI Theme - Green Color Palette:**
- Emerald green (#10B981) chosen for modern, professional appearance
- Replaced previous blue/purple theme for fresh look
- Maintains accessibility with high contrast ratios
- Consistent use across all interactive elements
- Smooth transitions and hover effects

**Branding - SwiftPay Logo:**
- Custom logo reinforces brand identity
- Replaces generic "todo" logo
- Professional appearance suitable for production use
- Responsive sizing for different screen sizes

**Delete All Feature:**
- Red color (#FC8181) clearly indicates destructive action
- Native confirmation dialog prevents accidental deletion
- Success message provides transparency (shows deleted count)
- Button only visible when needed (tasks present)
- Disabled state prevents double-clicks during operation

**MySQL Database:**
- Production-ready relational database
- ACID compliance for data integrity
- Supports concurrent access and transactions
- Standard SQL for queries
- Easy to scale and backup
- Repository pattern allows swapping to other databases

**Bulk Delete Endpoint:**
- Provides convenient way to clear all tasks
- Useful for testing and development
- Returns count of deleted tasks for confirmation
- Idempotent operation - safe to call multiple times
- Atomic operation - all tasks deleted in single transaction
- Uses proper HTTP exception handling (500 status on errors)
- **Route ordering critical**: Must be defined before `/tasks/{task_id}` to avoid path conflicts

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
- Modern, accessible UI design

### Limitations
- No authentication or authorization
- No real-time updates (polling required)
- No task sharing or collaboration features
- Basic MySQL configuration (not optimized for high load)
- Single MySQL instance (no replication or clustering)
- Bulk delete operation cannot be undone
- Delete All uses native browser confirmation dialog (not custom modal)

## 🤝 Contributing

### Development Process

1. **Fork and Clone:**
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output.git
   cd ab-sdlc-agent-ai-output
   ```

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
   - Test UI theme and branding
   - Test Delete All functionality

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
- ✅ UI changes match design specifications

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
- [MySQL Documentation](https://dev.mysql.com/doc/)

### Property-Based Testing
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/) - Python property-based testing
- [fast-check Documentation](https://fast-check.dev/) - JavaScript property-based testing
- [Property-Based Testing Guide](https://hypothesis.works/articles/what-is-property-based-testing/)

---

**Built with ❤️ using spec-driven development 📋**

**Tested with ✅ Property-Based Testing (Hypothesis & fast-check)**

**Designed with 🎨 Modern UI/UX (Green Theme & SwiftPay Branding)**
