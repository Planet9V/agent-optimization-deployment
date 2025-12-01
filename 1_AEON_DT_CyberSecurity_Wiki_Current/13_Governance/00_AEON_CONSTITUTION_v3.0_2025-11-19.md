# AEON Digital Twin - Constitution
**File**: 00_AEON_CONSTITUTION.md
**Created**: 2025-11-12 05:15:00 UTC
**Modified**: 2025-11-12 05:15:00 UTC
**Version**: 1.0.0
**Author**: AEON Architecture Team
**Purpose**: Governing principles, rules, and standards for AEON Digital Twin platform
**Status**: ACTIVE - CONSTITUTIONAL DOCUMENT

---

## Preamble

We, the AEON Digital Twin development team, establish this Constitution to guide the development, operation, and evolution of the AEON Digital Twin Cybersecurity Intelligence Platform. This document serves as the supreme governing framework for all technical, operational, and strategic decisions.

**Mission Statement**: To create the world's most comprehensive, intelligent, and actionable cybersecurity threat intelligence platform that answers McKenney's 8 Strategic Questions with unprecedented accuracy and insight.

**Vision**: To eliminate cybersecurity blind spots through semantic knowledge graphs, probabilistic reasoning, and continuous intelligence gathering, enabling organizations to proactively defend against evolving cyber threats.

---

## Article I: Foundational Principles

### Section 1.1: Core Values

**INTEGRITY** - All data must be traceable, verifiable, and accurate
- Every piece of information has a source citation
- All probabilities include confidence intervals
- No speculation presented as fact

**DILIGENCE** - Every task must be completed fully, documented thoroughly
- "Started = Finished" - No partial implementations
- All code includes comprehensive tests (≥85% coverage)
- All decisions documented in Qdrant memory

**COHERENCE** - All components must work together harmoniously
- No duplicate endpoints, APIs, or services
- Shared resources used whenever possible
- Breaking changes require migration paths

**FORWARD-THINKING** - Architected for scale, evolution, adaptation
- Modular design enabling component replacement
- Versioned APIs with deprecation policies
- Continuous learning from operational data

### Section 1.2: Non-Negotiable Rules

1. **NEVER BREAK CLERK AUTH** on Next.js frontend (port 3000)
   - All authentication flows must route through Clerk
   - Test authentication after every deployment
   - Maintain user session integrity

2. **ALWAYS USE EXISTING RESOURCES**
   - Before creating new endpoints, verify none exist
   - Before writing new code, check for shared libraries
   - Before deploying new containers, use existing infrastructure

3. **NO DEVELOPMENT THEATER**
   - Build actual working features, not frameworks to build features
   - Evidence of completion = working code, passing tests, populated databases
   - "COMPLETE" means deliverable exists and functions

4. **PATH INTEGRITY**
   - Never break file paths without migration
   - Document all file moves in CHANGELOG
   - Update all references when relocating files

5. **TASKMASTER COMPLIANCE**
   - All multi-step work uses TASKMASTER
   - Tasks tracked in Qdrant memory
   - Risks and issues documented at every step

---

## Article II: Technical Governance

### Section 2.1: Technology Stack - Immutable Foundation

