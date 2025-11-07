# Backend Test Suite

## Overview

Comprehensive test suite for the Green Theme Backend API built with FastAPI. This test suite provides 100% endpoint coverage with unit tests, integration tests, and error handling tests.

## Test Structure

```
backend/
├── tests/
│   ├── __init__.py          # Test package initialization
│   ├── conftest.py          # Pytest configuration and fixtures
│   └── test_main.py         # Main test suite
├── pytest.ini               # Pytest configuration
├── .coveragerc             # Coverage configuration
├── test_requirements.txt   # Test dependencies
└── requirements.txt        # Updated with test dependencies
```

## Test Coverage

### Endpoints Tested (5/5)

1. **GET /** - Root endpoint
   - Status code validation
   - Response structure
   - Welcome message
   - Endpoints list

2. **GET /health** - Health check
   - Status code validation
   - Health status
   - Timestamp validation
   - Multiple calls consistency

3. **POST /message** - Message processing
   - Valid input handling
   - Response structure
   - Message echoing
   - Timestamp validation
   - Various input types (parametrized)
   - Empty message validation (400)
   - Whitespace validation (400)
   - Missing field validation (422)
   - Invalid type validation (422)
   - Null value validation (422)

4. **GET /data** - Sample data
   - Status code validation
   - Response structure
   - Data list validation
   - Count accuracy
   - Item structure validation
   - Expected data content
   - Timestamp validation

5. **GET /info** - Application info
   - Status code validation
   - Response structure
   - Correct values
   - Features list
   - Expected features

### Additional Test Categories

- **CORS Configuration Tests**
  - CORS headers presence
  - OPTIONS preflight handling

- **Response Model Tests**
  - Pydantic model validation
  - Response schema compliance

- **Error Handling Tests**
  - 404 for invalid endpoints
  - 405 for invalid methods
  - 422 for malformed JSON

- **Integration Tests**
  - Full API workflow
  - Concurrent requests

## Running Tests

### Install Dependencies

```bash
cd backend
pip install -r test_requirements.txt
```

Or install from main requirements:

```bash
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

### Run with Coverage Report

```bash
pytest --cov=. --cov-report=html --cov-report=term
```

### Run Specific Test Class

```bash
pytest tests/test_main.py::TestMessageEndpoint -v
```

### Run Specific Test

```bash
pytest tests/test_main.py::TestMessageEndpoint::test_message_empty_string_returns_400 -v
```

### Run with Markers

```bash
# Run only integration tests
pytest -m integration

# Run only unit tests
pytest -m unit
```

## Coverage Reports

After running tests with coverage, view reports:

### Terminal Report

Displayed automatically after test run with `--cov-report=term`

### HTML Report

```bash
# Generate report
pytest --cov=. --cov-report=html

# Open in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### XML Report (for CI/CD)

```bash
pytest --cov=. --cov-report=xml
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Backend

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r test_requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest --cov=. --cov-report=xml --cov-report=term
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./backend/coverage.xml
```

### Docker Testing

```bash
# Build test image
docker build -t backend-test -f Dockerfile.test .

# Run tests in container
docker run --rm backend-test pytest
```

## Test Statistics

- **Total Tests**: 50+
- **Endpoint Coverage**: 100% (5/5 endpoints)
- **Test Categories**: 9 test classes
- **Parametrized Tests**: Multiple input variations
- **Error Scenarios**: Comprehensive validation and error cases
- **Integration Tests**: Full workflow and concurrent request handling

## Test Quality Features

✅ **Comprehensive Coverage**: All endpoints tested
✅ **Input Validation**: Edge cases and invalid inputs
✅ **Error Handling**: HTTP error codes (400, 404, 405, 422)
✅ **Type Safety**: Pydantic model validation
✅ **Integration**: End-to-end workflow testing
✅ **CORS**: Middleware configuration testing
✅ **Fixtures**: Reusable test data and clients
✅ **Parametrization**: Multiple input scenarios
✅ **Documentation**: Clear test descriptions
✅ **Coverage Reporting**: HTML, XML, and terminal reports

## Maintenance

### Adding New Tests

1. Create test class in `tests/test_main.py`
2. Use descriptive names: `test_<what>_<condition>_<result>`
3. Add docstrings explaining test purpose
4. Use fixtures for common setup
5. Parametrize similar tests
6. Update this README

### Best Practices

- Keep tests isolated and independent
- Use fixtures for common setup
- Test both success and failure cases
- Validate response structure and data
- Include edge cases and boundary conditions
- Maintain test coverage above 80%
- Document complex test scenarios

## Troubleshooting

### Import Errors

If you encounter import errors:

```python
# Ensure path is added in conftest.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```

### Coverage Not Working

Ensure `.coveragerc` and `pytest.ini` are in the backend directory.

### Tests Not Discovered

Check that:
- Test files start with `test_`
- Test functions start with `test_`
- Test classes start with `Test`
- `__init__.py` exists in tests directory

## Contact

For questions or issues with the test suite, please open an issue in the repository.
