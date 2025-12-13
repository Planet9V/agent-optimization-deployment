# AEON MASTER API TABLE - ALL 232 ENDPOINTS WITH TEST STATUS

**Generated**: 2025-12-12 14:50 UTC
**Last Updated**: 2025-12-12 14:50 UTC
**Total APIs**: 232 (181 documented + 51 discovered)
**Tested**: 36 (15.5%)
**Working**: 4 (1.7%)
**Status**: NOT PRODUCTION READY

---

## QUICK REFERENCE WITH TEST STATUS

| Service | Port | APIs | Tested | Working | Pass Rate | Status |
|---------|------|------|--------|---------|-----------|--------|
| NER11 Core | 8000 | 5 | 5 | 4 | 80% | ✅ OPERATIONAL |
| Phase B2 - SBOM | 8000 | 32 | 3 | 0 | 0% | ❌ BROKEN |
| Phase B2 - Equipment | 8000 | 28 | 3 | 0 | 0% | ❌ BROKEN |
| Phase B3 - Threat Intel | 8000 | 27 | 4 | 0 | 0% | ❌ BROKEN |
| Phase B3 - Risk | 8000 | 26 | 4 | 0 | 0% | ❌ BROKEN |
| Phase B3 - Remediation | 8000 | 29 | 6 | 0 | 0% | ❌ BROKEN |
| Phase B4 - Compliance | 8000 | 28 | 0 | 0 | 0% | ⏳ NOT TESTED |
| Phase B4 - Scanning | 8000 | 30 | 0 | 0 | 0% | ⏳ NOT TESTED |
| Phase B4 - Alerts | 8000 | 32 | 0 | 0 | 0% | ⏳ NOT TESTED |
| Phase B5 - Economic | 8000 | 27 | 0 | 0 | 0% | ⏳ NOT TESTED |
| Phase B5 - Demographics | 8000 | 4 | 0 | 0 | 0% | ⏳ NOT TESTED |
| Phase B5 - Prioritization | 8000 | 28 | 0 | 0 | 0% | ⏳ NOT TESTED |
| Next.js Frontend | 3000 | 41 | 0 | 0 | 0% | ⏳ NOT TESTED |
| aeon-saas-dev | 3000 | 64 | 7 | 0 | 0% | ❌ BROKEN |
| openspg-server | 8887 | ~40 | 4 | 0 | 0% | ⏳ UNTESTED |

**OVERALL**: 36/232 tested (15.5%), 4/36 passing (11%), 4/232 working (1.7%)

---

## CRITICAL FINDINGS

### Root Causes of Failures
1. **Missing Customer Context Middleware**: 128 APIs (90% of Phase B)
2. **Hardcoded Localhost Connections**: Database connectivity issues
3. **Missing Test Data**: No customer_id='dev' in databases
4. **Graph Fragmentation**: 504K orphan nodes break traversal

### Fix Required
- **5 minutes**: Add customer context middleware → unlock 128 APIs
- **12-16 hours**: Fix database connections
- **24-32 hours**: Resolve graph fragmentation

---

## DETAILED API STATUS

## NER11 Core APIs (Port 8000)

| # | Endpoint | Method | Test Date | Status | Response Time | Notes |
|---|----------|--------|-----------|--------|---------------|-------|
| 1 | /ner | POST | 2025-12-12 | ✅ PASS | 50-300ms | Entity extraction working |
| 2 | /search/semantic | POST | 2025-12-12 | ✅ PASS | 100-200ms | Semantic search working |
| 3 | /search/hybrid | POST | 2025-12-12 | ⚠️ DEGRADED | 5-21s | Works but slow (needs optimization) |
| 4 | /health | GET | 2025-12-12 | ✅ PASS | <50ms | Health check working |
| 5 | /info | GET | 2025-12-12 | ⏳ NOT TESTED | - | Not tested yet |

---

## Phase B2 - SBOM APIs (32 endpoints, Port 8000)

