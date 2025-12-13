# API QUICK REFERENCE CARD

**48 Working APIs** | **237+ Documented** | **Updated**: 2025-12-12

---

## 🚀 FASTEST START (30 Seconds)

```bash
# Test system health
curl http://localhost:3000/api/health

# Extract entities from text (no auth)
curl -X POST http://localhost:8000/ner \
  -H "Content-Type: application/json" \
  -d '{"text": "APT29 exploited CVE-2024-12345"}'

# Search semantically (no auth)
curl -X POST http://localhost:8000/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query": "ransomware", "limit": 5}'
```

---

## 📊 API CATEGORIES (48 Total)

### **Threat Intelligence** (8 APIs) - Port 3000
- `/api/threat-intel/analytics` - MITRE ATT&CK, Kill Chain
- `/api/threat-intel/ics` - Industrial threats
- `/api/threat-intel/landscape` - Threat overview
- `/api/threat-intel/vulnerabilities` - CVE intelligence
- `/api/threats/geographic` - Geographic threats
- `/api/threats/ics` - ICS threats

### **Dashboard** (4 APIs) - Port 3000
- `/api/dashboard/metrics` - System KPIs
- `/api/dashboard/activity` - Recent activity
- `/api/dashboard/distribution` - Data distribution
- `/api/health` - System health (**No auth**)

### **Analytics** (7 APIs) - Port 3000
- `/api/analytics/metrics` - Analytics KPIs
- `/api/analytics/timeseries` - Time series
- `/api/analytics/trends/cve` - CVE trends
- `/api/analytics/trends/threat-timeline` - Threat timeline
- `/api/analytics/trends/seasonality` - Seasonal patterns
- `/api/analytics/export` - Data export

### **Graph & Neo4j** (3 APIs) - Port 3000
- `/api/graph/query` - Cypher execution
- `/api/neo4j/statistics` - DB stats
- `/api/neo4j/cyber-statistics` - Cyber stats

### **NER11** (5 APIs) - Port 8000 (**No auth**)
- `POST /ner` - Entity extraction (60 types)
- `POST /search/semantic` - Vector search
- `POST /search/hybrid` - Vector + Graph (20-hop)
- `GET /health` - Health check
- `GET /info` - Model info (566 fine-grained types)

### **Pipeline** (2 APIs) - Port 3000
- `/api/pipeline/process` - Submit documents
- `/api/pipeline/status/[jobId]` - Job status

### **Query Control** (7 APIs) - Port 3000
- `/api/query-control/queries` - List queries
- `/api/query-control/queries/[queryId]` - Query details
- `/api/query-control/queries/[queryId]/pause` - Pause
- `/api/query-control/queries/[queryId]/resume` - Resume
- `/api/query-control/queries/[queryId]/checkpoints` - Checkpoints
- `/api/query-control/queries/[queryId]/model` - Change model
- `/api/query-control/queries/[queryId]/permissions` - Change permissions

### **Other** (12 APIs) - Port 3000
- Customers (2), Observability (3), Tags (3), Utilities (4)

---

## 🔑 AUTHENTICATION

**Most APIs Require Clerk Auth**:
```typescript
headers: {
  "Authorization": "Bearer YOUR_CLERK_TOKEN",
  "X-Customer-ID": "your-customer-id"
}
```

**No Auth Required**:
- `/api/health`
- All NER11 APIs (port 8000)
- Database direct access

---

## 🏛️ COMPLIANCE FRAMEWORKS

**Available in Neo4j** (32,907 nodes):
1. NERC CIP (100) - Energy sector
2. IEC 62443 (66K controls) - Industrial security
3. Industry Standards (2,567) - Dam, Transport, Commercial
4. SBOM Compliance (30,000+) - Software supply chain

**Planned** (Phase B4):
- NIST CSF, ISO 27001, SOC 2, PCI DSS, HIPAA, GDPR

**Assessment Questions**: 1 node (minimal - question bank not loaded)

---

## 📚 DOCUMENTATION

**Essential Reading**:
1. `FRONTEND_QUICK_START_ACTUAL_APIS.md` - Start here!
2. `IMPLEMENTED_APIS_COMPLETE_REFERENCE.md` - All 41 Next.js APIs
3. `NER11_API_COMPLETE_GUIDE.md` - All 5 NER APIs
4. `API_ARCHITECTURE_DIAGRAMS.md` - Visual architecture

**Implementation Plans**:
- `1_enhance/` - Plans for 196 additional APIs (Phases B2-B5)

---

**Last Updated**: 2025-12-12 02:55 UTC
**Status**: ✅ FACTUAL - Based on container inspection and database queries
