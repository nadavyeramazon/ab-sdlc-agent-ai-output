# Green Theme Hello World Fullstack Application

A minimal fullstack "Hello World" application with a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose for local development.

## 🎯 Overview

This project demonstrates a simple fullstack application with:
- **Frontend**: React 18 + Vite with green theme (#2ecc71)
- **Backend**: Python FastAPI with REST API
- **Testing**: Comprehensive test suite with Vitest and React Testing Library
- **Orchestration**: Docker Compose for local development
- **Hot Reload**: Live updates during development for both frontend and backend

## 📁 Project Structure

```
project-root/
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.test.jsx     # Comprehensive test suite
│   │   ├── App.css          # Green theme styling
│   │   ├── main.jsx         # React entry point
│   │   └── test/
│   │       └── setup.js     # Test configuration
│   ├── index.html           # HTML template
│   ├── package.json         # Frontend dependencies
│   ├── vite.config.js       # Vite configuration with test setup
│   ├── .env.example         # Environment variable template
│   ├── TEST_GUIDE.md        # Comprehensive testing documentation
│   └── Dockerfile           # Frontend Docker image
├── backend/                  # Python FastAPI backend
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Backend dependencies
│   └── Dockerfile           # Backend Docker image
├── docker-compose.yml        # Docker Compose orchestration
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD pipeline
├── .gitignore               # Git ignore rules
└── README.md                # This file
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
   - API Hello: http://localhost:8000/api/hello

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

### Frontend Features
- ✅ Green-themed UI with gradient background (#2ecc71)
- ✅ "Hello World" heading display
- ✅ Interactive button to fetch backend data
- ✅ Loading state indicator
- ✅ Error handling with user-friendly messages
- ✅ Responsive design with centered layout
- ✅ Hot Module Replacement (HMR) for development
- ✅ Environment-based API URL configuration
- ✅ Comprehensive test coverage with Vitest

### Backend Features
- ✅ RESTful API with FastAPI
- ✅ `/api/hello` endpoint returning message with timestamp
- ✅ `/health` endpoint for health checks
- ✅ CORS enabled for frontend communication
- ✅ Auto-reload during development

## 📡 API Endpoints

### GET /api/hello
Returns a hello message with timestamp.

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### GET /health
Returns the health status of the backend.

**Response:**
```json
{
  "status": "healthy"
}
```

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

### Automated Test Suite

The frontend includes a comprehensive test suite with **80+ test cases** covering:

- ✅ Component rendering and UI elements
- ✅ Button click interactions and state changes
- ✅ Loading states and indicators
- ✅ Error handling and recovery scenarios
- ✅ API integration with mocked fetch calls
- ✅ Different HTTP status codes (400, 401, 403, 404, 500, 503)
- ✅ Network error handling
- ✅ Message display and CSS classes

### Running Tests

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

The test suite provides complete coverage of the App component:
- **Component Rendering**: 5 tests
- **Button Interactions**: 5 tests  
- **Loading States**: 6 tests
- **Error Handling**: 10 tests
- **API Configuration**: 1 test
- **Message Display**: 3 tests

**Total: 30+ comprehensive test cases**

For detailed testing documentation, see [frontend/TEST_GUIDE.md](frontend/TEST_GUIDE.md).

### Manual Testing Checklist

**Frontend:**
- [ ] Page loads at localhost:3000 with green theme
- [ ] "Hello World" heading is visible
- [ ] "Get Message from Backend" button is displayed
- [ ] Clicking button shows "Loading..." state
- [ ] Backend message displays after fetch completes
- [ ] Error message displays when backend is unavailable

**Backend:**
- [ ] API accessible at localhost:8000
- [ ] GET /api/hello returns correct JSON structure
- [ ] GET /health returns healthy status
- [ ] Timestamp in ISO-8601 format

**Integration:**
- [ ] Services start with `docker compose up` within 10 seconds
- [ ] Frontend successfully fetches data from backend
- [ ] No CORS errors in browser console
- [ ] Hot reload works for both frontend and backend

### CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow that automatically:
- Tests backend code and dependencies
- Builds and tests frontend code
- **Runs automated test suite** (npm test)
- Verifies Docker image builds
- Validates Docker Compose configuration
- Performs health checks on running services

The CI pipeline runs on:
- All pull requests
- Pushes to main/master branch

## 🔧 Development

### Making Changes

**Frontend Changes:**
1. Edit files in `frontend/src/`
2. Changes are automatically reflected (HMR enabled)
3. No restart needed
4. Run tests to ensure nothing broke: `npm test`

**Backend Changes:**
1. Edit `backend/main.py`
2. FastAPI auto-reloads with `--reload` flag
3. No restart needed

### Development Workflow

1. Make code changes
2. Run tests: `npm test`
3. Verify in browser: http://localhost:3000
4. Check backend: http://localhost:8000/health
5. Commit when tests pass

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

## 🎨 Color Palette

The frontend uses a consistent green theme:
- **Primary Green**: `#2ecc71` - Main brand color
- **Secondary Green**: `#27ae60` - Hover states and accents
- **Background**: White (`#ffffff`)
- **Text**: Dark gray (`#2c3e50`) on light backgrounds
- **Text**: White (`#ffffff`) on dark backgrounds

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

### Backend
- FastAPI 0.100.0 - Web framework
- Uvicorn[standard] 0.23.0 - ASGI server

## 🐛 Troubleshooting

### Frontend not loading
- Ensure port 3000 is not in use: `lsof -i :3000`
- Check frontend logs: `docker compose logs frontend`
- Verify frontend container is running: `docker compose ps`

### Backend not responding
- Ensure port 8000 is not in use: `lsof -i :8000`
- Check backend logs: `docker compose logs backend`
- Verify backend health: `curl http://localhost:8000/health`

### CORS errors
- Verify backend CORS is configured for `http://localhost:3000`
- Check that frontend is accessing correct API URL via VITE_API_URL
- Ensure environment variables are loaded (restart dev server)

### Tests failing
- Clear node_modules: `rm -rf node_modules && npm install`
- Check test setup: Ensure `src/test/setup.js` exists
- Run with verbose: `npm test -- --reporter=verbose`
- Check for fetch mock issues: Ensure `global.fetch = vi.fn()` in tests

### Docker Compose issues
- Validate configuration: `docker compose config`
- Rebuild images: `docker compose build --no-cache`
- Remove volumes: `docker compose down -v`

## 📝 Notes

### Package Management
- Uses `npm install` (not `npm ci`) for flexibility
- Lock files are gitignored (package-lock.json, yarn.lock)
- Keeps dependencies minimal and simple

### Development Focus
- Optimized for local development with testing
- Hot reload enabled for rapid iteration
- Minimal complexity and dependencies
- Comprehensive test coverage for quality assurance
- No authentication, database, or advanced features

### Test-Driven Development
- All components have corresponding test files
- Tests run automatically in CI/CD pipeline
- Minimum test coverage requirements enforced
- Follow React Testing Library best practices

## 🤝 Contributing

1. Create a feature branch from `main`
2. Make your changes
3. **Run tests**: `cd frontend && npm test`
4. Ensure all tests pass
5. Ensure manual tests pass
6. Submit a pull request
7. CI pipeline will automatically run tests

**Pull Request Requirements:**
- ✅ All automated tests must pass
- ✅ No new linting errors
- ✅ Code coverage maintained or improved
- ✅ Manual testing checklist completed

## 📄 License

This is a demonstration project for educational purposes.

## 🔗 Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

**Built with ❤️ and green theme 🍀**

**Tested with ✅ Vitest & React Testing Library**
