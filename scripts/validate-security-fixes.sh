#!/bin/bash
# Security Fixes Validation Script for QW-001
# Verifies all 5 critical security issues are resolved

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  QW-001 Security Fixes Validation                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS_COUNT=0
FAIL_COUNT=0

# ============================================================================
# Test Functions
# ============================================================================

test_passed() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
    ((PASS_COUNT++))
}

test_failed() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    ((FAIL_COUNT++))
}

test_warning() {
    echo -e "${YELLOW}⚠️  WARN${NC}: $1"
}

# ============================================================================
# Issue #1: No Hardcoded Credentials
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Issue #1: Hardcoded Credentials Removal"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ROUTE_FILE="app/api/upload/route.ts"

# Check for hardcoded fallback values
if grep -q "|| 'minio'" "$ROUTE_FILE"; then
    test_failed "Hardcoded 'minio' credential fallback found"
else
    test_passed "No hardcoded 'minio' credential fallback"
fi

if grep -q "|| 'minio@openspg'" "$ROUTE_FILE"; then
    test_failed "Hardcoded 'minio@openspg' credential fallback found"
else
    test_passed "No hardcoded 'minio@openspg' credential fallback"
fi

if grep -q "|| 'aeon-documents'" "$ROUTE_FILE"; then
    test_failed "Hardcoded 'aeon-documents' bucket fallback found"
else
    test_passed "No hardcoded 'aeon-documents' bucket fallback"
fi

# Check for fail-fast validation
if grep -q "throw new Error('FATAL: MINIO_ACCESS_KEY" "$ROUTE_FILE"; then
    test_passed "Fail-fast validation for MINIO_ACCESS_KEY implemented"
else
    test_failed "Missing fail-fast validation for MINIO_ACCESS_KEY"
fi

if grep -q "throw new Error('FATAL: MINIO_SECRET_KEY" "$ROUTE_FILE"; then
    test_passed "Fail-fast validation for MINIO_SECRET_KEY implemented"
else
    test_failed "Missing fail-fast validation for MINIO_SECRET_KEY"
fi

# ============================================================================
# Issue #2: Filename Sanitization
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Issue #2: Filename Sanitization (Path Traversal Prevention)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if grep -q "function sanitizeFileName" "$ROUTE_FILE"; then
    test_passed "sanitizeFileName function exists"
else
    test_failed "Missing sanitizeFileName function"
fi

# Check for path traversal prevention
if grep -q "replace(/\\\\\\\\/g, '/')" "$ROUTE_FILE"; then
    test_passed "Path separator normalization implemented"
else
    test_failed "Missing path separator normalization"
fi

if grep -q "replace(/\\.\\.\\./g, '_')" "$ROUTE_FILE" || grep -q "replace(/\\.\\./g, '_')" "$ROUTE_FILE"; then
    test_passed "Parent directory reference removal implemented"
else
    test_failed "Missing parent directory reference removal"
fi

if grep -q "slice(0, 255)" "$ROUTE_FILE"; then
    test_passed "Filename length limit implemented"
else
    test_failed "Missing filename length limit"
fi

if grep -q "split('/').pop()" "$ROUTE_FILE"; then
    test_passed "Absolute path prevention implemented"
else
    test_failed "Missing absolute path prevention"
fi

# ============================================================================
# Issue #3: MIME Type Validation
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Issue #3: MIME Type Validation (Malware Prevention)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if grep -q "ALLOWED_MIME_TYPES" "$ROUTE_FILE"; then
    test_passed "ALLOWED_MIME_TYPES allowlist defined"
else
    test_failed "Missing ALLOWED_MIME_TYPES allowlist"
fi

if grep -q "function validateContentType" "$ROUTE_FILE"; then
    test_passed "validateContentType function exists"
else
    test_failed "Missing validateContentType function"
fi

if grep -q "ALLOWED_MIME_TYPES.has" "$ROUTE_FILE"; then
    test_passed "MIME type allowlist validation implemented"
else
    test_failed "Missing MIME type allowlist validation"
fi

# Check for common safe types
if grep -q "'application/pdf'" "$ROUTE_FILE"; then
    test_passed "PDF files allowed in MIME allowlist"
else
    test_failed "PDF files not in MIME allowlist"
fi

