# PHASE B API ACTIVATION ROADMAP

**Created**: 2025-12-12 03:25 UTC
**Purpose**: Systematic plan to activate 237 existing Phase B APIs
**Status**: READY FOR EXECUTION

---

## 🎯 SITUATION ASSESSMENT

**Current Reality**:
- ✅ **48 APIs working** (5 NER + 41 Next.js + 2 Database)
- ⏳ **237 APIs exist but disabled** (code in ner11-gold-api:/app/api/)
- 🐛 **Bugs blocking activation**: RiskTrend enum, Qdrant localhost hardcoding

**The Good News**: Code exists, bugs are fixable, not starting from scratch

**The Task**: Debug and activate existing Phase B code systematically

---

## 🐛 IDENTIFIED BUGS TO FIX

### **Bug #1: RiskTrend Enum Missing Values**

**File**: `/app/api/risk_scoring/risk_service.py:275`
**Error**: `AttributeError: INCREASING`
**Fix**: Define RiskTrend enum with required values
```python
class RiskTrend(str, Enum):
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    EMERGING = "emerging"
```
**Effort**: 15 minutes
**Impact**: Unblocks risk_scoring module

---

### **Bug #2: Qdrant Connection Hardcoded**

**Multiple Files**: Sprint 1 code uses `localhost:6333`
**Should Use**: `openspg-qdrant:6333` (Docker network)
**Fix**: Update all QdrantClient() calls
**Effort**: 30 minutes
**Impact**: Unblocks all Qdrant-dependent modules

---

### **Bug #3: Import Errors** (To be discovered during activation)

**Approach**: Fix incrementally as discovered
**Effort**: 1-2 days
**Method**: Enable one router at a time, fix imports, test

---

## 📅 ACTIVATION PLAN (3-Day Sprint)

### **Day 1: Bug Fixes** (6 hours)

**Morning** (9am-12pm):
1. Fix RiskTrend enum (15 min)
2. Fix all Qdrant localhost→openspg-qdrant (30 min)
3. Test import of all 11 routers (1 hour)
4. Fix any import errors discovered (1.5 hours)

**Afternoon** (1pm-5pm):
5. Enable and test sbom_router (1 hour)
6. Enable and test vendor_router (1 hour)
7. Fix any runtime errors (2 hours)

**Deliverable**: 2 router modules working (SBOM + Vendor Equipment)

---

### **Day 2: Phase B2-B3 Activation** (8 hours)

**Phase B2 Completion**:
1. Verify SBOM APIs (32 endpoints) - 2 hours
2. Verify Vendor Equipment APIs (28 endpoints) - 2 hours
3. Fix any bugs found - 1 hour

**Phase B3 Activation**:
4. Enable threat_intelligence router - 1 hour
5. Enable risk_scoring router (post bug-fix) - 1 hour
6. Enable remediation router - 1 hour

**Deliverable**: 142 APIs operational (Phase B2 + B3)

---

### **Day 3: Phase B4-B5 Activation** (8 hours)

**Phase B4**:
1. Enable compliance_mapping router - 1.5 hours
2. Enable automated_scanning router - 1.5 hours
3. Enable alert_management router - 1.5 hours

**Phase B5**:
4. Enable economic_impact router - 1 hour
5. Enable demographics router - 1 hour
6. Enable prioritization router - 1 hour

**Final Testing**:
7. Comprehensive endpoint testing - 1.5 hours

**Deliverable**: All 237 Phase B APIs operational

---

## ✅ ACCEPTANCE CRITERIA

**For Each Router**:
- [ ] Imports without errors
- [ ] Registers with FastAPI app
- [ ] Container starts successfully
- [ ] Endpoints return 200 (not 404/500)
- [ ] Multi-tenant isolation works
- [ ] Documented with examples

**Overall**:
- [ ] All 237 endpoints accessible
- [ ] Swagger docs show all routes
- [ ] Test suite passes (>80% coverage)
- [ ] Performance <500ms p95
- [ ] Updated documentation in 7_2025_DEC_11

---

## 🔧 EXECUTION COMMANDS

### **Fix Bug #1: RiskTrend Enum**
```bash
docker exec ner11-gold-api sed -i '275i\\    INCREASING = "increasing"\\n    DECREASING = "decreasing"\\n    STABLE = "stable"' /app/api/risk_scoring/risk_models.py
```

### **Fix Bug #2: Qdrant Connection**
```bash
# Find and replace in all files
docker exec ner11-gold-api find /app/api -name "*.py" -exec sed -i 's/localhost:6333/openspg-qdrant:6333/g' {} \;
```

### **Enable All Routers**
Edit `/app/serve_model.py`:
- Change `PHASE_B_ROUTERS_AVAILABLE = False` to `True`
- Uncomment import and registration blocks

### **Restart and Test**
```bash
docker restart ner11-gold-api
sleep 10
curl http://localhost:8000/docs | grep "/api/v2/"
curl http://localhost:8000/api/v2/sbom/summary -H "X-Customer-ID: test"
```

---

## 📊 EFFORT ESTIMATE

| Phase | APIs | Bugs to Fix | Time | Deliverable |
|-------|------|-------------|------|-------------|
| Day 1 | 60 | 5-10 | 6 hrs | Phase B2 working |
| Day 2 | 82 | 3-5 | 8 hrs | Phase B2+B3 working |
| Day 3 | 95 | 2-4 | 8 hrs | All Phase B working |
| **Total** | **237** | **10-19** | **22 hrs** | **285 total APIs** |

**Resource**: 1 senior backend developer
**Risk**: Low (code exists, bugs are straightforward)
**Confidence**: High (>90%)

---

## 🚀 POST-ACTIVATION

### **Immediate** (After activation):
1. Update `VERIFIED_CAPABILITIES_FINAL.md` with all 285 APIs
2. Update Swagger documentation
3. Notify frontend team APIs are live
4. Execute integration tests

### **This Week**:
5. Execute 3 ready procedures (PROC-116, 117, 133)
6. Execute PROC-114 (Psychometric) → Unlock Layer 6
7. Load Kaggle datasets for 6 procedures

### **This Month**:
8. Execute all Kaggle-ready procedures
9. Activate Layer 6 psychodynamic predictions
10. Full compliance framework loading (NIST, ISO, etc.)

---

**Next Step**: Execute Day 1 bug fixes to activate first 60 APIs (Phase B2)

Ready to proceed when you are. 🎯
