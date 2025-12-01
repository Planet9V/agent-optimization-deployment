# GAP-ML-007: Multi-R0 Ensemble

**File:** 08_GAP-ML-007_MULTI_R0.md
**Gap ID:** GAP-ML-007
**Created:** 2025-11-30
**Priority:** HIGH
**Phase:** 2 - Core Math
**Effort:** M (2-4 weeks)
**Status:** NOT STARTED

---

## Problem Statement

**Current State:**
- One vulnerability → one R0 value calculation
- No ensemble or competing pathogen modeling
- Static network topology assumed
- Single infection vector only

**Desired State:**
- Multi-vulnerability R0 matrix
- Dynamic network topology updates
- Competing/cooperating malware modeling
- Ensemble predictions with confidence intervals

---

## Technical Specification

### R0 Formula Review

```
Basic Reproduction Number:
R0 = (β/γ) × λ_max(A)

Where:
- β = transmission rate (probability of infection per contact)
- γ = recovery rate (rate of patching/containment)
- λ_max(A) = largest eigenvalue of adjacency matrix A
- R0 > 1 → epidemic growth
- R0 < 1 → epidemic dies out
```

### Multi-R0 Matrix Schema

```cypher
// R0 matrix stored as relationship properties
CREATE (v1:Vulnerability {id: 'CVE-2024-001'})-[:INTERACTS_WITH {
  interaction_type: 'COMPETING',  // COMPETING | COOPERATING | INDEPENDENT
  interaction_strength: -0.3,      // Negative = competing
  combined_r0: 1.8,               // Joint R0 when both present
  dominance_probability: 0.6      // Probability v1 dominates
}]->(v2:Vulnerability {id: 'CVE-2024-002'})

// Per-vulnerability R0 with network context
CREATE (v:Vulnerability {
  id: 'CVE-2024-001',

  // Base R0 parameters
  transmission_rate: 0.4,         // β
  recovery_rate: 0.1,             // γ
  base_r0: 4.0,                   // β/γ

  // Network-adjusted R0
  r0_energy_sector: 3.2,          // Sector-specific R0
  r0_water_sector: 2.8,
  r0_healthcare_sector: 4.5,

  // Ensemble statistics
  r0_mean: 3.5,
  r0_std: 0.6,
  r0_95_ci_lower: 2.3,
  r0_95_ci_upper: 4.7,

  // Time-varying R0
  r0_current: 3.2,
  r0_7d_trend: -0.1,              // Decreasing (containment working)
  r0_calculation_timestamp: datetime()
})
```

### Multi-Layer Network Projection

```cypher
// Project multi-layer network for R0 calculation
CALL gds.graph.project(
  'multilayer_epidemic_graph',
  ['Equipment', 'Actor', 'Vulnerability'],
  {
    CONNECTS_TO: {
      type: 'CONNECTS_TO',
      properties: ['bandwidth', 'latency']
    },
    HAS_VULNERABILITY: {
      type: 'HAS_VULNERABILITY',
      properties: ['exploitability']
    },
    OPERATES: {
      type: 'OPERATES',
      properties: ['access_level']
    }
  }
)

// Calculate eigenvalue for adjacency matrix
CALL gds.eigenvector.stream('multilayer_epidemic_graph')
YIELD nodeId, score
WITH max(score) as lambda_max
RETURN lambda_max
```

### Ensemble R0 Calculation

