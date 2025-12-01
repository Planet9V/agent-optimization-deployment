# AEON Digital Twin: Product Requirements Document (PRD)

**File**: 01_PRODUCT_REQUIREMENTS.md
**Created**: 2025-11-12 05:30:00 UTC
**Modified**: 2025-11-12 05:30:00 UTC
**Version**: 1.0.0
**Author**: AEON Development Team
**Purpose**: Comprehensive product requirements for AEON Digital Twin Cybersecurity Platform
**Status**: ACTIVE - AUTHORITATIVE REQUIREMENTS

**References**:
- Constitution: `/00_AEON_CONSTITUTION.md`
- Architecture: `/01_ARCHITECTURE/01_COMPREHENSIVE_ARCHITECTURE.md`
- Implementation Gaps: `/home/jim/2_OXOT_Projects_Dev/10_Ontologies/2_Working_Directory_2025_Nov_11/09_IMPLEMENTATION_GAPS.md`

---

## Executive Summary

### Product Vision

AEON Digital Twin is an **AI-powered cybersecurity intelligence platform** that transforms raw threat data into actionable defensive intelligence by answering **McKenney's 8 Strategic Questions**. The platform integrates MITRE ATT&CK, CVE, CWE, and CAPEC data into a semantic knowledge graph, enabling probabilistic attack chain analysis and equipment-specific risk assessment.

### Current State (2025-11-12)

**Completion Status**: 23% (5 of 22 core components implemented)

**What Exists**:
- ✅ Infrastructure: 7 Docker containers running (Neo4j, PostgreSQL, MySQL, Qdrant, MinIO, OpenSPG Server, Next.js Frontend)
- ✅ Data Layer: 570K Neo4j nodes, 3.3M edges
- ✅ NER v9: 16 entity types, 99% F1 score
- ✅ 16 Specialized Agents: Ruv-Swarm coordination
- ✅ Next.js Frontend: Clerk authentication

**What's Missing (77%)**:
- ❌ 5-Part Semantic Chain: CVE → CWE → CAPEC → Technique → Tactic (0% complete)
- ❌ AttackChainScorer: Bayesian probabilistic scoring (0% complete)
- ❌ Job Persistence: PostgreSQL job tracking (0% complete, 0% reliability)
- ❌ GNN Link Predictor: Graph neural network (0% complete)
- ❌ Equipment Risk Mapping: Customer-specific equipment analysis (0% complete)
- ❌ Mitigation/Detection Recommendations: Actionable outputs (0% complete)

### McKenney's 8 Strategic Questions (Answerability)

| # | Question | Current Answer | Target |
|---|----------|----------------|--------|
| 1 | What is my cyber risk? | ❌ 0% (no scoring) | ✅ 95% confidence intervals |
| 2 | What is my compliance risk? | ❌ 0% (no compliance mapping) | ✅ NIST, CIS, ISO mappings |
| 3 | What techniques do actors use against me? | 🟡 30% (ATT&CK data exists, not linked to CVEs) | ✅ CVE-specific technique chains |
| 4 | What equipment is at risk? | ❌ 0% (no equipment inventory) | ✅ Customer asset integration |
| 5 | What is my attack surface from equipment? | ❌ 0% (no surface analysis) | ✅ Automated surface mapping |
| 6 | What mitigations apply to my equipment? | ❌ 0% (no mitigation engine) | ✅ Equipment-specific mitigations |
| 7 | What detections apply to my equipment? | ❌ 0% (no detection engine) | ✅ SIEM/EDR rule generation |
| 8 | What should I do next? | ❌ 0% (no recommendation engine) | ✅ Prioritized action plans |

**Overall Answerability**: **0 of 8 questions fully answerable** → Target: **8 of 8 at 95%+ confidence**

---

## Section 1: Problem Statement

### 1.1 Core Problem

**Cybersecurity teams cannot answer fundamental strategic questions** because:

1. **Data Silos**: CVE, CWE, CAPEC, ATT&CK exist in separate databases with no semantic connections
2. **Manual Correlation**: Security analysts spend 70%+ time manually linking CVEs to techniques
3. **No Probabilistic Reasoning**: Existing tools provide binary yes/no, not likelihood scores
4. **Equipment Blindness**: CVE databases don't map to customer-specific equipment
5. **Actionability Gap**: Threat intelligence doesn't translate to mitigation/detection actions

### 1.2 Business Impact

**Without AEON**:
- **14+ hours/week** per analyst on manual CVE-to-ATT&CK mapping
- **60% false positives** in threat prioritization (no probability scoring)
- **$2.4M average cost** of missed critical vulnerabilities (Ponemon 2024)
- **18+ months** to answer "What should I patch first?" with confidence

**With AEON**:
- **2 minutes** to generate probabilistic attack chains for any CVE
- **95%+ accuracy** in threat prioritization using Bayesian scoring
- **$890K savings** from focused remediation (reduce false positives by 80%)
- **Real-time answers** to all 8 McKenney questions

### 1.3 User Personas

**Primary Persona: Senior Security Analyst**
- **Name**: Sarah Chen
- **Role**: Threat Intelligence Analyst, Fortune 500 Financial Services
- **Pain Points**:
  - "I spend 3 hours/day manually linking CVEs to ATT&CK techniques"
  - "I can't tell my CISO which vulnerabilities are most likely to be exploited"
  - "Our SIEM has 10,000+ alerts/day, but I don't know which matter"
- **Needs**:
  - Automated CVE → ATT&CK semantic mapping
  - Probabilistic risk scores with confidence intervals
  - Equipment-specific attack surface analysis
  - One-click mitigation recommendations

**Secondary Persona: CISO/Security Director**
- **Name**: Michael Rodriguez
- **Role**: Chief Information Security Officer, Healthcare System
- **Pain Points**:
  - "Board asks 'What's our cyber risk?' and I can't quantify it"
  - "Compliance auditors want proof we're addressing NIST controls"
  - "I need to justify $5M security budget with data, not gut feel"
- **Needs**:
  - Executive dashboard: risk scores, compliance gaps, trending
  - Automated compliance mapping (NIST CSF, CIS Controls, ISO 27001)
  - ROI analysis: cost of vulnerabilities vs. mitigation spend
  - Board-ready reports with confidence intervals

**Tertiary Persona: SOC Analyst**
- **Name**: Alex Thompson
- **Role**: Security Operations Center Analyst, Managed Security Services Provider (MSSP)
- **Pain Points**:
  - "We monitor 50+ customers, can't manually analyze every CVE"
  - "Need to prioritize 500+ vulnerabilities/month across all clients"
  - "Customer asks 'Should I patch CVE-X?' and I have no risk score"
- **Needs**:
  - Bulk CVE analysis (process 1,000+ CVEs/hour)
  - Multi-tenant equipment risk mapping
  - Automated SIEM rule generation for new threats
  - Customer-facing risk reports (non-technical language)

---

## Section 2: Product Scope and Vision

### 2.1 In-Scope Features (Phases 1-5)

#### Phase 1: Semantic Foundation (Months 1-3)
**Objective**: Build 5-part semantic chain linking CVEs to tactics

