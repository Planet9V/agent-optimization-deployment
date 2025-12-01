# AEON Cyber Digital Twin - McKenney-Lacan Foundation TASKMASTER

**File:** 00_COMPREHENSIVE_TASKMASTER.md
**Created:** 2025-11-30
**Version:** 1.0.0
**Purpose:** Complete implementation guide for 12 McKenney-Lacan foundation gaps
**Session Continuity:** Reference this file + Qdrant memory ID 98 (gap-tracker-state)

---

## Executive Summary

This TASKMASTER covers all 12 gaps required to complete the McKenney-Lacan Calculus integration into AEON Cyber Digital Twin. The implementation supports J. McKenney's vision of psychohistory-based cybersecurity prediction and prepares for the NER11 Gold keystone.

### Architecture Reference
- **Neo4j:** 172.18.0.5:7687 (aeon-neo4j-dev)
- **PostgreSQL:** 172.18.0.4:5432 (aeon-postgres-dev)
- **Qdrant:** 172.18.0.6:6333 (aeon-qdrant-dev)
- **SaaS Backend:** aeon-saas-dev

### CRITICAL RULES FOR ALL IMPLEMENTATIONS
```yaml
NO_THEATRE_RULES:
  - DO NOT create new schemas if existing schema covers requirements
  - DO NOT reimplement queries that exist in Cypher library
  - DO NOT add indexes that duplicate existing indexes
  - ALWAYS check 01_MCKENNEY_LACAN_NEO4J_SCHEMA.cypher first
  - ALWAYS check 02_MCKENNEY_LACAN_CYPHER_LIBRARY.cypher for existing queries
  - ALWAYS use existing GDS graph projections
  - AUDITOR REQUIRED for each task to verify compliance
```

---

## Phase Execution Order

```
PHASE 1 (Foundation) → PHASE 2 (Core Math) → PHASE 3 (Data Integration) → PHASE 4 (Validation)
     ↓                      ↓                       ↓                          ↓
[ML-004, ML-005,      [ML-001, ML-002,        [ML-003, ML-008,          [ML-012]
 ML-010, ML-011]       ML-006, ML-007]         ML-009]
```

---

## EXISTING COMPONENTS INVENTORY (USE THESE - NO THEATRE)

### Neo4j Schema Assets (01_MCKENNEY_LACAN_NEO4J_SCHEMA.cypher)

#### Constraints (ALREADY EXIST - DO NOT RECREATE)
```cypher
-- Primary Key Constraints
actor_id_unique, asset_id_unique, concept_id_unique, event_id_unique,
group_id_unique, vulnerability_id_unique, threat_actor_id_unique

-- Already support: Actor, Asset, Concept, Event, Group, Vulnerability, ThreatActor
```

#### Indexes (ALREADY EXIST - DO NOT RECREATE)
```cypher
-- Performance Indexes - Ising Model (Lines 24-28)
actor_spin_idx, actor_threshold_idx, actor_volatility_idx,
actor_external_field_idx

-- EWS Indexes (Lines 31-34) - CRITICAL FOR GAP-ML-005
actor_ews_variance_idx, actor_ews_autocorr_idx,
actor_ews_critical_distance_idx

-- Psychometric Indexes (Lines 37-40)
actor_disc_d_idx, actor_disc_i_idx, actor_ocean_o_idx,
actor_ocean_n_idx

-- Cascade Indexes (Lines 43-45)
actor_cascade_gen_idx, actor_cascade_active_idx

-- Lacanian Indexes (Lines 48-49)
actor_lacan_real_idx, actor_lacan_symbolic_idx
```

#### GDS Graph Projections (ALREADY EXIST - USE THESE)
```cypher
-- social_network projection (Lines 52-59) - USE FOR Ising simulations
-- influence_network projection (Lines 61-71) - USE FOR cascade analysis
-- cyber_network projection (Lines 73-85) - USE FOR vulnerability propagation
```

### Cypher Library Assets (02_MCKENNEY_LACAN_CYPHER_LIBRARY.cypher)

