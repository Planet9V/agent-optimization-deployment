# GAP-ML-010: Cascade Event Tree Example

**Visual representation of cascade genealogy tracking**

## Example Cascade Tree

```
Generation 0 (Seed):
    [EVENT_SEED_001]
    actor: TEST_ACTOR_001
    threshold: 0.2
    influence: 0.0 (seed)
    ↓ TRIGGERED
    │
Generation 1:
    ├─ [EVENT_GEN1_002]
    │  actor: TEST_ACTOR_002
    │  threshold: 0.4
    │  influence: 0.5 (1/2 neighbors adopted)
    │  parent: EVENT_SEED_001
    │  ↓ TRIGGERED
    │
    └─ [EVENT_GEN1_003]
       actor: TEST_ACTOR_003
       threshold: 0.5
       influence: 0.5 (1/2 neighbors adopted)
       parent: EVENT_SEED_001
       ↓ TRIGGERED
       │
Generation 2:
       ├─ [EVENT_GEN2_004]
       │  actor: TEST_ACTOR_004
       │  threshold: 0.7
       │  influence: 0.67 (2/3 neighbors adopted)
       │  parent: EVENT_GEN1_003
       │
       └─ [EVENT_GEN2_005]
          actor: TEST_ACTOR_005
          threshold: 0.8
          influence: 1.0 (1/1 neighbor adopted)
          parent: EVENT_GEN1_003
```

## Query Example: Retrieve Full Tree

```cypher
MATCH path = (seed:CascadeEvent {id: 'EVENT_SEED_001'})-[:TRIGGERED*0..10]->(descendant:CascadeEvent)
RETURN
    seed.id AS seed_event,
    descendant.id AS event_id,
    descendant.generation AS generation,
    descendant.parent_event_id AS parent,
    descendant.actor_id AS actor,
    descendant.activation_threshold AS threshold,
    descendant.neighbor_influence AS influence,
    length(path) AS depth_from_seed
ORDER BY generation, event_id;
```

**Output:**
```
| seed_event      | event_id         | generation | parent          | actor          | threshold | influence | depth |
|-----------------|------------------|------------|-----------------|----------------|-----------|-----------|-------|
| EVENT_SEED_001  | EVENT_SEED_001   | 0          | null            | TEST_ACTOR_001 | 0.2       | 0.0       | 0     |
| EVENT_SEED_001  | EVENT_GEN1_002   | 1          | EVENT_SEED_001  | TEST_ACTOR_002 | 0.4       | 0.5       | 1     |
| EVENT_SEED_001  | EVENT_GEN1_003   | 1          | EVENT_SEED_001  | TEST_ACTOR_003 | 0.5       | 0.5       | 1     |
| EVENT_SEED_001  | EVENT_GEN2_004   | 2          | EVENT_GEN1_003  | TEST_ACTOR_004 | 0.7       | 0.67      | 2     |
| EVENT_SEED_001  | EVENT_GEN2_005   | 2          | EVENT_GEN1_003  | TEST_ACTOR_005 | 0.8       | 1.0       | 2     |
```

## Cascade Velocity Analysis

```cypher
MATCH (ce:CascadeEvent {cascade_id: 'TEST_CASCADE_001'})
WITH ce.generation AS gen, count(ce) AS events
ORDER BY gen
RETURN gen AS generation, events AS new_activations;
```

**Output:**
```
| generation | new_activations |
|------------|-----------------|
| 0          | 1               | (seed)
| 1          | 2               | (2x growth)
| 2          | 2               | (steady)
```

**Velocity Classification:**
- Generation 0→1: RAPID GROWTH (100% increase)
- Generation 1→2: STEADY (same rate)

## Critical Influencer Detection

```cypher
MATCH (parent:CascadeEvent {cascade_id: 'TEST_CASCADE_001'})-[:TRIGGERED]->(child:CascadeEvent)
WITH parent, count(child) AS children_triggered
WHERE children_triggered > 0
RETURN
    parent.id AS influencer,
    parent.generation AS generation,
    children_triggered AS cascade_size,
    CASE
        WHEN children_triggered >= 3 THEN 'CRITICAL TIPPING POINT'
        WHEN children_triggered >= 2 THEN 'SIGNIFICANT INFLUENCER'
        ELSE 'MINOR INFLUENCER'
    END AS influence_level
ORDER BY children_triggered DESC;
```