**Features**:
1. **Semantic Chain Builder**
   - Query Neo4j for CVEs with CWE mappings (target: 10,000+ CVEs)
   - Build CWE → CAPEC relationships using MITRE CAPEC database
   - Map CAPEC → ATT&CK Techniques using MITRE mappings
   - Link Techniques → Tactics (14 ATT&CK tactics)
   - **Success Metric**: 80%+ chain completeness (8,000+ CVEs with full paths)

2. **Job Persistence Layer**
   - PostgreSQL schema: `jobs`, `job_steps`, `job_logs`
   - Retry logic: 3 attempts with exponential backoff
   - Progress tracking: 0-100% per job
   - **Success Metric**: 100% job reliability (zero lost jobs)

3. **Data Validation Pipeline**
   - Automated daily CVE updates from NVD API
   - CAPEC/CWE freshness checks (weekly)
   - ATT&CK version tracking (quarterly updates)
   - **Success Metric**: < 24-hour data lag from NVD publication

#### Phase 2: Probabilistic Intelligence (Months 4-6)
**Objective**: Implement Bayesian attack chain scoring

**Features**:
1. **AttackChainScorer**
   - Bayesian formula: `P(Tactic | CVE) = Σ P(Tactic | Technique) × P(Technique | CAPEC) × P(CAPEC | CWE) × P(CWE | CVE)`
   - Customer-specific priors (equipment type, sector, geographic location)
   - Monte Carlo simulation (10,000+ samples per CVE)
   - Wilson Score confidence intervals (95% CI)
   - **Success Metric**: 85%+ predictive accuracy on historical exploits

2. **Risk Score API**
   - RESTful endpoint: `POST /api/v1/score_cve`
   - Response time: < 2 seconds for single CVE
   - Batch scoring: 1,000+ CVEs in < 60 seconds
   - **Success Metric**: 99.5% uptime, p99 latency < 3s

3. **Uncertainty Quantification**
   - Confidence intervals for all scores
   - Data quality indicators (chain completeness, freshness)
   - Sensitivity analysis (impact of prior changes)
   - **Success Metric**: All scores include ±5% confidence bounds

#### Phase 3: Graph Neural Networks (Months 7-9)
**Objective**: Enable multi-hop reasoning and link prediction

**Features**:
1. **GNN Link Predictor**
   - PyTorch Geometric implementation
   - 3-layer Graph Attention Network (GAT)
   - Training dataset: 3.3M existing Neo4j edges
   - Predict missing CVE → CWE links
   - **Success Metric**: 90%+ precision on test set

2. **Multi-Hop Query Engine**
   - 20+ hop capability (e.g., CVE → CWE → CAPEC → Technique → Tactic → Mitigation → Detection)
   - Cypher query optimization (< 500ms for 10-hop queries)
   - Path ranking by probability
   - **Success Metric**: Answer 95%+ of multi-hop questions

3. **Embedding Pipeline**
   - Node2Vec embeddings for all Neo4j entities
   - 128-dimensional vectors
   - Qdrant storage for similarity search
   - **Success Metric**: < 100ms similarity queries

#### Phase 4: Equipment Integration (Months 10-12)
**Objective**: Map CVEs to customer-specific equipment

**Features**:
1. **Equipment Inventory Integration**
   - CSV/API import for customer asset lists
   - CPE (Common Platform Enumeration) matching
   - Automatic CVE → Equipment mapping
   - **Success Metric**: 95%+ auto-match rate for common software

2. **Attack Surface Calculator**
   - Equipment-specific CVE exposure
   - Network topology analysis (internal vs. external facing)
   - Exploitability scoring (CVSS + reachability)
   - **Success Metric**: Surface calculated in < 10 seconds per customer

3. **Risk Heatmaps**
   - Visual equipment risk dashboard
   - Color-coded by probability × impact
   - Drill-down to CVE details
   - **Success Metric**: Load < 2 seconds for 10,000+ assets

#### Phase 5: Actionable Outputs (Months 13-15)
**Objective**: Generate mitigations, detections, and recommendations

**Features**:
1. **Mitigation Recommendation Engine**
   - Query ATT&CK mitigations for relevant techniques
   - Equipment-specific patching guidance
   - Compensating controls (when patching not possible)
   - **Success Metric**: 90%+ mitigation coverage for scored CVEs

2. **Detection Rule Generator**
   - SIEM rule templates (Splunk, Sentinel, QRadar)
   - EDR queries (CrowdStrike, Carbon Black)
   - Sigma rule export
   - **Success Metric**: 80%+ auto-generated rules deploy without edits

3. **Priority Action Planner**
   - Ranked remediation list (highest risk first)
   - ROI calculator: risk reduction vs. effort
   - Timeline estimator (patch cycles, testing windows)
   - **Success Metric**: Answer "What should I do next?" in < 5 seconds

### 2.2 Out-of-Scope (Future Phases)

**Not in Phases 1-5**:
- Threat actor attribution modeling
- Real-time exploit kit monitoring
- Dark web intelligence integration
- Automated penetration testing
- AI red team simulation

---

## Section 3: Functional Requirements

### 3.1 Data Ingestion and Management

**FR-1.1: CVE Data Ingestion**
- **Description**: Daily automated import from NVD API (nvd.nist.gov)
- **Acceptance Criteria**:
  - Runs at 02:00 UTC daily
  - Imports all CVEs published in last 24 hours
  - Updates existing CVE records (CVSS score changes, CWE mappings)
  - Logs all ingestion errors to PostgreSQL `job_logs`
- **Dependencies**: NVD API key, Neo4j connection, Job persistence layer
- **TASKMASTER Reference**: TASK-2025-11-12-002 (Data Pipeline Engineer)

**FR-1.2: MITRE ATT&CK Updates**
- **Description**: Quarterly import of ATT&CK framework updates
- **Acceptance Criteria**:
  - Detects new ATT&CK versions via GitHub API
  - Merges new techniques, tactics, mitigations without breaking existing chains
  - Validates no orphaned relationships after update
  - Generates change report (added/deprecated techniques)
- **Dependencies**: GitHub API, Neo4j schema versioning
- **TASKMASTER Reference**: TASK-2025-11-12-003 (Knowledge Graph Engineer)

**FR-1.3: CAPEC and CWE Updates**
- **Description**: Monthly import from MITRE CAPEC/CWE databases
- **Acceptance Criteria**:
  - Downloads XML from capec.mitre.org and cwe.mitre.org
  - Parses CWE → CAPEC relationships
  - Updates Neo4j `(:CWE)-[:MAPS_TO_CAPEC]->(:CAPEC)` edges
  - Handles deprecated CWE/CAPEC IDs gracefully
- **Dependencies**: MITRE XML parsers, Neo4j transaction handling
- **TASKMASTER Reference**: TASK-2025-11-12-004 (Data Integration Specialist)

### 3.2 Semantic Chain Construction

**FR-2.1: CVE → CWE Mapping**
- **Description**: Extract CWE IDs from NVD CVE data
- **Acceptance Criteria**:
  - Parses `problemtype.problemtype_data[0].description[0].value` field
  - Handles multiple CWEs per CVE (create multiple edges)
  - Defaults to `CWE-NVD-noinfo` when CWE missing
  - **Target**: 95%+ CVEs have CWE mappings
- **Dependencies**: NVD data quality, NER v9 fallback extraction
- **TASKMASTER Reference**: TASK-2025-11-12-005 (Semantic Mapping Engineer)

