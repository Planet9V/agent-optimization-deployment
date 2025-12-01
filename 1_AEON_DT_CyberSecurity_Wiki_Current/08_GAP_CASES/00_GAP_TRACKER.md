# McKenney-Lacan Foundation Gaps - Master Tracker

**File:** 00_GAP_TRACKER.md
**Created:** 2025-11-30
**Purpose:** Track progress on 12 critical McKenney-Lacan Calculus foundation gaps
**Status:** ACTIVE - TASKMASTER DOCUMENT

---

## Executive Summary

**Total Gaps:** 12 Critical + Medium-Priority Foundation Gaps
**Estimated Duration:** 28 weeks (phased implementation)
**Current Phase:** Phase 1 - Foundation (Weeks 1-4)

### Quick Status

| Gap ID | Name | Priority | Phase | Status | Effort |
|--------|------|----------|-------|--------|--------|
| GAP-ML-001 | Loman Operator L-gGNN | CRITICAL | 2 | NOT STARTED | XL |
| GAP-ML-002 | Dynamic CB5T Parameters | CRITICAL | 2 | NOT STARTED | L |
| GAP-ML-003 | NER11 Gold Pipeline | CRITICAL | 3 | IN PROGRESS | XL |
| GAP-ML-004 | Temporal Versioning | CRITICAL | 1 | NOT STARTED | L |
| GAP-ML-005 | WebSocket EWS Streaming | CRITICAL | 1 | NOT STARTED | L |
| GAP-ML-006 | True Autocorrelation | HIGH | 2 | NOT STARTED | M |
| GAP-ML-007 | Multi-R0 Ensemble | HIGH | 2 | NOT STARTED | M |
| GAP-ML-008 | Demographic Data | HIGH | 3 | NOT STARTED | XL |
| GAP-ML-009 | Economic Indicators | HIGH | 3 | NOT STARTED | L |
| GAP-ML-010 | Cascade Event Tracking | HIGH | 1 | NOT STARTED | M |
| GAP-ML-011 | Batch Prediction API | HIGH | 1 | NOT STARTED | M |
| GAP-ML-012 | Backtesting Framework | HIGH | 4 | NOT STARTED | XL |

---

## Phase Breakdown

### PHASE 1: Foundation (Weeks 1-4) - START HERE
| Gap | Case File | Dependencies | Deliverables |
|-----|-----------|--------------|--------------|
| GAP-ML-004 | `01_GAP-ML-004_TEMPORAL_VERSIONING.md` | Neo4j schema | Event sourcing, point-in-time queries |
| GAP-ML-005 | `02_GAP-ML-005_WEBSOCKET_EWS.md` | Neo4j triggers | Real-time alerts, sub-second detection |
| GAP-ML-010 | `03_GAP-ML-010_CASCADE_TRACKING.md` | Neo4j schema | CASCADE_EVENT nodes, genealogy |
| GAP-ML-011 | `04_GAP-ML-011_BATCH_PREDICTION.md` | API infrastructure | Batch endpoints, job queue |

### PHASE 2: Core Math (Weeks 5-12)
| Gap | Case File | Dependencies | Deliverables |
|-----|-----------|--------------|--------------|
| GAP-ML-001 | `05_GAP-ML-001_LOMAN_OPERATOR.md` | GPU, training data | L-gGNN PyTorch model |
| GAP-ML-002 | `06_GAP-ML-002_DYNAMIC_CB5T.md` | Phase 1 complete | Real-time psychometric updates |
| GAP-ML-006 | `07_GAP-ML-006_AUTOCORRELATION.md` | TimescaleDB | Rolling ACF/PACF computation |
| GAP-ML-007 | `08_GAP-ML-007_MULTI_R0.md` | Phase 1 complete | Vectorized R0, ensemble |

### PHASE 3: Data Integration (Weeks 13-20)
| Gap | Case File | Dependencies | Deliverables |
|-----|-----------|--------------|--------------|
| GAP-ML-003 | `09_GAP-ML-003_NER11_PIPELINE.md` | NER11 Gold model | Streaming ingestion, entity resolution |
| GAP-ML-008 | `10_GAP-ML-008_DEMOGRAPHIC_DATA.md` | Data agreements | Census/polling integration |
| GAP-ML-009 | `11_GAP-ML-009_ECONOMIC_INDICATORS.md` | API keys | Market data feeds |

### PHASE 4: Validation (Weeks 21-28)
| Gap | Case File | Dependencies | Deliverables |
|-----|-----------|--------------|--------------|
| GAP-ML-012 | `12_GAP-ML-012_BACKTESTING.md` | Historical data | Validation framework |

---

## Memory Keys (Qdrant)

| Key | Namespace | Purpose |
|-----|-----------|---------|
| `aeon-architecture-complete` | aeon-research | Full platform architecture |
| `mckenney-lacan-research-complete` | aeon-research | Schema, queries, API spec |
| `aeon-project-status-2025-11-30` | aeon-research | Current status snapshot |
| `gap-tracker-state` | aeon-research | This tracker's current state |

---

## Dependency Notes

### NER11 Gold Status
- **Model:** Trained, high accuracy (566+ entity types)
- **Pipeline:** NOT COMPLETE - requires streaming ingestion
- **Blocker for:** GAP-ML-003 (full pipeline), data loading
- **Recommendation:** Complete NER11 pipeline before loading historical data

### Frontend (DO NOT TOUCH)
- **aeon-saas-dev:** Next.js 14+ with Clerk auth
- **aeon-postgres-dev:** PostgreSQL for app state
- **Status:** OPERATIONAL - No modifications needed for gap work

---

## Progress Log

### 2025-11-30
- Created master tracker
- Created 12 individual case files
- Stored architecture to Qdrant memory (ID: 97)
- Git commit pending

---

## How to Use This Tracker

1. **Select a Gap:** Choose from Phase 1 first
2. **Read Case File:** Full specification in `08_GAP_CASES/`
3. **Update Status:** Mark IN PROGRESS when starting
4. **Store Decisions:** Use Qdrant memory for all decisions
5. **Mark Complete:** Only when deliverables verified
6. **Update Tracker:** Maintain this file current

---

**Next Action:** Start with GAP-ML-004 (Temporal Versioning) or GAP-ML-005 (WebSocket EWS)
