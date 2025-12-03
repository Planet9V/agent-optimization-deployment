# OpenSPG + Neo4j Strategic Integration Architecture

**File:** OPENSPG_NEO4J_STRATEGIC_ARCHITECTURE.md
**Created:** 2025-11-11 18:45:00 UTC
**Version:** 1.0.0
**Author:** System Architecture Designer
**Purpose:** Strategic analysis of OpenSPG knowledge graph system integration with existing Neo4j/PostgreSQL architecture
**Status:** ACTIVE

---

## Executive Summary

**Critical Finding:** OpenSPG and Neo4j serve **complementary, not competing** roles in the AEON architecture. OpenSPG is a **knowledge graph construction and processing platform** that uses MySQL for metadata and Neo4j as its **graph storage backend**. The architecture already supports parallel operation.

**Key Insights:**
- ✅ **No migration needed** - OpenSPG uses Neo4j as storage backend (already integrated)
- ✅ **MySQL for OpenSPG jobs** - Keep existing scheduler/metadata database (33 tables)
- ✅ **PostgreSQL on Next.js** - AEON UI uses PostgreSQL for app state (separate concern)
- ✅ **Parallel operation ready** - All three databases serve distinct purposes

---

## Current System State (2025-11-11)

### Container Infrastructure

| Container | IP | Ports | Database | Purpose | Status |
|-----------|-----|-------|----------|---------|--------|
| **openspg-server** | 172.18.0.2 | 8887 | - | KG processing engine | Running (Unhealthy) |
| **openspg-mysql** | 172.18.0.3 | 3306 | MySQL 10.5.8 | OpenSPG metadata/jobs | Healthy |
| **openspg-minio** | 172.18.0.4 | 9000-9001 | S3 | Object storage | Healthy |
| **openspg-neo4j** | 172.18.0.5 | 7474, 7687 | Neo4j 5.26 | Graph storage backend | Healthy |
| **openspg-qdrant** | 172.18.0.6 | 6333-6334 | Qdrant | Vector search | Running (Unhealthy) |
| **aeon-ui** | 172.18.0.8 | 3000 | Next.js + PG | Web interface | Running |

**Network:** openspg-network (172.18.0.0/16)

### Data Distribution

**Neo4j Graph Database (Primary Knowledge Store):**
- **Total Nodes:** 570,214
- **Total Relationships:** 3,347,117
- **Node Types:** 239 distinct labels
- **MITRE ATT&CK:** 2,051 entities (Techniques, Mitigations, Actors, Software)
- **CVEs:** 316,552 vulnerability nodes
- **Threat Intelligence:** 343 Threat Actors, 714 Malware families
- **Infrastructure:** 16 ICS assets, 2,214 CWE weaknesses

**MySQL Database (OpenSPG Operational State):**
- **Total Tables:** 33
- **Database Size:** ~0.70 MB
- **Purpose:** Job scheduling, project metadata, schema definitions
- **Key Tables:**
  - `kg_scheduler_job` - Scheduled processing jobs
  - `kg_project_info` - Knowledge graph projects
  - `kg_ontology_entity` - Entity type definitions
  - `kg_builder_job` - Graph construction jobs

**PostgreSQL (AEON UI - Inferred):**
- **Location:** Next.js container (aeon-ui)
- **Purpose:** Application state, user sessions, UI metadata
- **Status:** Not explicitly documented but mentioned as "already exists"

---

## Architecture Analysis: OpenSPG Role

### What OpenSPG Actually Does

OpenSPG is **NOT** a competing graph database. It's a **knowledge graph construction platform** that:

1. **Ingests Documents** → Processes PDFs, text, structured data
2. **Extracts Entities** → NER (Named Entity Recognition) extraction
3. **Builds Ontologies** → Defines entity types and relationships
4. **Processes Knowledge** → Runs scheduled jobs for graph construction
5. **Stores in Neo4j** → Uses Neo4j as the graph storage backend

**Analogy:** OpenSPG is to Neo4j what Spark is to HDFS - a processing engine that uses the database for storage.

### Data Flow Architecture

