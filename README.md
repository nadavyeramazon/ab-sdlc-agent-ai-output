# Microservices Application with Docker Compose

This project demonstrates a microservices architecture with a FastAPI backend and a JavaScript/Express frontend, orchestrated using Docker Compose.

## 🏗️ Architecture

- **Backend**: FastAPI (Python) - RESTful API service
- **Frontend**: Express.js (Node.js) - Web interface with green theme
- **Orchestration**: Docker Compose - Container management

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Backend container configuration
│   └── .dockerignore
├── frontend/
│   ├── server.js           # Express.js server
│   ├── package.json        # Node.js dependencies
│   ├── Dockerfile         # Frontend container configuration
│   ├── .dockerignore
│   └── public/
│       ├── index.html     # Main HTML page
│       ├── styles.css     # Green-themed CSS
│       └── script.js      # Frontend JavaScript
├── docker-compose.yml      # Docker Compose configuration
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed ([Get Docker Compose](https://docs.docker.com/compose/install/))

### Running the Application

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd ab-sdlc-agent-ai-backend
   ```

2. **Start all services**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Backend API Docs: http://localhost:8000/docs

4. **Stop the services**:
   ```bash
   docker-compose down
   ```

## 🎯 Features

### Backend (FastAPI)
- ✅ RESTful API endpoints
- ✅ Health check endpoint
- ✅ CORS enabled for frontend communication
- ✅ Interactive API documentation (Swagger UI)
- ✅ Hello World endpoint
- ✅ Personalized greeting endpoint

### Frontend (Express.js)
- ✅ Beautiful green-themed UI
- ✅ Real-time backend communication
- ✅ Interactive greeting feature
- ✅ Responsive design
- ✅ Error handling and status display

## 📡 API Endpoints

### Backend Service (Port 8000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Hello World message |
| `/health` | GET | Health check |
| `/api/greeting` | GET | Get personalized greeting |
| `/docs` | GET | Interactive API documentation |

### Frontend Service (Port 3000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/health` | GET | Health check |
| `/api/backend-data` | GET | Fetch data from backend |
| `/api/greeting` | GET | Proxy to backend greeting |

## 🔧 Development

### Running Services Individually

#### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

### Environment Variables

#### Backend
- No additional environment variables required

#### Frontend
- `BACKEND_URL`: Backend service URL (default: `http://backend:8000`)
- `PORT`: Frontend port (default: `3000`)

## 🐳 Docker Commands

```bash
# Build and start services
docker-compose up --build

# Start services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes
docker-compose down -v

# Rebuild specific service
docker-compose build backend
docker-compose build frontend
```

## 🧪 Testing the Communication

1. Open the frontend at http://localhost:3000
2. Click the "Connect to Backend" button
3. You should see a successful response from the backend
4. Enter your name and click "Get Greeting" to test the greeting endpoint

## 🎨 Customization

### Backend
- Edit `backend/main.py` to add new endpoints or modify existing ones
- Update `backend/requirements.txt` for additional dependencies

### Frontend
- Modify `frontend/public/index.html` for UI changes
- Edit `frontend/public/styles.css` to customize the green theme
- Update `frontend/public/script.js` for functionality changes
- Edit `frontend/server.js` for server-side logic

## 📝 Notes

- The backend uses FastAPI with automatic API documentation
- The frontend is styled with a green theme as requested
- Both services include health check endpoints
- Docker Compose manages networking between services
- Services restart automatically unless stopped manually

## 🐛 Troubleshooting

### Services not starting
- Check if ports 3000 and 8000 are available
- Run `docker-compose logs` to see error messages

### Frontend can't connect to backend
- Ensure both services are running
- Check network configuration in `docker-compose.yml`
- Verify BACKEND_URL environment variable

### Port already in use
- Stop other services using ports 3000 or 8000
- Or modify ports in `docker-compose.yml`

## 📄 License

See LICENSE file for details.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!
