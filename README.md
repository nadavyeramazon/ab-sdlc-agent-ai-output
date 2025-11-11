# Green Theme Hello World Fullstack Application

A modern fullstack web application featuring a green-themed React frontend and Python FastAPI backend, orchestrated with Docker Compose.

## 🎯 Features

- **Frontend**: React 18+ with Vite for fast development and HMR (Hot Module Replacement)
- **Backend**: FastAPI with Python 3.11+ for high-performance API endpoints
- **Styling**: Beautiful green-themed UI with responsive design
- **API Integration**: Real-time data fetching from backend to frontend
- **Containerization**: Docker and Docker Compose for easy deployment
- **Error Handling**: Comprehensive error handling and user feedback
- **Testing**: Full test coverage with pytest and React Testing Library
- **CI/CD**: GitHub Actions workflow for automated testing

## 📋 Prerequisites

Before running this application, ensure you have the following installed:

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Node.js**: Version 18+ (for local development)
- **Python**: Version 3.11+ (for local development)

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
   cd ab-sdlc-agent-ai-backend
   git checkout feature/JIRA-777/fullstack-app
   ```

2. **Start all services**
   ```bash
   docker compose up
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Stop all services**
   ```bash
   docker compose down
   ```

### Local Development (Without Docker)

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend**
   ```bash
   python main.py
   ```
   Backend will be available at http://localhost:8000

#### Frontend Setup

1. **Navigate to frontend directory** (in a new terminal)
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```
   Frontend will be available at http://localhost:3000

## 🧪 Running Tests

### Backend Tests

```bash
cd backend
pip install -r requirements.txt
pytest -v
```

Tests include:
- API endpoint functionality
- Response format validation
- CORS configuration
- Performance benchmarks
- Error handling

### Frontend Tests

```bash
cd frontend
npm install
npm test
```

Tests cover:
- Component rendering
- User interactions
- API integration
- Loading states
- Error handling
- Accessibility

## 📁 Project Structure

```
project-root/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── test_main.py         # Backend tests
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container configuration
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Green theme styling
│   │   ├── App.test.jsx     # Frontend tests
│   │   ├── main.jsx         # React entry point
│   │   └── test/
│   │       └── setup.js     # Test configuration
│   ├── index.html           # HTML template
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   └── Dockerfile           # Frontend container configuration
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI workflow
├── docker-compose.yml       # Service orchestration
└── README.md                # This file
```

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
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy"
}
```

## 🎨 User Interface

The frontend features:
- **Green Theme**: Beautiful gradient background using #2ecc71 and #27ae60
- **Responsive Design**: Works seamlessly on mobile, tablet, and desktop
- **Interactive Button**: Fetch messages from backend on demand
- **Loading States**: Visual feedback during API requests
- **Error Handling**: User-friendly error messages
- **Accessibility**: WCAG AA compliant with proper contrast ratios

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: Lightning-fast ASGI server
- **Python 3.11**: Latest Python features and performance improvements
- **pytest**: Comprehensive testing framework

### Frontend
- **React 18**: Latest React with concurrent features
- **Vite**: Next-generation frontend tooling
- **CSS3**: Modern styling with animations and transitions
- **Vitest**: Fast unit testing framework
- **React Testing Library**: User-centric testing utilities

### DevOps
- **Docker**: Container platform
- **Docker Compose**: Multi-container orchestration
- **GitHub Actions**: CI/CD automation
- **Nginx**: Production-ready web server for frontend

## 🔧 Configuration

### Environment Variables

**Backend:**
- `PYTHONUNBUFFERED=1`: Ensures Python output is sent straight to terminal

**Frontend:**
- Backend URL is configured in `App.jsx` (default: http://localhost:8000)

### Port Configuration

- **Frontend**: 3000 (configurable in `vite.config.js` and `docker-compose.yml`)
- **Backend**: 8000 (configurable in `main.py` and `docker-compose.yml`)

## 📊 Performance Metrics

- **API Response Time**: < 100ms for both endpoints
- **Frontend Load Time**: < 2 seconds
- **Time to Interactive (TTI)**: < 3 seconds
- **Service Startup**: < 10 seconds

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Port Already in Use

If you see "port already in use" errors:

```bash
# Find process using the port
lsof -i :3000  # or :8000
# Kill the process
kill -9 <PID>
```

### Docker Issues

```bash
# Clean up Docker resources
docker compose down -v
docker system prune -f
```

### Frontend Can't Connect to Backend

- Ensure backend is running on port 8000
- Check CORS configuration in `backend/main.py`
- Verify network connectivity in Docker Compose

## 📞 Support

For issues and questions:
- Create an issue in the GitHub repository
- Check existing issues for solutions
- Review the troubleshooting section

## ✨ Acknowledgments

- React team for the amazing framework
- FastAPI community for the excellent web framework
- Docker for simplifying deployment

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production Ready