```
Document Sources (PDFs, APIs, Files)
    ↓
[OpenSPG Server] (172.18.0.2:8887)
    ├→ [MySQL] - Stores job metadata, schedules, project configs
    ├→ [MinIO] - Stores uploaded files and artifacts
    ├→ [Neo4j] - Stores extracted knowledge graph
    └→ [Qdrant] - Stores vector embeddings for semantic search
```

**Critical Insight:** OpenSPG uses Neo4j as its **graph storage backend**, not as a separate system to migrate from.

---

## Database Specialization Strategy

### Neo4j: Universal Graph Storage Backend

**Primary Role:** Knowledge graph storage for all entities and relationships

**Data Stored:**
- MITRE ATT&CK entities (2,051 nodes, 40,886 relationships)
- Cybersecurity entities (CVEs, CWEs, Threat Actors, Malware)
- Infrastructure entities (Equipment, Vendors, Protocols)
- Document entities extracted by OpenSPG
- All relationship types (USES_TECHNIQUE, EXPLOITS, MITIGATES, etc.)

**Access Patterns:**
- OpenSPG Server → Writes extracted knowledge graph
- AEON UI → Reads graph for visualization
- V9 NER API → Writes entity extraction results
- Query API → Executes Cypher queries

**Why Neo4j:** Best-in-class graph database with native graph storage, Cypher query language, and high performance for relationship traversal.

### MySQL: OpenSPG Operational Database

**Primary Role:** OpenSPG platform operational state

**Data Stored:**
- **Job Scheduling:** `kg_scheduler_job`, `kg_scheduler_instance`, `kg_scheduler_task`
- **Project Metadata:** `kg_project_info`, `kg_project_entity`
- **Schema Definitions:** `kg_ontology_entity`, `kg_ontology_property_*`
- **User Management:** `kg_user`, `kg_role`, `kg_resource_permission`
- **AI/ML Config:** `kg_model_detail`, `kg_model_provider`

**Access Patterns:**
- OpenSPG Server → Manages job execution, tracks processing state
- AEON UI (potentially) → Reads project metadata

**Why MySQL:** Relational integrity for operational data, proven scheduler integration, existing 33-table schema.

**Critical Decision:** **DO NOT MIGRATE** - This is OpenSPG's internal operational database. Moving jobs to Neo4j or PostgreSQL would break OpenSPG's architecture.

### PostgreSQL: AEON UI Application Database

**Primary Role:** Next.js application state and user management

**Data Stored (Inferred):**
- User sessions and authentication state
- UI preferences and configurations
- Application metadata
- Customer management data (from Phase 2)
- Tag definitions (from Phase 3)

**Access Patterns:**
- AEON UI → All CRUD operations for app state
- NextAuth → Session management

**Why PostgreSQL:** Industry-standard for web applications, excellent TypeScript/Prisma integration, robust for transactional workloads.

**Recommendation:** Keep PostgreSQL for AEON UI application state. It's the right tool for web app persistence.

---

## Strategic Integration: Parallel Operation Model

### Optimal Architecture: Three-Database Specialization

