# Hierarchical Label Design Options: NER11 to Neo4j

**Date**: 2025-11-26
**Objective**: Map 566 NER11 Entity Types to <30 Neo4j Node Labels.
**Constraint**: "There is NO Neo4j schema" (Greenfield Design).

This document presents three distinct architectural options for the new AEON Neo4j Schema. All options achieve the goal of supporting the full NER11 ontology while maintaining high graph performance and queryability.

---

## Option A: "The Universalist" (Extreme Consolidation)
**Philosophy**: Minimal Labels (< 10). Everything is a generic class. Heavy reliance on indexed `type` and `subtype` properties.
**Pros**: Maximum flexibility; schema changes rarely require migration; extremely simple graph model.
**Cons**: Cypher queries must always filter by property (e.g., `MATCH (n:Entity {type: 'Malware'})`); less visual distinction in graph explorers.

### Core Labels (8 Total)
1.  `Entity` (The root node for almost everything)
2.  `Actor` (Agents, People, Organizations)
3.  `Event` (Time-bound occurrences)
4.  `Location` (Physical or Virtual places)
5.  `Document` (Information artifacts)
6.  `Concept` (Abstract ideas, Psychometrics)
7.  `System` (Complex assemblies, OT)
8.  `Value` (Measurements, Metrics)

### Hierarchy Examples (Option A)
1.  **Malware**: `(:Entity {type: 'Malware', subtype: 'Ransomware', family: 'WannaCry'})`
2.  **Threat Actor**: `(:Actor {type: 'APT', name: 'APT28'})`
3.  **PLC**: `(:System {type: 'PLC', vendor: 'Siemens'})`
4.  **CVE**: `(:Document {type: 'Vulnerability', subtype: 'CVE', id: 'CVE-2024-1234'})`
5.  **Cognitive Bias**: `(:Concept {type: 'Psychometric', subtype: 'CognitiveBias', name: 'Confirmation Bias'})`
6.  **Company**: `(:Actor {type: 'Organization', subtype: 'Corporation'})`
7.  **Attack Technique**: `(:Concept {type: 'TTP', subtype: 'Technique', id: 'T1566'})`
8.  **IP Address**: `(:Location {type: 'Virtual', subtype: 'IPAddress', value: '192.168.1.1'})`
9.  **Incident**: `(:Event {type: 'SecurityIncident', severity: 'High'})`
10. **Voltage**: `(:Value {type: 'Measurement', unit: 'kV', value: 13.8})`

---

## Option B: "The Domain Specialist" (Balanced / Recommended)
**Philosophy**: Labels represent high-level semantic domains (Cyber, Physical, Social). Balanced approach (< 20 labels).
**Pros**: Intuitive for domain experts; optimized for domain-specific queries (e.g., `MATCH (n:CyberAsset)`); good balance of performance and readability.
**Cons**: Requires strict definition of domain boundaries.

### Core Labels (15 Total)
1.  `ThreatActor`
2.  `Malware`
3.  `Vulnerability`
4.  `AttackPattern` (TTPs)
5.  `Indicator` (IOCs)
6.  `CyberAsset` (IT/Network)
7.  `PhysicalAsset` (OT/ICS/Facilities)
8.  `Organization`
9.  `Person`
10. `Location`
11. `Event`
12. `Document`
13. `PsychProfile` (Psychometrics)
14. `Process` (Business/Industrial)
15. `Measurement`

### Hierarchy Examples (Option B)
1.  **Malware**: `(:Malware {type: 'Ransomware', family: 'WannaCry'})`
2.  **Threat Actor**: `(:ThreatActor {type: 'NationState', name: 'APT28'})`
3.  **PLC**: `(:PhysicalAsset {type: 'ControlSystem', subtype: 'PLC', vendor: 'Siemens'})`
4.  **CVE**: `(:Vulnerability {type: 'CVE', id: 'CVE-2024-1234'})`
5.  **Cognitive Bias**: `(:PsychProfile {type: 'CognitiveBias', name: 'Confirmation Bias'})`
6.  **Company**: `(:Organization {type: 'Corporation', sector: 'Energy'})`
7.  **Attack Technique**: `(:AttackPattern {type: 'Technique', id: 'T1566'})`
8.  **IP Address**: `(:CyberAsset {type: 'IPAddress', value: '192.168.1.1'})`
9.  **Incident**: `(:Event {type: 'Incident', category: 'Breach'})`
10. **Voltage**: `(:Measurement {type: 'Electrical', unit: 'kV', value: 13.8})`