if grep -q "'image/jpeg'" "$ROUTE_FILE" || grep -q "'image/png'" "$ROUTE_FILE"; then
    test_passed "Image files allowed in MIME allowlist"
else
    test_failed "Image files not in MIME allowlist"
fi

# ============================================================================
# Issue #4: HTTPS Endpoint Configuration
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Issue #4: HTTPS Endpoint Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check for hardcoded HTTP endpoint
if grep -q "endpoint: 'http://openspg-minio:9000'" "$ROUTE_FILE"; then
    test_failed "Hardcoded HTTP endpoint found"
else
    test_passed "No hardcoded HTTP endpoint"
fi

# Check for environment variable usage
if grep -q "endpoint: MINIO_ENDPOINT" "$ROUTE_FILE"; then
    test_passed "Endpoint from MINIO_ENDPOINT environment variable"
else
    test_failed "Endpoint not from environment variable"
fi

# Check for HTTPS warning in production
if grep -q "Production environment should use HTTPS" "$ROUTE_FILE"; then
    test_passed "HTTPS warning for production implemented"
else
    test_warning "Missing HTTPS warning for production"
fi

# ============================================================================
# Issue #5: Environment Variable Validation
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Issue #5: Environment Variable Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if grep -q "const MINIO_BUCKET = process.env.MINIO_BUCKET" "$ROUTE_FILE"; then
    test_passed "MINIO_BUCKET from environment variable (no fallback)"
else
    test_failed "MINIO_BUCKET has fallback or not from environment"
fi

if grep -q "throw new Error('FATAL: MINIO_BUCKET" "$ROUTE_FILE"; then
    test_passed "Fail-fast validation for MINIO_BUCKET implemented"
else
    test_failed "Missing fail-fast validation for MINIO_BUCKET"
fi

if grep -q "throw new Error('FATAL: MINIO_ENDPOINT" "$ROUTE_FILE"; then
    test_passed "Fail-fast validation for MINIO_ENDPOINT implemented"
else
    test_failed "Missing fail-fast validation for MINIO_ENDPOINT"
fi

# ============================================================================
# Additional Security Checks
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Additional Security Features"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if grep -q "function logSecurityEvent" "$ROUTE_FILE"; then
    test_passed "Security event logging function implemented"
else
    test_warning "Missing security event logging function"
fi

if grep -q "accessKeyId: undefined" "$ROUTE_FILE"; then
    test_passed "Credential sanitization in logs implemented"
else
    test_warning "Missing credential sanitization in logs"
fi

if grep -q "instanceof File" "$ROUTE_FILE"; then
    test_passed "Runtime type validation implemented"
else
    test_warning "Missing runtime type validation"
fi

# ============================================================================
# File Existence Checks
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Supporting Files"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "tests/security/upload-security.test.ts" ]; then
    test_passed "Security test suite exists"
else
    test_failed "Missing security test suite"
fi

if [ -f "config/.env.example" ]; then
    test_passed "Environment configuration template exists"
else
    test_warning "Missing environment configuration template"
fi

if [ -f "docs/SECURITY_FIXES_QW001.md" ]; then
    test_passed "Security fixes documentation exists"
else
    test_warning "Missing security fixes documentation"
fi

# ============================================================================
# Performance Verification
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Performance Architecture"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if grep -q "Promise.allSettled" "$ROUTE_FILE"; then
    test_passed "Parallel execution with Promise.allSettled maintained"
else
    test_failed "Missing parallel execution pattern"
fi

if grep -q "PARALLEL PREPARATION" "$ROUTE_FILE" && grep -q "PARALLEL UPLOADS" "$ROUTE_FILE"; then
    test_passed "Parallel preparation and upload comments present"
else
    test_warning "Missing parallel execution documentation"
fi

# ============================================================================
# Results Summary
# ============================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  VALIDATION RESULTS                                            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "Total Tests: $((PASS_COUNT + FAIL_COUNT))"
echo -e "${GREEN}Passed: $PASS_COUNT${NC}"
echo -e "${RED}Failed: $FAIL_COUNT${NC}"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✅ ALL SECURITY FIXES VERIFIED                                ║${NC}"
    echo -e "${GREEN}║  Status: PRODUCTION READY                                      ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ❌ SECURITY VALIDATION FAILED                                  ║${NC}"
    echo -e "${RED}║  Status: NOT READY FOR PRODUCTION                              ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi
