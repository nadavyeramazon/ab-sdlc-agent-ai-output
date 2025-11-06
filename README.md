# Green Greeting Full-Stack Application

A modern, secure full-stack greeting application with a green-themed UI, built with FastAPI backend and vanilla JavaScript frontend.

## 🌟 Features

- **Green-themed UI**: Beautiful, responsive design with nature-inspired green color scheme
- **Secure Input Validation**: Comprehensive client and server-side validation
- **Time-based Greetings**: Personalized greetings based on time of day
- **Comprehensive Testing**: Full test coverage for both frontend and backend
- **Docker Support**: Easy deployment with Docker Compose
- **Production Ready**: Security headers, rate limiting, and production configurations
- **CI/CD Pipeline**: Automated testing and security scanning

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)

### Running with Docker Compose

```bash
# Clone the repository
git clone <repository-url>
cd ab-sdlc-agent-ai-backend

# Start the application
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🧪 Testing

### Backend Tests

```bash
cd backend
pip install -r requirements.txt
pytest test_main.py -v --cov=main
```

### Frontend Tests

```bash
cd frontend
npm install
npm test
# For coverage report
npm run test:coverage
```

### Integration Tests

```bash
# Start services
docker-compose up -d

# Test backend health
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000

# Test greeting API
curl -X POST http://localhost:8000/greet \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User"}'
```

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────┐
│                      Frontend (Port 3000)                      │
│  - Vanilla JavaScript with green-themed CSS                  │
│  - Input validation and sanitization                         │
│  - Responsive design with loading states                     │
├────────────────────────────────────────────────────────┤
│                      Backend (Port 8000)                       │
│  - FastAPI with Pydantic validation                          │
│  - Security middleware and input sanitization               │
│  - Time-based greeting logic                                 │
│  - Comprehensive error handling                              │
└────────────────────────────────────────────────────────┘
```

## 🔒 Security Features

### Input Validation
- Client-side validation with regex patterns
- Server-side Pydantic model validation
- HTML escaping to prevent XSS
- Length limitations and character restrictions

### Security Headers
- X-Frame-Options: SAMEORIGIN
- X-XSS-Protection: 1; mode=block
- X-Content-Type-Options: nosniff
- Content-Security-Policy

### Rate Limiting
- API endpoints: 10 requests/second
- Web endpoints: 30 requests/second

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── test_main.py         # Backend tests
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Backend container
│   └── .gitignore
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── styles.css           # Green-themed CSS
│   ├── script.js            # Frontend JavaScript
│   ├── script.test.js       # Frontend tests
│   ├── jest.setup.js        # Jest configuration
│   ├── server.js            # Express server
│   ├── package.json         # Node.js dependencies
│   ├── Dockerfile           # Frontend container
│   └── .gitignore
├── .github/workflows/
│   └── test.yml             # CI/CD pipeline
├── docker-compose.yml        # Development setup
├── docker-compose.prod.yml   # Production setup
├── nginx.conf               # Nginx configuration
└── README.md
```

## 🛠️ API Endpoints

### `GET /`
Root endpoint with API information

### `GET /health`
Health check endpoint

### `POST /greet`
**Request Body:**
```json
{
  "name": "John Doe"
}
```

**Response:**
```json
{
  "message": "Good morning, John Doe! Welcome to our green-themed greeting service! 🌿",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "name": "John Doe"
}
```

### `GET /docs`
Interactive API documentation (Swagger UI)

## 🧪 Test Coverage

### Backend Tests
- ✅ API endpoint functionality
- ✅ Input validation and sanitization
- ✅ Error handling
- ✅ Security features
- ✅ Time-based greeting logic
- ✅ Response structure validation

### Frontend Tests
- ✅ DOM manipulation
- ✅ Form validation
- ✅ API communication
- ✅ Error state handling
- ✅ Security (XSS prevention)
- ✅ Loading states
- ✅ Integration scenarios

## 🚀 Production Deployment

### Using Production Docker Compose

```bash
# Build and start production services
docker-compose -f docker-compose.prod.yml up --build -d
```

### Environment Variables

**Backend:**
- `ENVIRONMENT`: production/development
- `API_KEY_REQUIRED`: Enable API key authentication
- `CORS_ORIGINS`: Allowed CORS origins
- `LOG_LEVEL`: Logging level

**Frontend:**
- `NODE_ENV`: production/development
- `API_URL`: Backend API URL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Development Setup

```bash
# Backend development
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend development
cd frontend
npm install
npm start
```

## 📊 Monitoring and Logging

- Health check endpoints for monitoring
- Structured logging with timestamps
- Error tracking and reporting
- Performance metrics collection

## 🔧 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure backend CORS settings match frontend URL
2. **Connection Refused**: Check if services are running on correct ports
3. **Validation Errors**: Review input format and validation rules

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
docker-compose up
```

## 📝 License

MIT License - see LICENSE file for details

## 🙋‍♀️ Support

For issues and questions, please open a GitHub issue or contact the development team.

---

**Built with 💚 by the Development Team**