#### Ising Model Queries (USE THESE - Lines 22-127)
- `ISING_HAMILTONIAN_TOTAL` - Calculate system energy
- `ISING_MAGNETIZATION` - Calculate system magnetization
- `ISING_LOCAL_FIELD` - Calculate local field for entity
- `ISING_FLIP_CANDIDATES` - Find entities likely to flip
- `ISING_SPIN_FLIP_PROBABILITY` - Calculate flip probability
- `ISING_UPDATE_SPINS_BATCH` - Batch update spins

#### Granovetter Cascade Queries (USE THESE - Lines 130-220)
- `GRANOVETTER_ACTIVATION_CHECK` - Check if entity activates
- `GRANOVETTER_CASCADE_STEP` - Execute one cascade step
- `GRANOVETTER_CASCADE_BLOCKERS` - Find cascade blockers
- `GRANOVETTER_THRESHOLD_DISTRIBUTION` - Get threshold distribution

#### Critical Slowing Down EWS (USE THESE - Lines 223-310)
- `EWS_VARIANCE_ROLLING` - Calculate rolling variance
- `EWS_AUTOCORRELATION_LAG1` - Calculate lag-1 autocorrelation
- `EWS_CRITICAL_DISTANCE` - Calculate distance to bifurcation
- `SELDON_CRISIS_DETECTOR` - Psychohistory status check

#### Bifurcation Theory (USE THESE - Lines 313-380)
- `BIFURCATION_DETECT` - Detect approaching bifurcation
- `BIFURCATION_PARAMETER_SWEEP` - Parameter space exploration

#### Epidemic R0 (USE THESE - Lines 383-450)
- `R0_BASIC_CALCULATION` - Calculate basic R0
- `R0_NETWORK_ADJUSTED` - Network-adjusted R0
- `R0_SPECTRAL` - Spectral R0 using eigenvalue

#### Psychometric Tensor (USE THESE - Lines 453-520)
- `PSYCHOMETRIC_TENSOR_CONSTRUCT` - Build tensor from DISC×OCEAN
- `CB5T_DERIVED_PARAMETERS` - Calculate stability/plasticity

---

## PHASE 1: FOUNDATION (Weeks 1-6)

### GAP-ML-004: Temporal Versioning
**Priority:** CRITICAL | **Effort:** L (4-6 weeks) | **Status:** NOT STARTED

#### Purpose
Enable event sourcing for all Neo4j nodes to support McKenney-Lacan temporal analysis.

#### EXISTING COMPONENTS TO USE
```yaml
use_existing:
  - All node type constraints (already exist)
  - actor_id_unique, asset_id_unique, etc.

do_not_duplicate:
  - Do NOT recreate constraints
  - Do NOT add redundant indexes
```

#### Implementation Tasks
```yaml
task_1:
  name: "Add temporal properties to existing node types"
  cypher: |
    // ADD to existing Actor nodes - DO NOT CREATE NEW TYPE
    MATCH (a:Actor)
    SET a.valid_from = COALESCE(a.valid_from, datetime()),
        a.valid_to = COALESCE(a.valid_to, datetime('9999-12-31')),
        a.version = COALESCE(a.version, 1),
        a.change_source = COALESCE(a.change_source, 'INITIAL'),
        a.change_actor = COALESCE(a.change_actor, 'SYSTEM')
  auditor_check:
    - "Verify no new node types created"
    - "Verify properties added to existing nodes"
    - "Verify valid_from defaults correct"

task_2:
  name: "Create temporal indexes"
  cypher: |
    CREATE INDEX actor_valid_from_idx IF NOT EXISTS FOR (a:Actor) ON (a.valid_from);
    CREATE INDEX actor_valid_to_idx IF NOT EXISTS FOR (a:Actor) ON (a.valid_to);
    CREATE INDEX actor_version_idx IF NOT EXISTS FOR (a:Actor) ON (a.version);
  auditor_check:
    - "Verify indexes created successfully"
    - "Verify no duplicate indexes exist"

task_3:
  name: "Create version creation procedure"
  implementation: "Create APOC procedure using existing APOC patterns from library"
  auditor_check:
    - "Verify uses APOC batch processing pattern from library (Line 580+)"
    - "Verify transaction handling correct"

task_4:
  name: "Create point-in-time query functions"
  implementation: "Add to Cypher library - follow existing function patterns"
  auditor_check:
    - "Verify follows library naming convention"
    - "Verify documentation format matches library"
```

