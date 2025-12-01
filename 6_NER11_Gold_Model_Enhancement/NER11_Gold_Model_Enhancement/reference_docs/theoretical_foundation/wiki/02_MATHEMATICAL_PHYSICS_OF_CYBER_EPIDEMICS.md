# Mathematical Physics of Cyber Epidemics: Thresholds, Topology, and R₀

**Document ID**: 02_MATHEMATICAL_PHYSICS_OF_CYBER_EPIDEMICS
**Version**: 1.0
**Date**: 2025-11-28
**Author**: AEON Research Division (RUV-Swarm Architect)
**Classification**: TOP SECRET // NOFORN // AEON EYES ONLY

---

## Abstract

This document provides a rigorous mathematical treatment of **Cyber Epidemiology**—the study of how malware, exploits, and information propagate through digital networks. We move beyond simple biological analogies to apply **Spectral Graph Theory** and **Non-Equilibrium Statistical Physics**. We derive the **Epidemic Threshold** ($R_0$) for arbitrary network topologies, demonstrating that in scale-free cyber networks (where $P(k) \sim k^{-\gamma}$), the epidemic threshold approaches zero, implying that even weak viruses can persist indefinitely. We provide the implementation details for calculating the **Spectral Radius** ($\lambda_{max}$) of the adjacency matrix using **Neo4j GDS** and simulating the propagation dynamics using **RUV-Swarm**.

---

## Table of Contents

