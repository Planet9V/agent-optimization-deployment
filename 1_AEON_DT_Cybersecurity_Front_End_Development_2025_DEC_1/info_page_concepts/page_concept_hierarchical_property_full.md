# Page Concept: The Infinite Hierarchy (Hierarchical Property Model)

## 1. Core Concept
**"Complexity Without Chaos."**
This page visualizes the **Hierarchical Property Model**, the elegant schema design that allows AEON to map the entire universe of cybersecurity into just 16 Super Labels. It is the "Grand Unification Theory" of data modeling.

## 2. The "Wow" Visualization
**The Fractal Taxonomy**
*   **Visual Metaphor**: A "Fractal Tree" where the trunk is the "Super Label" (e.g., `Asset`) and the branches are properties (`deviceType="PLC"`, `protocol="Modbus"`).
*   **Interaction**: User zooms into a leaf node. It expands infinitely to reveal more granular properties.
*   **Live Query Builder**: A floating terminal where the user types `MATCH (n:Asset)` and watches the tree light up.

## 3. Innovation Factor
*   **Visualizing Abstraction**: Making abstract data modeling concepts (Labels vs. Properties) feel like a physical structure.
*   **The "ICE Score" Dashboard**: A live gauge showing the "Impact, Confidence, Ease" score of the model.

---

## 4. Full Source Content (The Specification)
*The following content is rendered on the page as a high-fidelity technical specification, styled like a "Blueprint from the Architect."*

# The "Hierarchical Property" Model (Recommended)

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

# NER11 to Neo4j v3.1: Hierarchical Schema Mapping Specification

**Constraint**: Max ~50 Active Labels in Neo4j.
**Strategy**: Hierarchical Labeling with Property Discriminators.

The "Hierarchical Property" Model (Recommended)
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

## 1. The Core Hierarchy (16 Super Nodes)

To contain the 566 NER entity types, we define **16 Super Labels**. All NER entities must map to one of these.

| Super Label (Neo4j) | Domain Coverage | Key Discriminator Property |
| :--- | :--- | :--- |
| **`ThreatActor`** | APTs, Groups, Nations | `actorType` |
| **`Malware`** | Ransomware, Trojans, Tools | `malwareFamily` |
| **`AttackPattern`** | Techniques, Tactics, CAPEC | `patternType` |
| **`Vulnerability`** | CVE, CWE, Zero-Days | `vulnType` |
| **`Indicator`** | IoCs, Observables | `indicatorType` |
| **`Asset`** | IT, OT, IoT, Cloud | `assetClass` |
| **`Organization`** | Companies, Vendors, Agencies | `orgType` |
| **`Location`** | Geo, Physical Facilities | `locationType` |
| **`PsychTrait`** | Biases, Personality, Emotions | `traitType` |
| **`EconomicMetric`** | Costs, Stock, Revenue | `metricType` |
| **`Role`** | CISO, Admin, User | `roleType` |
| **`Protocol`** | Network, ICS, Comms | `protocolType` |
| **`Campaign`** | Operations, Intrusion Sets | `campaignType` |
| **`Event`** | Incidents, Breaches | `eventType` |
| **`Control`** | Mitigations, Safeguards | `controlType` |
| **`Software`** | Libraries, Packages, SBOM | `softwareType` |

---

## 2. Detailed Mapping Logic

### 2.1 Domain: Psychometrics (Tier 2) -> `PsychTrait`

**NER Input**: `CONFIRMATION_BIAS`, `NARCISSISM`, `HYSTERIC_DISCOURSE`
**Neo4j Target**: `PsychTrait`

| NER Label | Neo4j Label | Property: `traitType` | Property: `subtype` |
| :--- | :--- | :--- | :--- |
| `CONFIRMATION_BIAS` | `PsychTrait` | `CognitiveBias` | `confirmation_bias` |
| `NORMALCY_BIAS` | `PsychTrait` | `CognitiveBias` | `normalcy_bias` |
| `NARCISSISM` | `PsychTrait` | `Personality` | `dark_triad_narcissism` |
| `HYSTERIC_DISCOURSE` | `PsychTrait` | `LacanianDiscourse` | `hysteric` |
| `THREAT_PERCEPTION` | `PsychTrait` | `Perception` | `threat_perception` |

