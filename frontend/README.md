# Frontend - JavaScript Green Application

A simple JavaScript frontend application with a green theme that communicates with the FastAPI backend.

## Features

- Clean, modern green-themed UI
- REST API communication with backend
- Error handling and loading states
- Responsive design
- Containerized with Nginx

## Running Locally

You can open `index.html` directly in a browser, or use a simple HTTP server:

```bash
# Using Python
python -m http.server 3000

# Using Node.js
npx http-server -p 3000
```

The application will be available at http://localhost:3000

## Running with Docker

```bash
docker build -t frontend .
docker run -p 3000:80 frontend
```

## Configuration

The backend URL is configured in `app.js`. Update the `BACKEND_URL` constant if your backend runs on a different address.
