# Strategic Schema-Model Alignment Plan

**Date**: 2025-11-26
**Status**: DRAFT FOR DECISION
**Inputs**:
1.  `03_GAP_ANALYSIS_REPORT.md` (Functional Needs)
2.  `AEON_entity_expansion_impact_assessment.md` (Operational Constraints)

---

## 1. Executive Summary

We face a classic **"Expressiveness vs. Performance" trade-off**.
*   **The Model (NER11)** wants to express 566 distinct concepts (Psychology, Physics, Economics).
*   **The Database (Neo4j)** will collapse under the weight of 560+ labels (Index overhead, Query complexity).

**Strategic Goal**: Preserve the *richness* of the NER11 data without *breaking* the Neo4j architecture.

---

## 2. Strategic Options

### Option A: The "Hierarchical Property" Model (Recommended)
**Concept**: Cap labels at ~60. Use strict property taxonomies to capture granularity.
**Mechanism**:
*   **Psychometrics**: Create a single `PsychTrait` label. Use properties `type="CognitiveBias"`, `name="Confirmation Bias"`.
*   **OT/ICS**: Keep `Asset` label. Add properties `domain="ICS"`, `deviceType="PLC"`, `protocol="Modbus"`.
*   **Economics**: Create `ImpactMetric` label. Use properties `currency="USD"`, `amount=50000`, `category="Ransom"`.

**SWOT Analysis**:
*   **Strengths**: High performance (O(60) complexity). Native Cypher support. Easy to index specific properties.
*   **Weaknesses**: Queries become verbose (`MATCH (n:Asset) WHERE n.deviceType = 'PLC'`). Schema enforcement moves to application logic.
*   **Opportunities**: Aligns perfectly with the "Impact Assessment" recommendation.
*   **Threats**: "Property stuffing" can lead to sparse tables if not managed well.

**ICE Score**:
*   **Impact**: High (8/10) - Saves the DB, keeps most data.
*   **Confidence**: High (9/10) - Standard Neo4j best practice.
*   **Ease**: High (8/10) - No new infra, just schema discipline.
*   **Total**: **25/30**

---

### Option B: The "Vector-Enhanced" Graph (Advanced)
**Concept**: Offload semantic nuance to the Vector Database (Qdrant), keep Graph structural.
**Mechanism**:
*   **Neo4j**: Stores only structural nodes (`ThreatActor`, `Asset`, `Attack`).
*   **Qdrant**: Stores the full JSON profile (Psych, Econ, Physics) as a vector embedding + payload.
*   **Link**: Neo4j nodes contain a `vectorId` pointing to Qdrant.
*   **Query**: "Find actors with *narcissistic tendencies*" -> Query Qdrant -> Return IDs -> Match in Neo4j.

**SWOT Analysis**:
*   **Strengths**: Infinite expressiveness. Zero graph schema bloat. "Fuzzy" search capabilities.
*   **Weaknesses**: Complex "Split-Brain" queries (Graph + Vector). Higher latency for simple lookups.
*   **Opportunities**: Leverages the "already deployed" Qdrant instance. Future-proof for AI agents.
*   **Threats**: Data synchronization issues between Neo4j and Qdrant.

**ICE Score**:
*   **Impact**: Very High (9/10) - True "AI-Native" architecture.
*   **Confidence**: Medium (6/10) - Complex integration risk.
*   **Ease**: Low (4/10) - Requires significant query logic rewriting.
*   **Total**: **19/30**

---

### Option C: The "Polyglot Sidecar" (Data Lake)
**Concept**: Graph for connections, Document Store for details.
**Mechanism**:
*   **Neo4j**: Stores the "Skeleton" (Who talks to Whom).
*   **MongoDB/Elastic**: Stores the "Flesh" (Full 566-field documents).
*   **Link**: Neo4j nodes store a `docId`.

**SWOT Analysis**:
*   **Strengths**: Zero data loss. Perfect for reporting. Simple to implement.
*   **Weaknesses**: Adds a 3rd database technology to the stack (Maintenance burden). Graph queries cannot easily filter by document properties.
*   **Opportunities**: Easy to dump raw NER output.
*   **Threats**: "Portable" package becomes bloated with multiple DB containers.

**ICE Score**:
*   **Impact**: Medium (6/10) - Good for storage, bad for graph analysis.
*   **Confidence**: High (8/10) - Proven pattern.
*   **Ease**: Medium (5/10) - Infrastructure heaviness.
*   **Total**: **19/30**

---

## 3. Detailed Implementation Plan (for Option A)

To bridge the gap using **Option A**, we must define the **Target Schema (v3.1)**:

1.  **New Core Labels (Add ~10-15)**:
    *   `PsychTrait` (for Bias, Personality)
    *   `EconomicEvent` (for Financial Impact)
    *   `Protocol` (for OT comms)
    *   `Role` (for CISO, Admin)
    *   `Location` (Physical)

2.  **Property Taxonomies**:
    *   **Entity**: `Asset`
        *   **Property**: `assetClass` (Values: `IT`, `OT`, `IoT`)
        *   **Property**: `deviceType` (Values: `PLC`, `Server`, `Sensor`)
    *   **Entity**: `PsychTrait`
        *   **Property**: `traitType` (Values: `Bias`, `Personality`, `Discourse`)
        *   **Property**: `intensity` (Float: 0.0 - 1.0)

3.  **Ingestion Logic Update**:
    *   **Mapper**: A script must map NER labels to (Label + Property) pairs.
    *   *Example*: NER `CONFIRMATION_BIAS` -> Neo4j `(n:PsychTrait {traitType: 'Bias', name: 'Confirmation Bias'})`

---

## 4. Final Recommendation

**Adopt Option A (Hierarchical Property Model).**

*   **Why**: It balances the *need for data* with the *need for speed*. It avoids the operational catastrophe of 560 labels while still capturing the essence of the NER model's output.
*   **Next Step**: Create the `v3.1_SCHEMA_MAPPING.json` to define exactly how each of the 566 NER entities maps to the ~60 Neo4j labels.
