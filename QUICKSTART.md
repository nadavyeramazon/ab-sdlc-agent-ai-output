# Quick Start Guide

## Prerequisites
Make sure you have Docker and Docker Compose installed on your system.

## Start the Application (3 Simple Steps)

### 1. Clone and Navigate
```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
git checkout feature/test-10
```

### 2. Start with Docker Compose
```bash
docker-compose up --build
```

Wait for both services to start. You should see:
- Backend running on port 8000
- Frontend running on port 3000

### 3. Open Your Browser
Navigate to: **http://localhost:3000**

## Using the Application

1. **Enter your name** in the input field
2. **Click "Greet Me!"** button
3. **See your personalized greeting** with a beautiful green-themed response!

## What You'll See

- A beautiful green-themed interface
- Smooth animations and transitions
- Responsive design that works on all devices
- Real-time feedback from the backend

## API Endpoints

You can also interact directly with the backend:

### Test the Greeting API
```bash
curl -X POST http://localhost:8000/greet \
  -H "Content-Type: application/json" \
  -d '{"name": "Your Name"}'
```

### Check Backend Health
```bash
curl http://localhost:8000/health
```

### View API Documentation
Open: **http://localhost:8000/docs**

## Stopping the Application

Press `Ctrl+C` in the terminal, then:
```bash
docker-compose down
```

## Troubleshooting

### Port Already in Use?
If ports 3000 or 8000 are already in use:

1. Stop the conflicting service, or
2. Edit `docker-compose.yml` to use different ports:
   ```yaml
   ports:
     - "3001:80"  # Frontend
     - "8001:8000"  # Backend
   ```

### Backend Not Responding?
```bash
# Check if backend is healthy
docker-compose logs backend

# Restart the backend
docker-compose restart backend
```

### Frontend Not Loading?
```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild and restart
docker-compose up --build --force-recreate
```

## Architecture Overview

```
┌─────────────────┐         ┌─────────────────┐
│    Frontend     │         │     Backend     │
│   (Nginx:80)    │ ◄─────► │  (FastAPI:8000) │
│   Port 3000     │   HTTP  │                 │
└─────────────────┘         └─────────────────┘
     │                              │
     │                              │
  Static Files              REST API
  (HTML/CSS/JS)            (POST /greet)
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for technical details
- Explore the code in `backend/` and `frontend/` folders
- Try modifying the green theme colors in `frontend/styles.css`
- Add more endpoints to the backend API

## Need Help?

If you encounter any issues:
1. Check the logs: `docker-compose logs`
2. Verify Docker is running: `docker ps`
3. Check port availability: `lsof -i :3000` and `lsof -i :8000`
4. Try rebuilding: `docker-compose up --build --force-recreate`

Enjoy your green-themed greeting application! 🌿
