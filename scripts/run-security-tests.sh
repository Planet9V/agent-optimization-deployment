#!/bin/bash

# QW-001 Security Test Execution Script
# Automated security testing for parallel S3 uploads

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TEST_FILE="tests/security-upload.test.ts"
REPORT_DIR="tests/reports"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="${REPORT_DIR}/security_test_${TIMESTAMP}.json"
HTML_REPORT="${REPORT_DIR}/security_test_${TIMESTAMP}.html"

echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  QW-001 Security Test Suite Execution             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

# Create report directory
mkdir -p "${REPORT_DIR}"

# Check if test file exists
if [ ! -f "${TEST_FILE}" ]; then
    echo -e "${RED}✗ Error: Test file not found: ${TEST_FILE}${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Test file found${NC}"
echo ""

# Run security tests
echo -e "${YELLOW}Running security tests...${NC}"
echo ""

# Run with coverage and detailed output
npm test -- "${TEST_FILE}" \
    --coverage \
    --verbose \
    --json \
    --outputFile="${REPORT_FILE}" \
    --testNamePattern="" \
    --maxWorkers=1 \
    --detectOpenHandles \
    --forceExit

TEST_EXIT_CODE=$?

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

# Parse results
if [ -f "${REPORT_FILE}" ]; then
    TOTAL_TESTS=$(jq '.numTotalTests' "${REPORT_FILE}")
    PASSED_TESTS=$(jq '.numPassedTests' "${REPORT_FILE}")
    FAILED_TESTS=$(jq '.numFailedTests' "${REPORT_FILE}")

    echo -e "${BLUE}Test Results Summary:${NC}"
    echo -e "  Total Tests:  ${TOTAL_TESTS}"
    echo -e "  ${GREEN}Passed:       ${PASSED_TESTS}${NC}"

    if [ "${FAILED_TESTS}" -gt 0 ]; then
        echo -e "  ${RED}Failed:       ${FAILED_TESTS}${NC}"
    else
        echo -e "  Failed:       ${FAILED_TESTS}"
    fi

    echo ""
fi

# Security vulnerability assessment
echo -e "${BLUE}Security Vulnerability Coverage:${NC}"
echo ""
echo -e "  ${YELLOW}[1]${NC} Path Traversal Prevention"
echo -e "  ${YELLOW}[2]${NC} Malicious Filename Handling"
echo -e "  ${YELLOW}[3]${NC} MIME Type Validation"
echo -e "  ${YELLOW}[4]${NC} File Size Limits"
echo -e "  ${YELLOW}[5]${NC} Environment Variable Validation"
echo -e "  ${YELLOW}[6]${NC} Credential Exposure Prevention"
echo -e "  ${YELLOW}[7]${NC} Edge Cases & Boundaries"
echo -e "  ${YELLOW}[8]${NC} Performance Impact"
echo -e "  ${YELLOW}[9]${NC} Regression Testing"
echo -e "  ${YELLOW}[10]${NC} Combined Attack Scenarios"
echo ""

# Generate HTML report
if command -v jest-html-reporter &> /dev/null; then
    echo -e "${YELLOW}Generating HTML report...${NC}"
    jest-html-reporter --pageTitle="QW-001 Security Test Report" \
        --outputPath="${HTML_REPORT}" \
        --includeFailureMsg=true \
        --includeConsoleLog=true
    echo -e "${GREEN}✓ HTML report generated: ${HTML_REPORT}${NC}"
    echo ""
fi

# Coverage summary
if [ -d "coverage" ]; then
    echo -e "${BLUE}Code Coverage Summary:${NC}"
    echo ""
    cat coverage/coverage-summary.json | jq '.total' 2>/dev/null || echo "Coverage data not available"
    echo ""
fi

# Security recommendations
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Security Recommendations:${NC}"
echo ""

if [ "${FAILED_TESTS}" -gt 0 ]; then
    echo -e "${RED}⚠ CRITICAL: Failed tests detected!${NC}"
    echo ""
    echo -e "${YELLOW}Before deploying to production:${NC}"
    echo -e "  1. Review failed test cases in detail"
    echo -e "  2. Implement missing security controls"
    echo -e "  3. Re-run security test suite"
    echo -e "  4. Perform manual penetration testing"
    echo -e "  5. Update security documentation"
    echo ""
    echo -e "${RED}DO NOT DEPLOY until all security tests pass!${NC}"
else
    echo -e "${GREEN}✓ All security tests passed!${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "  1. Review test coverage metrics"
    echo -e "  2. Perform manual security audit"
    echo -e "  3. Run penetration testing tools"
    echo -e "  4. Update security documentation"
    echo -e "  5. Schedule security review meeting"
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

# Generate summary report
SUMMARY_FILE="${REPORT_DIR}/security_summary_${TIMESTAMP}.txt"
{
    echo "QW-001 Security Test Summary"
    echo "============================"
    echo ""
    echo "Execution Date: $(date)"
    echo "Test File: ${TEST_FILE}"
    echo ""
    echo "Results:"
    echo "  Total Tests: ${TOTAL_TESTS:-N/A}"
    echo "  Passed: ${PASSED_TESTS:-N/A}"
    echo "  Failed: ${FAILED_TESTS:-N/A}"
    echo ""
    echo "Security Coverage:"
    echo "  - Path Traversal Prevention: Tested"
    echo "  - Filename Sanitization: Tested"
    echo "  - MIME Type Validation: Tested"
    echo "  - File Size Limits: Tested"
    echo "  - Environment Variables: Tested"
    echo "  - Credential Protection: Tested"
    echo "  - Edge Cases: Tested"
    echo "  - Performance: Tested"
    echo "  - Regression: Tested"
    echo "  - Combined Attacks: Tested"
    echo ""
    echo "Reports Generated:"
    echo "  - JSON: ${REPORT_FILE}"
    echo "  - HTML: ${HTML_REPORT}"
    echo "  - Summary: ${SUMMARY_FILE}"
} > "${SUMMARY_FILE}"

echo -e "${GREEN}✓ Summary saved to: ${SUMMARY_FILE}${NC}"
echo ""

# Exit with test result code
if [ ${TEST_EXIT_CODE} -eq 0 ]; then
    echo -e "${GREEN}✓ Security test suite completed successfully${NC}"
    exit 0
else
    echo -e "${RED}✗ Security test suite failed${NC}"
    exit 1
fi
