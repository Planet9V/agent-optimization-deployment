# Deep Validation Report: NER11 & Neo4j Schema

**Date**: 2025-11-26
**Status**: CRITICAL FINDINGS - DISCREPANCIES IDENTIFIED
**Inspector**: Antigravity (Deep Inspection Agent)

---

## 1. Executive Summary
A "Deep Inspection" was performed on the NER11 Gold Standard training data and the running AEON Neo4j instance. **Significant discrepancies** were found between the documentation (Reference Artifacts) and the ground truth (Files & Database).

*   **NER11 Inventory**: Documentation claims **566** entity types. Actual training data contains **60** unique labels.
*   **Neo4j Schema**: Documentation claims **18** node types. Actual database contains **24** node types, with a strong divergence towards OT/ICS specifics (e.g., `EnergyDevice`, `WaterSystem`) not reflected in the docs.

This report provides the **EXHAUSTIVE** truth of the current state and proposes a **Hierarchical Label Design** to align the 566 intended concepts with a streamlined Neo4j schema (<30 labels).

---

## 2. NER11 Gold Standard Validation

### 2.1 The Claim
*   **Source**: `01_NER11_ENTITY_INVENTORY.md`
*   **Stated Count**: 566 Entity Types
*   **Structure**: 11 Tiers (Technical, Psychometric, etc.)

### 2.2 The Reality (Ground Truth)
*   **Source**: `NER11_AEON_Gold_2_Portable/NER11_AWS_Package/final_training_set/train.spacy`
*   **Actual Count**: **60** Unique Labels
*   **Observation**: The current training set uses high-level categories. It does **NOT** currently support granular entities like `NATION_STATE`, `RANSOMWARE`, or `BIG_5_OPENNESS` as distinct labels. These are likely subsumed under `THREAT_ACTOR`, `MALWARE`, and `PERSONALITY` respectively.

### 2.3 Validated Label List (60)
The following are the **ONLY** labels currently trainable:
1.  `ANALYSIS`
2.  `APT_GROUP`
3.  `ATTACK_TECHNIQUE`
4.  `ATTRIBUTES`
5.  `COGNITIVE_BIAS`
6.  `COMPONENT`
7.  `CONTROLS`
8.  `CORE_ONTOLOGY`
9.  `CVE`
10. `CWE`
11. `CWE_WEAKNESS`
12. `CYBER_SPECIFICS`
13. `DEMOGRAPHICS`
14. `DETERMINISTIC_CONTROL`
15. `DEVICE`
16. `ENGINEERING_PHYSICAL`
17. `FACILITY`
18. `HAZARD_ANALYSIS`
19. `IEC_62443`
20. `IMPACT`
21. `INDICATOR`
22. `LACANIAN`
23. `LOCATION`
24. `MALWARE`
25. `MATERIAL`
26. `MEASUREMENT`
27. `MECHANISM`
28. `META`
29. `METADATA`
30. `MITIGATION`
31. `MITRE_EM3D`
32. `NETWORK`
33. `OPERATING_SYSTEM`
34. `OPERATIONAL_MODES`
35. `ORGANIZATION`
36. `PATTERNS`
37. `PERSONALITY`
38. `PHYSICAL`
39. `PRIVILEGE_ESCALATION`
40. `PROCESS`
41. `PRODUCT`
42. `PROTOCOL`
43. `RAMS`
44. `ROLES`
45. `SECTOR`
46. `SECTORS`
47. `SECURITY_TEAM`
48. `SOFTWARE_COMPONENT`
49. `STANDARD`
50. `SYSTEM_ATTRIBUTES`
51. `TACTIC`
52. `TECHNIQUE`
53. `TEMPLATES`
54. `THREAT_ACTOR`
55. `THREAT_MODELING`
56. `THREAT_PERCEPTION`
57. `TIME_BASED_TREND`
58. `TOOL`
59. `VENDOR`
60. `VULNERABILITY`

---

## 3. Neo4j Schema Validation

### 3.1 The Claim
*   **Source**: `02_NEO4J_SCHEMA_INVENTORY.md`
*   **Stated Count**: 18 Node Types
*   **Focus**: General Cyber Threat Intelligence