#### Success Criteria
- [ ] All node types have temporal properties
- [ ] Version history queryable
- [ ] Point-in-time snapshots work
- [ ] No duplicate constraints/indexes

---

### GAP-ML-005: WebSocket EWS Streaming
**Priority:** CRITICAL | **Effort:** L (4-6 weeks) | **Status:** NOT STARTED

#### Purpose
Real-time streaming of Early Warning Signals for crisis detection.

#### EXISTING COMPONENTS TO USE
```yaml
use_existing:
  # EWS Indexes (already exist - Line 31-34 of schema)
  - actor_ews_variance_idx
  - actor_ews_autocorr_idx
  - actor_ews_critical_distance_idx

  # EWS Queries (already exist - Line 223-310 of library)
  - EWS_VARIANCE_ROLLING
  - EWS_AUTOCORRELATION_LAG1
  - EWS_CRITICAL_DISTANCE
  - SELDON_CRISIS_DETECTOR
```

#### Implementation Tasks
```yaml
task_1:
  name: "WebSocket Server Setup"
  location: "aeon-saas-dev backend"
  implementation: |
    // Use Socket.io with existing Express server
    // DO NOT create separate service if backend already has WS support
  auditor_check:
    - "Verify integrates with existing aeon-saas-dev"
    - "Verify uses existing auth middleware"

task_2:
  name: "EWS Threshold Query (USE EXISTING)"
  cypher: |
    // USE EXISTING SELDON_CRISIS_DETECTOR from library (Line 298-310)
    // DO NOT reimplement - just wrap for WebSocket
  auditor_check:
    - "Verify uses SELDON_CRISIS_DETECTOR verbatim"
    - "Verify no duplicate query created"

task_3:
  name: "CDC/Trigger Integration"
  implementation: |
    // Use Neo4j APOC triggers
    CALL apoc.trigger.add('ews_alert',
      "UNWIND $createdNodes AS n
       WITH n WHERE n.ews_critical_distance < 0.2
       // Publish to message queue",
      {phase: 'after'})
  auditor_check:
    - "Verify uses APOC trigger pattern"
    - "Verify threshold matches library constant"

task_4:
  name: "Integration Endpoints"
  endpoints:
    - "GET /api/v1/ews/status"
    - "POST /api/v1/ews/subscribe"
    - "WS ws://api/v1/ews/stream"
  auditor_check:
    - "Verify follows existing API patterns"
    - "Verify uses existing auth"
```

#### Success Criteria
- [ ] WebSocket streaming operational
- [ ] Uses existing EWS queries from library
- [ ] <1 second alert latency
- [ ] No duplicate queries created

---

### GAP-ML-010: Cascade Event Tracking
**Priority:** HIGH | **Effort:** M (2-4 weeks) | **Status:** NOT STARTED

#### Purpose
Track cascade genealogy and propagation metrics.

#### EXISTING COMPONENTS TO USE
```yaml
use_existing:
  # Cascade indexes (already exist - Line 43-45 of schema)
  - actor_cascade_gen_idx
  - actor_cascade_active_idx

  # Cascade queries (already exist - Line 130-220 of library)
  - GRANOVETTER_ACTIVATION_CHECK
  - GRANOVETTER_CASCADE_STEP
  - GRANOVETTER_CASCADE_BLOCKERS

  # GDS projections (already exist)
  - influence_network projection
```

