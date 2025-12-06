# Task Manager Application - SwiftPay Edition

> A production-ready task management application with comprehensive linting, testing, and security configurations. Rebranded with SwiftPay's green theme.

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
- **Branding**: SwiftPay green theme (#10b981) throughout the application

## 🎨 SwiftPay Theme

The application has been rebranded with SwiftPay's green color scheme:

**Color Palette:**
- **Primary Green**: `#10b981` (rgb(16, 185, 129))
- **Dark Green** (hover states): `#059669` (rgb(5, 150, 105))
- **Transparency**: `rgba(16, 185, 129, 0.1)` for focus states

**Styled Elements:**
- Background gradient: Green gradient from `#10b981` to `#059669`
- Primary buttons: Green background with darker green hover states
- Input focus: Green border with subtle green shadow
- Task hover effects: Green border and shadow
- Checkbox accent color: Green checkmarks
- Loading indicators: Green spinner
- SwiftPay logo in header

## 🎨 Features

### Task Management Features
-  **Create Tasks**: Add new tasks with title and description
-  **View Tasks**: Display all tasks ordered by creation date (newest first)
-  **Edit Tasks**: Update task title and description
-  **Delete Tasks**: Remove individual tasks
-  **Delete All Tasks**: Bulk delete all tasks with confirmation dialog
-  **Toggle Completion**: Mark tasks as complete or incomplete
-  **Data Persistence**: Tasks persist in MySQL database across restarts
-  **Input Validation**: Client and server-side validation for data integrity
-  **Error Handling**: User-friendly error messages for all operations

### Frontend Features
-  **SwiftPay Branding**: Green theme (#10b981) throughout the application
-  **SwiftPay Logo**: Custom logo in application header
-  Responsive task management UI
-  Task creation form with validation
-  Inline task editing
-  Visual distinction for completed tasks (strikethrough)
-  **Delete All with Confirmation**: Two-step confirmation dialog before bulk deletion
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
-  **Bulk Delete**: DELETE /api/tasks endpoint to delete all tasks
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

---

**Built with ❤️ using Clean Architecture and Modern Development Practices**

**Tested with  Property-Based Testing (Hypothesis & fast-check)**

**Powered by SwiftPay 🌿**