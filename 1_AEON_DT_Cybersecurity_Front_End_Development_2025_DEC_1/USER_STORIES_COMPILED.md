# AEON Digital Twin: Complete User Stories for Frontend Development

**File**: USER_STORIES_COMPILED.md
**Created**: 2025-12-02
**Purpose**: Comprehensive compilation of all user stories from wiki for frontend development
**Status**: ACTIVE - COMPLETE COMPILATION
**Sources**:
- `/04_USER_STORIES/01_USER_STORIES.md`
- `/04_USER_STORIES/E27_USER_STORIES.md`

---

## Table of Contents

1. [User Personas](#user-personas)
2. [High Priority Stories (MVP Must-Have)](#high-priority-mvp)
3. [Medium Priority Stories (Should-Have)](#medium-priority)
4. [Low Priority Stories (Nice-to-Have)](#low-priority)
5. [Enhancement 27: Psychohistory Stories](#enhancement-27-psychohistory)
6. [API Mapping Reference](#api-mapping)
7. [Data Requirements Reference](#data-requirements)

---

## User Personas

### Persona 1: Senior Security Analyst (Sarah Chen)
**Profile**:
- **Role**: Threat Intelligence Analyst
- **Organization**: Fortune 500 Financial Services
- **Experience**: 8+ years in cybersecurity
- **Technical Skills**: High (Python, SIEM, threat modeling)

**Pain Points**:
- Manual CVE-to-ATT&CK mapping consumes 14+ hours/week
- Cannot quantify risk with confidence intervals
- SIEM alert fatigue (10,000+ alerts/day)
- No equipment-specific threat intelligence

**Goals**:
- Automate semantic chain mapping (CVE → Tactic)
- Get probabilistic risk scores for all CVEs
- Prioritize remediation with data-driven confidence
- Generate SIEM rules automatically

---

### Persona 2: CISO/Security Director (Michael Rodriguez)
**Profile**:
- **Role**: Chief Information Security Officer
- **Organization**: Large Healthcare System
- **Experience**: 15+ years (technical + leadership)
- **Technical Skills**: Medium (high-level architecture, vendor evaluation)

**Pain Points**:
- Board asks "What's our cyber risk?" → cannot quantify
- Compliance audits require proof of NIST CSF coverage
- $5M security budget needs ROI justification
- No way to compare vulnerability severity across vendors

**Goals**:
- Executive dashboard with risk trending
- Automated compliance gap analysis (NIST, ISO, CIS)
- Board-ready reports with confidence intervals
- ROI metrics: cost of vulnerabilities vs. mitigation spend

---

### Persona 3: SOC Analyst (Alex Thompson)
**Profile**:
- **Role**: Security Operations Center Analyst
- **Organization**: Managed Security Service Provider (MSSP)
- **Experience**: 3 years in SOC operations
- **Technical Skills**: Medium (SIEM queries, alert triage)

**Pain Points**:
- Monitors 50+ customers, cannot analyze every CVE manually
- Prioritizes 500+ vulnerabilities/month without risk scores
- Customers ask "Should I patch CVE-X?" → no data-driven answer
- Spends 60% of time on false positive alerts

**Goals**:
- Bulk CVE analysis (process 1,000+ CVEs/hour)
- Multi-tenant equipment risk mapping
- Customer-facing risk reports (non-technical language)
- Automated alert tuning based on actual risk

---

## HIGH PRIORITY (MVP Must-Have)

### Story 1.1: Automated CVE Ingestion
**As a** Security Analyst
**I want** the system to automatically import CVEs from NVD daily
**So that** I always have the latest vulnerability data without manual effort

**Priority**: CRITICAL
**Story Points**: 8
**Persona**: Sarah Chen (Security Analyst)
**Phase**: Phase 1 (Months 1-3)

**APIs Required**:
- `POST /api/v1/cve/ingest` - Trigger manual ingestion
- `GET /api/v1/cve/ingest/status` - Check ingestion job status
- `GET /api/v1/cve/ingest/logs` - View ingestion logs

**Data Required**:
- CVE nodes with properties: cve_id, description, cvss_score, published_date
- CWE nodes with relationships: `(:CVE)-[:HAS_CWE]->(:CWE)`
- Job tracking: jobs table with status, timestamps, metrics

**Acceptance Criteria**:
- [ ] System runs at 02:00 UTC daily without manual intervention
- [ ] Imports all CVEs published in last 24 hours (≥ 95% completeness)
- [ ] Updates existing CVE records when NVD modifies CVSS or CWE
- [ ] Logs ingestion metrics: CVEs imported, errors, execution time
- [ ] Job persistence: 100% reliability (zero lost jobs after 3 retries)
- [ ] Alert to admin if ingestion fails 3 times consecutively
- [ ] Execution time < 15 minutes for typical daily load (500 CVEs)

**UI Components**:
- [ ] Dashboard widget showing last ingestion status
- [ ] Ingestion history table with date, CVE count, duration, status
- [ ] Manual trigger button for on-demand ingestion
- [ ] Real-time progress indicator during ingestion
- [ ] Alert notification banner for failed ingestions
- [ ] Logs viewer with filtering and search

---

### Story 1.2: CVE → CWE Semantic Mapping
**As a** Security Analyst
**I want** every CVE mapped to its Common Weakness Enumeration (CWE)
**So that** I can understand the root cause vulnerability class

**Priority**: CRITICAL
**Story Points**: 5
**Persona**: Sarah Chen (Security Analyst)
**Phase**: Phase 1 (Months 1-3)

**APIs Required**:
- `GET /api/v1/cve/{cve_id}/cwe` - Get CWE mappings for a CVE
- `GET /api/v1/cwe/{cwe_id}` - Get CWE details
- `GET /api/v1/validation/cwe-completeness` - Check mapping completeness

**Data Required**:
- CWE nodes: cwe_id, name, description
- Relationships: `(:CVE)-[:HAS_CWE {confidence: float}]->(:CWE)`
- Default CWE: `CWE-NVD-noinfo` for unmapped CVEs

**Acceptance Criteria**:
- [ ] 95%+ CVEs have at least one CWE mapping (from NVD data)
- [ ] Multiple CWEs per CVE supported
- [ ] Default to `CWE-NVD-noinfo` when NVD provides no CWE
- [ ] Confidence score stored: 0.95 for NVD-provided, < 0.80 for NER v9 extraction
- [ ] Daily validation job: check CWE mapping completeness, alert if < 90%

**UI Components**:
- [ ] CVE detail page showing all CWE mappings with confidence scores
- [ ] CWE badge with color coding by confidence (green: >0.9, yellow: 0.8-0.9, red: <0.8)
- [ ] Filterable CVE table by CWE type
- [ ] Dashboard widget showing CWE mapping completeness percentage
- [ ] Alert banner when completeness drops below 90%

---

### Story 2.1: Bayesian CVE Risk Scoring
**As a** Security Analyst
**I want** each CVE scored with a probability of leading to a specific tactic
**So that** I can prioritize remediation based on likelihood, not just CVSS

**Priority**: CRITICAL
**Story Points**: 13
**Persona**: Sarah Chen (Security Analyst), Michael Rodriguez (CISO)
**Phase**: Phase 2 (Months 4-6)

**APIs Required**:
- `POST /api/v1/score_cve` - Score single CVE
- `GET /api/v1/cve/{cve_id}/score` - Get cached score
- `POST /api/v1/score_batch` - Score multiple CVEs

**Data Required**:
- Complete semantic chains: CVE → CWE → CAPEC → Technique → Tactic
- Edge probabilities for Bayesian calculation
- Historical exploit data for validation

**Acceptance Criteria**:
- [ ] API endpoint returns probability score 0.0-1.0
- [ ] Formula: `P(Tactic | CVE) = Σ [P(Tactic|Tech) × P(Tech|CAPEC) × P(CAPEC|CWE) × P(CWE|CVE)]`
- [ ] Laplace smoothing (α=1.0) for zero-count edges
- [ ] Response includes overall probability + per-chain breakdowns
- [ ] Execution time < 2 seconds (p99)
- [ ] Accuracy ≥ 85% when validated against CISA KEV catalog

**UI Components**:
- [ ] Risk score display with probability (0.0-1.0) and color coding
- [ ] Expandable detail showing all chains contributing to score
- [ ] Visual chain diagram: CVE → CWE → CAPEC → Technique → Tactic
- [ ] Comparison to CVSS score side-by-side
- [ ] Filter CVEs by risk score range (high: >0.8, medium: 0.5-0.8, low: <0.5)
- [ ] Bulk score button for selected CVEs
- [ ] Loading indicator during score calculation

---

### Story 4.1: Equipment Inventory Import
**As a** Security Analyst
**I want** to upload my organization's equipment list from CSV or CMDB
**So that** I can see which CVEs affect my specific assets

**Priority**: CRITICAL
**Story Points**: 13
**Persona**: Sarah Chen (Security Analyst)
**Phase**: Phase 4 (Months 10-12)

**APIs Required**:
- `POST /api/v1/equipment/import/csv` - Upload CSV file
- `POST /api/v1/equipment/import/cmdb` - Connect to CMDB API
- `GET /api/v1/equipment/import/status` - Check import progress
- `POST /api/v1/equipment/cpe-match` - Manual CPE assignment

**Data Required**:
- Equipment nodes: hostname, software, version, location, criticality, cpe
- CPE dictionary for auto-matching
- Import history: timestamp, user, assets added/updated

**Acceptance Criteria**:
- [ ] CSV upload: headers (hostname, software, version, location, criticality)
- [ ] CMDB API integration: ServiceNow, Jira Assets connectors
- [ ] CPE auto-matching: 95%+ success rate for common software
- [ ] Fuzzy matching: "Microsoft Windows Server 2019" → "cpe:2.3:o:microsoft:windows_server_2019"
- [ ] Manual override: unmatched software shown in UI for manual CPE assignment
- [ ] Bulk import: 10,000 assets processed in < 15 minutes

**UI Components**:
- [ ] CSV upload form with drag-drop and file validation
- [ ] CMDB connection wizard with credential entry
- [ ] Import progress bar with real-time updates
- [ ] Unmatched assets table with manual CPE assignment dropdown
- [ ] Equipment inventory table with search, filter, and sort
- [ ] Import history table showing past uploads
- [ ] Success/error summary after import completion

---

### Story 4.2: CVE-to-Equipment Mapping
**As a** Security Analyst
**I want** CVEs automatically linked to my equipment via CPE
**So that** I see which assets are vulnerable without manual correlation

**Priority**: CRITICAL
**Story Points**: 13
**Persona**: Sarah Chen (Security Analyst)
**Phase**: Phase 4 (Months 10-12)

**APIs Required**:
- `GET /api/v1/equipment/{equipment_id}/cves` - Get CVEs for equipment
- `GET /api/v1/cve/{cve_id}/equipment` - Get affected equipment
- `GET /api/v1/equipment/summary` - Dashboard statistics

**Data Required**:
- Relationships: `(:Equipment)-[:AFFECTED_BY]->(:CVE)`
- CPE matching data from NVD
- Version range matching logic

**Acceptance Criteria**:
- [ ] Daily job: query NVD for CVE `cpe_match` configurations
- [ ] Match CVE CPEs against customer equipment CPEs
- [ ] Create Neo4j edges: `(:Equipment)-[:AFFECTED_BY]->(:CVE)`
- [ ] Multi-version matching: "Windows Server 2019 v1809-v21H2" affects all versions in range
- [ ] Update mappings when new CVEs published (real-time via NVD API webhook)
- [ ] Dashboard widget: "Your equipment has 1,247 associated CVEs (43 high risk)"

**UI Components**:
- [ ] Equipment detail page showing all associated CVEs
- [ ] CVE detail page showing all affected equipment
- [ ] Dashboard widget with total equipment and CVE counts
- [ ] Risk heatmap: equipment vs CVE severity
- [ ] Filter equipment by vulnerability count or risk level
- [ ] Export affected equipment list to CSV

---

### Story 5.1: Mitigation Recommendations
**As a** Security Analyst
**I want** automated mitigation suggestions for scored CVEs
**So that** I know how to reduce risk beyond just patching

**Priority**: CRITICAL
**Story Points**: 13
**Persona**: Sarah Chen (Security Analyst)
**Phase**: Phase 5 (Months 13-15)

**APIs Required**:
- `GET /api/v1/cve/{cve_id}/mitigations` - Get mitigation recommendations
- `GET /api/v1/mitigation/{mitigation_id}` - Get mitigation details
- `GET /api/v1/cve/{cve_id}/patch-info` - Get patching guidance

**Data Required**:
- ATT&CK mitigation nodes and relationships
- Vendor advisory database
- Compensating controls library

**Acceptance Criteria**:
- [ ] Query ATT&CK `mitigations` for techniques in CVE attack chains
- [ ] Prioritize mitigations by technique probability (highest first)
- [ ] Include patching guidance: vendor advisory URL, patch ID, release date
- [ ] Compensating controls: if patch unavailable, suggest network segmentation, WAF rules, HIDS
- [ ] Mitigation coverage: ≥ 90% of scored CVEs have ≥1 mitigation

**UI Components**:
- [ ] Mitigation recommendations panel on CVE detail page
- [ ] Prioritized list of mitigations with effectiveness scores
- [ ] Patch information card with download link and release date
- [ ] Compensating controls section when patch unavailable
- [ ] Implementation difficulty indicator (easy/medium/hard)
- [ ] Export mitigation plan to PDF

---

### Story 5.3: Priority Action Planner
**As a** CISO
**I want** a ranked to-do list of remediation actions
**So that** my team focuses on highest-impact, lowest-effort fixes first

**Priority**: CRITICAL
**Story Points**: 13
**Persona**: Michael Rodriguez (CISO)
**Phase**: Phase 5 (Months 13-15)

**APIs Required**:
- `GET /api/v1/actions/prioritized` - Get ranked action list
- `POST /api/v1/actions/update-status` - Update action status
- `POST /api/v1/actions/export` - Export to Jira/ServiceNow

**Data Required**:
- CVE risk scores and mitigation data
- Effort estimates: patch (low), config change (low), upgrade (medium), architecture (high)
- Patch cycles and change windows

**Acceptance Criteria**:
- [ ] Ranking formula: (Probability × CVSS Impact) - Remediation Effort
- [ ] Effort estimator based on action type
- [ ] Timeline accounting for patch cycles and change windows
- [ ] Output: JSON array with rank, cve_id, action, effort, deadline
- [ ] UI: Kanban board (To Do, In Progress, Done) with drag-drop
- [ ] Integration: export to Jira, ServiceNow as tickets
- [ ] Execution time: < 5 seconds for 500 actions

**UI Components**:
- [ ] Kanban board with three columns: To Do, In Progress, Done
- [ ] Drag-drop cards between columns
- [ ] Card showing: CVE ID, risk score, action, effort, deadline
- [ ] Filter by priority, deadline, or effort level
- [ ] Bulk export selected actions to ticketing system
- [ ] Timeline view showing upcoming patch cycles
- [ ] Export button for CSV or PDF report

---

### Story 7.1: Clerk Authentication Integration
**As a** Platform User
**I want** to log in securely with my email and password
**So that** my data is protected and only I can access it

**Priority**: CRITICAL
**Story Points**: 8
**Persona**: All users
**Phase**: Cross-Phase

**APIs Required**:
- Clerk.com authentication endpoints (external)
- `GET /api/v1/auth/verify` - Verify JWT token
- `POST /api/v1/auth/refresh` - Refresh expired token

**Data Required**:
- User authentication state via Clerk
- JWT tokens with 1-hour expiration, 30-day refresh
- Session management data

**Acceptance Criteria**:
- [ ] Clerk.com integration: Frontend (Next.js) + Backend (FastAPI)
- [ ] JWT token-based authentication (1-hour expiration, 30-day refresh)
- [ ] Multi-factor authentication: Optional (enforced for admin roles)
- [ ] **NEVER BREAK CLERK AUTH** → E2E tests on every deploy
- [ ] Login flow: < 3 seconds from submit to dashboard
- [ ] Password reset: Self-service email link
- [ ] Session management: Auto-logout after 12 hours of inactivity

**UI Components**:
- [ ] Login page with email and password fields
- [ ] "Forgot password" link
- [ ] MFA setup page (optional)
- [ ] Session timeout warning modal (5 minutes before expiry)
- [ ] Auto-redirect to login on expired session
- [ ] Loading spinner during authentication
- [ ] Error messages for invalid credentials

---

## MEDIUM PRIORITY (Should-Have)

### Story 2.2: Customer-Specific Risk Modifiers
**As a** CISO
**I want** risk scores adjusted for my industry sector and equipment
**So that** I get personalized threat intelligence relevant to my organization

**Priority**: HIGH
**Story Points**: 8
**Persona**: Michael Rodriguez (CISO)
**Phase**: Phase 2 (Months 4-6)

**APIs Required**:
- `GET /api/v1/customer/{customer_id}/profile` - Get customer profile
- `PUT /api/v1/customer/{customer_id}/profile` - Update profile
- `GET /api/v1/cve/{cve_id}/score?customer_id={id}` - Get customer-adjusted score

**Data Required**:
- Customer profiles: industry sector, equipment types, geographic region
- Sector modifiers: healthcare (1.3× ransomware), finance (1.5× credential access)
- Equipment modifiers: Windows Server (1.2×), Linux (0.8×)

**Acceptance Criteria**:
- [ ] Customer profile stored with sector, equipment, region
- [ ] Sector modifiers applied automatically
- [ ] Equipment modifiers applied based on inventory
- [ ] Geographic modifiers for APT targeting
- [ ] UI displays: "Risk score: 0.78 (base: 0.65, your sector: 1.2× modifier)"
- [ ] Modifiers configurable by admin

**UI Components**:
- [ ] Customer profile settings page
- [ ] Industry sector dropdown selector
- [ ] Equipment type multi-select
- [ ] Geographic region selector
- [ ] Risk score display showing base score and modifier breakdown
- [ ] Admin panel for configuring modifier values
- [ ] Visual indicator when modifiers are applied

---

### Story 2.3: Monte Carlo Confidence Intervals
**As a** CISO
**I want** risk scores to include 95% confidence intervals
**So that** I can communicate uncertainty to the board and auditors

**Priority**: HIGH
**Story Points**: 13
**Persona**: Michael Rodriguez (CISO)
**Phase**: Phase 2 (Months 4-6)

**APIs Required**:
- `GET /api/v1/cve/{cve_id}/score-with-ci` - Get score with confidence interval
- `POST /api/v1/monte-carlo/simulate` - Run Monte Carlo simulation

**Data Required**:
- Beta distributions for edge probabilities
- 10,000 Monte Carlo samples per CVE
- Wilson Score 95% CI calculation

**Acceptance Criteria**:
- [ ] 10,000 Monte Carlo samples per CVE score
- [ ] Each edge probability modeled as Beta distribution
- [ ] Wilson Score 95% CI calculated
- [ ] API response includes: `"confidence_interval": {"lower": 0.72, "upper": 0.84, "level": 0.95}`
- [ ] Execution time < 3 seconds for Monte Carlo simulation
- [ ] UI displays: "Risk: 0.78 (95% CI: 0.72-0.84)"

**UI Components**:
- [ ] Risk score with confidence interval range display
- [ ] Visual error bars or range indicator
- [ ] Tooltip explaining confidence interval meaning
- [ ] Toggle to show/hide confidence intervals
- [ ] Dashboard widget comparing risk scores with CI ranges
- [ ] Export reports including CI data

---

### Story 2.4: Batch CVE Scoring
**As a** SOC Analyst
**I want** to score 1,000+ CVEs in a single request
**So that** I can analyze monthly vulnerability scans efficiently

**Priority**: HIGH
**Story Points**: 13
**Persona**: Alex Thompson (SOC Analyst)
**Phase**: Phase 2 (Months 4-6)

**APIs Required**:
- `POST /api/v1/score_batch` - Score multiple CVEs (max 1,000)
- `GET /api/v1/score_batch/{batch_id}/status` - Check batch status
- WebSocket endpoint for real-time progress

**Data Required**:
- CVE IDs array for batch processing
- Parallel processing workers (8 threads)
- Progress tracking data

**Acceptance Criteria**:
- [ ] API endpoint accepts array of CVE IDs (max 1,000)
- [ ] Parallel processing: 8 worker threads
- [ ] Execution time: 1,000 CVEs in < 60 seconds
- [ ] Response includes: total, successful, failed counts + results array
- [ ] Partial success handling: if 5 CVEs fail, still return scores for other 995
- [ ] Rate limiting: 10 batch requests/minute per customer
- [ ] Progress indicator: WebSocket real-time updates "Processed 250/1000 (25%)"

**UI Components**:
- [ ] Bulk score interface with CVE ID input (paste or upload)
- [ ] Real-time progress bar with percentage and count
- [ ] Results table showing all scored CVEs
- [ ] Error summary panel for failed CVEs
- [ ] Export results to CSV
- [ ] Historical batch job list
- [ ] Cancel button for running batch jobs

---

### Story 3.1: GNN Link Prediction Training
**As a** ML Engineer
**I want** to train a Graph Attention Network on our Neo4j data
**So that** we can predict missing CVE → CWE links when NVD data is incomplete

**Priority**: HIGH
**Story Points**: 21
**Persona**: Technical/Backend Team
**Phase**: Phase 3 (Months 7-9)

**APIs Required**:
- `POST /api/v1/gnn/train` - Start training job
- `GET /api/v1/gnn/training/{job_id}/status` - Check training progress
- `GET /api/v1/gnn/model/{model_id}/metrics` - Get model performance

**Data Required**:
- 3.3M Neo4j edges for training
- 80/10/10 train/validation/test split
- PyTorch Geometric model: 3-layer GAT, 128-dim embeddings

**Acceptance Criteria**:
- [ ] PyTorch Geometric model: 3-layer GAT with 128-dimensional embeddings
- [ ] Training set: 80% of 3.3M edges, validation: 10%, test: 10%
- [ ] Hyperparameters: learning_rate=0.001, dropout=0.3, heads=4
- [ ] Training time: < 4 hours on NVIDIA V100 GPU
- [ ] Metrics: Precision ≥ 90%, Recall ≥ 85%, F1 ≥ 87% on test set
- [ ] Model saved to `/models/gnn_link_predictor_v1.pt`

**UI Components**:
- [ ] Training dashboard with loss/accuracy curves
- [ ] Hyperparameter configuration form
- [ ] Training progress bar with epoch count
- [ ] Model performance metrics display
- [ ] Historical training runs table
- [ ] Model comparison charts
- [ ] Export trained model button

---

### Story 5.2: SIEM/EDR Rule Generation
**As a** SOC Analyst
**I want** automated detection rules for CVE-associated techniques
**So that** I can deploy new threat detections without writing rules manually

**Priority**: HIGH
**Story Points**: 21
**Persona**: Alex Thompson (SOC Analyst)
**Phase**: Phase 5 (Months 13-15)

**APIs Required**:
- `POST /api/v1/rules/generate` - Generate rule for CVE
- `GET /api/v1/rules/{rule_id}` - Get rule details
- `POST /api/v1/rules/deploy` - Deploy rule to SIEM

**Data Required**:
- ATT&CK technique details (process names, file paths, registry keys)
- SIEM syntax templates (Splunk SPL, Sentinel KQL, Sigma YAML)
- Test logs for validation

**Acceptance Criteria**:
- [ ] Generate rules for: Splunk SPL, Microsoft Sentinel KQL, Sigma YAML
- [ ] Template variables: process names, file paths, registry keys from ATT&CK
- [ ] Test rules against MITRE ATT&CK Evals public logs
- [ ] Success rate: ≥ 80% rules deploy without syntax errors
- [ ] Rule testing: unit tests with sample logs before production deployment

**UI Components**:
- [ ] Rule generation form with CVE and SIEM type selection
- [ ] Rule preview with syntax highlighting
- [ ] Edit rule before deployment
- [ ] Test rule against sample logs
- [ ] Deploy button with confirmation
- [ ] Rule library with search and filter
- [ ] Deployment status indicator

---

### Story 7.2: Role-Based Access Control (RBAC)
**As a** System Administrator
**I want** to assign roles (Admin, Analyst, Read-Only) to users
**So that** I can control who can modify vs. view data

**Priority**: HIGH
**Story Points**: 13
**Persona**: System Administrator
**Phase**: Cross-Phase

**APIs Required**:
- `GET /api/v1/users` - List users
- `PUT /api/v1/users/{user_id}/role` - Assign role
- `GET /api/v1/permissions` - Get role permissions

**Data Required**:
- User roles: Admin, Analyst, Read-Only
- Clerk custom claims for JWT tokens
- Multi-tenant customer_id isolation

**Acceptance Criteria**:
- [ ] 3 roles: Admin (all permissions), Analyst (read + score + manage own equipment), Read-Only (view only)
- [ ] Clerk custom claims: Store role in JWT token
- [ ] API authorization: Middleware checks role before allowing writes
- [ ] UI: Hide/show buttons based on role
- [ ] Admin panel: Assign/revoke roles with audit trail
- [ ] Multi-tenant isolation: Users only see their customer_id data

**UI Components**:
- [ ] User management page (admin only)
- [ ] Role assignment dropdown
- [ ] Permission matrix display
- [ ] Audit log of role changes
- [ ] UI elements conditionally rendered by role
- [ ] Access denied page for unauthorized actions

---

### Story 7.4: System Health Monitoring
**As a** DevOps Engineer
**I want** real-time health checks for all services
**So that** I can detect and fix outages before users notice

**Priority**: HIGH
**Story Points**: 13
**Persona**: DevOps Engineer
**Phase**: Cross-Phase

**APIs Required**:
- `GET /api/health` - Health check endpoint
- `GET /api/metrics` - Prometheus metrics
- PagerDuty webhook integration

**Data Required**:
- Database connectivity status (PostgreSQL, Neo4j, Qdrant)
- System metrics: disk space, memory usage
- Prometheus metrics: up, http_requests_total, http_request_duration_seconds

**Acceptance Criteria**:
- [ ] Health check endpoints: `/api/health`
- [ ] Checks: database connectivity, disk space, memory usage
- [ ] Prometheus metrics exported
- [ ] Grafana dashboards: API performance, database health, business KPIs
- [ ] PagerDuty alerts: API down (1 min), database failure (2 min), high error rate (>10 errors/min)
- [ ] Uptime target: 99.5%

**UI Components**:
- [ ] System health dashboard
- [ ] Service status indicators (green/yellow/red)
- [ ] Real-time metrics charts
- [ ] Alert history table
- [ ] Database connection status
- [ ] API response time charts
- [ ] Disk and memory usage gauges

---

## LOW PRIORITY (Nice-to-Have)

### Story 2.5: Risk Score API Documentation
**As a** External Developer
**I want** comprehensive API documentation with examples
**So that** I can integrate AEON scoring into my security tools

**Priority**: MEDIUM
**Story Points**: 5
**Persona**: External Developers
**Phase**: Phase 2 (Months 4-6)

**APIs Required**:
- `GET /api/v1/openapi.json` - OpenAPI specification
- Swagger UI at `/docs`

**Data Required**:
- OpenAPI 3.0 specification
- Code samples: Python, JavaScript, cURL
- Authentication flow documentation

**Acceptance Criteria**:
- [ ] OpenAPI 3.0 spec published at `/api/v1/openapi.json`
- [ ] Swagger UI available at `/docs`
- [ ] Code samples provided: Python, JavaScript, cURL
- [ ] Rate limits documented
- [ ] Error codes documented with resolution steps
- [ ] Authentication flow (Clerk JWT) explained with examples
- [ ] Changelog maintained for API version updates

**UI Components**:
- [ ] Interactive Swagger UI
- [ ] Code sample viewer with copy button
- [ ] Authentication guide page
- [ ] Rate limit display
- [ ] Error code reference table
- [ ] API changelog page

---

### Story 3.2: Missing CWE Prediction
**As a** Security Analyst
**I want** the system to predict CWEs for CVEs when NVD provides no data
**So that** I can maintain high semantic chain completeness

**Priority**: MEDIUM
**Story Points**: 13
**Persona**: Sarah Chen (Security Analyst)
**Phase**: Phase 3 (Months 7-9)

**APIs Required**:
- `POST /api/v1/predict_cwe` - Predict CWE for CVE
- `PUT /api/v1/cve/{cve_id}/cwe/approve` - Approve predicted CWE
- `PUT /api/v1/cve/{cve_id}/cwe/reject` - Reject prediction

**Data Required**:
- GNN model predictions
- Confidence scores (>70% threshold)
- Analyst approval/rejection tracking

**Acceptance Criteria**:
- [ ] API endpoint accepts CVE ID + description
- [ ] Returns top 5 predicted CWEs with confidence scores
- [ ] Only suggests if confidence > 70%
- [ ] Human-in-the-loop: predictions flagged for analyst review before Neo4j insertion
- [ ] UI workflow: "Predicted CWE: CWE-79 (confidence: 0.85) [Approve] [Reject]"
- [ ] Approved predictions logged for accuracy tracking
- [ ] Monthly report: prediction accuracy vs. analyst corrections

**UI Components**:
- [ ] Prediction review queue page
- [ ] CVE detail with predicted CWEs
- [ ] Confidence score display
- [ ] Approve/Reject buttons
- [ ] Analyst feedback form
- [ ] Prediction accuracy dashboard
- [ ] Monthly accuracy report

---

### Story 3.3: Multi-Hop Graph Reasoning
**As a** Security Analyst
**I want** to query complex relationships across 10+ hops
**So that** I can answer questions like "Which CVEs lead to lateral movement via credential dumping?"

**Priority**: MEDIUM
**Story Points**: 13
**Persona**: Sarah Chen (Security Analyst)
**Phase**: Phase 3 (Months 7-9)

**APIs Required**:
- `POST /api/v1/graph/query` - Execute graph query
- `GET /api/v1/graph/saved-queries` - List saved queries
- `POST /api/v1/graph/query/save` - Save query

**Data Required**:
- Neo4j graph with 3.3M edges
- Cypher query library (20+ common patterns)
- Path ranking by probability score

**Acceptance Criteria**:
- [ ] Cypher query library: 20+ common patterns
- [ ] Natural language interface (future): "Find all CVEs that enable ransomware"
- [ ] Query performance: 10-hop queries complete in < 500ms
- [ ] Path ranking: results ordered by probability score (highest first)
- [ ] Export results: CSV, JSON, PDF report
- [ ] Saved queries: analysts can bookmark frequently used queries

**UI Components**:
- [ ] Graph query builder interface
- [ ] Natural language query input (future)
- [ ] Visual graph result display
- [ ] Results table with path details
- [ ] Export format selector (CSV/JSON/PDF)
- [ ] Saved queries library
- [ ] Query performance metrics

---

### Story 4.3: Attack Surface Calculator
**As a** CISO
**I want** a comprehensive view of my organization's CVE exposure
**So that** I can report attack surface to the board with confidence

**Priority**: HIGH
**Story Points**: 13
**Persona**: Michael Rodriguez (CISO)
**Phase**: Phase 4 (Months 10-12)

**APIs Required**:
- `GET /api/v1/attack-surface/summary` - Overall statistics
- `GET /api/v1/attack-surface/heatmap` - Equipment × Tactic matrix
- `POST /api/v1/attack-surface/export-pdf` - Generate board report

**Data Required**:
- All equipment and CVE mappings
- Risk scores and tactic associations
- Historical trend data

**Acceptance Criteria**:
- [ ] Calculate total CVEs per customer (all equipment combined)
- [ ] Filter by: location (internal/DMZ/external), criticality (critical/high/medium/low)
- [ ] Risk heatmap: equipment × tactic matrix (color-coded by probability × impact)
- [ ] Export to PDF: board-ready report with executive summary
- [ ] Execution time: < 10 seconds for 10,000 assets
- [ ] Trend analysis: compare attack surface week-over-week
- [ ] Top 10 vulnerable assets: ranked by (CVE count × average risk score)

**UI Components**:
- [ ] Attack surface overview dashboard
- [ ] Risk heatmap visualization (equipment × tactic)
- [ ] Filter controls (location, criticality)
- [ ] Top 10 vulnerable assets list
- [ ] Week-over-week trend chart
- [ ] PDF export button for board report
- [ ] Executive summary panel

---

### Story 7.3: Audit Logging
**As a** Compliance Officer
**I want** all API calls and user actions logged
**So that** I can audit who did what and when for compliance

**Priority**: MEDIUM
**Story Points**: 5
**Persona**: Compliance Officer
**Phase**: Cross-Phase

**APIs Required**:
- `GET /api/v1/audit-log` - Query audit logs
- `POST /api/v1/audit-log/export` - Export logs

**Data Required**:
- PostgreSQL audit_log table
- Fields: user_id, action, resource_type, resource_id, timestamp, IP, request_body, response_status
- 1-year retention

**Acceptance Criteria**:
- [ ] PostgreSQL `audit_log` table with all required fields
- [ ] All API calls logged automatically (FastAPI middleware)
- [ ] Retention: 1 year (configurable)
- [ ] UI: "Audit Log" page (admin-only) with filters
- [ ] Export: CSV, JSON for auditors
- [ ] Performance: Logging adds < 10ms to API response time

**UI Components**:
- [ ] Audit log viewer page (admin only)
- [ ] Filter controls (user, date range, action type)
- [ ] Search functionality
- [ ] Log detail modal
- [ ] Export button (CSV/JSON)
- [ ] Date range picker

---

### Story 7.5: Performance Testing and Optimization
**As a** DevOps Engineer
**I want** automated performance tests to catch regressions
**So that** we maintain p99 latency < 2s for all API endpoints

**Priority**: MEDIUM
**Story Points**: 13
**Persona**: DevOps Engineer
**Phase**: Cross-Phase

**APIs Required**:
- Load testing infrastructure (Locust)
- Benchmarking endpoints

**Data Required**:
- Performance baselines: p50, p90, p99, p99.9 latencies
- Throughput metrics (requests/second)
- Regression detection thresholds

**Acceptance Criteria**:
- [ ] Locust load testing: Simulate 100 concurrent users
- [ ] Performance benchmarks: Run weekly, compare to baseline
- [ ] Regression detection: Alert if p99 latency increases > 20%
- [ ] Optimization: Database indexes, Redis caching for hot paths
- [ ] CI/CD integration: Performance tests run on staging before production deploy
- [ ] Benchmarking report: p50, p90, p99, p99.9 latencies + throughput

**UI Components**:
- [ ] Performance dashboard
- [ ] Latency percentile charts
- [ ] Throughput graphs
- [ ] Regression alerts
- [ ] Baseline comparison view
- [ ] Historical performance trends
- [ ] Benchmark report viewer

---

## ENHANCEMENT 27: PSYCHOHISTORY STORIES

All Enhancement 27 stories are operational and deployed as of 2025-11-28.

### E27-1.1: Predict Seldon Crises Before Manifestation
**As a** Chief Information Security Officer
**I want** to detect emerging Seldon Crises 3-8 months before they manifest
**So that** I can implement interventions during the critical window

**Priority**: HIGH
**Story Points**: 21
**Persona**: Michael Rodriguez (CISO)
**Status**: DEPLOYED (2025-11-28)

**APIs Required**:
- `GET /api/v1/psychohistory/seldon-crises` - Get all crisis probabilities
- `GET /api/v1/psychohistory/crisis/{crisis_id}` - Get specific crisis details
- `GET /api/v1/psychohistory/crisis-indicators` - Get leading indicators

**Data Required**:
- SeldonCrisis nodes: SC001, SC002, SC003
- CrisisIndicator nodes with current_value and crisis_threshold
- Bifurcation analysis parameters

**Acceptance Criteria**:
- [ ] System displays composite probability scores for all 3 Seldon Crises
- [ ] Leading indicators update in real-time from threat intelligence feeds
- [ ] Crisis transitions: STABLE → CAUTION → WARNING → CRITICAL
- [ ] Intervention window countdown shows remaining time for action
- [ ] Dashboard highlights indicators approaching bifurcation points

**Working Query**:
```cypher
MATCH (sc:SeldonCrisis)
MATCH (ci:CrisisIndicator)-[:INDICATES]->(sc)
WHERE ci.current_value IS NOT NULL
WITH sc, avg(ci.current_value / ci.crisis_threshold) AS crisis_probability
RETURN sc.crisis_id, sc.name, crisis_probability,
       CASE
         WHEN crisis_probability > 0.8 THEN 'CRITICAL'
         WHEN crisis_probability > 0.6 THEN 'WARNING'
         WHEN crisis_probability > 0.4 THEN 'CAUTION'
         ELSE 'STABLE'
       END AS status
```

**UI Components**:
- [ ] Seldon Crisis dashboard with 3 crisis cards
- [ ] Crisis probability gauge (0-100%)
- [ ] Status indicator (STABLE/CAUTION/WARNING/CRITICAL)
- [ ] Intervention window countdown timer
- [ ] Leading indicators table with current values
- [ ] Bifurcation point alerts
- [ ] Historical crisis probability trend chart

---

### E27-1.2: Prioritize Vulnerabilities Using R₀ Calculations
**As a** CISO allocating limited remediation resources
**I want** to see which vulnerabilities have epidemic potential (R₀ > 1)
**So that** I focus patching efforts on threats that will spread

**Priority**: HIGH
**Story Points**: 13
**Persona**: Michael Rodriguez (CISO), Sarah Chen (Security Analyst)
**Status**: DEPLOYED (2025-11-28)

**APIs Required**:
- `GET /api/v1/psychohistory/r0/{cve_id}` - Get R₀ for CVE
- `GET /api/v1/psychohistory/r0/prioritized` - Get prioritized CVE list by R₀

**Data Required**:
- Vulnerability nodes with epidemic parameters
- Network topology eigenvalue λmax
- Transmission rate β and recovery rate γ

**Acceptance Criteria**:
- [ ] Each vulnerability displays calculated R₀ value
- [ ] Vulnerabilities ranked by R₀ × CVSS (epidemic potential × damage)
- [ ] Network topology eigenvalue λmax computed from asset graph
- [ ] Transmission rate β from historical exploit data
- [ ] Recovery rate γ from mean time to patch (MTTP)
- [ ] Dashboard shows: SPREADING (R₀ > 1), ENDEMIC (R₀ = 1), DECLINING (R₀ < 1)

**Working Query**:
```cypher
MATCH (v:Vulnerability)-[:EXPLOITS]->(s:System)
WITH v, count(s) AS susceptible_hosts
WITH v, susceptible_hosts,
     custom.psychohistory.epidemicThreshold(0.3, 0.1, susceptible_hosts) AS R0
RETURN v.cve_id, v.cvss_score, R0,
       CASE
         WHEN R0 > 1.5 THEN 'NOW (guaranteed spread)'
         WHEN R0 > 1.0 THEN 'NEXT (borderline)'
         ELSE 'NEVER (will die out)'
       END AS priority_tier
ORDER BY R0 DESC
```

**UI Components**:
- [ ] R₀ prioritization dashboard
- [ ] CVE table with R₀ column and color coding
- [ ] Priority tier badges (NOW/NEXT/NEVER)
- [ ] R₀ × CVSS combined score
- [ ] Filter by priority tier
- [ ] Epidemic spread visualization
- [ ] Network topology impact chart

---

### E27-2.1: Detect Critical Slowing Indicators in Real-Time
**As a** SOC analyst monitoring live alerts
**I want** to see when system behavior shows critical slowing indicators
**So that** I can escalate before a security event transitions to crisis state

**Priority**: HIGH
**Story Points**: 13
**Persona**: Alex Thompson (SOC Analyst)
**Status**: DEPLOYED (2025-11-28)

**APIs Required**:
- `GET /api/v1/psychohistory/critical-slowing` - Get critical slowing metrics
- `GET /api/v1/psychohistory/autocorrelation` - Get autocorrelation data
- WebSocket for real-time updates

**Data Required**:
- Time series data for security metrics (login failures, network anomalies)
- Autocorrelation calculations
- Variance increase tracking
- Detrended time series

**Acceptance Criteria**:
- [ ] Real-time autocorrelation plot for key security metrics
- [ ] Variance increase alerts when σ² exceeds baseline by 2× or more
- [ ] Detrended time series removes seasonal patterns
- [ ] Color-coded dashboard: GREEN (ρ < 0.4), YELLOW (0.4-0.6), ORANGE (0.6-0.8), RED (>0.8)
- [ ] Alert: "High autocorrelation detected in firewall denies - possible attack buildup"

**Working Query**:
```cypher
MATCH (org:Organization {id: 'org_42'})-[:HAS_INCIDENT]->(i:Incident)
WHERE i.timestamp > datetime() - duration('P90D')
WITH org, count(i) AS recent_incidents
WITH org, recent_incidents, 0.5 AS mu_stress, 0.3 AS resilience
WITH org,
     custom.psychohistory.bifurcationMu(mu_stress, resilience) AS mu,
     custom.psychohistory.crisisVelocity(mu_stress - resilience, 0.5) AS velocity
RETURN org.name, recent_incidents, mu AS crisis_parameter,
       velocity AS crisis_acceleration,
       CASE
         WHEN mu > 0.8 THEN 'RED (crisis imminent)'
         WHEN mu > 0.6 THEN 'ORANGE (high autocorrelation)'
         WHEN mu > 0.4 THEN 'YELLOW (elevated variance)'
         ELSE 'GREEN (stable)'
       END AS alert_level
```

**UI Components**:
- [ ] Real-time autocorrelation chart
- [ ] Variance increase indicator
- [ ] Detrended time series plot
- [ ] Color-coded alert level badge
- [ ] Critical slowing alerts panel
- [ ] Historical metric trends
- [ ] Alert threshold configuration

---

### E27-3.1: Quantified Risk with Confidence Intervals
**As a** enterprise risk manager
**I want** to report cyber risk exposure as a probability distribution with confidence intervals
**So that** I meet ERM standards for quantitative risk assessment

**Priority**: HIGH
**Story Points**: 13
**Persona**: Risk Manager
**Status**: DEPLOYED (2025-11-28)

**APIs Required**:
- `GET /api/v1/psychohistory/economic-metrics` - Get risk metrics with CI
- `POST /api/v1/psychohistory/monte-carlo` - Run Monte Carlo simulation

**Data Required**:
- Economic metrics: expected loss, CI lower/upper bounds
- Monte Carlo simulation results (10,000 iterations)
- Bootstrap confidence intervals

**Acceptance Criteria**:
- [ ] Risk register displays: "Expected Loss = $1.2M [95% CI: $0.8M - $1.9M]"
- [ ] Monte Carlo simulation runs 10,000 scenarios in <30 seconds
- [ ] Sensitivity analysis identifies key drivers
- [ ] Risk appetite comparison
- [ ] Integration with ERM tools (export to Archer, ServiceNow GRC)

**Working Query**:
```cypher
MATCH (org:Organization)-[:HAS_METRIC]->(em:EconomicMetric {metric_type: 'Cyber_Risk_Expected_Loss'})
WITH org, em.value AS expected_loss, em.ci_lower AS ci_lower, em.ci_upper AS ci_upper
RETURN org.name, expected_loss AS expected_loss_usd,
       ci_lower AS ci_95_lower, ci_upper AS ci_95_upper,
       (ci_upper - ci_lower) / 2.0 AS margin_of_error,
       'Monte Carlo simulation (10,000 iterations)' AS methodology
```

**UI Components**:
- [ ] Risk dashboard with expected loss display
- [ ] Confidence interval visualization (range bars)
- [ ] Monte Carlo simulation results chart
- [ ] Sensitivity analysis table
- [ ] Risk appetite gauge
- [ ] Export to ERM tools button
- [ ] Methodology documentation link

---

### E27-5.1: OT/ICS Attack Cascade Prediction
**As an** OT/ICS operator managing substations
**I want** to predict which control systems will be compromised next
**So that** I can implement network segmentation before cascades occur

**Priority**: HIGH
**Story Points**: 21
**Persona**: Infrastructure Operator
**Status**: DEPLOYED (2025-11-28)

**APIs Required**:
- `GET /api/v1/psychohistory/ics-cascade/{asset_id}` - Get cascade prediction
- `POST /api/v1/psychohistory/ics-simulate` - Simulate cascade scenarios

**Data Required**:
- SCADA/ICS network topology
- Asset communication relationships
- OT-specific R₀ calculations
- Protocol-specific transmission rates

**Acceptance Criteria**:
- [ ] SCADA network topology mapped with ICS-specific R₀ calculations
- [ ] Cascade simulation: "If attacker compromises HMI A, RTUs B/C/D compromised in 4 hours"
- [ ] Segmentation effectiveness analysis
- [ ] Protocol-specific transmission rates: Modbus, DNP3, IEC 61850
- [ ] Safety-critical system identification

**Working Query**:
```cypher
MATCH (scada:Asset {type: 'SCADA_HMI'})-[:COMMUNICATES_WITH*1..3]->(downstream:Asset)
WHERE scada.cve_id IS NOT NULL
WITH scada, collect(DISTINCT downstream) AS cascade_targets
WITH scada, cascade_targets,
     custom.psychohistory.epidemicThreshold(0.7, 0.2, size(cascade_targets)) AS R0_ics
RETURN scada.name, scada.cve_id, R0_ics,
       size(cascade_targets) AS systems_at_risk,
       CASE
         WHEN R0_ics > 2.0 THEN 'CRITICAL: Segment network immediately'
         WHEN R0_ics > 1.0 THEN 'WARNING: Prioritize patching'
         ELSE 'CONTAINED: Monitor only'
       END AS recommendation
```

**UI Components**:
- [ ] ICS network topology visualization
- [ ] Cascade simulation interface
- [ ] Systems at risk list
- [ ] Segmentation effectiveness calculator
- [ ] Protocol-specific parameters display
- [ ] Safety-critical system highlighting
- [ ] Recommendation action panel

---

## API MAPPING REFERENCE

### Core CVE APIs
- `POST /api/v1/cve/ingest` - Automated CVE ingestion
- `GET /api/v1/cve/{cve_id}` - Get CVE details
- `GET /api/v1/cve/{cve_id}/cwe` - Get CWE mappings
- `GET /api/v1/cve/{cve_id}/score` - Get risk score
- `POST /api/v1/score_cve` - Score single CVE
- `POST /api/v1/score_batch` - Batch score CVEs

### Equipment APIs
- `POST /api/v1/equipment/import/csv` - Upload equipment CSV
- `POST /api/v1/equipment/import/cmdb` - Connect to CMDB
- `GET /api/v1/equipment/{equipment_id}/cves` - Get equipment CVEs
- `GET /api/v1/equipment/summary` - Equipment dashboard stats

### Action & Mitigation APIs
- `GET /api/v1/cve/{cve_id}/mitigations` - Get mitigations
- `GET /api/v1/actions/prioritized` - Get ranked actions
- `POST /api/v1/actions/update-status` - Update action status
- `POST /api/v1/rules/generate` - Generate SIEM rules

### Psychohistory APIs (E27)
- `GET /api/v1/psychohistory/seldon-crises` - Seldon crisis probabilities
- `GET /api/v1/psychohistory/r0/{cve_id}` - Get R₀ for CVE
- `GET /api/v1/psychohistory/critical-slowing` - Critical slowing metrics
- `GET /api/v1/psychohistory/economic-metrics` - Risk metrics with CI
- `GET /api/v1/psychohistory/ics-cascade/{asset_id}` - ICS cascade prediction

### Authentication & Admin APIs
- `GET /api/v1/auth/verify` - Verify JWT token
- `GET /api/v1/users` - List users (admin)
- `PUT /api/v1/users/{user_id}/role` - Assign role (admin)
- `GET /api/v1/audit-log` - Query audit logs (admin)

### System APIs
- `GET /api/health` - Health check
- `GET /api/metrics` - Prometheus metrics
- `GET /api/v1/openapi.json` - OpenAPI specification

---

## DATA REQUIREMENTS REFERENCE

### Neo4j Graph Nodes
- **CVE**: cve_id, description, cvss_score, published_date
- **CWE**: cwe_id, name, description
- **CAPEC**: capec_id, name, description
- **Technique**: technique_id, name, tactic
- **Tactic**: tactic_id, name
- **Equipment**: hostname, software, version, location, criticality, cpe
- **SeldonCrisis**: crisis_id, name, intervention_window
- **CrisisIndicator**: indicator_id, current_value, crisis_threshold

### Neo4j Relationships
- `(:CVE)-[:HAS_CWE {confidence}]->(:CWE)`
- `(:CWE)-[:MAPS_TO_CAPEC {confidence}]->(:CAPEC)`
- `(:CAPEC)-[:MAPS_TO_TECHNIQUE {confidence}]->(:Technique)`
- `(:Technique)-[:BELONGS_TO_TACTIC]->(:Tactic)`
- `(:Equipment)-[:AFFECTED_BY]->(:CVE)`
- `(:CrisisIndicator)-[:INDICATES]->(:SeldonCrisis)`

### PostgreSQL Tables
- **jobs**: job_id, status, start_time, end_time, metrics
- **job_steps**: step_id, job_id, status, logs
- **job_logs**: log_id, job_id, level, message, timestamp
- **audit_log**: user_id, action, resource_type, resource_id, timestamp, IP, request_body, response_status
- **customer_profiles**: customer_id, industry_sector, equipment_types, geographic_region

### Qdrant Collections
- **cve_embeddings**: CVE text embeddings for similarity search
- **technique_embeddings**: ATT&CK technique embeddings

---

## IMPLEMENTATION PRIORITIES

### Sprint 1 (Weeks 1-2): Authentication & Core Infrastructure
1. Story 7.1: Clerk Authentication (CRITICAL)
2. Basic dashboard layout
3. API health checks

### Sprint 2 (Weeks 3-4): CVE Foundation
1. Story 1.1: CVE Ingestion (CRITICAL)
2. Story 1.2: CVE-CWE Mapping (CRITICAL)
3. CVE list and detail pages

### Sprint 3 (Weeks 5-6): Risk Scoring
1. Story 2.1: Bayesian Scoring (CRITICAL)
2. Risk score visualization
3. CVE prioritization interface

### Sprint 4 (Weeks 7-8): Equipment Integration
1. Story 4.1: Equipment Import (CRITICAL)
2. Story 4.2: CVE-Equipment Mapping (CRITICAL)
3. Equipment inventory interface

### Sprint 5 (Weeks 9-10): Actionable Outputs
1. Story 5.1: Mitigations (CRITICAL)
2. Story 5.3: Priority Planner (CRITICAL)
3. Kanban board implementation

### Sprint 6 (Weeks 11-12): Psychohistory (E27)
1. E27-1.1: Seldon Crisis Dashboard
2. E27-1.2: R₀ Prioritization
3. E27-2.1: Critical Slowing Indicators

---

## DESIGN SYSTEM COMPONENTS

### Core Components Needed
- **DataTable**: Sortable, filterable tables for CVEs, equipment, actions
- **Card**: Summary cards for dashboard widgets
- **Badge**: Status indicators (priority, risk level, confidence)
- **ProgressBar**: For ingestion jobs, batch scoring
- **Modal**: For confirmations, detail views
- **Form**: For CSV upload, CMDB connection, manual assignments
- **Chart**: Line charts (trends), bar charts (distributions), heatmaps (risk matrices)
- **KanbanBoard**: For action planner
- **GraphVisualization**: For semantic chains and network topology

### Color Scheme by Priority
- **Critical/High Risk**: Red (#DC2626)
- **Warning/Medium Risk**: Yellow (#F59E0B)
- **Caution/Low Risk**: Blue (#3B82F6)
- **Stable/No Risk**: Green (#10B981)
- **Info**: Gray (#6B7280)

---

**END OF COMPILATION**

**Total Stories**: 49 (31 base + 18 psychohistory)
**Personas Covered**: 6 (Security Analyst, CISO, SOC Analyst, Risk Manager, Compliance Officer, Infrastructure Operator)
**Phases**: 5 development phases + Enhancement 27
**API Endpoints**: 40+
**Data Nodes**: 10+ types
**Relationships**: 6+ types
