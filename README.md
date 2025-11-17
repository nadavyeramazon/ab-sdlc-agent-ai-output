# Green Theme Hello World Fullstack Application

A simple fullstack "Hello World" application demonstrating modern web development with a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose.

## 🌟 Features

- **Frontend**: React 18+ with Vite for fast development and HMR (Hot Module Replacement)
- **Backend**: FastAPI with async endpoints and CORS support
- **Styling**: Beautiful green theme (#2ecc71, #27ae60) with responsive design
- **Containerization**: Docker Compose for easy orchestration of services
- **Development**: Hot reload enabled for both frontend and backend
- **Testing**: Comprehensive test suites for both frontend and backend
- **CI/CD**: GitHub Actions workflow for automated testing

## 📋 Prerequisites

Before running this application, ensure you have:

- **Docker** (version 20.10 or higher)
- **Docker Compose V2** (comes with Docker Desktop or install separately)

To verify your installation:
```bash
docker --version
docker compose version
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
git checkout feature/JIRA-777/fullstack-app
```

### 2. Start the Application

```bash
docker compose up --build
```

This command will:
- Build Docker images for frontend and backend
- Start both services
- Create a network for inter-service communication
- Enable hot reload for development

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Health Check**: http://localhost:8000/health

### 4. Stop the Application

```bash
docker compose down
```

## 🎯 User Stories & Acceptance Criteria

### ✅ Story 1: Frontend Display
- Page displays "Hello World" heading in styled component
- Background uses green theme (#2ecc71, #27ae60)
- Content is responsive and vertically/horizontally centered
- Accessible via http://localhost:3000
- Built with React 18+ functional components

### ✅ Story 2: Backend API
- GET /api/hello returns JSON with message and ISO 8601 timestamp
- GET /health returns healthy status
- Backend runs on port 8000
- CORS enabled for localhost:3000
- Response time < 100ms

### ✅ Story 3: Frontend-Backend Integration
- Button labeled "Get Message from Backend" triggers API call
- Fetches data from /api/hello endpoint
- Displays backend message and timestamp
- Shows loading indicator during fetch
- Displays error message if API call fails
- Uses React hooks (useState) for state management

### ✅ Story 4: Docker Compose Orchestration
- `docker compose up` starts both services
- Frontend accessible at localhost:3000
- Backend accessible at localhost:8000
- Services communicate via Docker network
- Vite dev server with HMR enabled
- Services start within 10 seconds
- `docker compose down` cleanly stops services

## 🏗️ Project Structure

```
project-root/
├── frontend/                  # React frontend application
│   ├── src/
│   │   ├── App.jsx           # Main App component
│   │   ├── App.css           # Green theme styling
│   │   ├── App.test.jsx      # Comprehensive frontend tests
│   │   ├── main.jsx          # React entry point
│   │   └── setupTests.js     # Test configuration
│   ├── index.html            # HTML template
│   ├── package.json          # Frontend dependencies
│   ├── vite.config.js        # Vite configuration
│   ├── Dockerfile            # Frontend container
│   └── .dockerignore         # Docker ignore rules
├── backend/                   # FastAPI backend application
│   ├── main.py               # FastAPI application
│   ├── test_main.py          # Comprehensive backend tests
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile            # Backend container
│   └── .dockerignore         # Docker ignore rules
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI workflow
├── docker-compose.yml         # Multi-container orchestration
└── README.md                  # This file
```

## 🧪 Testing

### Backend Tests

The backend includes comprehensive pytest tests covering:
- API endpoint functionality
- Response format validation
- CORS headers
- Health check
- Performance requirements
- Error handling

**Run backend tests locally:**

```bash
cd backend
pip install -r requirements.txt
pytest test_main.py -v
```

**Test coverage includes:**
- ✅ GET /api/hello returns correct message
- ✅ Timestamp in ISO 8601 format
- ✅ GET /health returns healthy status
- ✅ CORS headers present
- ✅ Response time < 200ms (test environment margin)
- ✅ JSON content type
- ✅ Preflight OPTIONS requests

### Frontend Tests

The frontend includes comprehensive Vitest tests covering:
- Component rendering
- User interactions
- API integration
- Loading states
- Error handling
- Multiple API calls

**Run frontend tests locally:**

```bash
cd frontend
npm install
npm test
```

**Test coverage includes:**
- ✅ Initial render with correct elements
- ✅ Button click triggers API call
- ✅ Loading state displays during fetch
- ✅ Backend message displays correctly
- ✅ Timestamp displays correctly
- ✅ Error handling for failed requests
- ✅ Button disabled during loading
- ✅ Multiple successful fetches

### Integration Testing

**Manual testing steps:**

1. **Start the application:**
   ```bash
   docker compose up --build
   ```

2. **Verify frontend loads:**
   - Open http://localhost:3000
   - Should see "Hello World" heading with green background

3. **Test backend directly:**
   ```bash
   curl http://localhost:8000/api/hello
   curl http://localhost:8000/health
   ```

4. **Test frontend-backend integration:**
   - Click "Get Message from Backend" button
   - Should see "Hello World from Backend!" message
   - Should see timestamp below message

5. **Test error handling:**
   - Stop backend: `docker compose stop backend`
   - Click button in frontend
   - Should see error message
   - Restart: `docker compose up backend`

6. **Test hot reload (development):**
   - Edit `frontend/src/App.jsx`
   - Changes should appear instantly without refresh
   - Edit `backend/main.py`
   - Backend should reload automatically

## 🔧 API Documentation

### Endpoints

#### GET /api/hello

Returns a greeting message with timestamp.

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Headers:**
- Content-Type: application/json
- Access-Control-Allow-Origin: http://localhost:3000

#### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## 🎨 Design Specifications

### Color Theme
- **Primary Green**: #2ecc71
- **Secondary Green**: #27ae60
- **Text on Green**: #ffffff
- **Background**: Linear gradient from primary to secondary green

### Layout
- Responsive design using Flexbox
- Centered content (vertical and horizontal)
- Mobile-first approach
- Smooth animations and transitions

## 🐳 Docker Configuration

### Frontend Container
- **Base Image**: node:20-alpine
- **Port**: 3000
- **Features**: Vite dev server with HMR
- **Volume Mounts**: Source code for hot reload

### Backend Container
- **Base Image**: python:3.11-slim
- **Port**: 8000
- **Features**: Uvicorn with auto-reload
- **Volume Mounts**: Source code for hot reload
- **Health Check**: Curl to /health endpoint

### Network
- Custom bridge network for service communication
- Backend accessible to frontend via service name

## 🔄 CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) automatically:
- Runs on push and pull requests
- Executes backend tests with pytest
- Executes frontend tests with Vitest
- Reports test results
- Fails build if tests fail

## 🐛 Troubleshooting

### Issue: Containers won't start

**Solution:**
```bash
# Clean up existing containers and volumes
docker compose down -v

# Rebuild from scratch
docker compose up --build
```

### Issue: Port already in use

**Solution:**
```bash
# Find process using port 3000 or 8000
lsof -i :3000
lsof -i :8000

# Kill the process or change ports in docker-compose.yml
```

### Issue: Frontend can't connect to backend

**Checklist:**
1. Verify backend is running: `docker compose ps`
2. Check backend health: `curl http://localhost:8000/health`
3. Verify CORS configuration in `backend/main.py`
4. Check browser console for errors
5. Ensure you're using `http://localhost:8000` (not container name) in frontend

### Issue: Hot reload not working

**Solution:**
```bash
# Ensure volumes are properly mounted
docker compose down
docker compose up --build

# For Docker Desktop on Windows/Mac, ensure file sharing is enabled
```

### Issue: Backend tests fail

**Solution:**
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run tests with verbose output
pytest test_main.py -v -s

# Check for missing dependencies or import errors
```

### Issue: Frontend tests fail

**Solution:**
```bash
# Install dependencies
cd frontend
npm install

# Run tests with verbose output
npm test -- --reporter=verbose

# Clear cache if needed
rm -rf node_modules package-lock.json
npm install
```

### Issue: Docker Compose V2 not found

**Solution:**
```bash
# If using older Docker, try with hyphen
docker-compose up --build

# Or upgrade to Docker Desktop which includes Compose V2
```

## 📊 Performance Metrics

- **Backend Response Time**: < 100ms (typically 5-20ms)
- **Frontend Load Time**: < 2 seconds
- **Container Startup**: < 10 seconds
- **HMR Update Time**: < 1 second

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests to ensure they pass
5. Commit changes: `git commit -am 'Add my feature'`
6. Push to branch: `git push origin feature/my-feature`
7. Create a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🎯 Success Criteria Checklist

- ✅ User can access frontend at http://localhost:3000
- ✅ Frontend displays green-themed "Hello World" with React functional components
- ✅ User can click button to fetch data from backend
- ✅ Backend responds with correct JSON message including timestamp
- ✅ Loading state displays during API call
- ✅ Error handling works when backend is unavailable
- ✅ All services start successfully with `docker compose up`
- ✅ Vite HMR provides instant feedback on code changes
- ✅ README includes clear setup, run, and testing instructions
- ✅ All user story acceptance criteria are met
- ✅ Application runs on fresh clone with zero manual configuration
- ✅ Comprehensive test suites for frontend and backend
- ✅ GitHub Actions CI workflow for automated testing

## 📞 Support

For issues, questions, or contributions, please open an issue in the GitHub repository.
