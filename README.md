# Green Theme Hello World Fullstack Application

A minimal fullstack "Hello World" application with a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose for local development.

![Green Theme](https://img.shields.io/badge/Theme-Green%20%232ecc71-2ecc71?style=for-the-badge)
![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This project demonstrates a modern fullstack application setup with:

- **Frontend**: React 18+ with Vite bundler
- **Backend**: Python FastAPI with async endpoints
- **Orchestration**: Docker Compose for seamless local development
- **Theme**: Beautiful green color scheme (#2ecc71)

**Key Highlights:**
- ✅ Minimal dependencies - no bloat
- ✅ Hot reload enabled for both frontend and backend
- ✅ Docker Compose V2 for easy setup
- ✅ Clean, maintainable code structure
- ✅ Mobile-responsive UI design

## ✨ Features

### Frontend Features
- 🎨 Green-themed responsive UI (#2ecc71)
- ⚛️ React 18 with modern hooks (useState)
- ⚡ Vite for lightning-fast development
- 🔄 Real-time backend integration
- 📱 Mobile-responsive design
- 🎯 Loading states and error handling
- 🚫 No package-lock.json (minimal approach)

### Backend Features
- 🚀 FastAPI with async/await support
- 🔗 CORS enabled for frontend communication
- 📊 Health check endpoint
- ⏰ ISO-8601 timestamp support
- 🎯 Type hints and response validation
- 📦 Minimal dependencies (FastAPI + uvicorn only)

### DevOps Features
- 🐳 Docker Compose orchestration
- 🔄 Hot reload for both services
- 🔧 Development-optimized containers
- 🧪 GitHub Actions CI pipeline
- 📝 No lock files (npm, poetry, yarn)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Compose                        │
│  ┌──────────────────────┐  ┌──────────────────────┐    │
│  │  Frontend (React)    │  │  Backend (FastAPI)   │    │
│  │  Port: 3000          │◄─┤  Port: 8000          │    │
│  │  Vite Dev Server     │  │  Uvicorn Server      │    │
│  └──────────────────────┘  └──────────────────────┘    │
│           ▲                          ▲                   │
│           │                          │                   │
│      Volume Mount              Volume Mount              │
│     (Hot Reload)              (Hot Reload)               │
└─────────────────────────────────────────────────────────┘
```

**Service Communication:**
- Frontend → Backend: HTTP requests to `http://backend:8000`
- User → Frontend: Browser access via `http://localhost:3000`
- User → Backend: Direct API access via `http://localhost:8000`

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker**: Version 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose V2**: Included with Docker Desktop ([Verify installation](https://docs.docker.com/compose/install/))

### Verify Installation

```bash
# Check Docker version
docker --version
# Output: Docker version 20.10.x or higher

# Check Docker Compose version (V2 with space, not hyphen)
docker compose version
# Output: Docker Compose version v2.x.x or higher
```

**Note**: This project uses Docker Compose V2 syntax (`docker compose` with a space, not `docker-compose` with a hyphen).

## 🚀 Quick Start

Get the application running in 3 simple steps:

### 1. Clone the Repository

```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output.git
cd ab-sdlc-agent-ai-output
git checkout feature/JIRA-777/fullstack-app
```

### 2. Start the Application

```bash
# Start both frontend and backend services
docker compose up
```

**First-time startup takes 1-2 minutes** to:
- Build Docker images
- Install dependencies
- Start development servers

### 3. Access the Application

Once you see these logs, the application is ready:

```
backend-1   | INFO:     Uvicorn running on http://0.0.0.0:8000
frontend-1  | VITE ready in 500ms
frontend-1  | ➜  Local:   http://localhost:3000/
```

**URLs:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (FastAPI auto-generated)

### 4. Test the Integration

1. Open browser to http://localhost:3000
2. Click the green "Get Message from Backend" button
3. See the backend message with timestamp appear

## 📁 Project Structure

```
.
├── backend/                    # Python FastAPI backend
│   ├── Dockerfile             # Backend container configuration
│   ├── main.py                # FastAPI application with endpoints
│   └── requirements.txt       # Python dependencies (minimal)
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── App.css            # Green theme styling
│   │   └── main.jsx           # React entry point
│   ├── index.html             # HTML template
│   ├── vite.config.js         # Vite configuration
│   ├── package.json           # Node dependencies (minimal)
│   ├── Dockerfile             # Frontend container configuration
│   └── .gitignore             # Excludes node_modules, lock files
│
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI pipeline
│
├── docker-compose.yml         # Orchestration configuration
├── .gitignore                 # Project-wide exclusions
└── README.md                  # This file
```

## 📚 API Documentation

### Endpoint 1: Get Hello Message

**Request:**
```http
GET /api/hello HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-21T10:30:00.000000Z"
}
```

**Status Code:** 200 OK  
**Content-Type:** application/json

**Example with curl:**
```bash
curl http://localhost:8000/api/hello
```

### Endpoint 2: Health Check

**Request:**
```http
GET /health HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
{
  "status": "healthy"
}
```

**Status Code:** 200 OK  
**Content-Type:** application/json

**Example with curl:**
```bash
curl http://localhost:8000/health
```

### CORS Configuration

The backend enables CORS for the frontend origin:

- **Allowed Origin**: `http://localhost:3000`
- **Allowed Methods**: `GET`
- **Allowed Headers**: `Content-Type`

## 💻 Development

### Running Services Individually

#### Backend Only

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --port 8000

# Access API at http://localhost:8000
```

#### Frontend Only

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (use npm install, NOT npm ci)
npm install

# Run development server
npm run dev

# Access app at http://localhost:3000
```

### Docker Compose Commands

```bash
# Start services in foreground (see logs)
docker compose up

# Start services in background (detached mode)
docker compose up -d

# Stop services
docker compose down

# Rebuild images (after code changes to Dockerfile)
docker compose build

# View logs
docker compose logs

# View logs for specific service
docker compose logs frontend
docker compose logs backend

# Restart a single service
docker compose restart frontend

# Remove volumes (clean slate)
docker compose down -v
```

### Hot Reload

Both services support hot reload for rapid development:

- **Frontend**: Vite detects changes in `frontend/src/` and updates the browser instantly
- **Backend**: Uvicorn detects changes in `backend/main.py` and reloads the server automatically

**Example workflow:**
1. Edit `frontend/src/App.jsx`
2. Save the file
3. Browser automatically updates (< 2 seconds)

### Making Code Changes

#### Frontend Changes

1. Edit files in `frontend/src/`
2. Changes reflect immediately in browser
3. Check browser console for errors

**Example: Change the button text**
```jsx
// frontend/src/App.jsx
<button onClick={fetchMessage} disabled={loading}>
  Fetch Backend Data  {/* Changed text */}
</button>
```

#### Backend Changes

1. Edit `backend/main.py`
2. Uvicorn auto-reloads (watch terminal logs)
3. Test API with curl or frontend

**Example: Change the response message**
```python
# backend/main.py
@app.get("/api/hello")
async def get_hello() -> Dict[str, str]:
    return {
        "message": "Greetings from the Backend!",  # Changed message
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
```

## 🧪 Testing

### Manual Testing Checklist

#### Frontend Tests
- [ ] Page loads at http://localhost:3000
- [ ] "Hello World" heading displays in green
- [ ] Button is visible and styled correctly
- [ ] Clicking button shows "Loading..." state
- [ ] Backend message appears after button click
- [ ] Error message displays if backend is stopped
- [ ] Page is responsive on mobile/tablet/desktop

#### Backend Tests
- [ ] API accessible at http://localhost:8000
- [ ] GET /api/hello returns correct JSON format
- [ ] Timestamp is valid ISO-8601 format
- [ ] GET /health returns `{"status": "healthy"}`
- [ ] CORS headers present in responses
- [ ] Response time < 100ms

#### Integration Tests
- [ ] `docker compose up` starts both services
- [ ] Frontend can call backend successfully
- [ ] Services communicate across Docker network
- [ ] Hot reload works for frontend
- [ ] Hot reload works for backend

### Testing with curl

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test hello endpoint
curl http://localhost:8000/api/hello

# Test CORS headers
curl -I -X GET http://localhost:8000/api/hello

# Test from frontend origin
curl -H "Origin: http://localhost:3000" http://localhost:8000/api/hello
```

### CI/CD Pipeline

This project includes a GitHub Actions workflow that runs automatically on:
- Pull requests to any branch
- Push to main/master branch

**Pipeline stages:**
1. **Backend Tests**: Validates Python code and dependencies
2. **Frontend Tests**: Runs build verification
3. **Docker Validation**: Verifies Docker Compose configuration

View workflow runs at: `https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output/actions`

## 🔍 Troubleshooting

### Port Already in Use

**Error:**
```
Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:3000 -> 0.0.0.0:0: listen tcp 0.0.0.0:3000: bind: address already in use
```

**Solution:**
```bash
# Find process using port 3000 (or 8000)
lsof -ti:3000

# Kill the process (replace PID with actual process ID)
kill -9 <PID>

# Or use different ports in docker-compose.yml
```

### Frontend Cannot Connect to Backend

**Symptoms:**
- Browser shows CORS errors
- Network requests fail with ERR_CONNECTION_REFUSED

**Solutions:**

1. **Check backend is running:**
```bash
docker compose ps
# Both services should show "Up" status

curl http://localhost:8000/health
# Should return {"status": "healthy"}
```

2. **Check Docker network:**
```bash
docker compose down
docker compose up
```

3. **Verify backend URL in frontend code:**
```javascript
// frontend/src/App.jsx
const response = await fetch('http://localhost:8000/api/hello')
// Should be localhost:8000, not backend:8000 (that's for internal Docker network)
```

### Docker Build Fails

**Error:**
```
ERROR [backend internal] load metadata for docker.io/library/python:3.11-slim
```

**Solutions:**

1. **Check Docker daemon is running:**
```bash
docker ps
# Should list containers without errors
```

2. **Pull base images manually:**
```bash
docker pull python:3.11-slim
docker pull node:18-alpine
```

3. **Rebuild with no cache:**
```bash
docker compose build --no-cache
```

### Hot Reload Not Working

**Frontend hot reload issues:**

1. Check Vite configuration in `frontend/vite.config.js`:
```javascript
server: {
  host: true,  // Must be true for Docker
  port: 3000
}
```

2. Check volume mounts in `docker-compose.yml`:
```yaml
volumes:
  - ./frontend:/app
  - /app/node_modules  # Must exclude node_modules
```

**Backend hot reload issues:**

1. Check Uvicorn is running with `--reload` flag:
```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

2. Check volume mount includes source files:
```yaml
volumes:
  - ./backend:/app
```

### npm install Fails

**Error:**
```
npm ERR! code ENOLOCK
npm ERR! audit This command requires an existing lockfile.
```

**Solution:**
Always use `npm install` (NOT `npm ci`):

```bash
cd frontend
rm -f package-lock.json  # Remove if exists
npm install
```

### Permission Errors (Linux)

**Error:**
```
permission denied while trying to connect to Docker daemon socket
```

**Solutions:**

1. **Add user to docker group:**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

2. **Run with sudo (not recommended):**
```bash
sudo docker compose up
```

## 🎨 Customization

### Changing the Color Theme

Edit `frontend/src/App.css`:

```css
:root {
  --primary-green: #2ecc71;    /* Change this */
  --dark-green: #27ae60;        /* And this */
}
```

### Adding New API Endpoints

1. **Backend**: Add endpoint in `backend/main.py`
```python
@app.get("/api/custom")
async def custom_endpoint():
    return {"data": "custom response"}
```

2. **Frontend**: Call endpoint in `frontend/src/App.jsx`
```javascript
const response = await fetch('http://localhost:8000/api/custom')
const data = await response.json()
```

### Changing Ports

Edit `docker-compose.yml`:

```yaml
services:
  frontend:
    ports:
      - "3001:3000"  # Change external port (left side)
  
  backend:
    ports:
      - "8001:8000"  # Change external port (left side)
```

Remember to update the frontend fetch URL if backend port changes.

## 📄 License

This project is part of the AB SDLC Agent AI Output repository.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -am 'Add my feature'`
4. Push to branch: `git push origin feature/my-feature`
5. Open a Pull Request

## 📞 Support

For issues and questions:
- Create an issue in the GitHub repository
- Check existing issues for solutions
- Review troubleshooting section above

---

**Built with ❤️ using React, FastAPI, and Docker**

**Theme Color**: ![#2ecc71](https://via.placeholder.com/15/2ecc71/000000?text=+) `#2ecc71`
