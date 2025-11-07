# Green Theme Application

A full-stack application with a green-themed frontend and FastAPI backend, fully integrated with Docker Compose.

## 🌿 Features

- **Frontend**: Clean, green-themed UI built with vanilla JavaScript, HTML, and CSS
- **Backend**: FastAPI-based REST API with automatic documentation
- **Docker Integration**: Complete Docker Compose setup for easy deployment
- **CORS Enabled**: Frontend and backend communication configured
- **Health Checks**: Built-in health monitoring for both services

## 📁 Project Structure

```
.
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── styles.css          # Green-themed styling
│   ├── app.js              # JavaScript application logic
│   ├── nginx.conf          # Nginx configuration
│   └── Dockerfile          # Frontend Docker configuration
├── backend/
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend Docker configuration
├── docker-compose.yml      # Docker Compose configuration
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Start the application with Docker Compose:
```bash
docker-compose up --build
```

3. Access the application:
   - **Frontend**: http://localhost
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

### Stopping the Application

```bash
docker-compose down
```

## 🔌 API Endpoints

### GET `/`
Returns welcome message and API information

### GET `/health`
Health check endpoint

### POST `/message`
Send a message to the backend

**Request Body:**
```json
{
  "message": "Your message here"
}
```

**Response:**
```json
{
  "received_message": "Your message here",
  "response": "Thank you for your message! I received: 'Your message here'",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

### GET `/data`
Returns sample data

### GET `/info`
Returns application information

## 🎨 Frontend Features

- Responsive design
- Green color theme with gradient effects
- Interactive buttons with hover effects
- Real-time API communication
- Error handling with user-friendly messages
- Loading states for async operations

## 🔧 Backend Features

- FastAPI framework
- Automatic API documentation (Swagger UI)
- CORS middleware configured
- Request validation with Pydantic
- Structured logging
- Health check endpoint

## 🐳 Docker Configuration

### Backend Service
- Based on Python 3.11 slim image
- Runs on port 8000
- Hot reload enabled for development
- Health check monitoring

### Frontend Service
- Based on Nginx Alpine image
- Runs on port 80
- Optimized with gzip compression
- Static asset caching
- Health check monitoring

## 🌐 Network Configuration

Both services are connected via a custom bridge network (`app-network`) for secure inter-service communication.

## 📝 Development

### Running Backend Locally

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Running Frontend Locally

Simply open `frontend/index.html` in a web browser, or use a local server:

```bash
cd frontend
python -m http.server 8080
```

## 🔒 Production Considerations

- Update CORS origins in `backend/main.py` to specific domains
- Use environment variables for configuration
- Implement proper authentication and authorization
- Add rate limiting
- Use HTTPS
- Implement proper logging and monitoring
- Add database integration if needed

## 📄 License

See LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.