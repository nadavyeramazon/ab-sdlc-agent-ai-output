#!/bin/bash

# AC Requirements Compliance Test Runner
# This script runs all tests to verify AC-007 through AC-012 compliance

echo "🧪 Running AC Requirements Compliance Tests"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to run test and report results
run_ac_test() {
    local ac_number=$1
    local test_class=$2
    local description=$3
    
    echo -e "${YELLOW}Testing $ac_number: $description${NC}"
    
    if pytest tests/test_ac_compliance.py::$test_class -v --tb=short; then
        echo -e "${GREEN}✅ $ac_number: PASSED${NC}"
    else
        echo -e "${RED}❌ $ac_number: FAILED${NC}"
        exit 1
    fi
    echo ""
}

# Check if pytest is available
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}❌ pytest not found. Please install requirements: pip install -r requirements.txt${NC}"
    exit 1
fi

echo "📋 Running Individual AC Tests:"
echo ""

# Run each AC test individually
run_ac_test "AC-007" "TestAC007HelloEndpoint" "Hello endpoint returns 'Hello World from Backend!' message"
run_ac_test "AC-008" "TestAC008HealthEndpoint" "Health endpoint returns 'healthy' status"
run_ac_test "AC-009" "TestAC009PortConfiguration" "Backend runs on port 8000 and accepts HTTP requests"
run_ac_test "AC-010" "TestAC010CORSConfiguration" "CORS properly configured for frontend communication"
run_ac_test "AC-011" "TestAC011HTTPStatusCodes" "Proper HTTP status codes (200 for success)"
run_ac_test "AC-012" "TestAC012ResponseTime" "Response time under 100ms for all endpoints"

# Run integrated compliance test
echo -e "${YELLOW}Running Integrated AC Compliance Test...${NC}"
if pytest tests/test_ac_compliance.py::TestIntegratedACCompliance::test_ac_requirements_summary -v -s; then
    echo -e "${GREEN}✅ Integrated AC Test: PASSED${NC}"
else
    echo -e "${RED}❌ Integrated AC Test: FAILED${NC}"
    exit 1
fi
echo ""

# Run all tests for complete coverage
echo -e "${YELLOW}Running Complete Test Suite...${NC}"
if pytest tests/ -v --tb=short; then
    echo -e "${GREEN}✅ All Tests: PASSED${NC}"
else
    echo -e "${RED}❌ Some Tests: FAILED${NC}"
    exit 1
fi

echo ""
echo "🎉 AC REQUIREMENTS COMPLIANCE VERIFIED!"
echo "======================================="
echo -e "${GREEN}✅ AC-007: Hello endpoint compliance${NC}"
echo -e "${GREEN}✅ AC-008: Health endpoint compliance${NC}"
echo -e "${GREEN}✅ AC-009: Port 8000 configuration compliance${NC}"
echo -e "${GREEN}✅ AC-010: CORS configuration compliance${NC}"
echo -e "${GREEN}✅ AC-011: HTTP status codes compliance${NC}"
echo -e "${GREEN}✅ AC-012: Sub-100ms response time compliance${NC}"
echo ""
echo "Backend is ready for frontend integration! 🚀"
echo "API Documentation: http://localhost:8000/docs"
echo "Health Check: http://localhost:8000/health"
echo "Hello Endpoint: http://localhost:8000/api/hello"