**FR-2.2: CWE → CAPEC Mapping**
- **Description**: Use CAPEC database `Related_Weaknesses` field
- **Acceptance Criteria**:
  - Query CAPEC XML for `<Related_Weakness CWE_ID="XXX">`
  - Create Neo4j `(:CWE {id: "CWE-79"})-[:MAPS_TO_CAPEC]->(:CAPEC {id: "CAPEC-63"})`
  - Handle 1-to-many CWE → CAPEC relationships
  - **Target**: 80%+ CWEs have CAPEC mappings
- **Dependencies**: CAPEC XML parser, CWE database
- **TASKMASTER Reference**: TASK-2025-11-12-006 (CAPEC Integration Engineer)

**FR-2.3: CAPEC → Technique Mapping**
- **Description**: Use ATT&CK STIX bundle `x_capec_id` field
- **Acceptance Criteria**:
  - Parse ATT&CK STIX JSON for `external_references` with `source_name: "capec"`
  - Create `(:CAPEC)-[:MAPS_TO_TECHNIQUE]->(:Technique)`
  - Validate all 193 ATT&CK techniques reachable
  - **Target**: 70%+ CAPECs map to techniques
- **Dependencies**: ATT&CK STIX parser, CAPEC database
- **TASKMASTER Reference**: TASK-2025-11-12-007 (ATT&CK Integration Engineer)

**FR-2.4: Technique → Tactic Mapping**
- **Description**: Use ATT&CK `kill_chain_phases` field
- **Acceptance Criteria**:
  - Parse `kill_chain_phases[].phase_name` (e.g., "initial-access")
  - Create `(:Technique)-[:BELONGS_TO_TACTIC]->(:Tactic)`
  - Handle techniques in multiple tactics (e.g., T1566 in Initial Access + Execution)
  - **Target**: 100% techniques mapped to 14 tactics
- **Dependencies**: ATT&CK STIX data
- **TASKMASTER Reference**: TASK-2025-11-12-008 (Tactic Mapping Engineer)

**FR-2.5: Full Chain Validation**
- **Description**: Automated test: can we traverse CVE → Tactic for every CVE?
- **Acceptance Criteria**:
  - Cypher query: `MATCH (cve:CVE)-[:HAS_CWE]->(:CWE)-[:MAPS_TO_CAPEC]->(:CAPEC)-[:MAPS_TO_TECHNIQUE]->(:Technique)-[:BELONGS_TO_TACTIC]->(tactic:Tactic) RETURN count(DISTINCT cve)`
  - **Target**: 8,000+ CVEs (80% of 10,000 CVE corpus)
  - Daily validation job logs chain completeness
  - Alerts if completeness drops below 75%
- **Dependencies**: FR-2.1 through FR-2.4
- **TASKMASTER Reference**: TASK-2025-11-12-009 (QA Engineer)

### 3.3 Probabilistic Scoring

**FR-3.1: Bayesian Probability Calculation**
- **Description**: Implement `AttackChainScorer` class
- **Acceptance Criteria**:
  - Formula: `P(Tactic | CVE) = Σ [P(Tactic | Technique) × P(Technique | CAPEC) × P(CAPEC | CWE) × P(CWE | CVE)]`
  - Estimate priors from Neo4j edge frequencies
  - Handle multiple chains per CVE (sum probabilities)
  - Return JSON: `{"cve_id": "CVE-2024-1234", "chains": [...], "overall_probability": 0.78, "confidence_interval": [0.72, 0.84]}`
- **Dependencies**: Neo4j semantic chains, statistical libraries (SciPy)
- **TASKMASTER Reference**: TASK-2025-11-12-010 (ML Engineer)

**FR-3.2: Customer-Specific Priors**
- **Description**: Adjust probabilities based on customer context
- **Acceptance Criteria**:
  - Industry sector modifiers (healthcare 1.3x for ransomware tactics, finance 1.5x for credential access)
  - Equipment type modifiers (Windows 1.2x for certain techniques, Linux 0.8x for others)
  - Geographic modifiers (APT targeting by region)
  - Stores priors in PostgreSQL `customer_profiles` table
- **Dependencies**: Customer metadata, historical attack data
- **TASKMASTER Reference**: TASK-2025-11-12-011 (Domain Expert Analyst)

**FR-3.3: Monte Carlo Simulation**
- **Description**: Quantify uncertainty in probability estimates
- **Acceptance Criteria**:
  - Run 10,000+ simulations per CVE
  - Sample from beta distributions for each edge probability
  - Calculate 95% confidence intervals using Wilson Score
  - Execution time: < 5 seconds per CVE
- **Dependencies**: NumPy, multiprocessing
- **TASKMASTER Reference**: TASK-2025-11-12-012 (Statistical Modeling Engineer)

**FR-3.4: Batch Scoring API**
- **Description**: Score multiple CVEs in parallel
- **Acceptance Criteria**:
  - Endpoint: `POST /api/v1/score_batch` with JSON array `["CVE-2024-1", "CVE-2024-2", ...]`
  - Parallel processing: 8 worker threads
  - Rate limit: 10,000 CVEs/minute
  - Response includes all scores + metadata (execution time, chain completeness)
- **Dependencies**: FastAPI, Redis for caching
- **TASKMASTER Reference**: TASK-2025-11-12-013 (Backend Engineer)

### 3.4 Graph Neural Network

**FR-4.1: GNN Model Training**
- **Description**: Train link prediction model on Neo4j graph
- **Acceptance Criteria**:
  - Architecture: 3-layer GAT with 128-dimensional hidden layers
  - Training set: 80% of 3.3M edges (stratified sampling)
  - Validation set: 10% (for hyperparameter tuning)
  - Test set: 10% (held-out for final evaluation)
  - Metrics: Precision ≥ 90%, Recall ≥ 85%, F1 ≥ 87%
- **Dependencies**: PyTorch Geometric, CUDA GPU access
- **TASKMASTER Reference**: TASK-2025-11-12-014 (ML Research Engineer)

**FR-4.2: Missing Link Prediction**
- **Description**: Predict CVE → CWE links when NVD data is incomplete
- **Acceptance Criteria**:
  - Input: CVE description text + known CWE for similar CVEs
  - Output: Top 5 predicted CWEs with confidence scores
  - Threshold: Only suggest if confidence > 70%
  - Human-in-the-loop: Flag predictions for analyst review
- **Dependencies**: GNN model, NER v9 for text embeddings
- **TASKMASTER Reference**: TASK-2025-11-12-015 (ML Application Engineer)

**FR-4.3: Multi-Hop Reasoning**
- **Description**: Answer complex graph queries (e.g., "Which CVEs lead to lateral movement via credential dumping?")
- **Acceptance Criteria**:
  - Cypher template library: 20+ common query patterns
  - Natural language interface (future: GPT-4 query translation)
  - Path ranking: order results by probability score
  - Query performance: < 500ms for 10-hop queries on 3.3M edge graph
- **Dependencies**: Neo4j APOC procedures, GNN embeddings for similarity
- **TASKMASTER Reference**: TASK-2025-11-12-016 (Query Optimization Engineer)

### 3.5 Equipment and Asset Management

