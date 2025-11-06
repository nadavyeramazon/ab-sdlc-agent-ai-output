# Greeting Application 🌿

A resilient full-stack web application with a green-themed frontend and FastAPI backend that greets users by name, featuring comprehensive error handling and fallback mechanisms.

## 🏗️ Architecture

- **Backend**: FastAPI application in the `backend/` folder with enhanced error handling
- **Frontend**: JavaScript SPA with green theme in the `frontend/` folder  
- **Deployment**: Docker Compose for easy local development
- **Resilience**: Built-in fallback mechanisms for service unavailable scenarios

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ab-sdlc-agent-ai-backend
   ```

2. **Start the application**:
   ```bash
   docker-compose up --build
   ```

3. **Access the applications**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Setup

#### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the FastAPI server**:
   ```bash
   python main.py
   # or
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

#### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Serve the files** (using Python's built-in server):
   ```bash
   python -m http.server 3000
   ```

   Or use any static file server like `live-server`, `http-server`, etc.

## 🎨 Features

### Frontend
- **Green Theme**: Beautiful green-themed UI with gradients and animations
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Interactive Elements**: Smooth animations and hover effects
- **Enhanced Error Handling**: Comprehensive error messages, retry mechanisms, and fallback options
- **Service Status Monitoring**: Real-time health checks and connection monitoring
- **Fallback Mode**: Offline greeting capability when backend is unavailable
- **Accessibility**: Keyboard navigation and proper ARIA labels

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Resilient Architecture**: Global exception handling for service unavailable scenarios
- **CORS Support**: Configured to work with frontend
- **Input Validation**: Pydantic models with enhanced validation
- **Enhanced Health Checks**: Detailed health status with dependency information
- **Comprehensive Logging**: Structured logging with multiple output streams
- **Fallback Mechanisms**: Graceful degradation when external services are unavailable
- **Documentation**: Auto-generated API docs with Swagger UI

### Error Handling & Resilience
- **Service Unavailable Handling**: Specific handling for Bedrock and other external service failures
- **Retry Mechanisms**: Automatic retry with exponential backoff
- **Fallback Responses**: Alternative greeting generation when primary services fail
- **Circuit Breaker Pattern**: Prevents cascading failures
- **Graceful Degradation**: Application remains functional even when external dependencies fail

## 📚 API Endpoints

### GET `/`
Root endpoint with service information and available endpoints.

**Response**:
```json
{
  "message": "Welcome to the Resilient Greeting Service API",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "greet_post": "/greet",
    "greet_get": "/greet/{name}"
  }
}
```

### GET `/health`
Enhanced health check endpoint with detailed status information.

**Response**:
```json
{
  "status": "healthy",
  "service": "greeting-api",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "dependencies": {
    "database": "not_required",
    "external_services": "not_required"
  }
}
```

### POST `/greet`
Greet a user by name with enhanced error handling and fallback.

**Request Body**:
```json
{
  "name": "string"
}
```

**Success Response**:
```json
{
  "message": "Hello, John! Welcome to our green-themed application!",
  "name": "John",
  "status": "success"
}
```

**Fallback Response** (when external services are unavailable):
```json
{
  "message": "Hello, John! Welcome! (Service temporarily unavailable)",
  "name": "John",
  "status": "success"
}
```

### GET `/greet/{name}`
Greet a user by name via GET request with enhanced error handling.

**Success Response**:
```json
{
  "message": "Hello, John! Welcome to our green-themed application!",
  "name": "John",
  "status": "success"
}
```

## 🛡️ Error Handling

### Backend Error Handling
- **Global Exception Handler**: Catches and handles all unhandled exceptions
- **Service Unavailable Handler**: Specific handling for `serviceUnavailableException` and Bedrock errors
- **Validation Errors**: Clear error messages for invalid input
- **Timeout Handling**: Graceful handling of request timeouts
- **Logging**: Comprehensive error logging for debugging

### Frontend Error Handling
- **Service Status Monitoring**: Periodic health checks with visual indicators
- **Retry Mechanisms**: Automatic retry with exponential backoff for failed requests
- **Fallback Options**: Offline greeting capability with user-friendly interface
- **Connection Monitoring**: Real-time network status detection
- **User Feedback**: Clear error messages with actionable options

### Error Response Format
```json
{
  "error": "service_unavailable",
  "message": "External service temporarily unavailable. Using fallback response.",
  "status": "error"
}
```

## 🛠️ Development

### Project Structure
```
.
├── backend/
│   ├── main.py              # FastAPI application with error handling
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container config
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── styles.css          # Green-themed styles with error states
│   ├── script.js           # JavaScript with comprehensive error handling
│   ├── nginx.conf          # Nginx configuration
│   └── Dockerfile          # Frontend container config
├── docker-compose.yml      # Docker Compose with health checks
└── README.md              # This file
```

### Environment Variables

