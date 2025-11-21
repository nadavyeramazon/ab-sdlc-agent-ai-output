# Backend Test Suite Documentation

## Overview

This directory contains comprehensive backend tests for the FastAPI application using pytest. The test suite ensures full coverage of all API endpoints and validates their behavior.

## Test Coverage

The `test_main.py` file includes **40+ test cases** organized into the following test classes:

### 1. TestHelloEndpoint
Tests for the `/api/hello` endpoint:
- ✅ Successful response (status code 200)
- ✅ JSON structure validation (message + timestamp)
- ✅ Message content verification
- ✅ Timestamp format validation (ISO-8601 with UTC indicator)
- ✅ Timestamp recency check
- ✅ Multiple calls consistency
- ✅ Edge cases (trailing slashes, case sensitivity, query parameters)
- ✅ HTTP method restrictions (POST, PUT, DELETE should fail)

### 2. TestHealthEndpoint
Tests for the `/health` endpoint:
- ✅ Successful response (status code 200)
- ✅ JSON structure validation (status field)
- ✅ Status value verification ("healthy")
- ✅ Multiple calls consistency
- ✅ Edge cases (trailing slashes, case sensitivity, query parameters)
- ✅ HTTP method restrictions (POST, PUT, DELETE should fail)

### 3. TestCORSConfiguration
Tests for CORS middleware:
- ✅ CORS headers presence
- ✅ Frontend origin allowance (http://localhost:3000)

### 4. TestApplicationRoutes
Tests for routing behavior:
- ✅ Non-existent routes return 404
- ✅ Root path handling
- ✅ API prefix without endpoint

### 5. TestResponseHeaders
Tests for HTTP response headers:
- ✅ Content-Type validation (application/json)

### 6. TestEdgeCases
Additional edge cases and boundary conditions:
- ✅ Query parameter handling
- ✅ Concurrent request handling

## Running Tests

### Prerequisites

Install test dependencies:
```bash
cd backend
pip install -r requirements.txt
```

This will install:
- `pytest==7.4.0` - Test framework
- `httpx==0.24.1` - Required for FastAPI TestClient
- `fastapi==0.100.0` - Main application framework
- `uvicorn[standard]==0.23.0` - ASGI server

### Run All Tests

```bash
# From the backend directory
pytest

# Or with verbose output
pytest -v

# Or with even more detail
pytest -vv
```

### Run Specific Test Classes

```bash
# Run only /api/hello endpoint tests
pytest test_main.py::TestHelloEndpoint -v

# Run only /health endpoint tests
pytest test_main.py::TestHealthEndpoint -v

# Run only CORS tests
pytest test_main.py::TestCORSConfiguration -v
```

### Run Specific Test Cases

```bash
# Run a single test
pytest test_main.py::TestHelloEndpoint::test_hello_endpoint_success -v

# Run tests matching a pattern
pytest -k "timestamp" -v
pytest -k "health" -v
```

### Test Coverage Report

To generate a coverage report (requires pytest-cov):

```bash
# Install coverage tool
pip install pytest-cov

# Run tests with coverage
pytest --cov=main --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=main --cov-report=html
```

## Expected Test Results

All tests should pass with output similar to:

```
========================= test session starts ==========================
collected 41 items

test_main.py::TestHelloEndpoint::test_hello_endpoint_success PASSED
test_main.py::TestHelloEndpoint::test_hello_endpoint_status_code PASSED
test_main.py::TestHelloEndpoint::test_hello_endpoint_json_structure PASSED
...
test_main.py::TestEdgeCases::test_concurrent_requests_to_health PASSED

========================= 41 passed in 1.23s ===========================
```

## Test Organization

The tests follow pytest best practices:

1. **Fixtures**: Reusable test client fixture
2. **Classes**: Organized by feature/endpoint
3. **Descriptive Names**: Clear test method names
4. **Assertions**: Multiple assertions per test where appropriate
5. **Edge Cases**: Comprehensive edge case coverage
6. **Documentation**: Docstrings for all test methods

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError: No module named 'main'`:
```bash
# Make sure you're in the backend directory
cd backend
pytest
```

### FastAPI TestClient Issues

If you see errors about TestClient:
```bash
# Make sure httpx is installed
pip install httpx==0.24.1
```

### pytest Not Found

If pytest command is not found:
```bash
# Install pytest
pip install pytest==7.4.0

# Or reinstall all requirements
pip install -r requirements.txt
```

## CI/CD Integration

**Note**: To integrate these tests into the CI pipeline, the `.github/workflows/ci.yml` file should be updated to replace the current health check with:

```yaml
- name: Run pytest tests
  working-directory: ./backend
  run: |
    pytest -v
  continue-on-error: false
```

This would replace the current "Run health check" step in the backend-tests job.

## Test Maintenance

When adding new endpoints or modifying existing ones:

1. Add corresponding test class or methods
2. Verify all HTTP methods are tested
3. Test both success and error cases
4. Validate JSON structure and content
5. Test edge cases (trailing slashes, query params, etc.)
6. Run full test suite before committing

## Contributing

When adding new tests:
- Follow existing naming conventions
- Add descriptive docstrings
- Group related tests in classes
- Include both positive and negative test cases
- Test edge cases and boundary conditions

---

**Test Coverage**: 100% of backend API endpoints  
**Total Tests**: 41 test cases  
**Test Framework**: pytest 7.4.0  
**Last Updated**: 2024-01-21
