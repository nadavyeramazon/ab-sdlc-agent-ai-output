# Backend Testing Documentation

## Overview

This directory contains comprehensive test coverage for the backend API using pytest and FastAPI TestClient.

## Test Coverage

The test suite (`test_main.py`) provides comprehensive coverage for:

### API Endpoints Tested
- ✅ `/api/hello` - Hello world endpoint with timestamp
- ✅ `/health` - Health check endpoint

### Test Categories

1. **Successful Response Tests**
   - Correct status codes (200)
   - Response structure validation
   - Data type verification
   - Content validation

2. **Error Case Tests**
   - HTTP method restrictions (405 errors)
   - Nonexistent endpoints (404 errors)
   - Case sensitivity validation
   - Trailing slash handling

3. **Edge Case Tests**
   - Multiple consecutive requests
   - Timestamp validation and recency
   - Response consistency (idempotency)
   - API prefix without endpoints

4. **Configuration Tests**
   - CORS middleware configuration
   - Allowed origins validation
   - Content-Type headers

5. **Performance Tests**
   - Response time validation
   - Fast response guarantees (<1s)

### Test Statistics
- **Total Test Cases**: 25+ individual tests
- **Test Classes**: 6 organized test suites
- **Coverage**: Both API endpoints with comprehensive scenarios

## Installation

Install the required test dependencies:

```bash
pip install -r requirements.txt
```

This will install:
- `pytest>=7.4.0` - Testing framework
- `httpx>=0.24.0` - HTTP client for TestClient (required by FastAPI testing)
- `fastapi` and `uvicorn[standard]` - Application dependencies

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Tests with Verbose Output

```bash
pytest -v
```

### Run Tests with Coverage Report

```bash
pytest --cov=main --cov-report=term-missing
```

Note: You'll need to install `pytest-cov` for coverage reports:
```bash
pip install pytest-cov
```

### Run Specific Test Class

```bash
# Test only the hello endpoint
pytest test_main.py::TestHelloEndpoint -v

# Test only the health endpoint
pytest test_main.py::TestHealthEndpoint -v

# Test only error cases
pytest test_main.py::TestAPIErrors -v
```

### Run Specific Test Case

```bash
pytest test_main.py::TestHelloEndpoint::test_hello_success -v
```

### Run Tests Matching Pattern

```bash
# Run all tests with "health" in the name
pytest -k "health" -v

# Run all tests with "error" in the name
pytest -k "error" -v
```

## Test Structure

```
backend/
├── main.py              # FastAPI application
├── test_main.py         # Test suite
├── pytest.ini           # Pytest configuration
├── requirements.txt     # Dependencies (including test deps)
└── TEST_README.md       # This file
```

## Writing New Tests

When adding new endpoints or functionality, follow these patterns:

1. **Create a test class** for each major endpoint or feature:
```python
class TestNewEndpoint:
    """Test suite for /api/new endpoint"""
    
    def test_success_case(self, client):
        response = client.get("/api/new")
        assert response.status_code == 200
```

2. **Use the client fixture** provided in the test file:
```python
def test_my_endpoint(client):
    response = client.get("/my-endpoint")
    # assertions...
```

3. **Test multiple scenarios**:
   - Success cases (200 responses)
   - Error cases (4xx, 5xx responses)
   - Edge cases (empty data, special characters, etc.)
   - Response structure and types

4. **Use descriptive test names** that explain what is being tested:
   - ✅ `test_hello_returns_correct_timestamp_format`
   - ❌ `test_1` or `test_endpoint`

## Continuous Integration

These tests are designed to run in CI/CD pipelines. Ensure:

1. All tests pass before merging PRs
2. No test failures are ignored
3. New features include corresponding tests
4. Tests run in isolation (no side effects)

## Test Best Practices

✅ **DO:**
- Use descriptive test names
- Test one thing per test function
- Use fixtures for common setup
- Test both success and failure paths
- Validate response structure and types

❌ **DON'T:**
- Make tests dependent on each other
- Use hardcoded timeouts (except performance tests)
- Skip tests without good reason
- Test implementation details instead of behavior
- Leave commented-out test code

## Troubleshooting

### Tests fail with "ModuleNotFoundError: No module named 'main'"

Make sure you're running pytest from the `backend/` directory:
```bash
cd backend/
pytest
```

### Tests fail with import errors for FastAPI or httpx

Install dependencies:
```bash
pip install -r requirements.txt
```

### All tests pass but coverage is low

Run with coverage report to identify untested code:
```bash
pip install pytest-cov
pytest --cov=main --cov-report=html
# Open htmlcov/index.html in browser
```

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [TestClient Documentation](https://www.starlette.io/testclient/)
