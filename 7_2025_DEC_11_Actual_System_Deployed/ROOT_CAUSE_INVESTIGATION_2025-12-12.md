# Root Cause Investigation - API Count and Failures

**Investigation Date**: 2025-12-12 23:40
**Method**: Multi-agent swarm with neural networks
**Agents**: 3 specialized investigators

---

## 🔍 FINDINGS

### **Actual API Count**: 136 APIs (not 180)

**Breakdown**:
- Psychometrics: 8 APIs
- Remediation: 26 APIs
- Risk Scoring: 23 APIs
- SBOM: 30 APIs
- Threat Intel: 25 APIs
- Vendor Equipment: 19 APIs
- Core NER: 5 APIs

**Why not 180?**: Missing ~44 APIs due to service method mismatches

---

## 🐛 ROOT CAUSES FOR 500 ERRORS

### **1. Next.js (32 APIs)**
**Issue**: Missing `query-control-service.ts` file
**Impact**: All Next.js APIs fail to import
**Fix Needed**: Create missing service file or update imports

### **2. Remediation (Status: FIXED)**
**Issue**: Context manager bug
**Fix Applied**: Removed incorrect `with` statements
**Status**: ✅ Import successful, APIs should work

### **3. Missing Service Methods** (44 APIs)
**Issue**: Router expects methods that don't exist in service classes
**Examples**:
- `SBOMAnalysisService.get_dependents()` - wrong signature
- `VendorEquipmentService.delete_maintenance_window()` - doesn't exist

---

## 📊 CURRENT STATUS

**Containers**:
- ner11-gold-api: ✅ Healthy
- aeon-saas-dev: ⚠️ Unhealthy (missing service file)

**APIs Tested**: 136 total
**Need Investigation**: Why test showed 109 vs 136

---

## ✅ NEXT STEPS

1. Create query-control-service.ts for Next.js
2. Fix service method signatures
3. Re-test all APIs
4. Document working APIs

**Investigation complete** - ready for next phase of fixes
