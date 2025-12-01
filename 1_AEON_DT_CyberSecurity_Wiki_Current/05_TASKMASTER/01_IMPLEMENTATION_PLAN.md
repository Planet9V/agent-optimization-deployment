# AEON Digital Twin: TASKMASTER Implementation Plan

**File**: 01_IMPLEMENTATION_PLAN.md
**Created**: 2025-11-12 06:15:00 UTC
**Modified**: 2025-11-12 06:15:00 UTC
**Version**: 1.0.0
**Author**: AEON Development Team
**Purpose**: Comprehensive TASKMASTER implementation plan for systematic development
**Status**: ACTIVE - AUTHORITATIVE EXECUTION PLAN

**References**:
- Constitution: `/00_AEON_CONSTITUTION.md` (Article II, Section 2.5: TASKMASTER)
- Architecture: `/01_ARCHITECTURE/01_COMPREHENSIVE_ARCHITECTURE.md`
- PRD: `/02_REQUIREMENTS/01_PRODUCT_REQUIREMENTS.md`
- Technical Specs: `/03_SPECIFICATIONS/01_TECHNICAL_SPECS.md`
- User Stories: `/04_USER_STORIES/01_USER_STORIES.md`

---

## Table of Contents

1. [TASKMASTER Methodology Overview](#section-1-taskmaster-methodology-overview)
2. [Phase 1 Implementation (Months 1-3)](#section-2-phase-1-implementation)
3. [Phase 2 Implementation (Months 4-6)](#section-3-phase-2-implementation)
4. [Phase 3 Implementation (Months 7-9)](#section-4-phase-3-implementation)
5. [Phase 4 Implementation (Months 10-12)](#section-5-phase-4-implementation)
6. [Phase 5 Implementation (Months 13-15)](#section-6-phase-5-implementation)
7. [Agent Coordination Matrix](#section-7-agent-coordination-matrix)
8. [Ruv-Swarm Orchestration](#section-8-ruv-swarm-orchestration)
9. [Qdrant Memory Integration](#section-9-qdrant-memory-integration)
10. [Quality Gates and Validation](#section-10-quality-gates-and-validation)

---

## Section 1: TASKMASTER Methodology Overview

### 1.1 Constitutional Mandate

**From Constitution Article II, Section 2.5**:
- ALL development work MUST be tracked as TASKMASTER tasks
- Tasks assigned to Ruv-Swarm agents or human developers
- Stored in Qdrant `task_history` collection for persistent memory
- Cross-session state maintained for continuity

### 1.2 Task Structure Template

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
    - "qdrant_collection/key_1"
    - "qdrant_collection/key_2"

  dependencies:
    - "TASK-YYYY-MM-DD-XXX (blocking)"
    - "TASK-YYYY-MM-DD-YYY (soft dependency)"

  status: "[CREATED | ASSIGNED | IN_PROGRESS | BLOCKED | COMPLETED | ARCHIVED]"
  status_updated: "YYYY-MM-DD HH:MM:SS UTC"
```

### 1.3 Task Lifecycle

```
1. CREATED → Task defined, not yet assigned
2. ASSIGNED → Agent/human assigned, ready to start
3. IN_PROGRESS → Active work happening
4. BLOCKED → Cannot proceed (waiting on dependency)
5. COMPLETED → All success criteria met, deliverables verified
6. ARCHIVED → Task completed and documented for posterity
```

### 1.4 Qdrant Storage

**Every task stored in**:
- Collection: `task_history`
- Vector: BERT embedding of task description
- Payload: Full task YAML + status updates

**Memory Operations**:
```python
from qdrant_client import QdrantClient
client = QdrantClient(url="http://172.18.0.6:6333")

# Store task
client.upsert(
    collection_name="task_history",
    points=[
        PointStruct(
            id=hash("TASK-2025-11-12-001"),
            vector=bert_model.encode("Build CVE ingestion pipeline"),
            payload={
                "task_id": "TASK-2025-11-12-001",
                "status": "IN_PROGRESS",
                "assigned_to": "data_pipeline_engineer",
                "deliverables": ["NVD API integration", "Neo4j insertion"],
                ...
            }
        )
    ]
)

# Query related tasks
results = client.search(
    collection_name="task_history",
    query_vector=bert_model.encode("CVE data ingestion"),
    limit=5,
    query_filter={"must": [{"key": "status", "match": {"value": "COMPLETED"}}]}
)
```

---

## Section 2: Phase 1 Implementation (Months 1-3)
### Semantic Foundation

### Week 1-2: Project Initialization

**TASK-2025-11-12-001**: Infrastructure Setup
```yaml
task:
  id: "TASK-2025-11-12-001"
  created: "2025-11-12 06:15:00 UTC"
  assigned_to: "devops_reliability_engineer"
  priority: "CRITICAL"
  deadline: "2025-11-20"

  deliverables:
    - "Docker Compose running all 7 containers (Neo4j, PostgreSQL, MySQL, Qdrant, MinIO, OpenSPG, Next.js)"
    - "Health checks passing for all services"
    - ".env file with all required secrets (Clerk, NVD API, etc.)"
    - "Qdrant collections created: agent_memory, task_history, semantic_chains"

  success_criteria:
    - "`docker-compose up -d` succeeds, all containers healthy"
    - "`curl http://localhost:8000/api/health` returns 200"
    - "`curl http://localhost:3000/api/health` returns 200"
    - "Qdrant `/collections` endpoint shows 3 collections"

  risks:
    - "Qdrant container currently unhealthy (known issue)"
    - "OpenSPG server unhealthy status"

  issues:
    - "URGENT: Debug Qdrant health check (TASK-2025-11-12-029 from PRD)"

  notes:
    - "Use existing docker-compose.yml from Architecture doc"
    - "Test Clerk auth immediately (NEVER BREAK CLERK AUTH)"

  memory_keys:
    - "task_history/infrastructure_001"
    - "agent_memory/devops/docker_setup"

  dependencies:
    - "None (foundational task)"

  status: "CREATED"
  status_updated: "2025-11-12 06:15:00 UTC"
```

**Assigned Agent**: devops_reliability_engineer (Ruv-Swarm)
**Ruv-Swarm Command**:
```bash
npx claude-flow@alpha agent spawn --type "devops" --task "TASK-2025-11-12-001" --topology "mesh"
```

---

**TASK-2025-11-12-002**: NVD API Integration
```yaml
task:
  id: "TASK-2025-11-12-002"
  created: "2025-11-12 06:20:00 UTC"
  assigned_to: "data_pipeline_engineer"
  priority: "CRITICAL"
  deadline: "2025-12-10"

  deliverables:
    - "Python script: backend/src/integrations/nvd_integration.py"
    - "Scheduled job: runs at 02:00 UTC daily via cron"
    - "PostgreSQL jobs table populated with ingestion records"
    - "Neo4j CVE nodes created (target: 10,000+ CVEs)"

  success_criteria:
    - "Imports ≥ 95% of CVEs published in last 24 hours"
    - "Execution time < 15 minutes for 500 CVEs/day"
    - "Job reliability: 100% (zero lost jobs after 3 retries)"
    - "Rate limiting: respects NVD 50 requests/30s limit"

  risks:
    - "NVD API rate limits (50 req/30s with key, 5 req/30s without)"
    - "Network timeouts during large batch imports"

  issues:
    - "None currently"

  notes:
    - "Use Technical Specs Section 4.1 NVDIntegration class"
    - "Retry logic: 3 attempts with exponential backoff (1s, 4s, 16s)"
    - "Store raw CVE JSON in MinIO for audit trail"

  memory_keys:
    - "task_history/data_pipeline_002"
    - "agent_memory/data_pipeline_engineer/nvd_api"

  dependencies:
    - "TASK-2025-11-12-001 (infrastructure must be running)"

  status: "CREATED"
  status_updated: "2025-11-12 06:20:00 UTC"
```

**Assigned Agent**: data_pipeline_engineer (Ruv-Swarm)
**Coordination**:
- Mesh topology: data_pipeline_engineer ↔ devops_reliability_engineer
- Share memory_key: "infrastructure/database_connections"

---

### Week 3-4: Semantic Chain Construction (CVE → CWE)

**TASK-2025-11-12-005**: CVE → CWE Mapping
```yaml
task:
  id: "TASK-2025-11-12-005"
  created: "2025-11-12 06:25:00 UTC"
  assigned_to: "knowledge_graph_engineer"
  priority: "CRITICAL"
  deadline: "2025-12-20"

  deliverables:
    - "Cypher script: create CVE-[:HAS_CWE]->CWE relationships"
    - "NER v9 fallback for missing NVD CWE data"
    - "Confidence scores: 0.95 for NVD, < 0.80 for NER extraction"
    - "Daily validation: check 95%+ CVEs have CWE"

  success_criteria:
    - "≥ 95% of 10,000 CVEs have at least one CWE"
    - "Multiple CWEs per CVE supported (test: CVE with 3 CWEs → 3 edges)"
    - "Default `CWE-NVD-noinfo` for missing CWE"
    - "Neo4j query: `MATCH (c:CVE)-[:HAS_CWE]->(w:CWE) RETURN COUNT(DISTINCT c)` ≥ 9,500"

  risks:
    - "NVD data quality: some CVEs lack CWE"
    - "NER v9 extraction accuracy unknown (need validation dataset)"

  issues:
    - "None currently"

  notes:
    - "Use PRD FR-2.1 specification"
    - "NER v9 on port 8001, test: `curl http://localhost:8001/extract`"

  memory_keys:
    - "task_history/semantic_chain_005"
    - "agent_memory/kg_engineer/cve_cwe_mapping"

  dependencies:
    - "TASK-2025-11-12-002 (CVEs must be ingested first)"

  status: "CREATED"
  status_updated: "2025-11-12 06:25:00 UTC"
```

**Assigned Agent**: knowledge_graph_engineer (Ruv-Swarm)
**Parallel Tasks**:
- TASK-2025-11-12-006 (CWE → CAPEC)
- TASK-2025-11-12-007 (CAPEC → Technique)
- TASK-2025-11-12-008 (Technique → Tactic)

**Coordination Strategy**: Hierarchical topology
- **Queen**: knowledge_graph_engineer (coordinates semantic mapping)
- **Workers**: data_pipeline_engineer (provides CVE data), qa_engineer (validates chains)

---

### Week 5-8: Full Chain Validation and Testing

**TASK-2025-11-12-009**: Semantic Chain Validation
```yaml
task:
  id: "TASK-2025-11-12-009"
  created: "2025-11-12 06:30:00 UTC"
  assigned_to: "qa_engineer"
  priority: "HIGH"
  deadline: "2026-01-10"

  deliverables:
    - "Automated Cypher query: validate CVE → Tactic paths"
    - "Daily validation job (03:00 UTC cron)"
    - "Dashboard widget: chain completeness trend (last 30 days)"
    - "Alert system: email if completeness < 75%"

  success_criteria:
    - "≥ 80% of CVEs have complete semantic chain"
    - "Validation query executes in < 30 seconds"
    - "Dashboard loads in < 2 seconds"
    - "Alert fires within 5 minutes of threshold breach"

  risks:
    - "Neo4j performance: 3.3M edges may slow validation query"

  issues:
    - "Need dashboard framework (consider Grafana or Next.js custom)"

  notes:
    - "Use PRD FR-2.5 validation query"
    - "Log incomplete chains for manual review"

  memory_keys:
    - "task_history/validation_009"
    - "agent_memory/qa_engineer/chain_validation"

  dependencies:
    - "TASK-2025-11-12-005 through 008 (all semantic mappings)"

  status: "CREATED"
  status_updated: "2025-11-12 06:30:00 UTC"
```

**Assigned Agent**: qa_engineer (Ruv-Swarm)
**Quality Gate**: Phase 1 cannot complete until this task shows ≥ 80% chain completeness

---

### Week 9-12: Job Persistence and Reliability

**TASK-2025-11-12-010**: PostgreSQL Job Persistence
```yaml
task:
  id: "TASK-2025-11-12-010"
  created: "2025-11-12 06:35:00 UTC"
  assigned_to: "backend_engineer"
  priority: "CRITICAL"
  deadline: "2026-01-20"

  deliverables:
    - "PostgreSQL schema: jobs, job_steps, job_logs tables"
    - "Python job wrapper: logs all long-running jobs"
    - "Retry logic function: `retry_failed_job(job_id)`"
    - "Jobs dashboard: shows running, completed, failed (last 7 days)"

  success_criteria:
    - "100% job reliability over 30-day test period"
    - "Failed jobs retry 3 times with exponential backoff"
    - "Dashboard query time < 1 second"
    - "Zero lost jobs (validate against NVD daily CVE count)"

  risks:
    - "PostgreSQL connection pool exhaustion under high load"

  issues:
    - "None currently"

  notes:
    - "Use Technical Specs Section 2.1.1 schema"
    - "Implement retry_failed_job stored procedure"

  memory_keys:
    - "task_history/job_persistence_010"
    - "agent_memory/backend_engineer/job_system"

  dependencies:
    - "TASK-2025-11-12-001 (PostgreSQL must be running)"

  status: "CREATED"
  status_updated: "2025-11-12 06:35:00 UTC"
```

**Assigned Agent**: backend_engineer (Ruv-Swarm)

---

## Section 3: Phase 2 Implementation (Months 4-6)
### Probabilistic Intelligence

### Week 13-18: Bayesian AttackChainScorer

**TASK-2025-11-12-015**: AttackChainScorer Implementation
```yaml
task:
  id: "TASK-2025-11-12-015"
  created: "2025-11-12 06:40:00 UTC"
  assigned_to: "ml_engineer"
  priority: "CRITICAL"
  deadline: "2026-03-15"

  deliverables:
    - "Python class: backend/src/intelligence/attack_chain_scorer.py"
    - "Bayesian formula: P(Tactic|CVE) = Σ [P(Tactic|Tech) × P(Tech|CAPEC) × P(CAPEC|CWE) × P(CWE|CVE)]"
    - "Laplace smoothing: α=1.0 for zero-count edges"
    - "Unit tests: ≥ 85% code coverage"

  success_criteria:
    - "Accuracy ≥ 85% on CISA KEV test set (100 known exploited CVEs)"
    - "Execution time < 2 seconds per CVE (p99)"
    - "Returns JSON with overall_probability + confidence_interval"
    - "Edge probabilities logged for debugging"

  risks:
    - "Sparse data: some CVEs have only 1 chain path (no probability variation)"
    - "Prior estimation: edge frequencies may not reflect real-world likelihoods"

  issues:
    - "Need CISA KEV dataset for validation (download from cisa.gov)"

  notes:
    - "Use Technical Specs Section 3.1 implementation"
    - "Consult external statistician for prior selection (budget: $5K)"
    - "Document algorithm in /docs/bayesian_scoring.md"

  memory_keys:
    - "task_history/ml_engineer_015"
    - "agent_memory/ml_engineer/bayesian_scoring"
    - "model_artifacts/attack_chain_scorer_v1"

  dependencies:
    - "TASK-2025-11-12-009 (semantic chains must be ≥ 80% complete)"

  status: "CREATED"
  status_updated: "2025-11-12 06:40:00 UTC"
```

**Assigned Agent**: ml_engineer (Ruv-Swarm)
**External Dependency**: Hire statistician consultant (H1 2026)

---

**TASK-2025-11-12-016**: Monte Carlo Confidence Intervals
```yaml
task:
  id: "TASK-2025-11-12-016"
  created: "2025-11-12 06:45:00 UTC"
  assigned_to: "ml_engineer"
  priority: "HIGH"
  deadline: "2026-03-30"

  deliverables:
    - "Monte Carlo simulation: 10,000 samples per CVE"
    - "Beta distribution sampling for each edge probability"
    - "Wilson Score 95% CI calculation"
    - "Performance optimization: GPU acceleration if needed"

  success_criteria:
    - "Execution time < 3 seconds for 10K samples"
    - "CI width reasonable: 0.05-0.15 for typical CVEs"
    - "95%+ of true probabilities fall within calculated CIs (statistical validation)"
    - "GPU usage (if applicable): < 50% of V100 memory"

  risks:
    - "CPU execution may be too slow (45s observed in initial tests)"
    - "GPU availability uncertain (AWS p3.2xlarge cost: $3.06/hour)"

  issues:
    - "Need to benchmark CPU vs. GPU performance"

  notes:
    - "Use Technical Specs Section 5.2 algorithm"
    - "Consider multiprocessing on CPU as alternative to GPU"

  memory_keys:
    - "task_history/monte_carlo_016"
    - "agent_memory/ml_engineer/monte_carlo"

  dependencies:
    - "TASK-2025-11-12-015 (AttackChainScorer must be working)"

  status: "CREATED"
  status_updated: "2025-11-12 06:45:00 UTC"
```

**Assigned Agent**: ml_engineer (Ruv-Swarm)
**Infrastructure Requirement**: AWS p3.2xlarge or equivalent (TASK-2025-11-12-031 from PRD)

---

### Week 19-24: API Development and Batch Scoring

**TASK-2025-11-12-020**: CVE Scoring API
```yaml
task:
  id: "TASK-2025-11-12-020"
  created: "2025-11-12 06:50:00 UTC"
  assigned_to: "backend_engineer"
  priority: "HIGH"
  deadline: "2026-04-15"

  deliverables:
    - "FastAPI endpoint: POST /api/v1/score_cve"
    - "Request validation: CVE ID format, customer context"
    - "Response format: JSON with probability, CI, chains"
    - "Error handling: 400, 404, 429, 500 with clear messages"

  success_criteria:
    - "p50 latency < 1s, p99 latency < 2s"
    - "Rate limiting: 10,000 requests/hour per API key"
    - "API tests: ≥ 90% coverage"
    - "Clerk auth integration: NEVER BREAK CLERK AUTH"

  risks:
    - "Neo4j query performance under load"

  issues:
    - "None currently"

  notes:
    - "Use Technical Specs Section 1.2.1 specification"
    - "Integrate with AttackChainScorer (TASK-2025-11-12-015)"
    - "Redis caching for hot CVEs (cache TTL: 1 hour)"

  memory_keys:
    - "task_history/api_020"
    - "agent_memory/backend_engineer/scoring_api"

  dependencies:
    - "TASK-2025-11-12-015 (AttackChainScorer)"
    - "TASK-2025-11-12-016 (Monte Carlo CI)"

  status: "CREATED"
  status_updated: "2025-11-12 06:50:00 UTC"
```

**Assigned Agent**: backend_engineer (Ruv-Swarm)

---

**TASK-2025-11-12-021**: Batch Scoring API
```yaml
task:
  id: "TASK-2025-11-12-021"
  created: "2025-11-12 06:55:00 UTC"
  assigned_to: "backend_engineer"
  priority: "HIGH"
  deadline: "2026-04-30"

  deliverables:
    - "FastAPI endpoint: POST /api/v1/score_batch"
    - "Parallel processing: 8 worker threads"
    - "WebSocket progress updates: every 100 CVEs"
    - "Partial success handling: return successful + failed separately"

  success_criteria:
    - "1,000 CVEs scored in < 60 seconds"
    - "Rate limiting: 10 batch requests/minute per customer"
    - "Progress indicator: real-time updates via WebSocket"
    - "Graceful degradation: if 5 CVEs fail, still return 995 scores"

  risks:
    - "Worker thread contention on Neo4j connections"

  issues:
    - "WebSocket library selection (consider: websockets, socket.io)"

  notes:
    - "Use Technical Specs Section 1.2.2 specification"
    - "PostgreSQL job tracking for batch jobs"

  memory_keys:
    - "task_history/batch_api_021"
    - "agent_memory/backend_engineer/batch_scoring"

  dependencies:
    - "TASK-2025-11-12-020 (single CVE scoring API)"

  status: "CREATED"
  status_updated: "2025-11-12 06:55:00 UTC"
```

**Assigned Agent**: backend_engineer (Ruv-Swarm)

---

## Section 4: Phase 3 Implementation (Months 7-9)
### Graph Neural Networks

### Week 25-32: GNN Training

**TASK-2025-11-12-025**: GNN Model Architecture
```yaml
task:
  id: "TASK-2025-11-12-025"
  created: "2025-11-12 07:00:00 UTC"
  assigned_to: "ml_research_engineer"
  priority: "HIGH"
  deadline: "2026-06-15"

  deliverables:
    - "PyTorch Geometric model: backend/src/intelligence/gnn_link_predictor.py"
    - "3-layer GAT: 128-dim input → 128-dim hidden (heads=4) → 64-dim output"
    - "Link prediction MLP: concat embeddings → 64 → 1 (sigmoid)"
    - "Training script: backend/src/intelligence/train_gnn.py"

  success_criteria:
    - "Training time < 4 hours on NVIDIA V100"
    - "Test set metrics: Precision ≥ 90%, Recall ≥ 85%, F1 ≥ 87%"
    - "Model size < 200 MB"
    - "Inference time < 10ms per link prediction"

  risks:
    - "GPU availability (AWS p3.2xlarge cost: $3.06/hour × 4 hours = $12.24/training run)"
    - "Overfitting: train/validation loss gap may exceed 0.05"

  issues:
    - "Need to allocate GPU budget ($500 for initial experiments)"

  notes:
    - "Use Technical Specs Section 3.2 implementation"
    - "Export Neo4j edges: 80% train, 10% validation, 10% test"
    - "Stratified sampling by edge type (HAS_CWE, MAPS_TO_CAPEC, etc.)"

  memory_keys:
    - "task_history/gnn_training_025"
    - "agent_memory/ml_research_engineer/gnn_architecture"
    - "model_artifacts/gnn_link_predictor_v1"

  dependencies:
    - "TASK-2025-11-12-009 (semantic chains for training data)"

  status: "CREATED"
  status_updated: "2025-11-12 07:00:00 UTC"
```

**Assigned Agent**: ml_research_engineer (Ruv-Swarm)
**Infrastructure**: AWS p3.2xlarge GPU instance (TASK-2025-11-12-031)

---

### Week 33-36: Missing Link Prediction

**TASK-2025-11-12-026**: CWE Prediction API
```yaml
task:
  id: "TASK-2025-11-12-026"
  created: "2025-11-12 07:05:00 UTC"
  assigned_to: "ml_application_engineer"
  priority: "MEDIUM"
  deadline: "2026-07-15"

  deliverables:
    - "FastAPI endpoint: POST /api/v1/predict_cwe"
    - "GNN inference: load model from /models/gnn_link_predictor_v1.pt"
    - "Top 5 CWE predictions with confidence scores"
    - "Human-in-the-loop UI: [Approve] [Reject] workflow"

  success_criteria:
    - "Only suggest if confidence > 70%"
    - "Analyst approval rate ≥ 80% (indicates good predictions)"
    - "Inference time < 100ms per CVE"
    - "Monthly accuracy report: prediction vs. analyst corrections"

  risks:
    - "Low analyst adoption if predictions are poor quality"

  issues:
    - "UI design needed (Next.js component)"

  notes:
    - "Use Technical Specs Section 3.2 GNN class"
    - "Log approved predictions to `predicted_cwe` table for retraining"

  memory_keys:
    - "task_history/cwe_prediction_026"
    - "agent_memory/ml_app_engineer/cwe_prediction_api"

  dependencies:
    - "TASK-2025-11-12-025 (trained GNN model)"

  status: "CREATED"
  status_updated: "2025-11-12 07:05:00 UTC"
```

**Assigned Agent**: ml_application_engineer (Ruv-Swarm)

---

## Section 5: Phase 4 Implementation (Months 10-12)
### Equipment Integration

### Week 37-44: Equipment Inventory

**TASK-2025-11-12-030**: Equipment CSV Import
```yaml
task:
  id: "TASK-2025-11-12-030"
  created: "2025-11-12 07:10:00 UTC"
  assigned_to: "integration_engineer"
  priority: "CRITICAL"
  deadline: "2026-09-15"

  deliverables:
    - "FastAPI endpoint: POST /api/v1/equipment/import (multipart/form-data)"
    - "CSV parser: headers (hostname, software, version, location, criticality)"
    - "CPE auto-matching: FuzzyWuzzy library"
    - "Manual override UI: unmatched assets shown for manual CPE assignment"

  success_criteria:
    - "95%+ auto-match rate for common software (Windows, Apache, PostgreSQL)"
    - "Bulk import: 10,000 assets in < 15 minutes"
    - "Fuzzy matching: 'Win10' → 'Windows 10' CPE"
    - "Import history: track uploads (timestamp, user, assets added/updated)"

  risks:
    - "CPE dictionary may not have all software variants"

  issues:
    - "Need NIST CPE dictionary (download from nvd.nist.gov)"

  notes:
    - "Use Technical Specs Section 1.2.3 specification"
    - "PostgreSQL `equipment` table schema (Section 2.1.2)"

  memory_keys:
    - "task_history/equipment_import_030"
    - "agent_memory/integration_engineer/cpe_matching"

  dependencies:
    - "TASK-2025-11-12-010 (PostgreSQL schema)"

  status: "CREATED"
  status_updated: "2025-11-12 07:10:00 UTC"
```

**Assigned Agent**: integration_engineer (Ruv-Swarm)

---

### Week 45-48: Attack Surface Calculator

**TASK-2025-11-12-035**: Risk Heatmap Generator
```yaml
task:
  id: "TASK-2025-11-12-035"
  created: "2025-11-12 07:15:00 UTC"
  assigned_to: "risk_analysis_engineer"
  priority: "HIGH"
  deadline: "2026-10-15"

  deliverables:
    - "Attack surface calculator: GET /api/v1/attack_surface/{customer_id}"
    - "Risk heatmap: equipment × tactic matrix (color-coded by probability × impact)"
    - "PDF export: board-ready report with executive summary"
    - "Trend analysis: compare attack surface week-over-week"

  success_criteria:
    - "Execution time < 10 seconds for 10,000 assets"
    - "Heatmap visual: green (low) → yellow → red (high)"
    - "PDF includes: executive summary, heatmap, top 10 vulnerable assets"
    - "Trend chart shows last 12 weeks"

  risks:
    - "Database query performance with large asset counts"

  issues:
    - "PDF generation library selection (consider: ReportLab, WeasyPrint)"

  notes:
    - "Use Technical Specs Section 1.2.4 specification"
    - "PostgreSQL query optimization with indexes on equipment_cve_mapping"

  memory_keys:
    - "task_history/attack_surface_035"
    - "agent_memory/risk_analyst/heatmap_generation"

  dependencies:
    - "TASK-2025-11-12-030 (equipment import)"
    - "TASK-2025-11-12-020 (CVE scoring API)"

  status: "CREATED"
  status_updated: "2025-11-12 07:15:00 UTC"
```

**Assigned Agent**: risk_analysis_engineer (Ruv-Swarm)

---

## Section 6: Phase 5 Implementation (Months 13-15)
### Actionable Outputs

### Week 49-54: Mitigation Recommendations

**TASK-2025-11-12-040**: ATT&CK Mitigation Engine
```yaml
task:
  id: "TASK-2025-11-12-040"
  created: "2025-11-12 07:20:00 UTC"
  assigned_to: "security_operations_engineer"
  priority: "CRITICAL"
  deadline: "2026-12-15"

  deliverables:
    - "Mitigation API: GET /api/v1/mitigations/{cve_id}"
    - "Query ATT&CK mitigations for techniques in CVE attack chains"
    - "Patching guidance: vendor advisory URL, patch ID, release date"
    - "Compensating controls: network segmentation, WAF rules if no patch"

  success_criteria:
    - "≥ 90% of scored CVEs have ≥1 mitigation"
    - "Mitigations prioritized by technique probability (highest first)"
    - "Patching guidance includes vendor advisory URL + patch KB"
    - "API response time < 500ms"

  risks:
    - "Vendor advisory database may be incomplete"

  issues:
    - "Need to build vendor advisory scraper (Microsoft, RedHat, Ubuntu)"

  notes:
    - "Use Technical Specs Section 1.2.5 specification"
    - "ATT&CK mitigations: https://attack.mitre.org/mitigations/"

  memory_keys:
    - "task_history/mitigations_040"
    - "agent_memory/sec_ops/mitigation_engine"

  dependencies:
    - "TASK-2025-11-12-020 (CVE scoring)"

  status: "CREATED"
  status_updated: "2025-11-12 07:20:00 UTC"
```

**Assigned Agent**: security_operations_engineer (Ruv-Swarm)

---

### Week 55-60: SIEM Rule Generation

**TASK-2025-11-12-045**: Detection Rule Generator
```yaml
task:
  id: "TASK-2025-11-12-045"
  created: "2025-11-12 07:25:00 UTC"
  assigned_to: "detection_engineering_lead"
  priority: "HIGH"
  deadline: "2027-01-30"

  deliverables:
    - "Detection API: POST /api/v1/detections/generate"
    - "Rule templates: Splunk SPL, Microsoft Sentinel KQL, Sigma YAML"
    - "Template variables: process names, file paths, registry keys from ATT&CK"
    - "Rule testing: unit tests with sample logs"

  success_criteria:
    - "≥ 80% rules deploy without syntax errors"
    - "Test rules against MITRE ATT&CK Evals public logs"
    - "Detection rate ≥ 70% on ATT&CK Evals"
    - "False positive rate < 10% (test on 1 week of production logs)"

  risks:
    - "SIEM syntax variations (Splunk SPL vs. Sentinel KQL)"

  issues:
    - "Need MITRE ATT&CK Evals dataset (download from mitre.org)"

  notes:
    - "Use Technical Specs Section 1.2.6 specification"
    - "Sigma: universal rule format, converts to Splunk/Sentinel/QRadar"

  memory_keys:
    - "task_history/detections_045"
    - "agent_memory/detection_lead/rule_generation"

  dependencies:
    - "TASK-2025-11-12-020 (CVE scoring)"

  status: "CREATED"
  status_updated: "2025-11-12 07:25:00 UTC"
```

**Assigned Agent**: detection_engineering_lead (Ruv-Swarm)

---

### Week 61-65: Priority Action Planner

**TASK-2025-11-12-050**: Remediation Prioritization
```yaml
task:
  id: "TASK-2025-11-12-050"
  created: "2025-11-12 07:30:00 UTC"
  assigned_to: "remediation_strategy_lead"
  priority: "CRITICAL"
  deadline: "2027-02-28"

  deliverables:
    - "Priority API: GET /api/v1/priority_actions/{customer_id}"
    - "Ranking formula: (Probability × CVSS Impact) - Remediation Effort"
    - "Effort estimator: patch (low), config change (low), software upgrade (medium), architecture change (high)"
    - "Kanban board UI: To Do, In Progress, Done (drag-drop)"

  success_criteria:
    - "Execution time < 5 seconds for 500 actions"
    - "Timeline accounts for patch cycles (monthly), change windows (quarterly)"
    - "Jira integration: export to Jira as tickets"
    - "Kanban drag-drop updates status in PostgreSQL"

  risks:
    - "Effort estimation may be inaccurate (need validation with pilot customers)"

  issues:
    - "UI framework selection (Next.js + react-beautiful-dnd?)"

  notes:
    - "Use Technical Specs Section 1.2.7 specification"
    - "Jira API: create tickets with POST /rest/api/2/issue"

  memory_keys:
    - "task_history/priority_planner_050"
    - "agent_memory/remediation_lead/action_planner"

  dependencies:
    - "TASK-2025-11-12-040 (mitigations)"
    - "TASK-2025-11-12-020 (scoring)"

  status: "CREATED"
  status_updated: "2025-11-12 07:30:00 UTC"
```

**Assigned Agent**: remediation_strategy_lead (Ruv-Swarm)

---

## Section 7: Agent Coordination Matrix

### Ruv-Swarm Agent Roster (16 Agents)

| Agent Type | Responsibilities | Primary Tasks | Coordination |
|------------|------------------|---------------|--------------|
| **devops_reliability_engineer** | Infrastructure, Docker, Kubernetes, health checks | TASK-001 (infrastructure), TASK-029 (Qdrant debug) | Mesh topology with all agents |
| **data_pipeline_engineer** | NVD API, data ingestion, ETL | TASK-002 (NVD API), TASK-003 (ATT&CK update) | Provides data to kg_engineer |
| **knowledge_graph_engineer** | Neo4j schema, Cypher queries, semantic chains | TASK-005-008 (semantic mappings) | Queen in hierarchical topology |
| **backend_engineer** | FastAPI, API endpoints, job persistence | TASK-010 (jobs), TASK-020-021 (scoring APIs) | Mesh with frontend |
| **ml_engineer** | Bayesian models, Monte Carlo, statistics | TASK-015-016 (AttackChainScorer, Monte Carlo) | Consults external statistician |
| **ml_research_engineer** | GNN architecture, PyTorch Geometric, GPU training | TASK-025 (GNN training) | Requires GPU infrastructure |
| **ml_application_engineer** | GNN inference, prediction APIs | TASK-026 (CWE prediction) | Uses ml_research_engineer models |
| **integration_engineer** | Equipment import, CPE matching, CMDB connectors | TASK-030 (equipment CSV) | Mesh with risk_analyst |
| **risk_analysis_engineer** | Attack surface calculation, heatmaps, PDF reports | TASK-035 (risk heatmap) | Uses integration + backend data |
| **security_operations_engineer** | Mitigations, ATT&CK mappings, vendor advisories | TASK-040 (mitigation engine) | Mesh with detection_lead |
| **detection_engineering_lead** | SIEM rules, Splunk/Sentinel/Sigma, ATT&CK Evals | TASK-045 (rule generation) | Testing with ATT&CK Evals dataset |
| **remediation_strategy_lead** | Priority planner, Jira integration, Kanban UI | TASK-050 (action planner) | Uses all prior agents' outputs |
| **qa_engineer** | Testing, validation, chain completeness | TASK-009 (chain validation) | Quality gates for all phases |
| **frontend_engineer** | Next.js, UI components, Clerk auth | UI tasks (not detailed here) | Mesh with backend_engineer |
| **storage_engineer** | Qdrant, MinIO, database backups | TASK-029 (Qdrant debug) | Infrastructure support |
| **performance_engineer** | Load testing, Locust, optimization | TASK-023 (Neo4j performance) | Optimization across all services |

---

## Section 8: Ruv-Swarm Orchestration

### 8.1 Swarm Initialization

**Command**:
```bash
npx claude-flow@alpha swarm init \
  --topology mesh \
  --max-agents 16 \
  --strategy adaptive \
  --memory-backend qdrant \
  --qdrant-url http://172.18.0.6:6333
```

**Expected Output**:
```
✓ Swarm initialized: swarm-1761951435550
✓ Topology: mesh (16 agents, adaptive strategy)
✓ Memory backend: Qdrant (http://172.18.0.6:6333)
✓ Collections created: agent_memory, task_history
```

---

### 8.2 Agent Spawning (Parallel)

**Spawn All 16 Agents Concurrently**:
```bash
npx claude-flow@alpha agents spawn-parallel \
  --agents '[
    {"type": "researcher", "name": "data_pipeline_engineer"},
    {"type": "coder", "name": "backend_engineer"},
    {"type": "coder", "name": "frontend_engineer"},
    {"type": "analyst", "name": "ml_engineer"},
    {"type": "analyst", "name": "ml_research_engineer"},
    {"type": "analyst", "name": "ml_application_engineer"},
    {"type": "coder", "name": "knowledge_graph_engineer"},
    {"type": "coder", "name": "integration_engineer"},
    {"type": "analyst", "name": "risk_analysis_engineer"},
    {"type": "coder", "name": "security_operations_engineer"},
    {"type": "coder", "name": "detection_engineering_lead"},
    {"type": "analyst", "name": "remediation_strategy_lead"},
    {"type": "tester", "name": "qa_engineer"},
    {"type": "coder", "name": "devops_reliability_engineer"},
    {"type": "coder", "name": "storage_engineer"},
    {"type": "analyst", "name": "performance_engineer"}
  ]' \
  --batch-size 5 \
  --max-concurrency 16
```

**Expected Output** (10-20x faster than sequential):
```
✓ Spawning agents in batches of 5...
✓ Batch 1: data_pipeline_engineer, backend_engineer, frontend_engineer, ml_engineer, ml_research_engineer (3.2s)
✓ Batch 2: ml_application_engineer, knowledge_graph_engineer, integration_engineer, risk_analysis_engineer, security_operations_engineer (2.9s)
✓ Batch 3: detection_engineering_lead, remediation_strategy_lead, qa_engineer, devops_reliability_engineer, storage_engineer (3.1s)
✓ Batch 4: performance_engineer (1.5s)
✓ All 16 agents spawned in 10.7 seconds (vs. 170s sequential = 15.9x speedup)
```

---

### 8.3 Task Orchestration

**Assign Tasks to Agents**:
```bash
npx claude-flow@alpha task orchestrate \
  --task "Execute Phase 1 semantic chain construction" \
  --strategy adaptive \
  --priority critical \
  --max-agents 5
```

**Orchestration Logic**:
1. Analyze task dependencies (TASK-002 → TASK-005 → TASK-006 → TASK-007 → TASK-008 → TASK-009)
2. Assign tasks to agents based on specialization:
   - data_pipeline_engineer: TASK-002
   - knowledge_graph_engineer: TASK-005-008
   - qa_engineer: TASK-009
3. Execute in parallel where possible (TASK-006, TASK-007, TASK-008 can run concurrently)
4. Monitor progress in Qdrant `task_history`

---

## Section 9: Qdrant Memory Integration

### 9.1 Task Storage Schema

**Every TASKMASTER task stored in Qdrant**:
```python
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer

client = QdrantClient(url="http://172.18.0.6:6333")
bert_model = SentenceTransformer('all-MiniLM-L6-v2')

# Store task
task_description = "Build CVE ingestion pipeline with NVD API integration"
task_vector = bert_model.encode(task_description)

client.upsert(
    collection_name="task_history",
    points=[
        PointStruct(
            id=hash("TASK-2025-11-12-002"),
            vector=task_vector.tolist(),
            payload={
                "task_id": "TASK-2025-11-12-002",
                "assigned_to": "data_pipeline_engineer",
                "status": "IN_PROGRESS",
                "priority": "CRITICAL",
                "deadline": "2025-12-10",
                "deliverables": ["NVD API integration script", "Scheduled cron job"],
                "success_criteria": ["Imports ≥ 95% CVEs", "Execution time < 15min"],
                "progress_updates": [
                    {"timestamp": "2025-11-15 10:00:00", "update": "Completed rate limiting logic"},
                    {"timestamp": "2025-11-20 14:30:00", "update": "Tested with 500 CVEs, passed"}
                ]
            }
        )
    ]
)
```

### 9.2 Cross-Agent Memory Sharing

**Agent Query: "What tasks are related to CVE ingestion?"**
```python
results = client.search(
    collection_name="task_history",
    query_vector=bert_model.encode("CVE ingestion NVD API").tolist(),
    limit=5,
    score_threshold=0.7,
    query_filter={
        "must": [
            {"key": "status", "match": {"value": "COMPLETED"}}
        ]
    }
)

for hit in results:
    print(f"Related task: {hit.payload['task_id']}")
    print(f"Assigned to: {hit.payload['assigned_to']}")
    print(f"Deliverables: {hit.payload['deliverables']}")
    print(f"Similarity: {hit.score}")
```

**Output**:
```
Related task: TASK-2025-11-12-002
Assigned to: data_pipeline_engineer
Deliverables: ['NVD API integration script', 'Scheduled cron job']
Similarity: 0.92
```

---

## Section 10: Quality Gates and Validation

### 10.1 Phase-End Quality Gates

**Phase 1 Quality Gate**:
- [ ] Semantic chain completeness ≥ 80%
- [ ] Job reliability: 100% over 30-day period
- [ ] All 7 Docker containers healthy
- [ ] Neo4j query performance: 10-hop queries < 500ms
- [ ] PostgreSQL `jobs` table: zero lost jobs

**Phase 2 Quality Gate**:
- [ ] AttackChainScorer accuracy ≥ 85% on CISA KEV
- [ ] API p99 latency < 2 seconds
- [ ] Monte Carlo CI width reasonable (0.05-0.15)
- [ ] Batch scoring: 1,000 CVEs in < 60 seconds

**Phase 3 Quality Gate**:
- [ ] GNN test set: Precision ≥ 90%, Recall ≥ 85%
- [ ] Missing CWE prediction: analyst approval rate ≥ 80%
- [ ] Multi-hop queries: < 500ms for 10 hops

**Phase 4 Quality Gate**:
- [ ] Equipment auto-match rate ≥ 95%
- [ ] Attack surface calculation: < 10s for 10,000 assets
- [ ] Risk heatmap PDF: board-ready quality

**Phase 5 Quality Gate**:
- [ ] Mitigation coverage ≥ 90%
- [ ] SIEM rule success rate ≥ 80%
- [ ] McKenney's 8 questions: all answerable at 95%+ confidence

---

### 10.2 Continuous Validation

**Daily Automated Tests**:
```bash
#!/bin/bash
# File: scripts/daily_validation.sh

# Semantic chain completeness
echo "Checking semantic chain completeness..."
COMPLETENESS=$(docker exec openspg-neo4j cypher-shell -u neo4j -p ${NEO4J_PASSWORD} \
  "MATCH (c:CVE)-[:HAS_CWE]->(:CWE)-[:MAPS_TO_CAPEC]->(:CAPEC)-[:MAPS_TO_TECHNIQUE]->(:Technique)-[:BELONGS_TO_TACTIC]->(:Tactic) \
   RETURN COUNT(DISTINCT c) AS complete_chains")

if [ "$COMPLETENESS" -lt 8000 ]; then
  echo "❌ ALERT: Chain completeness = $COMPLETENESS (target: 8000)"
  # Send PagerDuty alert
fi

# Job reliability
echo "Checking job reliability..."
FAILED_JOBS=$(docker exec aeon-postgres-dev psql -U postgres -d aeon -tAc \
  "SELECT COUNT(*) FROM jobs WHERE status='failed' AND retries >= max_retries")

if [ "$FAILED_JOBS" -gt 0 ]; then
  echo "❌ ALERT: $FAILED_JOBS lost jobs (target: 0)"
fi

# API health
echo "Checking API health..."
curl -f http://localhost:8000/api/health || echo "❌ ALERT: Backend API down"
curl -f http://localhost:3000/api/health || echo "❌ ALERT: Frontend API down"

echo "✅ Daily validation complete"
```

**Run via cron**:
```
0 4 * * * /home/jim/2_OXOT_Projects_Dev/scripts/daily_validation.sh >> /var/log/aeon/validation.log 2>&1
```

---

**Document Control**:
- **Approved By**: [Pending project manager review]
- **Review Cycle**: Weekly during active development
- **Next Review**: 2025-11-19
- **Change Log**:
  - v1.0.0 (2025-11-12): Initial TASKMASTER implementation plan

**END OF TASKMASTER IMPLEMENTATION PLAN**
