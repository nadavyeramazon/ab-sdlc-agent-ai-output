# Green Greeting Application

A full-stack web application with a green-themed UI that greets users by name. The application demonstrates frontend-backend integration using Docker Compose.

## 🌿 Features

- **Frontend**: Beautiful green-themed UI built with HTML, CSS, and JavaScript
- **Backend**: FastAPI application that provides a greeting API
- **Containerization**: Docker and Docker Compose for easy deployment
- **CORS Support**: Configured for seamless frontend-backend communication

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3 (Custom green theme)
- Vanilla JavaScript
- Nginx (Alpine)

### Backend
- Python 3.11
- FastAPI
- Uvicorn
- Pydantic

### DevOps
- Docker
- Docker Compose

## 🚀 Getting Started

### Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)

### Installation & Running

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ab-sdlc-agent-ai-backend
   ```

2. **Start the application**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Stop the application**:
   ```bash
   docker-compose down
   ```

## 📝 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Backend container configuration
│   └── .dockerignore        # Docker ignore patterns
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── styles.css           # Green-themed CSS styles
│   ├── script.js            # JavaScript functionality
│   ├── nginx.conf           # Nginx configuration
│   └── Dockerfile           # Frontend container configuration
├── docker-compose.yml       # Docker Compose configuration
└── README.md                # This file
```

## 📡 API Endpoints

### Backend API

- **GET /** - Welcome message
- **POST /greet** - Get a personalized greeting
  - Request Body: `{"name": "Your Name"}`
  - Response: `{"message": "Hello, Your Name! Welcome to our green-themed application!"}`
- **GET /health** - Health check endpoint

## 🎨 Green Theme

The application features a beautiful green color palette:
- Primary Green: `#2d7a3e`
- Secondary Green: `#4caf50`
- Light Green: `#81c784`
- Very Light Green: `#c8e6c9`
- Dark Green: `#1b5e20`

## 🔧 Development

### Running Backend Locally

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Running Frontend Locally

Simply open `frontend/index.html` in a web browser, or use a local server:

```bash
cd frontend
python -m http.server 8080
```

## 📝 Environment Variables

The application uses the following default configurations:
- Backend Port: `8000`
- Frontend Port: `80`
- API Base URL: `http://localhost:8000` (configured in `frontend/script.js`)

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📜 License

See LICENSE file for details.

## ✨ Features Highlight

- ✅ Responsive design for mobile and desktop
- ✅ Error handling and user feedback
- ✅ Health check endpoints
- ✅ CORS configuration
- ✅ Docker multi-container setup
- ✅ Beautiful green-themed UI with animations
- ✅ Input validation
- ✅ RESTful API design

## 🐛 Troubleshooting

**Issue**: Frontend cannot connect to backend
- **Solution**: Ensure both containers are running with `docker-compose ps`
- Check if backend is healthy: `curl http://localhost:8000/health`

**Issue**: Port already in use
- **Solution**: Change the port mapping in `docker-compose.yml`

**Issue**: Docker build fails
- **Solution**: Ensure Docker daemon is running and you have sufficient disk space

---

Made with 💚 and FastAPI
