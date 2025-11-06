# Green Greeting Application 🌿

A beautiful full-stack web application with a green-themed UI that provides personalized greetings. Built with FastAPI backend and vanilla JavaScript frontend, containerized with Docker.

## ✨ Features

- **Green-themed UI**: Beautiful, responsive interface with various shades of green
- **Personalized Greetings**: Multiple greeting types (Hello, Hi, Welcome, Good Morning, etc.)
- **Real-time API Status**: Live connection status indicator
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Docker Containerized**: Easy deployment with Docker Compose
- **Health Checks**: Built-in health monitoring for both services
- **Error Handling**: Graceful error handling with user-friendly messages

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Ports 3000 and 8000 available

### Running the Application

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ab-sdlc-agent-ai-backend
   ```

2. **Start the application:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Stopping the Application
```bash
docker-compose down
```

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.11
- **Port**: 8000
- **Features**:
  - RESTful API endpoints
  - CORS enabled for frontend communication
  - Input validation with Pydantic
  - Health check endpoint
  - Multiple greeting types

### Frontend (Vanilla JavaScript)
- **Technology**: HTML5, CSS3, JavaScript (ES6+)
- **Server**: Nginx
- **Port**: 3000
- **Features**:
  - Responsive green-themed design
  - Interactive form with validation
  - Real-time API status monitoring
  - Smooth animations and transitions
  - Error handling and loading states

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with API info |
| GET | `/health` | Health check |
| POST | `/greet` | Generate personalized greeting |
| GET | `/greeting-types` | Get available greeting types |
| GET | `/docs` | Interactive API documentation |

### Example API Usage

**POST /greet**
```json
{
  "name": "John",
  "greeting_type": "hello"
}
```

**Response:**
```json
{
  "message": "Hello, John! Welcome to our green-themed application!",
  "user_name": "John",
  "greeting_type": "hello"
}
```

## 🎨 Greeting Types

- **hello**: Standard friendly greeting
- **hi**: Casual greeting
- **welcome**: Welcoming message
- **good_morning**: Morning greeting
- **good_afternoon**: Afternoon greeting
- **good_evening**: Evening greeting

## 🛠️ Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend Development
Serve the frontend directory with any static file server, or use the nginx container.

### Running Tests
```bash
cd backend
python -m pytest test_main.py -v
```

## 🔧 Configuration

### Environment Variables
- `PYTHONPATH`: Python path for backend
- `ENVIRONMENT`: Development/production environment

### Ports
- Frontend: 3000 (configurable in docker-compose.yml)
- Backend: 8000 (configurable in docker-compose.yml)

## 🐳 Docker Configuration

### Services
- **backend**: FastAPI application with Python 3.11
- **frontend**: Nginx serving static files

### Volumes
- Backend source code mounted for development
- Frontend files mounted read-only
- Cache volume for Python packages

### Network
- Custom bridge network for service communication
- Health checks for both services

## 🎯 Usage Examples

1. **Enter your name** in the input field
2. **Select a greeting type** from the dropdown
3. **Click "Get My Greeting"** to receive your personalized message
4. **Try different combinations** for various greeting styles

## 🔍 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Check what's using the port
lsof -i :3000
lsof -i :8000

# Stop conflicting services or change ports in docker-compose.yml
```

**API connection issues:**
- Check if backend container is running: `docker-compose logs backend`
- Verify API health: `curl http://localhost:8000/health`
- Check network connectivity between containers

**Frontend not loading:**
- Check nginx logs: `docker-compose logs frontend`
- Verify frontend container status: `docker-compose ps`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details.

---

**Enjoy your green greeting experience! 🌱✨**
