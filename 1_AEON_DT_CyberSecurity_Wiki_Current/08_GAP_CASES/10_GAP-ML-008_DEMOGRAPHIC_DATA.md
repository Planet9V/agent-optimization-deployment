# GAP-ML-008: Demographic Data Integration

**File:** 10_GAP-ML-008_DEMOGRAPHIC_DATA.md
**Gap ID:** GAP-ML-008
**Created:** 2025-11-30
**Priority:** HIGH
**Phase:** 3 - Data Integration
**Effort:** XL (8+ weeks)
**Status:** NOT STARTED

---

## Problem Statement

**Current State:**
- Cyber-only actor modeling
- No population-scale dynamics
- Cannot model social movements or political shifts
- Limited to organizational actors

**Desired State:**
- Census/demographic data integration
- Population-scale Ising simulations
- Political/economic actor modeling
- Regional and demographic segmentation

---

## Technical Specification

### Data Sources

```yaml
primary_sources:
  us_census:
    api: "https://api.census.gov/data"
    datasets:
      - "acs/acs5"  # American Community Survey
      - "dec/pl"    # Decennial Census
    update_frequency: "annual"

  world_bank:
    api: "https://api.worldbank.org/v2"
    indicators:
      - "SP.POP.TOTL"  # Total population
      - "NY.GDP.PCAP.CD"  # GDP per capita
      - "IT.NET.USER.ZS"  # Internet users %
    update_frequency: "annual"

  bls:
    api: "https://api.bls.gov/publicAPI/v2"
    series:
      - "LAUCN*"  # Local area unemployment
      - "CUUR*"   # Consumer price index
    update_frequency: "monthly"

secondary_sources:
  polling_aggregators:
    - "538"
    - "RealClearPolitics"
  social_sentiment:
    - "Twitter/X API"
    - "Reddit API"
```

### Demographic Node Schema

```cypher
// Geographic Region
CREATE (r:Region {
  id: 'US-CA-LOS_ANGELES',
  name: 'Los Angeles County',
  type: 'COUNTY',
  parent_id: 'US-CA',

  // Demographics
  population: 10014009,
  population_density: 2498.4,
  median_age: 36.2,
  median_income: 68044,

  // Technology penetration
  internet_penetration: 0.89,
  smartphone_penetration: 0.85,
  social_media_usage: 0.72,

  // Ising model parameters
  spin: 0,                    // Aggregate opinion (-1 to 1)
  volatility: 0.4,            // Temperature
  susceptibility: 0.6,        // How easily influenced
  external_field: 0.1,        // Media/government influence

  // Update metadata
  data_source: 'US_CENSUS_ACS5',
  data_year: 2023,
  last_updated: datetime()
})

// Demographic Segment
CREATE (s:DemographicSegment {
  id: 'US-TECH-WORKERS',
  name: 'Technology Industry Workers',
  description: 'Workers in NAICS 54 (Professional, Scientific, Technical)',

  // Size
  population_estimate: 9200000,
  geographic_distribution: '{"CA": 0.22, "TX": 0.11, "NY": 0.09}',

  // Psychometric aggregates
  avg_ocean_o: 0.72,          # High openness
  avg_ocean_c: 0.65,
  avg_disc_d: 0.58,

  // Ising parameters
  internal_coupling: 0.7,     # Strong within-group connections
  external_coupling: 0.3,     # Weaker cross-group connections
  threshold_distribution: 'beta(2,5)',  # Low thresholds

  // Vulnerability factors
  remote_work_percentage: 0.65,
  byod_percentage: 0.45,
  security_training_rate: 0.78
})

// Regional relationship
CREATE (r:Region)-[:CONTAINS_SEGMENT {
  population: 450000,
  percentage: 0.045
}]->(s:DemographicSegment)
```

### Population-Scale Ising Simulation