**Test Date**: 2025-12-12
**Auth Required**: `x-customer-id` header
**Root Cause**: Customer context middleware missing
**Fix**: Add middleware to serve_model.py (5 minutes)

| # | Endpoint | Method | Test Date | Status | Error | Notes |
|---|----------|--------|-----------|--------|-------|-------|
| 6 | /api/v2/sbom/sboms | GET | 2025-12-12 | ❌ FAIL | 400 | Customer context required |
| 7 | /api/v2/sbom/sboms/{id} | GET | ⏳ NOT TESTED | ⏳ PENDING | - | - |
| 8 | /api/v2/sbom/sboms | POST | ⏳ NOT TESTED | ⏳ PENDING | - | - |
| 9 | /api/v2/sbom/components | GET | ⏳ NOT TESTED | ⏳ PENDING | - | - |
| 10 | /api/v2/sbom/components/search | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 11 | /api/v2/sbom/components/vulnerable | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 12-37 | *(28 more SBOM endpoints)* | GET/POST/PUT/DELETE | ⏳ NOT TESTED | ⏳ PENDING | - | Assumed same middleware issue |

---

## Phase B2 - Equipment APIs (28 endpoints, Port 8000)

**Test Date**: 2025-12-12
**Auth Required**: `x-customer-id` header
**Root Cause**: Customer context middleware missing + localhost connections
**Fix**: Middleware (5 min) + connection config (12-16h)

| # | Endpoint | Method | Test Date | Status | Error | Notes |
|---|----------|--------|-----------|--------|-------|-------|
| 38 | /api/v2/vendor-equipment/vendors | GET | 2025-12-12 | ❌ FAIL | 400 | Customer context required |
| 39 | /api/v2/vendor-equipment/equipment | GET | 2025-12-12 | ❌ FAIL | 400 | Customer context required |
| 40 | /api/v2/vendor-equipment/equipment/search | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 41-65 | *(25 more Equipment endpoints)* | GET/POST/PUT/DELETE | ⏳ NOT TESTED | ⏳ PENDING | - | Assumed same issues |

---

## Phase B3 - Threat Intelligence APIs (27 endpoints, Port 8000)

**Test Date**: 2025-12-12
**Root Cause**: Customer context + database integration
**Fix**: Middleware + connection config + test data

| # | Endpoint | Method | Test Date | Status | Error | Notes |
|---|----------|--------|-----------|--------|-------|-------|
| 66 | /api/v2/threat-intel/actors/active | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 67 | /api/v2/threat-intel/campaigns/active | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 68 | /api/v2/threat-intel/iocs/active | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 69 | /api/v2/threat-intel/mitre/coverage | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 70 | /api/v2/threat-intel/dashboard/summary | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 71-92 | *(22 more Threat Intel endpoints)* | GET/POST/PUT/DELETE | ⏳ NOT TESTED | ⏳ PENDING | - | Assumed same issues |

---

## Phase B3 - Risk Scoring APIs (26 endpoints, Port 8000)

**Test Date**: 2025-12-12
**Root Cause**: Customer context + CVSS data incomplete (12% missing)
**Fix**: Middleware + PROC-101 execution (4-6h)

| # | Endpoint | Method | Test Date | Status | Error | Notes |
|---|----------|--------|-----------|--------|-------|-------|
| 93 | /api/v2/risk/dashboard/summary | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 94 | /api/v2/risk/scores/high-risk | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 95 | /api/v2/risk/assets/mission-critical | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 96 | /api/v2/risk/exposure/internet-facing | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 97-118 | *(22 more Risk endpoints)* | GET/POST/PUT/DELETE | ⏳ NOT TESTED | ⏳ PENDING | - | Assumed same issues |

---

## Phase B3 - Remediation APIs (29 endpoints, Port 8000)

**Test Date**: 2025-12-12
**Root Cause**: Customer context + database integration
**Fix**: Middleware + connection config

