# Green Theme Hello World Fullstack Application

A modern fullstack web application featuring a green-themed React frontend and FastAPI backend, orchestrated with Docker Compose.

## 🚀 Features

- **React Frontend**: Modern React 18 with Vite for lightning-fast development
- **FastAPI Backend**: High-performance Python backend with automatic API documentation
- **Green Theme**: Beautiful, responsive green-themed UI design
- **Docker Compose**: One-command deployment for both services
- **Health Checks**: Built-in health monitoring for both services
- **CORS Configured**: Proper cross-origin resource sharing setup
- **Error Handling**: Comprehensive error handling with user-friendly messages

## 📋 Prerequisites

- Docker Desktop 4.0+ (includes Docker Compose)
- Git

Optional for local development:
- Node.js 18.17+ 
- Python 3.11+

## 🏃 Quick Start

### Using Docker Compose (Recommended)

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
   - API Documentation: http://localhost:8000/api/docs
   - Health Check: http://localhost:8000/health

4. **Stop the application**
   ```bash
   docker compose down
   ```

## 🏗️ Architecture

### Docker Networking

This application follows critical Docker networking best practices:

**Frontend → Backend Communication:**
- ✅ Frontend code uses `http://localhost:8000` to reach backend
- ❌ Frontend does NOT use Docker service names (like `http://backend:8000`)
- **Why?** Frontend React code runs in the browser, and browsers connect to localhost ports, not Docker internal networks

**Port Mappings:**
- Backend: `8000:8000` (exposes backend on localhost:8000)
- Frontend: `3000:80` (exposes frontend on localhost:3000, maps to nginx port 80 inside container)

**Service Communication:**
```
Browser → localhost:3000 → Frontend Container (nginx on port 80)
Browser → localhost:8000 → Backend Container (FastAPI on port 8000)
```

### Project Structure

```
.
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   ├── App.css              # Styling with green theme
│   │   ├── main.jsx             # React entry point
│   │   └── components/          # Reusable components
│   ├── Dockerfile               # Frontend container configuration
│   ├── nginx.conf               # Nginx web server configuration
│   ├── package.json             # Node.js dependencies
│   └── vite.config.js           # Vite build configuration
├── backend/
│   ├── main.py                  # FastAPI application
│   ├── Dockerfile               # Backend container configuration
│   ├── requirements.txt         # Python dependencies
│   └── tests/                   # Backend tests
├── docker-compose.yml           # Service orchestration
└── README.md                    # This file
```

## 🔧 Development

### Local Frontend Development

```bash
cd frontend
npm install
npm run dev
```

Access at: http://localhost:5173

### Local Backend Development

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Access at: http://localhost:8000

### Running Tests

**Backend Tests:**
```bash
cd backend
pytest
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

## 📡 API Endpoints

### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "healthy"
}
```

### GET /api/hello
Get hello world message with timestamp

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

## 🎨 Frontend Features

- **Green Theme**: Consistent green color palette
  - Primary: `#2ecc71`
  - Secondary: `#27ae60`
  - Dark: `#1e5631`
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages
- **Accessibility**: ARIA labels and semantic HTML

## 🐛 Troubleshooting

### Frontend can't connect to backend

**Problem:** Error message "Failed to fetch message from backend"

**Solution:**
1. Ensure backend is running: `docker compose ps`
2. Check backend health: `curl http://localhost:8000/health`
3. Verify backend logs: `docker compose logs backend`
4. Confirm frontend is using `http://localhost:8000` (not Docker service names)

### Port already in use

**Problem:** Error "port is already allocated"

**Solution:**
```bash
# Stop any existing containers
docker compose down

# If port 3000 or 8000 is still in use, find and stop the process
# On Mac/Linux:
lsof -ti:3000 -ti:8000 | xargs kill -9

# On Windows:
netstat -ano | findstr :3000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Docker build issues

**Problem:** Build fails or takes too long

**Solution:**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker compose build --no-cache
```

## 📝 Environment Variables

No environment variables are required for basic operation. The application uses hardcoded localhost URLs for simplicity and correctness.

**Why no VITE_API_URL?**
- Frontend code runs in browser
- Browser must use localhost to reach exposed Docker ports
- Environment variables for API URLs are unnecessary and can cause confusion

## 🚢 Deployment Considerations

For production deployment:

1. **Update API URLs**: Change `http://localhost:8000` to your production backend URL
2. **Enable HTTPS**: Configure SSL/TLS certificates
3. **Update CORS**: Restrict allowed origins to your production domains
4. **Environment Variables**: Use proper environment management
5. **Health Checks**: Configure proper health check intervals
6. **Logging**: Enable structured logging and monitoring
7. **Security**: Implement rate limiting, authentication, etc.

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📚 Additional Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 🔍 Technical Details

### Frontend Stack
- React 18.2.0
- Vite 4.4.0
- CSS3 with modern features
- Nginx for production serving

### Backend Stack
- Python 3.11
- FastAPI 0.104.0
- Uvicorn 0.24.0
- Pydantic for data validation

### DevOps
- Docker multi-stage builds
- Health check probes
- Graceful shutdown handling
- Container networking

---

**Made with ❤️ using React, FastAPI, and Docker**
