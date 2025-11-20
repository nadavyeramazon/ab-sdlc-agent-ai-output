# Green Theme Hello World Fullstack Application

A minimal fullstack "Hello World" application demonstrating React frontend and Python FastAPI backend integration, orchestrated with Docker Compose for local development.

## 🎯 Features

- ✅ Green-themed React UI displaying "Hello World"
- ✅ FastAPI backend with REST endpoints
- ✅ Button to fetch dynamic data from backend
- ✅ Docker Compose orchestration for one-command startup
- ✅ Hot reload enabled for development
- ✅ CORS configured for frontend-backend communication

## 🛠 Technology Stack

- **Frontend**: React 18+, Vite
- **Backend**: Python 3.11+, FastAPI
- **Deployment**: Docker Compose (local development)

## 📁 Project Structure

```
project-root/
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Green theme styling
│   │   └── main.jsx         # React entry point
│   ├── index.html           # HTML template
│   ├── package.json         # Frontend dependencies
│   ├── vite.config.js       # Vite configuration
│   ├── Dockerfile           # Frontend Docker image
│   └── .dockerignore        # Docker ignore rules
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Backend Docker image
│   └── .dockerignore        # Docker ignore rules
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD pipeline
├── docker-compose.yml       # Docker Compose orchestration
├── .gitignore               # Git ignore rules (includes lock files)
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git

### Running the Application

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   git checkout feature/JIRA-777/fullstack-app
   ```

2. **Start all services with Docker Compose**:
   ```bash
   docker compose up --build
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Stop the services**:
   ```bash
   docker compose down
   ```

## 🧪 Manual Testing Checklist

- [ ] Frontend loads at http://localhost:3000 with green theme
- [ ] "Hello World" heading displays correctly
- [ ] Button click triggers API call
- [ ] Loading state shows during fetch
- [ ] Backend response displays on page
- [ ] Error handling works when backend is down
- [ ] Health endpoint responds at http://localhost:8000/health
- [ ] Services start successfully with `docker compose up`
- [ ] Hot reload works for frontend changes

## 📡 API Endpoints

### GET /api/hello

Returns a hello world message with timestamp.

**Response**: 200 OK
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### GET /health

Health check endpoint.

**Response**: 200 OK
```json
{
  "status": "healthy"
}
```

## 🎨 Color Scheme

- **Primary Green**: #2ecc71
- **Secondary Green**: #27ae60
- **Text on Green**: #ffffff

## 🔧 Development

### Running Services Separately

#### Backend Only

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Only

```bash
cd frontend
npm install
npm run dev
```

### Making Changes

- **Frontend**: Edit files in `frontend/src/` - hot reload will update automatically
- **Backend**: Edit `backend/main.py` - Uvicorn will reload automatically
- **Docker**: After changing Dockerfiles, rebuild with `docker compose up --build`

## 🔒 Important Notes

### Package Management

- **Frontend**: Use `npm install` (NOT `npm ci`)
- **Backend**: Use `pip install -r requirements.txt`
- **Lock files** (package-lock.json, yarn.lock, poetry.lock) are excluded via .gitignore

### CORS Configuration

The backend is configured to allow requests from:
- http://localhost:3000 (frontend development server)

Allowed methods: GET, POST, PUT, DELETE
Allowed headers: Content-Type

## 🚦 CI/CD Pipeline

The project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

1. **Backend Tests**: Validates Python dependencies and imports
2. **Frontend Tests**: Builds the frontend application
3. **Docker Build Verification**: Validates Docker Compose configuration and builds

Triggers:
- Pull requests to `main` or `master`
- Pushes to `main` or `master`

## 📝 Success Criteria

Implementation is complete when:

- ✅ User can access frontend at http://localhost:3000
- ✅ Frontend displays green-themed "Hello World" with React
- ✅ User can click button to fetch backend data
- ✅ Backend responds with JSON message including timestamp
- ✅ Health endpoint returns healthy status
- ✅ All services start with single `docker compose up` command
- ✅ Vite HMR works for frontend development
- ✅ No lock files present in repository
- ✅ Application runs successfully on localhost

## 🐛 Troubleshooting

### Port Already in Use

If ports 3000 or 8000 are already in use:
```bash
# Stop the containers
docker compose down

# Check what's using the ports
lsof -i :3000
lsof -i :8000

# Kill the process or change ports in docker-compose.yml
```

### Frontend Can't Connect to Backend

1. Ensure backend is running: `curl http://localhost:8000/health`
2. Check Docker network: `docker compose ps`
3. Verify CORS configuration in `backend/main.py`

### Docker Build Fails

```bash
# Clean Docker cache and rebuild
docker compose down -v
docker system prune -f
docker compose up --build
```

## 📜 License

This is a demonstration project for educational purposes.

## 👥 Contributing

This is a demo project. For production use, consider adding:
- Authentication and authorization
- Database integration
- Comprehensive testing suite
- Production deployment configurations
- Monitoring and logging
- Error tracking

## 🔗 Resources

- [React Documentation](https://react.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vite Documentation](https://vitejs.dev/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
