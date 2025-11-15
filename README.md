# Green Theme Hello World Fullstack Application

[![CI Pipeline](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml/badge.svg?branch=feature/JIRA-777/fullstack-app)](https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend/actions/workflows/ci.yml)

A simple fullstack "Hello World" application demonstrating frontend-backend integration with a beautiful green theme. This project features a React frontend that displays static content and fetches dynamic data from a Python FastAPI backend, all orchestrated with Docker Compose.

## 🌟 Features

- **Green-themed React Frontend**: Beautiful, responsive UI with emerald green (#2ecc71) theme
- **FastAPI Backend**: Fast, modern Python API with automatic documentation
- **Docker Compose Orchestration**: Single command to run the entire stack
- **Hot Module Replacement**: Fast development iteration with Vite HMR
- **Environment Variable Configuration**: Flexible API URL configuration for different environments
- **Comprehensive Testing**: Unit tests, integration tests, and E2E tests with Cypress
- **CI/CD Pipeline**: Automated testing with GitHub Actions

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Docker Compose                       │
│                                                          │
│  ┌────────────────────┐      ┌──────────────────────┐  │
│  │  Frontend          │      │  Backend             │  │
│  │  React + Vite      │◄────►│  FastAPI + Python    │  │
│  │  Port: 3000        │      │  Port: 8000          │  │
│  └────────────────────┘      └──────────────────────┘  │
│          ▲                            ▲                 │
│          │                            │                 │
└──────────┼────────────────────────────┼─────────────────┘
           │                            │
           │                            │
      ┌────▼────┐                  ┌───▼────┐
      │ Browser │                  │  API   │
      │  User   │                  │ Client │
      └─────────┘                  └────────┘
```

## 📋 Prerequisites

Before running this application, ensure you have the following installed:

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher

### Verify Installation

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker compose version
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
git checkout feature/JIRA-777/fullstack-app
```

### 2. Start the Application

```bash
# Start both frontend and backend services
docker compose up
```

This command will:
- Build Docker images for frontend and backend
- Start both services
- Display logs from both services in your terminal
- Enable hot module replacement for development
- Configure the frontend to communicate with backend via Docker network

### 3. Access the Application

- **Frontend**: Open your browser to [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)
- **Alternative API Docs**: [http://localhost:8000/redoc](http://localhost:8000/redoc) (ReDoc)

### 4. Stop the Application

```bash
# Stop services (press Ctrl+C in terminal, then)
docker compose down

# Or stop and remove volumes
docker compose down -v
```

## ⚙️ Configuration

### Environment Variables

The application uses environment variables for configuration. The key variable is:

- **`VITE_API_BASE_URL`**: The base URL for the backend API

#### Docker Environment (Default)

When running with Docker Compose, the frontend automatically uses the internal Docker network:

```yaml
VITE_API_BASE_URL=http://backend:8000
```

This is configured in `docker-compose.yml` and allows containers to communicate via Docker's internal DNS.

#### Local Development (Without Docker)

If running the frontend locally (outside Docker), create a `.env` file in the `frontend/` directory:

```bash
VITE_API_BASE_URL=http://localhost:8000
```

Then start the services:

```bash
# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

#### Production Environment

For production deployments, set the environment variable to your production API URL:

```bash
VITE_API_BASE_URL=https://api.yourdomain.com
```

See `.env.example` for a template of all available environment variables.

## 🎯 Using the Application

1. **View the Static Content**: When you open [http://localhost:3000](http://localhost:3000), you'll see:
   - A large "Hello World" heading in emerald green
   - A green-themed button labeled "Get Message from Backend"

2. **Fetch Dynamic Data**: 
   - Click the "Get Message from Backend" button
   - Watch the loading indicator appear
   - See the message "Hello World from Backend!" with a timestamp

3. **Test Multiple Requests**:
   - Click the button multiple times to fetch fresh data
   - Each request will return an updated timestamp

4. **Test Error Handling**:
   - Stop the backend service: `docker compose stop backend`
   - Click the button to see the error message
   - Restart backend: `docker compose start backend`

## 🧪 Testing

### Run Backend Tests

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run tests
pytest test_main.py -v
```

### Run Frontend Tests

```bash
# Install dependencies
cd frontend
npm install

# Run tests
npm test
```

### Run E2E Tests

```bash
# Start the application first
docker compose up -d

# Install Cypress
npm install cypress

# Run E2E tests
npx cypress run

# Or open Cypress UI
npx cypress open
```

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── test_main.py         # Backend tests
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend Docker configuration
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Green theme styling
│   │   ├── App.test.jsx     # Frontend tests
│   │   ├── main.jsx         # React entry point
│   │   └── test/
│   │       └── setup.js     # Test configuration
│   ├── index.html           # HTML template
│   ├── package.json         # Node.js dependencies
│   ├── vite.config.js       # Vite configuration
│   ├── Dockerfile           # Production frontend Docker config
│   ├── Dockerfile.dev       # Development frontend Docker config
│   └── nginx.conf           # Nginx configuration
│
├── cypress/
│   ├── e2e/
│   │   └── app.cy.js        # E2E tests
│   └── support/
│       ├── e2e.js           # Cypress support
│       └── commands.js      # Custom commands
│
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI pipeline
│
├── docker-compose.yml       # Docker Compose orchestration
├── cypress.config.js        # Cypress configuration
├── .env.example            # Environment variable template
└── README.md               # This file
```

## 🔧 Development

### Backend Development

The backend uses FastAPI with hot reload enabled. Any changes to `backend/main.py` will automatically restart the server.

```bash
# View backend logs
docker compose logs -f backend

# Access backend container
docker compose exec backend sh
```

### Frontend Development

The frontend uses Vite with Hot Module Replacement. Changes to React files will automatically update in the browser.

```bash
# View frontend logs
docker compose logs -f frontend

# Access frontend container
docker compose exec frontend sh
```

### Making Code Changes

1. Edit files in `backend/` or `frontend/`
2. Changes are automatically reflected (thanks to volume mounts)
3. No need to rebuild Docker images during development

## 🌐 API Endpoints

### GET /api/hello

Returns a hello world message with timestamp.

**Response:**
```json
{
  "message": "Hello World from Backend!",
  "timestamp": "2024-01-15T10:30:00.000000Z"
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

## 🎨 Color Scheme

- **Primary Green**: #2ecc71 (Emerald)
- **Secondary Green**: #27ae60 (Nephritis)
- **Background**: Linear gradient from #e8f8f5 to #d5f4e6
- **Text**: Various shades optimized for readability

## 🔍 Troubleshooting

### Port Already in Use

```bash
# Check what's using port 3000
lsof -i :3000

# Check what's using port 8000
lsof -i :8000

# Kill the process or change ports in docker-compose.yml
```

### Container Won't Start

```bash
# View detailed logs
docker compose logs

# Rebuild images
docker compose build --no-cache
docker compose up
```

### Cannot Connect to Backend

1. Verify backend is running: `curl http://localhost:8000/health`
2. Check CORS configuration in `backend/main.py`
3. Verify Docker network is working: `docker network ls`
4. Check that `VITE_API_BASE_URL` is set correctly for your environment

### Frontend Shows Blank Page

1. Check browser console for errors (F12)
2. Verify frontend container is running: `docker compose ps`
3. Check frontend logs: `docker compose logs frontend`
4. Ensure environment variables are properly configured

### API Connection Issues in Docker

If the frontend can't connect to the backend in Docker:

1. Verify both containers are on the same network: `docker network inspect ab-sdlc-agent-ai-backend_app-network`
2. Check that `VITE_API_BASE_URL=http://backend:8000` in docker-compose.yml
3. Rebuild the frontend container: `docker compose build frontend && docker compose up frontend`

## 📊 CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow that runs:

- ✅ Backend unit tests (pytest)
- ✅ Frontend unit tests (Vitest)
- ✅ Docker image builds
- ✅ E2E integration tests (Cypress)
- ✅ Code quality checks

The CI pipeline runs on:
- Push to `feature/JIRA-777/fullstack-app`
- Pull requests to `main`

## 🤝 Contributing

This is a demonstration project. For improvements or issues:

1. Create a new branch from `feature/JIRA-777/fullstack-app`
2. Make your changes
3. Run tests locally
4. Submit a pull request

## 📝 License

See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend powered by [React](https://react.dev/) and [Vite](https://vitejs.dev/)
- Tested with [pytest](https://pytest.org/), [Vitest](https://vitest.dev/), and [Cypress](https://www.cypress.io/)

---

**Status**: ✅ Ready for Development

**Version**: 1.0.0

**Last Updated**: 2024