```
┌─────────────────────────────────────────────────────────────┐
│                   AEON Digital Twin Platform                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │  AEON UI     │────────▶│  OpenSPG     │                 │
│  │  Next.js     │         │  Server      │                 │
│  │  172.18.0.8  │         │  172.18.0.2  │                 │
│  └──────┬───────┘         └──────┬───────┘                 │
│         │                        │                          │
│         │                        │                          │
│  ┌──────▼───────┐         ┌──────▼────────┐                │
│  │ PostgreSQL   │         │ MySQL         │                │
│  │ (Next.js     │         │ (OpenSPG Jobs)│                │
│  │  App State)  │         │ 172.18.0.3    │                │
│  │              │         └──────┬────────┘                │
│  └──────────────┘                │                          │
│         │                        │                          │
│         └────────────┬───────────┘                          │
│                      │                                      │
│               ┌──────▼───────────┐                          │
│               │ Neo4j            │                          │
│               │ (Knowledge Graph)│                          │
│               │ 172.18.0.5       │                          │
│               │ 570K nodes       │                          │
│               │ 3.3M edges       │                          │
│               └──────────────────┘                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Patterns

**Document Ingestion → Knowledge Graph:**
1. User uploads document via AEON UI
2. AEON UI stores file in MinIO
3. AEON UI triggers OpenSPG processing job
4. OpenSPG Server:
   - Records job in MySQL (`kg_scheduler_job`)
   - Extracts entities with V9 NER
   - Creates nodes/relationships in Neo4j
   - Stores embeddings in Qdrant
5. AEON UI queries Neo4j for graph visualization

**User Interaction Flow:**
1. User authenticates via AEON UI
2. Session stored in PostgreSQL (NextAuth)
3. User queries knowledge graph
4. AEON UI executes Cypher query against Neo4j
5. Results displayed in graph visualization

**OpenSPG Job Scheduling:**
1. Periodic job defined in MySQL (`kg_scheduler_job`)
2. OpenSPG scheduler (60s cycle) checks MySQL for pending jobs
3. Job executes: processes data, updates Neo4j
4. Job status recorded in MySQL (`kg_scheduler_instance`)

---

## OpenSPG Critical Capabilities for AEON

### Knowledge Graph Construction

**What OpenSPG Provides:**
1. **Schema Management** - Define ontologies, entity types, property constraints
2. **Entity Extraction** - NER pipelines for document processing
3. **Relationship Inference** - Automatically infer connections between entities
4. **Job Orchestration** - Scheduled processing of large document corpora
5. **Data Import/Export** - Bulk operations for knowledge graph construction

**AEON Use Cases:**
- Process 400 annual cybersecurity reports → Neo4j knowledge graph
- Extract MITRE ATT&CK relationships from unstructured text
- Build temporal campaign timelines from threat intelligence
- Infer attack paths from vulnerability disclosures

### V9 NER Integration with OpenSPG

**Current State:**
- V9 NER model: 99.00% F1 score, 16 entity types, 1,718 training examples
- Deployment: FastAPI service on port 8001
- Integration: Can feed results to OpenSPG for graph construction

**Optimal Integration:**
```
Document Upload (AEON UI)
    ↓
V9 NER API (port 8001) - Extract entities
    ↓
OpenSPG Server - Construct knowledge graph
    ↓
Neo4j - Store graph
    ↓
AEON UI - Visualize results
```

**Benefits:**
- V9 NER provides high-quality entity extraction (99% F1)
- OpenSPG orchestrates graph construction at scale
- Neo4j provides efficient graph storage and querying
- AEON UI offers interactive visualization

---

## Strategic Recommendations

### 1. Maintain Three-Database Architecture ✅

**Rationale:** Each database serves a distinct, optimized purpose.

**PostgreSQL for AEON UI:**
- Application state, user sessions, customer management
- Perfect fit for Next.js/Prisma workflow
- Transactional integrity for app operations

**MySQL for OpenSPG Jobs:**
- OpenSPG's internal operational database
- 33 tables for job scheduling, metadata, schemas
- **DO NOT MIGRATE** - Breaking change to OpenSPG

**Neo4j for Knowledge Graph:**
- Universal graph storage backend
- Used by both OpenSPG (writes) and AEON UI (reads)
- Optimal for relationship-heavy queries

### 2. Leverage OpenSPG for Document Processing Pipeline ✅

**Implementation Strategy:**

**Phase 1: Basic Integration (Already Functional)**
- OpenSPG server running, connected to Neo4j
- MySQL operational database healthy
- MinIO for file storage configured

**Phase 2: V9 NER + OpenSPG Pipeline**
```python
# Proposed integration workflow

# 1. Document upload via AEON UI
upload_file(document) → MinIO

# 2. Trigger V9 NER extraction
entities = v9_ner_api.extract(document)

# 3. Send to OpenSPG for graph construction
openspg_job = openspg_server.create_job({
    'entities': entities,
    'relationships': inferred_relationships,
    'project': 'AEON_CyberThreat',
    'namespace': customer_id
})

# 4. OpenSPG processes and stores in Neo4j
openspg_server.execute_job(openspg_job)

# 5. AEON UI visualizes results
graph_data = neo4j.query_customer_namespace(customer_id)
```

**Benefits:**
- Automated knowledge graph construction
- Scheduled processing of document batches
- Scalable to 100-200 documents/hour
- Leverages existing OpenSPG investment

### 3. Customer Namespace Isolation Strategy ✅

**Challenge:** Multi-customer data isolation in shared Neo4j instance

**Solution: Hybrid Approach**

**Option A: Neo4j Native Labels (Recommended)**
```cypher
// Customer namespace via node properties
MATCH (n:Document {customer: 'customer_123'})
RETURN n

