# Green Theme Hello World Fullstack Application

A simple fullstack "Hello World" application demonstrating frontend-backend integration with a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose. This application serves as a foundational template for modern web development with containerized services.

## 🎯 Features

- **Green-themed React frontend** with modern, responsive design
- **FastAPI backend** with RESTful API endpoints
- **Docker Compose orchestration** for easy development and deployment
- **Hot reload enabled** for both frontend (Vite HMR) and backend
- **Comprehensive test coverage** with pytest and React Testing Library
- **GitHub Actions CI/CD** pipeline for automated testing
- **CORS configured** for secure cross-origin requests
- **Error handling** and loading states for better UX

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker**: Version 20.10 or higher ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose**: Version 2.0 or higher ([Install Docker Compose](https://docs.docker.com/compose/install/))
- **Git**: For cloning the repository

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
- Build Docker images for both frontend and backend
- Start both services in containers
- Display logs from both services in your terminal

### 3. Access the Application

- **Frontend**: Open your browser and navigate to [http://localhost:3000](http://localhost:3000)
- **Backend API**: Available at [http://localhost:8000](http://localhost:8000)
- **API Documentation**: Interactive Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Test the Application

1. You should see a green-themed page with "Hello World" heading
2. Click the "Get Message from Backend" button
3. The backend will respond with a message and timestamp
4. The response will be displayed on the page

### 5. Stop the Application

```bash
docker compose down
```

To stop and remove all containers, networks, and volumes:

```bash
docker compose down -v
```

## 📁 Project Structure

```
project-root/
├── frontend/                  # React frontend application
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── App.css           # Styling with green theme
│   │   ├── App.test.jsx      # Frontend tests
│   │   ├── main.jsx          # React entry point
│   │   └── setupTests.js     # Test configuration
│   ├── index.html            # HTML template
│   ├── package.json          # Node.js dependencies
│   ├── vite.config.js        # Vite configuration
│   ├── nginx.conf            # Nginx configuration for production
│   ├── Dockerfile            # Multi-stage Docker build
│   └── .dockerignore         # Docker ignore patterns
├── backend/                   # FastAPI backend application
│   ├── main.py               # FastAPI application
│   ├── test_main.py          # Backend tests
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile            # Backend Docker build
│   └── .dockerignore         # Docker ignore patterns
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI pipeline
├── docker-compose.yml        # Docker Compose orchestration
├── docker-compose.dev.yml    # Development-specific config
└── README.md                 # This file
```

## 🛠️ Technology Stack

### Frontend
- **React** 18.2.0 - UI library
- **Vite** 5.0.8 - Build tool and dev server
- **CSS3** - Styling with green theme (#2ecc71, #27ae60)
- **React Testing Library** - Component testing
- **Vitest** - Test runner

### Backend
- **Python** 3.11
- **FastAPI** 0.109.0 - Web framework
- **Uvicorn** 0.27.0 - ASGI server
- **Pydantic** 2.5.3 - Data validation
- **pytest** 7.4.4 - Testing framework

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Production web server (frontend)
- **GitHub Actions** - CI/CD pipeline

## 🔌 API Endpoints

### GET /api/hello

Returns a greeting message with timestamp.

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### GET /health

Health check endpoint for service monitoring.

**Response:**
```json
{
  "status": "healthy"
}
```

## 🧪 Running Tests

### Backend Tests

```bash
# Run tests in Docker container
docker compose exec backend pytest -v

# Or run locally (requires Python 3.11+)
cd backend
pip install -r requirements.txt
pytest -v
```

### Frontend Tests

```bash
# Run tests in Docker container
docker compose exec frontend npm test

# Or run locally (requires Node.js 18+)
cd frontend
npm install
npm test
```

### Integration Tests

The CI pipeline runs comprehensive integration tests including:
- Unit tests for both frontend and backend
- Docker build verification
- End-to-end API testing
- CORS validation
- Service health checks

## 🔧 Development

### Hot Reload

Both services support hot reload during development:

- **Frontend**: Vite HMR automatically updates the browser when you edit files in `frontend/src/`
- **Backend**: Uvicorn reloads the server when you edit files in `backend/`

### Environment Variables

You can customize the application using environment variables in `docker-compose.yml`:

```yaml
backend:
  environment:
    - DEBUG=true
    - LOG_LEVEL=debug

frontend:
  environment:
    - VITE_API_URL=http://localhost:8000
```

### Development Mode

For development-specific configuration:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## 🐛 Troubleshooting

### Services Won't Start

1. **Check if ports are already in use:**
   ```bash
   # Check port 3000 (frontend)
   lsof -i :3000
   
   # Check port 8000 (backend)
   lsof -i :8000
   ```

2. **Clean up Docker resources:**
   ```bash
   docker compose down -v
   docker system prune -f
   ```

3. **Rebuild from scratch:**
   ```bash
   docker compose build --no-cache
   docker compose up
   ```

### Backend Returns 500 Error

1. Check backend logs:
   ```bash
   docker compose logs backend
   ```

2. Verify backend is healthy:
   ```bash
   curl http://localhost:8000/health
   ```

### Frontend Can't Connect to Backend

1. **Verify CORS configuration** in `backend/main.py`
2. **Check network connectivity:**
   ```bash
   docker compose exec frontend ping backend
   ```

3. **Verify backend is running:**
   ```bash
   docker compose ps
   ```

### Docker Compose Issues

1. **Update Docker Compose:**
   ```bash
   docker compose version
   # Should be 2.0 or higher
   ```

2. **Check Docker daemon:**
   ```bash
   docker ps
   ```

### Tests Failing

1. **Backend tests:**
   ```bash
   cd backend
   pytest -v --tb=long
   ```

2. **Frontend tests:**
   ```bash
   cd frontend
   npm test -- --reporter=verbose
   ```

## 📊 Performance

- **API Response Time**: < 100ms for both endpoints
- **Page Load Time**: < 2 seconds on standard broadband
- **Docker Services Start Time**: < 10 seconds

## 🔒 Security

- CORS configured to allow only frontend origin
- No sensitive data in code or configuration files
- Docker images use official base images
- Multi-stage builds minimize attack surface

## 🤝 Contributing

This is a template project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [React](https://react.dev/)
- Powered by [FastAPI](https://fastapi.tiangolo.com/)
- Containerized with [Docker](https://www.docker.com/)

## 📞 Support

For issues and questions:
- Open an issue in the GitHub repository
- Check the troubleshooting section above
- Review the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs)

---

**Happy Coding! 🚀**
