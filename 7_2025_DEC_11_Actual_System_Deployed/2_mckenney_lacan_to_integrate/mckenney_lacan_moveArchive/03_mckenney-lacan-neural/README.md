# McKenney-Lacan Psychometric Calculus: Neural Implementation

A deep learning system implementing the McKenney-Lacan Psychometric Calculus for real-time persona analysis, dialectic tracking, and multi-person organa dynamics.

## Overview

This project implements a 5-layer neural ensemble:
1. **Feature Extraction** - BERT embeddings + linguistic analysis
2. **Multi-Task Encoder** - Register, Dialectic, Discourse, Traits classification
3. **Temporal Predictor** - Ψ(t) → Ψ(t+1) evolution
4. **Graph Neural Network** - Multi-person interaction dynamics
5. **Swarm Coordinator** - Collective emergence detection

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download pre-trained models
python scripts/download_models.py
```

## Quick Start

```python
from inference.realtime_analyzer import RealtimeAnalyzer

# Initialize
analyzer = RealtimeAnalyzer()

# Analyze utterance
result = await analyzer.process_utterance(
    person_id="user_1",
    text="I've been feeling overwhelmed lately...",
    timestamp=datetime.now()
)

# View persona state
print(result['psi_current'])  # Current Ψ
print(result['psi_predicted'])  # Predicted next state
```

## Project Structure

```
mckenney-lacan-neural/
├── data/              # Training and evaluation datasets
├── models/            # Neural network implementations
├── training/          # Training scripts
├── inference/         # Real-time analysis API
├── evaluation/        # Metrics and validation
├── utils/             # Helper functions
├── notebooks/         # Jupyter demos
└── docker/            # Containerization
```

## Documentation

- [Implementation Plan](../../../.gemini/antigravity/brain/.../implementation_plan.md)
- [Theoretical Foundation](../../../.gemini/antigravity/brain/.../mckenney_lacan_calculus_formalization.md)

## Applications

### 1. Therapeutic Monitoring
Track patient Ψ(t) trajectories through therapy sessions.

### 2. Executive Hiring (OrganaFit™)
Assess candidate-organization compatibility based on psychometric fit.

### 3. Team Dynamics
Optimize group composition for maximum emergence.

## License

MIT

## Citation

```bibtex
@software{mckenney_lacan_2025,
  title={McKenney-Lacan Psychometric Calculus: Neural Implementation},
  author={MMM Psychometric Therapy},
  year={2025}
}
```