```python
import numpy as np
from typing import Dict, List

class PopulationIsingModel:
    """
    Ising model simulation for population-scale opinion dynamics.
    """

    def __init__(self, regions: List[Dict], segments: List[Dict]):
        self.regions = {r['id']: r for r in regions}
        self.segments = {s['id']: s for s in segments}
        self.coupling_matrix = self._build_coupling_matrix()

    def _build_coupling_matrix(self) -> np.ndarray:
        """Build J_ij coupling matrix from geographic and demographic proximity."""
        n = len(self.regions)
        J = np.zeros((n, n))

        region_ids = list(self.regions.keys())
        for i, r1 in enumerate(region_ids):
            for j, r2 in enumerate(region_ids):
                if i != j:
                    # Geographic coupling (adjacent regions)
                    geo_coupling = self._geographic_coupling(r1, r2)
                    # Demographic similarity coupling
                    demo_coupling = self._demographic_coupling(r1, r2)
                    # Economic coupling
                    econ_coupling = self._economic_coupling(r1, r2)

                    J[i, j] = 0.4 * geo_coupling + 0.3 * demo_coupling + 0.3 * econ_coupling

        return J

    def simulate_step(self, spins: np.ndarray, temperature: float) -> np.ndarray:
        """Single Metropolis-Hastings step."""
        n = len(spins)

        for i in range(n):
            # Calculate local field
            h_i = self.regions[list(self.regions.keys())[i]].get('external_field', 0)

            # Energy change if we flip spin i
            delta_E = 2 * spins[i] * (np.dot(self.coupling_matrix[i], spins) + h_i)

            # Metropolis acceptance
            if delta_E < 0 or np.random.random() < np.exp(-delta_E / temperature):
                spins[i] *= -1

        return spins

    def run_simulation(
        self,
        initial_spins: np.ndarray,
        temperature: float,
        n_steps: int = 1000
    ) -> Dict:
        """Run full simulation and return statistics."""
        spins = initial_spins.copy()
        magnetization_history = []

        for step in range(n_steps):
            spins = self.simulate_step(spins, temperature)
            magnetization = np.mean(spins)
            magnetization_history.append(magnetization)

        return {
            'final_spins': spins,
            'final_magnetization': np.mean(spins),
            'magnetization_history': magnetization_history,
            'consensus_reached': abs(np.mean(spins)) > 0.8,
            'convergence_time': self._find_convergence(magnetization_history)
        }
```

---

## Implementation Steps

### Step 1: Data Source Integration (Week 1-3)
- [ ] Set up Census API integration
- [ ] Set up World Bank API integration
- [ ] Set up BLS API integration
- [ ] Create data refresh pipeline

### Step 2: Schema Implementation (Week 4-5)
- [ ] Create Region node type in Neo4j
- [ ] Create DemographicSegment node type
- [ ] Build geographic hierarchy
- [ ] Create relationships

### Step 3: Ising Integration (Week 6-7)
- [ ] Implement PopulationIsingModel
- [ ] Connect to Neo4j for coupling matrix
- [ ] Run simulations on population data
- [ ] Validate against historical events

### Step 4: API & Visualization (Week 8+)
- [ ] Create demographic query endpoints
- [ ] Build population simulation endpoint
- [ ] Create geographic visualization
- [ ] Documentation

---

## Success Criteria

- [ ] Census data for all US counties loaded
- [ ] Population-scale Ising simulations running
- [ ] Regional coupling matrix accurate
- [ ] Predictions validated against historical polls
- [ ] API endpoints operational

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Data access limitations | High | Medium | Multiple source fallbacks |
| Privacy concerns | High | Medium | Aggregation only, no PII |
| Model accuracy | Medium | Medium | Validate against known events |

---

## Dependencies

- Census API keys
- World Bank API access
- Phase 1 & 2 gaps complete

---

## Memory Keys

- `gap-ml-008-sources`: Data source configurations
- `gap-ml-008-schema`: Schema design decisions

---

## References

- Ising Theory: `mckenney-lacan-calculus-2025-11-28/Predictive_02_ISING_DYNAMICS_OPINION.md`
- Population Dynamics: `mckenney-lacan-calculus-2025-11-28/06_SCHELLING_GRANOVETTER_TEAM_COMPOSITION.md`
