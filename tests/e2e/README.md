# E2E Tests for Red Greeting Application

This directory contains end-to-end (e2e) tests that verify the complete integration of the frontend and backend services using Docker Compose and curl.

## Overview

The e2e tests ensure that:
- Backend API endpoints are functioning correctly
- Frontend is accessible and serving correct files
- Frontend and backend can communicate properly
- The red theme is implemented throughout the application
- CORS is configured correctly
- Error handling works as expected

## Running the Tests

### Prerequisites

- Docker and Docker Compose installed
- Bash shell (Linux, macOS, or WSL on Windows)
- curl command-line tool

### Execute the Test Suite

```bash
# Make the script executable
chmod +x tests/e2e/test_e2e.sh

# Run the tests
./tests/e2e/test_e2e.sh
```

Or from the project root:

```bash
bash tests/e2e/test_e2e.sh
```

## Test Categories

### Backend API Tests (Tests 1-9)

1. **Health Check Endpoint** - Verifies `/health` returns healthy status
2. **Root Endpoint** - Verifies `/` returns welcome message
3. **POST /greet** - Tests greeting with JSON body
4. **GET /greet/{name}** - Tests greeting with path parameter
5. **POST /howdy** - Tests howdy greeting with JSON body
6. **GET /howdy/{name}** - Tests howdy greeting with path parameter
7. **Invalid POST (empty name)** - Verifies validation for empty names
8. **Invalid POST (whitespace)** - Verifies validation for whitespace-only names
9. **Red Theme Verification** - Ensures "red-themed" is mentioned in responses

### Frontend Tests (Tests 10-15)

10. **Frontend Accessibility** - Verifies frontend is accessible on port 80
11. **Correct Title** - Checks for "Red Greeting App" in HTML title
12. **CSS Inclusion** - Verifies styles.css is linked
13. **JavaScript Inclusion** - Verifies app.js is linked
14. **CSS Accessibility** - Ensures CSS file is served correctly
15. **JavaScript Accessibility** - Ensures JS file is served correctly

### Integration Tests (Tests 16-20)

16. **CORS Headers** - Verifies CORS headers are present
17. **Health Check JSON Structure** - Validates required fields in health response
18. **API Documentation** - Ensures /docs is accessible
19. **OpenAPI JSON** - Verifies /openapi.json is accessible
20. **Service Name Consistency** - Checks service name matches red theme

## Test Output

The test script provides colored output:
- 🟢 **Green** - Test passed
- 🔴 **Red** - Test failed
- 🔵 **Blue** - Information messages

Example output:
```
========================================
  Red Greeting App - E2E Test Suite
========================================

Step 1: Building and starting services with docker-compose...
Services started successfully

Step 2: Waiting for backend service to be ready...
Backend is ready! (attempt 5/30)

Step 3: Running Backend API Tests
==========================================

Test 1: Health check endpoint... ✓ PASSED
Test 2: Root endpoint... ✓ PASSED
...

========================================
  Test Summary
========================================
Tests Passed: 20
Tests Failed: 0
Total Tests: 20

========================================
  ✓ ALL TESTS PASSED!
========================================
```

## Continuous Integration

These tests are automatically run in the GitHub Actions CI pipeline on:
- Push to `main` branch
- Push to `feature/*` branches
- Pull requests to `main`

See `.github/workflows/ci.yml` for the CI configuration.

## Troubleshooting

### Tests Failing

1. **Check Docker Services**:
   ```bash
   docker compose ps
   docker compose logs backend
   docker compose logs frontend
   ```

2. **Manual Testing**:
   ```bash
   # Start services
   docker compose up -d
   
   # Test backend
   curl http://localhost:8000/health
   
   # Test frontend
   curl http://localhost:80
   ```

3. **Clean Start**:
   ```bash
   docker compose down -v
   docker compose up -d --build
   ```

### Port Conflicts

If ports 80 or 8000 are already in use:

1. Stop the conflicting services
2. Or modify `docker-compose.yml` to use different ports

### Permission Issues

If you get "Permission denied" when running the script:

```bash
chmod +x tests/e2e/test_e2e.sh
```

## Writing New Tests

To add new e2e tests:

1. Add test cases to `test_e2e.sh`
2. Follow the existing pattern:
   ```bash
   echo -n "Test N: Description... "
   RESPONSE=$(curl -s -w "\n%{http_code}" "URL")
   HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
   
   if [ "$HTTP_CODE" -eq 200 ]; then
       test_result
   else
       echo -e "${ERROR_COLOR}✗ FAILED${RESET_COLOR}"
       ((TESTS_FAILED++))
   fi
   ```
3. Update the test count and description in this README

## Related Documentation

- [Main README](../../README.md) - Project overview
- [Backend Tests](../../backend/tests/) - Unit and integration tests
- [CI Workflow](../../.github/workflows/ci.yml) - Automated testing setup
