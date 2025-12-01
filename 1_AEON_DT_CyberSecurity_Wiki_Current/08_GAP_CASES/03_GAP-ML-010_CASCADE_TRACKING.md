# GAP-ML-010: Cascade Event Tracking

**File:** 03_GAP-ML-010_CASCADE_TRACKING.md
**Gap ID:** GAP-ML-010
**Created:** 2025-11-30
**Priority:** HIGH
**Phase:** 1 - Foundation
**Effort:** M (2-4 weeks)
**Status:** NOT STARTED

---

## Problem Statement

**Current State:**
- Events exist but cascade relationships incomplete
- No cascade genealogy tracking
- Cannot trace propagation paths
- No cascade velocity/acceleration metrics

**Desired State:**
- Full CASCADE_EVENT subgraph
- Generation tracking (seed → N-hop)
- Cascade velocity and acceleration metrics
- Complete propagation path analysis

---

## Technical Specification

### New Node Type: CascadeEvent

```cypher
CREATE (ce:CascadeEvent {
  // Identity
  id: 'CASCADE-2025-001',
  cascade_type: 'GRANOVETTER',  // GRANOVETTER | EPIDEMIC | BIFURCATION

  // Genealogy
  seed_entity_id: 'ACTOR-001',  // Original trigger
  generation: 0,                 // 0 = seed, 1 = first hop, etc.
  parent_event_id: null,         // null for seed, parent ID otherwise

  // Timing
  started_at: datetime(),
  detected_at: datetime(),
  completed_at: null,

  // Metrics
  total_activated: 15,           // Total entities activated
  current_generation_count: 3,   // Active at current generation
  velocity: 2.5,                 // Activations per time unit
  acceleration: 0.3,             // Change in velocity

  // Status
  status: 'ACTIVE',              // ACTIVE | CONTAINED | COMPLETED
  containment_point: null,       // Where cascade stopped

  // Context
  trigger_event: 'CVE-2024-1234 exploitation',
  sector_id: 'energy'
})
```

### New Relationship: TRIGGERED

```cypher
// Cascade genealogy relationship
(parent:CascadeEvent)-[:TRIGGERED {
  generation: 1,
  timestamp: datetime(),
  activation_threshold: 0.3,
  actual_activation_ratio: 0.45
}]->(child:CascadeEvent)

// Entity participation
(a:Actor)-[:PARTICIPATED_IN {
  role: 'SEED' | 'ACTIVATED' | 'RESISTANT',
  generation: 0,
  activation_time: datetime(),
  prior_spin: -1,
  post_spin: 1
}]->(ce:CascadeEvent)
```

### Cascade Tree Queries

```cypher
// Get full cascade tree from seed
MATCH path = (seed:CascadeEvent {id: $cascade_id})-[:TRIGGERED*0..10]->(descendant:CascadeEvent)
RETURN path

// Get all entities activated in cascade
MATCH (a:Actor)-[p:PARTICIPATED_IN]->(ce:CascadeEvent {id: $cascade_id})
WHERE p.role = 'ACTIVATED'
RETURN a, p.generation, p.activation_time
ORDER BY p.generation, p.activation_time

// Calculate cascade velocity over time
MATCH (ce:CascadeEvent {id: $cascade_id})<-[p:PARTICIPATED_IN]-(a:Actor)
WITH ce, p.generation as gen, count(a) as activated_count
RETURN gen, activated_count,
       activated_count - lag(activated_count) OVER (ORDER BY gen) as delta
ORDER BY gen

// Find containment points (where cascade stopped)
MATCH (a:Actor)-[p:PARTICIPATED_IN {role: 'RESISTANT'}]->(ce:CascadeEvent {id: $cascade_id})
RETURN a.id, a.threshold, p.generation
```

---

## Implementation Steps

### Step 1: Schema Creation (Week 1)
- [ ] Create CascadeEvent node type
- [ ] Create TRIGGERED relationship type
- [ ] Create PARTICIPATED_IN relationship type
- [ ] Add indexes for cascade_id, generation

### Step 2: Tracking Procedures (Week 2)
- [ ] Create `initiate_cascade()` procedure
- [ ] Create `propagate_cascade()` procedure
- [ ] Create `record_activation()` procedure
- [ ] Create `calculate_metrics()` procedure

### Step 3: Analytics Queries (Week 3)
- [ ] Cascade tree traversal queries
- [ ] Velocity/acceleration calculations
- [ ] Containment analysis queries
- [ ] Historical cascade comparison

### Step 4: Integration (Week 4)
- [ ] Connect to Granovetter cascade engine
- [ ] Add to Cypher query library
- [ ] Update API endpoints
- [ ] Documentation

---

## Success Criteria

- [ ] CascadeEvent nodes created for all cascade types
- [ ] Full genealogy tracking operational
- [ ] Velocity/acceleration metrics accurate
- [ ] Query performance <100ms for cascade trees up to 10 generations
- [ ] Historical cascades can be replayed

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Large cascade graphs | Medium | Medium | Limit generation depth, archive old cascades |
| Real-time tracking overhead | Medium | Low | Batch updates, async processing |

---

## Dependencies

- Neo4j schema access
- Granovetter cascade engine (for testing)

---

## Memory Keys

- `gap-ml-010-design`: Schema design decisions
- `gap-ml-010-progress`: Implementation progress

---

## References

- Theory: `mckenney-lacan-calculus-2025-11-28/Predictive_03_GRANOVETTER_THRESHOLDS_CASCADE.md`
- Queries: `mckenney-lacan-calculus-2025-11-28/neo4j-schema/02_MCKENNEY_LACAN_CYPHER_LIBRARY.cypher`
