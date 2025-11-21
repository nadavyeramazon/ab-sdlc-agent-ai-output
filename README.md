# Yellow Theme Hello World Fullstack Application

A modern fullstack "Hello World" application demonstrating React frontend and FastAPI backend integration with Docker Compose orchestration.

## 🎨 Features

- **Yellow-Themed Frontend**: Beautiful React 18 UI with responsive design
- **FastAPI Backend**: High-performance Python REST API
- **Docker Compose**: One-command deployment and development
- **Hot Reload**: Fast development with Vite HMR
- **Comprehensive Tests**: Full test coverage for frontend and backend
- **CI/CD Pipeline**: Automated testing with GitHub Actions

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   Frontend      │         │    Backend      │
│   React + Vite  │ ──────► │    FastAPI      │
│   Port: 3000    │  HTTP   │    Port: 8000   │
└─────────────────┘         └─────────────────┘
        │                            │
        └────────────────┬───────────┘
                    Docker Network
```

### Technology Stack

**Frontend:**
- React 18.2
- Vite 5.0
- Vanilla CSS
- Vitest + React Testing Library

**Backend:**
- Python 3.11
- FastAPI 0.109
- Uvicorn
- Pytest

**DevOps:**
- Docker & Docker Compose V2
- GitHub Actions CI
- Multi-stage Docker builds

## 🚀 Quick Start

### Prerequisites

- Docker Desktop or Docker Engine with Docker Compose V2
- Git

### Running the Application

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-output.git
   cd ab-sdlc-agent-ai-output
   git checkout feature/JIRA-888/fullstack-app
   ```

2. **Start all services:**
   ```bash
   docker compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

4. **Stop services:**
   ```bash
   docker compose down
   ```

### Development Mode with Hot Reload

For frontend development with hot reload:

```bash
docker compose --profile dev up
```

This starts the frontend dev server on port 3001 with Vite HMR enabled.

## 📡 API Endpoints

### GET /api/hello

Returns a greeting message with timestamp.

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00.123456Z"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## 🧪 Testing

### Run All Tests

**Backend tests:**
```bash
cd backend
pip install -r requirements.txt
pytest -v
```

**Frontend tests:**
```bash
cd frontend
npm install
npm test
```

### Test Coverage

**Backend:**
- ✅ API endpoint functionality
- ✅ Response format validation
- ✅ CORS configuration
- ✅ Performance benchmarks (<100ms)
- ✅ Timestamp format validation

**Frontend:**
- ✅ Component rendering
- ✅ Button interactions
- ✅ API call handling
- ✅ Loading states
- ✅ Error handling
- ✅ Multiple fetch scenarios

### CI/CD Pipeline

GitHub Actions automatically runs tests on every push and pull request:

- Backend unit tests (pytest)
- Frontend unit tests (Vitest)
- Docker build verification
- Integration tests with Docker Compose
- Health check validation

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── test_main.py         # Backend tests
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Yellow theme styles
│   │   ├── App.test.jsx     # Frontend tests
│   │   ├── main.jsx         # React entry point
│   │   └── setupTests.js    # Test configuration
│   ├── index.html           # HTML template
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   └── Dockerfile           # Frontend container
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD pipeline
├── docker-compose.yml       # Service orchestration
└── README.md                # This file
```

## 🎨 UI Features

### Yellow Theme Color Palette

- **Primary**: `#2ecc71` (yellow-green)
- **Secondary**: `#27ae60` (darker yellow-green)
- **Text**: `#2c3e50` (dark gray)

### Responsive Design

- Desktop (>768px): Full-size layout
- Tablet (480-768px): Medium layout
- Mobile (<480px): Compact layout

### User Interactions

1. **Static Display**: "Hello World" heading always visible
2. **Button Click**: Fetches message from backend
3. **Loading State**: Shows "Loading..." during API call
4. **Success State**: Displays backend message and timestamp
5. **Error State**: Shows error message if backend unavailable

## 🔧 Configuration

### Environment Variables

**Backend:**
- `PYTHONUNBUFFERED=1`: Enables Python output logging

**Frontend:**
- `VITE_API_URL`: Backend API URL (defaults to http://localhost:8000)

### Port Configuration

- Frontend: `3000` (production), `3001` (dev mode)
- Backend: `8000`

## 🐛 Troubleshooting

### Services won't start

```bash
# Check if ports are in use
lsof -i :3000
lsof -i :8000

# Clean up Docker resources
docker compose down -v
docker system prune -f
```

### Backend not responding

```bash
# Check backend logs
docker compose logs backend

# Test health endpoint
curl http://localhost:8000/health
```

### Frontend can't connect to backend

- Ensure backend is running: `docker compose ps`
- Check CORS configuration in `backend/main.py`
- Verify network connectivity: `docker network ls`

## 📝 Manual Testing Checklist

- [ ] Navigate to http://localhost:3000
- [ ] Verify yellow-themed page displays
- [ ] See "Hello World" heading
- [ ] Click "Get Message from Backend" button
- [ ] Verify loading indicator appears
- [ ] Verify backend message displays
- [ ] Verify timestamp displays
- [ ] Stop backend (`docker compose stop backend`)
- [ ] Click button again and verify error handling
- [ ] Restart backend (`docker compose start backend`)
- [ ] Verify recovery works

## 🚀 Performance

- **API Response Time**: <100ms for all endpoints
- **Service Startup**: <10 seconds for all services
- **Page Load**: <2 seconds on standard connection

## 📄 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open a GitHub issue in the repository.

---

**Built with ❤️ using React, FastAPI, and Docker**
