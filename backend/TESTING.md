# Backend Testing Guide

Quick guide to running and understanding the backend test suite.

## Quick Start

```bash
# Navigate to backend directory
cd backend

# Install dependencies (including test dependencies)
pip install -r requirements.txt

# Run all tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
# or
start htmlcov/index.html  # Windows
```

## Using Test Runner Scripts

### Unix/Linux/macOS
```bash
chmod +x run_tests.sh
./run_tests.sh
```

### Windows
```cmd
run_tests.bat
```

## Test Categories

### Run Specific Test Categories
```bash
# Unit tests only (fast, isolated tests)
pytest -m unit

# Integration tests only (end-to-end tests)
pytest -m integration

# CORS tests only
pytest -m cors
```

### Run Specific Files
```bash
# API endpoint tests
pytest tests/test_api.py

# CORS configuration tests
pytest tests/test_cors.py

# Integration tests
pytest tests/test_integration.py

# Application setup tests
pytest tests/test_application.py
```

### Run Specific Tests
```bash
# Run specific test class
pytest tests/test_api.py::TestHelloEndpoint

# Run specific test function
pytest tests/test_api.py::TestHelloEndpoint::test_hello_endpoint_returns_200
```

## Understanding Test Output

### Successful Test Run
```
============================= test session starts ==============================
collected 100 items

tests/test_api.py ..................................... [ 35%]
tests/test_application.py .............. [ 49%]
tests/test_cors.py ............. [ 62%]
tests/test_integration.py .......................... [100%]

======================== 100 passed in 2.45s ===============================
```

### Test with Coverage
```
---------- coverage: platform darwin, python 3.11.5 -----------
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
main.py                15      0   100%
-------------------------------------------------
TOTAL                  15      0   100%
```

## Test Structure Overview

```
backend/
├── tests/
│   ├── __init__.py              # Package marker
│   ├── conftest.py              # Shared fixtures
│   ├── test_api.py              # Endpoint tests (56 tests)
│   ├── test_application.py      # App config tests (21 tests)
│   ├── test_cors.py             # CORS tests (13 tests)
│   ├── test_integration.py      # Integration tests (25 tests)
│   └── README.md                # Detailed documentation
├── pytest.ini                   # Pytest configuration
├── .coveragerc                  # Coverage configuration
└── requirements.txt             # Dependencies (includes test tools)
```

## What's Tested

### ✅ All API Endpoints
- `/api/hello` - Hello world endpoint with timestamp
- `/health` - Health check endpoint
- OpenAPI documentation endpoints (`/docs`, `/redoc`)

### ✅ Request/Response Validation
- HTTP status codes (200, 404, 405)
- Response headers (Content-Type, Content-Length)
- JSON response structure
- Timestamp format validation
- Error handling and edge cases

### ✅ CORS Configuration
- CORS middleware setup
- Allowed origins (localhost:3000)
- Preflight requests
- Header/method permissions

### ✅ Application Configuration
- FastAPI app initialization
- Route registration
- Middleware configuration
- OpenAPI schema generation

### ✅ Edge Cases & Error Handling
- Invalid endpoints (404 errors)
- Wrong HTTP methods (405 errors)
- Query parameters handling
- Concurrent requests
- Response consistency

## Coverage Goals

Current Coverage: **~100%** ✅

| Component | Coverage | Status |
|-----------|----------|--------|
| API Endpoints | 100% | ✅ |
| CORS Config | 100% | ✅ |
| App Setup | 100% | ✅ |
| Error Handling | 100% | ✅ |

## Common Commands

```bash
# Run tests with different verbosity
pytest -v              # Verbose
pytest -vv             # Very verbose
pytest -q              # Quiet

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Show test durations
pytest --durations=10

# Generate all report formats
pytest --cov=. --cov-report=html --cov-report=xml --cov-report=term

# Run tests matching pattern
pytest -k "hello"      # Run tests with "hello" in name
pytest -k "not cors"   # Skip CORS tests
```

## Troubleshooting

### Issue: ModuleNotFoundError: No module named 'main'
**Solution:** Make sure you're in the `backend` directory when running tests.
```bash
cd backend
pytest
```

### Issue: pytest: command not found
**Solution:** Install test dependencies.
```bash
pip install -r requirements.txt
```

### Issue: Tests pass locally but fail in CI
**Solution:** Check that CI environment has all dependencies installed and uses correct Python version (3.11+).

### Issue: Coverage report not generated
**Solution:** Ensure pytest-cov is installed.
```bash
pip install pytest-cov
pytest --cov=. --cov-report=html
```

## Writing New Tests

When adding new endpoints or features:

1. Add endpoint tests in `tests/test_api.py`
2. Add integration tests in `tests/test_integration.py`
3. Update OpenAPI tests if schema changes
4. Add CORS tests if CORS config changes
5. Run full test suite: `pytest`
6. Check coverage: `pytest --cov=.`

### Test Template
```python
@pytest.mark.unit
def test_new_feature(client):
    \"\"\"Test description.\"\"\"
    # Arrange
    expected_result = "value"
    
    # Act
    response = client.get("/api/new-endpoint")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["key"] == expected_result
```

## CI/CD Integration

Tests run automatically on:
- Every push to feature branches
- Pull request creation/updates
- Before merge to main

See `.github/workflows/ci.yml` for CI configuration.

## Resources

- [Full Test Documentation](tests/README.md) - Detailed test guide
- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)

## Test Metrics

- **Total Tests:** 115+
- **Test Files:** 5
- **Test Classes:** 20+
- **Code Coverage:** ~100%
- **Average Run Time:** 2-3 seconds

---

**Need Help?** Check the [tests/README.md](tests/README.md) for comprehensive documentation.
