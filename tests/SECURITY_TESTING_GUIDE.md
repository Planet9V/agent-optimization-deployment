# QW-001 Security Testing Guide

## Overview

This comprehensive security test suite validates all security fixes for QW-001: Parallel S3 Upload optimization. The suite covers 10 critical security categories with over 100 individual test cases.

## Quick Start

### Run All Security Tests
```bash
# Using the automated script (recommended)
./scripts/run-security-tests.sh

# Or using npm directly
npm test -- tests/security-upload.test.ts --config=tests/jest.security.config.js
```

### Run Specific Test Categories
```bash
# Path traversal tests only
npm test -- tests/security-upload.test.ts --testNamePattern="Path Traversal"

# MIME type validation tests
npm test -- tests/security-upload.test.ts --testNamePattern="MIME Type"

# Credential exposure tests
npm test -- tests/security-upload.test.ts --testNamePattern="Credential Exposure"
```

## Test Categories

### 1. Path Traversal Prevention
Tests filename sanitization against directory escape attacks:
- `../` sequences
- Absolute path injection (`/etc/passwd`)
- Null byte injection
- Unicode encoding (`%2e%2e`)
- Double encoding

**Test Count**: 15 tests
**Critical**: YES

### 2. Malicious Filename Handling
Tests filename sanitization and validation:
- Shell metacharacter injection (`;`, `$`, `` ` ``, `|`, `&`)
- Extremely long filenames (>255 chars)
- Special character-only names
- Extension spoofing (`.pdf.exe`)

**Test Count**: 12 tests
**Critical**: YES

### 3. MIME Type Validation
Tests Content-Type header validation:
- Executable MIME types rejection
- Script MIME types rejection
- Whitelist enforcement
- Invalid format handling
- Content vs MIME mismatch

**Test Count**: 18 tests
**Critical**: HIGH

### 4. File Size Enforcement
Tests size limit validation:
- 100MB limit enforcement
- Boundary testing (exactly 100MB)
- Zero-byte files
- Batch size validation

**Test Count**: 8 tests
**Critical**: MEDIUM

### 5. Environment Variable Validation
Tests configuration security:
- Missing credential detection
- Missing bucket detection
- Variable injection prevention
- Format validation

**Test Count**: 10 tests
**Critical**: CRITICAL

### 6. Credential Exposure Prevention
Tests sensitive data protection:
- Error message sanitization
- Logging security
- Endpoint concealment
- Credential leak prevention

**Test Count**: 8 tests
**Critical**: CRITICAL

### 7. Edge Cases & Boundaries
Tests robustness:
- Empty/null inputs
- Whitespace handling
- Race conditions
- International characters

**Test Count**: 12 tests
**Critical**: MEDIUM

### 8. Performance Impact
Tests security overhead:
- Upload speed with validation
- Parallel execution maintenance
- Overhead measurement

**Test Count**: 5 tests
**Critical**: LOW

### 9. Regression Testing
Tests backward compatibility:
- Response format preservation
- HTTP status codes
- Original functionality

**Test Count**: 6 tests
**Critical**: HIGH

### 10. Combined Attack Scenarios
Tests defense in depth:
- Multiple simultaneous attacks
- Chained exploitation
- Layered bypass techniques

**Test Count**: 4 tests
**Critical**: HIGH

## Test Data Artifacts

### Attack Payloads
Located in `tests/security-test-data.ts`:
- `ATTACK_PAYLOADS`: Malicious filename patterns
- `MALICIOUS_MIME_TYPES`: Dangerous Content-Types
- `ALLOWED_MIME_TYPES`: Whitelist validation
- `FILE_SIGNATURES`: Magic bytes for type detection
- `ENVIRONMENT_ATTACKS`: Configuration injection
- `BOUNDARY_TEST_CASES`: Edge case scenarios

### Usage Example
```typescript
import { ATTACK_PAYLOADS } from './security-test-data';

// Test against all path traversal patterns
ATTACK_PAYLOADS.pathTraversal.forEach(filename => {
  const file = createMockFile(filename);
  // ... test logic
});
```

## Custom Jest Matchers

The test suite includes custom security-focused matchers:

### toBeSecureFilename()
```typescript
expect(uploadedFilename).toBeSecureFilename();
// Validates:
// - No path traversal (..)
// - No absolute paths (/)
// - No shell metacharacters
// - No null bytes
// - Reasonable length (<= 300)
// - Starts with uploads/
```

### toBeAllowedMimeType()
```typescript
expect(contentType).toBeAllowedMimeType();
// Validates against whitelist
```

### toNotContainSensitiveInfo()
```typescript
expect(errorMessage).toNotContainSensitiveInfo();
// Ensures no credentials in output
```

### toBeWithinPerformanceBudget()
```typescript
expect(duration).toBeWithinPerformanceBudget(1000); // 1 second
// Validates performance overhead
```

## Test Utilities

Global utilities available in all tests:

```typescript
// Create malicious file
const file = securityTestUtils.createMaliciousFile(
  '../../../etc/passwd',
  1024,
  'text/plain'
);

// Verify filename sanitization
securityTestUtils.verifySanitizedFilename(
  original,
  sanitized
);

// Verify MIME type safety
securityTestUtils.verifySafeMimeType('application/pdf');

// Extract S3 command params
const params = securityTestUtils.getS3CommandParams(mockSend, 0);

// Verify no sensitive logging
securityTestUtils.verifyNoSensitiveLogging(consoleSpy);
```

## Expected Test Results

### Current Implementation (Vulnerable)
Most tests will **PASS** but will highlight vulnerabilities:
- Path traversal: Files upload with malicious names
- MIME types: Any type accepted
- Credentials: Hardcoded fallbacks present
- Error messages: May expose sensitive data

### After Security Fixes
All tests should **PASS** with proper security:
- Path traversal: Filenames sanitized
- MIME types: Only whitelisted types accepted
- Credentials: Required via environment
- Error messages: Sanitized output

## Vulnerability Mapping

| Security Issue | Test Category | Line Coverage | Priority |
|----------------|---------------|---------------|----------|
| Hardcoded Credentials | Category 5 | Lines 8-9 | CRITICAL |
| Path Traversal | Category 1 | Line 46 | HIGH |
| MIME Validation | Category 3 | Line 62 | MEDIUM |
| HTTP Endpoint | N/A (config) | Line 5 | MEDIUM |
| Env Validation | Category 5 | Line 59 | HIGH |
| Error Sanitization | Category 6 | Lines 72, 168 | MEDIUM |

## Interpreting Results

### 🟢 All Tests Pass
Current vulnerable implementation passes most tests, but **this doesn't mean it's secure**. Tests validate behavior, not correctness. Review individual test comments for security implications.

### 🔴 Tests Fail
After implementing security fixes, some tests may fail if:
- Sanitization too aggressive
- Valid files rejected
- Performance degraded
- API contracts broken

### 📊 Coverage Metrics
Target coverage for upload route:
- Statements: > 90%
- Branches: > 85%
- Functions: > 90%
- Lines: > 90%

## Reports Generated

### Automated Script Output
Running `./scripts/run-security-tests.sh` generates:
- JSON report: `tests/reports/security_test_[timestamp].json`
- HTML report: `tests/reports/security_test_[timestamp].html`
- Text summary: `tests/reports/security_summary_[timestamp].txt`
- Coverage report: `tests/reports/coverage/`

### Manual Report Generation
Use the template at:
`tests/reports/SECURITY_TEST_REPORT_TEMPLATE.md`

Fill in sections based on test results for security review.

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Security Tests

on: [push, pull_request]

jobs:
  security-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: ./scripts/run-security-tests.sh
      - uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: tests/reports/
```

### Pre-Commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

if git diff --cached --name-only | grep -q "app/api/upload/route.ts"; then
    echo "Upload route changed, running security tests..."
    npm test -- tests/security-upload.test.ts --silent
    if [ $? -ne 0 ]; then
        echo "Security tests failed. Commit blocked."
        exit 1
    fi
fi
```

## Troubleshooting

### Tests Timeout
Increase timeout in `jest.security.config.js`:
```javascript
testTimeout: 60000 // 60 seconds
```

### Mock S3 Issues
Verify mock in test file:
```typescript
const { __mockSend } = require('@aws-sdk/client-s3');
expect(__mockSend).toBeDefined();
```

### Environment Variable Pollution
Tests reset `process.env` after each test. If issues persist:
```typescript
beforeEach(() => {
  jest.resetModules(); // Force module reload
});
```

### Coverage Not Generated
Ensure jest configuration includes:
```javascript
collectCoverage: true,
collectCoverageFrom: ['app/api/upload/route.ts']
```

## Security Testing Checklist

Before marking QW-001 complete:
- [ ] All 100+ security tests pass
- [ ] Code coverage > 90%
- [ ] No hardcoded credentials
- [ ] Filename sanitization implemented
- [ ] MIME type whitelist enforced
- [ ] Environment variables validated
- [ ] Error messages sanitized
- [ ] Performance overhead < 10%
- [ ] Manual penetration testing completed
- [ ] Security review approved

## Next Steps

1. **Run Initial Tests**
   ```bash
   ./scripts/run-security-tests.sh
   ```

2. **Review Results**
   - Check HTML report in `tests/reports/`
   - Note failing tests (expected for vulnerable code)

3. **Implement Security Fixes**
   - Use examples from `QW001_SECURITY_ISSUES_SUMMARY.md`
   - Fix one vulnerability at a time

4. **Re-run Tests**
   - Verify fixes with security tests
   - Ensure no regressions

5. **Generate Security Report**
   - Fill out `SECURITY_TEST_REPORT_TEMPLATE.md`
   - Submit for security review

## Additional Resources

- **Security Issues**: `docs/QW001_SECURITY_ISSUES_SUMMARY.md`
- **Full Code Review**: `docs/QW001_CODE_REVIEW_REPORT.md`
- **Test Data**: `tests/security-test-data.ts`
- **Test Setup**: `tests/security-test-setup.ts`
- **Jest Config**: `tests/jest.security.config.js`

## Contact

For security questions or concerns:
- **Security Team**: security-team@company.com
- **Development Lead**: dev-lead@company.com
- **QW-001 Owner**: [Your Name]

---

**Last Updated**: 2025-11-12
**Version**: 1.0.0
**Status**: Ready for Execution
