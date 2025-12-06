## Task Manager Application

> A production-ready task management application with comprehensive linting, testing, and security configurations.

A full-stack task management application with a React frontend and Python FastAPI backend, orchestrated with Docker Compose for local development. Create, view, update, and delete tasks with persistent MySQL storage.

## 🎯 Overview

This project is a complete CRUD application for managing tasks with:
- **Frontend**: React 18 + Vite with responsive UI, custom hooks, and SwiftPay branding
- **Backend**: Python FastAPI with clean architecture (repository pattern, dependency injection)
- **Database**: MySQL 8.0 for persistent data storage with connection pooling
- **Testing**: Comprehensive test suite with property-based testing (Hypothesis & fast-check)
- **Code Quality**: Pre-commit hooks with Black, isort, flake8, Bandit, Prettier, ESLint
- **CI/CD**: GitHub Actions pipeline with sequential quality gates
- **Orchestration**: Docker Compose for local development
- **Hot Reload**: Live updates during development for both frontend and backend

## 🎨 UI Design & Branding

### SwiftPay Theme
The application features SwiftPay's signature green branding:
- **Primary Color**: Emerald-500 (`#10b981`) - Used for buttons, accents, and interactive elements
- **Secondary Color**: Emerald-600 (`#059669`) - Used for hover states and gradients
- **Logo**: SwiftPay logo with clean, modern design
- **Gradient Background**: Smooth emerald gradient from emerald-500 to emerald-600

### UI Components
- **Delete All Button**: Outlined danger button (red) for bulk delete operations
  - Only visible when tasks exist
  - Requires confirmation via native browser dialog
  - Disabled state during deletion operation
  - Shows "Deleting..." feedback during operation
- **Task Cards**: Clean white cards with green accents on hover
- **Form Inputs**: Green focus states matching brand colors
- **Buttons**: Consistent styling with SwiftPay green theme

## 🚀 Features

### Task Management Features
-  **Create Tasks**: Add new tasks with title and description
-  **View Tasks**: Display all tasks ordered by creation date (newest first)
-  **Edit Tasks**: Update task title and description
-  **Delete Single Task**: Remove individual tasks with confirmation
-  **Delete All Tasks**: Bulk delete all tasks with double confirmation
  - Confirmation dialog: "Are you sure you want to delete ALL tasks? This action cannot be undone."
  - Only visible when tasks exist (automatically hides when list is empty)
  - Optimistic UI updates with automatic rollback on error
  - Loading state with "Deleting..." text during operation
-  **Toggle Completion**: Mark tasks as complete or incomplete
-  **Data Persistence**: Tasks persist in MySQL database across restarts
-  **Input Validation**: Client and server-side validation for data integrity
-  **Error Handling**: User-friendly error messages for all operations

### Frontend Features
-  Responsive task management UI with SwiftPay branding
-  Task creation form with validation
-  Inline task editing
-  Bulk operations (Delete All Tasks)
-  Visual distinction for completed tasks (strikethrough)
-  Loading state indicators for all operations
-  Error handling with user-friendly messages
-  Empty state messaging
-  Hot Module Replacement (HMR) for development
-  Environment-based API URL configuration
-  Comprehensive test coverage with property-based testing
-  Custom hooks for state management (`useTasks`)
-  Reusable component architecture
-  Danger button styling for destructive actions

### Backend Features
-  RESTful API with FastAPI
-  Full CRUD operations for tasks
-  Bulk delete endpoint (DELETE /api/tasks)
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

### DELETE /api/tasks
Delete all tasks from the database.

**Request:** No request body required.

**Response (204 No Content):**
No response body. Returns empty response with HTTP 204 status code.

**Usage Notes:**
- This endpoint deletes ALL tasks from the database
- Use with caution as this operation cannot be undone
- Returns 204 even when no tasks exist (idempotent operation)
- Useful for clearing test data or resetting the application state
- Frontend provides confirmation dialog before calling this endpoint

**Example using curl:**
```bash
curl -X DELETE http://localhost:8000/api/tasks
```

**Example using JavaScript:**
```javascript
const response = await fetch('http://localhost:8000/api/tasks', {
  method: 'DELETE'
});
// response.status === 204
```

**Frontend Implementation:**
The frontend implements a two-step safety mechanism:
1. Button only shows when tasks exist (`tasks.length > 0`)
2. Native browser confirmation dialog: "Are you sure you want to delete ALL tasks? This action cannot be undone."
3. Optimistic UI update with rollback on error
4. Loading state during operation

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

## 🧪 Testing

### Testing Philosophy

This project uses a dual testing approach combining traditional unit tests with property-based testing:

- **Unit Tests**: Verify specific examples, edge cases, and integration points
- **Property-Based Tests**: Verify universal properties that should hold across all inputs

Property-based testing uses:
- **Backend**: Hypothesis library (Python)
- **Frontend**: fast-check library (JavaScript)

Each property test runs 100+ iterations with randomly generated inputs to catch edge cases that manual testing might miss.

### Test Coverage

