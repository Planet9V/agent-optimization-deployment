# AEON Digital Twin: User Stories and Acceptance Criteria

**File**: 01_USER_STORIES.md
**Created**: 2025-11-12 06:00:00 UTC
**Modified**: 2025-11-12 06:00:00 UTC
**Version**: 1.0.0
**Author**: AEON Development Team
**Purpose**: Comprehensive user stories with acceptance criteria for AEON Digital Twin platform
**Status**: ACTIVE - AUTHORITATIVE USER STORIES

**References**:
- Constitution: `/00_AEON_CONSTITUTION.md`
- Architecture: `/01_ARCHITECTURE/01_COMPREHENSIVE_ARCHITECTURE.md`
- PRD: `/02_REQUIREMENTS/01_PRODUCT_REQUIREMENTS.md`
- Technical Specs: `/03_SPECIFICATIONS/01_TECHNICAL_SPECS.md`

---

## Table of Contents

1. [User Persona Definitions](#section-1-user-persona-definitions)
2. [Phase 1 User Stories (Months 1-3)](#section-2-phase-1-user-stories)
3. [Phase 2 User Stories (Months 4-6)](#section-3-phase-2-user-stories)
4. [Phase 3 User Stories (Months 7-9)](#section-4-phase-3-user-stories)
5. [Phase 4 User Stories (Months 10-12)](#section-5-phase-4-user-stories)
6. [Phase 5 User Stories (Months 13-15)](#section-6-phase-5-user-stories)
7. [Cross-Phase Stories (Non-functional)](#section-7-cross-phase-stories)
8. [McKenney's 8 Questions Mapping](#section-8-mckenneys-8-questions-mapping)
9. [Story Point Estimates](#section-9-story-point-estimates)
10. [Prioritization Matrix](#section-10-prioritization-matrix)

---

## Section 1: User Persona Definitions

### Persona 1: Senior Security Analyst (Sarah Chen)

**Profile**:
- **Role**: Threat Intelligence Analyst
- **Organization**: Fortune 500 Financial Services
- **Experience**: 8+ years in cybersecurity
- **Technical Skills**: High (Python, SIEM, threat modeling)
- **Pain Points**:
  - Manual CVE-to-ATT&CK mapping consumes 14+ hours/week
  - Cannot quantify risk with confidence intervals
  - SIEM alert fatigue (10,000+ alerts/day, unsure which matter)
  - No equipment-specific threat intelligence

**Goals**:
- Automate semantic chain mapping (CVE → Tactic)
- Get probabilistic risk scores for all CVEs
- Prioritize remediation with data-driven confidence
- Generate SIEM rules for new threats automatically

**Technology Access**:
- Splunk SIEM
- CrowdStrike EDR
- Internal CMDB with 50,000+ assets
- Python scripting environment

---

### Persona 2: CISO/Security Director (Michael Rodriguez)

**Profile**:
- **Role**: Chief Information Security Officer
- **Organization**: Large Healthcare System
- **Experience**: 15+ years (technical + leadership)
- **Technical Skills**: Medium (high-level architecture, vendor evaluation)
- **Pain Points**:
  - Board asks "What's our cyber risk?" → cannot quantify
  - Compliance audits require proof of NIST CSF coverage
  - $5M security budget needs ROI justification
  - No way to compare vulnerability severity across vendors

**Goals**:
- Executive dashboard with risk trending
- Automated compliance gap analysis (NIST, ISO, CIS)
- Board-ready reports with confidence intervals
- ROI metrics: cost of vulnerabilities vs. mitigation spend

**Technology Access**:
- PowerBI/Tableau for dashboards
- Risk management platforms (Archer, ServiceNow GRC)
- Budget tracking tools

---

### Persona 3: SOC Analyst (Alex Thompson)

**Profile**:
- **Role**: Security Operations Center Analyst
- **Organization**: Managed Security Service Provider (MSSP)
- **Experience**: 3 years in SOC operations
- **Technical Skills**: Medium (SIEM queries, alert triage)
- **Pain Points**:
  - Monitors 50+ customers, cannot analyze every CVE manually
  - Prioritizes 500+ vulnerabilities/month without risk scores
  - Customers ask "Should I patch CVE-X?" → no data-driven answer
  - Spends 60% of time on false positive alerts

**Goals**:
- Bulk CVE analysis (process 1,000+ CVEs/hour)
- Multi-tenant equipment risk mapping
- Customer-facing risk reports (non-technical language)
- Automated alert tuning based on actual risk

**Technology Access**:
- Multi-tenant SIEM (Sentinel, QRadar)
- Vulnerability scanners (Nessus, Qualys)
- Ticketing systems (Jira, ServiceNow)

---

## Section 2: Phase 1 User Stories (Months 1-3)
### Semantic Foundation

---

### Story 1.1: Automated CVE Ingestion

**As a** Security Analyst
**I want** the system to automatically import CVEs from NVD daily
**So that** I always have the latest vulnerability data without manual effort

**Acceptance Criteria**:
- [ ] System runs at 02:00 UTC daily without manual intervention
- [ ] Imports all CVEs published in last 24 hours (≥ 95% completeness)
- [ ] Updates existing CVE records when NVD modifies CVSS or CWE
- [ ] Logs ingestion metrics: CVEs imported, errors, execution time
- [ ] Job persistence: 100% reliability (zero lost jobs after 3 retries)
- [ ] Alert to admin if ingestion fails 3 times consecutively
- [ ] Execution time < 15 minutes for typical daily load (500 CVEs)

**Priority**: CRITICAL
**Story Points**: 8
**TASKMASTER Reference**: TASK-2025-11-12-002
**Dependencies**: NVD API key, PostgreSQL jobs table, Neo4j connection

**Test Cases**:
1. **Happy Path**: Run ingestion, verify 500 CVEs imported in < 15 min
2. **NVD API Downtime**: Simulate NVD 503 error, verify retry with exponential backoff
3. **Duplicate CVE**: Import CVE-2024-1, update CVSS score, re-import, verify update
4. **Zero New CVEs**: Run on day with no new CVEs, verify graceful handling

---

### Story 1.2: CVE → CWE Semantic Mapping

**As a** Security Analyst
**I want** every CVE mapped to its Common Weakness Enumeration (CWE)
**So that** I can understand the root cause vulnerability class

**Acceptance Criteria**:
- [ ] 95%+ CVEs have at least one CWE mapping (from NVD data)
- [ ] Multiple CWEs per CVE supported (e.g., CVE-2024-1 → CWE-79, CWE-89)
- [ ] Default to `CWE-NVD-noinfo` when NVD provides no CWE
- [ ] Neo4j relationship: `(:CVE)-[:HAS_CWE {confidence: 0.95}]->(:CWE)`
- [ ] Confidence score stored: 0.95 for NVD-provided, < 0.80 for NER v9 extraction
- [ ] Daily validation job: check CWE mapping completeness, alert if < 90%

**Priority**: CRITICAL
**Story Points**: 5
**TASKMASTER Reference**: TASK-2025-11-12-005
**Dependencies**: Story 1.1 (CVE ingestion), CWE database

**Test Cases**:
1. **Single CWE**: CVE-2024-1 with one CWE → verify single edge created
2. **Multiple CWEs**: CVE-2024-2 with 3 CWEs → verify 3 edges created
3. **Missing CWE**: CVE with no NVD CWE → verify `CWE-NVD-noinfo` assigned
4. **NER v9 Fallback**: CVE description contains "SQL injection" → verify CWE-89 extracted with confidence < 0.80

---

### Story 1.3: CWE → CAPEC Semantic Mapping

**As a** Security Analyst
**I want** CWEs mapped to Common Attack Pattern Enumeration (CAPEC)
**So that** I can see how weaknesses are exploited in practice

**Acceptance Criteria**:
- [ ] 80%+ CWEs have at least one CAPEC mapping
- [ ] Uses MITRE CAPEC database `Related_Weaknesses` field
- [ ] 1-to-many relationships supported (CWE-79 → 5 CAPECs)
- [ ] Neo4j relationship: `(:CWE)-[:MAPS_TO_CAPEC {confidence: 0.80}]->(:CAPEC)`
- [ ] Quarterly CAPEC database updates (auto-detect new CAPEC versions)
- [ ] Validation: ensure no orphaned CAPECs (all reachable from CWEs)

**Priority**: HIGH
**Story Points**: 8
**TASKMASTER Reference**: TASK-2025-11-12-006
**Dependencies**: Story 1.2, CAPEC database import

**Test Cases**:
1. **Common CWE**: CWE-79 (XSS) → verify maps to CAPEC-63, CAPEC-18, etc.
2. **Rare CWE**: CWE-1234 (hypothetical) → verify graceful handling if no CAPEC
3. **CAPEC Update**: New CAPEC released, quarterly job runs → verify new CAPEC imported
4. **Orphan Detection**: Manually delete CWE edge → validation job detects orphaned CAPEC

---

### Story 1.4: CAPEC → ATT&CK Technique Mapping

**As a** Security Analyst
**I want** CAPECs mapped to MITRE ATT&CK Techniques
**So that** I can link attack patterns to real-world adversary behaviors

**Acceptance Criteria**:
- [ ] 70%+ CAPECs have at least one ATT&CK Technique mapping
- [ ] Uses ATT&CK STIX `external_references` with `source_name: "capec"`
- [ ] Neo4j relationship: `(:CAPEC)-[:MAPS_TO_TECHNIQUE {confidence: 0.75}]->(:Technique)`
- [ ] All 193 ATT&CK techniques reachable from at least one CAPEC
- [ ] Quarterly ATT&CK STIX updates (GitHub API monitors new versions)
- [ ] Change report generated: added/deprecated techniques

**Priority**: HIGH
**Story Points**: 8
**TASKMASTER Reference**: TASK-2025-11-12-007
**Dependencies**: Story 1.3, ATT&CK STIX import

**Test Cases**:
1. **Common Technique**: T1059 (Command Execution) → verify reachable from multiple CAPECs
2. **Multi-Tactic Technique**: T1566 (Phishing) → verify belongs to Initial Access + Execution
3. **ATT&CK Update**: New technique added → quarterly job imports, sends change notification
4. **Coverage Check**: Query all 193 techniques → verify all have incoming CAPEC edges

---

### Story 1.5: Technique → Tactic Hierarchical Mapping

**As a** Security Analyst
**I want** ATT&CK Techniques categorized by Tactic
**So that** I understand the adversary's strategic objective

**Acceptance Criteria**:
- [ ] 100% of 193 ATT&CK techniques mapped to 14 tactics
- [ ] Multi-tactic techniques supported (e.g., T1059 → Execution + Defense Evasion)
- [ ] Neo4j relationship: `(:Technique)-[:BELONGS_TO_TACTIC {confidence: 1.0}]->(:Tactic)`
- [ ] Tactic nodes: TA0001 (Initial Access) through TA0040 (Impact)
- [ ] UI displays tactic names (not just IDs): "Execution" not "TA0002"
- [ ] No orphaned techniques (all belong to at least one tactic)

**Priority**: HIGH
**Story Points**: 5
**TASKMASTER Reference**: TASK-2025-11-12-008
**Dependencies**: Story 1.4

**Test Cases**:
1. **Single Tactic**: T1003 (Credential Dumping) → verify only belongs to TA0006
2. **Multi-Tactic**: T1059 → verify belongs to both TA0002 and TA0005
3. **Tactic Coverage**: Count techniques per tactic → verify reasonable distribution
4. **UI Display**: Query technique → verify tactic name shown, not just ID

---

### Story 1.6: Full Semantic Chain Validation

**As a** Security Analyst
**I want** to verify complete chains from CVE to Tactic
**So that** I trust the data quality for risk scoring

**Acceptance Criteria**:
- [ ] 80%+ CVEs have at least one complete chain: CVE → CWE → CAPEC → Technique → Tactic
- [ ] Daily validation Cypher query runs at 03:00 UTC
- [ ] Metrics logged: total CVEs, CVEs with complete chains, completeness %
- [ ] Alert if completeness drops below 75%
- [ ] Dashboard widget shows chain completeness trend (last 30 days)
- [ ] Incomplete chains logged for manual review (e.g., CVE-2024-X has CWE but no CAPEC)

**Priority**: HIGH
**Story Points**: 5
**TASKMASTER Reference**: TASK-2025-11-12-009
**Dependencies**: Stories 1.2-1.5

**Test Cases**:
1. **Happy Path**: CVE-2024-1234 → verify returns full 5-node chain
2. **Incomplete Chain**: CVE with CWE but no CAPEC → verify flagged in logs
3. **Trend Dashboard**: Simulate 7 days of validation → verify dashboard shows trend line
4. **Alert Trigger**: Manually corrupt chains → drop completeness to 70% → verify alert fired

---

### Story 1.7: Job Persistence and Retry Logic

**As a** System Administrator
**I want** all long-running jobs to persist state and retry on failure
**So that** we achieve 100% job reliability

**Acceptance Criteria**:
- [ ] PostgreSQL `jobs`, `job_steps`, `job_logs` tables created
- [ ] All jobs (ingestion, updates, validation) logged to `jobs` table
- [ ] Failed jobs retry 3 times with exponential backoff (1s, 4s, 16s)
- [ ] After 3 failures, job marked as "failed", admin alerted
- [ ] Jobs dashboard shows: running, completed, failed (last 7 days)
- [ ] Manual retry button for failed jobs
- [ ] Zero lost jobs over 30-day period (success metric)

**Priority**: CRITICAL
**Story Points**: 8
**TASKMASTER Reference**: TASK-2025-11-12-002
**Dependencies**: PostgreSQL schema

**Test Cases**:
1. **Successful Job**: Run CVE ingestion → verify logged to `jobs` with status "completed"
2. **Transient Failure**: Simulate Neo4j timeout → verify retries 3 times → succeeds on retry 2
3. **Permanent Failure**: Simulate invalid API key → verify fails 3 times → marked "failed" → admin alerted
4. **Manual Retry**: Admin clicks retry button → verify job re-queued, attempts counter reset

---

## Section 3: Phase 2 User Stories (Months 4-6)
### Probabilistic Intelligence

---

### Story 2.1: Bayesian CVE Risk Scoring

**As a** Security Analyst
**I want** each CVE scored with a probability of leading to a specific tactic
**So that** I can prioritize remediation based on likelihood, not just CVSS

**Acceptance Criteria**:
- [ ] API endpoint `POST /api/v1/score_cve` returns probability score 0.0-1.0
- [ ] Formula: `P(Tactic | CVE) = Σ [P(Tactic|Tech) × P(Tech|CAPEC) × P(CAPEC|CWE) × P(CWE|CVE)]`
- [ ] Laplace smoothing (α=1.0) for zero-count edges
- [ ] Response includes overall probability + per-chain breakdowns
- [ ] Execution time < 2 seconds (p99)
- [ ] Accuracy ≥ 85% when validated against CISA KEV catalog
- [ ] Documented algorithm in `/docs/bayesian_scoring.md`

**Priority**: CRITICAL
**Story Points**: 13
**TASKMASTER Reference**: TASK-2025-11-12-010
**Dependencies**: Phase 1 complete (semantic chains)

**Test Cases**:
1. **Known Exploit**: CVE from CISA KEV → verify predicted tactic matches known exploit tactic
2. **Multiple Chains**: CVE-2024-1 with 3 chains to TA0002 → verify probability = sum of chain probs
3. **Zero Edge Count**: CVE with rare CWE → verify Laplace smoothing prevents probability = 0
4. **Performance**: Score 100 CVEs → verify p99 latency < 2s

---

### Story 2.2: Customer-Specific Risk Modifiers

**As a** CISO
**I want** risk scores adjusted for my industry sector and equipment
**So that** I get personalized threat intelligence relevant to my organization

**Acceptance Criteria**:
- [ ] Customer profile stored: industry sector (healthcare, finance, etc.), equipment types, geographic region
- [ ] Sector modifiers applied: healthcare 1.3x for ransomware (Impact) tactics, finance 1.5x for Credential Access
- [ ] Equipment modifiers: Windows Server 1.2x for certain techniques, Linux 0.8x for others
- [ ] Geographic modifiers: APT groups target specific regions
- [ ] UI displays: "Risk score: 0.78 (base: 0.65, your sector: 1.2x modifier)"
- [ ] Modifiers configurable by admin (PostgreSQL `customer_profiles` table)

**Priority**: HIGH
**Story Points**: 8
**TASKMASTER Reference**: TASK-2025-11-12-011
**Dependencies**: Story 2.1

**Test Cases**:
1. **Healthcare Customer**: Score CVE with ransomware tactic → verify 1.3x modifier applied
2. **Finance Customer**: Score CVE with credential access → verify 1.5x modifier
3. **No Modifier**: Score generic CVE for retail customer → verify modifier = 1.0
4. **UI Transparency**: View score details → verify shows base probability + modifier breakdown

---

### Story 2.3: Monte Carlo Confidence Intervals

**As a** CISO
**I want** risk scores to include 95% confidence intervals
**So that** I can communicate uncertainty to the board and auditors

**Acceptance Criteria**:
- [ ] 10,000 Monte Carlo samples per CVE score
- [ ] Each edge probability modeled as Beta distribution
- [ ] Wilson Score 95% CI calculated: `(p̂ + z²/2n ± z√[p̂(1-p̂)/n + z²/4n²]) / (1 + z²/n)`
- [ ] API response includes: `"confidence_interval": {"lower": 0.72, "upper": 0.84, "level": 0.95}`
- [ ] Execution time < 3 seconds for Monte Carlo simulation
- [ ] UI displays: "Risk: 0.78 (95% CI: 0.72-0.84)"
- [ ] Documented statistical methodology in `/docs/monte_carlo.md`

**Priority**: HIGH
**Story Points**: 13
**TASKMASTER Reference**: TASK-2025-11-12-012
**Dependencies**: Story 2.1

**Test Cases**:
1. **CI Width**: Score 10 CVEs → verify CI width reasonable (0.05-0.15 typical)
2. **Contains True Mean**: Run simulation 100 times → verify 95%+ CIs contain true probability
3. **Performance**: Monte Carlo with 10K samples → verify completes in < 3s
4. **UI Display**: View CVE score → verify CI shown as range with visual (error bars)

---

### Story 2.4: Batch CVE Scoring

**As a** SOC Analyst
**I want** to score 1,000+ CVEs in a single request
**So that** I can analyze monthly vulnerability scans efficiently

**Acceptance Criteria**:
- [ ] API endpoint `POST /api/v1/score_batch` accepts array of CVE IDs (max 1,000)
- [ ] Parallel processing: 8 worker threads
- [ ] Execution time: 1,000 CVEs in < 60 seconds
- [ ] Response includes: total, successful, failed counts + results array
- [ ] Partial success handling: if 5 CVEs fail, still return scores for other 995
- [ ] Rate limiting: 10 batch requests/minute per customer
- [ ] Progress indicator: WebSocket real-time updates "Processed 250/1000 (25%)"

**Priority**: HIGH
**Story Points**: 13
**TASKMASTER Reference**: TASK-2025-11-12-013
**Dependencies**: Story 2.1

**Test Cases**:
1. **Happy Path**: Submit 1,000 CVEs → verify all scored in < 60s
2. **Partial Failure**: Include 5 invalid CVE IDs → verify 995 scored, 5 errors returned
3. **Rate Limit**: Submit 11 batches in 1 minute → verify 11th rejected with 429 status
4. **Progress**: Submit 1,000 CVEs → verify WebSocket updates every 100 CVEs

---

### Story 2.5: Risk Score API Documentation

**As a** External Developer
**I want** comprehensive API documentation with examples
**So that** I can integrate AEON scoring into my security tools

**Acceptance Criteria**:
- [ ] OpenAPI 3.0 spec published at `/api/v1/openapi.json`
- [ ] Swagger UI available at `/docs`
- [ ] Code samples provided: Python, JavaScript, cURL
- [ ] Rate limits documented
- [ ] Error codes documented with resolution steps
- [ ] Authentication flow (Clerk JWT) explained with examples
- [ ] Changelog maintained for API version updates

**Priority**: MEDIUM
**Story Points**: 5
**TASKMASTER Reference**: TASK-2025-11-12-013
**Dependencies**: API endpoints implemented

**Test Cases**:
1. **OpenAPI Validation**: Run `swagger-cli validate openapi.json` → verify passes
2. **Code Samples**: Copy Python example → run → verify scores CVE successfully
3. **Error Documentation**: Trigger 404 error → verify error response matches documentation
4. **Swagger UI**: Navigate to `/docs` → verify interactive API explorer works

---

## Section 4: Phase 3 User Stories (Months 7-9)
### Graph Neural Networks

---

### Story 3.1: GNN Link Prediction Training

**As a** ML Engineer
**I want** to train a Graph Attention Network on our Neo4j data
**So that** we can predict missing CVE → CWE links when NVD data is incomplete

**Acceptance Criteria**:
- [ ] PyTorch Geometric model: 3-layer GAT with 128-dimensional embeddings
- [ ] Training set: 80% of 3.3M Neo4j edges, validation: 10%, test: 10%
- [ ] Hyperparameters: learning_rate=0.001, dropout=0.3, heads=4
- [ ] Training time: < 4 hours on NVIDIA V100 GPU
- [ ] Metrics: Precision ≥ 90%, Recall ≥ 85%, F1 ≥ 87% on test set
- [ ] Model saved to `/models/gnn_link_predictor_v1.pt`
- [ ] Training logs: loss per epoch, validation metrics every 10 epochs

**Priority**: HIGH
**Story Points**: 21
**TASKMASTER Reference**: TASK-2025-11-12-014
**Dependencies**: Neo4j with 3.3M edges, GPU access

**Test Cases**:
1. **Training Convergence**: Run 100 epochs → verify loss decreases monotonically
2. **Overfitting Check**: Compare train vs. validation loss → verify gap < 0.05
3. **Test Set Performance**: Evaluate on held-out 10% → verify Precision ≥ 90%
4. **Model Save/Load**: Save model → load in new session → verify predictions identical

---

### Story 3.2: Missing CWE Prediction

**As a** Security Analyst
**I want** the system to predict CWEs for CVEs when NVD provides no data
**So that** I can maintain high semantic chain completeness

**Acceptance Criteria**:
- [ ] API endpoint `POST /api/v1/predict_cwe` accepts CVE ID + description
- [ ] Returns top 5 predicted CWEs with confidence scores
- [ ] Only suggests if confidence > 70%
- [ ] Human-in-the-loop: predictions flagged for analyst review before Neo4j insertion
- [ ] UI workflow: "Predicted CWE: CWE-79 (confidence: 0.85) [Approve] [Reject]"
- [ ] Approved predictions logged to `predicted_cwe` table for accuracy tracking
- [ ] Monthly report: prediction accuracy vs. analyst corrections

**Priority**: MEDIUM
**Story Points**: 13
**TASKMASTER Reference**: TASK-2025-11-12-015
**Dependencies**: Story 3.1

**Test Cases**:
1. **High Confidence**: CVE with no NVD CWE → GNN predicts CWE-79 (confidence 0.92) → analyst approves → edge created
2. **Low Confidence**: GNN predicts CWE-123 (confidence 0.65) → not suggested (below 70% threshold)
3. **Analyst Override**: GNN suggests CWE-79, analyst rejects, manually assigns CWE-89 → logged for retraining
4. **Accuracy Tracking**: Monthly report shows 88% of predictions approved by analysts

---

### Story 3.3: Multi-Hop Graph Reasoning

**As a** Security Analyst
**I want** to query complex relationships across 10+ hops
**So that** I can answer questions like "Which CVEs lead to lateral movement via credential dumping?"

**Acceptance Criteria**:
- [ ] Cypher query library: 20+ common patterns (e.g., CVE → Technique → Mitigation)
- [ ] Natural language interface (future): "Find all CVEs that enable ransomware"
- [ ] Query performance: 10-hop queries complete in < 500ms
- [ ] Path ranking: results ordered by probability score (highest first)
- [ ] Export results: CSV, JSON, PDF report
- [ ] Saved queries: analysts can bookmark frequently used queries

**Priority**: MEDIUM
**Story Points**: 13
**TASKMASTER Reference**: TASK-2025-11-12-016
**Dependencies**: Phase 1 semantic chains, Story 2.1 scoring

**Test Cases**:
1. **Lateral Movement Query**: "CVEs → Technique:T1021 (Remote Services)" → verify returns 500+ CVEs ranked by probability
2. **Performance**: 10-hop query across 3.3M edges → verify < 500ms
3. **Export**: Run query → export to CSV → verify all fields included
4. **Saved Query**: Save query "Ransomware CVEs" → load later → verify executes correctly

---

## Section 5: Phase 4 User Stories (Months 10-12)
### Equipment Integration

---

### Story 4.1: Equipment Inventory Import

**As a** Security Analyst
**I want** to upload my organization's equipment list from CSV or CMDB
**So that** I can see which CVEs affect my specific assets

**Acceptance Criteria**:
- [ ] CSV upload: headers (hostname, software, version, location, criticality)
- [ ] CMDB API integration: ServiceNow, Jira Assets connectors
- [ ] CPE auto-matching: 95%+ success rate for common software (Windows, Apache, PostgreSQL)
- [ ] Fuzzy matching: "Microsoft Windows Server 2019" → "cpe:2.3:o:microsoft:windows_server_2019"
- [ ] Manual override: unmatched software shown in UI for manual CPE assignment
- [ ] Bulk import: 10,000 assets processed in < 15 minutes
- [ ] Import history: track uploads (timestamp, user, assets added/updated)

**Priority**: CRITICAL
**Story Points**: 13
**TASKMASTER Reference**: TASK-2025-11-12-017
**Dependencies**: NIST CPE dictionary, FuzzyWuzzy library

**Test Cases**:
1. **CSV Upload**: Upload 1,000 assets → verify 95%+ auto-matched
2. **Fuzzy Matching**: "Win10" → verify matched to "Windows 10" CPE
3. **Manual Override**: 50 unmatched assets → analyst assigns CPEs → verify saved
4. **CMDB Integration**: Connect to ServiceNow → import 5,000 assets → verify success

---

### Story 4.2: CVE-to-Equipment Mapping

**As a** Security Analyst
**I want** CVEs automatically linked to my equipment via CPE
**So that** I see which assets are vulnerable without manual correlation

**Acceptance Criteria**:
- [ ] Daily job: query NVD for CVE `cpe_match` configurations
- [ ] Match CVE CPEs against customer equipment CPEs
- [ ] Create Neo4j edges: `(:Equipment)-[:AFFECTED_BY]->(:CVE)`
- [ ] Multi-version matching: "Windows Server 2019 v1809-v21H2" affects all versions in range
- [ ] Update mappings when new CVEs published (real-time via NVD API webhook)
- [ ] Dashboard widget: "Your equipment has 1,247 associated CVEs (43 high risk)"

**Priority**: CRITICAL
**Story Points**: 13
**TASKMASTER Reference**: TASK-2025-11-12-018
**Dependencies**: Story 4.1, NVD CPE data

**Test Cases**:
1. **Exact Match**: Equipment "Apache 2.4.54" → CVE targets exactly 2.4.54 → verify edge created
2. **Version Range**: Equipment "Windows Server 2019 v1809" → CVE affects v1809-v21H2 → verify matched
3. **No Match**: Equipment "Custom Software 1.0" → no CVEs target it → verify zero edges
4. **Real-time Update**: New CVE published targeting "PostgreSQL 14.5" → verify edge created within 1 hour

---

### Story 4.3: Attack Surface Calculator

**As a** CISO
**I want** a comprehensive view of my organization's CVE exposure
**So that** I can report attack surface to the board with confidence

**Acceptance Criteria**:
- [ ] Calculate total CVEs per customer (all equipment combined)
- [ ] Filter by: location (internal/DMZ/external), criticality (critical/high/medium/low)
- [ ] Risk heatmap: equipment × tactic matrix (color-coded by probability × impact)
- [ ] Export to PDF: board-ready report with executive summary
- [ ] Execution time: < 10 seconds for 10,000 assets
- [ ] Trend analysis: compare attack surface week-over-week
- [ ] Top 10 vulnerable assets: ranked by (number of CVEs × average risk score)

**Priority**: HIGH
**Story Points**: 13
**TASKMASTER Reference**: TASK-2025-11-12-019
**Dependencies**: Story 4.2, Story 2.1 (scoring)

**Test Cases**:
1. **Full Calculation**: 10,000 assets → verify calculates in < 10s
2. **Heatmap**: Generate equipment × tactic heatmap → verify color gradient (green=low, red=high)
3. **Filtering**: Filter DMZ assets only → verify shows subset
4. **PDF Export**: Generate board report → verify includes executive summary + heatmap + top 10 assets

---

## Section 6: Phase 5 User Stories (Months 13-15)
### Actionable Outputs

---

### Story 5.1: Mitigation Recommendations

**As a** Security Analyst
**I want** automated mitigation suggestions for scored CVEs
**So that** I know how to reduce risk beyond just patching

**Acceptance Criteria**:
- [ ] Query ATT&CK `mitigations` for techniques in CVE attack chains
- [ ] Prioritize mitigations by technique probability (highest first)
- [ ] Include patching guidance: vendor advisory URL, patch ID, release date
- [ ] Compensating controls: if patch unavailable, suggest network segmentation, WAF rules, HIDS
- [ ] Mitigation coverage: ≥ 90% of scored CVEs have ≥1 mitigation
- [ ] UI: "CVE-2024-1234 → Mitigations: [M1038 Execution Prevention] [Patch KB5028244] [Compensating: WAF rule #42]"

**Priority**: CRITICAL
**Story Points**: 13
**TASKMASTER Reference**: TASK-2025-11-12-020
**Dependencies**: ATT&CK mitigations, vendor advisory database

**Test Cases**:
1. **Patching Available**: CVE with vendor patch → verify patch KB ID + URL shown
2. **No Patch**: CVE with no patch → verify compensating controls suggested
3. **Coverage**: Score 1,000 CVEs → verify ≥ 90% have mitigation suggestions
4. **Prioritization**: CVE with 3 mitigations → verify ordered by technique probability

---

### Story 5.2: SIEM/EDR Rule Generation

**As a** SOC Analyst
**I want** automated detection rules for CVE-associated techniques
**So that** I can deploy new threat detections without writing rules manually

**Acceptance Criteria**:
- [ ] Generate rules for: Splunk SPL, Microsoft Sentinel KQL, Sigma YAML
- [ ] Template variables: process names, file paths, registry keys from ATT&CK
- [ ] Test rules against MITRE ATT&CK Evals public logs
- [ ] Success rate: ≥ 80% rules deploy without syntax errors
- [ ] Rule testing: unit tests with sample logs before production deployment
- [ ] UI workflow: "CVE-2024-1 → [Generate Splunk Rule] → Preview → [Deploy to SIEM]"

**Priority**: HIGH
**Story Points**: 21
**TASKMASTER Reference**: TASK-2025-11-12-021
**Dependencies**: ATT&CK technique details, SIEM syntax libraries

**Test Cases**:
1. **Splunk Rule**: Generate SPL for T1059 (Command Execution) → deploy to Splunk → verify no syntax errors
2. **Sigma Rule**: Generate Sigma YAML → convert to QRadar query → verify valid
3. **False Positive Rate**: Deploy 10 rules → run on 1 week of logs → verify FP rate < 10%
4. **ATT&CK Evals**: Test rules against public ATT&CK Evals logs → verify detection rate ≥ 70%

---

### Story 5.3: Priority Action Planner

**As a** CISO
**I want** a ranked to-do list of remediation actions
**So that** my team focuses on highest-impact, lowest-effort fixes first

**Acceptance Criteria**:
- [ ] Ranking formula: (Probability × CVSS Impact) - Remediation Effort
- [ ] Effort estimator: patch (low), config change (low), software upgrade (medium), architecture change (high)
- [ ] Timeline: account for patch cycles (monthly), change windows (quarterly)
- [ ] Output: JSON array `[{rank: 1, cve_id, action, effort, deadline}, ...]`
- [ ] UI: Kanban board (To Do, In Progress, Done) with drag-drop
- [ ] Integration: export to Jira, ServiceNow as tickets
- [ ] Execution time: < 5 seconds for 500 actions

**Priority**: CRITICAL
**Story Points**: 13
**TASKMASTER Reference**: TASK-2025-11-12-022
**Dependencies**: Stories 5.1 (mitigations), 2.1 (scoring)

**Test Cases**:
1. **Ranking Logic**: 10 CVEs with varying probability/impact/effort → verify ranked correctly
2. **Timeline**: Patch cycle = monthly, change window = quarterly → verify deadlines respect cycles
3. **Jira Integration**: Export 50 actions to Jira → verify tickets created with correct priority
4. **Kanban Board**: Drag action from "To Do" to "In Progress" → verify status updated in database

---

### Story 5.4: McKenney's 8 Questions Answered

**As a** CISO
**I want** the system to answer all 8 strategic questions
**So that** I can have data-driven conversations with my board and auditors

**Acceptance Criteria**:
- [ ] Question 1 ("What is my cyber risk?") → Overall risk score: P(attack success) aggregated across all equipment
- [ ] Question 2 ("Compliance risk?") → NIST CSF, CIS Controls, ISO 27001 gap analysis
- [ ] Question 3 ("Techniques used against me?") → Top 20 techniques by probability for my equipment
- [ ] Question 4 ("Equipment at risk?") → Asset list ranked by total CVE exposure
- [ ] Question 5 ("Attack surface from equipment?") → CVE count + risk heatmap per asset
- [ ] Question 6 ("Mitigations for my equipment?") → Equipment-specific mitigation list
- [ ] Question 7 ("Detections for my equipment?") → SIEM rules tailored to my tech stack
- [ ] Question 8 ("What should I do next?") → Priority action planner (Story 5.3)
- [ ] All questions answerable with ≥ 95% confidence
- [ ] Dashboard: "McKenney's 8 Questions" page with one-click answers

**Priority**: CRITICAL
**Story Points**: 21
**TASKMASTER Reference**: PRD Section 1.3
**Dependencies**: All Phase 1-5 stories

**Test Cases**:
1. **Question 1**: Click "What is my cyber risk?" → verify returns overall risk score + confidence interval in < 5s
2. **Question 3**: Click "Techniques used against me?" → verify returns top 20 techniques ranked by probability
3. **Question 8**: Click "What should I do next?" → verify returns ranked action list (Story 5.3)
4. **Confidence Check**: Manually review all 8 answers → verify all have ≥ 95% confidence (data completeness, accuracy)

---

## Section 7: Cross-Phase Stories (Non-functional)

---

### Story 7.1: Clerk Authentication Integration

**As a** Platform User
**I want** to log in securely with my email and password
**So that** my data is protected and only I can access it

**Acceptance Criteria**:
- [ ] Clerk.com integration: Frontend (Next.js) + Backend (FastAPI)
- [ ] JWT token-based authentication (1-hour expiration, 30-day refresh)
- [ ] Multi-factor authentication: Optional (enforced for admin roles)
- [ ] **NEVER BREAK CLERK AUTH** (Constitutional mandate) → E2E tests on every deploy
- [ ] Login flow: < 3 seconds from submit to dashboard
- [ ] Password reset: Self-service email link
- [ ] Session management: Auto-logout after 12 hours of inactivity

**Priority**: CRITICAL
**Story Points**: 8
**Dependencies**: Clerk account, environment variables

**Test Cases**:
1. **Login**: Enter email/password → verify JWT token issued → redirected to dashboard in < 3s
2. **Invalid Credentials**: Enter wrong password → verify error message, no token issued
3. **Session Expiration**: Wait 1 hour → make API call → verify 401 error, prompt to re-login
4. **E2E Test**: Automated test runs on every deploy → verifies login flow works

---

### Story 7.2: Role-Based Access Control (RBAC)

**As a** System Administrator
**I want** to assign roles (Admin, Analyst, Read-Only) to users
**So that** I can control who can modify vs. view data

**Acceptance Criteria**:
- [ ] 3 roles: Admin (all permissions), Analyst (read + score + manage own equipment), Read-Only (view only)
- [ ] Clerk custom claims: Store role in JWT token
- [ ] API authorization: Middleware checks role before allowing writes
- [ ] UI: Hide/show buttons based on role (Analyst sees "Score CVE", Read-Only does not)
- [ ] Admin panel: Assign/revoke roles with audit trail
- [ ] Multi-tenant isolation: Users only see their customer_id data

**Priority**: HIGH
**Story Points**: 13
**Dependencies**: Story 7.1 (Clerk auth)

**Test Cases**:
1. **Admin**: Login as admin → verify can create users, assign roles
2. **Analyst**: Login as analyst → verify can score CVEs, cannot create users
3. **Read-Only**: Login as read-only → verify cannot score CVEs, button hidden
4. **Multi-Tenant**: User from Customer A → verify cannot see Customer B's data

---

### Story 7.3: Audit Logging

**As a** Compliance Officer
**I want** all API calls and user actions logged
**So that** I can audit who did what and when for compliance

**Acceptance Criteria**:
- [ ] PostgreSQL `audit_log` table: user_id, action, resource_type, resource_id, timestamp, IP, request_body, response_status
- [ ] All API calls logged automatically (FastAPI middleware)
- [ ] Retention: 1 year (configurable)
- [ ] UI: "Audit Log" page (admin-only) with filters (user, date range, action)
- [ ] Export: CSV, JSON for auditors
- [ ] Performance: Logging adds < 10ms to API response time

**Priority**: MEDIUM
**Story Points**: 5
**Dependencies**: PostgreSQL schema, RBAC

**Test Cases**:
1. **API Call**: Score CVE → verify logged to `audit_log` with user_id, timestamp, IP
2. **UI Search**: Filter logs by user "sarah@example.com" + date range → verify returns correct logs
3. **Export**: Export 1,000 audit logs to CSV → verify all fields included
4. **Performance**: Benchmark API with logging enabled → verify < 10ms overhead

---

### Story 7.4: System Health Monitoring

**As a** DevOps Engineer
**I want** real-time health checks for all services
**So that** I can detect and fix outages before users notice

**Acceptance Criteria**:
- [ ] Health check endpoints: `/api/health` (FastAPI), `/api/health` (Next.js)
- [ ] Checks: database connectivity (PostgreSQL, Neo4j, Qdrant), disk space, memory usage
- [ ] Prometheus metrics exported: `up`, `http_requests_total`, `http_request_duration_seconds`
- [ ] Grafana dashboards: API performance, database health, business KPIs
- [ ] PagerDuty alerts: API down (1 min), database connection failure (2 min), high error rate (> 10 errors/min)
- [ ] Uptime target: 99.5% (4.38 hours downtime/year)

**Priority**: HIGH
**Story Points**: 13
**Dependencies**: Prometheus, Grafana, PagerDuty integration

**Test Cases**:
1. **Health Check**: `curl /api/health` → verify returns `{"status": "ok", "database": "connected"}`
2. **Prometheus Metrics**: Query Prometheus → verify `http_requests_total` incrementing
3. **Grafana Dashboard**: View "API Performance" dashboard → verify request rate chart displays
4. **PagerDuty Alert**: Stop Neo4j container → verify PagerDuty alert fired within 2 minutes

---

### Story 7.5: Performance Testing and Optimization

**As a** DevOps Engineer
**I want** automated performance tests to catch regressions
**So that** we maintain p99 latency < 2s for all API endpoints

**Acceptance Criteria**:
- [ ] Locust load testing: Simulate 100 concurrent users
- [ ] Performance benchmarks: Run weekly, compare to baseline
- [ ] Regression detection: Alert if p99 latency increases > 20%
- [ ] Optimization: Database indexes, Redis caching for hot paths
- [ ] CI/CD integration: Performance tests run on staging before production deploy
- [ ] Benchmarking report: p50, p90, p99, p99.9 latencies + throughput (req/s)

**Priority**: MEDIUM
**Story Points**: 13
**Dependencies**: Locust, staging environment

**Test Cases**:
1. **Baseline**: Run Locust with 100 users → record p99 = 1.8s as baseline
2. **Regression**: Deploy code change → run Locust → p99 = 2.5s → verify alert fired
3. **Optimization**: Add Redis cache → run Locust → verify p99 reduced to 1.2s
4. **CI/CD**: Push to staging branch → verify performance tests run automatically

---

## Section 8: McKenney's 8 Questions Mapping

| Question | User Stories | Completion Criteria |
|----------|-------------|---------------------|
| **1. What is my cyber risk?** | 2.1 (Bayesian scoring), 2.2 (modifiers), 4.2 (equipment mapping), 4.3 (attack surface) | Overall risk score: P(attack success) aggregated across all equipment, with 95% CI |
| **2. What is my compliance risk?** | 5.4 (compliance gap analysis) | NIST CSF, CIS Controls, ISO 27001 gap reports |
| **3. What techniques do actors use against me?** | 1.4 (CAPEC→Technique), 2.1 (scoring), 4.2 (equipment CVEs) | Top 20 techniques by probability for customer's equipment |
| **4. What equipment is at risk?** | 4.1 (import), 4.2 (CVE mapping), 4.3 (surface calc) | Asset list ranked by total CVE exposure |
| **5. What is my attack surface from equipment?** | 4.3 (attack surface calculator) | CVE count + risk heatmap per asset |
| **6. What mitigations apply to my equipment?** | 5.1 (mitigation recommendations) | Equipment-specific mitigation list |
| **7. What detections apply to my equipment?** | 5.2 (SIEM rule generation) | SIEM rules tailored to customer's tech stack |
| **8. What should I do next?** | 5.3 (priority action planner) | Ranked remediation to-do list |

---

## Section 9: Story Point Estimates

**Fibonacci Scale**: 1, 2, 3, 5, 8, 13, 21

### Phase 1 (Semantic Foundation)
- 1.1 CVE Ingestion: **8 points**
- 1.2 CVE → CWE: **5 points**
- 1.3 CWE → CAPEC: **8 points**
- 1.4 CAPEC → Technique: **8 points**
- 1.5 Technique → Tactic: **5 points**
- 1.6 Full Chain Validation: **5 points**
- 1.7 Job Persistence: **8 points**
- **Phase 1 Total**: **47 points** (~12 weeks @ 4 points/week velocity)

### Phase 2 (Probabilistic Intelligence)
- 2.1 Bayesian Scoring: **13 points**
- 2.2 Customer Modifiers: **8 points**
- 2.3 Monte Carlo CI: **13 points**
- 2.4 Batch Scoring: **13 points**
- 2.5 API Documentation: **5 points**
- **Phase 2 Total**: **52 points** (~13 weeks)

### Phase 3 (GNN)
- 3.1 GNN Training: **21 points**
- 3.2 Missing CWE Prediction: **13 points**
- 3.3 Multi-Hop Reasoning: **13 points**
- **Phase 3 Total**: **47 points** (~12 weeks)

### Phase 4 (Equipment)
- 4.1 Equipment Import: **13 points**
- 4.2 CVE-Equipment Mapping: **13 points**
- 4.3 Attack Surface: **13 points**
- **Phase 4 Total**: **39 points** (~10 weeks)

### Phase 5 (Actionable Outputs)
- 5.1 Mitigations: **13 points**
- 5.2 SIEM Rules: **21 points**
- 5.3 Priority Planner: **13 points**
- 5.4 McKenney's 8 Questions: **21 points**
- **Phase 5 Total**: **68 points** (~17 weeks)

### Cross-Phase (Non-functional)
- 7.1 Clerk Auth: **8 points**
- 7.2 RBAC: **13 points**
- 7.3 Audit Logging: **5 points**
- 7.4 Monitoring: **13 points**
- 7.5 Performance: **13 points**
- **Cross-Phase Total**: **52 points** (spread across all phases)

**Grand Total**: **305 story points** (~76 weeks at 4 points/week velocity, ~18 months with 25% buffer)

---

## Section 10: Prioritization Matrix

### MoSCoW Prioritization

**Must Have (Critical for MVP)**:
- Story 1.1: CVE Ingestion
- Story 1.2-1.6: Semantic chain construction
- Story 1.7: Job Persistence
- Story 2.1: Bayesian Scoring
- Story 4.1-4.3: Equipment integration
- Story 5.1: Mitigations
- Story 5.3: Priority Planner
- Story 7.1: Clerk Auth

**Should Have (High Value)**:
- Story 2.2-2.3: Customer modifiers, CI
- Story 2.4: Batch Scoring
- Story 3.1-3.2: GNN link prediction
- Story 5.2: SIEM Rules
- Story 5.4: McKenney's 8 Questions
- Story 7.2: RBAC
- Story 7.4: Monitoring

**Could Have (Nice to Have)**:
- Story 2.5: API Documentation (can defer to post-launch)
- Story 3.3: Multi-Hop Reasoning (future enhancement)
- Story 7.3: Audit Logging (compliance requirement, not MVP blocker)
- Story 7.5: Performance Testing (continuous improvement)

**Won't Have (Out of Scope for First 15 Months)**:
- Threat actor attribution
- Real-time exploit kit monitoring
- Dark web intelligence
- Automated pentesting

---

**Document Control**:
- **Approved By**: [Pending product review]
- **Review Cycle**: Monthly during development
- **Next Review**: 2025-12-12
- **Change Log**:
  - v1.0.0 (2025-11-12): Initial user stories with acceptance criteria

**END OF USER STORIES DOCUMENT**
