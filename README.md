# Green Theme Hello World Fullstack Application

🌱 A modern, responsive fullstack web application featuring a beautiful green theme, built with React 18, Vite, and FastAPI.

## 🎆 Features

### Frontend (React 18 + Vite)
- 🌱 **Green Theme**: Beautiful green color palette (#2ecc71, #27ae60, #1e8449)
- ⚡ **Vite**: Lightning-fast development with Hot Module Replacement (HMR)
- 📱 **Responsive Design**: Mobile-first approach with breakpoints for all devices
- ♿ **Accessibility**: WCAG 2.1 AA compliant with semantic HTML and ARIA labels
- 🔄 **API Integration**: Seamless backend communication with loading states
- 🧪 **Testing**: Comprehensive test suite with React Testing Library and Vitest
- 🎨 **Modern CSS**: Custom properties, animations, and responsive utilities
- 🚀 **Performance**: Optimized builds with code splitting and tree shaking

### Backend (FastAPI)
- 🚀 **FastAPI**: High-performance Python web framework
- 📊 **API Documentation**: Auto-generated OpenAPI/Swagger docs
- 🔒 **CORS Support**: Configured for cross-origin requests
- 👥 **Health Checks**: Built-in health monitoring endpoints
- 📝 **Logging**: Structured logging for debugging and monitoring
- 🧪 **Testing**: Unit tests with pytest and httpx

### DevOps & Deployment
- 🐳 **Docker**: Full containerization with multi-stage builds
- 🔧 **Docker Compose**: Easy orchestration for development and production
- 🛠️ **Development Mode**: Hot reload for both frontend and backend
- 🏭 **Production Ready**: Optimized builds with Nginx for static serving
- 📊 **Health Monitoring**: Container health checks and restart policies

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ and npm (for local development)
- Python 3.11+ (for local development)

### Option 1: Docker Compose (Recommended)

#### Development Mode
```bash
# Clone the repository
git clone <repository-url>
cd ab-sdlc-agent-ai-backend

# Start development environment with hot reload
docker-compose --profile dev up --build

# Or run in detached mode
docker-compose --profile dev up -d --build
```

#### Production Mode
```bash
# Start production environment
docker-compose --profile prod up --build

# Or run in detached mode
docker-compose --profile prod up -d --build
```

### Option 2: Local Development

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```

## 🗺️ Application URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## 📝 API Endpoints

### Core Endpoints
- `GET /` - API information and available endpoints
- `GET /health` - Health check endpoint
- `GET /api/hello` - Hello World message
- `GET /api/hello/{name}` - Personalized greeting
- `GET /docs` - Interactive API documentation

### Example Responses

#### Hello World
```json
{
  "message": "Hello World! 🌱 Welcome to our beautiful green-themed fullstack application! Built with React, Vite, and FastAPI. 🚀",
  "status": "success",
  "theme": "green"
}
```

#### Health Check
```json
{
  "status": "healthy",
  "service": "green-hello-world-api",
  "version": "1.0.0",
  "theme": "green"
}
```

## 📊 Testing

### Frontend Tests
```bash
cd frontend

# Run tests
npm test

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage

# Run linting
npm run lint
```

### Backend Tests
```bash
cd backend

# Run tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html
```

## 📜 Project Structure

```
┌── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── test/            # Test utilities
│   │   ├── App.jsx          # Root component
│   │   ├── App.css          # Global styles
│   │   └── main.jsx         # Entry point
│   ├── public/              # Static assets
│   ├── package.json         # Dependencies and scripts
│   ├── vite.config.js       # Vite configuration
│   ├── Dockerfile           # Production Docker image
│   └── Dockerfile.dev       # Development Docker image
├── backend/                # FastAPI backend application
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Docker image
│   └── tests/               # Backend tests
├── docker-compose.yml      # Container orchestration
└── README.md               # This file
```

## 🎈 Key Technologies

### Frontend Stack
- **React 18**: Latest React with concurrent features
- **Vite**: Next-generation frontend tooling
- **CSS3**: Modern CSS with custom properties and Grid/Flexbox
- **React Testing Library**: Component testing utilities
- **Vitest**: Fast unit test runner
- **ESLint**: Code linting and formatting

### Backend Stack
- **FastAPI**: Modern, fast Python web framework
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for FastAPI
- **pytest**: Python testing framework
- **httpx**: HTTP client for testing

### DevOps Stack
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Web server for production frontend
- **GitHub Actions**: CI/CD (if configured)

## 🎨 Design System

### Color Palette
- **Primary**: #2ecc71 (Emerald Green)
- **Secondary**: #27ae60 (Nephritis Green)
- **Accent**: #1e8449 (Forest Green)
- **Light**: #a9dfbf (Light Green)
- **Background**: #f8fff9 (Mint Cream)

### Typography
- **Font Family**: System fonts (-apple-system, BlinkMacSystemFont, etc.)
- **Responsive Typography**: Fluid scaling with clamp()
- **Accessibility**: High contrast ratios and scalable text

### Spacing Scale
- Based on 0.25rem (4px) increments
- Consistent spacing throughout the application
- Responsive adjustments for different screen sizes

## ♿ Accessibility Features

- **Semantic HTML**: Proper heading hierarchy and landmarks
- **ARIA Labels**: Comprehensive labeling for screen readers
- **Keyboard Navigation**: Full keyboard accessibility
- **Focus Management**: Visible focus indicators
- **High Contrast**: Support for high contrast mode
- **Reduced Motion**: Respects user motion preferences
- **Screen Reader**: Optimized for assistive technologies

## 📊 Performance Optimizations

### Frontend
- **Code Splitting**: Automatic route-based splitting
- **Tree Shaking**: Eliminate dead code
- **Asset Optimization**: Minified CSS and JS
- **Caching**: Efficient browser caching strategies
- **Bundle Analysis**: Size monitoring and optimization

### Backend
- **Async Operations**: Non-blocking request handling
- **Response Caching**: Efficient API response caching
- **Connection Pooling**: Optimized database connections (if applicable)
- **Request Validation**: Early request validation and filtering

## 🚪 Environment Variables

### Frontend
- `NODE_ENV`: Environment mode (development/production)
- `VITE_API_URL`: Backend API URL (for production builds)

### Backend
- `ENVIRONMENT`: Application environment
- `PYTHONUNBUFFERED`: Python output buffering

## 🚀 Deployment

### Production Deployment
1. Set environment variables
2. Build containers: `docker-compose --profile prod build`
3. Start services: `docker-compose --profile prod up -d`
4. Monitor health: `docker-compose ps`

### Scaling
```bash
# Scale backend instances
docker-compose --profile prod up -d --scale backend=3

# Scale with load balancer (requires configuration)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 🐛 Troubleshooting

### Common Issues

#### Frontend not connecting to backend
1. Check if backend is running: `curl http://localhost:8000/health`
2. Verify CORS configuration in backend
3. Check network connectivity between containers

#### Hot reload not working
1. Ensure volume mounts are correct in docker-compose.yml
2. Check file permissions on mounted directories
3. Verify Vite configuration for HMR

#### Build failures
1. Clear Docker cache: `docker system prune -a`
2. Rebuild without cache: `docker-compose build --no-cache`
3. Check dependency versions and compatibility

### Logs and Debugging
```bash
# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Execute commands in running containers
docker-compose exec backend bash
docker-compose exec frontend sh
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes following the existing code style
4. Add tests for new functionality
5. Ensure all tests pass: `npm test` and `pytest`
6. Run linting: `npm run lint`
7. Commit your changes: `git commit -m 'Add amazing feature'`
8. Push to the branch: `git push origin feature/amazing-feature`
9. Open a Pull Request

### Code Style Guidelines
- Follow existing naming conventions
- Add JSDoc comments for functions
- Maintain test coverage above 80%
- Use semantic commit messages
- Ensure accessibility compliance

## 📜 Documentation

- **API Documentation**: Available at `/docs` when backend is running
- **Component Documentation**: JSDoc comments in component files
- **Architecture Decisions**: Documented in code comments
- **Testing Strategy**: Detailed in test files

## 📌 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚀 Future Enhancements

- [ ] User authentication and authorization
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Real-time features with WebSockets
- [ ] Internationalization (i18n)
- [ ] Progressive Web App (PWA) features
- [ ] Advanced caching strategies
- [ ] Monitoring and observability
- [ ] CI/CD pipeline integration
- [ ] Load balancing and scaling
- [ ] Security hardening

---

📞 **Support**: For questions or issues, please open a GitHub issue or contact the development team.

🎆 **Acknowledgments**: Built with love using modern web technologies and best practices.

---

**Happy coding!** 🚀🌱