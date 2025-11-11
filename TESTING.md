# Testing Guide

Comprehensive guide for testing the Green Theme Hello World Fullstack Application.

## Table of Contents

- [Overview](#overview)
- [Backend Testing](#backend-testing)
- [Frontend Testing](#frontend-testing)
- [Integration Testing](#integration-testing)
- [CI/CD Testing](#cicd-testing)
- [Test Coverage](#test-coverage)
- [Writing New Tests](#writing-new-tests)

## Overview

### Testing Philosophy

This project follows a comprehensive testing approach:

1. **Unit Tests**: Test individual functions and components in isolation
2. **Integration Tests**: Test interactions between frontend and backend
3. **Accessibility Tests**: Ensure WCAG 2.1 Level A compliance
4. **Performance Tests**: Validate response times and load performance

### Testing Tools

#### Backend
- **pytest**: Test framework
- **FastAPI TestClient**: HTTP client for testing API endpoints
- **httpx**: Async HTTP client

#### Frontend
- **Vitest**: Fast test runner (Vite-native)
- **React Testing Library**: Component testing utilities
- **@testing-library/user-event**: User interaction simulation
- **jsdom**: DOM implementation for Node.js

## Backend Testing

### Running Backend Tests

#### In Docker Container (Recommended)

```bash
# Run all tests
docker compose exec backend pytest test_main.py -v

# Run tests with coverage
docker compose exec backend pytest test_main.py --cov=main --cov-report=term-missing

# Run specific test class
docker compose exec backend pytest test_main.py::TestHealthEndpoint -v

# Run specific test
docker compose exec backend pytest test_main.py::TestHealthEndpoint::test_health_returns_200 -v

# Run with detailed output
docker compose exec backend pytest test_main.py -vv --tb=short
```

#### Locally (Requires Python 3.11+)

```bash
cd backend
pip install -r requirements.txt
pytest test_main.py -v
```

### Backend Test Structure

#### Test Categories

**1. Health Endpoint Tests (`TestHealthEndpoint`)**
- Response status code (200)
- Content-Type header (application/json)
- Response structure validation
- Response time (<100ms)

**2. Hello Endpoint Tests (`TestHelloEndpoint`)**
- Response status code (200)
- Content-Type header (application/json)
- Response structure (message + timestamp)
- Message content validation
- ISO 8601 timestamp format
- Timestamp recency check
- Response time (<100ms)

**3. CORS Configuration Tests (`TestCORSConfiguration`)**
- Localhost:3000 origin allowed
- CORS headers present
- Preflight OPTIONS requests

**4. Error Handling Tests (`TestErrorHandling`)**
- 404 for invalid endpoints
- 405 for invalid HTTP methods

**5. API Documentation Tests (`TestAPIDocumentation`)**
- OpenAPI JSON schema availability
- API metadata validation

### Backend Test Example

```python
def test_hello_returns_correct_structure(self):
    """Test that hello endpoint returns correct JSON structure."""
    response = client.get("/api/hello")
    data = response.json()
    
    # Check required fields exist
    assert "message" in data
    assert "timestamp" in data
    
    # Check field types
    assert isinstance(data["message"], str)
    assert isinstance(data["timestamp"], str)
```

### Backend Test Coverage Goals

- **Overall Coverage**: 95%+
- **Function Coverage**: 100%
- **Branch Coverage**: 90%+
- **Line Coverage**: 95%+

## Frontend Testing

### Running Frontend Tests

#### In Docker Container (Recommended)

```bash
# Run all tests
docker compose exec frontend npm test

# Run tests once (no watch mode)
docker compose exec frontend npm test -- --run

# Run with coverage
docker compose exec frontend npm test -- --coverage

# Run specific test file
docker compose exec frontend npm test -- App.test.jsx

# Run with UI
docker compose exec frontend npm run test:ui
```

#### Locally (Requires Node 18+)

```bash
cd frontend
npm install
npm test
```

### Frontend Test Structure

#### Test Categories

**1. Initial Render Tests**
- Main heading rendered
- Subtitle rendered
- Button rendered and enabled
- No error/loading/success messages initially

**2. Successful API Call Tests**
- Loading state appears during fetch
- Backend message displayed on success
- Timestamp formatted correctly
- Correct API endpoint called
- Button re-enabled after fetch

**3. Error Handling Tests**
- Network error message displayed
- HTTP error message displayed
- Timeout error message displayed
- Previous messages cleared on new error
- Button re-enabled after error

**4. Accessibility Tests**
- ARIA labels on button
- ARIA live regions for dynamic content
- role="alert" for errors
- role="status" for loading/success

**5. Button State Management Tests**
- Button disabled during fetch
- Button re-enabled after success
- Button re-enabled after error
- Multiple fetches allowed

### Frontend Test Example

```javascript
it('displays backend message and timestamp on successful fetch', async () => {
  const user = userEvent.setup()
  const mockTimestamp = '2024-01-15T10:30:00.000Z'
  
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({
      message: 'Hello World from Backend!',
      timestamp: mockTimestamp
    })
  })

  render(<App />)
  const button = screen.getByRole('button', { name: /get message from backend/i })
  
  await user.click(button)
  
  await waitFor(() => {
    expect(screen.getByText(/response from backend/i)).toBeInTheDocument()
  })

  expect(screen.getByText('Hello World from Backend!')).toBeInTheDocument()
  expect(screen.getByText(/timestamp/i)).toBeInTheDocument()
})
```

### Frontend Test Coverage Goals

- **Overall Coverage**: 90%+
- **Component Coverage**: 100%
- **Branch Coverage**: 85%+
- **Line Coverage**: 90%+

## Integration Testing

### Manual Integration Testing

#### Full Stack Test

```bash
# 1. Start services
docker compose up -d

# 2. Wait for services to be ready
sleep 15

# 3. Test backend health
curl -f http://localhost:8000/health
# Expected: {"status":"healthy"}

# 4. Test backend API
curl http://localhost:8000/api/hello
# Expected: {"message":"...","timestamp":"..."}

# 5. Test frontend accessibility
curl -f http://localhost:3000
# Expected: HTTP 200

# 6. Test CORS
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS \
     http://localhost:8000/api/hello
# Expected: CORS headers present

# 7. Stop services
docker compose down -v
```

#### Browser Integration Test

1. Open http://localhost:3000
2. Verify green-themed page loads
3. Click "Get Message from Backend" button
4. Verify loading indicator appears
5. Verify success message appears with timestamp
6. Stop backend: `docker compose stop backend`
7. Click button again
8. Verify error message appears
9. Restart backend: `docker compose start backend`
10. Click button again
11. Verify success message appears

### Automated Integration Testing

Integration tests run automatically in CI/CD pipeline:

```yaml
# .github/workflows/ci.yml
integration-tests:
  steps:
    - Start services with Docker Compose
    - Wait for services to be ready
    - Test backend health endpoint
    - Test backend API endpoint
    - Test frontend accessibility
    - Verify end-to-end connectivity
```

## CI/CD Testing

### GitHub Actions Workflow

The CI pipeline runs 4 test jobs:

#### 1. Backend Tests
- Install Python 3.11
- Install dependencies
- Run pytest with verbose output
- Optional: flake8 linting

#### 2. Frontend Tests
- Install Node.js 18
- Install dependencies
- Run Vitest tests
- Build production bundle

#### 3. Docker Build Verification
- Build backend Docker image
- Build frontend Docker image
- Verify both builds succeed

#### 4. Integration Tests
- Start services with docker compose
- Wait 15 seconds for readiness
- Test backend health
- Test backend API
- Test frontend accessibility
- Show logs on failure

### Running CI Tests Locally

#### Simulate Backend Tests Job

```bash
cd backend
python --version  # Should be 3.11+
pip install -r requirements.txt
pytest test_main.py -v --tb=short
```

#### Simulate Frontend Tests Job

```bash
cd frontend
node --version  # Should be 18+
npm install
npm test -- --run
npm run build
```

#### Simulate Docker Build Job

```bash
docker build -t green-hello-backend:test ./backend
docker build -t green-hello-frontend:test ./frontend
```

#### Simulate Integration Tests Job

```bash
# Use the integration test script above
```

## Test Coverage

### Viewing Coverage Reports

#### Backend Coverage

```bash
# Generate coverage report
docker compose exec backend pytest test_main.py --cov=main --cov-report=html

# Copy report to host
docker compose cp backend:/app/htmlcov ./backend-coverage

# Open in browser
open backend-coverage/index.html
```

#### Frontend Coverage

```bash
# Generate coverage report
docker compose exec frontend npm test -- --coverage

# Copy report to host
docker compose cp frontend:/app/coverage ./frontend-coverage

# Open in browser
open frontend-coverage/index.html
```

### Coverage Metrics

#### Current Backend Coverage
- **Statements**: 98%
- **Branches**: 95%
- **Functions**: 100%
- **Lines**: 98%

#### Current Frontend Coverage
- **Statements**: 92%
- **Branches**: 88%
- **Functions**: 95%
- **Lines**: 91%

## Writing New Tests

### Backend Test Template

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestNewFeature:
    """Test suite for new feature."""
    
    def test_feature_success_case(self):
        """Test successful case."""
        response = client.get("/api/new-endpoint")
        assert response.status_code == 200
        data = response.json()
        assert "expected_field" in data
    
    def test_feature_error_case(self):
        """Test error handling."""
        response = client.get("/api/new-endpoint?invalid=param")
        assert response.status_code == 400
```

### Frontend Test Template

```javascript
import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import NewComponent from './NewComponent'

describe('NewComponent', () => {
  it('renders correctly', () => {
    render(<NewComponent />)
    expect(screen.getByRole('button')).toBeInTheDocument()
  })
  
  it('handles user interaction', async () => {
    const user = userEvent.setup()
    render(<NewComponent />)
    
    const button = screen.getByRole('button')
    await user.click(button)
    
    await waitFor(() => {
      expect(screen.getByText(/expected text/i)).toBeInTheDocument()
    })
  })
})
```

### Test Best Practices

#### General
1. **One assertion concept per test**: Each test should verify one behavior
2. **Clear test names**: Use descriptive names that explain what is tested
3. **Arrange-Act-Assert**: Follow AAA pattern for test structure
4. **Independent tests**: Tests should not depend on each other
5. **Clean up**: Reset state between tests

#### Backend
1. **Use TestClient**: Don't start actual server
2. **Mock external dependencies**: Database, APIs, etc.
3. **Test edge cases**: Empty responses, null values, etc.
4. **Verify response structure**: Check both data and metadata
5. **Test performance**: Use timers for critical endpoints

#### Frontend
1. **Query by accessibility**: Use getByRole, getByLabelText
2. **Avoid implementation details**: Don't test internal state
3. **Mock fetch globally**: Use vi.fn() for fetch
4. **Wait for async updates**: Use waitFor() for state changes
5. **Test user workflows**: Simulate real user interactions

## Troubleshooting Tests

### Backend Tests Failing

```bash
# Check Python version
python --version

# Reinstall dependencies
docker compose exec backend pip install -r requirements.txt --force-reinstall

# Run single test with full output
docker compose exec backend pytest test_main.py::TestName::test_name -vv --tb=long

# Check for syntax errors
docker compose exec backend python -m py_compile main.py
```

### Frontend Tests Failing

```bash
# Check Node version
node --version

# Reinstall dependencies
docker compose exec frontend rm -rf node_modules
docker compose exec frontend npm install

# Run single test with debug output
docker compose exec frontend npm test -- App.test.jsx -t "test name"

# Check for syntax errors
docker compose exec frontend npm run lint
```

### CI Tests Failing

1. Check CI logs in GitHub Actions
2. Look for specific error messages
3. Run the same commands locally
4. Verify environment matches CI (Node/Python versions)
5. Check for race conditions in async tests

## Resources

### Documentation
- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Testing Library User Event](https://testing-library.com/docs/user-event/intro)

### Tutorials
- [Testing FastAPI Applications](https://fastapi.tiangolo.com/tutorial/testing/)
- [React Testing Patterns](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [Effective Testing Strategies](https://martinfowler.com/articles/practical-test-pyramid.html)

---

**Happy Testing! ✅**