**FR-5.1: Equipment Inventory Import**
- **Description**: Ingest customer asset lists from CSV, API, or CMDB
- **Acceptance Criteria**:
  - Supported formats: CSV (headers: hostname, software, version, location, criticality), JSON API, ServiceNow CMDB connector
  - CPE matching: map software names to NIST CPE dictionary
  - Fuzzy matching: handle "Microsoft Windows Server 2019" vs. "Windows Server 2019 Datacenter"
  - Auto-match rate: ≥ 95% for common software (Windows, Linux, Apache, nginx)
- **Dependencies**: NIST CPE dictionary, FuzzyWuzzy library
- **TASKMASTER Reference**: TASK-2025-11-12-017 (Integration Engineer)

**FR-5.2: CVE → Equipment Mapping**
- **Description**: Link CVEs to customer equipment via CPE
- **Acceptance Criteria**:
  - Query NVD API for CVE `configurations.nodes.cpe_match`
  - Match against customer equipment CPEs
  - Create Neo4j `(:Equipment)-[:AFFECTED_BY]->(:CVE)` edges
  - Update mappings daily (as new CVEs published)
- **Dependencies**: Equipment inventory, NVD CPE data
- **TASKMASTER Reference**: TASK-2025-11-12-018 (Vulnerability Mapping Engineer)

**FR-5.3: Attack Surface Calculation**
- **Description**: Calculate total CVE exposure per customer
- **Acceptance Criteria**:
  - Aggregate CVEs by equipment, network location (internal/DMZ/external), criticality
  - Score each CVE using AttackChainScorer (FR-3.1)
  - Generate risk heatmap: equipment × tactic matrix
  - Export to CSV, JSON, or PDF report
- **Dependencies**: Equipment mappings, AttackChainScorer
- **TASKMASTER Reference**: TASK-2025-11-12-019 (Risk Analysis Engineer)

### 3.6 Mitigation and Detection

**FR-6.1: Mitigation Recommendation**
- **Description**: Suggest mitigations from ATT&CK framework
- **Acceptance Criteria**:
  - Query ATT&CK `mitigations` for techniques in CVE attack chains
  - Prioritize by technique probability (from FR-3.1)
  - Include patching guidance (link to vendor advisories)
  - Compensating controls: if patch unavailable, suggest network segmentation, WAF rules, etc.
- **Dependencies**: ATT&CK mitigations, CVE attack chains
- **TASKMASTER Reference**: TASK-2025-11-12-020 (Security Operations Engineer)

**FR-6.2: Detection Rule Generation**
- **Description**: Auto-generate SIEM/EDR rules for CVE-associated techniques
- **Acceptance Criteria**:
  - Template library: Splunk SPL, Microsoft Sentinel KQL, Sigma YAML
  - Variables: process names, file paths, registry keys from ATT&CK technique data
  - Test rules against MITRE ATT&CK Evals public logs
  - Success rate: ≥ 80% rules deploy without syntax errors
- **Dependencies**: ATT&CK technique details, SIEM syntax libraries
- **TASKMASTER Reference**: TASK-2025-11-12-021 (Detection Engineering Lead)

**FR-6.3: Priority Action Planner**
- **Description**: Generate ranked remediation to-do list
- **Acceptance Criteria**:
  - Rank by: (Probability × CVSS Impact) - Remediation Effort
  - Effort estimator: patch (low), config change (low), software upgrade (medium), architecture change (high)
  - Timeline: account for patch cycles (monthly), change windows (quarterly)
  - Output: JSON `[{rank: 1, cve_id: "CVE-2024-X", action: "Patch Windows Server", effort: "low", deadline: "2025-12-01"}, ...]`
- **Dependencies**: Attack surface, scoring, mitigation engine
- **TASKMASTER Reference**: TASK-2025-11-12-022 (Remediation Strategy Lead)

---

## Section 4: Non-Functional Requirements

### 4.1 Performance

**NFR-1.1: API Response Times**
- Single CVE scoring: < 2 seconds (p99)
- Batch scoring (1,000 CVEs): < 60 seconds
- Equipment attack surface: < 10 seconds
- Graph queries (10-hop): < 500ms
- Dashboard load: < 2 seconds

**NFR-1.2: Scalability**
- Support 1M+ CVEs in Neo4j
- Handle 10,000+ simultaneous API requests
- Process 10,000+ daily CVE updates
- Store 100,000+ customer equipment records

**NFR-1.3: Availability**
- System uptime: 99.5% (4.38 hours downtime/year)
- Database replication: PostgreSQL streaming, Neo4j Causal Cluster
- Automated failover: < 30 seconds

### 4.2 Security

**NFR-2.1: Authentication and Authorization**
- **NEVER BREAK CLERK AUTH** on Next.js frontend (Constitutional mandate)
- API authentication: JWT tokens with 1-hour expiration
- Role-based access control (RBAC): admin, analyst, read-only
- Multi-tenant isolation: customer data segregated by `customer_id`

**NFR-2.2: Data Protection**
- Encryption at rest: PostgreSQL pgcrypto, Neo4j encrypted volumes
- Encryption in transit: TLS 1.3 for all connections
- Secrets management: Kubernetes secrets, AWS Secrets Manager
- Audit logging: All API calls logged to PostgreSQL with user ID, timestamp, action

**NFR-2.3: Vulnerability Management**
- Monthly dependency scans: `npm audit`, `pip-audit`
- Container image scanning: Trivy, Clair
- Penetration testing: Annual third-party assessment
- Bug bounty program: HackerOne (Phase 5)

### 4.3 Reliability

**NFR-3.1: Job Persistence**
- **CRITICAL**: 100% job reliability (zero lost jobs)
- PostgreSQL `jobs` table with ACID guarantees
- Retry logic: 3 attempts with exponential backoff (1s, 4s, 16s)
- Dead letter queue: Failed jobs after 3 retries go to `failed_jobs` table for manual review

**NFR-3.2: Data Integrity**
- Daily Neo4j backups to MinIO (retention: 30 days)
- PostgreSQL WAL archiving (point-in-time recovery)
- Consistency checks: Automated Cypher queries validate no orphaned nodes

**NFR-3.3: Monitoring**
- Health checks: `/api/health` endpoint (database connectivity, disk space, memory)
- Metrics: Prometheus + Grafana (request rates, latencies, error rates)
- Alerting: PagerDuty for critical failures (database down, API errors > 5%)

### 4.4 Usability

**NFR-4.1: Documentation**
- API reference: OpenAPI 3.0 spec (auto-generated from FastAPI)
- User guide: Step-by-step tutorials for common workflows
- Video demos: 5-minute walkthroughs (YouTube, Loom)
- Code samples: Python, JavaScript, cURL for all API endpoints

**NFR-4.2: User Interface**
- Mobile-responsive: Works on tablets, desktops
- Accessibility: WCAG 2.1 AA compliance (keyboard navigation, screen readers)
- Load times: < 2 seconds for all pages
- Error messages: Clear, actionable (not "Error 500", but "Database connection failed. Contact support@aeon.com")

### 4.5 Maintainability

**NFR-5.1: Code Quality**
- Test coverage: ≥ 80% (Jest for frontend, pytest for backend)
- Linting: ESLint, Pylint (enforced in CI/CD)
- Code reviews: All PRs require 1 approval
- Documentation: Inline comments for complex logic, README per repository