**Frontend Test Coverage for Delete All Feature:**

*Unit Tests:*
-  Delete All button only renders when tasks exist
-  Delete All button shows confirmation dialog
-  Delete All button disabled during deletion
-  Delete All button shows "Deleting..." text during operation
-  Optimistic UI update (tasks cleared immediately)
-  State rollback on API error
-  Error message displayed on failure
-  Button hidden after successful deletion (when list becomes empty)

*Property-Based Tests:*
-  Delete All operation clears all tasks regardless of task count (1-100 tasks)
-  Delete All operation rollback preserves exact original state on error
-  Delete All button visibility correctly reflects task list state

*Integration Tests:*
-  Complete user flow: Create tasks → Delete All → Confirm → List empty
-  Complete error flow: Create tasks → Delete All → API fails → Rollback → Error shown

**API Test Coverage for Delete All Feature:**
-  DELETE /api/tasks returns 204 on success
-  DELETE /api/tasks is idempotent (returns 204 even when no tasks exist)
-  DELETE /api/tasks throws error on server failure
-  DELETE /api/tasks included in property-based error handling tests (100+ iterations)

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

For detailed testing documentation:
- Backend: See inline test documentation in `backend/tests/`
- Frontend: See `frontend/TEST_GUIDE.md`

## 🎨 Design Decisions & Notes

### UI/UX Decisions

**SwiftPay Branding:**
- Clean, modern green theme using emerald color palette
- Professional look suitable for financial services
- Consistent color usage across all interactive elements
- Smooth gradient background for visual appeal

**Delete All Button Design:**
- **Placement**: Between form and task list for easy access
- **Visibility**: Only shows when tasks exist (prevents confusion)
- **Color**: Red outline (danger styling) to signal destructive action
- **Confirmation**: Native browser dialog for familiarity and accessibility
- **Feedback**: Loading state and disabled state during operation
- **Hover Effect**: Fills with red background on hover for clear interaction feedback

**Safety Mechanisms for Bulk Delete:**
1. **Visual Distinction**: Danger styling (red) separates from primary actions (green)
2. **Conditional Rendering**: Button hidden when no tasks exist
3. **Confirmation Dialog**: Two-step process (click button → confirm dialog)
4. **Clear Warning**: Dialog text emphasizes irreversibility
5. **Loading State**: Prevents double-clicks and shows progress
6. **Optimistic Updates**: Immediate feedback with automatic rollback on error

### Technical Decisions

**Optimistic UI Updates:**
- Tasks cleared immediately from UI when Delete All is clicked
- Provides instant feedback and perceived performance
- Automatic rollback if API call fails
- Preserves exact original state including order and properties

**Native Confirmation Dialog:**
- Uses `window.confirm()` for simplicity and familiarity
- Cross-browser compatible
- Accessible by default (keyboard navigation works)
- No additional dependencies required
- Consistent UX across platforms

**Button State Management:**
- Separate loading state for Delete All (`deleteAllLoading`)
- Independent from individual delete operations
- Disabled state prevents multiple simultaneous operations
- Loading text provides clear feedback

## 🔧 Development

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

**SwiftPay Theme Colors:**
- Primary: `#10b981` (emerald-500)
- Dark: `#059669` (emerald-600)
- Usage: buttons, links, borders, focus states, loading indicators

**Danger Button Styling:**
- Border: `#ef4444` (red-500)
- Background: transparent → `#ef4444` on hover
- Color: `#ef4444` → white on hover
- Usage: destructive actions (Delete All)

## 📝 Recent Changes

### Version History

**Latest Update - SwiftPay Rebranding & Bulk Delete Feature:**
- ✅ Added Delete All Tasks button with confirmation dialog
- ✅ Rebranded UI with SwiftPay green theme (emerald-500/600)
- ✅ Added danger button styling for destructive actions
- ✅ Implemented optimistic UI updates with rollback
- ✅ Added comprehensive tests for Delete All functionality
- ✅ Updated API to support bulk delete operations
- ✅ Enhanced UX with loading states and confirmation dialogs

**Previous Updates:**
- Full CRUD operations for tasks
- Property-based testing implementation
- CI/CD pipeline with GitHub Actions
- Docker Compose orchestration
- MySQL data persistence

## 🤝 Contributing

### Code Style

**Python:**
- Follow PEP 8 style guide
- Use Black for formatting (line length: 100)
- Use type hints where appropriate
- Document functions and classes with docstrings

**JavaScript:**
- Use ESLint recommended rules
- Use Prettier for formatting (2-space indentation, semicolons, single quotes)
- Use meaningful variable and function names
- Add JSDoc comments for complex functions
- Follow React best practices (hooks, functional components)

**CSS:**
- Use consistent spacing (multiples of 0.25rem)
- Follow SwiftPay color palette for brand consistency
- Use semantic class names
- Group related styles together
- Comment complex selectors or calculations

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

**Styled with 🎨 SwiftPay Branding**

**Tested with ✅ Property-Based Testing (Hypothesis & fast-check)**
