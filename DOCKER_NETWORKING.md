# Docker Networking Guide for Browser-Based Frontend Applications

## Overview

This document explains the Docker networking configuration for this application and clarifies common misconceptions about how browser-based frontends communicate with backend services in Docker.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User's Machine                        │
│                                                              │
│  ┌──────────────┐                                           │
│  │   Browser    │                                           │
│  │              │                                           │
│  │ Loads React  │                                           │
│  │ from         │                                           │
│  │ localhost:   │                                           │
│  │ 3000         │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         │ fetch('http://localhost:8000/api/hello')         │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Docker Port Mapping                     │   │
│  │                                                       │   │
│  │  localhost:3000 ───► frontend:3000 (container)      │   │
│  │  localhost:8000 ───► backend:8000  (container)      │   │
│  │                                                       │   │
│  │  ┌──────────────┐         ┌──────────────┐         │   │
│  │  │  frontend    │         │   backend    │         │   │
│  │  │  container   │         │   container  │         │   │
│  │  │              │         │              │         │   │
│  │  │  Serves      │         │  FastAPI     │         │   │
│  │  │  React app   │         │  API         │         │   │
│  │  │              │         │              │         │   │
│  │  └──────────────┘         └──────────────┘         │   │
│  │                                                       │   │
│  │  Internal network: app-network                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Key Concepts

### 1. Where Does the React App Run?

**CRITICAL UNDERSTANDING:** The React application runs **in the user's browser**, not in the Docker container.

- The frontend Docker container serves/builds the React app
- The browser downloads the React app (HTML, CSS, JavaScript)
- The React app executes in the browser (client-side)
- API calls are made from the browser, not from the container

### 2. How Does the Browser Access Services?

The browser runs on the user's machine and can only access services via:

- **localhost** (or 127.0.0.1)
- **Public IP addresses**
- **Domain names** that resolve via public DNS

 The browser **CANNOT** access:

- Docker service names (like 'backend', 'frontend')
- Docker internal networks
- Private container hostnames

### 3. Docker Port Mapping

Docker's port mapping makes internal container ports accessible on the host machine:

```yaml
ports:
  - "8000:8000"  # Maps container port 8000 to host port 8000
```

This means:
- Inside Docker: Service accessible as `backend:8000`
- Outside Docker (browser): Service accessible as `localhost:8000`

## Configuration Explained

### docker-compose.yml

```yaml
backend:
  ports:
    - "8000:8000"  # Expose backend to host
  # Inside Docker network: accessible as 'backend:8000'
  # On host machine: accessible as 'localhost:8000'

frontend:
  ports:
    - "3000:3000"  # Expose frontend to host
  environment:
    # MUST use localhost because browser makes the API calls
    - VITE_API_URL=http://localhost:8000
```

### Why `localhost:8000` is Correct

```javascript
// In frontend/src/App.jsx
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// When browser executes this:
fetch(`${API_URL}/api/hello`)  // fetch('http://localhost:8000/api/hello')
```

**Flow:**
1. Browser executes: `fetch('http://localhost:8000/api/hello')`
2. Request goes to host machine's `localhost:8000`
3. Docker routes `localhost:8000` → `backend:8000` (container)
4. Backend processes request
5. Response returns through the same path

### Why `backend:8000` Would Fail

```yaml
# INCORRECT CONFIGURATION
frontend:
  environment:
    - VITE_API_URL=http://backend:8000  # ❌ WRONG!
```

```javascript
// Browser tries to execute:
fetch('http://backend:8000/api/hello')
// ❌ Error: Browser cannot resolve 'backend' hostname
// Result: "Failed to fetch" or "DNS resolution failed"
```

**Why it fails:**
- 'backend' is a Docker service name
- Docker's internal DNS only works inside the Docker network
- Browser is not inside the Docker network
- Browser's DNS cannot resolve 'backend'

## When to Use Service Names

Docker service names (like 'backend', 'database', 'redis') are used for:

### ✅ Container-to-Container Communication

```python
# In another backend service (running in Docker):
import requests
response = requests.get('http://backend:8000/api/hello')  # ✅ Works!
```

```javascript
// In a Node.js backend service (running in Docker):
fetch('http://backend:8000/api/hello')  // ✅ Works!
```

### ❌ Browser-to-Container Communication

```javascript
// In React app (running in browser):
fetch('http://backend:8000/api/hello')  // ❌ Fails!
```

## CORS Configuration

The backend must allow requests from the frontend's origin:

```python
# backend/main.py
origins = [
    "http://frontend:3000",      # For container-to-container (not used here)
    "http://localhost:3000",     # ✅ For browser access (Vite dev server)
    "http://localhost:5173",     # ✅ For browser access (alternative Vite port)
]
```

The browser sends requests from `http://localhost:3000` (where it loaded the app), so CORS must allow `http://localhost:3000`.

## Testing the Configuration

### Start the Application

```bash
docker compose up --build
```

### Access in Browser

1. Open: `http://localhost:3000`
2. Click "Get Message from Backend"
3. Should successfully fetch from backend

### Verify in Browser Console

```javascript
// Check the actual request URL
fetch('http://localhost:8000/api/hello')
  .then(r => r.json())
  .then(d => console.log(d))
// Should return: {message: "Hello World from Backend!", timestamp: "..."}
```

## Common Misconceptions

### ❌ Misconception 1
"Since frontend and backend are in the same Docker network, frontend should use service names."

**Reality:** The frontend *container* is in the Docker network, but the React *app* runs in the browser, which is not.

### ❌ Misconception 2
"Environment variables in docker-compose.yml are for the running application."

**Reality:** For React/Vite, `VITE_API_URL` is used at *build time* and embedded in the JavaScript bundle that runs in the browser.

### ❌ Misconception 3
"Changing VITE_API_URL to use service name will make it work inside Docker."

**Reality:** The URL is used by the browser, which runs outside Docker. Service names never work in browsers.

## Troubleshooting

### Issue: "Failed to fetch" in Browser

**Check:**
1. Is backend port exposed? (`ports: "8000:8000"` in docker-compose.yml)
2. Is VITE_API_URL using `localhost`? (not service name)
3. Is CORS allowing the frontend origin? (check backend CORS config)
4. Is backend running? (`docker compose ps`)

### Issue: CORS Error in Browser

**Check:**
1. Backend CORS allows `http://localhost:3000`
2. Backend CORS allows the HTTP method (GET, POST, etc.)
3. Browser is accessing from correct origin

### Issue: "Cannot connect to backend"

**Check:**
1. Backend is running: `docker compose ps`
2. Backend is healthy: `curl http://localhost:8000/health`
3. Ports are correctly mapped in docker-compose.yml
4. No port conflicts with other applications

## Summary

✅ **CORRECT Configuration:**
- `VITE_API_URL=http://localhost:8000`
- Backend exposes port: `ports: "8000:8000"`
- CORS allows: `http://localhost:3000`

❌ **INCORRECT Configuration:**
- `VITE_API_URL=http://backend:8000` (browser can't resolve)
- No port exposure (browser can't connect)
- CORS allows only `http://frontend:3000` (wrong origin)

## References

- [Docker Networking Documentation](https://docs.docker.com/network/)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [React in Docker Best Practices](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/)
- [CORS Explained](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
