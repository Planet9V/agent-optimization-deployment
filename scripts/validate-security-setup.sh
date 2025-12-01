#!/bin/bash

# Validation script to verify security test suite setup
# Run this to confirm all files are in place and properly configured

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  QW-001 Security Test Suite Validation            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

ERRORS=0
WARNINGS=0

# Check files exist
echo -e "${YELLOW}Checking required files...${NC}"
echo ""

FILES=(
    "tests/security-upload.test.ts:Security test suite"
    "tests/security-test-data.ts:Attack simulation data"
    "tests/security-test-setup.ts:Custom matchers and utilities"
    "tests/jest.security.config.js:Security Jest configuration"
    "tests/SECURITY_TESTING_GUIDE.md:Usage documentation"
    "tests/reports/SECURITY_TEST_REPORT_TEMPLATE.md:Report template"
    "scripts/run-security-tests.sh:Automated execution script"
    "jest.config.js:Default Jest configuration"
    "package.json:Package configuration"
    "app/api/upload/route.ts:Upload implementation"
    "docs/SECURITY_TEST_SUMMARY.md:Summary documentation"
)

for FILE_DESC in "${FILES[@]}"; do
    IFS=':' read -r FILE DESC <<< "$FILE_DESC"
    if [ -f "$FILE" ]; then
        echo -e "  ${GREEN}✓${NC} $DESC"
    else
        echo -e "  ${RED}✗${NC} $DESC (missing: $FILE)"
        ((ERRORS++))
    fi
done

echo ""

# Check file permissions
echo -e "${YELLOW}Checking file permissions...${NC}"
echo ""

EXEC_FILES=(
    "scripts/run-security-tests.sh"
    "scripts/validate-security-setup.sh"
)

for FILE in "${EXEC_FILES[@]}"; do
    if [ -x "$FILE" ]; then
        echo -e "  ${GREEN}✓${NC} $FILE is executable"
    else
        echo -e "  ${YELLOW}⚠${NC} $FILE is not executable (run: chmod +x $FILE)"
        ((WARNINGS++))
    fi
done

echo ""

# Check package.json scripts
echo -e "${YELLOW}Checking package.json scripts...${NC}"
echo ""

SCRIPTS=(
    "test"
    "test:security"
    "test:security:watch"
    "test:security:coverage"
    "test:security:report"
)

for SCRIPT in "${SCRIPTS[@]}"; do
    if grep -q "\"$SCRIPT\":" package.json; then
        echo -e "  ${GREEN}✓${NC} Script '$SCRIPT' defined"
    else
        echo -e "  ${RED}✗${NC} Script '$SCRIPT' missing"
        ((ERRORS++))
    fi
done

echo ""

# Check dependencies
echo -e "${YELLOW}Checking dependencies...${NC}"
echo ""

DEPS=(
    "jest"
    "ts-jest"
    "@types/jest"
    "typescript"
    "ts-node"
)

for DEP in "${DEPS[@]}"; do
    if grep -q "\"$DEP\":" package.json; then
        echo -e "  ${GREEN}✓${NC} Dependency '$DEP' listed"
    else
        echo -e "  ${YELLOW}⚠${NC} Dependency '$DEP' missing (may need: npm install --save-dev $DEP)"
        ((WARNINGS++))
    fi
done

echo ""

# Check directory structure
echo -e "${YELLOW}Checking directory structure...${NC}"
echo ""

DIRS=(
    "tests"
    "tests/reports"
    "scripts"
    "docs"
    "app/api/upload"
)

for DIR in "${DIRS[@]}"; do
    if [ -d "$DIR" ]; then
        echo -e "  ${GREEN}✓${NC} Directory $DIR exists"
    else
        echo -e "  ${RED}✗${NC} Directory $DIR missing"
        ((ERRORS++))
    fi
done

echo ""

# Count test cases
echo -e "${YELLOW}Analyzing test suite...${NC}"
echo ""

if [ -f "tests/security-upload.test.ts" ]; then
    TEST_COUNT=$(grep -c "^\s*it(" tests/security-upload.test.ts || echo "0")
    CATEGORY_COUNT=$(grep -c "^\s*describe(" tests/security-upload.test.ts || echo "0")

    echo -e "  ${BLUE}ℹ${NC} Test categories: $CATEGORY_COUNT"
    echo -e "  ${BLUE}ℹ${NC} Individual tests: $TEST_COUNT"

    if [ "$TEST_COUNT" -ge 90 ]; then
        echo -e "  ${GREEN}✓${NC} Comprehensive test coverage ($TEST_COUNT tests)"
    else
        echo -e "  ${YELLOW}⚠${NC} Test count below expected ($TEST_COUNT < 90)"
        ((WARNINGS++))
    fi
fi

echo ""

# Check attack payload data
echo -e "${YELLOW}Analyzing attack payloads...${NC}"
echo ""

if [ -f "tests/security-test-data.ts" ]; then
    PAYLOAD_COUNT=$(grep -c "^\s*'.*'," tests/security-test-data.ts || echo "0")
    echo -e "  ${BLUE}ℹ${NC} Attack payloads defined: $PAYLOAD_COUNT"

    if [ "$PAYLOAD_COUNT" -ge 70 ]; then
        echo -e "  ${GREEN}✓${NC} Comprehensive attack simulation data"
    else
        echo -e "  ${YELLOW}⚠${NC} Attack payload count below expected"
        ((WARNINGS++))
    fi
fi

echo ""

# Check custom matchers
echo -e "${YELLOW}Checking custom matchers...${NC}"
echo ""

MATCHERS=(
    "toBeSecureFilename"
    "toBeAllowedMimeType"
    "toNotContainSensitiveInfo"
    "toBeWithinPerformanceBudget"
)

for MATCHER in "${MATCHERS[@]}"; do
    if grep -q "$MATCHER" tests/security-test-setup.ts; then
        echo -e "  ${GREEN}✓${NC} Custom matcher '$MATCHER' defined"
    else
        echo -e "  ${RED}✗${NC} Custom matcher '$MATCHER' missing"
        ((ERRORS++))
    fi
done

echo ""

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Validation Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "  1. Install dependencies: npm install"
    echo "  2. Run security tests: npm run test:security:report"
    echo "  3. Review test output in tests/reports/"
    echo ""
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ Validation passed with warnings${NC}"
    echo -e "  Warnings: $WARNINGS"
    echo ""
    echo -e "${YELLOW}Please address warnings before running tests${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Validation failed${NC}"
    echo -e "  Errors: $ERRORS"
    echo -e "  Warnings: $WARNINGS"
    echo ""
    echo -e "${RED}Please fix errors before running tests${NC}"
    echo ""
    exit 1
fi
