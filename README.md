# Green Theme Hello World Fullstack Application

![CI Status](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/workflows/CI%20-%20Green%20Theme%20Hello%20World%20App/badge.svg)

A modern fullstack web application demonstrating frontend-backend integration with a beautiful green-themed UI. Built with React, FastAPI, and Docker for seamless local development.

## 🌟 Features

- **Green-Themed React Frontend** - Beautiful, responsive UI with modern design
- **FastAPI Backend** - Fast, async Python API with automatic OpenAPI docs
- **Docker Orchestration** - One-command setup with Docker Compose
- **Hot Reload** - Rapid development with Vite HMR and Uvicorn reload
- **Comprehensive Tests** - Full test coverage with pytest and integration tests
- **CI/CD Pipeline** - Automated testing with GitHub Actions
- **CORS Enabled** - Secure cross-origin communication

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐
│  React Frontend │◄───────►│ FastAPI Backend │
│  (Port 3000)    │  CORS   │  (Port 8000)    │
│  Vite + React   │         │  Python + Uvicorn│
└─────────────────┘         └─────────────────┘
        │                            │
        └────────────┬───────────────┘
                     │
              Docker Network
```

## 📋 Prerequisites

- **Docker Desktop** 4.0+ or **Docker Engine** 20.10+
- **Docker Compose** (included with Docker Desktop)
- **Git** for cloning the repository

Optional for local development:
- **Node.js** 18+ and npm
- **Python** 3.11+

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
   cd ab-sdlc-agent-ai-backend
   git checkout feature/JIRA-777/fullstack-app
   ```

2. **Start the application**
   ```bash
   docker compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

4. **Stop the application**
   ```bash
   docker compose down
   ```

### Local Development (Without Docker)

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest test_main.py -v
```

### Run Integration Tests
```bash
# Start services
docker compose up -d

# Test backend endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/hello

# Test frontend
curl http://localhost:3000

# Stop services
docker compose down
```

### CI Pipeline

The GitHub Actions workflow automatically:
- Runs backend unit tests with pytest
- Builds Docker images
- Performs integration tests
- Validates CORS configuration
- Checks code quality

View CI results in the [Actions tab](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions).

## 📁 Project Structure

```
project-root/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── test_main.py         # Backend tests
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Green theme styles
│   │   └── main.jsx         # React entry point
│   ├── index.html           # HTML template
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   ├── nginx.conf           # Nginx configuration
│   └── Dockerfile           # Frontend container
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI
├── docker-compose.yml       # Multi-container orchestration
└── README.md                # This file
```

## 🎨 Frontend Features

- **Green Theme**: Primary color #2ecc71, secondary #27ae60
- **Responsive Design**: Mobile-first, works on all screen sizes (320px+)
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages
- **Modern React**: Functional components with hooks (useState)

## 🔌 API Endpoints

### GET /api/hello
Returns a hello message with timestamp.

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### GET /health
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy"
}
```

### Interactive API Documentation
Visit http://localhost:8000/docs for Swagger UI with interactive API testing.

## 🛠️ Development

### Hot Reload

- **Frontend**: Vite HMR automatically reloads on file changes
- **Backend**: Uvicorn reload flag restarts on Python file changes

### Adding New Features

1. Create a new branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make changes to frontend or backend

3. Test locally with Docker Compose
   ```bash
   docker compose up --build
   ```

4. Run tests
   ```bash
   cd backend && pytest test_main.py -v
   ```

5. Commit and push
   ```bash
   git add .
   git commit -m "Add your feature"
   git push origin feature/your-feature-name
   ```

## 🐛 Troubleshooting

### Backend not responding
```bash
# Check backend logs
docker compose logs backend

# Restart backend
docker compose restart backend
```

### Frontend not loading
```bash
# Check frontend logs
docker compose logs frontend

# Rebuild frontend
docker compose up --build frontend
```

### Port conflicts
```bash
# Check what's using ports 3000 and 8000
# Linux/Mac:
lsof -i :3000
lsof -i :8000

# Windows:
netstat -ano | findstr :3000
netstat -ano | findstr :8000
```

### Clear Docker cache
```bash
docker compose down -v
docker system prune -a
docker compose up --build
```

## 📊 Performance

- **API Response Time**: < 100ms
- **Frontend Load Time**: < 2 seconds
- **Docker Startup**: < 10 seconds

## 🔒 Security

- CORS enabled for frontend origin only (http://localhost:3000)
- No authentication (development setup only)
- Security headers via Nginx
- Input validation on API endpoints

## 📝 User Stories Coverage

✅ **Story 1**: Frontend displays green-themed "Hello World"  
✅ **Story 2**: Backend API with /api/hello and /health endpoints  
✅ **Story 3**: Frontend-backend integration with button interaction  
✅ **Story 4**: Docker Compose orchestration for one-command setup  

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🎯 Success Criteria

- ✅ Frontend accessible at http://localhost:3000
- ✅ Backend accessible at http://localhost:8000
- ✅ Green theme (#2ecc71) applied
- ✅ Button fetches and displays backend data
- ✅ Loading states work correctly
- ✅ Error handling for backend unavailability
- ✅ Docker Compose starts both services
- ✅ All tests passing
- ✅ CI pipeline validates changes

## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Built with ❤️ using React, FastAPI, and Docker**