**NFR-5.2: DevOps**
- CI/CD: GitHub Actions (build, test, deploy on every push to `main`)
- Infrastructure as Code: Terraform for AWS, Kubernetes manifests
- Rollback capability: Blue-green deployments, instant rollback on errors
- Automated testing: Unit, integration, E2E tests in CI pipeline

---

## Section 5: Success Metrics and KPIs

### 5.1 Phase 1 Success Metrics (Months 1-3)

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Semantic chain completeness | ≥ 80% CVEs | Cypher query: `MATCH (cve:CVE)...RETURN count(*)` |
| Job reliability | 100% (zero lost jobs) | PostgreSQL `jobs` table: `SELECT COUNT(*) WHERE status='failed' AND retries_exhausted=true` |
| Data freshness | < 24 hours lag | NVD API timestamp vs. Neo4j ingestion timestamp |
| API uptime | ≥ 99.0% | Prometheus `up` metric |

### 5.2 Phase 2 Success Metrics (Months 4-6)

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Scoring accuracy | ≥ 85% | Evaluate predictions against known exploited CVEs (CISA KEV catalog) |
| API response time (p99) | < 2 seconds | Prometheus histogram |
| Confidence interval coverage | 95% | Wilson Score statistical test |
| Customer satisfaction | ≥ 4.0/5.0 | Post-demo survey (5-point Likert scale) |

### 5.3 Phase 3 Success Metrics (Months 7-9)

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| GNN precision | ≥ 90% | Test set evaluation (10% held-out edges) |
| Multi-hop query performance | < 500ms | Prometheus query duration |
| Embedding quality | ≥ 0.80 AUC | Link prediction AUC-ROC curve |

### 5.4 Phase 4 Success Metrics (Months 10-12)

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| CPE auto-match rate | ≥ 95% | `matched_equipment / total_equipment` |
| Attack surface calculation time | < 10 seconds | API response time |
| Equipment onboarding time | < 15 minutes | User stopwatch test (import 1,000 assets) |

### 5.5 Phase 5 Success Metrics (Months 13-15)

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Mitigation coverage | ≥ 90% | CVEs with ≥1 mitigation / total scored CVEs |
| Detection rule success rate | ≥ 80% | Rules that deploy without syntax errors |
| McKenney's 8 questions answered | 8 of 8 | Manual review: can system answer all questions at 95%+ confidence? |

### 5.6 Business Impact Metrics

| Metric | Baseline (No AEON) | Target (With AEON) |
|--------|-------------------|-------------------|
| Time to answer "What's my risk?" | 14 hours (manual) | 2 minutes (automated) |
| False positive rate | 60% | < 20% |
| Analyst time on CVE correlation | 70% of week | < 10% of week |
| Mean time to prioritize vulnerabilities | 18+ months | Real-time |
| Cost of missed critical CVEs | $2.4M/year | < $500K/year (80% reduction) |

---

## Section 6: Phased Implementation Plan

### Phase 1: Semantic Foundation (Months 1-3)

**Milestones**:
- Week 1-2: PostgreSQL job persistence schema (FR-1.1)
- Week 3-4: CVE → CWE mapping (FR-2.1)
- Week 5-6: CWE → CAPEC mapping (FR-2.2)
- Week 7-8: CAPEC → Technique mapping (FR-2.3)
- Week 9-10: Technique → Tactic mapping (FR-2.4)
- Week 11-12: Full chain validation + testing (FR-2.5)

**Deliverables**:
- ✅ Neo4j with 8,000+ complete semantic chains
- ✅ PostgreSQL `jobs` table with 100% reliability
- ✅ Automated daily CVE updates
- ✅ Phase 1 completion report

**TASKMASTER Tasks**: TASK-2025-11-12-002 through TASK-2025-11-12-009

### Phase 2: Probabilistic Intelligence (Months 4-6)

**Milestones**:
- Month 4: AttackChainScorer implementation (FR-3.1)
- Month 5: Customer-specific priors + Monte Carlo (FR-3.2, FR-3.3)
- Month 6: Batch scoring API + performance optimization (FR-3.4)

**Deliverables**:
- ✅ Bayesian scoring engine with 85%+ accuracy
- ✅ RESTful API: `/api/v1/score_cve`, `/api/v1/score_batch`
- ✅ 95% confidence intervals for all scores
- ✅ Phase 2 validation report (test against CISA KEV catalog)

**TASKMASTER Tasks**: TASK-2025-11-12-010 through TASK-2025-11-12-013

### Phase 3: Graph Neural Networks (Months 7-9)

**Milestones**:
- Month 7: GNN model training (FR-4.1)
- Month 8: Missing link prediction (FR-4.2)
- Month 9: Multi-hop reasoning engine (FR-4.3)

**Deliverables**:
- ✅ Trained GAT model (90%+ precision)
- ✅ Link prediction API for incomplete CVE data
- ✅ 20+ hop query capability
- ✅ Phase 3 performance benchmark report

**TASKMASTER Tasks**: TASK-2025-11-12-014 through TASK-2025-11-12-016

### Phase 4: Equipment Integration (Months 10-12)

**Milestones**:
- Month 10: Equipment inventory import (FR-5.1)
- Month 11: CVE → Equipment mapping (FR-5.2)
- Month 12: Attack surface calculator + dashboard (FR-5.3)

**Deliverables**:
- ✅ CSV/API/CMDB import connectors
- ✅ Automated CPE matching (95%+ auto-match)
- ✅ Risk heatmap dashboard
- ✅ Phase 4 customer pilot (5 beta customers)

**TASKMASTER Tasks**: TASK-2025-11-12-017 through TASK-2025-11-12-019

### Phase 5: Actionable Outputs (Months 13-15)

**Milestones**:
- Month 13: Mitigation recommendation engine (FR-6.1)
- Month 14: Detection rule generator (FR-6.2)
- Month 15: Priority action planner (FR-6.3)

**Deliverables**:
- ✅ Automated mitigation suggestions (90%+ coverage)
- ✅ SIEM/EDR rule templates (Splunk, Sentinel, Sigma)
- ✅ Ranked remediation to-do lists
- ✅ **Final validation**: Can we answer all 8 McKenney questions at 95%+ confidence?

**TASKMASTER Tasks**: TASK-2025-11-12-020 through TASK-2025-11-12-022

---

## Section 7: Dependencies and Risks

### 7.1 External Dependencies

| Dependency | Provider | Risk | Mitigation |
|------------|----------|------|------------|
| NVD CVE API | NIST | Rate limits, downtime | Cache CVE data, retry with exponential backoff |
| MITRE ATT&CK | MITRE Corporation | Framework changes | Version tracking, automated compatibility tests |
| MITRE CAPEC | MITRE Corporation | Deprecation of IDs | Graceful handling, fallback to CWE-only chains |
| Clerk Authentication | Clerk.com | Service outage | **NEVER BREAK** - have backup local auth (disabled by default) |
| Neo4j Community Edition | Neo4j Inc. | License changes | Budget for Enterprise if needed (Phase 4+) |

### 7.2 Technical Risks

**RISK-1: Neo4j Performance Degradation (CRITICAL)**
- **Description**: 3.3M edges may slow queries as data grows
- **Probability**: 60%
- **Impact**: API response times > 5 seconds (NFR-1.1 violation)
- **Mitigation**:
  - Index all relationship types
  - Neo4j Causal Cluster (Phase 4)
  - Query caching in Redis
  - Horizontal scaling (multiple Neo4j instances)