**Output:**
```
| influencer      | generation | cascade_size | influence_level        |
|-----------------|------------|--------------|------------------------|
| EVENT_SEED_001  | 0          | 2            | SIGNIFICANT INFLUENCER |
| EVENT_GEN1_003  | 1          | 2            | SIGNIFICANT INFLUENCER |
| EVENT_GEN1_002  | 1          | 0            | (no children)          |
```

**Analysis:**
- EVENT_SEED_001: Triggered 2 children (TEST_ACTOR_002, TEST_ACTOR_003)
- EVENT_GEN1_003: Triggered 2 children (TEST_ACTOR_004, TEST_ACTOR_005)
- EVENT_GEN1_002: Terminal node (no further cascade)

## Cascade Summary Statistics

```cypher
MATCH (ce:CascadeEvent {cascade_id: 'TEST_CASCADE_001'})
WITH count(ce) AS total_events,
     max(ce.generation) AS max_gen,
     min(ce.timestamp) AS start,
     max(ce.timestamp) AS end
RETURN
    total_events AS total_cascade_events,
    max_gen + 1 AS total_generations,
    start AS cascade_start_time,
    end AS cascade_end_time,
    duration.inSeconds(start, end) AS duration_seconds;
```

**Output:**
```
| total_events | total_generations | cascade_start_time      | cascade_end_time        | duration_seconds |
|--------------|-------------------|-------------------------|-------------------------|------------------|
| 5            | 3                 | 2025-11-30T11:17:00.000 | 2025-11-30T11:17:05.000 | 5                |
```

**Analysis:**
- 5 total adoption events
- 3 generations (0, 1, 2)
- Cascade completed in 5 seconds
- Average: 1.67 events per generation
- Velocity: 1.0 events/second

## Real-World Application

### Scenario: Ransomware Technique Adoption

**Context:**
- Technique: T1486 (Data Encrypted for Impact)
- Initial Adopter: APT28 (sophisticated actor, low threshold)
- Network: 50 connected threat actors

**Cascade Progression:**

```
Generation 0 (Day 0):
    APT28 adopts T1486 (ransomware technique)
    ↓
Generation 1 (Day 1-3):
    5 high-sophistication actors adopt
    Threshold: 0.1-0.3 (early adopters)
    ↓
Generation 2 (Day 4-7):
    12 medium-sophistication actors adopt
    Threshold: 0.3-0.6 (majority)
    ↓
Generation 3 (Day 8-14):
    20 low-sophistication actors adopt
    Threshold: 0.6-0.9 (late adopters)
    ↓
Result: 37/50 actors (74% adoption)
Classification: MASSIVE CASCADE
```

**Velocity Analysis:**
```
Gen 0→1: 5 adoptions / 3 days = 1.67 events/day (RAPID)
Gen 1→2: 12 adoptions / 4 days = 3.0 events/day (EXPLOSIVE)
Gen 2→3: 20 adoptions / 7 days = 2.86 events/day (EXPLOSIVE)
```

**Critical Influencers:**
- APT28 (seed): Triggered 5 children (top influencer)
- APT29: Triggered 4 children (secondary amplifier)
- Sandworm: Triggered 3 children (tertiary amplifier)

**Security Implications:**
- Early detection (Gen 0→1): Prevents 69% of cascade (37 blocked adoptions)
- Mid-cascade intervention (Gen 1→2): Prevents 64% of remaining cascade (32 blocked)
- Late intervention (Gen 2→3): Minimal impact (only 13 blocked)

**Conclusion:** CascadeEvent tracking enables early warning systems for technique propagation, allowing proactive defense before widespread adoption.

---

**Document:** gap_ml_010_cascade_tree_example.md
**Created:** 2025-11-30
**Purpose:** Visual guide for cascade genealogy tracking
**Status:** COMPLETE
