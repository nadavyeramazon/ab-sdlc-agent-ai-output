#!/bin/bash

# AC Compliance Test Runner for Green Theme Backend
# Final production verification script

set -e  # Exit on any error

echo "🚀 Starting Final AC Compliance Verification for Production..."
echo "==============================================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Verifying AC Requirements (AC-007 through AC-012)${NC}"
echo

# Run AC compliance tests
echo -e "${YELLOW}🧪 Running AC Compliance Test Suite...${NC}"
pytest tests/test_ac_compliance.py -v --tb=short
ac_exit_code=$?

if [ $ac_exit_code -eq 0 ]; then
    echo -e "${GREEN}✅ AC Compliance Tests: PASSED${NC}"
else
    echo -e "${RED}❌ AC Compliance Tests: FAILED${NC}"
    exit 1
fi

echo
echo -e "${YELLOW}🧪 Running General Test Suite...${NC}"
pytest tests/test_main.py -v --tb=short
main_exit_code=$?

if [ $main_exit_code -eq 0 ]; then
    echo -e "${GREEN}✅ General Tests: PASSED${NC}"
else
    echo -e "${RED}❌ General Tests: FAILED${NC}"
    exit 1
fi

echo
echo -e "${YELLOW}📊 Running Performance Validation...${NC}"
pytest tests/test_ac_compliance.py::TestAC012ResponseTime -v --tb=short
perf_exit_code=$?

if [ $perf_exit_code -eq 0 ]; then
    echo -e "${GREEN}✅ Performance Tests (AC-012): PASSED${NC}"
else
    echo -e "${RED}❌ Performance Tests (AC-012): FAILED${NC}"
    exit 1
fi

echo
echo -e "${GREEN}🎉 FINAL VERIFICATION COMPLETE${NC}"
echo -e "${GREEN}===============================${NC}"
echo -e "${GREEN}✅ ALL AC REQUIREMENTS VERIFIED${NC}"
echo -e "${GREEN}✅ PRODUCTION READY FOR DEPLOYMENT${NC}"
echo
echo -e "${BLUE}📋 AC Requirements Status:${NC}"
echo -e "${GREEN}  ✅ AC-007: Hello endpoint implementation${NC}"
echo -e "${GREEN}  ✅ AC-008: Health endpoint implementation${NC}"
echo -e "${GREEN}  ✅ AC-009: Port 8000 configuration${NC}"
echo -e "${GREEN}  ✅ AC-010: CORS configuration${NC}"
echo -e "${GREEN}  ✅ AC-011: HTTP status codes${NC}"
echo -e "${GREEN}  ✅ AC-012: Response time <100ms${NC}"
echo
echo -e "${BLUE}🚀 Ready for Production Deployment!${NC}"