- **TASKMASTER Reference**: TASK-2025-11-12-023 (Performance Engineer)

**RISK-2: Incomplete CVE → CWE Mappings (HIGH)**
- **Description**: NVD data quality varies; some CVEs lack CWE
- **Probability**: 80% (known issue)
- **Impact**: Semantic chains incomplete (< 80% target)
- **Mitigation**:
  - NER v9 fallback: extract CWE from CVE descriptions
  - GNN link prediction (Phase 3)
  - Manual curation for critical CVEs
- **TASKMASTER Reference**: TASK-2025-11-12-024 (Data Quality Analyst)

**RISK-3: Bayesian Model Overfitting (MEDIUM)**
- **Description**: Priors trained on historical data may not generalize to zero-day exploits
- **Probability**: 40%
- **Impact**: Accuracy < 85% on novel attack patterns
- **Mitigation**:
  - Regularization (Laplace smoothing)
  - Cross-validation on multiple time periods
  - Ensemble methods (combine Bayesian + GNN scores)
- **TASKMASTER Reference**: TASK-2025-11-12-025 (ML QA Engineer)

**RISK-4: GNN Training Data Bias (MEDIUM)**
- **Description**: Neo4j edges may reflect reporting bias (more edges for popular CVEs)
- **Probability**: 50%
- **Impact**: GNN predicts popular links, misses rare but critical ones
- **Mitigation**:
  - Stratified sampling by CVE severity
  - Synthetic edge generation for underrepresented classes
  - Domain expert validation of predictions
- **TASKMASTER Reference**: TASK-2025-11-12-026 (ML Fairness Engineer)

**RISK-5: Equipment CPE Matching Failures (MEDIUM)**
- **Description**: Customer asset names may not match NIST CPE dictionary
- **Probability**: 30%
- **Impact**: Auto-match rate < 95% (NFR)
- **Mitigation**:
  - Fuzzy matching with FuzzyWuzzy (edit distance)
  - Manual mapping interface for unmatched software
  - CPE alias database (e.g., "Win10" → "cpe:2.3:o:microsoft:windows_10")
- **TASKMASTER Reference**: TASK-2025-11-12-027 (Integration QA Engineer)

### 7.3 Operational Risks

**RISK-6: Agent Coordination Failures (HIGH)**
- **Description**: 16 Ruv-Swarm agents may have race conditions, deadlocks
- **Probability**: 50%
- **Impact**: Jobs fail silently, 0% reliability
- **Mitigation**:
  - PostgreSQL advisory locks
  - Agent health checks every 60 seconds
  - Automatic agent restart on failure
  - **Ruv-Swarm orchestration monitoring in Qdrant**
- **TASKMASTER Reference**: TASK-2025-11-12-028 (DevOps Reliability Engineer)

**RISK-7: Qdrant Vector Store Corruption (MEDIUM)**
- **Description**: Currently "unhealthy" status on Qdrant container
- **Probability**: 40%
- **Impact**: Agent memory loss, context degradation
- **Mitigation**:
  - **IMMEDIATE ACTION**: Debug Qdrant health check (TASK-2025-11-12-029)
  - Daily Qdrant snapshots to MinIO
  - Fallback to in-memory storage (degraded mode)
- **TASKMASTER Reference**: TASK-2025-11-12-029 (Storage Engineer)

**RISK-8: Clerk Auth Breakage (CATASTROPHIC)**
- **Description**: Code changes inadvertently disable authentication
- **Probability**: 10% (Constitutional protection in place)
- **Impact**: **Unauthorized access to all customer data**
- **Mitigation**:
  - **Constitutional Rule**: NEVER BREAK CLERK AUTH
  - Automated E2E tests: login flow on every deploy
  - Code review checklist: "Did this change affect auth?"
  - Rollback within 30 seconds if auth fails
- **TASKMASTER Reference**: TASK-2025-11-12-030 (Security Compliance Lead)

### 7.4 Resource Risks

**RISK-9: GPU Availability for GNN Training (MEDIUM)**
- **Description**: Phase 3 requires CUDA-compatible GPU
- **Probability**: 30%
- **Impact**: Training time 10x slower on CPU
- **Mitigation**:
  - AWS p3.2xlarge instances (NVIDIA V100)
  - Google Colab Pro (fallback)
  - Pre-trained model transfer learning
- **TASKMASTER Reference**: TASK-2025-11-12-031 (Infrastructure Engineer)

**RISK-10: Team Expertise Gaps (HIGH)**
- **Description**: Bayesian statistics, GNN, Neo4j Cypher require specialized skills
- **Probability**: 60%
- **Impact**: Slower development, quality issues
- **Mitigation**:
  - Hire ML engineer with GNN experience (Phase 2 start)
  - Neo4j certification for 2 team members
  - External consultant for Bayesian modeling (Month 4)
- **TASKMASTER Reference**: TASK-2025-11-12-032 (Hiring Manager)

---

## Section 8: Acceptance Criteria Summary

### 8.1 Phase 1 Acceptance Criteria

**To exit Phase 1, ALL must be TRUE**:
- [ ] 8,000+ CVEs have complete semantic chains (CVE → CWE → CAPEC → Technique → Tactic)
- [ ] PostgreSQL `jobs` table shows 100% reliability (zero failed jobs with exhausted retries)
- [ ] Daily NVD updates run successfully for 14 consecutive days
- [ ] Chain completeness monitoring alerts fire correctly (tested by artificially dropping completeness)
- [ ] All Phase 1 unit tests pass (≥ 80% code coverage)

### 8.2 Phase 2 Acceptance Criteria

**To exit Phase 2, ALL must be TRUE**:
- [ ] AttackChainScorer predicts ≥ 85% of CISA KEV exploits correctly (validate against Known Exploited Vulnerabilities catalog)
- [ ] Batch scoring API processes 1,000 CVEs in < 60 seconds
- [ ] All scores include 95% confidence intervals (Wilson Score)
- [ ] Customer-specific priors adjust scores by ≥ 10% (validate with test customer profiles)
- [ ] API uptime ≥ 99.5% over 30-day period

### 8.3 Phase 3 Acceptance Criteria

**To exit Phase 3, ALL must be TRUE**:
- [ ] GNN link prediction achieves ≥ 90% precision on test set
- [ ] Multi-hop queries (10 hops) complete in < 500ms
- [ ] Missing link prediction suggests ≥ 1 CWE for 95% of CVEs lacking NVD data
- [ ] Embedding quality: AUC-ROC ≥ 0.80 on link prediction task

### 8.4 Phase 4 Acceptance Criteria

**To exit Phase 4, ALL must be TRUE**:
- [ ] Equipment import processes 1,000+ assets in < 15 minutes
- [ ] CPE auto-match rate ≥ 95% on test asset list (100 common software packages)
- [ ] Attack surface calculator completes in < 10 seconds for customer with 10,000 assets
- [ ] Risk heatmap dashboard loads in < 2 seconds
- [ ] 5 beta customers complete pilot successfully (satisfaction ≥ 4.0/5.0)

### 8.5 Phase 5 Acceptance Criteria

