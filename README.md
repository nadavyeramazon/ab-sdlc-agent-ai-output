# Green-Themed Greeting Application

A full-stack web application featuring a beautiful green-themed frontend and a FastAPI Python backend that greets users based on their input.

## 🌿 Project Overview

This project consists of two main components:

1. **Backend**: FastAPI-based REST API that provides personalized greeting functionality
2. **Frontend**: Green-themed web interface with smooth animations and responsive design

## ✨ Features

### Frontend
- 🌱 Beautiful green color scheme throughout the UI
- 👋 Interactive greeting interface
- 📱 Fully responsive design (mobile, tablet, desktop)
- ✨ Smooth animations and transitions
- ⚡ Real-time input validation
- 🔄 Comprehensive error handling

### Backend
- 🚀 Fast and modern FastAPI framework
- 🔒 Type-safe with Pydantic validation
- 📝 Auto-generated API documentation
- ✅ Health check endpoints
- 🔄 CORS support for frontend integration

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic

**Frontend:**
- HTML5
- CSS3 (with CSS Variables and Animations)
- Vanilla JavaScript

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A modern web browser

### 1. Clone the Repository

```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

### 2. Set Up the Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
python main.py
```

The backend will start at `http://localhost:8000`

### 3. Set Up the Frontend

```bash
# In a new terminal, navigate to frontend folder
cd frontend

# Option 1: Open directly in browser
# Simply open index.html in your web browser

# Option 2: Use a local server (recommended)
python -m http.server 3000
# Then open http://localhost:3000 in your browser
```

### 4. Use the Application

1. Open the frontend in your browser (http://localhost:3000 or open index.html)
2. Enter your name in the input field
3. Click "Greet Me!" or press Enter
4. Enjoy your personalized green-themed greeting!

## 📚 API Documentation

Once the backend is running, you can access:

- Interactive API docs (Swagger): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

### Available Endpoints

#### GET `/`
Welcome message

#### GET `/health`
Health check endpoint

#### POST `/greet`
Greet a user based on their name

**Request:**
```json
{
  "name": "John"
}
```

**Response:**
```json
{
  "message": "Hello, John! Welcome to our green-themed greeting service. Have a wonderful day!"
}
```

## 📁 Project Structure

```
ab-sdlc-agent-ai-backend/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Docker configuration
│   └── README.md            # Backend documentation
│
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── styles.css           # Green-themed styling
│   ├── app.js               # JavaScript functionality
│   ├── Dockerfile           # Docker configuration
│   ├── nginx.conf           # Nginx configuration
│   └── README.md            # Frontend documentation
│
├── docker-compose.yml    # Docker Compose configuration
├── .env.example          # Environment variables example
├── .gitignore            # Git ignore file
├── LICENSE               # License file
└── README.md             # This file
```

## 🐳 Docker Support

You can run the entire application using Docker Compose:

```bash
# Build and start all services
docker-compose up --build

# Access the application:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

To stop the services:

```bash
docker-compose down
```

## 🎨 Color Palette

The green theme uses the following colors:

- **Primary Green**: `#2d5f2e` - Main brand color
- **Secondary Green**: `#4a7c4e` - Accent color
- **Light Green**: `#7cb87f` - Borders and highlights
- **Very Light Green**: `#a8d5aa` - Backgrounds
- **Pale Green**: `#e8f5e9` - Light backgrounds
- **Dark Green**: `#1b3a1c` - Text on light backgrounds
- **Accent Green**: `#76c776` - Interactive elements

## ⚙️ Configuration

### Backend Configuration

Set environment variables:

```bash
# Port configuration
export PORT=8000

# Then run
python main.py
```

### Frontend Configuration

Update the API URL in `frontend/app.js` if your backend runs on a different address:

```javascript
const API_URL = 'http://your-backend-url:port';
```

## 🧪 Testing

### Test the Backend

```bash
# Health check
curl http://localhost:8000/health

# Test greeting endpoint
curl -X POST http://localhost:8000/greet \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'
```

### Test the Frontend

1. Open the application in your browser
2. Try entering different names
3. Test with an empty name
4. Try stopping the backend to see error handling

## 🛠️ Development

### Backend Development

```bash
cd backend

# Run with auto-reload
uvicorn main:app --reload
```

### Frontend Development

Simply edit the HTML, CSS, or JavaScript files and refresh your browser.

## 🐛 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Use a different port
PORT=8001 python main.py
```

**Module not found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Issues

**Can't connect to backend:**
1. Ensure backend is running on http://localhost:8000
2. Check the browser console for errors
3. Verify the API_URL in app.js is correct

**CORS errors:**
1. Make sure backend CORS middleware is configured
2. Use a local server instead of opening HTML directly

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Initial work - [nadavyeramazon](https://github.com/nadavyeramazon)

## 🙏 Acknowledgments

- FastAPI for the excellent Python web framework
- The open-source community for inspiration

---

**Enjoy your green-themed greeting experience! 🌿👋**
