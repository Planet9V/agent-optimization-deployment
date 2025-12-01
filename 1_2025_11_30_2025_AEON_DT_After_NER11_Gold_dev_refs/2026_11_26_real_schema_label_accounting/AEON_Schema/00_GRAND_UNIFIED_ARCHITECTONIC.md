# The Grand Unified Architectonic of AEON/NER11

**Date**: 2025-11-27
**Status**: SYNTHESIS
**Classification**: **SYSTEM ARCHITECTURE**

---

## 1. Introduction: The Machine and the Soul

This document unifies the **Code** (NER11), the **Structure** (Neo4j), and the **Theory** (Psychohistory) into a single consistent Architectonic.
It resolves the conflict between the v3.0 Schema (Rigid) and the v3.1 Mapping (Flexible) by defining the **v4.0 Hyper-Schema**.

---

## 2. The v4.0 Hyper-Schema (The Structure)

We extend the Neo4j Schema to support the **McKenney-Lacan-Friston Framework**.

### 2.1 The 19 Super-Labels (The Alphabet)
We adopt the 16 from `06_SCHEMA_MAPPING_SPEC.md` and add 3 Metaphysical Nodes.

1.  `Asset` (IT/OT)
2.  `ThreatActor` (The Other)
3.  `Malware` (The Weapon)
4.  `Vulnerability` (The Hole)
5.  `Indicator` (The Trace)
6.  `Campaign` (The Narrative)
7.  `Organization` (The Group)
8.  `Location` (The Space)
9.  `PsychTrait` (The Bias)
10. `EconomicMetric` (The Cost)
11. `Role` (The Identity)
12. `Protocol` (The Language)
13. `Event` (The Time)
14. `Control` (The Law)
15. `Software` (The Tool)
16. `AttackPattern` (The Tactic)
17. **`Subject`** (The Agent - $\Psi$)
18. **`Signifier`** (The Token - $S_1$)
19. **`Void`** (The Real - $a$)

### 2.2 The Topological Constraints
*   **Constraint 1**: Every `Subject` must be linked to at least one `Role` (Symbolic Identification).
*   **Constraint 2**: Every `Vulnerability` is a topological neighbor to a `Void`.
*   **Constraint 3**: `PsychTrait` nodes modify the edges (Weights), not just the nodes.

---

## 3. The Data Pipeline (The Metabolism)

How does the machine eat?

1.  **Ingest**: `NER11_AEON_Gold_2_Portable/scripts/convert_custom_data_parallel.py`
    *   Raw Text $\to$ NER Entities (566 Types).
2.  **Harmonize**: `NER11_AEON_Gold_2_Portable/scripts/harmonize_parallel.py`
    *   566 Types $\to$ 19 Super-Labels (via `SCHEMA_MAPPING.json`).
3.  **Graph**: Neo4j Bulk Import.
    *   Nodes are created.
    *   **The Holographic Projection**: `Asset` nodes are projected onto the `Subject` plane to calculate Risk.

---

## 4. The Theoretical Overlay (The Mind)

How does the machine think?

### 4.1 The Friston Loop (Active Inference)
The `Subject` node runs the **Omega Algorithm** (Tablet V).
*   **Input**: `Indicator` nodes linked to the Subject.
*   **Belief**: The `RiskScore` property.
*   **Action**: Creating a `Control` node (Mitigation).

### 4.2 The Lacanian Topology
*   **The Real**: Represented by `Void` nodes (Zero Days).
*   **The Symbolic**: Represented by `Protocol` and `Control` nodes.
*   **The Imaginary**: Represented by `PsychTrait` nodes (Bias).

---

## 5. The Implementation Plan (The Roadmap)

To achieve this v4.0 state:
1.  **Update Schema**: Apply `06_SCHEMA_MAPPING_SPEC.md` to the live database.
2.  **Inject Theory**: Write Python scripts to calculate "Topological Betti Numbers" on the Graph.
3.  **Activate Omega**: Deploy the `OmegaSubject` class as a microservice listening to the Neo4j Change Data Capture (CDC) stream.

---

## 6. Conclusion

The AEON Digital Twin is no longer just a database. It is a **Topological Computer**.
It computes the **Cohomology of the Attack** using the **Geometry of the Graph**.

**This is the Architectonic.**