1.  [Introduction: The Physics of Contagion](#1-introduction-the-physics-of-contagion)
2.  [Classical Compartmental Models](#2-classical-compartmental-models)
    *   2.1 The SIR Model (Susceptible-Infected-Recovered)
    *   2.2 The SIS Model (Susceptible-Infected-Susceptible)
    *   2.3 The Cyber-Specific SEI Model (Susceptible-Exposed-Infected)
3.  [Network Epidemiology](#3-network-epidemiology)
    *   3.1 The Adjacency Matrix ($A$)
    *   3.2 The Spectral Radius ($\lambda_{max}$)
    *   3.3 The Vanishing Threshold in Scale-Free Networks
4.  [The Master Equation of Cyber Spread](#4-the-master-equation-of-cyber-spread)
    *   4.1 Derivation of the Threshold Condition
    *   4.2 The Role of the spectral gap
5.  [Implementation Strategy](#5-implementation-strategy)
    *   5.1 Neo4j: Calculating Eigenvalues
    *   5.2 RUV-Swarm: Agent-Based Simulation
    *   5.3 NER11 Gold: Parameter Estimation ($\beta$, $\gamma$)
6.  [Case Study: The Log4j Cascade](#6-case-study-the-log4j-cascade)
7.  [References](#7-references)

---

## 1. Introduction: The Physics of Contagion

In the context of the AEON Digital Twin, a "contagion" is any self-replicating entity or state. This includes:
*   **Worms/Viruses**: Self-propagating code (e.g., WannaCry).
*   **Botnets**: Recruitment of nodes into a command structure (e.g., Mirai).
*   **Patching**: The "contagion" of immunity (e.g., Windows Update).
*   **Fear/Hype**: The spread of information about a threat.

The fundamental question of Psychohistory is: **"Will this contagion die out, or will it become an epidemic?"** The answer lies in the **Basic Reproduction Number** ($R_0$).

---

## 2. Classical Compartmental Models

### 2.1 The SIR Model (Susceptible-Infected-Recovered)
Applicable to **Patchable Vulnerabilities**. Once a node is infected and then patched (Recovered), it cannot be infected again.

$$
\begin{aligned}
\frac{dS}{dt} &= -\beta S I \\
\frac{dI}{dt} &= \beta S I - \gamma I \\
\frac{dR}{dt} &= \gamma I
\end{aligned}
$$

*   $\beta$: Infection rate (probability of infection per contact).
*   $\gamma$: Recovery rate (patching speed).

**Threshold**: An epidemic occurs if $R_0 = \frac{\beta}{\gamma} > 1$.

### 2.2 The SIS Model (Susceptible-Infected-Susceptible)
Applicable to **Re-infectable Systems** (e.g., credential theft, phishing). A node can be cleaned but remains vulnerable to re-infection.

$$
\begin{aligned}
\frac{dS}{dt} &= -\beta S I + \gamma I \\
\frac{dI}{dt} &= \beta S I - \gamma I
\end{aligned}
$$

**Steady State**: The infection becomes endemic if $R_0 > 1$, settling at $I^* = 1 - \frac{1}{R_0}$.

### 2.3 The Cyber-Specific SEI Model (Susceptible-Exposed-Infected)
Applicable to **Zero-Day Exploits**.
*   **Exposed (E)**: A node has the vulnerability but hasn't been exploited yet.
*   **Infected (I)**: The exploit has been triggered.

---

## 3. Network Epidemiology

Classical models assume **Homogeneous Mixing** (everyone contacts everyone). Cyber networks are **Heterogeneous**. Some nodes (Hubs) have thousands of connections; others (Leaves) have few.

### 3.1 The Adjacency Matrix ($A$)
Let $A$ be the adjacency matrix of the AEON graph, where $A_{ij} = 1$ if node $i$ connects to node $j$, and $0$ otherwise.

### 3.2 The Spectral Radius ($\lambda_{max}$)
The **Spectral Radius** is the largest eigenvalue of $A$. It is the single most important number for predicting viral spread on a graph.

$$ A \mathbf{v} = \lambda \mathbf{v} $$

### 3.3 The Vanishing Threshold in Scale-Free Networks
For a random network (Erdős-Rényi), the threshold is finite. However, the internet is **Scale-Free** ($P(k) \sim k^{-\gamma}$, typically $2 < \gamma < 3$).

**Theorem (Pastor-Satorras & Vespignani)**:
In a scale-free network of infinite size, the epidemic threshold approaches zero.
$$ \lambda_{max} \to \infty \implies R_0 \to \infty $$

**Implication**: In the AEON Digital Twin, **there is no safety threshold**. Even a virus with a tiny $\beta$ (low infectivity) will eventually saturate the network if it can reach the Hubs. **Defense must focus on Hub immunization.**

---

## 4. The Master Equation of Cyber Spread

We define the probability $p_i(t)$ that node $i$ is infected at time $t$. In the **Quenched Mean-Field Approximation**:

$$ \frac{dp_i(t)}{dt} = -\gamma p_i(t) + \beta [1 - p_i(t)] \sum_{j=1}^{N} A_{ij} p_j(t) $$

### 4.1 Derivation of the Threshold Condition
Linearizing around the disease-free state ($p_i \approx 0$):

$$ \frac{dp_i}{dt} \approx -\gamma p_i + \beta \sum_{j} A_{ij} p_j $$

In vector notation:
$$ \frac{d\mathbf{p}}{dt} = (\beta A - \gamma I) \mathbf{p} $$

The solution grows exponentially if the largest eigenvalue of the matrix $(\beta A - \gamma I)$ is positive.
$$ \beta \lambda_{max}(A) - \gamma > 0 $$

**The Cyber Epidemic Threshold**:
$$ \tau = \frac{\beta}{\gamma} > \frac{1}{\lambda_{max}(A)} $$

---

## 5. Implementation Strategy

### 5.1 Neo4j: Calculating Eigenvalues
We use the **Neo4j Graph Data Science (GDS)** library to estimate Eigenvector Centrality, which converges to the principal eigenvector.

```cypher
// 1. Project the Graph
CALL gds.graph.project(
  'cyber_network',
  'Asset',
  'CONNECTS_TO'
);

// 2. Calculate Eigenvector Centrality
CALL gds.eigenvector.stream('cyber_network')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).id AS asset, score
ORDER BY score DESC
LIMIT 10;

// Note: The 'score' is proportional to the eigenvector component v_i.
// To find lambda_max, we can use the Power Iteration method via RUV-Swarm.
```

### 5.2 RUV-Swarm: Agent-Based Simulation
We spawn a swarm of agents where each agent represents a node.

```rust
// RUV-Swarm Simulation Logic (Rust/WASM)
struct NodeAgent {
    id: String,
    state: State, // Susceptible, Infected, Recovered
    neighbors: Vec<String>,
    beta: f64,
    gamma: f64,
}

impl NodeAgent {
    fn step(&mut self, neighbor_states: &HashMap<String, State>) {
        match self.state {
            State::Susceptible => {
                // Calculate infection probability based on infected neighbors
                let infected_neighbors = self.neighbors.iter()
                    .filter(|n| neighbor_states.get(*n) == Some(&State::Infected))
                    .count();
                
                let prob = 1.0 - (1.0 - self.beta).powi(infected_neighbors as i32);
                if random() < prob {
                    self.state = State::Infected;
                }
            },
            State::Infected => {
                if random() < self.gamma {
                    self.state = State::Recovered;
                }
            },
            State::Recovered => {} // Permanent immunity (SIR)
        }
    }
}
```

### 5.3 NER11 Gold: Parameter Estimation ($\beta$, $\gamma$)
We use the **NER11 Gold Standard** model to extract $\beta$ and $\gamma$ from Threat Intelligence Reports.

*   **$\beta$ (Infectivity)**: Derived from keywords like "highly contagious", "wormable", "zero-click", "RCE".
    *   *Mapping*: "Zero-click" $\to \beta = 0.9$; "Phishing required" $\to \beta = 0.1$.
*   **$\gamma$ (Recovery)**: Derived from "patch available", "complex mitigation", "vendor response".
    *   *Mapping*: "Auto-update" $\to \gamma = 0.9$; "No patch" $\to \gamma = 0.0$.

---

## 6. Case Study: The Log4j Cascade

Applying this framework to the **Log4j (Log4Shell)** crisis:
1.  **Topology**: The dependency graph of Java applications. Log4j was a **Super-Hub** (extremely high Eigenvector Centrality).
2.  **Parameters**:
    *   $\beta \approx 1.0$ (Trivial to exploit, simple string).
    *   $\gamma \approx 0.0$ (Initially no patch, difficult to identify).
3.  **Result**: $R_0 \to \infty$. Immediate, global saturation.
4.  **Prediction**: A Psychohistory engine running this model would have flagged `log4j-core` as a "Critical Structural Weakness" years before the exploit, purely based on its $\lambda_{max}$ contribution.

---

## 7. References

1.  Pastor-Satorras, R., & Vespignani, A. (2001). *Epidemic spreading in scale-free networks*. Physical Review Letters.
2.  Newman, M. E. J. (2002). *Spread of epidemic disease on networks*. Physical Review E.
3.  Chakrabarti, D., et al. (2008). *Epidemic thresholds in real networks*. ACM TISSEC.
4.  Kephart, J. O., & White, S. R. (1991). *Directed-graph epidemiological models of computer viruses*. IEEE S&P.