---

## Option C: "The Functionalist" (Action-Oriented)
**Philosophy**: Labels represent the *role* or *function* of the node in the graph (Attacker, Target, Tool, Result). (< 25 labels).
**Pros**: Aligns well with "Storytelling" and Attack Graphs; very clear "Subject-Verb-Object" structure.
**Cons**: Entities can change roles (a `Target` can become an `Attacker`), leading to label churn or multi-label complexity.

### Core Labels (12 Total)
1.  `Agent` (Who acts)
2.  `Tool` (What is used)
3.  `Target` (What is acted upon)
4.  `Weakness` (Where the flaw is)
5.  `Action` (What happened)
6.  `Evidence` (Traces left behind)
7.  `Context` (Environment/Location)
8.  `Standard` (Rules/Governance)
9.  `Metric` (Quantification)
10. `Psychology` (Mindset)
11. `Structure` (Organization/Sector)
12. `Resource` (Data/Money)

### Hierarchy Examples (Option C)
1.  **Malware**: `(:Tool {category: 'Malware', type: 'Ransomware'})`
2.  **Threat Actor**: `(:Agent {category: 'ThreatGroup', type: 'APT'})`
3.  **PLC**: `(:Target {category: 'ICS', type: 'PLC'})` (Note: Could also be a `Tool` in botnets)
4.  **CVE**: `(:Weakness {type: 'Vulnerability', id: 'CVE-2024-1234'})`
5.  **Cognitive Bias**: `(:Psychology {type: 'Bias', name: 'Confirmation Bias'})`
6.  **Company**: `(:Structure {type: 'Organization', role: 'Victim'})`
7.  **Attack Technique**: `(:Action {type: 'TTP', id: 'T1566'})`
8.  **IP Address**: `(:Context {type: 'NetworkAddress', value: '192.168.1.1'})`
9.  **Incident**: `(:Action {type: 'Incident', status: 'Active'})`
10. **Voltage**: `(:Metric {type: 'Voltage', value: 13.8})`

---

## Recommendation: Option B (The Domain Specialist)

**Reasoning**:
1.  **Balance**: It avoids the "Blob" problem of Option A (where everything is an `Entity`) and the "Role Confusion" of Option C.
2.  **Alignment**: It aligns perfectly with the NER11 Tiers (Technical, Psychometric, Economic, etc.).
3.  **Performance**: Queries like `MATCH (n:Malware)` are much faster and cheaper than `MATCH (n:Entity) WHERE n.type = 'Malware'`.
4.  **Extensibility**: New domains (e.g., "Space Assets") can be added as a new label or folded into `PhysicalAsset` without breaking the core schema.

### Detailed Hierarchy for Option B (Sample Expansion)

#### 1. `PhysicalAsset` (OT/ICS Focus)
*   `type`: "ControlSystem"
    *   `subtype`: "PLC", "RTU", "DCS", "SafetySystem"
*   `type`: "FieldDevice"
    *   `subtype`: "Sensor", "Actuator", "IED"
*   `type`: "Facility"
    *   `subtype`: "Substation", "Datacenter", "Plant"

#### 2. `PsychProfile` (Human Factors)
*   `type`: "CognitiveBias"
    *   `subtype`: "Confirmation", "Availability", "Anchoring"
*   `type`: "Personality"
    *   `subtype`: "Big5", "DarkTriad"
*   `type`: "Lacanian"
    *   `subtype`: "Real", "Symbolic", "Imaginary"

#### 3. `Event` (Temporal)
*   `type`: "CyberAttack"
    *   `subtype`: "Campaign", "Intrusion", "Exfiltration"
*   `type`: "PhysicalEvent"
    *   `subtype`: "EquipmentFailure", "Maintenance", "Hazard"