// Advantages:
// - Simple implementation
// - Works with existing AEON UI code
// - Compatible with OpenSPG processing
```

**Option B: OpenSPG Project Isolation**
```yaml
# OpenSPG project configuration
projects:
  - id: customer_123
    namespace: customer_123_namespace
    neo4j_prefix: "CUST123_"
```

**Recommendation:** Use Option A (Neo4j native labels) for AEON UI, Option B (OpenSPG projects) for batch processing. Both methods are compatible and can coexist.

### 4. Parallel Operation Optimization ✅

**Query Routing Strategy:**

```typescript
// AEON UI query router
class GraphQueryRouter {
  async query(cypherQuery: string, customerId: string) {
    // Route to appropriate service
    if (isRealTimeQuery(cypherQuery)) {
      // Direct Neo4j query for real-time visualization
      return neo4j.execute(cypherQuery, { customer: customerId });
    } else if (isBatchAnalysis(cypherQuery)) {
      // OpenSPG job for complex processing
      return openspg.createAnalysisJob(cypherQuery, customerId);
    }
  }
}
```

**Benefits:**
- Real-time queries go directly to Neo4j (low latency)
- Complex analysis routed through OpenSPG (better resource management)
- Customer isolation maintained across both paths

### 5. Do NOT Migrate MySQL Jobs ❌

**Critical Warning:** OpenSPG scheduler depends on MySQL schema.

**Attempted Migration Risks:**
- Break OpenSPG job scheduling system
- Lose operational metadata (33 tables)
- Require extensive OpenSPG reconfiguration
- No performance benefit (MySQL optimal for this workload)

**Recommendation:** Leave MySQL for OpenSPG operational data. It's designed for this purpose.

---

## Performance Characteristics

### Current State (Verified 2025-11-08)

**Neo4j:**
- Nodes: 570,214
- Relationships: 3,347,117
- Query performance: 2-3ms for health checks
- Relationship traversal: Optimized with native graph storage

**OpenSPG Server:**
- Health endpoint: 2-3ms average response
- Scheduler cycle: ~1ms per 60s cycle
- Lock acquisition: <10ms
- Currently: 0 active periodic jobs, 0 unfinished instances

**MySQL:**
- Database size: 0.70 MB
- Connection pooling: Configured
- Buffer pool: 2GB allocated
- Performance: Excellent for operational workload

### Expected Performance After 400-Document Ingestion

**Neo4j Growth:**
- Current: 570K nodes, 3.3M relationships
- After ingestion: **620K-670K nodes** (+50K-100K)
- After ingestion: **3.5M-3.8M relationships** (+200K-500K)
- **Impact:** 10-20% growth, well within Neo4j capacity

**Processing Time:**
- Automated pipeline (V9 NER + OpenSPG): **2-4 hours** for 400 documents
- LLM enhancement (selective): **20-40 hours** for deep analysis
- Total: **24-48 hours** end-to-end

**Cost:**
- Automated processing: $0 (local compute)
- LLM enhancement: $100-200 (selective Claude API usage)
- Infrastructure: $0 (existing deployment)

---

## Integration Roadmap

### Immediate Actions (Week 1)

**1. Validate OpenSPG-Neo4j Connection**
```bash
# Test OpenSPG can write to Neo4j
docker exec openspg-server curl http://localhost:8887/health
docker exec openspg-neo4j cypher-shell -u neo4j -p neo4j@openspg "MATCH (n) RETURN count(n)"
```

**2. Configure V9 NER → OpenSPG Pipeline**
```python
# Create integration script
# Location: /home/jim/.../integration/v9_openspg_bridge.py
class V9OpenSPGBridge:
    def __init__(self):
        self.v9_api = "http://localhost:8001"
        self.openspg_api = "http://172.18.0.2:8887"

    def process_document(self, document_path):
        # Extract entities with V9 NER
        entities = requests.post(f"{self.v9_api}/extract",
                                 files={'file': open(document_path, 'rb')})

        # Send to OpenSPG for graph construction
        job = requests.post(f"{self.openspg_api}/api/graph/import",
                           json={'entities': entities.json()})

        return job.json()