**To exit Phase 5, ALL must be TRUE**:
- [ ] **McKenney's 8 questions**: Manual review confirms ALL 8 questions answerable at 95%+ confidence
- [ ] Mitigation coverage: ≥ 90% of scored CVEs have ≥1 mitigation suggestion
- [ ] Detection rule generator: ≥ 80% of rules deploy without syntax errors (test with Splunk sandbox)
- [ ] Priority action planner generates ranked to-do list in < 5 seconds
- [ ] Customer satisfaction ≥ 4.5/5.0 (post-Phase 5 survey)

---

## Section 9: TASKMASTER Integration

### 9.1 Task Structure Template

All tasks MUST follow this format (per Constitution Article II, Section 2.5):

```yaml
task:
  id: "TASK-YYYY-MM-DD-NNN"
  created: "YYYY-MM-DD HH:MM:SS UTC"
  assigned_to: "[agent_name or human_name]"
  priority: "[CRITICAL | HIGH | MEDIUM | LOW]"
  deadline: "YYYY-MM-DD"

  deliverables:
    - "Specific, measurable output 1"
    - "Specific, measurable output 2"

  success_criteria:
    - "Quantifiable metric 1 (e.g., test coverage ≥ 80%)"
    - "Quantifiable metric 2"

  risks:
    - "Potential blocker 1"
    - "Potential blocker 2"

  issues:
    - "[Current blockers if any]"

  notes:
    - "Context, background, or special instructions"

  memory_keys:
    - "qdrant_collection_name/key_1"
    - "qdrant_collection_name/key_2"

  dependencies:
    - "TASK-YYYY-MM-DD-XXX (blocking)"
    - "TASK-YYYY-MM-DD-YYY (soft dependency)"

  status: "[CREATED | ASSIGNED | IN_PROGRESS | BLOCKED | COMPLETED | ARCHIVED]"
  status_updated: "YYYY-MM-DD HH:MM:SS UTC"
```

### 9.2 Example TASKMASTER Tasks

**TASK-2025-11-12-002: Data Pipeline Engineer**
```yaml
task:
  id: "TASK-2025-11-12-002"
  created: "2025-11-12 06:00:00 UTC"
  assigned_to: "data_pipeline_engineer"
  priority: "CRITICAL"
  deadline: "2025-12-15"

  deliverables:
    - "NVD API integration script (Python) that runs at 02:00 UTC daily"
    - "PostgreSQL job_logs table with ingestion timestamps, error counts"
    - "Retry logic: 3 attempts with exponential backoff (1s, 4s, 16s)"

  success_criteria:
    - "Imports ≥ 95% of CVEs published in last 24 hours"
    - "Zero failed jobs (after 3 retries)"
    - "Execution time < 15 minutes for 500 CVEs/day"

  risks:
    - "NVD API rate limits (10 requests/30 seconds)"
    - "Network timeouts during large batch imports"

  issues:
    - "None currently"

  notes:
    - "Use `nvdlib` Python library for API calls"
    - "Store raw JSON in MinIO for audit trail"

  memory_keys:
    - "task_history/data_pipeline_002"
    - "agent_memory/data_pipeline_engineer/nvd_integration"

  dependencies:
    - "None (foundational task)"

  status: "CREATED"
  status_updated: "2025-11-12 06:00:00 UTC"
```

**TASK-2025-11-12-010: ML Engineer (AttackChainScorer)**
```yaml
task:
  id: "TASK-2025-11-12-010"
  created: "2025-11-12 06:15:00 UTC"
  assigned_to: "ml_engineer"
  priority: "HIGH"
  deadline: "2026-03-15"

  deliverables:
    - "AttackChainScorer class in Python (src/intelligence/scorer.py)"
    - "Bayesian probability calculation: P(Tactic | CVE)"
    - "Unit tests with ≥ 85% code coverage"

  success_criteria:
    - "Accuracy ≥ 85% on CISA KEV test set (100 known exploited CVEs)"
    - "Execution time < 2 seconds per CVE (p99)"
    - "Returns JSON with overall_probability and confidence_interval"

  risks:
    - "Sparse data: some CVEs have only 1 chain path (no probability variation)"
    - "Prior estimation: edge frequencies may not reflect real-world likelihoods"

  issues:
    - "Need historical exploit data to validate priors (waiting on CISA KEV download)"

  notes:
    - "Use SciPy for beta distributions"
    - "Laplace smoothing to handle zero-count edges"
    - "Consult external statistician for prior selection"

  memory_keys:
    - "task_history/ml_engineer_010"
    - "agent_memory/ml_engineer/bayesian_scoring"
    - "model_artifacts/attack_chain_scorer_v1"

  dependencies:
    - "TASK-2025-11-12-009 (semantic chain validation - must be 80%+ complete)"

  status: "CREATED"
  status_updated: "2025-11-12 06:15:00 UTC"
```

### 9.3 Agent Assignment Matrix

| Agent Type (Ruv-Swarm) | Assigned Tasks | Primary Responsibilities |
|------------------------|----------------|--------------------------|
| **data_pipeline_engineer** | TASK-002, TASK-003, TASK-004 | NVD/ATT&CK/CAPEC ingestion, data validation |
| **knowledge_graph_engineer** | TASK-003, TASK-005, TASK-006, TASK-007, TASK-008 | Neo4j schema, semantic chains, Cypher queries |
| **ml_engineer** | TASK-010, TASK-012, TASK-014 | Bayesian scoring, GNN training, Monte Carlo |
| **backend_engineer** | TASK-013 (Batch API) | FastAPI, Redis caching, performance optimization |
| **integration_engineer** | TASK-017 (Equipment import) | CSV/API connectors, CPE matching |
| **security_operations_engineer** | TASK-020 (Mitigations) | ATT&CK mitigation queries, patching guidance |
| **detection_engineering_lead** | TASK-021 (SIEM rules) | Splunk/Sentinel/Sigma templates |
| **qa_engineer** | TASK-009 (Chain validation) | Automated testing, CI/CD integration |
| **devops_reliability_engineer** | TASK-028 (Agent health) | Monitoring, alerting, failover |
| **storage_engineer** | TASK-029 (Qdrant debug) | **URGENT**: Fix Qdrant unhealthy status |

---

## Section 10: Qdrant Memory Architecture

### 10.1 Collections Schema

**Collection: `agent_memory`**
- **Purpose**: Cross-agent persistent memory for task coordination
- **Vector Size**: 768 (BERT embeddings)
- **Distance**: Cosine similarity
- **Payload Schema**:
  ```json
  {
    "agent_id": "ml_engineer",
    "task_id": "TASK-2025-11-12-010",
    "memory_type": "decision",
    "timestamp": "2025-11-12T06:15:00Z",
    "content": "Chose Laplace smoothing for zero-count edge handling",
    "related_agents": ["data_pipeline_engineer", "qa_engineer"],
    "tags": ["bayesian", "smoothing", "phase_2"]
  }
  ```

**Collection: `task_history`**
- **Purpose**: Complete task execution history
- **Vector Size**: 768
- **Distance**: Cosine
- **Payload Schema**:
  ```json
  {
    "task_id": "TASK-2025-11-12-010",
    "status": "COMPLETED",
    "completion_timestamp": "2026-03-20T14:30:00Z",
    "deliverables": ["scorer.py", "tests/test_scorer.py"],
    "success_metrics": {"accuracy": 0.87, "latency_p99": 1.8},
    "lessons_learned": "Monte Carlo simulation needed GPU acceleration",
    "next_actions": ["Deploy to staging", "Run load tests"]
  }
  ```

