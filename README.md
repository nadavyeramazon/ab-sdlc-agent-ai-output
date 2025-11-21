# Hello World Fullstack Application

A minimal fullstack "Hello World" application featuring a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose for local development.

## 🎯 Features

- **Frontend**: React 18 + Vite with green theme (#2ecc71)
- **Backend**: Python FastAPI with RESTful endpoints
- **Orchestration**: Docker Compose for easy local development
- **Hot Reload**: Both frontend and backend support live code changes
- **Simple Integration**: Button-click API interaction demo

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Git**: For cloning the repository

To verify your installations:
```bash
docker --version
docker compose version
git --version
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output.git
cd ab-sdlc-agent-ai-output
git checkout feature/JIRA-777/fullstack-app
```

### 2. Start the Application

Run both frontend and backend services with a single command:

```bash
docker compose up --build
```

**Expected output:**
- Backend will start on port 8000
- Frontend will start on port 3000
- Services should be ready within 15 seconds

### 3. Access the Application

- **Frontend**: http://localhost:3000
  - Displays "Hello World" with green theme
  - Click "Get Message from Backend" button to test API integration

- **Backend API**: http://localhost:8000
  - Health check: http://localhost:8000/health
  - Hello endpoint: http://localhost:8000/api/hello
  - API documentation: http://localhost:8000/docs (FastAPI auto-generated)

### 4. Stop the Application

Press `Ctrl+C` in the terminal, then run:

```bash
docker compose down
```

To remove volumes and clean up completely:

```bash
docker compose down -v
```

## 📁 Project Structure

```
project-root/
├── frontend/                    # React frontend application
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── App.css             # Green theme styles
│   │   └── main.jsx            # React entry point
│   ├── index.html              # HTML template
│   ├── package.json            # Frontend dependencies
│   ├── vite.config.js          # Vite configuration
│   ├── Dockerfile              # Frontend container image
│   └── .gitignore              # Frontend-specific ignores
├── backend/                     # Python FastAPI backend
│   ├── main.py                 # FastAPI application
│   ├── test_main.py            # Backend tests
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # Backend container image
├── .github/
│   └── workflows/
│       └── ci.yml              # CI/CD pipeline
├── docker-compose.yml          # Service orchestration
├── .gitignore                  # Root-level ignores
└── README.md                   # This file
```

## 🔌 API Endpoints

### Health Check
```
GET /health
```
**Response:**
```json
{
  "status": "healthy"
}
```

### Hello World
```
GET /api/hello
```
**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

## 🛠️ Development

### Running Without Docker

#### Backend (Python)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend (React)
```bash
cd frontend
npm install
npm run dev
```

### Running Tests

#### Backend Tests
```bash
cd backend
pip install -r requirements.txt pytest httpx
pytest
```

#### Frontend Tests
```bash
cd frontend
npm install
npm test
```

### Hot Reload

Both services support hot reload during development:

- **Backend**: Modify `backend/main.py` and save - changes apply immediately
- **Frontend**: Modify `frontend/src/App.jsx` and save - browser updates automatically (Vite HMR)

## 🎨 Color Scheme

The frontend uses a green theme:

- **Primary Green**: `#2ecc71` (background)
- **Secondary Green**: `#27ae60` (button)
- **Hover Green**: `#229954` (button hover state)
- **Text**: White for high contrast
- **Error**: `#ff6b6b` (error messages)

## 🧪 Testing the Integration

1. Navigate to http://localhost:3000
2. Verify "Hello World" heading displays with green background
3. Click "Get Message from Backend" button
4. Verify loading state appears briefly
5. Verify backend message displays with timestamp
6. Test error handling by stopping backend (`docker compose stop backend`)
7. Click button again and verify error message displays

## 🔧 Configuration

### Environment Variables

**Frontend** (`docker-compose.yml`):
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)

**Backend**:
- `PYTHONUNBUFFERED=1`: Ensures Python output is sent straight to terminal

### Port Configuration

Default ports (can be modified in `docker-compose.yml`):
- Frontend: 3000
- Backend: 8000

## 📊 CI/CD Pipeline

The project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that runs on:
- Pull requests
- Pushes to main/master branch

**Pipeline includes:**
1. Backend tests with Python 3.11
2. Frontend validation with Node.js 18
3. Docker Compose configuration validation
4. Image build verification

## 🚫 Out of Scope

This is a minimal implementation focused on demonstrating fullstack integration. The following are intentionally excluded:

- Authentication/Authorization
- Database integration
- Production builds or deployment configurations
- Advanced error logging or monitoring
- Automated E2E tests
- State management libraries (Redux, Zustand)
- CSS frameworks (Bootstrap, Tailwind)
- Lock files (package-lock.json, yarn.lock)

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Check what's using the port
lsof -i :3000  # or :8000

# Kill the process or change port in docker-compose.yml
```

### Docker Build Issues
```bash
# Clean rebuild
docker compose down -v
docker compose build --no-cache
docker compose up
```

### Frontend Can't Connect to Backend
- Verify both services are running: `docker compose ps`
- Check backend logs: `docker compose logs backend`
- Ensure CORS is configured correctly in `backend/main.py`

### Hot Reload Not Working
```bash
# Restart services
docker compose restart

# If still not working, rebuild
docker compose up --build
```

## 📝 Success Criteria

✅ User accesses http://localhost:3000 and sees green-themed "Hello World" page  
✅ Frontend button click fetches data from backend and displays response  
✅ GET http://localhost:8000/api/hello returns valid JSON with message and timestamp  
✅ GET http://localhost:8000/health returns `{"status": "healthy"}`  
✅ `docker compose up` starts both services successfully  
✅ Vite HMR works (edit App.jsx, see changes without refresh)  
✅ All acceptance criteria from user stories are met  

## 📄 License

This is a demo project for educational purposes.

## 🤝 Contributing

This is a demonstration project. For educational purposes only.

---

**Built with ❤️ using React, FastAPI, and Docker**
