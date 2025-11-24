# Backend Test Suite Documentation

## Overview

This directory contains comprehensive backend tests for the Task Manager FastAPI application using pytest. The test suite includes both traditional unit tests and property-based tests using Hypothesis to ensure correctness across all possible inputs.

## Test Philosophy

The test suite uses a dual testing approach:

- **Unit Tests**: Verify specific examples, edge cases, and API behavior
- **Property-Based Tests**: Verify universal properties that should hold across all inputs using Hypothesis

Property-based tests run 100+ iterations with randomly generated data to catch edge cases that manual testing might miss.

## Test Structure

Tests are organized in the `tests/` directory following Python best practices:

```
backend/
├── tests/
│   ├── __init__.py
│   ├── test_main.py              # API endpoint tests with property-based tests
│   └── test_task_repository.py   # Repository layer tests with property-based tests
├── main.py
├── task_repository.py
└── pytest.ini                     # pytest configuration
```

## Test Coverage

### test_main.py

API endpoint tests organized into test classes:

#### Unit Tests

**Task CRUD Operations:**
- ✅ GET /api/tasks returns all tasks
- ✅ GET /api/tasks returns empty list when no tasks exist
- ✅ POST /api/tasks creates new task with valid data
- ✅ POST /api/tasks rejects empty title (422)
- ✅ POST /api/tasks rejects whitespace-only title (422)
- ✅ POST /api/tasks rejects title exceeding 200 characters (422)
- ✅ GET /api/tasks/{id} returns specific task
- ✅ GET /api/tasks/{id} returns 404 for non-existent task
- ✅ PUT /api/tasks/{id} updates task with valid data
- ✅ PUT /api/tasks/{id} rejects empty title (422)
- ✅ PUT /api/tasks/{id} returns 404 for non-existent task
- ✅ DELETE /api/tasks/{id} removes task (204)
- ✅ DELETE /api/tasks/{id} returns 404 for non-existent task

**Health Endpoint:**
- ✅ GET /health returns healthy status

#### Property-Based Tests

Each property test runs 100+ iterations with randomly generated data:

**Property 1: Task creation persistence**
- *For any* valid task, creating it should make it retrievable
- Validates: Requirements 1.1, 1.4

**Property 2: Empty title rejection**
- *For any* whitespace-only string, task creation should fail with 422
- Validates: Requirements 1.2

**Property 3: Task retrieval completeness**
- *For any* set of tasks in storage, GET /api/tasks returns all of them
- Validates: Requirements 2.1

**Property 4: Completion toggle idempotence**
- *For any* task, toggling completion twice returns to original state
- Validates: Requirements 3.1, 3.3

**Property 5: Delete operation removes task**
- *For any* task, after deletion it should not be retrievable
- Validates: Requirements 4.1, 4.2

**Property 6: Update preserves identity**
- *For any* task update, ID and created_at should remain unchanged
- Validates: Requirements 5.2, 5.4

**Property 7: Invalid update rejection**
- *For any* whitespace-only title update, should fail with 422
- Validates: Requirements 5.3

**Property 8: RESTful status codes**
- *For any* operation, correct HTTP status codes are returned
- Validates: Requirements 6.2, 6.3, 6.4, 6.5

### test_task_repository.py

Repository layer tests:

#### Unit Tests
- ✅ Repository initialization
- ✅ Create task with valid data
- ✅ Get all tasks
- ✅ Get task by ID
- ✅ Update task
- ✅ Delete task
- ✅ File persistence operations

#### Property-Based Tests

**Property 9: Persistence across restarts**
- *For any* set of tasks, restarting the repository should preserve all data
- Validates: Requirements 7.1, 7.3

## Running Tests

### Prerequisites

Install test dependencies:
```bash
cd backend
pip install -r requirements.txt
```

This will install:
- `pytest==7.4.0` - Test framework
- `pytest-cov==4.1.0` - Coverage reporting
- `hypothesis==6.92.0` - Property-based testing library
- `httpx==0.24.1` - Required for FastAPI TestClient
- `fastapi==0.100.0` - Main application framework
- `uvicorn[standard]==0.23.0` - ASGI server
- `pydantic==2.0+` - Data validation

### Run All Tests

```bash
# From the backend directory
pytest

# Or with verbose output
pytest -v

# Or with even more detail
pytest -vv
```

### Run Specific Test Files

```bash
# Run only API endpoint tests
pytest tests/test_main.py -v

# Run only repository tests
pytest tests/test_task_repository.py -v
```

### Run Specific Test Cases

```bash
# Run a single test
pytest tests/test_main.py::TestTaskAPIEndpoints::test_post_task_valid_data -v

# Run tests matching a pattern
pytest -k "property" -v          # Run all property-based tests
pytest -k "create" -v            # Run all creation tests
pytest -k "delete" -v            # Run all deletion tests
```

### Run Only Property-Based Tests

```bash
# Run all property tests
pytest -k "property" -v

# Run specific property test
pytest tests/test_main.py::TestTaskCreationProperties::test_property_empty_title_rejection -v
```

### Test Coverage Report

```bash
# Run tests with coverage
pytest --cov=. --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=. --cov-report=html

# View HTML report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Expected Test Results

All tests should pass with output similar to:

```
========================= test session starts ==========================
collected 30+ items

