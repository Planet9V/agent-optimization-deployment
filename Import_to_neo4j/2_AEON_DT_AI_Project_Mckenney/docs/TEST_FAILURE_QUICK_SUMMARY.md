# Test Failure Quick Summary
**Date**: 2025-11-05
**Total Failures**: 14 tests

## TL;DR - Critical Finding

**ROOT CAUSE**: Missing `watchdog` Python dependency blocks ALL test imports

**FIX**: Install watchdog → Fix 11 tests immediately
```bash
pip3 install watchdog
```

---

## Failure Breakdown

### CRITICAL: Dependency Issue (11 tests) - 1 minute fix
- **Problem**: `ModuleNotFoundError: No module named 'watchdog'`
- **Impact**: Blocks all SBOM CVE validation tests from running
- **Files Affected**:
  - `test_sbom_cve_validation.py` (9 tests)
  - `test_sbom_cve_direct.py` (1 test)
  - Plus 1 entity resolution test blocked
- **Fix**: `pip3 install watchdog` (already in requirements.txt)

### MEDIUM: CAPEC Parameter Bug (2 tests) - 2 minute fix
- **Problem**: Cypher query parameter mismatch
- **Error**: `Expected parameter(s): capec_id`
- **Location**: `tests/test_entity_resolution.py:201`
- **Files Affected**:
  - `test_capec_resolution_same_logic_as_cve`
  - `test_mixed_entity_types_all_resolved`
- **Fix**: Change `capecId=capec_id` to `capec_id=capec_id` in parameter binding

### LOW: Test Logic Bug (1 test) - 2 minute fix
- **Problem**: Case-sensitive string matching
- **Error**: Looking for 'Confidentiality' but text has 'confidentiality'
- **Location**: `tests/unit/test_nlp_extractor.py:113`
- **File Affected**: `test_impact_classification`
- **Fix**: Change to case-insensitive: `if k.lower() in text.lower()`

---

## Fix Order & Timeline

1. **Install watchdog** (1 min) → 11 tests unblocked ✅
2. **Fix CAPEC bug** (2 min) → 2 tests fixed ✅
3. **Fix NLP case** (2 min) → 1 test fixed ✅

**Total Time**: ~5 minutes to fix all 14 test failures

---

## Detailed Report

See: `docs/TEST_FAILURE_ANALYSIS_REPORT.md` for complete analysis with:
- Full error stack traces
- Root cause analysis for each failure
- Step-by-step fix instructions
- Validation commands
- Long-term recommendations
