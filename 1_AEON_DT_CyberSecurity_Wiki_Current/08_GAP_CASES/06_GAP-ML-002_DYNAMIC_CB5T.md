# GAP-ML-002: Dynamic CB5T Parameters

**File:** 06_GAP-ML-002_DYNAMIC_CB5T.md
**Gap ID:** GAP-ML-002
**Created:** 2025-11-30
**Priority:** CRITICAL
**Phase:** 2 - Core Math
**Effort:** L (4-6 weeks)
**Status:** NOT STARTED

---

## Problem Statement

**Current State:**
- DISC and OCEAN scores set at actor creation (static)
- No mechanism for psychometric drift over time
- No real-time assessment integration
- Lacanian register values never update

**Desired State:**
- Dynamic psychometric updates from behavioral signals
- Integration with HR systems, security training results
- Lacanian register updates from incident participation
- Temporal tracking of personality changes

---

## Technical Specification

### Enhanced Actor Schema

```cypher
// Current (Static)
CREATE (a:Actor {
  disc_d: 0.7,  // Set once, never updated
  ocean_n: 0.8
})

// Enhanced (Dynamic with History)
CREATE (a:Actor {
  // Current Values
  disc_d: 0.7,
  disc_i: 0.4,
  disc_s: 0.3,
  disc_c: 0.6,

  ocean_o: 0.5,
  ocean_c: 0.6,
  ocean_e: 0.4,
  ocean_a: 0.7,
  ocean_n: 0.8,

  lacan_real: 0.6,
  lacan_symbolic: 0.4,
  lacan_imaginary: 0.5,

  // Psychometric History (JSON arrays)
  disc_history: '[{"d":0.6,"i":0.3,"s":0.4,"c":0.5,"ts":"2025-01-01"},...]',
  ocean_history: '[{"o":0.4,"c":0.5,"e":0.3,"a":0.6,"n":0.7,"ts":"2025-01-01"},...]',
  lacan_history: '[{"r":0.5,"s":0.3,"i":0.4,"ts":"2025-01-01"},...]',

  // Update Metadata
  psychometric_last_update: datetime(),
  psychometric_update_source: 'BEHAVIORAL_SIGNAL',
  psychometric_confidence: 0.85,

  // Drift Parameters
  trait_stability: 0.9,      // How resistant to change (0-1)
  assessment_count: 5,       // Number of assessments
  behavioral_signal_count: 23 // Behavioral observations
})
```

### Update Triggers

```cypher
// 1. Security Incident Participation → Update Lacanian registers
MATCH (a:Actor)-[:PARTICIPATED_IN]->(e:SecurityEvent)
WHERE e.severity = 'CRITICAL'
WITH a,
     a.lacan_real + 0.1 as new_real,  // Trauma exposure
     a.lacan_symbolic - 0.05 as new_symbolic  // Protocol trust decrease
SET a.lacan_real = CASE WHEN new_real > 1 THEN 1 ELSE new_real END,
    a.lacan_symbolic = CASE WHEN new_symbolic < 0 THEN 0 ELSE new_symbolic END,
    a.psychometric_last_update = datetime(),
    a.psychometric_update_source = 'INCIDENT_PARTICIPATION'

// 2. Training Completion → Update OCEAN traits
MATCH (a:Actor)-[:COMPLETED]->(t:Training)
WHERE t.type = 'SECURITY_AWARENESS'
WITH a,
     a.ocean_o + (t.score - 0.5) * 0.1 as new_o,  // Learning → Openness
     a.ocean_c + (t.completion_rate - 0.5) * 0.1 as new_c  // Diligence → Conscientiousness
SET a.ocean_o = CASE WHEN new_o > 1 THEN 1 WHEN new_o < 0 THEN 0 ELSE new_o END,
    a.ocean_c = CASE WHEN new_c > 1 THEN 1 WHEN new_c < 0 THEN 0 ELSE new_c END

// 3. Communication Pattern → Update DISC
MATCH (a:Actor)-[c:COMMUNICATED_WITH]->(b:Actor)
WHERE c.timestamp > datetime() - duration('P7D')
WITH a, count(c) as comm_count, avg(c.response_time) as avg_response
WITH a,
     CASE WHEN comm_count > 50 THEN a.disc_i + 0.05 ELSE a.disc_i END as new_i,
     CASE WHEN avg_response < 60 THEN a.disc_d + 0.03 ELSE a.disc_d END as new_d
SET a.disc_i = new_i, a.disc_d = new_d
```

### Decay/Drift Model

```python
# Personality traits have stability - they don't change dramatically
def update_trait(current_value, observation, stability=0.9):
    """
    Bayesian update with stability constraint.

    Args:
        current_value: Current trait estimate (0-1)
        observation: New behavioral observation (0-1)
        stability: How resistant the trait is to change (0-1)
    """
    # Weight observation by inverse stability
    observation_weight = 1 - stability

    # Bayesian-like update
    new_value = (current_value * stability) + (observation * observation_weight)

    # Bound to [0, 1]
    return max(0, min(1, new_value))

# Example: High stability trait (Conscientiousness)
new_c = update_trait(current_c=0.6, observation=0.8, stability=0.95)
# Result: 0.61 (small change despite large observation)

# Example: Lower stability trait (Extraversion)
new_e = update_trait(current_e=0.4, observation=0.8, stability=0.7)
# Result: 0.52 (larger change)
```

---

## Implementation Steps

### Step 1: Schema Enhancement (Week 1)
- [ ] Add history array properties to Actor nodes
- [ ] Add update metadata properties
- [ ] Add drift parameters
- [ ] Migrate existing actors

### Step 2: Update Triggers (Week 2)
- [ ] Implement incident participation trigger
- [ ] Implement training completion trigger
- [ ] Implement communication pattern trigger
- [ ] Create scheduled drift calculations

### Step 3: Integration APIs (Week 3)
- [ ] HR system integration endpoint
- [ ] Training platform webhook
- [ ] Behavioral signal ingestion API
- [ ] Manual assessment endpoint

### Step 4: Validation & Tuning (Week 4)
- [ ] Validate update formulas against psychological literature
- [ ] Tune stability parameters
- [ ] Performance testing
- [ ] Documentation

---

## Success Criteria

- [ ] Psychometric values update automatically from signals
- [ ] History tracking captures all changes
- [ ] Update frequency appropriate (not too volatile)
- [ ] Integration with at least one external system
- [ ] Lacanian registers reflect incident participation

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Over-volatility | Medium | Medium | High stability defaults, rate limiting |
| Privacy concerns | High | Medium | Anonymization, consent management |
| Integration failures | Medium | Medium | Fallback to manual updates |

---

## Dependencies

- GAP-ML-004 (Temporal Versioning) for history tracking
- External system APIs (HR, training)
- Neo4j triggers operational

---

## Memory Keys

- `gap-ml-002-formulas`: Update formula decisions
- `gap-ml-002-integrations`: External system configs

---

## References

- Psychometric Theory: `mckenney-lacan-calculus-2025-11-28/05_PSYCHOMETRIC_TENSOR_DISC_BIG5.md`
- Lacanian Dynamics: `mckenney-lacan-calculus-2025-11-28/04_LACANIAN_MIRROR_AND_GROUP_DYNAMICS.md`
