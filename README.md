# Greeting Application 🌿

A full-stack web application with a green-themed frontend and FastAPI backend that greets users by name.

## 🏗️ Architecture

- **Backend**: FastAPI application in the `backend/` folder
- **Frontend**: JavaScript SPA with green theme in the `frontend/` folder  
- **Deployment**: Docker Compose for easy local development

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
- **Error Handling**: Comprehensive error messages and loading states
- **Accessibility**: Keyboard navigation and proper ARIA labels

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **CORS Support**: Configured to work with frontend
- **Input Validation**: Pydantic models for request/response validation
- **Health Checks**: Built-in health endpoint for monitoring
- **Documentation**: Auto-generated API docs with Swagger UI

## 📚 API Endpoints

### GET `/`
Root endpoint with welcome message.

### GET `/health`
Health check endpoint.

### POST `/greet`
Greet a user by name.

**Request Body**:
```json
{
  "name": "string"
}
```

**Response**:
```json
{
  "message": "Hello, John! Welcome to our green-themed application!",
  "name": "John"
}
```

### GET `/greet/{name}`
Greet a user by name via GET request.

**Response**:
```json
{
  "message": "Hello, John! Welcome to our green-themed application!",
  "name": "John"
}
```

## 🛠️ Development

### Project Structure
```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container config
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── styles.css          # Green-themed styles
│   ├── script.js           # JavaScript functionality
│   ├── nginx.conf          # Nginx configuration
│   └── Dockerfile          # Frontend container config
├── docker-compose.yml      # Docker Compose configuration
└── README.md              # This file
```

### Environment Variables

The application uses the following default configurations:
- Backend runs on port `8000`
- Frontend runs on port `3000` (port `80` inside container)
- API base URL is set to `http://localhost:8000`

### Customization

#### Changing the Theme
Edit the CSS variables in `frontend/styles.css`:
```css
:root {
    --primary-green: #2d5f3f;
    --secondary-green: #4a7c59;
    --light-green: #68a47c;
    /* ... */
}
```

#### Backend Configuration
Modify `backend/main.py` to change API behavior, add new endpoints, or update CORS settings.

## 🧪 Testing

### Backend Testing
```bash
cd backend
curl http://localhost:8000/health
curl -X POST http://localhost:8000/greet -H "Content-Type: application/json" -d '{"name":"Test User"}'
```

### Frontend Testing
1. Open http://localhost:3000 in your browser
2. Enter a name in the input field
3. Click "Get Greeting" to test the API integration

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

### Rebuild specific service
```bash
docker-compose build backend
docker-compose build frontend
```

## 🔧 Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure the backend CORS configuration includes your frontend URL
2. **Connection Refused**: Ensure both services are running and ports are not blocked
3. **Build Failures**: Check Docker is running and you have sufficient disk space

### Debug Mode
Enable debug mode in the frontend by running this in the browser console:
```javascript
localStorage.setItem('debug', 'true');
```

## 📦 Dependencies

### Backend
- FastAPI 0.104.1
- Uvicorn 0.24.0
- Pydantic 2.5.0

### Frontend
- Pure JavaScript (no frameworks)
- CSS3 with custom properties
- HTML5

### Infrastructure
- Docker & Docker Compose
- Nginx (for frontend serving)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes
4. Test thoroughly
5. Commit your changes: `git commit -am 'Add new feature'`
6. Push to the branch: `git push origin feature/new-feature`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Future Enhancements

- [ ] Add user authentication
- [ ] Implement greeting history
- [ ] Add more greeting templates
- [ ] Include unit and integration tests
- [ ] Add CI/CD pipeline
- [ ] Implement logging and monitoring
- [ ] Add database integration
- [ ] Create mobile app version

---

**Made with 💚 and FastAPI**