**DATABASES** (3-database architecture):
- **Neo4j 5.26** (bolt://172.18.0.5:7687) - Knowledge graph, relationships
- **PostgreSQL 16** (172.18.0.4:5432) - Structured data, Next.js state, job persistence
- **MySQL 10.5.8** (172.18.0.4:3306) - OpenSPG operational data

**VECTOR INTELLIGENCE**:
- **Qdrant** (http://172.18.0.6:6333) - Vector embeddings, agent memory, similarity search

**KNOWLEDGE GRAPH ENGINE**:
- **OpenSPG Server** (http://172.18.0.2:8887) - Knowledge graph construction

**FRONTEND**:
- **Next.js 14+** (port 3000) - React framework with App Router
- **Clerk** - Authentication and user management
- **TailwindCSS** - Styling framework

**BACKEND SERVICES**:
- **NER v9** (port 8001) - spaCy-based entity extraction (99% F1 score)
- **FastAPI** - Python backend services
- **Express.js** - Node.js backend services

**AI COORDINATION**:
- **Ruv-Swarm** - Agent coordination and task orchestration
- **Claude-Flow** - Persistent memory and cross-session state
- **16 Specialized Agents** - Domain experts for all tasks

### Section 2.2: Architectural Constraints

**THREE-DATABASE PARALLEL OPERATION**
- Neo4j: Single source of truth for relationships
- PostgreSQL: Application state and job management
- MySQL: OpenSPG operational metadata
- Qdrant: Vector intelligence layer
- **Constraint**: No duplicate data across databases (each has specific role)

**MICROSERVICES BOUNDARIES**
```
┌─────────────────────────────────────────────────────────────┐
│                   AEON Digital Twin Platform                 │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐         ┌──────────────┐                 │
│  │  AEON UI     │────────▶│  OpenSPG     │                 │
│  │  Next.js     │         │  Server      │                 │
│  │  172.18.0.8  │         │  172.18.0.2  │                 │
│  └──────┬───────┘         └──────┬───────┘                 │
│         │                        │                          │
│  ┌──────▼───────┐         ┌──────▼────────┐                │
│  │ PostgreSQL   │         │ MySQL         │                │
│  │ (App State)  │         │ (OpenSPG Jobs)│                │
│  │              │         └──────┬────────┘                │
│  └──────────────┘                │                          │
│         └────────────┬───────────┘                          │
│                      │                                      │
│               ┌──────▼───────────┐                          │
│               │ Neo4j            │                          │
│               │ (Knowledge Graph)│                          │
│               │ 570K nodes       │                          │
│               │ 3.3M edges       │                          │
│               └──────────────────┘                          │
│                      │                                      │
│               ┌──────▼───────────┐                          │
│               │ Qdrant (Vectors) │                          │
│               └──────────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

**DATA FLOW MANDATE**
1. **Ingestion**: Documents → NER v9 → Entities
2. **Extraction**: Entities → OpenSPG → Relationships
3. **Storage**: Relationships → Neo4j → Knowledge Graph
4. **Intelligence**: Knowledge Graph → Semantic Reasoning → Insights
5. **Presentation**: Insights → Next.js UI → Users

### Section 2.3: Quality Standards

**CODE QUALITY THRESHOLDS**
- Test Coverage: ≥85% for all production code
- Type Safety: 100% TypeScript strict mode (frontend), Python type hints (backend)
- Linting: Zero errors, warnings acceptable with justification
- Documentation: Every public function/API documented

**PERFORMANCE TARGETS**
- API Response Time: <200ms (95th percentile)
- Graph Query Time: <100ms (simple), <500ms (complex multi-hop)
- Job Processing: ≥100 documents/hour (with distributed workers)
- UI Load Time: <3 seconds (Time to Interactive)

**RELIABILITY REQUIREMENTS**
- Uptime: 99.5% (planned maintenance excluded)
- Job Success Rate: ≥98% (with retry mechanisms)
- Data Integrity: 100% (no data loss tolerated)
- Error Recovery: Automatic retry up to 3 attempts

---

## Article III: Development Process

### Section 3.1: TASKMASTER Methodology

**ALL MULTI-STEP WORK MUST USE TASKMASTER**

**TASKMASTER Structure**:
```yaml
task:
  id: "TASK-2025-11-12-001"
  created: "2025-11-12 05:15:00 UTC"
  assigned_to: "relationship_engineer"
  priority: "CRITICAL"
  deadline: "2026-03-15"

  description: "Build 10,000+ CVE→CWE→CAPEC→Technique→Tactic semantic chains"

  deliverables:
    - "Query Neo4j for 10,000 CVEs with CWE mappings"
    - "Build CWE→CAPEC relationships using MITRE CAPEC database"
    - "Map CAPEC→ATT&CK Techniques using existing mappings"
    - "Create Technique→Tactic edges (193 techniques, 14 tactics)"
    - "Store complete 5-part chains as graph paths"
    - "Validate chain completeness (target: 80%+ CVEs with full chains)"
    - "Generate chain statistics and quality metrics"

  success_criteria:
    - "10,000+ CVEs with semantic chain paths"
    - "Chain completeness ≥80%"
    - "Query performance <100ms for chain traversal"
    - "Documentation of chain construction methodology"

  risks:
    - "Neo4j performance degradation with 3.3M edges"
    - "Data quality issues in CAPEC mappings"
    - "CWE→CAPEC mapping gaps"

  issues:
    - type: "BLOCKER"
      description: "MySQL CAPEC database access credentials unknown"
      resolution: "Contact DevOps for credentials"

  notes:
    - "2025-11-12 05:15: Task orchestrated to 16 agents"
    - "2025-11-12 05:20: Neo4j connection verified"

  memory_keys:
    - "semantic_chains_task_001"
    - "neo4j_query_patterns"
    - "capec_mapping_strategy"

  dependencies:
    - "Neo4j database operational"
    - "MySQL OpenSPG database accessible"
    - "Neo4j bolt driver configured"
```

**TASKMASTER Lifecycle**:
1. **Creation**: Task defined with all required fields
2. **Assignment**: Task assigned to agent(s) via ruv-swarm
3. **Execution**: Agent executes with progress tracking
4. **Documentation**: All decisions stored in Qdrant memory
5. **Validation**: Success criteria verified before marking complete
6. **Archival**: Completed tasks archived with full history

### Section 3.2: Documentation Requirements

**EVERY DOCUMENT MUST HAVE**:
```markdown
**File**: <filename>
**Created**: YYYY-MM-DD HH:MM:SS UTC
**Modified**: YYYY-MM-DD HH:MM:SS UTC
**Version**: X.Y.Z (semantic versioning)
**Author**: <author/team name>
**Purpose**: <clear statement of purpose>
**Status**: ACTIVE | DEPRECATED | ARCHIVED
```

**VERSION CONTROL**:
- Major version (X): Breaking changes, architectural shifts
- Minor version (Y): New features, significant updates
- Patch version (Z): Bug fixes, typos, clarifications

**DEPRECATION PROCESS**:
1. Update Status to DEPRECATED
2. Add deprecation date and replacement file reference
3. Move to `/archive/deprecated/<year>/<month>/` after 90 days
4. Never delete (maintain historical record)

### Section 3.3: Testing Mandates

**BEFORE DEPLOYMENT - MUST VERIFY**:
```bash
# 1. Clerk Authentication
curl -X POST http://localhost:3000/api/auth/session \
  -H "Cookie: __session=<test_token>" \
  -v | grep "200 OK"

# 2. Database Connections
docker exec openspg-neo4j cypher-shell -u neo4j -p <password> "MATCH (n) RETURN count(n) LIMIT 1"
docker exec aeon-postgres-dev psql -U postgres -c "SELECT version();"
docker exec openspg-mysql mysql -u root -p<password> -e "SELECT 1;"

# 3. Services Health
curl http://localhost:8001/health  # NER v9
curl http://172.18.0.2:8887/health  # OpenSPG
curl http://172.18.0.6:6333/  # Qdrant

# 4. API Endpoints
curl http://localhost:3000/api/health
curl http://localhost:3000/api/neo4j/stats

# 5. File Paths (after any moves)
node scripts/verify-paths.js
```

**AFTER DEPLOYMENT - SMOKE TESTS**:
1. User can log in via Clerk
2. Dashboard loads within 3 seconds
3. Search returns results
4. Graph visualization renders
5. NER extraction completes successfully

---

## Article IV: Memory and State Management

### Section 4.1: Qdrant Memory Architecture

**ALL AGENT OPERATIONS MUST USE QDRANT MEMORY**

**Memory Structure**:
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Initialize Qdrant client
qdrant = QdrantClient(url="http://172.18.0.6:6333")

# Collection schema
collections = {
    "agent_memory": {
        "description": "Cross-agent persistent memory",
        "vector_size": 768,  # BERT embedding dimension
        "distance": Distance.COSINE
    },
    "task_history": {
        "description": "Complete task execution history",
        "vector_size": 768,
        "distance": Distance.COSINE
    },
    "code_patterns": {
        "description": "Reusable code patterns and solutions",
        "vector_size": 768,
        "distance": Distance.COSINE
    },
    "api_contracts": {
        "description": "API specifications and examples",
        "vector_size": 768,
        "distance": Distance.COSINE
    },
    "user_queries": {
        "description": "User interaction patterns",
        "vector_size": 768,
        "distance": Distance.COSINE
    }
}

# Memory operations
class AEONMemory:
    """Centralized memory management for AEON platform"""

    def store_task_decision(self, task_id: str, decision: str, rationale: str):
        """Store task-related decisions with reasoning"""
        qdrant.upsert(
            collection_name="task_history",
            points=[PointStruct(
                id=f"{task_id}_{timestamp}",
                vector=embed(decision),  # BERT embedding
                payload={
                    "task_id": task_id,
                    "decision": decision,
                    "rationale": rationale,
                    "timestamp": datetime.utcnow().isoformat(),
                    "agent": current_agent_id
                }
            )]
        )

    def retrieve_similar_solutions(self, problem: str, top_k: int = 5):
        """Find similar problems solved in the past"""
        results = qdrant.search(
            collection_name="code_patterns",
            query_vector=embed(problem),
            limit=top_k
        )
        return [hit.payload for hit in results]
```

**MEMORY LIFECYCLE**:
1. **Creation**: All task decisions, code patterns, API contracts stored in Qdrant
2. **Retrieval**: Agents query memory before starting new work
3. **Update**: Memory updated as tasks progress
4. **Consolidation**: Similar memories merged to reduce duplication
5. **Archival**: Old memories archived (never deleted) after 1 year

### Section 4.2: Cross-Session Continuity

**EVERY SESSION MUST**:
1. Load relevant memory from Qdrant
2. Check for in-progress tasks
3. Resume work from last checkpoint
4. Store progress updates continuously
5. Save complete state at session end

**SESSION PATTERN**:
```python
# Session Start
def start_session():
    # 1. Load memory
    memories = qdrant.search(
        collection_name="agent_memory",
        query_vector=embed(f"agent_{agent_id}_current_tasks"),
        limit=10
    )

    # 2. Check in-progress tasks
    tasks = [m.payload for m in memories if m.payload['status'] == 'in_progress']

    # 3. Resume or start new
    if tasks:
        resume_task(tasks[0])
    else:
        await_new_assignment()

# Session End
def end_session():
    # 1. Store current state
    qdrant.upsert(
        collection_name="agent_memory",
        points=[PointStruct(
            id=f"session_{session_id}_state",
            vector=embed(current_state),
            payload={
                "session_id": session_id,
                "agent_id": agent_id,
                "state": current_state,
                "timestamp": datetime.utcnow().isoformat(),
                "tasks": active_tasks
            }
        )]
    )

    # 2. Save checkpoint
    checkpoint_id = save_checkpoint()

    # 3. Log completion
    log_session_end(session_id, checkpoint_id)
```

---

## Article V: Data Governance

### Section 5.1: Data Sources - Single Source of Truth

**MITRE ATT&CK** (Primary Threat Intelligence)
- Source: https://github.com/mitre/cti
- Update Frequency: Quarterly (aligned with MITRE release schedule)
- Version Control: Git tags for each version
- Authority: MITRE Corporation

**NVD CVE Database** (Vulnerability Intelligence)
- Source: https://services.nvd.nist.gov/rest/json/cves/2.0
- Update Frequency: Daily (automated)
- Version Control: CVE modification timestamps
- Authority: NIST

**MITRE CAPEC** (Attack Pattern Intelligence)
- Source: https://capec.mitre.org/data/xml/capec_latest.xml
- Update Frequency: Quarterly
- Version Control: CAPEC version numbers
- Authority: MITRE Corporation

**CWE Database** (Weakness Intelligence)
- Source: https://cwe.mitre.org/data/xml/cwec_latest.xml.zip
- Update Frequency: Quarterly
- Version Control: CWE version numbers
- Authority: MITRE Corporation

### Section 5.2: Data Quality Standards

**ALL DATA MUST BE**:
- **Traceable**: Every data point has a source field
- **Timestamped**: Created and modified timestamps
- **Versioned**: Version number for all imported data
- **Validated**: Schema validation before storage

**DATA VALIDATION RULES**:
```python
from pydantic import BaseModel, Field, validator

class CVERecord(BaseModel):
    """CVE data model with validation"""

    cve_id: str = Field(..., regex=r'^CVE-\d{4}-\d{4,}$')
    description: str = Field(..., min_length=10)
    cvss_score: float = Field(..., ge=0.0, le=10.0)
    cvss_vector: str
    published_date: datetime
    modified_date: datetime
    cwe_ids: List[str]
    source: str = "NVD"
    version: str

    @validator('cwe_ids')
    def validate_cwe_ids(cls, v):
        for cwe_id in v:
            if not cwe_id.startswith('CWE-'):
                raise ValueError(f'Invalid CWE ID: {cwe_id}')
        return v
```

### Section 5.3: Data Retention and Archival

**RETENTION POLICY**:
- **Production Data**: Indefinite (never deleted)
- **Deprecated Data**: Moved to archive, accessible for historical analysis
- **Test Data**: 90 days, then purged
- **Logs**: 1 year in hot storage, then move to cold storage
- **Memory Vectors**: 1 year active, then archived

**ARCHIVAL STRUCTURE**:
```
/home/jim/2_OXOT_Projects_Dev/
└── 1_AEON_DT_CyberSecurity_Wiki_Current/
    ├── 00_ACTIVE/  # Current documentation
    ├── archive/
    │   ├── 2025/
    │   │   ├── 11/  # November 2025
    │   │   │   ├── deprecated/  # Deprecated but reference-able
    │   │   │   └── legacy/  # Old versions for historical record
    │   │   └── 12/
    │   └── 2024/
    └── CHANGELOG.md  # All file moves documented here
```

---

## Article VI: Security and Compliance

### Section 6.1: Authentication and Authorization

**CLERK AUTH - NON-NEGOTIABLE**:
- All frontend authentication via Clerk
- No custom auth implementations
- Session management delegated to Clerk
- RBAC via Clerk organizations and roles

**API SECURITY**:
- All API endpoints require authentication (except `/health`)
- JWT tokens validated on every request
- Rate limiting: 1000 requests/minute per user
- API keys rotated every 90 days

**DATABASE SECURITY**:
- Least privilege access (each service has own credentials)
- Encrypted connections (TLS 1.2+)
- No plaintext passwords (environment variables only)
- Audit logging for all data modifications

### Section 6.2: Data Privacy

**PII HANDLING**:
- No PII stored in knowledge graph (customer names anonymized)
- User data segregated by organization (multi-tenancy)
- GDPR compliance: Right to be forgotten implemented
- Data export available for all users

**LOGGING CONSTRAINTS**:
- Never log credentials, tokens, or sensitive data
- Sanitize all log outputs
- Structured logging (JSON format)
- Log levels: DEBUG (dev only), INFO, WARN, ERROR, CRITICAL

---

## Article VII: Operational Excellence

### Section 7.1: Monitoring and Observability

**REQUIRED METRICS**:
```yaml
system_metrics:
  - docker_container_health
  - database_connection_pool_usage
  - api_response_time_p95
  - job_success_rate
  - neo4j_query_performance

business_metrics:
  - documents_processed_per_hour
  - semantic_chains_created_per_day
  - user_queries_answered
  - average_time_to_insight

quality_metrics:
  - ner_extraction_accuracy
  - graph_completeness_percentage
  - api_error_rate
  - test_coverage_percentage
```

**ALERTING THRESHOLDS**:
- API Error Rate >5%: WARNING
- API Error Rate >10%: CRITICAL
- Database Connection Failures: CRITICAL (immediate)
- Job Success Rate <95%: WARNING
- Any container unhealthy >5 minutes: CRITICAL

### Section 7.2: Incident Response

**SEVERITY LEVELS**:
- **SEV-1 CRITICAL**: Production down, data loss, security breach
  - Response Time: <15 minutes
  - All hands on deck
  - Executive notification

- **SEV-2 HIGH**: Significant degradation, feature unavailable
  - Response Time: <1 hour
  - Core team mobilized

- **SEV-3 MEDIUM**: Minor degradation, workaround available
  - Response Time: <4 hours
  - Normal support channels

**POST-INCIDENT**:
1. Root cause analysis within 48 hours
2. Action items assigned with deadlines
3. Documentation updated (runbooks, alerts)
4. Memory updated in Qdrant (lessons learned)

---

## Article VIII: Change Management

### Section 8.1: Breaking Changes Policy

**BEFORE MAKING BREAKING CHANGES**:
1. Propose change in design document
2. Get stakeholder approval
3. Create migration plan
4. Implement backward compatibility (if possible)
5. Deprecate old version (90-day notice)
6. Document in CHANGELOG.md

**MIGRATION REQUIREMENTS**:
```markdown
## Migration Guide: API v1 → v2

### Breaking Changes:
- Endpoint: `/api/graph/query` → `/api/v2/graph/query`
- Response format: `{ results: [] }` → `{ data: { nodes: [], edges: [] } }`

### Migration Steps:
1. Update all API calls to use `/api/v2/` prefix
2. Update response parsing to access `data.nodes` instead of `results`
3. Test with sample queries before deploying

### Rollback Procedure:
If issues arise, revert to v1 by setting `API_VERSION=v1` in `.env`

### Deprecation Timeline:
- 2025-11-12: v2 released, v1 still supported
- 2026-02-12: v1 deprecated warning in logs
- 2026-05-12: v1 removed
```

### Section 8.2: File Organization Mandate

**BEFORE MOVING/RENAMING FILES**:
1. Search codebase for all references: `git grep "old_filename"`
2. Update all imports, requires, file paths
3. Test all affected services
4. Document move in CHANGELOG.md
5. Create symlink (temporary) for transition period
6. Verify no broken paths: `node scripts/verify-paths.js`

**EXAMPLE MIGRATION**:
```bash
# 1. Find all references
git grep "old_file.ts" > references.txt

# 2. Create new file location
mkdir -p new/location
git mv old/path/old_file.ts new/location/new_file.ts

# 3. Update all references (automated)
sed -i 's|old/path/old_file|new/location/new_file|g' $(cat references.txt | cut -d: -f1)

# 4. Create temporary symlink
ln -s new/location/new_file.ts old/path/old_file.ts

# 5. Update CHANGELOG.md
echo "- MOVED: old/path/old_file.ts → new/location/new_file.ts (2025-11-12)" >> CHANGELOG.md

# 6. Test everything
npm test && npm run build && npm run verify-paths

# 7. Commit with clear message
git add -A
git commit -m "refactor: move old_file.ts to new/location/ for better organization

Breaking change: File path changed
Migration: Update imports from old/path to new/location
See CHANGELOG.md for details"
```

---

## Article IX: Continuous Improvement

### Section 9.1: Retrospective Cadence

**MONTHLY RETROSPECTIVES**:
- What went well?
- What didn't go well?
- What should we do differently?
- Action items with owners and deadlines

**QUARTERLY REVIEWS**:
- Architecture assessment
- Performance benchmarking against targets
- Security audit
- Dependency updates

### Section 9.2: Innovation Pipeline

**EXPERIMENTAL FEATURES**:
- Developed in feature branches
- Flagged as "EXPERIMENTAL" in UI
- User opt-in required
- Graduate to production after 90 days of stability

**FEATURE REQUEST PROCESS**:
1. User submits request via GitHub Issues
2. Team triages (accept/reject/defer)
3. Accepted features added to roadmap
4. PRD created with success criteria
5. Implementation tracked in TASKMASTER
6. Release with changelog entry

---

## Article X: Enforcement and Amendments

### Section 10.1: Constitutional Violations

**VIOLATIONS ARE TRACKED**:
- All violations logged in Qdrant memory
- Monthly review of violation patterns
- Training provided for repeat violations

**SEVERITY OF VIOLATIONS**:
- **CRITICAL**: Breaking Clerk auth, data loss, security breach
  - Immediate rollback required
  - Post-mortem within 24 hours

- **HIGH**: Breaking paths, duplicate resources, incomplete implementations
  - Fix required within 1 week
  - Document in CHANGELOG

- **MEDIUM**: Missing documentation, inadequate testing
  - Fix required within 2 weeks
  - Improve processes to prevent recurrence

### Section 10.2: Amendments

**THIS CONSTITUTION CAN BE AMENDED**:
1. Proposal submitted with rationale
2. Team discussion (all stakeholders)
3. Approval by majority vote
4. Amendment added with version increment
5. Effective date specified

**AMENDMENT FORMAT**:
```markdown
## Amendment I: [Title]
**Proposed**: YYYY-MM-DD
**Approved**: YYYY-MM-DD
**Effective**: YYYY-MM-DD
**Version**: 1.1.0

### Rationale:
[Why this amendment is needed]

### Changes:
[Specific changes to the Constitution]

### Impact:
[How this affects existing practices]
```

---

## Appendix A: Quick Reference

**CRITICAL PATHS**:
- Wiki: `/home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current`
- Working Docs: `/home/jim/2_OXOT_Projects_Dev/10_Ontologies/2_Working_Directory_2025_Nov_11`
- Next.js App: `/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE`

**CRITICAL SERVICES**:
- Next.js: http://localhost:3000
- Neo4j Browser: http://localhost:7474
- Qdrant UI: http://172.18.0.6:6333/dashboard
- OpenSPG: http://172.18.0.2:8887
- NER v9: http://localhost:8001

**CRITICAL COMMANDS**:
```bash
# Health check all services
docker ps --format "table {{.Names}}\t{{.Status}}"

# Verify Clerk auth
curl http://localhost:3000/api/auth/session -v

# Check databases
docker exec openspg-neo4j cypher-shell "MATCH (n) RETURN count(n) LIMIT 1"
docker exec aeon-postgres-dev psql -U postgres -c "SELECT version();"

# Verify paths
node scripts/verify-paths.js

# Run tests
npm test
pytest tests/

# Store in Qdrant memory
python scripts/store_decision.py --decision="..." --rationale="..."
```

---

## Appendix B: Glossary

**AEON**: Adaptive Evolutionary Ontology Network
**McKenney's 8 Questions**: Core business questions the platform must answer
**TASKMASTER**: Task management and tracking methodology
**Ruv-Swarm**: Multi-agent coordination framework
**Claude-Flow**: Persistent memory and cross-session state management
**NER v9**: Named Entity Recognition version 9 (spaCy-based)
**Qdrant**: Vector database for embeddings and memory
**OpenSPG**: Knowledge graph construction engine

---

**RATIFIED**: 2025-11-12 05:15:00 UTC
**EFFECTIVE**: Immediately
**NEXT REVIEW**: 2026-02-12 (Quarterly)

*This Constitution is the supreme governing document for the AEON Digital Twin platform. All code, documentation, and operational decisions must align with these principles.*