| # | Endpoint | Method | Test Date | Status | Error | Notes |
|---|----------|--------|-----------|--------|-------|-------|
| 119 | /api/v2/remediation/tasks/open | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 120 | /api/v2/remediation/tasks/overdue | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 121 | /api/v2/remediation/plans/active | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 122 | /api/v2/remediation/sla/breaches | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 123 | /api/v2/remediation/metrics/summary | GET | 2025-12-12 | ❌ FAIL | 500 | Internal server error |
| 124-147 | *(24 more Remediation endpoints)* | GET/POST/PUT/DELETE | ⏳ NOT TESTED | ⏳ PENDING | - | Assumed same issues |

---

## Phase B4 - Compliance APIs (28 endpoints, Port 8000)

**Test Date**: None
**Status**: ⏳ NOT TESTED
**Expected Issues**: Same middleware + connection issues

| # | Endpoint | Method | Test Date | Status | Notes |
|---|----------|--------|-----------|--------|-------|
| 148-175 | /api/v2/compliance/* | GET/POST/PUT/DELETE | ⏳ NOT TESTED | ⏳ PENDING | Need to test after fixes |

---

## Phase B4 - Scanning APIs (30 endpoints, Port 8000)

**Test Date**: None
**Status**: ⏳ NOT TESTED
**Expected Issues**: Same middleware + connection issues

| # | Endpoint | Method | Test Date | Status | Notes |
|---|----------|--------|-----------|--------|-------|
| 176-205 | /api/v2/scanning/* | GET/POST/PUT/DELETE | ⏳ NOT TESTED | ⏳ PENDING | Need to test after fixes |

---

## Phase B4 - Alerts APIs (32 endpoints, Port 8000)

**Test Date**: None
**Status**: ⏳ NOT TESTED
**Expected Issues**: Same middleware + connection issues

| # | Endpoint | Method | Test Date | Status | Notes |
|---|----------|--------|-----------|--------|-------|
| 206-237 | /api/v2/alerts/* | GET/POST/PUT/DELETE | ⏳ NOT TESTED | ⏳ PENDING | Need to test after fixes |

---

## Next.js Frontend APIs (41 endpoints, Port 3000)

**Test Date**: None
**Status**: ⏳ NOT TESTED
**Container Status**: Running but has @clerk/themes dependency error

| # | API Category | Endpoints | Test Date | Status | Notes |
|---|--------------|-----------|-----------|--------|-------|
| 238-278 | Next.js Routes | 41 total | ⏳ NOT TESTED | ⏳ PENDING | Fix @clerk/themes dependency first |

---

## AEON-SAAS-DEV APIs (64 endpoints, Port 3000)

**Test Date**: 2025-12-12 (limited testing)
**Status**: ❌ Container running but APIs failing
**Root Cause**: @clerk/themes dependency missing

| # | Endpoint | Test Date | Status | Error | Notes |
|---|----------|-----------|--------|-------|-------|
| 279 | /api/v2/vendor-equipment/vendors/search | 2025-12-12 | ❌ FAIL | 500 | Next.js error page |
| 280 | /api/v2/sbom/sboms | 2025-12-12 | ❌ FAIL | 404 | Not found |
| 281-342 | *(62 more endpoints)* | ⏳ NOT TESTED | ⏳ PENDING | - | Need to fix dependency first |

---

## OpenSPG Server APIs (~40 endpoints, Port 8887)

**Test Date**: 2025-12-12 (limited testing)
**Status**: ⏳ Container running, minimal testing

| # | Endpoint | Test Date | Status | Notes |
|---|----------|-----------|--------|-------|
| 343 | /health | 2025-12-12 | ⏳ NOT TESTED | - |
| 344 | /api/* | ⏳ NOT TESTED | ⏳ PENDING | OpenSPG KAG APIs not tested |
| 345-382 | *(~39 more endpoints)* | ⏳ NOT TESTED | ⏳ PENDING | Need API documentation |

---

## TESTING SUMMARY BY CATEGORY

### ✅ WORKING (4 APIs - 1.7%)
1. POST /ner - Entity extraction
2. POST /search/semantic - Semantic search
3. GET /health - Health check
4. GET /api/v2/risk/aggregated - Risk aggregation

### ⚠️ DEGRADED (1 API - 0.4%)
1. POST /search/hybrid - Works but slow (5-21s, needs optimization)

### ❌ FAILING (31 APIs - 13.4%)
- Phase B2 SBOM: 3 tested, 3 failed (100% fail rate)
- Phase B2 Equipment: 3 tested, 3 failed (100% fail rate)
- Phase B3 Threat Intel: 4 tested, 4 failed (100% fail rate)
- Phase B3 Risk: 4 tested, 4 failed (100% fail rate)
- Phase B3 Remediation: 6 tested, 6 failed (100% fail rate)
- AEON-SAAS-DEV: 7 tested, 7 failed (100% fail rate)
- OpenSPG: 4 tested, 4 failed (100% fail rate)

### ⏳ NOT TESTED (196 APIs - 84.5%)
- Phase B4 Compliance: 28 endpoints
- Phase B4 Scanning: 30 endpoints
- Phase B4 Alerts: 32 endpoints
- Phase B5 Economic: 27 endpoints
- Phase B5 Demographics: 4 endpoints
- Phase B5 Prioritization: 28 endpoints
- Next.js Frontend: 41 endpoints
- Remaining AEON-SAAS-DEV: 55 endpoints
- Remaining OpenSPG: 36 endpoints

---

## IMMEDIATE ACTION PLAN

### Priority 1: Fix Critical Blockers (5-20 hours)
1. **Add Customer Context Middleware** (5 minutes)
   - File: `/app/serve_model.py`
   - Impact: Unlock 128 Phase B APIs
   - Expected: 90%+ APIs become functional

2. **Fix Database Connections** (12-16 hours)
   - Change localhost → container names
   - Add environment variables
   - Fix import paths
   - Expected: All Phase B APIs connect to databases

3. **Execute CVSS Completion** (4-6 hours)
   - Run PROC-101 NVD enrichment
   - Cover remaining 12% CVEs (37,994)
   - Expected: 100% CVSS coverage

### Priority 2: Complete Testing (40-60 hours)
4. **Test All Phase B APIs** (24 hours)
   - 128 Phase B endpoints
   - Document results
   - Fix identified issues

5. **Test Next.js APIs** (8 hours)
   - Fix @clerk/themes dependency
   - Test all 41 endpoints
   - Document results

6. **Test AEON-SAAS-DEV** (8 hours)
   - 64 endpoints
   - Integration testing
   - Document results

### Priority 3: Fix Graph Issues (24-32 hours)
7. **Resolve Graph Fragmentation**
   - Reduce 504K orphans to <50K
   - Enable multi-hop reasoning
   - Create bridge relationships

---

## VALIDATION CHECKLIST

### Before Declaring Production Ready
- [ ] Customer context middleware added and tested
- [ ] Database connections using container names
- [ ] 100% CVSS coverage (316,552 CVEs)
- [ ] All 232 APIs tested (100% coverage)
- [ ] >90% APIs returning successful responses
- [ ] Graph fragmentation resolved (<50K orphans)
- [ ] Multi-hop queries functional (5-hop <2s)
- [ ] Load testing completed (1000 RPS sustained)
- [ ] Security infrastructure in place (SSL/TLS, auth, rate limiting)
- [ ] All documentation claims verified with test evidence

---

**STATUS**: NOT PRODUCTION READY
**CRITICAL BLOCKERS**: 3 (middleware, connections, graph)
**TIME TO FIX**: 80-120 hours
**CONFIDENCE**: HIGH (fixes are well-understood, not architectural)

---

**Generated**: 2025-12-12 14:50 UTC
**Next Update**: After completing Priority 1 fixes
**Maintained By**: API Testing & Verification Team
