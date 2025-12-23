# Task Manager Application

> A production-ready task management application with comprehensive linting, testing, and security configurations.

A full-stack task management application with a React frontend and Python FastAPI backend, orchestrated with Docker Compose for local development. Create, view, update, and delete tasks with persistent MySQL storage.

## 🎯 Overview

This project is a complete CRUD application for managing tasks with:
- **Frontend**: React 18 + Vite with responsive UI, custom hooks, and green theme (SwiftPay branding)
- **Backend**: Python FastAPI with clean architecture (repository pattern, dependency injection)
- **Database**: MySQL 8.0 for persistent data storage with connection pooling
- **Testing**: Comprehensive test suite with property-based testing (Hypothesis & fast-check)
- **Code Quality**: Pre-commit hooks with Black, isort, flake8, Bandit, Prettier, ESLint
- **CI/CD**: GitHub Actions pipeline with sequential quality gates
- **Orchestration**: Docker Compose for local development
- **Hot Reload**: Live updates during development for both frontend and backend

## 🎨 Theme & Branding

The application features a professional emerald green theme with SwiftPay branding:

- **Primary Green**: `#10b981` (emerald-500)
- **Dark Green**: `#059669` (emerald-600)
- **Logo**: SwiftPay branding in header
- **Consistent styling**: Buttons, borders, accents, and animations
- **Modern UI**: Smooth transitions and hover effects

## ✨ Features

### Task Management
- **Create Tasks**: Add new tasks with title and optional description
- **View Tasks**: Display all tasks with creation date and completion status
- **Edit Tasks**: Modify existing task details
- **Delete Tasks**: Remove individual tasks
- **Toggle Completion**: Mark tasks as complete or incomplete

### Delete All Tasks
- **Inline Confirmation**: Custom confirmation dialog (no window.confirm)
- **Two-Step Process**: Prevents accidental deletion
- **Loading States**: Visual feedback during operation
- **Optimistic Updates**: Immediate UI feedback with automatic rollback on error
- **Error Handling**: 
  - Graceful rollback on API failure
  - Tasks remain visible after failed operations
  - Clear error messages displayed alongside task list
  - Users can retry or dismiss confirmation after errors
- **Conditional Display**: Button only visible when tasks exist

### Error Handling & User Experience

The application implements robust error handling with optimistic updates:

1. **Optimistic Updates**: UI updates immediately before API confirmation
2. **Automatic Rollback**: Failed operations automatically restore previous state
3. **Clear Feedback**: Error messages display without hiding content
4. **Graceful Degradation**: Errors don't break the user experience
5. **Retry Options**: Users can retry failed operations or cancel

**Example Flow - Delete All with Error**:
```
1. User clicks "Delete All Tasks" → Confirmation dialog appears
2. User confirms → Tasks clear immediately (optimistic update)
3. API call fails (500 error) → Tasks automatically restored (rollback)
4. Error message displays → Tasks remain visible
5. User can retry or cancel → Confirmation dialog stays open
```

### Component Architecture

**TaskList Component**:
- Displays loading states, errors, and tasks simultaneously when appropriate
- Shows error messages above task list during rollback scenarios
- Handles empty states with contextual messages
- Maintains task visibility during error states for better UX

---

For detailed installation and usage instructions, see sections below.
