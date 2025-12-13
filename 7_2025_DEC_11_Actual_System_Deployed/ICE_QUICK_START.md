# ICE PRIORITIZATION - QUICK START GUIDE

**Version:** 1.0.0
**Date:** 2025-12-12
**For:** Development Team

---

## 🎯 START HERE: Sprint 1 (Next 2 Weeks)

### Week 1-2 Focus: Foundation APIs (15 APIs)

**Team Assignment:**
- **Developer A**: SBOM APIs (8 endpoints)
- **Developer B**: Equipment APIs (7 endpoints)
- **Tech Lead**: Database schemas + API architecture
- **QA**: API testing framework setup

---

## 📋 SPRINT 1 TASK BREAKDOWN

### Developer A: SBOM Analysis (8 APIs)

#### Day 1-3: Core SBOM Ingestion
```
✅ POST /sbom/analyze
   - Accept CycloneDX/SPDX format
   - Parse components and dependencies
   - Store in Neo4j graph
   - Return SBOM ID
   Time: 3 days

✅ GET /sbom/{sbom_id}
   - Retrieve SBOM details
   - Include component count, vulnerability summary
   Time: 1 day
```

#### Day 4-6: Vulnerability Correlation
```
✅ GET /sbom/components/{id}/vulnerabilities
   - Query Neo4j for CVE relationships
   - Return CVSS scores, exploitability
   Time: 4 days

✅ POST /sbom/dependencies/map
   - Build dependency tree
   - Identify transitive vulnerabilities
   Time: 5 days
```

#### Day 7-10: Supporting APIs
```
✅ GET /sbom/licenses
   - Extract license info from SBOM
   Time: 2 days

✅ GET /sbom/summary
   - Aggregate component stats
   Time: 1 day

✅ GET /sbom/components/search
   - Semantic search via Qdrant
   Time: 2 days

✅ GET /sbom/export
   - Export SBOM as JSON
   Time: 1 day
```

**Total:** 8 APIs in 10 days

---

### Developer B: Equipment Lifecycle (7 APIs)

#### Day 1-3: Core Equipment CRUD
```
✅ POST /equipment
   - Create equipment record
   - Vendor, model, lifecycle stage
   Time: 2 days

✅ GET /equipment/{equipment_id}
   - Retrieve equipment details
   Time: 1 day

✅ GET /equipment/search
   - Semantic search for equipment
   Time: 3 days
```

#### Day 4-6: Lifecycle Tracking
```
✅ PUT /equipment/{id}/lifecycle
   - Update lifecycle stage
   - State machine: new → production → eol → decommissioned
   Time: 2 days

✅ GET /equipment/eol-report
   - Find EOL equipment
   - Sync with vendor EOL databases
   Time: 4 days
```

#### Day 7-10: Supporting APIs
```
✅ GET /equipment/summary
   - Equipment stats dashboard
   Time: 1 day

✅ GET /equipment/by-vendor
   - Group equipment by vendor
   Time: 1 day
```

**Total:** 7 APIs in 10 days

---

## 🗄️ DATABASE SCHEMAS (Tech Lead)

### Neo4j Node Types

**SBOM Schema:**
```cypher
CREATE (s:SBOM {
  sbom_id: string,
  format: "cyclonedx" | "spdx",
  project_name: string,
  version: string,
  created_at: datetime,
  customer_id: string
})

CREATE (c:Component {
  component_id: string,
  name: string,
  version: string,
  purl: string,
  cpe: string,
  license: string,
  customer_id: string
})

CREATE (s)-[:CONTAINS]->(c)
CREATE (c)-[:DEPENDS_ON]->(c)
CREATE (c)-[:HAS_VULNERABILITY]->(v:CVE)
```

**Equipment Schema:**
```cypher
CREATE (e:Equipment {
  equipment_id: string,
  vendor: string,
  model: string,
  serial_number: string,
  lifecycle_stage: "new" | "production" | "eol" | "decommissioned",
  install_date: datetime,
  eol_date: datetime,
  customer_id: string
})

CREATE (e)-[:MANUFACTURED_BY]->(v:Vendor)
CREATE (e)-[:HAS_VULNERABILITY]->(cve:CVE)
```

---

## 🔌 API AUTHENTICATION

### Multi-Tenant Headers (REQUIRED)

**Every API request must include:**
```http
X-Customer-ID: customer_001
X-Namespace: customer_production
X-User-ID: analyst_123
X-Access-Level: read
```

**Access Levels:**
- `read`: Read-only access
- `write`: Read + write operations
- `admin`: Full administrative access

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/v2/sbom/analyze \
  -H "Content-Type: application/json" \
  -H "X-Customer-ID: customer_001" \
  -H "X-Access-Level: write" \
  -d @sbom.json