```python
import numpy as np
from scipy.linalg import eigh
from typing import List, Dict

class R0Ensemble:
    """
    Multi-vulnerability R0 ensemble calculation.
    """

    def __init__(self, adjacency_matrix: np.ndarray):
        """
        Args:
            adjacency_matrix: Network adjacency matrix (N x N)
        """
        self.A = adjacency_matrix
        self.lambda_max = self._calculate_lambda_max()

    def _calculate_lambda_max(self) -> float:
        """Calculate largest eigenvalue of adjacency matrix."""
        eigenvalues, _ = eigh(self.A)
        return max(eigenvalues)

    def calculate_r0(self, beta: float, gamma: float) -> float:
        """
        Calculate R0 for single vulnerability.

        Args:
            beta: Transmission rate
            gamma: Recovery rate
        """
        return (beta / gamma) * self.lambda_max

    def calculate_ensemble_r0(
        self,
        vulnerabilities: List[Dict],
        n_samples: int = 1000
    ) -> Dict:
        """
        Calculate ensemble R0 with uncertainty.

        Args:
            vulnerabilities: List of {beta, gamma, beta_std, gamma_std}
            n_samples: Monte Carlo samples

        Returns:
            {mean, std, ci_95_lower, ci_95_upper, samples}
        """
        r0_samples = []

        for _ in range(n_samples):
            # Sample parameters with uncertainty
            total_r0 = 0
            for v in vulnerabilities:
                beta = np.random.normal(v['beta'], v.get('beta_std', 0.05))
                gamma = np.random.normal(v['gamma'], v.get('gamma_std', 0.01))
                gamma = max(gamma, 0.01)  # Prevent division by zero

                r0 = self.calculate_r0(beta, gamma)

                # Apply interaction effects
                if 'interaction_factor' in v:
                    r0 *= v['interaction_factor']

                total_r0 += r0

            r0_samples.append(total_r0)

        r0_samples = np.array(r0_samples)

        return {
            'mean': np.mean(r0_samples),
            'std': np.std(r0_samples),
            'ci_95_lower': np.percentile(r0_samples, 2.5),
            'ci_95_upper': np.percentile(r0_samples, 97.5),
            'epidemic_probability': np.mean(r0_samples > 1),
            'samples': r0_samples
        }

    def calculate_competing_r0(
        self,
        vuln_a: Dict,
        vuln_b: Dict,
        competition_strength: float = 0.5
    ) -> Dict:
        """
        Calculate R0 for competing vulnerabilities.

        When two vulnerabilities compete, the effective R0 is reduced.
        """
        r0_a = self.calculate_r0(vuln_a['beta'], vuln_a['gamma'])
        r0_b = self.calculate_r0(vuln_b['beta'], vuln_b['gamma'])

        # Competition reduces both R0s
        effective_r0_a = r0_a * (1 - competition_strength * (r0_b / (r0_a + r0_b)))
        effective_r0_b = r0_b * (1 - competition_strength * (r0_a / (r0_a + r0_b)))

        # Dominant strain
        dominant = 'A' if effective_r0_a > effective_r0_b else 'B'

        return {
            'r0_a_effective': effective_r0_a,
            'r0_b_effective': effective_r0_b,
            'dominant': dominant,
            'combined_r0': max(effective_r0_a, effective_r0_b)
        }
```

---

## Implementation Steps

### Step 1: Network Projection (Week 1)
- [ ] Create multi-layer GDS projection
- [ ] Implement eigenvalue calculation
- [ ] Store lambda_max per sector/subgraph

### Step 2: R0 Ensemble Service (Week 2)
- [ ] Implement R0Ensemble class
- [ ] Create Monte Carlo sampling
- [ ] Build competing/cooperating models
- [ ] Add confidence interval calculations

### Step 3: Neo4j Integration (Week 3)
- [ ] Store ensemble R0 results in Vulnerability nodes
- [ ] Create interaction relationships
- [ ] Build sector-specific R0 queries

### Step 4: API & Validation (Week 4)
- [ ] Create batch R0 calculation endpoint
- [ ] Validate against historical outbreaks
- [ ] Performance optimization
- [ ] Documentation

---

## Success Criteria

- [ ] Ensemble R0 with confidence intervals
- [ ] Multi-vulnerability interaction modeling
- [ ] Sector-specific R0 calculations
- [ ] API returns ensemble statistics
- [ ] Validated against WannaCry, NotPetya spread patterns

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Eigenvalue computation cost | Medium | Medium | Cache per subgraph, incremental updates |
| Interaction model accuracy | Medium | Medium | Validate against historical data |

---

## Dependencies

- Neo4j GDS library
- Graph projections operational
- Historical outbreak data for validation

---

## Memory Keys

- `gap-ml-007-models`: R0 model configurations
- `gap-ml-007-validation`: Validation results

---

## References

- Epidemic Theory: `mckenney-lacan-calculus-2025-11-28/Predictive_01_EPIDEMIC_THRESHOLDS_R0.md`
- Cypher Library: `mckenney-lacan-calculus-2025-11-28/neo4j-schema/02_MCKENNEY_LACAN_CYPHER_LIBRARY.cypher`
