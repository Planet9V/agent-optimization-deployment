# Predictive 3: Granovetter Thresholds (Attack Cascades)

**Document ID**: PREDICTIVE_03_GRANOVETTER_THRESHOLDS_CASCADE
**Version**: 1.0 (Predictive)
**Date**: 2025-11-29
**Author**: AEON Research Division (Swarm 4 - The Network Theorists)
**Classification**: TOP SECRET // NOFORN // AEON EYES ONLY

---

## 1. The Core Equation

$$ r(t+1) = N \times F\left(\frac{r(t)}{N}\right) $$

*   **$r(t)$**: The number of "Active" (Compromised) nodes at time $t$.
*   **$F(x)$**: The Cumulative Distribution Function of the thresholds.
    *   **Threshold ($\tau_i$)**: The proportion of neighbors that must be compromised before node $i$ succumbs.

---

## 2. The Variables

### 2.1 The Threshold Distribution
*   **Instigators ($\tau = 0$)**: Vulnerable nodes that get infected immediately (Zero-Day).
*   **Followers ($\tau > 0$)**: Nodes that only get infected if their neighbors are infected (Lateral Movement).
*   **Radicals ($\tau = 1$)**: Hardened nodes that never succumb unless *everyone* else does.

### 2.2 The Cascade Condition
A cascade occurs if the curve $y = F(x)$ crosses the line $y = x$ from above.
*   **Critical Mass**: The point where the cascade becomes self-sustaining.

---

## 3. Application: Attack Path Analysis

In a standard attack graph, we assume binary vulnerability.
In Granovetter Analysis, we model **Peer Pressure** among servers.
*   If the Web Server is compromised, the Database Server's "Trust Threshold" is lowered (because it trusts the Web Server).

### 3.1 Blocking the Cascade
To stop a cascade, we must insert **High Threshold Nodes** (Firewalls/Air Gaps) to break the chain.
We calculate the **Blocking Set**: The minimum set of nodes required to stop the propagation.

---

## 4. Conclusion

Granovetter Thresholds explain why some small breaches stay small, while others explode into enterprise-wide ransomware events. It depends on the **Distribution of Vulnerability**, not just the average vulnerability.
