# GAP-ML-004: Temporal Versioning (Event Sourcing)

**File:** 01_GAP-ML-004_TEMPORAL_VERSIONING.md
**Gap ID:** GAP-ML-004
**Created:** 2025-11-30
**Priority:** CRITICAL
**Phase:** 1 - Foundation
**Effort:** L (4-6 weeks)
**Status:** NOT STARTED

---

## Problem Statement

**Current State:**
- Node properties overwritten on update
- No historical state tracking
- Cannot replay past system states
- Lost audit trail for property changes

**Desired State:**
- Full event sourcing with temporal properties
- Point-in-time queries for any timestamp
- Complete audit trail for all property changes
- Ability to replay historical states

---

## Technical Specification

### Schema Changes Required

```cypher
// ADD to all node types
valid_from: datetime,      // When this version became active
valid_to: datetime,        // When this version was superseded (null = current)
version: integer,          // Incrementing version number
change_source: string,     // What triggered the change
change_actor: string       // Who/what made the change

// Example: Actor with temporal properties
CREATE (a:Actor {
  id: 'ACTOR-001',
  name: 'John Smith',

  // Current values
  spin: 1,
  threshold: 0.3,

  // Temporal metadata
  valid_from: datetime('2025-11-30T00:00:00Z'),
  valid_to: null,  // Current version
  version: 1,
  change_source: 'INITIAL_LOAD',
  change_actor: 'system'
})
```

### Event Log Node Type

```cypher
// New node type for event history
CREATE (e:PropertyChangeEvent {
  id: 'PCE-001',
  entity_id: 'ACTOR-001',
  entity_type: 'Actor',
  property_name: 'spin',
  old_value: -1,
  new_value: 1,
  changed_at: datetime(),
  change_source: 'CASCADE_ACTIVATION',
  change_actor: 'granovetter_cascade_engine',
  metadata: '{"cascade_id": "CASCADE-2025-001", "generation": 3}'
})
```

### Temporal Query Functions

```cypher
// Point-in-time query: Get actor state at specific timestamp
MATCH (a:Actor {id: $actor_id})
WHERE a.valid_from <= $timestamp
  AND (a.valid_to IS NULL OR a.valid_to > $timestamp)
RETURN a

// History query: Get all versions of an actor
MATCH (a:Actor {id: $actor_id})
RETURN a ORDER BY a.version DESC

// Change log query: Get all changes to an actor
MATCH (e:PropertyChangeEvent {entity_id: $actor_id})
RETURN e ORDER BY e.changed_at DESC
```

---

## Implementation Steps

### Step 1: Schema Migration (Week 1)
- [ ] Add temporal properties to Actor nodes
- [ ] Add temporal properties to Asset nodes
- [ ] Add temporal properties to Concept nodes
- [ ] Create PropertyChangeEvent node type
- [ ] Create indexes on valid_from, valid_to

### Step 2: Update Procedures (Week 2)
- [ ] Create `temporal_update()` procedure
- [ ] Create `temporal_delete()` procedure (soft delete)
- [ ] Create `get_at_timestamp()` function
- [ ] Create `get_history()` function

### Step 3: Migration Script (Week 3)
- [ ] Migrate existing nodes to have temporal properties
- [ ] Set valid_from = creation_date or epoch
- [ ] Set valid_to = null (all current)
- [ ] Set version = 1 for all existing

### Step 4: API Integration (Week 4)
- [ ] Update Neo4j Cypher library
- [ ] Add temporal query endpoints
- [ ] Add history endpoints
- [ ] Update documentation

---

## Success Criteria

- [ ] All node types have temporal properties
- [ ] Point-in-time queries return correct historical state
- [ ] PropertyChangeEvent captures all mutations
- [ ] Query performance <100ms for temporal queries
- [ ] Migration script runs without data loss

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Storage growth | Medium | High | Implement archival policy for old versions |
| Query complexity | Medium | Medium | Create helper functions, optimize indexes |
| Migration data loss | Critical | Low | Full backup before migration, staged rollout |

---

## Dependencies

- Neo4j 5.26+ operational
- Admin access to Neo4j
- No dependencies on other gaps

---

## Memory Keys

- `gap-ml-004-design`: Design decisions
- `gap-ml-004-progress`: Implementation progress
- `gap-ml-004-issues`: Issues encountered

---

## References

- Source: `mckenney-lacan-calculus-2025-11-28/neo4j-schema/03_MCKENNEY_LACAN_GAP_ANALYSIS.md`
- Schema: `mckenney-lacan-calculus-2025-11-28/neo4j-schema/01_MCKENNEY_LACAN_NEO4J_SCHEMA.cypher`
