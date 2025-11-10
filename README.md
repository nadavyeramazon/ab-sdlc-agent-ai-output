# Green Theme Hello World Fullstack Application

![CI Pipeline](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/workflows/CI%20Pipeline/badge.svg?branch=feature/JIRA-777/fullstack-app)

A modern fullstack "Hello World" application featuring a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose. This project demonstrates best practices in web development, containerization, API integration, and responsive UI design.

## 🚀 Features

- **Green-themed React Frontend** with responsive design
- **FastAPI Backend** with RESTful API endpoints
- **Docker Compose** orchestration for seamless local development
- **Hot Module Replacement (HMR)** for rapid development
- **Comprehensive Test Coverage** for both frontend and backend
- **GitHub Actions CI/CD** pipeline
- **CORS Configuration** for frontend-backend communication
- **Error Handling** and loading states
- **Accessibility Features** with ARIA labels and semantic HTML

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker Engine**: 20.0 or higher
- **Docker Compose**: 2.0 or higher
- **Git**: For version control

For local development without Docker:
- **Node.js**: 18.0 or higher (LTS)
- **Python**: 3.11 or higher

## 🏗️ Project Structure

```
.
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Green theme styles
│   │   ├── main.jsx         # React entry point
│   │   ├── App.test.jsx     # Frontend tests
│   │   └── test/
│   │       └── setup.js     # Test configuration
│   ├── index.html           # HTML template
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   ├── Dockerfile           # Production build
│   ├── Dockerfile.dev       # Development build
│   └── nginx.conf           # Nginx configuration
├── backend/                 # FastAPI backend application
│   ├── main.py              # FastAPI application
│   ├── test_main.py         # Backend tests
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD pipeline
├── docker-compose.yml       # Multi-container orchestration
└── README.md                # This file
```

## 🚀 Quick Start

### Running with Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
   cd ab-sdlc-agent-ai-backend
   git checkout feature/JIRA-777/fullstack-app
   ```

2. **Start all services**
   ```bash
   docker-compose up
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Stop the application**
   ```bash
   docker-compose down
   ```

### Running Services Individually

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

## 🧪 Testing

### Backend Tests

```bash
cd backend
pip install -r requirements.txt
pytest test_main.py -v
```

### Frontend Tests

```bash
cd frontend
npm install
npm test
```

### Run All Tests

```bash
# Backend tests
cd backend && pytest test_main.py -v && cd ..

# Frontend tests
cd frontend && npm test -- --run && cd ..
```

## 📡 API Endpoints

### GET /api/hello

Returns a hello message with timestamp.

**Response (200 OK):**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:45.123456Z"
}
```

### GET /health

Health check endpoint for monitoring.

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

### GET /

Root endpoint with API information.

**Response (200 OK):**
```json
{
  "message": "Welcome to Hello World API",
  "docs": "/docs",
  "health": "/health"
}
```

## 🎨 UI Features

- **Green Theme**: Primary (#2ecc71) and Secondary (#27ae60) green colors
- **Responsive Design**: Works on mobile (320px+), tablet, and desktop
- **Loading States**: Spinner animation during API calls
- **Error Handling**: User-friendly error messages
- **Accessibility**: ARIA labels, semantic HTML, keyboard navigation

## 🛠️ Development

### Hot Module Replacement (HMR)

Both frontend and backend support hot reload:

- **Frontend**: Vite HMR updates instantly when you modify `src/` files
- **Backend**: Uvicorn reloads automatically when you modify `main.py`

### Making Changes

1. **Frontend changes**: Edit files in `frontend/src/`
   - Changes appear instantly in the browser
   
2. **Backend changes**: Edit `backend/main.py`
   - Server reloads automatically
   
3. **Styling changes**: Edit `frontend/src/App.css`
   - Styles update without page reload

### Debugging

**View logs:**
```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

**Access container shell:**
```bash
# Backend
docker-compose exec backend sh

# Frontend
docker-compose exec frontend sh
```

## 🐛 Troubleshooting

### Services won't start

1. Check if ports 3000 and 8000 are available:
   ```bash
   lsof -i :3000
   lsof -i :8000
   ```

2. Remove old containers and volumes:
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

### Frontend can't connect to backend

1. Verify backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Check browser console for CORS errors

3. Ensure backend CORS middleware allows `http://localhost:3000`

### Tests failing

1. **Backend tests**:
   ```bash
   cd backend
   pip install -r requirements.txt --upgrade
   pytest test_main.py -v
   ```

2. **Frontend tests**:
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   npm test -- --run
   ```

### Docker build issues

1. Clear Docker cache:
   ```bash
   docker-compose build --no-cache
   ```

2. Remove all containers and images:
   ```bash
   docker-compose down -v --rmi all
   docker-compose up --build
   ```

## 📊 CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow that:

1. **Backend Tests**: Runs pytest with Python 3.11
2. **Frontend Tests**: Runs Vitest with Node.js 18
3. **Docker Builds**: Verifies all Docker images build successfully
4. **Integration Tests**: Tests full stack with Docker Compose
5. **Health Checks**: Validates API endpoints are working

View pipeline status: [GitHub Actions](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions)

## 🔒 Security Notes

This is a development/demo application. For production:

- Add authentication and authorization
- Configure HTTPS/TLS
- Set up environment-specific configurations
- Implement rate limiting
- Add input validation and sanitization
- Configure security headers
- Use secrets management for sensitive data

## 📝 Manual Testing Checklist

- [ ] Page loads at http://localhost:3000
- [ ] "Hello World" heading is visible with green theme
- [ ] Page is responsive (test at 320px, 768px, 1920px)
- [ ] Button "Get Message from Backend" is visible and clickable
- [ ] Clicking button shows loading spinner
- [ ] Backend message displays after successful fetch
- [ ] Timestamp displays in readable format
- [ ] Error message displays when backend is stopped
- [ ] Button can be clicked multiple times
- [ ] No console errors during normal operation
- [ ] GET /api/hello returns 200 with correct JSON
- [ ] GET /health returns {"status": "healthy"}
- [ ] API documentation accessible at http://localhost:8000/docs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

## 👥 Authors

- Repository: [nadavyeramazon/ab-sdlc-agent-ai-backend](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend)
- Branch: feature/JIRA-777/fullstack-app

## 🙏 Acknowledgments

- React team for the amazing frontend framework
- FastAPI team for the high-performance backend framework
- Vite team for the blazingly fast build tool
- Docker team for containerization technology

---

**Status**: ✅ Ready for Development

**Version**: 1.0.0

**Last Updated**: 2024
