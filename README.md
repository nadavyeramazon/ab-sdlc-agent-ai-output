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

## ✨ New Features

### Delete All Tasks
- **Inline Confirmation**: Custom confirmation dialog (no window.confirm)
- **Two-Step Process**: Prevents accidental deletion
- **Loading States**: Visual feedback during operation
- **Error Handling**: Rollback on failure with error messages
- **Conditional Display**: Button only visible when tasks exist

---

For detailed installation and usage instructions, see sections below.
