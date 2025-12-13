# Psychohistory Mathemathical Schema

This document defines the core mathematical schemas used in the Psychohistory engine, corresponding to the `ingest_demographics.py` implementation.

## 1. Monad Level (The Individual)

**Concept**: The Monad is defined by a **Markov Blanket**, a statistical boundary separating internal states from external states.

**Properties**:
*   **Structure**: $\text{Monad} = \{ Internal, Sensory, Active \}$
*   **Formula (Free Energy)**:
    $$ F = \sum (s - \mu)^2 $$
    Where:
    *   $s$ = Sensory Input (The "Real")
    *   $\mu$ = Internal Belief/Prediction (The "Symbolic")
    *   $F$ = Variational Free Energy (Surprise/Entropy)

## 2. Dyad Level (The Relationship)

**Concept**: Relationships are modeled as coupled differential equations (Gottman/Lewin).

**Properties**:
*   **Formula (Influence)**:
    $$ \frac{dW}{dt} = I + rW + \alpha(H) $$
    Where:
    *   $W$ = State of Agent W (e.g., Affect)
    *   $I$ = Inertia (Internal State)
    *   $r$ = Dampening factor
    *   $\alpha(H)$ = Influence function of Agent H

## 3. Population Level (Sociophysics)

**Concept**: Large-scale group dynamics modeled using Statistical Physics (Ising Model).

**Properties**:
*   **Social Temperature ($T$)**:
    $$ T = \sigma^2 = \frac{1}{N} \sum (x_i - \bar{x})^2 $$
    *   High $T$: High social volatility / panic.
    *   Low $T$: Rigid social order.

*   **Magnetization ($M$)**:
    $$ M = \frac{1}{N} \sum s_i $$
    *   Where $s_i \in \{-1, +1\}$ (Binary opinion)
    *   $M \approx 0$: Disordered / No consensus.
    *   $M \approx \pm 1$: Total consensus (Ferromagnetic state).
