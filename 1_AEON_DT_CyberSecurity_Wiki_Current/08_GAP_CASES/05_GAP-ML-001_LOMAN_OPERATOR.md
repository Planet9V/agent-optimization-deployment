# GAP-ML-001: Loman Operator (L-gGNN) Implementation

**File:** 05_GAP-ML-001_LOMAN_OPERATOR.md
**Gap ID:** GAP-ML-001
**Created:** 2025-11-30
**Priority:** CRITICAL
**Phase:** 2 - Core Math
**Effort:** XL (8+ weeks)
**Status:** NOT STARTED

---

## Problem Statement

**Current State:**
- Theoretical definition exists in documentation
- L-gGNN architecture described but not deployed
- LacanianGRUCell PyTorch code in documentation only
- No production inference capability

**Desired State:**
- Production L-gGNN running on GPU cluster
- Real-time processing of dialogue/event streams
- Integration with Neo4j for state updates
- Trained model with validated accuracy

---

## Technical Specification

### L-gGNN Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Loman Operator (L-gGNN)                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Input: G = (V, E, X) - Graph with node features            │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  LacanianGRUCell                      │   │
│  │                                                        │   │
│  │  CB5T Parameters: θ = [O, C, E, A, N] (per node)     │   │
│  │                                                        │   │
│  │  Reset Gate (Plasticity):                             │   │
│  │    r_t = σ(W_r[h_{t-1}, x_t] + b_r + λ_O * θ_O)      │   │
│  │                                                        │   │
│  │  Update Gate (Stability):                             │   │
│  │    z_t = σ(W_z[h_{t-1}, x_t] + b_z + λ_C*θ_C - λ_N*θ_N) │
│  │                                                        │   │
│  │  Candidate Hidden:                                    │   │
│  │    h̃_t = tanh(W_h[r_t ⊙ h_{t-1}, x_t] + b_h)        │   │
│  │                                                        │   │
│  │  Output:                                              │   │
│  │    h_t = (1 - z_t) ⊙ h_{t-1} + z_t ⊙ h̃_t            │   │
│  │                                                        │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                  │
│                    ┌──────▼──────┐                          │
│                    │  Readout    │                          │
│                    │  Layer      │                          │
│                    └──────┬──────┘                          │
│                           │                                  │
│  Output: Predictions for each RSI stave                     │
│    - Real (R): Trauma/Zero-day likelihood                   │
│    - Symbolic (S): Protocol compliance probability          │
│    - Imaginary (I): Perception/ego state                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### PyTorch Implementation (Reference)

