# Backend Test Suite

Comprehensive pytest test suite for the FastAPI backend application.

## Overview

This test suite provides comprehensive coverage of the FastAPI backend including:
- Unit tests for individual endpoints
- Integration tests for complete request/response cycles
- CORS configuration tests
- Error handling and edge case tests
- Application configuration tests

## Test Statistics

- **Total Test Files**: 5
- **Test Classes**: 20+
- **Test Functions**: 100+
- **Coverage Target**: >95%

## Running Tests

### Prerequisites

Install test dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest tests/test_api.py
pytest tests/test_cors.py
pytest tests/test_integration.py
pytest tests/test_application.py
```

### Run Specific Test Class

```bash
pytest tests/test_api.py::TestHelloEndpoint
pytest tests/test_api.py::TestHealthEndpoint
```

### Run Specific Test Function

```bash
pytest tests/test_api.py::TestHelloEndpoint::test_hello_endpoint_returns_200
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only CORS tests
pytest -m cors

# Run all except slow tests
pytest -m "not slow"
```

### Run with Coverage Report

```bash
# Terminal report
pytest --cov=. --cov-report=term-missing

# HTML report (opens in browser)
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### Run with Different Verbosity Levels

```bash
# Minimal output
pytest -q

# Verbose output
pytest -v

# Very verbose output (show all test names)
pytest -vv
```

## Test Structure

### Test Files

- **`test_api.py`**: Endpoint-specific tests
  - `TestHelloEndpoint`: Tests for `/api/hello`
  - `TestHealthEndpoint`: Tests for `/health`
  - `TestInvalidEndpoints`: Tests for error cases
  - `TestResponseHeaders`: Tests for HTTP headers
  - `TestEdgeCases`: Edge case and boundary tests

- **`test_cors.py`**: CORS configuration tests
  - `TestCORSConfiguration`: CORS middleware tests
  - `TestCORSEdgeCases`: CORS edge cases

- **`test_integration.py`**: Integration tests
  - `TestFullRequestResponseCycle`: End-to-end tests
  - `TestAPIDocumentation`: OpenAPI/Swagger tests
  - `TestApplicationConfiguration`: App config tests
  - `TestResponseConsistency`: Response consistency tests

- **`test_application.py`**: Application setup tests
  - `TestApplicationSetup`: App initialization tests
  - `TestRouteConfiguration`: Route registration tests
  - `TestMiddlewareConfiguration`: Middleware tests
  - `TestOpenAPIDocumentation`: API doc generation tests

- **`conftest.py`**: Shared fixtures and configuration

### Fixtures

- **`test_app`**: FastAPI application instance (session scope)
- **`client`**: FastAPI TestClient (function scope)
- **`api_headers`**: Standard API headers
- **`mock_datetime`**: Mock datetime for timestamp testing

## Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Individual endpoint functionality
- Response structure validation
- Request method validation
- Header validation
- Edge cases

### Integration Tests (`@pytest.mark.integration`)
- Complete request/response cycles
- Sequential requests
- Error handling flows
- OpenAPI documentation
- Application configuration

### CORS Tests (`@pytest.mark.cors`)
- CORS header validation
- Preflight requests
- Origin validation
- Method/header permissions

## Coverage Goals

| Component | Target Coverage |
|-----------|----------------|
| Endpoints | 100% |
| CORS Config | 100% |
| Error Handling | 100% |
| Documentation | 100% |
| **Overall** | **>95%** |

## Test Examples

### Basic Endpoint Test
```python
def test_hello_endpoint_returns_200(client):
    response = client.get("/api/hello")
    assert response.status_code == 200
```

### Response Validation Test
```python
def test_hello_endpoint_response_structure(client):
    response = client.get("/api/hello")
    data = response.json()
    
    assert "message" in data
    assert "timestamp" in data
    assert isinstance(data["message"], str)
```

### Error Handling Test
```python
def test_invalid_endpoint_returns_404(client):
    response = client.get("/invalid")
    assert response.status_code == 404
    assert "detail" in response.json()
```

### Integration Test
```python
def test_sequential_requests(client):
    response1 = client.get("/health")
    assert response1.status_code == 200
    
    response2 = client.get("/api/hello")
    assert response2.status_code == 200
```

## Continuous Integration

Tests are automatically run in CI/CD pipeline:
- On every push to feature branches
- On pull request creation/update
- Before merge to main branch

CI configuration: `.github/workflows/ci.yml`

## Troubleshooting

### ImportError: No module named 'main'

Make sure you're in the backend directory:
```bash
cd backend
pytest
```

### Tests Fail with CORS Errors

CORS tests may behave differently in TestClient vs real browser. This is expected - the tests verify configuration, not browser behavior.

### Coverage Not Generated

Ensure pytest-cov is installed:
```bash
pip install pytest-cov
```

### Slow Test Execution

Run only fast tests:
```bash
pytest -m "not slow"
```

Or run tests in parallel:
```bash
pip install pytest-xdist
pytest -n auto
```

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Clear Names**: Test names should describe what they test
3. **Arrange-Act-Assert**: Follow AAA pattern
4. **One Assertion Per Concept**: Test one thing at a time
5. **Use Fixtures**: Share setup code via fixtures
6. **Mark Tests**: Use markers for categorization
7. **Mock External Dependencies**: Don't depend on external services
8. **Test Error Cases**: Don't just test happy paths

## Adding New Tests

When adding new endpoints or functionality:

1. Create test class in appropriate file
2. Write tests for success cases
3. Write tests for error cases
4. Write tests for edge cases
5. Add integration tests if needed
6. Update this README if needed

Example:
```python
class TestNewEndpoint:
    @pytest.mark.unit
    def test_new_endpoint_success(self, client):
        response = client.get("/api/new")
        assert response.status_code == 200
    
    @pytest.mark.unit
    def test_new_endpoint_error_handling(self, client):
        response = client.post("/api/new")
        assert response.status_code == 405
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [httpx Documentation](https://www.python-httpx.org/)

## Support

For issues with tests:
1. Check test output for specific error messages
2. Run with `-vv` for detailed output
3. Check pytest.ini configuration
4. Verify all dependencies are installed
5. Review fixture definitions in conftest.py
