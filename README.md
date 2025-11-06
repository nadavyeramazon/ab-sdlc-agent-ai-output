# 🌿 Green Greeter Application

A beautiful, green-themed web application that greets users with a friendly message. The application consists of a FastAPI backend and a JavaScript frontend, containerized with Docker Compose.

## ✨ Features

- 🎨 **Green-themed UI**: Beautiful, nature-inspired design with gradients and animations
- 🚀 **FastAPI Backend**: Fast, modern Python API with automatic documentation
- 💫 **Interactive Frontend**: Responsive JavaScript UI with real-time validation
- 🐳 **Docker Compose**: Easy deployment with containerization
- 🔒 **Input Validation**: Secure handling of user input with proper error handling
- 📱 **Responsive Design**: Works great on desktop and mobile devices
- ⚡ **Real-time Communication**: Frontend communicates with backend via REST API

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/REST API    ┌─────────────────┐
│                 │ ──────────────────► │                 │
│   Frontend      │                     │    Backend      │
│   (JavaScript)  │ ◄────────────────── │   (FastAPI)     │
│   Port: 3000    │                     │   Port: 8000    │
└─────────────────┘                     └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed on your system
- Git to clone the repository

### Running the Application

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
   cd ab-sdlc-agent-ai-backend
   git checkout feature/test-13
   ```

2. **Start the application with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

## 📁 Project Structure

```
.
├── backend/                 # FastAPI backend application
│   ├── app.py              # Main FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container configuration
├── frontend/               # JavaScript frontend application
│   ├── index.html         # Main HTML file
│   ├── styles.css         # Green-themed CSS styles
│   ├── script.js          # JavaScript functionality
│   ├── nginx.conf         # Nginx configuration
│   └── Dockerfile         # Frontend container configuration
├── docker-compose.yml      # Multi-container orchestration
└── README.md              # This file
```

## 🎯 How It Works

1. **User Input**: User enters their name in the frontend form
2. **Validation**: JavaScript validates the input client-side
3. **API Call**: Frontend sends a POST request to `/greet` endpoint
4. **Processing**: Backend processes the request and generates a greeting
5. **Response**: Backend returns a personalized greeting message
6. **Display**: Frontend displays the greeting with beautiful animations

## 🛠️ Development

### Running Backend Locally

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The backend will be available at http://localhost:8000

### Running Frontend Locally

Simply open `frontend/index.html` in your browser, or serve it with a local server:

```bash
cd frontend
python -m http.server 3000
```

The frontend will be available at http://localhost:3000

### API Endpoints

- `GET /` - Root endpoint with welcome message
- `GET /health` - Health check endpoint
- `POST /greet` - Greet a user by name
  - Request body: `{"name": "string"}`
  - Response: `{"message": "string"}`

## 🎨 UI Features

- **Green Theme**: Nature-inspired color palette with gradients
- **Responsive Design**: Adapts to different screen sizes
- **Animations**: Smooth transitions and loading effects
- **Interactive Elements**: Hover effects and focus states
- **Error Handling**: User-friendly error messages
- **Loading States**: Visual feedback during API calls
- **Keyboard Shortcuts**: 
  - Enter to submit
  - Escape to clear
  - Ctrl+Enter for quick greeting

## 🔧 Configuration

### Environment Variables

The application uses the following default configurations:

- **Frontend Port**: 3000
- **Backend Port**: 8000
- **API Base URL**: http://localhost:8000

To modify these settings, update the `docker-compose.yml` file or the JavaScript configuration in `script.js`.

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**:
   - Change the ports in `docker-compose.yml`
   - Or stop conflicting services

2. **Backend Not Responding**:
   - Check if backend container is running: `docker-compose ps`
   - View backend logs: `docker-compose logs backend`

3. **CORS Issues**:
   - The backend is configured to allow all origins for development
   - In production, update CORS configuration in `app.py`

4. **Docker Build Issues**:
   - Clean Docker cache: `docker system prune`
   - Rebuild without cache: `docker-compose build --no-cache`

## 🚀 Production Deployment

For production deployment:

1. **Update CORS settings** in `backend/app.py`
2. **Set proper environment variables**
3. **Use a reverse proxy** (nginx/traefik) for HTTPS
4. **Enable proper logging** and monitoring
5. **Set up health checks** and auto-restart policies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🌟 Acknowledgments

- Built with ❤️ and a love for green themes
- FastAPI for the amazing Python web framework
- Modern web technologies for smooth user experience

---

**Enjoy greeting your users with this beautiful green-themed application! 🌿✨**