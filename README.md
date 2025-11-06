# 🌿 Green Greeter Application 🌱

A beautiful, eco-friendly web application that greets users with a green-themed interface. Built with FastAPI backend and vanilla JavaScript frontend, containerized with Docker.

## 🎆 Features

- **Green-themed UI**: Beautiful, responsive interface with nature-inspired design
- **FastAPI Backend**: Fast, modern Python web API with automatic documentation
- **Vanilla JavaScript Frontend**: Clean, dependency-free frontend with animations
- **Docker Support**: Full containerization with Docker Compose
- **Comprehensive Testing**: Backend tests with pytest, frontend tests with Jest
- **Health Checks**: Built-in health monitoring for both services
- **Environment Configuration**: Separate configs for development and production
- **CORS Security**: Configurable CORS settings for different environments

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Pytest**: Testing framework

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **Vanilla JavaScript**: No frameworks, pure JS
- **Jest**: JavaScript testing framework
- **Nginx**: Web server for production

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-service orchestration
- **Health Checks**: Service monitoring

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Node.js (for running frontend tests locally)
- Python 3.11+ (for running backend tests locally)

### Running with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd green-greeter
   ```

2. **Start the application**
   ```bash
   # Production mode
   docker-compose up -d
   
   # Development mode (with hot reload)
   docker-compose -f docker-compose.dev.yml up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Stop the application**
   ```bash
   docker-compose down
   ```

### Local Development

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=app
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies (for testing)
npm install

# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Serve files (simple HTTP server)
python -m http.server 3000
```

## 🧪 Testing

### Backend Tests
The backend includes comprehensive tests covering:
- API endpoints functionality
- Input validation
- Error handling
- Health checks
- CORS configuration
- Edge cases (empty names, special characters, long names)

```bash
# Run all tests
cd backend
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app --cov-report=html
```

### Frontend Tests
The frontend tests cover:
- DOM manipulation
- API integration
- Error handling
- User interactions
- Environment configuration
- Input validation

```bash
# Run all tests
cd frontend
npm test

# Run in watch mode
npm run test:watch

# Run with coverage
npm run test:coverage
```

### Running Tests in Docker
```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests (requires Node.js in container)
docker-compose exec frontend npm test
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
ENVIRONMENT=development
API_BASE_URL=http://localhost:8000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
BACKEND_PORT=8000
FRONTEND_PORT=8080
```

### CORS Configuration

- **Development**: Allows all origins for easier testing
- **Production**: Restricted to specific domains for security

### API URL Configuration

The frontend automatically detects the environment:
- **Docker**: Uses `http://backend:8000`
- **Development**: Uses `http://localhost:8000`
- **Custom**: Set via `API_BASE_URL` environment variable

## 🌍 API Documentation

### Endpoints

#### `GET /`
- **Description**: Welcome message
- **Response**: `{"message": "Welcome to the Green Greeter API!"}`

#### `POST /greet`
- **Description**: Greet a user
- **Request Body**: `{"name": "string"}`
- **Response**: `{"greeting": "string", "timestamp": "string"}`
- **Features**:
  - Handles empty names (defaults to "Anonymous")
  - Strips whitespace
  - Supports Unicode characters
  - Returns ISO timestamp

#### `GET /health`
- **Description**: Health check endpoint
- **Response**: `{"status": "healthy"}`

### Interactive Documentation
Visit http://localhost:8000/docs for Swagger UI documentation.

## 📊 Health Monitoring

Both services include health checks:

- **Backend**: `GET /health` endpoint
- **Frontend**: Nginx status check
- **Docker**: Automatic health monitoring with retries

```bash
# Check service health
docker-compose ps

# View health check logs
docker-compose logs backend
docker-compose logs frontend
```

## 🔒 Security Features

- **CORS Protection**: Environment-specific CORS configuration
- **Input Validation**: Pydantic models for request validation
- **Error Handling**: Graceful error responses without exposing internals
- **Health Checks**: Monitor service availability
- **Container Security**: Minimal Docker images with security updates

## 🌍 Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 📝 Project Structure

```
.
├── backend/
│   ├── app.py              # FastAPI application
│   ├── test_app.py         # Backend tests
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── styles.css          # Green-themed styles
│   ├── script.js           # Frontend JavaScript
│   ├── package.json        # NPM configuration
│   ├── test-setup.js       # Jest setup
│   ├── __tests__/
│   │   └── script.test.js  # Frontend tests
│   ├── nginx.conf          # Nginx configuration
│   └── Dockerfile          # Frontend container
├── docker-compose.yml      # Production compose
├── docker-compose.dev.yml  # Development compose
├── .env.example            # Environment template
└── README.md               # This file
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Change ports in docker-compose.yml or stop conflicting services
   docker-compose down
   sudo lsof -i :8000
   sudo lsof -i :8080
   ```

2. **CORS errors**
   - Check `ALLOWED_ORIGINS` in backend configuration
   - Verify `API_BASE_URL` in frontend

3. **Health check failures**
   ```bash
   # Check service logs
   docker-compose logs backend
   docker-compose logs frontend
   
   # Manually test health endpoints
   curl http://localhost:8000/health
   curl http://localhost:8080
   ```

4. **Tests failing**
   ```bash
   # Backend: Check Python version and dependencies
   python --version
   pip install -r backend/requirements.txt
   
   # Frontend: Check Node.js version and dependencies
   node --version
   npm install
   ```

### Debug Mode

```bash
# Run in development mode with logs
docker-compose -f docker-compose.dev.yml up

# View real-time logs
docker-compose logs -f
```

## 🕰️ Performance

- **Backend**: Sub-100ms response times for greeting endpoints
- **Frontend**: Lightweight vanilla JS, no framework overhead
- **Docker**: Optimized images with multi-stage builds
- **Caching**: Nginx static file caching for frontend assets

## 🎆 Future Enhancements

- [ ] User authentication and personalization
- [ ] Greeting history and favorites
- [ ] Multiple language support
- [ ] Database integration for persistent greetings
- [ ] Rate limiting and API quotas
- [ ] WebSocket support for real-time greetings
- [ ] Progressive Web App (PWA) features
- [ ] Docker multi-stage builds optimization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines

- Write tests for new features
- Follow existing code style
- Update documentation
- Ensure Docker builds succeed
- Verify health checks pass

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

🌿 **Happy Greeting!** 🌱