#### Implementation Tasks
```yaml
task_1:
  name: "Create CascadeEvent Node Type"
  cypher: |
    // NEW node type required - not duplicating existing
    CREATE CONSTRAINT cascade_event_id_unique IF NOT EXISTS
    FOR (ce:CascadeEvent) REQUIRE ce.id IS UNIQUE;

    CREATE INDEX cascade_event_generation_idx IF NOT EXISTS
    FOR (ce:CascadeEvent) ON (ce.generation);
  auditor_check:
    - "Verify CascadeEvent doesn't duplicate Event"
    - "Verify constraint naming follows pattern"

task_2:
  name: "Create TRIGGERED relationship"
  cypher: |
    // New relationship for cascade genealogy
    // (parent:CascadeEvent)-[:TRIGGERED]->(child:CascadeEvent)
  auditor_check:
    - "Verify doesn't duplicate existing relationships"

task_3:
  name: "Cascade Tracking Procedures"
  implementation: |
    // USE existing GRANOVETTER queries as foundation
    // Add generation tracking on top
  auditor_check:
    - "Verify uses GRANOVETTER_CASCADE_STEP"
    - "Verify uses existing influence_network projection"

task_4:
  name: "Add Cascade Queries to Library"
  queries:
    - "CASCADE_TREE_QUERY"
    - "CASCADE_VELOCITY_CALC"
    - "CASCADE_CONTAINMENT_ANALYSIS"
  auditor_check:
    - "Verify added to existing Cypher library"
    - "Verify follows library documentation format"
```

#### Success Criteria
- [ ] CascadeEvent nodes track genealogy
- [ ] Uses existing Granovetter queries
- [ ] Velocity/acceleration metrics work
- [ ] Query performance <100ms

---

### GAP-ML-011: Batch Prediction API
**Priority:** HIGH | **Effort:** M (2-4 weeks) | **Status:** NOT STARTED

#### Purpose
Enable batch predictions for multiple entities efficiently.

#### EXISTING COMPONENTS TO USE
```yaml
use_existing:
  # Batch processing patterns (Line 580+ of library)
  - APOC batch processing patterns

  # Prediction queries (already exist in library)
  - ISING_FLIP_CANDIDATES (batch compatible)
  - ISING_UPDATE_SPINS_BATCH
  - EWS queries (all batch compatible)
```

#### Implementation Tasks
```yaml
task_1:
  name: "Job Queue Infrastructure"
  implementation: |
    // Redis + Celery on existing infrastructure
    // DO NOT create new services if Redis exists
  auditor_check:
    - "Verify uses existing Redis if available"
    - "Verify integrates with aeon-saas-dev"

task_2:
  name: "Batch Ising Endpoint"
  endpoint: "POST /api/v1/predict/batch/ising"
  implementation: |
    // USE ISING_FLIP_CANDIDATES query
    // USE APOC batch processing pattern
    CALL apoc.periodic.iterate(
      "UNWIND $entity_ids AS id MATCH (a:Actor {id: id}) RETURN a",
      "// Use ISING_SPIN_FLIP_PROBABILITY",
      {batchSize: 100, parallel: true}
    )
  auditor_check:
    - "Verify uses ISING_SPIN_FLIP_PROBABILITY from library"
    - "Verify uses APOC batch pattern"

task_3:
  name: "Batch EWS Endpoint"
  endpoint: "POST /api/v1/predict/batch/ews"
  auditor_check:
    - "Verify uses EWS queries from library"
    - "Verify batch size appropriate"

task_4:
  name: "Job Status Endpoints"
  endpoints:
    - "GET /api/v1/jobs/{job_id}"
    - "GET /api/v1/jobs/{job_id}/results"
  auditor_check:
    - "Verify follows REST conventions"
    - "Verify status tracking works"
```

#### Success Criteria
- [ ] Batch endpoints handle 1000 entities
- [ ] Uses existing Cypher queries
- [ ] Job queue processes efficiently
- [ ] No duplicate query implementations

---

## PHASE 2: CORE MATH (Weeks 7-12)

### GAP-ML-001: Loman Operator (L-gGNN)
**Priority:** CRITICAL | **Effort:** XL (8+ weeks) | **Status:** NOT STARTED

#### Purpose
Implement Lacanian Gated Graph Neural Network with CB5T parameters.

#### EXISTING COMPONENTS TO USE
```yaml
use_existing:
  # Psychometric indexes (already exist)
  - actor_disc_d_idx, actor_disc_i_idx
  - actor_ocean_o_idx, actor_ocean_n_idx

  # Lacanian indexes (already exist)
  - actor_lacan_real_idx, actor_lacan_symbolic_idx

  # CB5T queries (already exist - Line 453-520)
  - PSYCHOMETRIC_TENSOR_CONSTRUCT
  - CB5T_DERIVED_PARAMETERS

  # GDS projections for message passing
  - social_network, influence_network
```

