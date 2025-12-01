# NER11 vs. Neo4j Gap Analysis Report

**Date**: 2025-11-26
**Status**: CRITICAL DISCONNECTS IDENTIFIED
**Reference Artifacts**:
1.  `01_NER11_ENTITY_INVENTORY.md` (566 NER Types)
2.  `02_NEO4J_SCHEMA_INVENTORY.md` (18 Neo4j Node Types)

---

## 1. Executive Summary

This report documents a **fundamental architectural mismatch** between the **NER11 Gold Standard Model** (trained for "Total Context Awareness") and the **AEON Cyber Digital Twin Neo4j Schema v3.0** (designed for "Standard Threat Intelligence").

*   **NER11 Capability**: Can identify 566 distinct entity types, ranging from specific malware families (`RANSOMWARE`) to psychological biases (`CONFIRMATION_BIAS`) and physical infrastructure (`SUBSTATION`).
*   **Neo4j Capability**: Can store only 18 generic node types (`ThreatActor`, `Asset`, `Malware`).
*   **The Gap**: Approximately **45% of the NER model's output has no valid destination** in the current graph schema.

**Verdict**: Deploying the current model with the current schema will result in massive data loss or "property stuffing" (dumping complex data into unstructured text fields), negating the value of the specialized training.

---

## 2. Detailed Gap Analysis by Domain

### Domain A: Psychometrics & Human Factors (Tier 2)
*   **NER11**: 60+ entities including `COGNITIVE_BIAS`, `PERSONALITY_TRAIT`, `DISCOURSE_POSITION`, `REAL_REGISTER`.
*   **Neo4j**: **ZERO** support. No nodes, no properties.
*   **Impact**: **100% Data Loss**. The model will detect "Confirmation Bias" in a threat actor's manifesto, but the graph cannot store it.
*   **Recommendation**: Create a `PsychProfile` node linked to `ThreatActor` or `User`.

### Domain B: Operational Technology (OT) & Physics (Tier 1 & 7)
*   **NER11**: Highly granular. `SUBSTATION`, `PLC`, `SCADA_SYSTEM`, `TRANSMISSION_LINE`, `SENSOR`.
*   **Neo4j**: Single generic `Asset` node.
*   **Impact**: **Semantic Flattening**. A "Nuclear Centrifuge" and a "Office Laptop" are both stored as `Asset`. You lose the ability to query "Show me all PLCs".
*   **Recommendation**: Use Neo4j secondary labels (e.g., `Asset:ICS:PLC`) or add an `assetClass` property taxonomy.

### Domain C: Economics & Business (Tier 4)
*   **NER11**: `STOCK_PRICE`, `REVENUE`, `GDPR_FINE`, `BREACH_COST`.
*   **Neo4j**: **ZERO** support.
*   **Impact**: **100% Data Loss**. Cannot graph the financial impact of a campaign.
*   **Recommendation**: Create `FinancialMetric` or `ImpactEvent` nodes.

### Domain D: Threat Actor Granularity (Tier 1)
*   **NER11**: Distinguishes `APT_GROUP`, `NATION_STATE`, `HACKTIVIST`, `CRIME_SYNDICATE`.
*   **Neo4j**: Single `ThreatActor` node with a generic `actorType` string property.
*   **Impact**: **Manageable**. Can be mapped to the `actorType` property, but graph queries will be slower/less precise than if they were distinct labels.

### Domain E: Malware Granularity (Tier 1)
*   **NER11**: Distinguishes `RANSOMWARE`, `WORM`, `TROJAN`, `ROOTKIT`.
*   **Neo4j**: Single `Malware` node with `malwareType` property.
*   **Impact**: **Manageable**. Similar to Threat Actors, this can be handled via properties.

---

## 3. Specific Entity-to-Node Mapping Failures

The following table highlights specific high-value NER entities that have **no clear home** in the schema.

| NER Entity | Best Current Neo4j Match | Loss of Fidelity |
| :--- | :--- | :--- |
| `CONFIRMATION_BIAS` | *None* | **Total** |
| `STOCK_PRICE` | *None* | **Total** |
| `SUBSTATION` | `Asset` | High (becomes generic) |
| `PLC` | `Asset` | High (becomes generic) |
| `IEC_61850` (Protocol) | *None* (maybe generic string?) | High |
| `MTBF` (Reliability) | *None* | **Total** |
| `CISO` (Role) | `User` | Medium (loss of role context) |
| `SECURITY_CULTURE` | `Organization` (property?) | High |
| `GEOPOLITICAL_RISK` | *None* | **Total** |

---

## 4. Remediation Options

### Option 1: "The Big Upgrade" (Recommended)
**Action**: Update Neo4j Schema to v3.1 to match NER11 capabilities.
*   **Add Nodes**: `PsychProfile`, `EconomicMetric`, `Protocol`, `Role`.
*   **Add Labels**: `Asset:ICS`, `Asset:IT`, `Asset:Facility`.
*   **Pros**: Unlocks full value of NER11. True "Digital Twin".
*   **Cons**: Requires database migration and query updates.

### Option 2: "The Great Filter" (Pragmatic)
**Action**: Filter out unsupported entities in the ingestion pipeline.
*   **Logic**: If NER detects `CONFIRMATION_BIAS`, ignore it.
*   **Pros**: Keeps schema clean and simple. Zero migration cost.
*   **Cons**: Wastes training effort. Ignores valuable context.

### Option 3: "Property Stuffing" (Quick Fix)
**Action**: Dump complex data into JSON blobs on existing nodes.
*   **Logic**: Store `CONFIRMATION_BIAS` as a JSON string in `ThreatActor.properties`.
*   **Pros**: Saves the data. No schema changes.
*   **Cons**: Data is "dead" (cannot be queried effectively).

---

## 5. Conclusion

The **NER11 model is significantly more advanced** than the current **Neo4j v3.0 schema**.

To avoid wasting the "Gold Standard" capabilities, **Option 1 (Schema Upgrade)** is strongly recommended. The graph should be elevated to meet the model, not the model dumbed down to fit the graph.
