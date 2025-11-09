#!/bin/bash

# E2E Test Script for Red Greeting Application
# This script tests the full stack using docker-compose and curl

set -e  # Exit on any error

ECHO_COLOR="\033[1;32m"  # Green for success
ERROR_COLOR="\033[1;31m"  # Red for errors
INFO_COLOR="\033[1;34m"   # Blue for info
RESET_COLOR="\033[0m"

echo -e "${INFO_COLOR}========================================${RESET_COLOR}"
echo -e "${INFO_COLOR}  Red Greeting App - E2E Test Suite${RESET_COLOR}"
echo -e "${INFO_COLOR}========================================${RESET_COLOR}"
echo ""

# Configuration
BACKEND_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:80"
MAX_RETRIES=30
RETRY_DELAY=2

# Cleanup function
cleanup() {
    echo -e "${INFO_COLOR}Cleaning up...${RESET_COLOR}"
    docker compose down -v 2>/dev/null || true
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Test result function
test_result() {
    if [ $? -eq 0 ]; then
        echo -e "${ECHO_COLOR}✓ PASSED${RESET_COLOR}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${ERROR_COLOR}✗ FAILED${RESET_COLOR}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

echo -e "${INFO_COLOR}Step 1: Building and starting services with docker-compose...${RESET_COLOR}"
docker compose down -v 2>/dev/null || true
docker compose up -d --build

if [ $? -ne 0 ]; then
    echo -e "${ERROR_COLOR}Failed to start services with docker-compose${RESET_COLOR}"
    exit 1
fi

echo -e "${ECHO_COLOR}Services started successfully${RESET_COLOR}"
echo ""

echo -e "${INFO_COLOR}Step 2: Waiting for backend service to be ready...${RESET_COLOR}"
for i in $(seq 1 $MAX_RETRIES); do
    if curl -f -s "${BACKEND_URL}/health" > /dev/null 2>&1; then
        echo -e "${ECHO_COLOR}Backend is ready! (attempt $i/$MAX_RETRIES)${RESET_COLOR}"
        break
    fi
    
    if [ $i -eq $MAX_RETRIES ]; then
        echo -e "${ERROR_COLOR}Backend failed to start after $MAX_RETRIES attempts${RESET_COLOR}"
        echo -e "${INFO_COLOR}Backend logs:${RESET_COLOR}"
        docker compose logs backend
        exit 1
    fi
    
    echo "Waiting for backend... (attempt $i/$MAX_RETRIES)"
    sleep $RETRY_DELAY
done
echo ""

echo -e "${INFO_COLOR}Step 3: Running Backend API Tests${RESET_COLOR}"
echo "=========================================="
echo ""

# Test 1: Health Check Endpoint
echo -n "Test 1: Health check endpoint... "
RESPONSE=$(curl -s -w "\n%{http_code}" "${BACKEND_URL}/health")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    if echo "$BODY" | grep -q '"status":"healthy"'; then
        test_result
    else
        echo -e "${ERROR_COLOR}✗ FAILED - Invalid response body${RESET_COLOR}"
        echo "Response: $BODY"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${ERROR_COLOR}✗ FAILED - HTTP $HTTP_CODE${RESET_COLOR}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 2: Root Endpoint
echo -n "Test 2: Root endpoint... "
RESPONSE=$(curl -s -w "\n%{http_code}" "${BACKEND_URL}/")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    if echo "$BODY" | grep -q '"message"'; then
        test_result
    else
        echo -e "${ERROR_COLOR}✗ FAILED - Invalid response body${RESET_COLOR}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${ERROR_COLOR}✗ FAILED - HTTP $HTTP_CODE${RESET_COLOR}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3: POST /greet endpoint
echo -n "Test 3: POST /greet endpoint... "
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${BACKEND_URL}/greet" \
    -H "Content-Type: application/json" \
    -d '{"name":"Alice"}')
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    if echo "$BODY" | grep -q 'Alice'; then
        test_result
    else
        echo -e "${ERROR_COLOR}✗ FAILED - Name not in response${RESET_COLOR}"
        echo "Response: $BODY"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${ERROR_COLOR}✗ FAILED - HTTP $HTTP_CODE${RESET_COLOR}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 4: GET /greet/{name} endpoint
echo -n "Test 4: GET /greet/{name} endpoint... "
RESPONSE=$(curl -s -w "\n%{http_code}" "${BACKEND_URL}/greet/Bob")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    if echo "$BODY" | grep -q 'Bob'; then
        test_result
    else
        echo -e "${ERROR_COLOR}✗ FAILED - Name not in response${RESET_COLOR}"
        echo "Response: $BODY"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${ERROR_COLOR}✗ FAILED - HTTP $HTTP_CODE${RESET_COLOR}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 5: POST /howdy endpoint
echo -n "Test 5: POST /howdy endpoint... "
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${BACKEND_URL}/howdy" \
    -H "Content-Type: application/json" \
    -d '{"name":"Charlie"}')
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    if echo "$BODY" | grep -q 'Howdy'; then
        test_result
    else
        echo -e "${ERROR_COLOR}✗ FAILED - Howdy not in response${RESET_COLOR}"
        echo "Response: $BODY"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${ERROR_COLOR}✗ FAILED - HTTP $HTTP_CODE${RESET_COLOR}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 6: GET /howdy/{name} endpoint
echo -n "Test 6: GET /howdy/{name} endpoint... "
RESPONSE=$(curl -s -w "\n%{http_code}" "${BACKEND_URL}/howdy/Dave")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    if echo "$BODY" | grep -q 'Howdy' && echo "$BODY" | grep -q 'Dave'; then
        test_result
    else
        echo -e "${ERROR_COLOR}✗ FAILED - Invalid response${RESET_COLOR}"
        echo "Response: $BODY"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${ERROR_COLOR}✗ FAILED - HTTP $HTTP_CODE${RESET_COLOR}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 7: Invalid POST request (empty name) - Expects 422 due to Pydantic validation
echo -n "Test 7: Invalid POST request (empty name)... "
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${BACKEND_URL}/greet" \
    -H "Content-Type: application/json" \
    -d '{"name":""}')
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" -eq 422 ]; then
    test_result
else
    echo -e "${ERROR_COLOR}✗ FAILED - Expected HTTP 422, got $HTTP_CODE${RESET_COLOR}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 8: Invalid POST request (whitespace only) - Custom validation returns 400
echo -n "Test 8: Invalid POST request (whitespace only)... "
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${BACKEND_URL}/greet" \
    -H "Content-Type: application/json" \
    -d '{"name":"   "}')
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" -eq 400 ]; then
    test_result
else
    echo -e "${ERROR_COLOR}✗ FAILED - Expected HTTP 400, got $HTTP_CODE${RESET_COLOR}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 9: Red theme verification in greeting response
echo -n "Test 9: Red theme message in greeting... "
RESPONSE=$(curl -s "${BACKEND_URL}/greet/TestUser")
if echo "$RESPONSE" | grep -q 'red-themed'; then
    test_result
else
    echo -e "${ERROR_COLOR}✗ FAILED - Red theme not mentioned${RESET_COLOR}"
    echo "Response: $RESPONSE"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

echo ""
echo -e "${INFO_COLOR}Step 4: Running Frontend Tests${RESET_COLOR}"
echo "=========================================="
echo ""

# Test 10: Frontend accessibility
echo -n "Test 10: Frontend accessible... "
RESPONSE=$(curl -s -w "\n%{http_code}" "${FRONTEND_URL}")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    if echo "$BODY" | grep -q 'Red Greeting'; then
        test_result
    else
        echo -e "${ERROR_COLOR}✗ FAILED - Red Greeting not found in HTML${RESET_COLOR}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${ERROR_COLOR}✗ FAILED - HTTP $HTTP_CODE${RESET_COLOR}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 11: Frontend has correct title
echo -n "Test 11: Frontend has correct title... "
HTML=$(curl -s "${FRONTEND_URL}")
if echo "$HTML" | grep -q '<title>Red Greeting App</title>'; then
    test_result
else
    echo -e "${ERROR_COLOR}✗ FAILED - Title not found or incorrect${RESET_COLOR}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 12: Frontend includes CSS file
echo -n "Test 12: Frontend includes CSS... "
HTML=$(curl -s "${FRONTEND_URL}")
if echo "$HTML" | grep -q 'styles.css'; then
    test_result
else
    echo -e "${ERROR_COLOR}✗ FAILED - CSS link not found${RESET_COLOR}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 13: Frontend includes JavaScript file
echo -n "Test 13: Frontend includes JavaScript... "
HTML=$(curl -s "${FRONTEND_URL}")
if echo "$HTML" | grep -q 'app.js'; then
    test_result
else
    echo -e "${ERROR_COLOR}✗ FAILED - JavaScript link not found${RESET_COLOR}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 14: CSS file accessible
echo -n "Test 14: CSS file accessible... "
RESPONSE=$(curl -s -w "\n%{http_code}" "${FRONTEND_URL}/styles.css")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    if echo "$BODY" | grep -q 'Red Theme'; then
        test_result
    else
        echo -e "${ERROR_COLOR}✗ FAILED - CSS content incorrect${RESET_COLOR}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${ERROR_COLOR}✗ FAILED - HTTP $HTTP_CODE${RESET_COLOR}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 15: JavaScript file accessible
echo -n "Test 15: JavaScript file accessible... "
RESPONSE=$(curl -s -w "\n%{http_code}" "${FRONTEND_URL}/app.js")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    if echo "$BODY" | grep -q 'Red Greeting'; then
        test_result
    else
        echo -e "${ERROR_COLOR}✗ FAILED - JavaScript content incorrect${RESET_COLOR}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${ERROR_COLOR}✗ FAILED - HTTP $HTTP_CODE${RESET_COLOR}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

echo ""
echo -e "${INFO_COLOR}Step 5: Running Integration Tests${RESET_COLOR}"
echo "=========================================="
echo ""

# Test 16: CORS headers present (with Origin header to trigger CORS)
echo -n "Test 16: CORS headers present... "
HEADERS=$(curl -s -D - -o /dev/null -H "Origin: http://localhost:3000" "${BACKEND_URL}/health")
if echo "$HEADERS" | grep -qi 'access-control-allow-origin'; then
    test_result
else
    echo -e "${ERROR_COLOR}✗ FAILED - CORS headers not found${RESET_COLOR}"
    echo "Headers received:"
    echo "$HEADERS"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 17: Health check returns correct structure
echo -n "Test 17: Health check JSON structure... "
RESPONSE=$(curl -s "${BACKEND_URL}/health")
if echo "$RESPONSE" | grep -q '"status"' && \
   echo "$RESPONSE" | grep -q '"service"' && \
   echo "$RESPONSE" | grep -q '"version"'; then
    test_result
else
    echo -e "${ERROR_COLOR}✗ FAILED - Missing required fields${RESET_COLOR}"
    echo "Response: $RESPONSE"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 18: API Documentation accessible
echo -n "Test 18: API documentation accessible... "
RESPONSE=$(curl -s -w "\n%{http_code}" "${BACKEND_URL}/docs")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" -eq 200 ]; then
    test_result
else
    echo -e "${ERROR_COLOR}✗ FAILED - HTTP $HTTP_CODE${RESET_COLOR}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 19: OpenAPI JSON accessible
echo -n "Test 19: OpenAPI JSON accessible... "
RESPONSE=$(curl -s -w "\n%{http_code}" "${BACKEND_URL}/openapi.json")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    if echo "$BODY" | grep -q 'openapi'; then
        test_result
    else
        echo -e "${ERROR_COLOR}✗ FAILED - Invalid OpenAPI response${RESET_COLOR}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${ERROR_COLOR}✗ FAILED - HTTP $HTTP_CODE${RESET_COLOR}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 20: Service name consistency
echo -n "Test 20: Service name matches theme... "
RESPONSE=$(curl -s "${BACKEND_URL}/health")
if echo "$RESPONSE" | grep -q 'red-greeting'; then
    test_result
else
    echo -e "${ERROR_COLOR}✗ FAILED - Service name doesn't match red theme${RESET_COLOR}"
    echo "Response: $RESPONSE"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

echo ""
echo -e "${INFO_COLOR}========================================${RESET_COLOR}"
echo -e "${INFO_COLOR}  Test Summary${RESET_COLOR}"
echo -e "${INFO_COLOR}========================================${RESET_COLOR}"
echo -e "${ECHO_COLOR}Tests Passed: $TESTS_PASSED${RESET_COLOR}"
echo -e "${ERROR_COLOR}Tests Failed: $TESTS_FAILED${RESET_COLOR}"
echo -e "Total Tests: $((TESTS_PASSED + TESTS_FAILED))"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${ECHO_COLOR}========================================${RESET_COLOR}"
    echo -e "${ECHO_COLOR}  ✓ ALL TESTS PASSED!${RESET_COLOR}"
    echo -e "${ECHO_COLOR}========================================${RESET_COLOR}"
    exit 0
else
    echo -e "${ERROR_COLOR}========================================${RESET_COLOR}"
    echo -e "${ERROR_COLOR}  ✗ SOME TESTS FAILED${RESET_COLOR}"
    echo -e "${ERROR_COLOR}========================================${RESET_COLOR}"
    
    echo -e "${INFO_COLOR}Showing service logs for debugging...${RESET_COLOR}"
    echo -e "${INFO_COLOR}Backend logs:${RESET_COLOR}"
    docker compose logs backend | tail -n 50
    echo ""
    echo -e "${INFO_COLOR}Frontend logs:${RESET_COLOR}"
    docker compose logs frontend | tail -n 20
    
    exit 1
fi