### 3.2 The Reality (Ground Truth)
*   **Source**: `openspg-neo4j` Container (Cypher Query)
*   **Actual Count**: **24** Node Types
*   **Observation**: The actual schema is **OT/ICS Heavy**. It includes nodes like `Substation`, `TransmissionLine`, and `WaterSystem` which are completely missing from the documentation. Conversely, documented nodes like `Campaign` and `Indicator` are missing or named differently.

### 3.3 Validated Schema (24 Nodes)
| Node Label | Observed Properties (Sample) |
| :--- | :--- |
| `AttackPattern` | `id`, `name`, `description`, `patternId` |
| `AttackTechnique` | `id`, `name`, `description`, `tactics`, `is_subtechnique`, `stix_id` |
| `ComplianceFramework` | `id`, `name`, `description`, `frameworkId` |
| `CVE` | `id`, `description`, `cvssScore`, `severity`, `publicationDate` |
| `DistributedEnergyResource` | `id`, `name`, `derId` |
| `EnergyDevice` | `id`, `name`, `deviceId`, `deviceType` |
| `EnergyManagementSystem` | `id`, `name`, `emsId` |
| `EnergyProperty` | `id`, `name`, `propertyId` |
| `Exploit` | `id`, `name`, `description`, `exploitId` |
| `IncidentReport` | `id`, `description`, `incidentId`, `severity` |
| `Location` | `id`, `city`, `country`, `locationId` |
| `MalwareVariant` | `id`, `name`, `malwareId`, `malwareType` |
| `Measurement` | `id`, `name`, `measurementId` |
| `Mitigation` | `id`, `name`, `description`, `stix_id` |
| `NERCCIPStandard` | `id`, `name`, `standardId` |
| `Organization` | `id`, `name`, `organizationId`, `sector` |
| `Sector` | `id`, `name`, `sectorId` |
| `Software` | `id`, `name`, `description`, `type`, `stix_id` |
| `Substation` | `id`, `name`, `substationId`, `voltageClass` |
| `ThreatActor` | `id`, `name`, `description`, `actorId`, `aliases` |
| `TransmissionLine` | `id`, `name`, `lineId` |
| `VulnerabilityReport` | `id`, `description`, `reportId` |
| `WaterProperty` | `id`, `name` |
| `WaterSystem` | `id`, `name`, `waterSystemId` |

### 3.4 Validated Relationships (11 Types)
1.  `BELONGS_TO_SECTOR`
2.  `MITIGATED_BY`
3.  `MITIGATES`
4.  `OPERATES_IN`
5.  `PARENT_OF`
6.  `REVOKED_BY`
7.  `REVOKED_BY_REV`
8.  `SUBTECHNIQUE_OF`
9.  `TARGETS_SECTOR`
10. `USED_BY`
11. `USES`

---

## 4. Hierarchical Label Design Plan

To support the **566** intended concepts within a manageable Neo4j schema (<30 labels), we propose a **Hierarchical Property Model**.

### 4.1 Design Principle
**Label = Class (Broad Category)**
**Property = Subclass (Specific Type)**

Instead of creating a node label for every specific type (e.g., `(n:Ransomware)`), we use a broad label (e.g., `(n:Malware)`) and specify the type in a property (`type: "Ransomware"`). This keeps the graph schema clean and performant while retaining full granularity.

### 4.2 Proposed Hierarchy (Top 10 Examples)

#### 1. Equipment Hierarchy
*   **Neo4j Label**: `Equipment` (or `Asset`)
*   **Subtypes (via `type` property)**:
    *   `PLC`
    *   `RTU`
    *   `HMI`
    *   `Sensor`
    *   `Actuator`
    *   `Server`
    *   `Workstation`
*   **Example Cypher**:
    ```cypher
    CREATE (n:Equipment {
      name: "Siemens S7-1200",
      type: "PLC",
      subtype: "S7-1200",
      vendor: "Siemens"
    })
    ```

#### 2. Threat Actor Hierarchy
*   **Neo4j Label**: `ThreatActor`
*   **Subtypes**:
    *   `APT` (Advanced Persistent Threat)
    *   `NationState`
    *   `CyberCriminal`
    *   `Hacktivist`
    *   `Insider`