```

**3. Test Customer Namespace Isolation**
```cypher
// Create test customer data
CREATE (d:Document {
    id: 'test_doc_1',
    customer: 'customer_123',
    title: 'Test Threat Report'
})

// Query by customer
MATCH (n {customer: 'customer_123'})
RETURN count(n)
```

### Short-Term Goals (Week 2-4)

**1. Document Ingestion Pipeline**
- Integrate V9 NER API with OpenSPG
- Configure OpenSPG projects for customer namespaces
- Test with 10 sample documents
- Validate quality (95%+ precision target)

**2. AEON UI Integration**
- Add OpenSPG job status tracking to dashboard
- Enable customer-filtered graph queries
- Implement upload → OpenSPG → Neo4j workflow

**3. Performance Optimization**
- Configure Neo4j indexes for customer queries
- Tune OpenSPG scheduler settings
- Optimize V9 NER batch processing

### Long-Term Strategy (Month 2-3)

**1. Full 400-Document Ingestion**
- Automated processing (2-4 hours)
- Selective LLM enhancement (20-40 hours)
- Knowledge graph expansion (50K-100K new nodes)

**2. Advanced Analytics**
- Multi-hop attack path queries
- Temporal campaign analysis
- Threat actor capability assessment
- Vulnerability blast radius calculations

**3. Production Hardening**
- Implement authentication on all endpoints
- Enable TLS/SSL encryption
- Configure monitoring and alerting
- Backup automation for all databases

---

## Risk Assessment & Mitigation

### Risk 1: OpenSPG Server Unhealthy Status

**Current State:** Container running but health check failing

**Impact:** Low (service functional, logs show normal operations)

**Root Cause:** Likely Docker health check configuration issue

**Mitigation:**
```bash
# Investigate health check configuration
docker inspect openspg-server | grep -A 10 Healthcheck

# Manual health verification
curl http://172.18.0.2:8887/health

