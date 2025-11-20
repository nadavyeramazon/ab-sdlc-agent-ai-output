#!/bin/bash
# Test runner script for backend tests

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}==============================================" 
echo -e "Backend Test Suite Runner"
echo -e "============================================== ${NC}"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}Error: pytest is not installed${NC}"
    echo "Run: pip install -r requirements.txt"
    exit 1
fi

echo -e "${YELLOW}Installing/updating dependencies...${NC}"
pip install -q -r requirements.txt

echo ""
echo -e "${YELLOW}Running tests with coverage...${NC}"
echo ""

# Run pytest with coverage
pytest -v \
    --cov=. \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-report=xml \
    --cov-config=.coveragerc \
    --tb=short \
    --strict-markers \
    -ra

TEST_RESULT=$?

echo ""
if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    echo -e "${YELLOW}Coverage report generated:${NC}"
    echo "  - Terminal: See above"
    echo "  - HTML: htmlcov/index.html"
    echo "  - XML: coverage.xml"
    echo ""
    echo -e "${YELLOW}To view HTML coverage report:${NC}"
    echo "  open htmlcov/index.html  # macOS"
    echo "  xdg-open htmlcov/index.html  # Linux"
    echo "  start htmlcov/index.html  # Windows"
else
    echo -e "${RED}✗ Tests failed${NC}"
    echo ""
    echo -e "${YELLOW}To run specific test categories:${NC}"
    echo "  pytest -m unit          # Run unit tests only"
    echo "  pytest -m integration   # Run integration tests only"
    echo "  pytest -m cors          # Run CORS tests only"
    echo ""
    echo -e "${YELLOW}To run specific test file:${NC}"
    echo "  pytest tests/test_api.py"
    echo ""
    echo -e "${YELLOW}For more verbose output:${NC}"
    echo "  pytest -vv"
    exit 1
fi

exit 0