*   **Example Cypher**:
    ```cypher
    CREATE (n:ThreatActor {
      name: "APT28",
      type: "APT",
      origin: "Russia",
      aliases: ["Fancy Bear", "Sofacy"]
    })
    ```

#### 3. Malware Hierarchy
*   **Neo4j Label**: `Malware`
*   **Subtypes**:
    *   `Ransomware`
    *   `Trojan`
    *   `Worm`
    *   `Spyware`
    *   `Rootkit`
*   **Example Cypher**:
    ```cypher
    CREATE (n:Malware {
      name: "WannaCry",
      type: "Ransomware",
      family: "WannaCrypt"
    })
    ```

#### 4. Vulnerability Hierarchy
*   **Neo4j Label**: `Vulnerability`
*   **Subtypes**:
    *   `CVE`
    *   `ZeroDay`
    *   `Weakness` (CWE)
*   **Example Cypher**:
    ```cypher
    CREATE (n:Vulnerability {
      id: "CVE-2017-0144",
      type: "CVE",
      severity: "Critical"
    })
    ```

#### 5. Psychometric Hierarchy
*   **Neo4j Label**: `PsychProfile`
*   **Subtypes**:
    *   `CognitiveBias`
    *   `PersonalityTrait`
    *   `LacanianRegister`
*   **Example Cypher**:
    ```cypher
    CREATE (n:PsychProfile {
      name: "Confirmation Bias",
      type: "CognitiveBias",
      category: "Processing Error"
    })
    ```

#### 6. Organization Hierarchy
*   **Neo4j Label**: `Organization`
*   **Subtypes**:
    *   `Company`
    *   `GovernmentAgency`
    *   `Vendor`
    *   `NGO`
*   **Example Cypher**:
    ```cypher
    CREATE (n:Organization {
      name: "Microsoft",
      type: "Vendor",
      sector: "Technology"
    })
    ```

#### 7. Event Hierarchy
*   **Neo4j Label**: `Event`
*   **Subtypes**:
    *   `Incident`
    *   `Breach`
    *   `Campaign`
    *   `Observation`
*   **Example Cypher**:
    ```cypher
    CREATE (n:Event {
      name: "SolarWinds Hack",
      type: "SupplyChainAttack",
      date: "2020-12-01"
    })
    ```

#### 8. Location Hierarchy
*   **Neo4j Label**: `Location`
*   **Subtypes**:
    *   `Country`
    *   `City`
    *   `Region`
    *   `Facility`
    *   `Datacenter`
*   **Example Cypher**:
    ```cypher
    CREATE (n:Location {
      name: "Ashburn",
      type: "City",
      region: "Virginia",
      country: "USA"
    })
    ```

#### 9. Control Hierarchy
*   **Neo4j Label**: `Control`
*   **Subtypes**:
    *   `Mitigation`
    *   `Standard` (e.g., NIST)
    *   `Policy`
    *   `Procedure`
*   **Example Cypher**:
    ```cypher
    CREATE (n:Control {
      name: "MFA",
      type: "Mitigation",
      framework: "NIST 800-53"
    })
    ```

#### 10. Process Hierarchy (Physics/OT)
*   **Neo4j Label**: `Process`
*   **Subtypes**:
    *   `IndustrialProcess`
    *   `BusinessProcess`
    *   `DataFlow`
*   **Example Cypher**:
    ```cypher
    CREATE (n:Process {
      name: "Water Filtration",
      type: "IndustrialProcess",
      sector: "Water"
    })
    ```

### 4.3 Recommended Schema (Target < 30 Labels)
Based on the above, the recommended Neo4j schema labels are:

1.  `Equipment` (Hardware)
2.  `Software` (Applications, OS)
3.  `ThreatActor` (Agents)
4.  `Malware` (Tools)
5.  `AttackPattern` (TTPs)
6.  `Vulnerability` (Flaws)
7.  `Event` (Incidents, Campaigns)
8.  `Indicator` (IOCs)
9.  `Organization` (Entities)
10. `Person` (Individuals)
11. `Location` (Places)
12. `Sector` (Industries)
13. `Document` (Reports, Standards)
14. `PsychProfile` (Human Factors)
15. `Process` (Activities)
16. `Control` (Defenses)
17. `Measurement` (Metrics)

**Total**: 17 Labels. This is well under the 30-label limit and supports infinite granularity via properties.
