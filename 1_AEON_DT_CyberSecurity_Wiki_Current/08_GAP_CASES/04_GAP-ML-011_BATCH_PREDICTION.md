# GAP-ML-011: Batch Prediction API

**File:** 04_GAP-ML-011_BATCH_PREDICTION.md
**Gap ID:** GAP-ML-011
**Created:** 2025-11-30
**Priority:** HIGH
**Phase:** 1 - Foundation
**Effort:** M (2-4 weeks)
**Status:** NOT STARTED

---

## Problem Statement

**Current State:**
- Single-entity prediction endpoints only
- Inefficient for bulk analysis operations
- No job queue system for long-running predictions
- No result caching mechanism

**Desired State:**
- Batch prediction endpoints for multiple entities
- Async job processing with status tracking
- Result caching for repeated queries
- Efficient bulk operations

---

## Technical Specification

### Batch Endpoint Design

```yaml
# Batch Ising Prediction
POST /api/v1/predict/batch/ising
  Request:
    entity_ids: ["ACTOR-001", "ACTOR-002", ..., "ACTOR-100"]
    prediction_type: "spin_flip_probability"
    parameters:
      temperature: 0.5
      time_horizon: "24h"
  Response:
    job_id: "JOB-2025-001"
    status: "QUEUED"
    estimated_completion: "2025-11-30T15:00:00Z"
    callback_url: "/api/v1/jobs/JOB-2025-001/results"

# Batch Granovetter Cascade
POST /api/v1/predict/batch/cascade
  Request:
    seed_entities: ["ACTOR-001", "ACTOR-005"]
    max_generations: 5
    threshold_distribution: "uniform"
  Response:
    job_id: "JOB-2025-002"
    status: "QUEUED"

# Batch EWS Analysis
POST /api/v1/predict/batch/ews
  Request:
    entity_ids: ["ACTOR-001", "ACTOR-002", ...]
    metrics: ["variance", "autocorrelation", "critical_distance"]
    time_window: "7d"
  Response:
    job_id: "JOB-2025-003"
    status: "QUEUED"

# Job Status
GET /api/v1/jobs/{job_id}
  Response:
    job_id: "JOB-2025-001"
    status: "PROCESSING" | "COMPLETED" | "FAILED"
    progress: 0.45
    results_ready: false
    created_at: "..."
    updated_at: "..."

# Job Results
GET /api/v1/jobs/{job_id}/results
  Response:
    job_id: "JOB-2025-001"
    status: "COMPLETED"
    results: [
      { entity_id: "ACTOR-001", prediction: {...} },
      { entity_id: "ACTOR-002", prediction: {...} }
    ]
    metadata:
      total_entities: 100
      successful: 98
      failed: 2
      execution_time_ms: 4500
```

### Job Queue Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Batch Prediction System                   │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐         ┌──────────────┐                 │
│  │  API Server  │────────▶│  Redis Queue │                 │
│  │  (FastAPI)   │         │  (Job Queue) │                 │
│  └──────────────┘         └──────┬───────┘                 │
│                                  │                          │
│         ┌────────────────────────┼────────────────────┐    │
│         │                        │                    │    │
│  ┌──────▼───────┐   ┌──────▼───────┐   ┌──────▼───────┐  │
│  │ Worker 1     │   │ Worker 2     │   │ Worker N     │  │
│  │ (Celery)     │   │ (Celery)     │   │ (Celery)     │  │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘  │
│         │                  │                  │          │
│         └──────────────────┼──────────────────┘          │
│                            │                              │
│                     ┌──────▼───────┐                     │
│                     │  Neo4j       │                     │
│                     │  (Queries)   │                     │
│                     └──────────────┘                     │
│                            │                              │
│                     ┌──────▼───────┐                     │
│                     │  Redis Cache │                     │
│                     │  (Results)   │                     │
│                     └──────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

### Caching Strategy

```python
# Cache key format
cache_key = f"prediction:{prediction_type}:{hash(entity_ids)}:{hash(parameters)}"

# Cache TTL by prediction type
CACHE_TTL = {
    "ising": 3600,        # 1 hour (relatively stable)
    "cascade": 1800,      # 30 min (changes with network)
    "ews": 900,           # 15 min (time-sensitive)
    "bifurcation": 300    # 5 min (highly dynamic)
}

# Cache invalidation triggers
- Entity property update
- New relationship created
- EWS threshold breach
- Manual invalidation
```

---

## Implementation Steps

### Step 1: Infrastructure (Week 1)
- [ ] Set up Redis for job queue
- [ ] Set up Celery workers
- [ ] Create job tracking database tables
- [ ] Implement job status API

### Step 2: Batch Endpoints (Week 2)
- [ ] Create `/predict/batch/ising` endpoint
- [ ] Create `/predict/batch/cascade` endpoint
- [ ] Create `/predict/batch/ews` endpoint
- [ ] Create `/jobs/{id}` and `/jobs/{id}/results` endpoints

### Step 3: Worker Implementation (Week 3)
- [ ] Implement Ising batch worker
- [ ] Implement Cascade batch worker
- [ ] Implement EWS batch worker
- [ ] Add error handling and retry logic

### Step 4: Caching & Optimization (Week 4)
- [ ] Implement Redis caching layer
- [ ] Add cache invalidation triggers
- [ ] Performance testing and tuning
- [ ] Documentation

---

## Success Criteria

- [ ] Batch endpoints accept up to 1000 entities
- [ ] Job queue processes 100 predictions/minute
- [ ] Cache hit rate >70% for repeated queries
- [ ] API response time <200ms for job submission
- [ ] Worker failure recovery operational

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Queue backlog | Medium | Medium | Auto-scaling workers, priority queues |
| Cache staleness | Medium | Low | Aggressive TTL, invalidation triggers |
| Neo4j overload | High | Medium | Connection pooling, query optimization |

---

## Dependencies

- Redis infrastructure
- Celery installed
- Neo4j connection pool

---

## Memory Keys

- `gap-ml-011-design`: Architecture decisions
- `gap-ml-011-progress`: Implementation progress

---

## References

- API Spec: `mckenney-lacan-calculus-2025-11-28/neo4j-schema/04_MCKENNEY_LACAN_UNIFIED_API.yaml`