test_main.py::test_get_all_tasks_empty PASSED
test_main.py::test_create_task PASSED
test_main.py::test_property_task_creation_persistence PASSED
test_main.py::test_property_empty_title_rejection PASSED
...
test_task_repository.py::test_property_persistence_across_restarts PASSED

========================= 30+ passed in 2.5s ===========================
```

Property-based tests will show additional output indicating the number of examples tested:

```
test_main.py::test_property_task_creation_persistence PASSED
  Hypothesis: 100 examples generated
```

## Property-Based Testing with Hypothesis

### What is Property-Based Testing?

Property-based testing verifies that certain properties hold true across all possible inputs, rather than testing specific examples. Hypothesis automatically generates test cases to find edge cases.

### How It Works

1. Define a property that should always be true
2. Hypothesis generates random test data
3. The property is tested with 100+ different inputs
4. If a failure is found, Hypothesis minimizes the failing example
5. Failing examples are saved and replayed on subsequent runs

### Example Property Test

```python
from hypothesis import given, strategies as st

@given(st.text(min_size=1, max_size=200))
def test_property_valid_titles_accepted(title):
    """Any non-empty title should be accepted"""
    response = client.post("/api/tasks", json={"title": title.strip()})
    if title.strip():
        assert response.status_code == 201
    else:
        assert response.status_code == 422
```

### Hypothesis Features Used

- **Strategies**: Define the shape of random data (text, integers, lists, etc.)
- **Shrinking**: Automatically simplifies failing examples
- **Example Database**: Stores failing examples in `.hypothesis/examples/`
- **Deterministic**: Same seed produces same test data

### Benefits

- ✅ Catches edge cases developers don't think of
- ✅ Tests thousands of inputs automatically
- ✅ Provides mathematical confidence in correctness
- ✅ Complements traditional unit tests

## Test Organization

The tests follow pytest and property-based testing best practices:

1. **Fixtures**: Reusable test client and repository fixtures
2. **Descriptive Names**: Clear test method names with `test_property_` prefix for property tests
3. **Property Comments**: Each property test includes a comment linking to the design document
4. **Assertions**: Multiple assertions per test where appropriate
5. **Edge Cases**: Comprehensive edge case coverage via property tests
6. **Documentation**: Docstrings for all test methods
7. **Hypothesis Settings**: Configured for 100+ examples per property test

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError`:
```bash
# Make sure you're in the backend directory
cd backend
pytest
```

### Hypothesis Errors

If you see errors about Hypothesis:
```bash
# Install hypothesis
pip install hypothesis==6.92.0
```

### Property Test Failures

When a property test fails:

1. **Review the counterexample**: Hypothesis shows the failing input
2. **Check if it's a bug**: Does the code violate the property?
3. **Check if it's a test issue**: Is the property correctly specified?
4. **Replay the failure**: Hypothesis saves failing examples in `.hypothesis/examples/`

Example failure output:
```
Falsifying example: test_property_example(
    title='  '  # Whitespace-only title
)
```

### Clearing Hypothesis Cache

If you need to clear saved examples:
```bash
rm -rf .hypothesis/
```

### pytest Not Found

If pytest command is not found:
```bash
# Install pytest
pip install pytest==7.4.0

# Or reinstall all requirements
pip install -r requirements.txt
```

### Data Persistence Issues

If tests fail due to file conflicts:
```bash
# Clean up test data
rm -rf data/tasks.json

# Or use a test-specific data directory
# (tests should handle this automatically)
```

## CI/CD Integration

The tests are integrated into the GitHub Actions CI pipeline:

```yaml
- name: Run pytest tests
  working-directory: ./backend
  run: |
    pytest -v
```

All property-based tests run with 100+ iterations in CI to ensure comprehensive coverage.

## Test Maintenance

When adding new features:

1. **Update Requirements**: Add acceptance criteria to `requirements.md`
2. **Define Properties**: Add correctness properties to `design.md`
3. **Write Property Tests**: Implement property-based tests for each property
4. **Write Unit Tests**: Add specific example tests
5. **Verify Coverage**: Ensure all endpoints and edge cases are tested
6. **Run Full Suite**: `pytest -v` before committing

### Adding Property-Based Tests

When adding a new property test:

1. Reference the design document property in a comment:
   ```python
   # Feature: task-manager-app, Property 1: Task creation persistence
   # Validates: Requirements 1.1, 1.4
   ```

2. Use appropriate Hypothesis strategies:
   ```python
   from hypothesis import given, strategies as st
   
   @given(st.text(min_size=1, max_size=200))
   def test_property_example(title):
       # Test implementation
   ```

3. Configure for 100+ examples:
   ```python
   from hypothesis import settings
   
   @settings(max_examples=100)
   @given(...)
   def test_property_example(...):
       # Test implementation
   ```

## Contributing

When adding new tests:
- Follow existing naming conventions (`test_property_` for property tests)
- Add descriptive docstrings
- Include property references in comments
- Test both success and error cases
- Use property-based tests for universal properties
- Use unit tests for specific examples
- Run full test suite before committing

## Resources

- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [Property-Based Testing Guide](https://hypothesis.works/articles/what-is-property-based-testing/)
- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

---

**Test Coverage**: Full API and repository coverage  
**Total Tests**: 30+ test cases (unit + property-based)  
**Test Framework**: pytest 7.4.0 + Hypothesis 6.92.0  
**Property Tests**: 9 correctness properties with 100+ examples each  
**Last Updated**: 2024-01-23
