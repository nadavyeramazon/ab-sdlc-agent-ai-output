#!/bin/bash
# Acceptance Test Script for Green Theme Fullstack Application

set -e  # Exit on error

echo "=================================================="
echo "  Green Theme Fullstack - Acceptance Tests"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counter for tests
PASSED=0
FAILED=0

pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
    ((PASSED++))
}

fail() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    ((FAILED++))
}

warn() {
    echo -e "${YELLOW}⚠️  WARN${NC}: $1"
}

info() {
    echo -e "ℹ️  $1"
}

# 1. Start services
info "Starting services with docker compose..."
docker compose up -d --build

if [ $? -ne 0 ]; then
    fail "docker compose up failed"
    exit 1
fi
pass "Services started successfully"

# 2. Wait for startup
info "Waiting for services to initialize (15 seconds)..."
sleep 15

# 3. Check service status
info "Checking service status..."
SERVICE_STATUS=$(docker compose ps --format json)
if echo "$SERVICE_STATUS" | grep -q '"State":"running"'; then
    pass "Services are running"
else
    fail "Services not running properly"
    docker compose ps
fi

# 4. Test backend health
info "Testing backend health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
if [[ $HEALTH_RESPONSE == *'"status":"healthy"'* ]]; then
    pass "Health check successful"
else
    fail "Health check failed. Response: $HEALTH_RESPONSE"
fi

# 5. Test backend API
info "Testing backend API endpoint..."
API_RESPONSE=$(curl -s http://localhost:8000/api/hello)
if [[ $API_RESPONSE == *'"message":"Hello World from Backend!"'* ]]; then
    pass "API message correct"
else
    fail "API message incorrect. Response: $API_RESPONSE"
fi

# 6. Validate timestamp format
info "Validating timestamp format..."
TIMESTAMP=$(echo $API_RESPONSE | grep -oP '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z')
if [ -n "$TIMESTAMP" ]; then
    pass "Timestamp format valid (ISO-8601): $TIMESTAMP"
else
    fail "Timestamp format invalid. Response: $API_RESPONSE"
fi

# 7. Test frontend accessibility
info "Testing frontend accessibility..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ "$FRONTEND_STATUS" == "200" ]; then
    pass "Frontend accessible (HTTP 200)"
else
    fail "Frontend not accessible. Status: $FRONTEND_STATUS"
fi

# 8. Test CORS headers
info "Testing CORS configuration..."
CORS_RESPONSE=$(curl -s -H "Origin: http://localhost:3000" -v http://localhost:8000/api/hello 2>&1)
if echo "$CORS_RESPONSE" | grep -qi "access-control-allow-origin"; then
    pass "CORS headers present"
else
    warn "CORS headers not detected in response"
fi

# 9. Test performance
info "Testing API response time..."
START_TIME=$(date +%s%3N)
curl -s http://localhost:8000/api/hello > /dev/null
END_TIME=$(date +%s%3N)
RESPONSE_TIME=$((END_TIME - START_TIME))

if [ $RESPONSE_TIME -lt 200 ]; then
    pass "API response time: ${RESPONSE_TIME}ms (< 200ms)"
else
    warn "API response time: ${RESPONSE_TIME}ms (target: < 100ms)"
fi

# 10. Test error handling
info "Testing error handling..."
info "  Stopping backend service..."
docker compose stop backend > /dev/null 2>&1
sleep 2

info "  Backend stopped. Manual test required:"
echo "    1. Open http://localhost:3000 in browser"
echo "    2. Click 'Get Message from Backend' button"
echo "    3. Verify user-friendly error message displays"
echo ""

info "  Restarting backend service..."
docker compose start backend > /dev/null 2>&1
sleep 5

BACKEND_HEALTH=$(curl -s http://localhost:8000/health 2>&1)
if [[ $BACKEND_HEALTH == *'"status":"healthy"'* ]]; then
    pass "Backend restarted successfully"
else
    fail "Backend failed to restart properly"
fi

# 11. Test service logs
info "Checking service logs..."
BACKEND_LOGS=$(docker compose logs backend 2>&1)
FRONTEND_LOGS=$(docker compose logs frontend 2>&1)

if [[ $BACKEND_LOGS == *"backend"* ]] || [[ $BACKEND_LOGS == *"green-theme-backend"* ]]; then
    pass "Backend logs accessible"
else
    warn "Backend log labels may not be clear"
fi

if [[ $FRONTEND_LOGS == *"frontend"* ]] || [[ $FRONTEND_LOGS == *"green-theme-frontend"* ]]; then
    pass "Frontend logs accessible"
else
    warn "Frontend log labels may not be clear"
fi

# Summary
echo ""
echo "=================================================="
echo "           Test Results Summary"
echo "=================================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All automated tests passed!${NC}"
else
    echo -e "${RED}⚠️  Some tests failed. Review the output above.${NC}"
fi

echo ""
echo "=================================================="
echo "           Manual Tests Required"
echo "=================================================="
echo ""
echo "Please complete the following manual tests:"
echo ""
echo "1. Visual Verification:"
echo "   - Open http://localhost:3000 in browser"
echo "   - Verify green theme (#2ecc71) is visible"
echo "   - Verify 'Hello World' heading is prominent"
echo "   - Check button styling and hover effects"
echo ""
echo "2. Interaction Testing:"
echo "   - Click 'Get Message from Backend' button"
echo "   - Verify loading indicator appears"
echo "   - Verify button disables during loading"
echo "   - Verify message and timestamp display"
echo "   - Test multiple consecutive clicks"
echo ""
echo "3. Responsive Design:"
echo "   - Open DevTools (F12)"
echo "   - Test at 375px width (mobile)"
echo "   - Test at 768px width (tablet)"
echo "   - Test at 1920px width (desktop)"
echo "   - Verify no horizontal scrolling"
echo ""
echo "4. Development Experience:"
echo "   - Edit frontend/src/App.jsx (change heading text)"
echo "   - Verify browser updates automatically (HMR)"
echo "   - Edit backend/main.py (change message)"
echo "   - Verify uvicorn reloads (~2 seconds)"
echo "   - Test endpoint to confirm changes"
echo ""
echo "=================================================="
echo ""
info "Services are still running. Test manually now."
info "Run 'docker compose down' to stop services when done."
echo ""

if [ $FAILED -eq 0 ]; then
    exit 0
else
    exit 1
fi
