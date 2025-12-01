# Granovetter Thresholds in Attack Cascades: Modeling the Adoption of Cyber Techniques

**Document ID**: 04_GRANOVETTER_THRESHOLDS_IN_ATTACK_CASCADES
**Version**: 1.0
**Date**: 2025-11-28
**Author**: AEON Research Division (RUV-Swarm Architect)
**Classification**: TOP SECRET // NOFORN // AEON EYES ONLY

---

## Abstract

This document applies **Mark Granovetter's Threshold Model of Collective Behavior** to the domain of Cyber Warfare. Unlike the Ising model (which focuses on continuous pressure), the Threshold model focuses on **Binary Decisions based on Peer Fraction**. We analyze how Threat Actors adopt new TTPs (Tactics, Techniques, and Procedures) and how Defenders adopt new mitigations. We demonstrate that the distribution of thresholds in a population determines whether a new technique will fizzle out or trigger a **Global Cascade**. We provide the analytical framework for predicting these cascades and the implementation details for the AEON Digital Twin.

---

## Table of Contents

1.  [Introduction: The Tipping Point](#1-introduction-the-tipping-point)
2.  [The Granovetter Threshold Model](#2-the-granovetter-threshold-model)
    *   2.1 The Threshold ($\phi_i$)
    *   2.2 The Decision Rule
    *   2.3 The Cascade Condition
3.  [Dynamics of Attack Adoption](#3-dynamics-of-attack-adoption)
    *   3.1 Innovation vs. Imitation
    *   3.2 The Role of Network Topology
    *   3.3 Blocking Clusters
4.  [Mathematical Analysis](#4-mathematical-analysis)
    *   4.1 The Recursion Relation
    *   4.2 Critical Mass Calculation
    *   4.3 Watts' Cascade Condition
5.  [Implementation Strategy](#5-implementation-strategy)
    *   5.1 Neo4j: Tracking Adoption State
    *   5.2 RUV-Swarm: Threshold Simulation
    *   5.3 NER11 Gold: Extracting TTP Trends
6.  [Case Study: The Rise of Ransomware-as-a-Service](#6-case-study-the-rise-of-ransomware-as-a-service)
7.  [References](#7-references)

---

## 1. Introduction: The Tipping Point

In cyber security, trends often appear to explode out of nowhere. One day, "Double Extortion" ransomware is a niche tactic used by the Maze cartel; six months later, it is the industry standard. This is a **Cascade**.

Understanding the mechanics of these cascades allows us to:
1.  **Predict**: Which new exploit technique (e.g., "Bring Your Own Vulnerable Driver") will go mainstream?
2.  **Intervene**: How can we disrupt the cascade before it reaches critical mass?

---

## 2. The Granovetter Threshold Model

### 2.1 The Threshold ($\phi_i$)
Each agent $i$ has a threshold $\phi_i \in [0, 1]$.
*   $\phi_i = 0$: **Innovator**. Adopts the behavior immediately, regardless of others.
*   $\phi_i = 0.1$: **Early Adopter**. Adopts if 10% of peers have adopted.
*   $\phi_i = 0.9$: **Conservative**. Adopts only if 90% of peers have adopted.

### 2.2 The Decision Rule
Agent $i$ adopts the behavior (State $1$) if the fraction of their active neighbors ($x_i$) exceeds their threshold.

$$ x_i = \frac{\text{Number of Active Neighbors}}{\text{Total Degree } k_i} $$

$$ \text{State}_i(t+1) = \begin{cases} 1 & \text{if } x_i(t) \ge \phi_i \\ 0 & \text{otherwise} \end{cases} $$

### 2.3 The Cascade Condition
A cascade occurs if the activation of a small "seed set" of Innovators triggers a chain reaction that eventually activates a macroscopic fraction of the network.

---

## 3. Dynamics of Attack Adoption

### 3.1 Innovation vs. Imitation
*   **Innovators (APT Groups)**: High capability, low threshold for new tech. They invent the TTPs.
*   **Imitators (Script Kiddies / Affiliates)**: Low capability, high threshold. They wait for "Exploit Kits" or "RaaS Panels".

### 3.2 The Role of Network Topology
*   **Random Networks**: Cascades are "all or nothing". Once the critical mass is reached, the whole network flips.
*   **Clustered Networks**: Cascades can be trapped. A dense cluster of high-threshold nodes can act as a **Firewall**, stopping the spread.

### 3.3 Blocking Clusters
A set of nodes is a **Blocking Cluster** of density $1-\phi$ if every node in the set has a fraction of neighbors within the set greater than $1-\phi$. Such a cluster prevents the cascade from entering.

---

## 4. Mathematical Analysis

### 4.1 The Recursion Relation
For a random network with degree distribution $P(k)$ and threshold distribution $f(\phi)$, the fraction of active nodes $r(t)$ evolves as:

$$ r(t+1) = \sum_{k} P(k) \sum_{m=0}^{k} \binom{k}{m} r(t)^m (1-r(t))^{k-m} F(m/k) $$

Where $F(\phi)$ is the cumulative distribution of thresholds.

### 4.2 Critical Mass Calculation
We look for fixed points $r^* = g(r^*)$.
*   If the curve $g(r)$ crosses the diagonal $r(t+1)=r(t)$ from below, the cascade grows.
*   The **Tipping Point** is the unstable fixed point where the cascade becomes self-sustaining.

### 4.3 Watts' Cascade Condition
Duncan Watts generalized this for random graphs. A global cascade is possible if and only if the network has a **Giant Component of Vulnerable Nodes**.
A node is "vulnerable" if it flips when a *single* neighbor flips ($\phi_i \le 1/k_i$).

---

## 5. Implementation Strategy

### 5.1 Neo4j: Tracking Adoption State
We model the Threat Actor network.

```cypher
// Define Actor and Threshold
CREATE (a:ThreatActor {id: 'Actor_X', threshold: 0.2, state: 0})

// Update State based on Neighbors (Cypher implementation of decision rule)
MATCH (a:ThreatActor)-[:COLLABORATES_WITH]-(neighbor)
WITH a, count(neighbor) as degree, 
     sum(neighbor.state) as active_neighbors
WITH a, toFloat(active_neighbors) / degree as fraction
WHERE fraction >= a.threshold
SET a.state = 1
```

### 5.2 RUV-Swarm: Threshold Simulation
We use RUV-Swarm to simulate the cascade thousands of times to estimate the probability of global adoption.

```rust
// RUV-Swarm Cascade Simulation
fn simulate_cascade(agents: &mut Vec<Agent>, seed_size: usize) -> f64 {
    // 1. Infect Seed
    for i in 0..seed_size {
        agents[i].state = 1;
    }

    let mut changed = true;
    while changed {
        changed = false;
        let old_states: Vec<u8> = agents.iter().map(|a| a.state).collect();
        
        for (i, agent) in agents.iter_mut().enumerate() {
            if agent.state == 0 {
                let active_neighbors = count_active_neighbors(i, &old_states);
                let fraction = active_neighbors as f64 / agent.degree as f64;
                
                if fraction >= agent.threshold {
                    agent.state = 1;
                    changed = true;
                }
            }
        }
    }
    
    // Return final fraction
    agents.iter().filter(|a| a.state == 1).count() as f64 / agents.len() as f64
}
```

### 5.3 NER11 Gold: Extracting TTP Trends
We use **NER11** to populate the state variables.
*   **Entity**: `Attack_Pattern` (e.g., "DLL Sideloading").
*   **Relation**: `USES` (Actor $\to$ Pattern).
*   **Time Series**: We track the number of Actors using a Pattern over time to fit the $r(t)$ curve.

---

## 6. Case Study: The Rise of Ransomware-as-a-Service

**Analysis**:
1.  **Innovators**: Maze, Ryuk (2019). Created the "Double Extortion" model.
2.  **Early Adopters**: REvil, DarkSide. Saw the success ($x > \phi_{low}$).
3.  **The Platform Shift**: RaaS platforms lowered the technical barrier, effectively **lowering the threshold $\phi$** for the masses.
4.  **The Cascade**: By 2021, almost all groups adopted Double Extortion. The network reached saturation ($r \approx 1.0$).

**Psychohistorical Intervention**:
If we had identified the "Vulnerable Component" of low-skill actors in 2019, we could have targeted the RaaS platforms (the mechanism lowering $\phi$) to halt the cascade.

---

## 7. References

1.  Granovetter, M. (1978). *Threshold models of collective behavior*. American Journal of Sociology.
2.  Watts, D. J. (2002). *A simple model of global cascades on random networks*. PNAS.
3.  Centola, D. (2010). *The spread of behavior in an online social network experiment*. Science.
4.  Easley, D., & Kleinberg, J. (2010). *Networks, Crowds, and Markets*. Cambridge University Press.