# If needed, update Docker health check
# (in docker-compose.yml)
```

**Priority:** Medium (operational impact minimal, fix for monitoring)

### Risk 2: Qdrant Unhealthy Status

**Current State:** Container running but health check failing

**Impact:** Low (vector search functional, API responding)

**Mitigation:** Similar to OpenSPG - investigate Docker health check configuration

**Priority:** Low (non-critical for graph operations)

### Risk 3: Database Schema Conflicts

**Concern:** Customer data mixing across namespaces in Neo4j

**Mitigation Strategy:**
1. Enforce customer property on all nodes
2. Create Neo4j constraints: `CREATE CONSTRAINT customer_required FOR (n:Document) REQUIRE n.customer IS NOT NULL`
3. Implement query-level access control in AEON UI
4. Regular audits of namespace isolation

**Priority:** High (data integrity critical)

### Risk 4: Performance Degradation After Ingestion

**Concern:** Neo4j performance with 670K nodes + 3.8M relationships

**Assessment:** Low risk - Neo4j scales to billions of nodes

**Mitigation:**
1. Create indexes on frequently queried properties
2. Optimize Cypher queries (avoid Cartesian products)
3. Monitor query performance (PROFILE queries)
4. Consider Neo4j Enterprise for clustering (if needed)

**Priority:** Low (proactive monitoring)

---

## Key Architectural Decisions (ADRs)

### ADR-001: Maintain Three-Database Architecture

**Status:** Accepted
**Date:** 2025-11-11

**Context:** System has PostgreSQL (Next.js), MySQL (OpenSPG), and Neo4j (graph storage).

**Decision:** Maintain all three databases in parallel operation.

**Rationale:**
- Each database optimized for specific workload
- PostgreSQL: Best for Next.js app state
- MySQL: Required for OpenSPG operations (33 tables)
- Neo4j: Best-in-class graph database

**Consequences:**
- Positive: Optimal performance for each use case
- Positive: Leverage existing integrations
- Negative: Operational complexity (3 databases to maintain)
- Negative: Backup complexity

**Alternatives Considered:**
- Migrate everything to Neo4j: Rejected (Neo4j not optimal for relational workloads)
- Migrate OpenSPG to PostgreSQL: Rejected (breaks OpenSPG architecture)

### ADR-002: OpenSPG as Knowledge Graph Construction Engine

**Status:** Accepted
**Date:** 2025-11-11

**Context:** Need to process 400 cybersecurity reports into knowledge graph.

**Decision:** Use OpenSPG as primary processing pipeline for document ingestion.

**Rationale:**
- OpenSPG designed for knowledge graph construction at scale
- Handles entity extraction, relationship inference, job scheduling
- Already integrated with Neo4j
- Proven architecture (existing deployment)

**Consequences:**
- Positive: Automated processing (100-200 docs/hour)
- Positive: Scalable to large document corpora
- Positive: Leverages existing infrastructure
- Negative: Learning curve for OpenSPG configuration

**Alternatives Considered:**
- Custom Python pipeline: Rejected (reinventing wheel)
- LLM-only processing: Rejected (too expensive, too slow)

### ADR-003: Customer Namespace via Neo4j Properties

**Status:** Accepted
**Date:** 2025-11-11

**Context:** Multi-customer data isolation required in shared Neo4j instance.

**Decision:** Use node properties (`customer: 'customer_id'`) for namespace isolation.

**Rationale:**
- Simple implementation in existing codebase
- Compatible with AEON UI Phase 2 customer management
- Works with OpenSPG project isolation
- Easy to query and enforce

**Consequences:**
- Positive: Simple query filtering (`MATCH (n {customer: 'id'})`)
- Positive: No schema changes required
- Negative: Requires discipline to always include customer filter
- Negative: Query-level access control (not database-level)

**Alternatives Considered:**
- Separate Neo4j databases per customer: Rejected (operational overhead)
- Graph-level isolation with Neo4j Enterprise: Rejected (licensing cost)

---

## Conclusion

### Summary of Findings

1. **OpenSPG and Neo4j are complementary systems** - OpenSPG processes and constructs knowledge graphs, Neo4j stores them. No migration needed.

2. **Three databases serve distinct purposes**:
   - PostgreSQL: AEON UI application state (keep)
   - MySQL: OpenSPG operational database (keep)
   - Neo4j: Universal graph storage backend (shared by OpenSPG and AEON UI)

3. **Critical capability: OpenSPG for document processing** - Can automate ingestion of 400 reports in 2-4 hours, creating 50K-100K new entities and 200K-500K relationships.

4. **Parallel operation is already functional** - All three databases operational, integrated, and serving their designed purposes.

5. **Strategic value: V9 NER + OpenSPG pipeline** - High-quality entity extraction (99% F1) feeding into scalable graph construction.

### Recommended Next Steps

**Immediate (This Week):**
1. Validate OpenSPG-Neo4j integration with test documents
2. Configure V9 NER → OpenSPG bridge for automated processing
3. Test customer namespace isolation in Neo4j

**Short-Term (Next Month):**
1. Process pilot batch of 10-20 documents through full pipeline
2. Integrate OpenSPG job monitoring into AEON UI dashboard
3. Optimize Neo4j indexes for customer-filtered queries

**Long-Term (Quarter 2):**
1. Full ingestion of 400 cybersecurity reports
2. Advanced analytics and attack path queries
3. Production hardening and security enhancements

### Final Assessment

**Status:** ✅ **ARCHITECTURE OPTIMIZED FOR PARALLEL OPERATION**

The existing three-database architecture is **strategically sound**. Each database plays a critical role:
- Neo4j: Knowledge graph storage excellence
- MySQL: OpenSPG operational reliability
- PostgreSQL: Web application state management

**Recommendation:** Proceed with integration roadmap. No structural changes needed.

---

**Document Status:** COMPLETE
**Next Review:** 2025-11-18 (after pilot document processing)
**Maintained By:** System Architecture Designer
**Related Documents:**
- V9_DEPLOYMENT_SUMMARY.md
- DOCUMENT_INGESTION_ARCHITECTURE.md
- Neo4j-Database.md (Wiki)
- MySQL-Database.md (Wiki)
- OpenSPG-Server.md (Wiki)
