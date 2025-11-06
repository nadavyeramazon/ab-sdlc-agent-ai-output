# Greeting Application

A full-stack web application with a green-themed UI that greets users by their name. Built with FastAPI backend and vanilla JavaScript frontend.

## Features

- **Backend**: FastAPI REST API that accepts user names and returns personalized greetings
- **Frontend**: Green-themed responsive UI built with HTML, CSS, and vanilla JavaScript
- **Docker Compose**: Easy deployment with containerization
- **CORS Support**: Frontend and backend communicate seamlessly
- **Health Checks**: Built-in health monitoring for the backend

## Technology Stack

### Backend
- Python 3.11
- FastAPI
- Uvicorn (ASGI server)
- Pydantic (data validation)

### Frontend
- HTML5
- CSS3 (Green theme with animations)
- Vanilla JavaScript (ES6+)
- Nginx (web server)

### DevOps
- Docker
- Docker Compose

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Backend container configuration
│   └── .dockerignore        # Docker ignore file
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── styles.css           # Green-themed CSS
│   ├── app.js               # JavaScript application logic
│   ├── nginx.conf           # Nginx configuration
│   └── Dockerfile           # Frontend container configuration
├── docker-compose.yml   # Docker Compose configuration
└── README.md            # This file
```

## Getting Started

### Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 1.29 or higher)

### Installation & Running

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ab-sdlc-agent-ai-backend
   ```

2. **Start the application with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Usage

1. Open your web browser and navigate to http://localhost:3000
2. Enter your name in the input field
3. Click the "Greet Me!" button
4. Receive a personalized greeting message

## API Endpoints

### Backend API

- **GET /** - Root endpoint
  - Returns: Welcome message

- **POST /greet** - Greet a user
  - Request Body: `{"name": "string"}`
  - Response: `{"message": "string"}`
  - Example:
    ```bash
    curl -X POST http://localhost:8000/greet \
      -H "Content-Type: application/json" \
      -d '{"name": "John"}'
    ```

- **GET /health** - Health check
  - Returns: `{"status": "healthy"}`

## Development

### Running Backend Locally (without Docker)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Running Frontend Locally (without Docker)

```bash
cd frontend
python -m http.server 3000
# or use any other static file server
```

## Stopping the Application

To stop the application:

```bash
docker-compose down
```

To stop and remove volumes:

```bash
docker-compose down -v
```

## Troubleshooting

### Backend Not Responding

- Ensure port 8000 is not in use by another application
- Check backend logs: `docker-compose logs backend`
- Verify backend health: `curl http://localhost:8000/health`

### Frontend Connection Issues

- Verify the backend is running and healthy
- Check browser console for JavaScript errors
- Ensure CORS is properly configured in the backend

### Docker Issues

- Rebuild containers: `docker-compose up --build --force-recreate`
- Check running containers: `docker ps`
- View logs: `docker-compose logs`

## Features to Note

### Green Theme
- Primary Green: #2e7d32
- Secondary Green: #4caf50
- Light Green: #81c784
- Background gradient with green shades
- Smooth animations and transitions

### Responsive Design
- Mobile-friendly interface
- Adaptive layout for different screen sizes
- Touch-optimized controls

### User Experience
- Input validation
- Loading states with spinner
- Success and error feedback
- Keyboard support (Enter key to submit)
- Smooth animations

## License

See LICENSE file for details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