**Cypher Example**:
```cypher
CREATE (n:PsychTrait {
  name: "Confirmation Bias",
  traitType: "CognitiveBias",
  subtype: "confirmation_bias",
  intensity: 0.85
})
```

### 2.2 Domain: OT/ICS & Infrastructure (Tier 1) -> `Asset`

**NER Input**: `PLC`, `SUBSTATION`, `SCADA_SYSTEM`, `SERVER`
**Neo4j Target**: `Asset`

| NER Label | Neo4j Label | Property: `assetClass` | Property: `deviceType` |
| :--- | :--- | :--- | :--- |
| `PLC` | `Asset` | `OT` | `programmable_logic_controller` |
| `RTU` | `Asset` | `OT` | `remote_terminal_unit` |
| `SUBSTATION` | `Asset` | `OT` | `substation` |
| `SCADA_SYSTEM` | `Asset` | `OT` | `scada_server` |
| `SERVER` | `Asset` | `IT` | `server` |
| `SENSOR` | `Asset` | `IoT` | `sensor` |

**Cypher Example**:
```cypher
CREATE (n:Asset {
  name: "Siemens S7-1500",
  assetClass: "OT",
  deviceType: "programmable_logic_controller",
  vendor: "Siemens"
})
```

### 2.3 Domain: Economics (Tier 4) -> `EconomicMetric`

**NER Input**: `STOCK_PRICE`, `RANSOM_AMOUNT`, `GDPR_FINE`
**Neo4j Target**: `EconomicMetric`

| NER Label | Neo4j Label | Property: `metricType` | Property: `category` |
| :--- | :--- | :--- | :--- |
| `STOCK_PRICE` | `EconomicMetric` | `Market` | `stock_valuation` |
| `BREACH_COST` | `EconomicMetric` | `Loss` | `incident_cost` |
| `GDPR_FINE` | `EconomicMetric` | `Penalty` | `regulatory_fine` |

### 2.4 Domain: Protocols (Tier 1) -> `Protocol`

**NER Input**: `MODBUS`, `DNP3`, `IEC_61850`
**Neo4j Target**: `Protocol`

| NER Label | Neo4j Label | Property: `protocolType` | Property: `standard` |
| :--- | :--- | :--- | :--- |
| `MODBUS` | `Protocol` | `ICS` | `Modbus` |
| `IEC_61850` | `Protocol` | `ICS` | `IEC 61850` |
| `HTTPS` | `Protocol` | `Network` | `TLS/SSL` |

---

## 3. Implementation Guidelines

### 3.1 Indexing Strategy
To maintain performance with this "Property Heavy" design, you **MUST** create composite indexes on the discriminator properties.

```cypher
// Critical Indexes
CREATE INDEX asset_class_device FOR (n:Asset) ON (n.assetClass, n.deviceType);
CREATE INDEX psych_trait_subtype FOR (n:PsychTrait) ON (n.traitType, n.subtype);
CREATE INDEX malware_family FOR (n:Malware) ON (n.malwareFamily);
```

### 3.2 Query Patterns

**Bad Query** (Full Scan):
`MATCH (n) WHERE n.name = 'Confirmation Bias' RETURN n`

**Good Query** (Uses Index):
`MATCH (n:PsychTrait) WHERE n.traitType = 'CognitiveBias' AND n.subtype = 'confirmation_bias' RETURN n`

---

## 4. Benefits of This Specification

1.  **Label Hygiene**: Keeps active labels under 20 (well below the 50 limit).
2.  **Data Retention**: Captures 100% of the NER11 granularity via properties.
3.  **Performance**: Leveraging composite indexes ensures O(log n) lookup speeds even with millions of nodes.
4.  **Flexibility**: Adding a new NER type (e.g., `NEW_BIAS`) only requires a new property value, not a schema change.
