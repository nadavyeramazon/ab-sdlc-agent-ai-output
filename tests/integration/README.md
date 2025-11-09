# Integration Tests for Docker Compose Deployment

This directory contains comprehensive integration tests that validate the fullstack application after deployment with `docker compose up --build`.

## Overview

These tests are designed to verify that:
1. Both backend and frontend services start correctly
2. Backend API endpoints function properly
3. Frontend files are served correctly through nginx
4. Frontend-backend communication works via nginx proxy
5. CORS is configured correctly
6. API documentation is accessible
7. Error handling works as expected
8. Theme consistency is maintained

## Test Coverage

### Backend API Tests
- Health check endpoint
- Root endpoint
- POST /greet endpoint
- GET /greet/{name} endpoint
- POST /howdy endpoint
- GET /howdy/{name} endpoint
- Input validation (empty name, whitespace)

### Frontend Serving Tests
- Index.html accessibility
- Correct page title
- CSS file inclusion and accessibility
- JavaScript file inclusion and accessibility

### Nginx Proxy Integration Tests
- Health endpoint through proxy
- Greet endpoint through proxy
- Howdy endpoint through proxy
- Content-Type header preservation

### CORS Configuration Tests
- CORS headers presence
- All origins allowed (as configured)
- OPTIONS preflight requests

### API Documentation Tests
- Swagger UI accessibility
- OpenAPI JSON accessibility
- ReDoc accessibility

### Theme Consistency Tests
- Service name matches red theme
- Greeting messages mention red theme
- No green theme references
- Frontend title matches theme

### Error Handling Tests
- Invalid endpoint returns 404
- Invalid HTTP method returns 405
- Invalid JSON returns 422
- Missing required fields return 422

### Service Health Tests
- Backend response time
- Frontend response time
- Concurrent request handling

## Prerequisites

Before running these tests, ensure:
1. Docker and Docker Compose are installed
2. The application is running via `docker compose up --build`
3. Services are accessible on:
   - Backend: http://localhost:8000
   - Frontend: http://localhost:80

## Running the Tests

### From Repository Root

```bash
# Start the application
docker compose up -d --build

# Wait for services to be ready (tests include automatic retry logic)
sleep 10

# Run all integration tests
pytest tests/integration/ -v

# Run with detailed output
pytest tests/integration/ -v -s

# Run specific test class
pytest tests/integration/test_docker_compose_integration.py::TestBackendAPI -v

# Run with coverage
pytest tests/integration/ --cov=tests/integration --cov-report=html
```

### Cleanup

```bash
# Stop and remove containers
docker compose down -v
```

## Test Configuration

The tests use the following configuration:
- `BACKEND_URL`: http://localhost:8000
- `FRONTEND_URL`: http://localhost:80
- `FRONTEND_API_PROXY`: http://localhost:80/api
- `MAX_RETRIES`: 30 (for waiting for services)
- `RETRY_DELAY`: 2 seconds

## CI/CD Integration

These tests are integrated into the GitHub Actions CI pipeline:
1. Services are built with `docker compose up -d --build`
2. Tests wait for services to be ready
3. All integration tests are executed
4. Services are cleaned up with `docker compose down -v`

## Troubleshooting

### Services Not Starting

If tests fail with "Service failed to start":
```bash
# Check service logs
docker compose logs backend
docker compose logs frontend

# Check service status
docker compose ps

# Rebuild from scratch
docker compose down -v
docker system prune -f
docker compose up -d --build
```

### Port Conflicts

If ports 80 or 8000 are already in use:
```bash
# Check what's using the ports
sudo lsof -i :80
sudo lsof -i :8000

# Stop conflicting services or modify docker-compose.yml ports
```

### Network Issues

If tests fail with connection errors:
```bash
# Verify services are running
curl http://localhost:8000/health
curl http://localhost:80

# Check Docker network
docker network ls
docker network inspect <network_name>
```

## Adding New Tests

When adding new tests:
1. Create a new test class for logical grouping
2. Use descriptive test names starting with `test_`
3. Add appropriate assertions
4. Include docstrings explaining what's being tested
5. Handle potential race conditions with retries
6. Clean up any resources created during tests

## Test Output Example

```
🔄 Waiting for services to be ready...
✅ Backend ready (attempt 3/30)
✅ Frontend ready (attempt 1/30)
✅ All services are ready!

tests/integration/test_docker_compose_integration.py::TestBackendAPI::test_backend_health_endpoint PASSED
tests/integration/test_docker_compose_integration.py::TestBackendAPI::test_backend_greet_post PASSED
tests/integration/test_docker_compose_integration.py::TestFrontendServing::test_frontend_index_accessible PASSED
tests/integration/test_docker_compose_integration.py::TestNginxProxyIntegration::test_proxy_health_endpoint PASSED
...

========================= 25 passed in 15.32s =========================
```