```

---

## 🧪 TESTING REQUIREMENTS

### API Testing Checklist

**Unit Tests (Jest/Pytest):**
- ✅ Request validation (schema checks)
- ✅ Business logic (SBOM parsing, equipment state transitions)
- ✅ Error handling (invalid inputs, missing data)
- ✅ Customer isolation (data leakage prevention)

**Integration Tests:**
- ✅ Neo4j queries (graph traversal, relationship creation)
- ✅ Qdrant semantic search (vector similarity)
- ✅ Multi-tenant isolation (customer data separation)
- ✅ End-to-end workflows (upload SBOM → find vulnerabilities)

**Performance Tests:**
- ✅ Response time < 500ms (P95)
- ✅ Concurrent requests (100 users)
- ✅ Large SBOM files (10K+ components)

---

## 📊 SUCCESS CRITERIA (Sprint 1)

### Must-Have Deliverables

**Functional:**
- [ ] Upload SBOM file (CycloneDX format)
- [ ] Extract vulnerabilities from SBOM
- [ ] Create equipment record
- [ ] Track equipment EOL status
- [ ] Search equipment by vendor/model
- [ ] Multi-tenant data isolation verified

**Technical:**
- [ ] All 15 APIs deployed to dev environment
- [ ] Neo4j schemas created and tested
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Unit test coverage > 80%
- [ ] Integration tests passing

**Quality:**
- [ ] No P0/P1 bugs
- [ ] API response time < 500ms
- [ ] Customer isolation validated
- [ ] Security review passed

---

## 🚀 SPRINT 2 PREVIEW (Week 3-4)

**Next Sprint Focus:** Threat Intelligence + Economic Dashboards

**APIs to Build (32 APIs):**
- Threat actors (7 APIs)
- Campaigns (5 APIs)
- MITRE mapping (6 APIs)
- Economic cost/ROI (14 APIs)

**Team Expansion:**
- Add Data Engineer for threat feed integration
- Add Frontend Developer for dashboards

---

## 📞 DAILY STANDUP TEMPLATE

**What I did yesterday:**
- [ ] API endpoints completed
- [ ] Schema changes deployed
- [ ] Tests written/passing

**What I'm doing today:**
- [ ] API endpoints in progress
- [ ] Blockers/dependencies

**Blockers:**
- [ ] Waiting on: schema review, data access, etc.

---

## 🔗 RESOURCES

**Documentation:**
- ICE Prioritization Matrix: `/7_2025_DEC_11_Actual_System_Deployed/ICE_PRIORITIZATION_MATRIX.md`
- API Complete Reference: `/7_2025_DEC_11_Actual_System_Deployed/docs/API_COMPLETE_REFERENCE.md`
- Neo4j Connection: `bolt://localhost:7687` (user: neo4j, pass: neo4j@openspg)
- Qdrant Connection: `http://localhost:6333`

**Code Repositories:**
- Backend API: `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/backend/`
- Frontend Dashboard: `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/frontend/`
- Database Migrations: `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/migrations/`

**External APIs:**
- NIST NVD: `https://nvd.nist.gov/developers`
- FIRST EPSS: `https://api.first.org/data/v1/epss`
- CISA KEV: `https://www.cisa.gov/known-exploited-vulnerabilities-catalog`

---

## 🎓 TRAINING RESOURCES

**SBOM Formats:**
- CycloneDX Specification: https://cyclonedx.org/specification/
- SPDX Specification: https://spdx.dev/specifications/

**Graph Database:**
- Neo4j Cypher Tutorial: https://neo4j.com/developer/cypher/
- Graph Data Science: https://neo4j.com/docs/graph-data-science/

**Vector Search:**
- Qdrant Documentation: https://qdrant.tech/documentation/
- Semantic Search Best Practices: https://qdrant.tech/documentation/tutorials/search-beginners/

---

## 🏁 GET STARTED NOW

**Step 1:** Review ICE matrix (10 minutes)
- Read: `/7_2025_DEC_11_Actual_System_Deployed/ICE_PRIORITIZATION_MATRIX.md`

**Step 2:** Claim your APIs (5 minutes)
- Developer A: SBOM APIs (1-8)
- Developer B: Equipment APIs (9-15)

**Step 3:** Create branches (5 minutes)
```bash
git checkout -b sprint1-sbom-apis
git checkout -b sprint1-equipment-apis
```

**Step 4:** Start coding (today!)
- Begin with: `POST /sbom/analyze` and `POST /equipment`

---

**QUESTIONS?** Contact Tech Lead or Product Owner

**LET'S BUILD! 🚀**
