# Frontend API Reference - Working APIs

**Last Updated**: 2025-12-12 23:19
**Total Working**: 37 APIs
**Status**: Verified via TEST_ALL_APIS_DEFINITIVE.sh

---

## 🚀 QUICK START

**Base URL**: `http://localhost:8000`
**Auth Header**: `-H "x-customer-id: dev"` (for Phase B APIs)

---

## ✅ WORKING APIS (37 Total)

### **Category: NER & Search** (2 APIs)

1. **POST /ner** - Extract entities
```bash
curl -X POST http://localhost:8000/ner \
  -H "Content-Type: application/json" \
  -d '{"text":"APT29 exploited CVE-2024-12345"}'
```

2. **GET /health** - Service health
```bash
curl http://localhost:8000/health
```

### **Category: SBOM Analysis** (7 APIs)

3. **GET /api/v2/sbom/sboms** - List SBOMs
```bash
curl http://localhost:8000/api/v2/sbom/sboms -H "x-customer-id: dev"
```

4-9. *[Additional SBOM APIs - see full list in report]*

### **Category: Threat Intelligence** (12 APIs)

10. **GET /api/v2/threat-intel/iocs/active** - Active IOCs
```bash
curl http://localhost:8000/api/v2/threat-intel/iocs/active -H "x-customer-id: dev"
```

11-21. *[Additional threat intel APIs]*

### **Category: Risk Scoring** (9 APIs)

22. **GET /api/v2/risk/dashboard** - Risk dashboard
```bash
curl http://localhost:8000/api/v2/risk/dashboard -H "x-customer-id: dev"
```

23-30. *[Additional risk APIs]*

### **Category: Equipment** (5 APIs)

31. **GET /api/v2/equipment/dashboard/summary** - Equipment overview
```bash
curl http://localhost:8000/api/v2/equipment/dashboard/summary -H "x-customer-id: dev"
```

32-35. *[Additional equipment APIs]*

### **Category: System** (2 APIs)

36. **GET /info** - System info
37. **POST /search/hybrid** - Hybrid search

---

## 📍 STANDARDIZED LOCATION

**This document**: `7_2025_DEC_11_Actual_System_Deployed/FRONTEND_API_REFERENCE.md`

**Always check here for working APIs** ✅