**Collection: `semantic_chains`**
- **Purpose**: Cache computed semantic chains for fast retrieval
- **Vector Size**: 768
- **Distance**: Cosine
- **Payload Schema**:
  ```json
  {
    "cve_id": "CVE-2024-1234",
    "chain_path": ["CVE-2024-1234", "CWE-79", "CAPEC-63", "T1059", "TA0002"],
    "chain_probability": 0.78,
    "computed_at": "2025-11-15T10:00:00Z",
    "ttl": "2025-12-15T10:00:00Z"
  }
  ```

### 10.2 Memory Operations

**Store Task Update**:
```python
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

client = QdrantClient(url="http://172.18.0.6:6333")

client.upsert(
    collection_name="task_history",
    points=[
        PointStruct(
            id=hash("TASK-2025-11-12-010"),
            vector=embedding_model.encode("AttackChainScorer implementation"),
            payload={
                "task_id": "TASK-2025-11-12-010",
                "status": "IN_PROGRESS",
                "last_update": "2026-02-15T09:00:00Z",
                "blocker": "Waiting for CISA KEV dataset"
            }
        )
    ]
)
```

**Retrieve Related Tasks**:
```python
results = client.search(
    collection_name="task_history",
    query_vector=embedding_model.encode("Bayesian scoring CVE risk"),
    limit=5,
    score_threshold=0.7
)

for hit in results:
    print(f"Related task: {hit.payload['task_id']}, similarity: {hit.score}")
```

---

## Section 11: Path Integrity and File Management

### 11.1 Path Verification Script

**File**: `/scripts/verify_paths.sh`
```bash
#!/bin/bash
# Path integrity checker (Constitutional Article II, Section 2.8)

echo "🔍 Verifying API endpoints..."
grep -r "app.get\|app.post" backend/ | while read -r line; do
    endpoint=$(echo "$line" | grep -oP '(?<=["'"'"'])/api/[^"'"'"']+')
    if ! grep -q "$endpoint" frontend/src/; then
        echo "⚠️  Orphaned endpoint: $endpoint (no frontend reference)"
    fi
done

echo "🔍 Verifying Neo4j Cypher queries..."
grep -r "session.run" backend/ | while read -r file_line; do
    file=$(echo "$file_line" | cut -d: -f1)
    if ! grep -q "neo4j" "$file"; then
        echo "⚠️  Missing neo4j import in $file"
    fi
done

echo "🔍 Verifying database connections..."
for service in aeon-saas-dev openspg-server; do
    docker exec "$service" pg_isready -h aeon-postgres-dev -p 5432 || echo "❌ PostgreSQL unreachable from $service"
    docker exec "$service" curl -f http://openspg-neo4j:7474 || echo "❌ Neo4j unreachable from $service"
done

echo "✅ Path verification complete"
```

### 11.2 File Migration Checklist

**Before moving ANY file** (Constitutional mandate):
1. [ ] Run `git grep "old_file_name"` to find all references
2. [ ] Update all import statements, API calls, configuration files
3. [ ] Create temporary symlink: `ln -s new/path/file.ts old/path/file.ts`
4. [ ] Run full test suite: `npm test && pytest`
5. [ ] Run path verification: `bash scripts/verify_paths.sh`
6. [ ] Update `CHANGELOG.md` with migration entry
7. [ ] Deploy to staging, test all affected endpoints
8. [ ] Remove symlink only after 30-day grace period

---

## Section 12: Next Steps After PRD Approval

### 12.1 Immediate Actions (Week 1)

1. **Qdrant Health Check** (TASK-2025-11-12-029)
   - Debug why openspg-qdrant container is "unhealthy"
   - Verify Qdrant API responds: `curl http://172.18.0.6:6333/collections`
   - Restore from backup if needed

2. **OpenSPG Server Health Check** (TASK-2025-11-12-033)
   - Investigate unhealthy status
   - Review logs: `docker logs openspg-server --tail 100`
   - Restart if configuration issue

3. **Phase 1 Kickoff Meeting**
   - Review this PRD with full development team
   - Assign TASKMASTER tasks to agents and humans
   - Set up daily standups (15 minutes, 09:00 UTC)

4. **Create Technical Specifications** (Next PRD deliverable)
   - API endpoint specifications (OpenAPI 3.0)
   - Database schemas (DDL scripts)
   - Class diagrams for AttackChainScorer, GNN models
   - Deployment architecture (Kubernetes manifests)

### 12.2 Documentation Roadmap

**Completed**:
- ✅ Constitution (`00_AEON_CONSTITUTION.md`)
- ✅ Architecture (`01_ARCHITECTURE/01_COMPREHENSIVE_ARCHITECTURE.md`)
- ✅ PRD (`02_REQUIREMENTS/01_PRODUCT_REQUIREMENTS.md`)

**Next to Create**:
- ⏳ Technical Specifications (`03_SPECIFICATIONS/01_TECHNICAL_SPECS.md`)
- ⏳ User Stories (`04_USER_STORIES/01_USER_STORIES.md`)
- ⏳ TASKMASTER Implementation Plan (`05_TASKMASTER/01_IMPLEMENTATION_PLAN.md`)
- ⏳ Existing Resources Inventory (`05_TASKMASTER/02_RESOURCE_INVENTORY.md`)
- ⏳ Path Verification Script (`/scripts/verify_paths.sh`)

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **ATT&CK** | MITRE Adversarial Tactics, Techniques, and Common Knowledge framework |
| **CAPEC** | Common Attack Pattern Enumeration and Classification |
| **CPE** | Common Platform Enumeration (NIST standard for software/hardware naming) |
| **CVE** | Common Vulnerabilities and Exposures |
| **CWE** | Common Weakness Enumeration |
| **GAT** | Graph Attention Network (GNN architecture) |
| **GNN** | Graph Neural Network |
| **KEV** | Known Exploited Vulnerabilities (CISA catalog) |
| **NER** | Named Entity Recognition |
| **NVD** | National Vulnerability Database (NIST) |
| **RBAC** | Role-Based Access Control |
| **Tactic** | High-level ATT&CK objective (14 tactics: Initial Access, Execution, etc.) |
| **Technique** | Specific ATT&CK method (193 techniques: e.g., T1566 Phishing) |
| **Wilson Score** | Statistical confidence interval for binomial proportions |

## Appendix B: Reference Links

- **NVD API**: https://nvd.nist.gov/developers/vulnerabilities
- **MITRE ATT&CK**: https://attack.mitre.org/
- **MITRE CAPEC**: https://capec.mitre.org/
- **MITRE CWE**: https://cwe.mitre.org/
- **CISA KEV Catalog**: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- **Neo4j Cypher Manual**: https://neo4j.com/docs/cypher-manual/
- **PyTorch Geometric**: https://pytorch-geometric.readthedocs.io/
- **Clerk Authentication**: https://clerk.com/docs

---

**Document Control**:
- **Approved By**: [Pending stakeholder review]
- **Review Cycle**: Quarterly
- **Next Review**: 2026-02-12
- **Change Log**:
  - v1.0.0 (2025-11-12): Initial PRD creation

**END OF PRODUCT REQUIREMENTS DOCUMENT**