#### Implementation Tasks
```yaml
task_1:
  name: "LacanianGRUCell PyTorch Implementation"
  location: "aeon-saas-dev/ml/models/"
  code_structure: |
    class LacanianGRUCell(nn.Module):
        # CB5T → GRU gate biases
        # USE CB5T_DERIVED_PARAMETERS query to fetch parameters
  auditor_check:
    - "Verify fetches CB5T from Neo4j"
    - "Verify uses existing CB5T_DERIVED_PARAMETERS query"

task_2:
  name: "L-gGNN Layer Implementation"
  dependencies: ["task_1"]
  implementation: |
    class LomanOperatorLayer(MessagePassing):
        # USE existing GDS projections for graph structure
        # USE PSYCHOMETRIC_TENSOR_CONSTRUCT for features
  auditor_check:
    - "Verify uses GDS graph export"
    - "Verify uses existing psychometric queries"

task_3:
  name: "Neo4j Integration Layer"
  implementation: |
    // Export graph to PyTorch using GDS
    CALL gds.graph.nodeProperties.stream('social_network', ['spin', 'threshold', 'disc_d', 'ocean_o'])
  auditor_check:
    - "Verify uses existing GDS projection"
    - "Verify property export efficient"

task_4:
  name: "Training Pipeline"
  implementation: "Standard PyTorch training with Neo4j data export"
  auditor_check:
    - "Verify data pipeline uses existing indexes"
    - "Verify batch loading efficient"
```

#### Mathematical Foundation (From Schema)
```python
# CB5T → GRU Gate Biases (DO NOT CHANGE - from theory)
bias_reset = O * SCALING_FACTOR_O      # Openness → Reset gate (plasticity)
bias_update = (C * SCALING_C) - (N * SCALING_N)  # Stability - Neuroticism
bias_new = (E * SCALING_E) + (A * SCALING_A)     # Social engagement
```

#### Success Criteria
- [ ] L-gGNN training on Neo4j data
- [ ] Uses existing CB5T queries
- [ ] Uses existing GDS projections
- [ ] No duplicate psychometric calculations

---

### GAP-ML-002: Dynamic CB5T Parameters
**Priority:** CRITICAL | **Effort:** L (4-6 weeks) | **Status:** NOT STARTED

#### Purpose
Enable psychometric parameter updates from behavioral signals.

#### EXISTING COMPONENTS TO USE
```yaml
use_existing:
  # Psychometric indexes (already exist)
  - All DISC and OCEAN indexes
  - All Lacanian indexes

  # Psychometric queries (already exist)
  - PSYCHOMETRIC_TENSOR_CONSTRUCT
  - CB5T_DERIVED_PARAMETERS
```

#### Implementation Tasks
```yaml
task_1:
  name: "Add History Properties to Actor"
  cypher: |
    // ADD to existing Actor nodes - DO NOT CREATE NEW TYPE
    MATCH (a:Actor)
    SET a.disc_history = COALESCE(a.disc_history, '[]'),
        a.ocean_history = COALESCE(a.ocean_history, '[]'),
        a.lacan_history = COALESCE(a.lacan_history, '[]'),
        a.psychometric_last_update = datetime()
  auditor_check:
    - "Verify added to existing Actor"
    - "Verify defaults correct"

task_2:
  name: "Create Update Triggers"
  implementation: |
    // APOC trigger for incident participation
    CALL apoc.trigger.add('psychometric_incident_update',
      "MATCH (a:Actor)-[:PARTICIPATED_IN]->(e:Event)
       WHERE e.severity = 'CRITICAL'
       // Update Lacanian registers",
      {phase: 'after'})
  auditor_check:
    - "Verify uses APOC trigger pattern"
    - "Verify update formula from spec"

task_3:
  name: "Drift/Decay Model Implementation"
  implementation: |
    // Python function for Bayesian update
    // Stability parameter controls change rate
  auditor_check:
    - "Verify formula matches spec"
    - "Verify bounds enforced [0,1]"

task_4:
  name: "Integration APIs"
  endpoints:
    - "POST /api/v1/actors/{id}/psychometric/update"
    - "GET /api/v1/actors/{id}/psychometric/history"
  auditor_check:
    - "Verify follows REST conventions"
    - "Verify returns history correctly"
```

