# Green Theme Hello World - Fullstack Application

<div align="center">

![Green Theme](https://img.shields.io/badge/Theme-Green-2ecc71?style=for-the-badge)
![React](https://img.shields.io/badge/React-18.2.0-61dafb?style=for-the-badge&logo=react)
![Vite](https://img.shields.io/badge/Vite-5.0.8-646cff?style=for-the-badge&logo=vite)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ed?style=for-the-badge&logo=docker)
![Tests](https://img.shields.io/badge/Coverage-80%25+-success?style=for-the-badge)

A modern, responsive fullstack application with a beautiful green theme, featuring React frontend with Vite and backend API integration.

[Features](#features) • [Quick Start](#quick-start) • [Architecture](#architecture) • [Development](#development) • [Testing](#testing) • [Deployment](#deployment)

</div>

---

## ✨ Features

### Frontend
- ✅ **React 18+** with functional components and hooks
- ✅ **Vite** for lightning-fast development with HMR
- ✅ **Beautiful Green Theme** with smooth animations
- ✅ **Fully Responsive** design for all screen sizes
- ✅ **Accessibility Compliant** (WCAG 2.1 AA)
- ✅ **Comprehensive Testing** with React Testing Library (80%+ coverage)
- ✅ **Error Boundary** for graceful error handling
- ✅ **Loading States** with spinners and feedback

### Backend
- ✅ **RESTful API** with clean endpoints
- ✅ **CORS Enabled** for cross-origin requests
- ✅ **Health Check** endpoint for monitoring
- ✅ **Error Handling** with proper HTTP status codes
- ✅ **Docker Ready** for containerization

### DevOps
- ✅ **Docker Compose** for one-command deployment
- ✅ **Multi-stage Builds** for optimized images
- ✅ **Health Checks** for both services
- ✅ **Production Ready** with nginx

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
git checkout feature/JIRA-777/fullstack-app

# Start the entire stack
docker-compose up --build

# Access the application
# Frontend: http://localhost
# Backend API: http://localhost:8000/api/hello
```

### Option 2: Local Development

#### Backend Setup
```bash
cd backend
npm install
npm start
# Backend runs on http://localhost:8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
# Frontend runs on http://localhost:3000
```

## 🏛️ Architecture

```
┌────────────────────────────────┐
│         User Browser          │
└─────────────┬───────────────────┘
               │
               │ HTTP/HTTPS
               │
               │
┌─────────────┴───────────────────┐
│    nginx (Frontend)          │
│    - Serves React SPA        │
│    - Proxies /api to backend │
│    - Port 80                 │
└─────────────┬───────────────────┘
               │
               │ /api/*
               │
┌─────────────┴───────────────────┐
│    Backend API               │
│    - Node.js / Python        │
│    - RESTful endpoints       │
│    - Port 8000               │
└────────────────────────────────┘
```

### Project Structure

```
.
├── frontend/               # React + Vite application
│   ├── src/
│   │   ├── App.jsx         # Main component with backend integration
│   │   ├── App.css         # Green theme styling
│   │   ├── main.jsx        # React entry point
│   │   ├── components/     # Reusable components
│   │   └── __tests__/      # React Testing Library tests
│   ├── Dockerfile          # Multi-stage build with nginx
│   ├── nginx.conf          # nginx server configuration
│   ├── package.json        # Dependencies and scripts
│   └── vite.config.js      # Vite configuration
│
├── backend/                # Backend API (Node.js/Python)
│   ├── server.js           # API server
│   ├── Dockerfile          # Backend container
│   └── package.json        # Backend dependencies
│
├── docker-compose.yml      # Full stack orchestration
└── README.md               # This file
```

## 🛠️ Development

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start dev server with HMR
npm run dev

# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Generate coverage report
npm run test:coverage

# Build for production
npm run build

# Preview production build
npm run preview
```

### Environment Variables

Create `frontend/.env` file:

```env
VITE_API_URL=http://localhost:8000
```

### Color Palette

| Color      | Hex       | Usage                |
|------------|-----------|----------------------|
| Primary    | `#2ecc71` | Main theme color     |
| Secondary  | `#27ae60` | Hover states         |
| Accent     | `#1e8449` | Dark elements        |
| Background | Gradient  | Page background      |

## 🧪 Testing

### Frontend Tests

The application includes comprehensive tests covering:

- **Initial Rendering**: All UI elements display correctly
- **User Interactions**: Button clicks, loading states
- **API Integration**: Success and error scenarios
- **Accessibility**: ARIA labels, keyboard navigation
- **State Management**: Multiple API calls, state transitions

```bash
cd frontend

# Run all tests
npm test

# Coverage report
npm run test:coverage

# Expected output:
# ✓ Lines: 80%+
# ✓ Functions: 80%+
# ✓ Branches: 80%+
# ✓ Statements: 80%+
```

## 🚀 Deployment

### Docker Compose (Production)

```bash
# Build and start all services
docker-compose up -d --build

# Check service health
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Docker Containers

#### Frontend
```bash
cd frontend
docker build -t green-hello-frontend .
docker run -p 80:80 green-hello-frontend
```

#### Backend
```bash
cd backend
docker build -t green-hello-backend .
docker run -p 8000:8000 green-hello-backend
```

### Health Checks

- **Frontend**: `http://localhost/`
- **Backend**: `http://localhost:8000/health`
- **API Endpoint**: `http://localhost:8000/api/hello`

## 📊 API Documentation

### GET /api/hello

Returns a greeting message from the backend.

**Response (200 OK)**:
```json
{
  "message": "Hello from the backend!"
}
```

**Error Response (500)**:
```json
{
  "error": "Internal server error"
}
```

## ♈ Accessibility

This application follows WCAG 2.1 AA guidelines:

- ✅ Semantic HTML
- ✅ ARIA labels and live regions
- ✅ Keyboard navigation
- ✅ Focus indicators
- ✅ Screen reader support
- ✅ Reduced motion support
- ✅ High contrast colors

## 📝 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 🐛 Troubleshooting

### Frontend not connecting to backend

1. Check backend is running: `curl http://localhost:8000/api/hello`
2. Verify CORS settings in backend
3. Check `VITE_API_URL` environment variable
4. Review browser console for network errors

### Docker issues

```bash
# Clean up Docker resources
docker-compose down -v
docker system prune -a

# Rebuild from scratch
docker-compose up --build --force-recreate
```

### Port conflicts

```bash
# Change ports in docker-compose.yml or use:
FRONTEND_PORT=8080 BACKEND_PORT=8001 docker-compose up
```

## 📝 License

See LICENSE file in repository root.

## 👥 Contributing

Contributions are welcome! Please ensure:

1. Tests pass with 80%+ coverage
2. Code follows existing patterns
3. Accessibility standards maintained
4. Documentation updated

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

---

<div align="center">

**Built with ❤️ using React, Vite, and a beautiful green theme**

[Documentation](./frontend/README.md) • [Report Bug](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/issues) • [Request Feature](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/issues)

</div>