Create a `.env` file in the root directory:
```env
LOG_LEVEL=info
API_BASE_URL=http://localhost:8000
```

Available configurations:
- Backend runs on port `8000`
- Frontend runs on port `3000` (port `80` inside container)
- API base URL is set to `http://localhost:8000`
- Log level can be set to `debug`, `info`, `warning`, or `error`

### Service Monitoring

#### Health Check Endpoints
- Backend: `GET /health`
- Frontend: `curl http://localhost:3000` (via nginx)

#### Docker Health Checks
Both services include Docker health checks:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 5
  start_period: 60s
```

### Customization

#### Changing the Theme
Edit the CSS variables in `frontend/styles.css`:
```css
:root {
    --primary-green: #2d5f3f;
    --secondary-green: #4a7c59;
    --light-green: #68a47c;
    --fallback-yellow: #ffc107;  /* For fallback mode */
    --error-red: #dc3545;        /* For error states */
    /* ... */
}
```

#### Backend Configuration
Modify `backend/main.py` to:
- Add new endpoints
- Update error handling logic
- Configure external service integrations
- Modify logging levels and formats

## 🧪 Testing

### Backend Testing
```bash
cd backend

# Health check
curl http://localhost:8000/health

# Normal greeting
curl -X POST http://localhost:8000/greet \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User"}'

# Test error handling
curl -X POST http://localhost:8000/greet \
  -H "Content-Type: application/json" \
  -d '{"name":""}'
```

### Frontend Testing
1. Open http://localhost:3000 in your browser
2. Test normal functionality:
   - Enter a name and click "Get Greeting"
3. Test error scenarios:
   - Try submitting without a name
   - Stop the backend service to test fallback mode
   - Enable debug mode: `localStorage.setItem('debug', 'true')`

### Error Scenario Testing
1. **Service Unavailable**: Stop the backend and test frontend fallback
2. **Network Issues**: Disable network to test offline handling  
3. **Invalid Input**: Test with empty names or very long strings
4. **Timeout Handling**: Introduce delays to test timeout scenarios

## 🐳 Docker Commands

### Build and start services
```bash
docker-compose up --build
```

### Start services in background
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs
docker-compose logs backend
docker-compose logs frontend
```

### Health status
```bash
docker-compose ps
```

### Rebuild specific service
```bash
docker-compose build backend
docker-compose build frontend
```

## 🔧 Troubleshooting

### Common Issues

1. **Service Unavailable Errors**: 
   - Check if backend is running: `curl http://localhost:8000/health`
   - Review backend logs: `docker-compose logs backend`
   - Frontend will automatically use fallback mode

2. **CORS Errors**: 
   - Ensure backend CORS configuration includes your frontend URL
   - Check browser console for specific CORS error messages

3. **Connection Refused**: 
   - Verify both services are running: `docker-compose ps`
   - Check ports are not blocked by firewall
   - Wait for services to fully start (health checks)

4. **Build Failures**: 
   - Ensure Docker is running and you have sufficient disk space
   - Clear Docker cache: `docker system prune`

### Debug Mode
Enable comprehensive debugging:

**Frontend**:
```javascript
localStorage.setItem('debug', 'true');
// Reload the page to activate debug mode
```

**Backend**: Set environment variable:
```bash
LOG_LEVEL=debug docker-compose up
```

### Error Monitoring
- Backend logs are available in the `backend_logs` Docker volume
- Frontend errors are logged to browser console
- Health check failures are logged by Docker Compose

## 📦 Dependencies

### Backend
- FastAPI 0.104.1 - Web framework
- Uvicorn 0.24.0 - ASGI server
- Pydantic 2.5.0 - Data validation
- python-multipart 0.0.6 - Form handling
- httpx 0.25.2 - HTTP client for health checks

### Frontend
- Pure JavaScript (no frameworks)
- CSS3 with custom properties and error state styling
- HTML5 with enhanced error handling elements

### Infrastructure
- Docker & Docker Compose
- Nginx (for frontend serving)
- Volume mounts for log persistence

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes
4. Test error scenarios thoroughly
5. Update documentation if needed
6. Commit your changes: `git commit -am 'Add new feature'`
7. Push to the branch: `git push origin feature/new-feature`
8. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Future Enhancements

- [ ] Add user authentication with error handling
- [ ] Implement greeting history with offline sync
- [ ] Add more greeting templates with fallback options
- [ ] Include unit and integration tests for error scenarios
- [ ] Add CI/CD pipeline with health checks
- [ ] Implement advanced logging and monitoring (Prometheus, Grafana)
- [ ] Add database integration with connection pooling
- [ ] Create mobile app version with offline capability
- [ ] Implement real-time notifications for service status
- [ ] Add load balancing and circuit breaker patterns

---

**Made with 💚, FastAPI, and resilient architecture**

*Now with comprehensive error handling for service unavailable scenarios including Bedrock integration fallbacks!*