#### Success Criteria
- [ ] Psychometric values update from signals
- [ ] History tracking works
- [ ] Uses existing indexes
- [ ] No duplicate queries created

---

### GAP-ML-006: True Autocorrelation
**Priority:** HIGH | **Effort:** M (2-4 weeks) | **Status:** NOT STARTED

#### Purpose
Implement proper lag-1 autocorrelation for EWS detection.

#### EXISTING COMPONENTS TO USE
```yaml
use_existing:
  # EWS indexes (already exist)
  - actor_ews_variance_idx
  - actor_ews_autocorr_idx

  # EWS queries - EXTEND, don't replace
  - EWS_AUTOCORRELATION_LAG1 (improve this)
```

#### Implementation Tasks
```yaml
task_1:
  name: "Enhance EWS_AUTOCORRELATION_LAG1"
  implementation: |
    // IMPROVE existing query, don't create duplicate
    // Add to library as EWS_AUTOCORRELATION_LAG1_V2
  auditor_check:
    - "Verify extends existing query"
    - "Verify doesn't duplicate"

task_2:
  name: "Add Rolling Window Support"
  cypher: |
    // Use APOC for time-series operations
    // Window-based autocorrelation calculation
  auditor_check:
    - "Verify uses APOC patterns"
    - "Verify window size configurable"
```

#### Success Criteria
- [ ] True lag-1 autocorrelation
- [ ] Rolling window support
- [ ] Extends existing EWS queries

---

### GAP-ML-007: Multi-R0 Ensemble
**Priority:** HIGH | **Effort:** M (2-4 weeks) | **Status:** NOT STARTED

#### Purpose
Ensemble of R0 calculations for robust epidemic threshold estimation.

#### EXISTING COMPONENTS TO USE
```yaml
use_existing:
  # R0 queries (already exist - Line 383-450)
  - R0_BASIC_CALCULATION
  - R0_NETWORK_ADJUSTED
  - R0_SPECTRAL

  # GDS projections
  - cyber_network (for vulnerability propagation)
```

#### Implementation Tasks
```yaml
task_1:
  name: "Create Ensemble Query"
  implementation: |
    // COMBINE existing R0 queries
    // DO NOT reimplement individual R0 calculations
    WITH basic_r0, network_r0, spectral_r0
    RETURN {
      basic: basic_r0,
      network_adjusted: network_r0,
      spectral: spectral_r0,
      ensemble: (basic_r0 + network_r0 + spectral_r0) / 3,
      confidence_interval: [min, max]
    }
  auditor_check:
    - "Verify uses all three existing R0 queries"
    - "Verify doesn't duplicate calculations"
```

#### Success Criteria
- [ ] Ensemble combines existing R0 methods
- [ ] Confidence intervals provided
- [ ] No duplicate R0 implementations

---

## PHASE 3: DATA INTEGRATION (Weeks 13-20)

### GAP-ML-003: NER11 Gold Pipeline
**Priority:** CRITICAL | **Effort:** XL (8+ weeks) | **Status:** IN PROGRESS

#### Purpose
Streaming ingestion from threat feeds with automatic entity resolution.

#### EXISTING COMPONENTS TO USE
```yaml
use_existing:
  # All node type constraints (for entity creation)
  # All indexes (for entity lookup)
  # NER11 model (already trained)
```

#### Implementation Tasks
```yaml
task_1:
  name: "Kafka Infrastructure"
  topics: ["raw_docs", "entities", "graph_updates"]
  auditor_check:
    - "Verify integrates with existing infrastructure"

task_2:
  name: "Entity Resolution with Qdrant"
  implementation: |
    // Use existing Qdrant at 172.18.0.6:6333
    // Create collections per entity type
  auditor_check:
    - "Verify uses existing Qdrant"
    - "Verify collection naming consistent"

task_3:
  name: "Neo4j MERGE Operations"
  implementation: |
    // Use MERGE to avoid duplicates
    // Follow existing constraint patterns
    MERGE (a:Actor {id: $entity_id})
    ON CREATE SET a += $properties
    ON MATCH SET a.last_seen = datetime()
  auditor_check:
    - "Verify uses MERGE correctly"
    - "Verify respects existing constraints"
```

