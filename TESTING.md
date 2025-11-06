# Testing Guide

This document provides comprehensive information about testing the Greeting Application.

## Overview

The application includes comprehensive test coverage for both backend and frontend components:

- **Backend Tests**: Python/pytest based API testing
- **Frontend Tests**: JavaScript-based UI and integration testing
- **Security Tests**: Input validation and CORS testing
- **Integration Tests**: End-to-end workflow testing

## Backend Testing

### Running Backend Tests

#### Option 1: Direct Python Testing
```bash
cd backend
pip install -r requirements.txt
python -m pytest test_main.py -v
```

#### Option 2: Docker Testing
```bash
# Run tests in isolated container
docker-compose --profile testing up backend-tests

# Or build and run manually
docker build -t greeting-backend ./backend
docker run --rm greeting-backend python -m pytest test_main.py -v
```

### Backend Test Coverage

The backend tests cover:

- ✅ **API Endpoints**: All REST endpoints (`/`, `/health`, `/greet`)
- ✅ **Request Validation**: Input validation and error handling
- ✅ **Response Format**: Correct JSON response structure
- ✅ **Security**: Input sanitization and XSS prevention
- ✅ **Error Handling**: Various error scenarios
- ✅ **Greeting Types**: All supported greeting variations
- ✅ **Edge Cases**: Empty inputs, long names, special characters
- ✅ **Concurrency**: Multiple simultaneous requests

### Sample Backend Test Output
```
test_main.py::TestGreetingAPI::test_root_endpoint PASSED
test_main.py::TestGreetingAPI::test_health_check PASSED
test_main.py::TestGreetingAPI::test_greet_post_basic PASSED
test_main.py::TestGreetingAPI::test_greet_post_with_greeting_type PASSED
test_main.py::TestGreetingAPI::test_all_greeting_types PASSED
test_main.py::TestGreetingAPI::test_invalid_greeting_type PASSED
test_main.py::TestGreetingAPI::test_empty_name PASSED
...
======================== 20 passed in 2.34s ========================
```

## Frontend Testing

### Running Frontend Tests

#### Option 1: Browser Testing
1. Start the application:
   ```bash
   docker-compose up
   ```
2. Open browser to: `http://localhost:8080/test.html`
3. Tests run automatically and can be re-run manually

#### Option 2: Development Testing
1. Start backend: `cd backend && python main.py`
2. Serve frontend: `cd frontend && python -m http.server 8080`
3. Open: `http://localhost:8080/test.html`

### Frontend Test Coverage

The frontend tests cover:

- ✅ **Utility Functions**: Input validation and sanitization
- ✅ **API Integration**: Communication with backend services
- ✅ **UI Functions**: Error/success message handling
- ✅ **Form Validation**: Client-side input validation
- ✅ **Integration Flows**: Complete user workflows
- ✅ **Error Handling**: Network errors and API failures
- ✅ **Mock Testing**: Isolated testing with mock responses

### Frontend Test Categories

1. **Utility Functions Tests**
   - Input validation logic
   - Error message formatting
   - Data sanitization

2. **API Functions Tests**
   - HTTP request handling
   - Response parsing
   - Error response handling
   - Different greeting types

3. **UI Functions Tests**
   - Success message display
   - Error message display
   - UI state management

4. **Form Validation Tests**
   - Client-side validation rules
   - Input sanitization
   - Edge case handling

5. **Integration Tests**
   - End-to-end user workflows
   - API + UI integration
   - Error flow testing

## Security Testing

### Input Validation Tests

Both backend and frontend include comprehensive input validation:

```javascript
// Tests include validation for:
- Empty names ❌
- Names too long (>100 chars) ❌
- Names with HTML/script tags ❌
- Invalid greeting types ❌
- Valid international characters ✅
- Whitespace handling ✅
```

### CORS Security

The backend now uses secure CORS configuration:

```python
# Secure origins instead of wildcard
allowed_origins = [
    "http://localhost:3000",  # Development
    "http://localhost:8080",  # Production
    "http://frontend:8080",   # Docker
]
```

### Docker Security

Enhanced Docker security features:

```yaml
security_opt:
  - no-new-privileges:true
read_only: true  # Where possible
tmpfs:
  - /tmp:rw,noexec,nosuid,nodev
```

## Integration Testing

### Full Application Testing

1. **Start the application**:
   ```bash
   docker-compose up
   ```

2. **Verify services**:
   ```bash
   # Check backend health
   curl http://localhost:8000/health
   
   # Check frontend
   curl http://localhost:8080
   ```

3. **Test API endpoints**:
   ```bash
   # Test POST endpoint
   curl -X POST http://localhost:8000/greet \
     -H "Content-Type: application/json" \
     -d '{"name": "John", "greeting_type": "hello"}'
   
   # Test GET endpoint
   curl "http://localhost:8000/greet/John?greeting_type=welcome"
   ```

4. **Test frontend integration**:
   - Open `http://localhost:8080`
   - Test form submission
   - Verify error handling
   - Check different greeting types

## Performance Testing

### Load Testing Backend

```bash
# Install apache bench
sudo apt-get install apache2-utils

# Test backend performance
ab -n 1000 -c 10 -H "Content-Type: application/json" \
   -p post_data.json http://localhost:8000/greet
```

### Testing Checklist

Before deployment, ensure all tests pass:

- [ ] Backend unit tests (pytest)
- [ ] Frontend JavaScript tests (browser)
- [ ] Integration tests (full stack)
- [ ] Security validation tests
- [ ] Docker health checks
- [ ] CORS configuration
- [ ] Input validation
- [ ] Error handling
- [ ] Performance benchmarks

## Continuous Integration

### GitHub Actions Example

```yaml
name: Test Suite
on: [push, pull_request]
jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Backend Tests
        run: |
          cd backend
          pip install -r requirements.txt
          python -m pytest test_main.py -v
  
  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Integration Tests
        run: |
          docker-compose up -d
          # Wait for services
          sleep 30
          # Run integration tests
          curl -f http://localhost:8000/health
          curl -f http://localhost:8080
```

## Troubleshooting

### Common Issues

1. **Backend tests fail**:
   ```bash
   # Check Python version and dependencies
   python --version
   pip install -r backend/requirements.txt
   ```

2. **Frontend tests don't load**:
   ```bash
   # Check if backend is running
   curl http://localhost:8000/health
   ```

3. **Docker health checks fail**:
   ```bash
   # Check container logs
   docker-compose logs backend
   docker-compose logs frontend
   ```

4. **CORS errors in browser**:
   - Verify frontend URL is in CORS allowed origins
   - Check browser developer console for specific errors

### Debug Commands

```bash
# View detailed logs
docker-compose logs -f

# Check container health
docker-compose ps

# Run tests with verbose output
docker-compose --profile testing up backend-tests

# Check network connectivity
docker network ls
docker network inspect greeting_app-network
```

## Test Metrics

Current test coverage:
- **Backend**: 20+ test cases covering all endpoints and edge cases
- **Frontend**: 15+ test categories with comprehensive UI testing
- **Integration**: Full end-to-end workflow testing
- **Security**: Input validation and CORS testing
- **Performance**: Basic load testing capabilities

The application maintains high test coverage to ensure reliability and security in production deployments.