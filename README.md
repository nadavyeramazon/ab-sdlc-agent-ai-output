# Green Theme Hello World Fullstack Application

A modern fullstack "Hello World" application demonstrating containerized development workflows with a green-themed React frontend and Python FastAPI backend.

## 🚀 Features

- **Green-themed responsive React UI** with modern design
- **FastAPI backend** with RESTful API endpoints
- **Docker Compose orchestration** for easy development
- **Hot Module Replacement (HMR)** for rapid frontend development
- **Auto-reload** for backend code changes
- **Comprehensive testing** with pytest
- **CI/CD pipeline** with GitHub Actions

## 📋 Prerequisites

Before running this application, ensure you have the following installed:

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)
- **Git**

To verify your installations:

```bash
docker --version
docker-compose --version
git --version
```

## 🛠️ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
git checkout feature/JIRA-777/fullstack-app
```

### 2. Start the Application

```bash
docker-compose up
```

This single command will:
- Build both frontend and backend Docker images
- Start both services
- Set up networking between services
- Enable hot-reload for development

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (FastAPI Swagger UI)
- **Health Check**: http://localhost:8000/health

## 🎯 Usage

1. Open your browser and navigate to http://localhost:3000
2. You'll see a green-themed page with "Hello World" heading
3. Click the **"Get Message from Backend"** button
4. The application will fetch data from the backend API
5. Backend message and timestamp will be displayed below the button

## 🏗️ Project Structure

```
.
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Green theme styles
│   │   └── main.jsx         # Application entry point
│   ├── index.html           # HTML template
│   ├── package.json         # Node.js dependencies
│   ├── vite.config.js       # Vite configuration
│   ├── Dockerfile           # Frontend container definition
│   └── nginx.conf           # Nginx server configuration
├── backend/
│   ├── main.py              # FastAPI application
│   ├── test_main.py         # Comprehensive test suite
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container definition
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI pipeline
├── docker-compose.yml       # Service orchestration
└── README.md               # This file
```

## 🧪 Running Tests

### Backend Tests

```bash
cd backend
pip install -r requirements.txt
pytest -v test_main.py
```

The test suite covers:
- ✅ Endpoint functionality (/api/hello, /health)
- ✅ Response structure validation
- ✅ CORS configuration
- ✅ Timestamp format validation (ISO 8601)
- ✅ Performance requirements (<100ms response time)

### Manual Integration Testing

```bash
# Test backend health
curl http://localhost:8000/health

# Test backend hello endpoint
curl http://localhost:8000/api/hello

# Test frontend
curl http://localhost:3000
```

## 🔧 Development

### Frontend Development

The frontend uses Vite with Hot Module Replacement (HMR). Changes to files in `frontend/src/` will automatically reload in the browser.

**To modify the frontend:**
1. Edit files in `frontend/src/`
2. Save your changes
3. Browser will automatically reload (HMR)

### Backend Development

The backend uses Uvicorn with `--reload` flag. Changes to Python files will automatically restart the server.

**To modify the backend:**
1. Edit `backend/main.py`
2. Save your changes
3. Server will automatically reload

## 🛑 Stopping the Application

```bash
# Stop services (Ctrl+C in the terminal where docker-compose is running)
# Or run:
docker-compose down
```

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

## 🎨 Design Specifications

### Color Palette

- **Primary Green**: `#2ecc71`
- **Secondary Green**: `#27ae60`
- **Light Background**: `#e8f8f5`
- **Text Color**: `#2c3e50`
- **Error Color**: `#e74c3c`

### Responsive Breakpoints

- **Mobile**: 320px - 480px
- **Tablet**: 481px - 768px
- **Desktop**: 769px+

## 🐛 Troubleshooting

### Port Already in Use

**Error:** `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solution:**
```bash
# Find and kill process using the port
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9

# Or change ports in docker-compose.yml
```

### Docker Build Fails

**Solution:**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

### Backend Not Accessible from Frontend

**Check:**
1. Backend service is healthy: `docker-compose ps`
2. Backend logs: `docker-compose logs backend`
3. CORS configuration in `backend/main.py`

### Frontend Not Loading

**Check:**
1. Frontend build succeeded: `docker-compose logs frontend`
2. Nginx configuration: `frontend/nginx.conf`
3. Browser console for errors (F12)

### Services Won't Start

**Solution:**
```bash
# Check Docker daemon is running
sudo systemctl status docker

# Restart Docker
sudo systemctl restart docker

# Check disk space
df -h
```

## 🔄 CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow that runs on every push and pull request:

- ✅ **Backend Tests**: Runs pytest with full coverage
- ✅ **Frontend Build**: Validates React build process
- ✅ **Docker Builds**: Tests Docker image creation
- ✅ **Integration Tests**: Validates full-stack communication

**Workflow file**: `.github/workflows/ci.yml`

## 📝 Technical Details

### Backend Stack

- **Python**: 3.11
- **FastAPI**: 0.100+
- **Uvicorn**: ASGI server with hot-reload
- **Pydantic**: Data validation

### Frontend Stack

- **React**: 18.2
- **Vite**: 5.0+ (build tool)
- **JavaScript**: ES6+
- **CSS**: CSS3 with flexbox

### Infrastructure

- **Docker**: Multi-stage builds
- **Docker Compose**: Service orchestration
- **Nginx**: Production-ready web server

## 🚢 Production Considerations

**Note:** This is a development setup. For production:

- ❌ Remove `--reload` flag from Uvicorn
- ❌ Remove volume mounts from docker-compose.yml
- ✅ Add HTTPS/SSL certificates
- ✅ Implement proper logging
- ✅ Add authentication/authorization
- ✅ Use production-grade database
- ✅ Implement rate limiting
- ✅ Add monitoring and alerting

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent async web framework
- React team for the powerful UI library
- Vite for blazing fast development experience
- Docker for containerization platform

---

**Happy Coding! 🎉**

For questions or issues, please open an issue on GitHub.