#### Success Criteria
- [ ] Pipeline processes 100+ docs/hour
- [ ] Entity resolution >90% accuracy
- [ ] Uses existing Neo4j schema

---

### GAP-ML-008: Demographic Data Integration
**Priority:** HIGH | **Effort:** XL (8+ weeks) | **Status:** NOT STARTED

#### Purpose
Population-scale Ising simulations using census/demographic data.

#### EXISTING COMPONENTS TO USE
```yaml
use_existing:
  # Ising queries (for simulations)
  - ISING_HAMILTONIAN_TOTAL
  - ISING_MAGNETIZATION
  - ISING_UPDATE_SPINS_BATCH

  # GDS projections
  - social_network (extend for regions)
```

#### Implementation Tasks
```yaml
task_1:
  name: "Create Region Node Type"
  cypher: |
    CREATE CONSTRAINT region_id_unique IF NOT EXISTS
    FOR (r:Region) REQUIRE r.id IS UNIQUE;
  auditor_check:
    - "Verify follows naming convention"
    - "Verify doesn't duplicate existing types"

task_2:
  name: "Population Ising Simulation"
  implementation: |
    // REUSE existing ISING queries
    // Just change node type filter
  auditor_check:
    - "Verify uses existing Ising queries"
    - "Verify doesn't duplicate Hamiltonian calculation"
```

#### Success Criteria
- [ ] Regional data loaded
- [ ] Uses existing Ising queries
- [ ] Population simulations work

---

### GAP-ML-009: Economic Indicators Integration
**Priority:** HIGH | **Effort:** L (4-6 weeks) | **Status:** NOT STARTED

#### Purpose
Economic bifurcation detection using EWS metrics.

#### EXISTING COMPONENTS TO USE
```yaml
use_existing:
  # EWS queries (for economic indicators)
  - EWS_VARIANCE_ROLLING
  - EWS_CRITICAL_DISTANCE
  - SELDON_CRISIS_DETECTOR

  # Bifurcation queries
  - BIFURCATION_DETECT
```

#### Implementation Tasks
```yaml
task_1:
  name: "Create EconomicIndicator Node Type"
  cypher: |
    CREATE CONSTRAINT economic_indicator_id_unique IF NOT EXISTS
    FOR (ei:EconomicIndicator) REQUIRE ei.id IS UNIQUE;
  auditor_check:
    - "Verify follows naming convention"

task_2:
  name: "Recession Probability Model"
  implementation: |
    // REUSE EWS queries for economic indicators
    // Apply same bifurcation detection logic
  auditor_check:
    - "Verify uses existing EWS queries"
    - "Verify uses BIFURCATION_DETECT"
```

#### Success Criteria
- [ ] Market data refreshing
- [ ] Uses existing EWS queries
- [ ] Recession model works

---

## PHASE 4: VALIDATION (Weeks 21-28)

### GAP-ML-012: Backtesting Framework
**Priority:** HIGH | **Effort:** XL (8+ weeks) | **Status:** NOT STARTED

#### Purpose
Backtest McKenney-Lacan predictions against historical events.

#### EXISTING COMPONENTS TO USE
```yaml
use_existing:
  # All prediction queries (to test)
  - ISING_*, GRANOVETTER_*, EWS_*, R0_*

  # Temporal queries (from GAP-ML-004)
  - Point-in-time snapshots
```

#### Historical Events for Validation
```yaml
cyber_incidents:
  - WANNACRY-2017: R0 validation (observed R0 = 2.8)
  - NOTPETYA-2017: Cascade validation (observed R0 = 3.5)
  - SOLARWINDS-2020: Supply chain cascade
  - LOG4SHELL-2021: Zero-day epidemic (observed R0 = 4.2)

economic_crises:
  - GFC-2008: Bifurcation validation
  - COVID-CRASH-2020: Black swan detection
```