```python
import torch
import torch.nn as nn
from torch_geometric.nn import MessagePassing

SCALING_FACTOR_O = 0.1  # Openness → Plasticity
SCALING_FACTOR_C = 0.1  # Conscientiousness → Stability
SCALING_FACTOR_N = 0.1  # Neuroticism → Instability

class LacanianGRUCell(nn.Module):
    """
    Gated Recurrent Unit with CB5T personality biases.
    Implements the Loman Operator for psychodynamic graph learning.
    """

    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.hidden_dim = hidden_dim

        # GRU weights
        self.W_r = nn.Linear(input_dim + hidden_dim, hidden_dim)
        self.W_z = nn.Linear(input_dim + hidden_dim, hidden_dim)
        self.W_h = nn.Linear(input_dim + hidden_dim, hidden_dim)

        # CB5T parameters (learnable per-node)
        self.O = nn.Parameter(torch.zeros(1))  # Openness
        self.C = nn.Parameter(torch.zeros(1))  # Conscientiousness
        self.E = nn.Parameter(torch.zeros(1))  # Extraversion
        self.A = nn.Parameter(torch.zeros(1))  # Agreeableness
        self.N = nn.Parameter(torch.zeros(1))  # Neuroticism

    def forward(self, x, h_prev, cb5t_params=None):
        """
        Args:
            x: Input features [batch, input_dim]
            h_prev: Previous hidden state [batch, hidden_dim]
            cb5t_params: Optional per-node CB5T parameters [batch, 5]
        """
        # Use provided CB5T or learned defaults
        if cb5t_params is not None:
            O, C, E, A, N = cb5t_params.unbind(dim=-1)
        else:
            O, C, E, A, N = self.O, self.C, self.E, self.A, self.N

        combined = torch.cat([h_prev, x], dim=-1)

        # Reset Gate (Plasticity - driven by Openness)
        bias_r = O * SCALING_FACTOR_O
        r_t = torch.sigmoid(self.W_r(combined) + bias_r)

        # Update Gate (Stability - Conscientiousness vs Neuroticism)
        bias_z = (C * SCALING_FACTOR_C) - (N * SCALING_FACTOR_N)
        z_t = torch.sigmoid(self.W_z(combined) + bias_z)

        # Candidate hidden state
        combined_reset = torch.cat([r_t * h_prev, x], dim=-1)
        h_tilde = torch.tanh(self.W_h(combined_reset))

        # Final hidden state
        h_t = (1 - z_t) * h_prev + z_t * h_tilde

        return h_t


class LomanOperator(MessagePassing):
    """
    Full Loman Operator with message passing on graphs.
    """

    def __init__(self, node_dim, hidden_dim, num_layers=3):
        super().__init__(aggr='mean')
        self.num_layers = num_layers

        # Stack of LacanianGRUCells
        self.cells = nn.ModuleList([
            LacanianGRUCell(node_dim if i == 0 else hidden_dim, hidden_dim)
            for i in range(num_layers)
        ])

        # RSI output heads
        self.real_head = nn.Linear(hidden_dim, 1)      # Real: trauma/zero-day
        self.symbolic_head = nn.Linear(hidden_dim, 1)  # Symbolic: protocol
        self.imaginary_head = nn.Linear(hidden_dim, 1) # Imaginary: perception

    def forward(self, x, edge_index, cb5t):
        """
        Args:
            x: Node features [num_nodes, node_dim]
            edge_index: Graph connectivity [2, num_edges]
            cb5t: CB5T parameters per node [num_nodes, 5]
        """
        h = torch.zeros(x.size(0), self.cells[0].hidden_dim, device=x.device)

        for cell in self.cells:
            # Message passing + GRU update
            messages = self.propagate(edge_index, x=x)
            h = cell(messages, h, cb5t)

        # RSI predictions
        real = torch.sigmoid(self.real_head(h))
        symbolic = torch.sigmoid(self.symbolic_head(h))
        imaginary = torch.sigmoid(self.imaginary_head(h))

        return {
            'real': real,
            'symbolic': symbolic,
            'imaginary': imaginary,
            'hidden': h
        }
```

---

## Implementation Steps

### Step 1: Infrastructure (Week 1-2)
- [ ] Provision GPU infrastructure (CUDA capable)
- [ ] Set up PyTorch + PyTorch Geometric environment
- [ ] Create model repository structure
- [ ] Set up MLflow for experiment tracking

### Step 2: Data Pipeline (Week 3-4)
- [ ] Extract training data from Neo4j (actors, relationships)
- [ ] Create CB5T feature extraction from psychometric properties
- [ ] Build graph batching pipeline
- [ ] Implement train/val/test splits

### Step 3: Model Development (Week 5-6)
- [ ] Implement LacanianGRUCell
- [ ] Implement LomanOperator
- [ ] Create training loop with loss functions
- [ ] Implement RSI prediction heads

### Step 4: Training (Week 7)
- [ ] Train on historical incident data
- [ ] Hyperparameter tuning
- [ ] Cross-validation
- [ ] Model selection

### Step 5: Deployment (Week 8+)
- [ ] Export model to ONNX format
- [ ] Create FastAPI inference service
- [ ] Integrate with Neo4j triggers
- [ ] Performance optimization

---

## Success Criteria

- [ ] L-gGNN model trained with >80% accuracy on test set
- [ ] Inference latency <50ms per graph
- [ ] Integration with Neo4j operational
- [ ] RSI predictions validated against known incidents
- [ ] Model deployed and serving predictions

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Insufficient training data | Critical | Medium | Synthetic data generation, transfer learning |
| GPU resource constraints | High | Medium | Cloud GPU provisioning, model optimization |
| Overfitting | Medium | Medium | Regularization, early stopping, cross-validation |

---

## Dependencies

- GPU infrastructure
- Labeled training data from historical incidents
- Phase 1 gaps complete (temporal versioning for training data)
- Neo4j CB5T properties populated

---

## Memory Keys

- `gap-ml-001-architecture`: Model architecture decisions
- `gap-ml-001-training`: Training configuration and results
- `gap-ml-001-deployment`: Deployment configuration

---

## References

- Theory: `mckenney-lacan-calculus-2025-11-28/Background_theory/The Loman Operator_ A Topological Score of Act I.md`
- GGNN Spec: `mckenney-lacan-calculus-2025-11-28/mckenney-lacan_music_10_scores_classics/Simulating Calculus with GGNN.md`