#### Implementation Tasks
```yaml
task_1:
  name: "Historical Data Collection"
  implementation: "Build time-series snapshots for each event"
  auditor_check:
    - "Verify uses GAP-ML-004 temporal queries"

task_2:
  name: "Backtest Runner"
  implementation: |
    // Run predictions at T-N for each event
    // Compare to actual outcomes
  auditor_check:
    - "Verify uses existing prediction queries"
    - "Verify metrics calculation correct"

task_3:
  name: "Calibration Grid Search"
  implementation: |
    // Optimize parameters using backtests
    // Store calibrated parameters
  auditor_check:
    - "Verify parameter bounds sensible"
    - "Verify results stored for reuse"
```

#### Success Criteria
- [ ] Backtest against 10+ cyber incidents
- [ ] Accuracy >70% at 30-day window
- [ ] Calibrated parameters stored
- [ ] Uses existing prediction queries

---

## AGENT COORDINATION PROTOCOL

### For Each Gap Implementation
```yaml
agent_team:
  researcher:
    role: "Analyze existing components before implementation"
    deliverable: "Component inventory checklist"

  coder:
    role: "Implement using existing components"
    constraint: "NO new code if existing code works"

  tester:
    role: "Validate implementation"
    constraint: "Must test against existing queries"

  auditor:
    role: "Verify NO THEATRE compliance"
    checklist:
      - "[ ] No duplicate constraints created"
      - "[ ] No duplicate indexes created"
      - "[ ] Existing queries used where available"
      - "[ ] GDS projections reused"
      - "[ ] Follows library naming convention"
      - "[ ] Documentation format matches library"
```

### Auditor Checklist Template (USE FOR EVERY TASK)
```markdown
## AUDITOR VERIFICATION - [GAP-ID] [TASK-NAME]

### Schema Compliance
- [ ] No duplicate constraints (checked against schema lines 12-19)
- [ ] No duplicate indexes (checked against schema lines 24-49)
- [ ] GDS projections reused (checked against schema lines 52-85)

### Query Library Compliance
- [ ] Existing queries used (checked against library)
- [ ] No duplicate calculations
- [ ] Follows naming convention

### Integration Compliance
- [ ] Uses existing infrastructure (Neo4j, Qdrant, PostgreSQL)
- [ ] Follows API patterns
- [ ] Documentation complete

### NO THEATRE Verification
- [ ] Actual work done (not framework building)
- [ ] Deliverables exist and work
- [ ] No unnecessary abstraction

Auditor: ________________
Date: ________________
```

---

## MEMORY KEYS FOR SESSION CONTINUITY

```yaml
qdrant_memories:
  - ID 97: "aeon-architecture-complete" (infrastructure details)
  - ID 98: "gap-tracker-state" (gap status)
  - ID 99: "taskmaster-complete" (this document reference)

local_files:
  - "08_Planned_Enhancements/00_COMPREHENSIVE_TASKMASTER.md" (this file)
  - "08_GAP_CASES/*.md" (individual gap specs)
  - "mckenney-lacan-calculus-2025-11-28/neo4j-schema/" (schema + library)
```

---

## QUICK START FOR NEW SESSION

```bash
# 1. Load context
Read: 08_Planned_Enhancements/00_COMPREHENSIVE_TASKMASTER.md
Query Qdrant: IDs 97, 98, 99

# 2. Check current gap status
Read: 08_GAP_CASES/00_GAP_TRACKER.md

# 3. Find existing components
Read: mckenney-lacan-calculus-2025-11-28/neo4j-schema/01_MCKENNEY_LACAN_NEO4J_SCHEMA.cypher
Read: mckenney-lacan-calculus-2025-11-28/neo4j-schema/02_MCKENNEY_LACAN_CYPHER_LIBRARY.cypher

# 4. Continue implementation
# Follow phase order: PHASE 1 → PHASE 2 → PHASE 3 → PHASE 4
```

---

**Document Version:** 1.0.0
**Created:** 2025-11-30
**Author:** AEON Development Team
**Purpose:** McKenney-Lacan Foundation Implementation Guide
