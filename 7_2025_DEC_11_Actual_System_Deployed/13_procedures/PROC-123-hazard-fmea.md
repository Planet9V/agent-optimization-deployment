# PROCEDURE: [PROC-123] Hazard & FMEA Analysis Integration

**Procedure ID**: PROC-123
**Version**: 1.0.0
**Created**: 2025-11-26
**Last Modified**: 2025-11-26
**Author**: AEON ETL Agent System
**Status**: APPROVED

---

## 1. METADATA

| Field | Value |
|-------|-------|
| **Category** | ANALYSIS |
| **Frequency** | SEMI-ANNUAL |
| **Priority** | CRITICAL |
| **Estimated Duration** | 2-3 hours |
| **Risk Level** | MEDIUM |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Integrate Hazard Analysis and FMEA (Failure Mode and Effects Analysis) methodologies to identify safety-critical equipment failure scenarios, calculate Risk Priority Numbers (RPN), and prioritize safety improvements.

### 2.2 Business Objectives
- [x] Identify hazardous equipment failure modes
- [x] Calculate RPN (Risk Priority Number) = Severity × Occurrence × Detection
- [x] Rank hazards by criticality
- [x] Link hazards to CVE vulnerabilities
- [x] Generate safety improvement recommendations

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q1: What equipment do we have? | Equipment with hazard profiles |
| Q3: What do attackers know? | Cyber-physical attack scenarios |
| Q5: How do we defend? | Hazard mitigation strategies |
| Q8: What should we do? | RPN-prioritized safety improvements |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification |
|-----------|---------------|--------------|
| Neo4j | Running | `docker ps \| grep neo4j` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query | Expected |
|-----------|-------------------|----------|
| Equipment nodes exist | `MATCH (e:Equipment) RETURN count(e)` | >= 29,774 |
| Safety zones assigned | `MATCH (e:Equipment)-[:LOCATED_IN]->(:SafetyZone) RETURN count(e)` | >= 29,774 |

### 3.3 Prior Procedures Required

| Procedure ID | Procedure Name | Dependency |
|--------------|---------------|------------|
| PROC-121 | IEC 62443 Safety Zones | Zone assignments |
| PROC-122 | RAMS Reliability | Failure occurrence rates |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source | Type | Location | Format |
|--------|------|----------|--------|
| FMEA Database | CSV/External | CSV import | Tabular |
| Hazard Library | Static | JSON file | JSON |
| Neo4j Equipment | Graph | localhost:7687 | Cypher |

### 4.2 FMEA Methodology

**RPN Calculation**:
```
RPN = Severity × Occurrence × Detection

Severity (1-10):
  10 = Catastrophic (loss of life, major equipment destruction)
  7-9 = Critical (severe injury, extensive damage)
  4-6 = Moderate (minor injury, significant downtime)
  1-3 = Minor (no injury, minimal impact)

Occurrence (1-10):
  10 = Very High (>1 per day)
  7-9 = High (1 per week to 1 per month)
  4-6 = Moderate (1 per month to 1 per year)
  1-3 = Low (<1 per year)

Detection (1-10):
  10 = Cannot detect
  7-9 = Very low detection capability
  4-6 = Moderate detection capability
  1-3 = High detection capability

RPN Range: 1-1000
RPN >= 200: CRITICAL PRIORITY
RPN 100-199: HIGH PRIORITY
RPN < 100: MODERATE PRIORITY
```

### 4.3 Hazard Categories

```json
{
  "hazard_types": [
    "Physical Injury", "Equipment Damage", "Environmental Release",
    "Process Upset", "Cyber-Physical Attack", "Data Corruption",
    "Supply Chain Disruption", "Cascading Failure"
  ]
}
```

---

## 5. DESTINATION

### 5.1 Target Schema

#### Node Types Created

| Label | Properties | Purpose |
|-------|-----------|---------|
| Hazard | hazard_id, hazard_type, description, severity, occurrence, detection, rpn | Safety hazard tracking |
| FailureMode | mode_id, description, equipment_type, cause, effect | FMEA failure scenarios |
| SafetyControl | control_id, description, control_type, effectiveness | Mitigation measures |

#### Relationship Types Created

| Type | Source | Target | Properties |
|------|--------|--------|------------|
| HAS_HAZARD | (:Equipment) | (:Hazard) | rpn_score |
| EXHIBITS_FAILURE_MODE | (:Equipment) | (:FailureMode) | probability |
| MITIGATED_BY | (:Hazard) | (:SafetyControl) | effectiveness_percent |
| CAN_TRIGGER | (:CVE) | (:Hazard) | exploit_chain |

---

## 6. TRANSFORMATION LOGIC

### 6.1 RPN Calculation

```cypher
// Calculate RPN for each hazard
MATCH (e:Equipment)-[:HAS_HAZARD]->(h:Hazard)
SET h.rpn = h.severity * h.occurrence * h.detection
RETURN h.hazard_id, h.rpn
ORDER BY h.rpn DESC;
```

### 6.2 Cyber-Physical Hazard Linking

```cypher
// Link CVEs to physical hazards they could trigger
MATCH (cve:CVE)-[:AFFECTS]->(e:Equipment)-[:HAS_HAZARD]->(h:Hazard)
WHERE cve.cvssV3Severity IN ['CRITICAL', 'HIGH']
  AND h.hazard_type = 'Cyber-Physical Attack'
MERGE (cve)-[:CAN_TRIGGER {
  exploit_chain: 'Cyber exploit → Equipment compromise → Physical hazard',
  risk_level: 'CRITICAL'
}]->(h);
```

---

## 7. EXECUTION STEPS

### 7.1 Step-by-Step Execution

#### Step 1: Import FMEA Database

**Command**:
```cypher
LOAD CSV WITH HEADERS FROM 'file:///fmea_hazards.csv' AS row
CREATE (h:Hazard {
  hazard_id: row.hazard_id,
  hazard_type: row.hazard_type,
  description: row.description,
  severity: toInteger(row.severity),
  occurrence: toInteger(row.occurrence),
  detection: toInteger(row.detection)
});

// Calculate RPN
MATCH (h:Hazard)
SET h.rpn = h.severity * h.occurrence * h.detection;
```

#### Step 2: Link Hazards to Equipment

**Command**:
```cypher
LOAD CSV WITH HEADERS FROM 'file:///equipment_hazards.csv' AS row
MATCH (e:Equipment {equipment_id: row.equipment_id})
MATCH (h:Hazard {hazard_id: row.hazard_id})
CREATE (e)-[:HAS_HAZARD {rpn_score: h.rpn}]->(h);
```

#### Step 3: Create Failure Mode Nodes

**Command**:
```cypher
CREATE (fm:FailureMode {
  mode_id: 'FM001',
  description: 'PLC CPU failure',
  equipment_type: 'PLC',
  cause: 'Component wear, power surge, firmware corruption',
  effect: 'Loss of process control, safety system unavailable',
  severity: 9,
  occurrence: 4,
  detection: 6,
  rpn: 216
});

// Link to equipment
MATCH (e:Equipment {equipment_type: 'PLC'})
MATCH (fm:FailureMode {mode_id: 'FM001'})
MERGE (e)-[:EXHIBITS_FAILURE_MODE {probability: 0.05}]->(fm);
```

#### Step 4: Create Safety Controls

**Command**:
```cypher
CREATE (sc:SafetyControl {
  control_id: 'SC001',
  description: 'Redundant PLC configuration with fail-safe logic',
  control_type: 'Engineering Control',
  effectiveness: 0.85
});

// Link controls to hazards
MATCH (h:Hazard {hazard_type: 'Process Upset'})
MATCH (sc:SafetyControl {control_id: 'SC001'})
MERGE (h)-[:MITIGATED_BY {effectiveness_percent: 85}]->(sc);
```

#### Step 5: Link Cyber Vulnerabilities to Physical Hazards

**Command**:
```cypher
MATCH (cve:CVE)-[:AFFECTS]->(e:Equipment)
MATCH (e)-[:HAS_HAZARD]->(h:Hazard)
WHERE cve.cvssV3Severity = 'CRITICAL'
  AND h.hazard_type IN ['Cyber-Physical Attack', 'Equipment Damage', 'Process Upset']
MERGE (cve)-[:CAN_TRIGGER {
  attack_vector: 'Remote exploit → Equipment malfunction → Physical consequence',
  combined_risk: cve.cvssV3BaseScore * h.rpn
}]->(h);
```

---

## 8. POST-EXECUTION

### 8.1 Verification Queries

#### Verify Hazards Created

```cypher
MATCH (h:Hazard)
RETURN h.hazard_type, count(h) AS count, avg(h.rpn) AS avg_rpn
ORDER BY avg_rpn DESC;
```

#### Top 20 Critical Hazards

```cypher
MATCH (e:Equipment)-[:HAS_HAZARD]->(h:Hazard)
WHERE h.rpn >= 200
RETURN e.equipment_id, e.sector, h.description, h.rpn
ORDER BY h.rpn DESC
LIMIT 20;
```

#### Cyber-Physical Attack Scenarios

```cypher
MATCH (cve:CVE)-[r:CAN_TRIGGER]->(h:Hazard)
RETURN cve.cve_id, cve.cvssV3Severity, h.description, r.combined_risk
ORDER BY r.combined_risk DESC
LIMIT 10;
```

### 8.2 Success Criteria

| Criterion | Measurement | Threshold | Actual |
|-----------|-------------|-----------|--------|
| Hazards identified | Count of Hazard nodes | >= 100 | [To fill] |
| Equipment with hazards | % equipment with HAS_HAZARD | >= 80% | [To fill] |
| Critical hazards (RPN >= 200) | Count | >= 10 | [To fill] |
| Cyber-physical links | CVE→Hazard relationships | >= 50 | [To fill] |

---

## 9. ROLLBACK PROCEDURE

```cypher
// Remove FMEA artifacts
MATCH (h:Hazard)
WHERE h.created_date = date()
DETACH DELETE h;

MATCH (fm:FailureMode)
DETACH DELETE fm;

MATCH (sc:SafetyControl)
DETACH DELETE sc;
```

---

## 10. SCHEDULING & AUTOMATION

```cron
# Semi-annual FMEA update on Jan 1 and Jul 1 at 5 AM
0 5 1 1,7 * /home/jim/scripts/etl/proc_123_fmea.sh >> /var/log/aeon/proc_123.log 2>&1
```

---

## 11. MONITORING & ALERTING

| Metric | Threshold | Alert |
|--------|-----------|-------|
| Critical hazards (RPN >= 200) | > 50 | CRITICAL |
| Unmitigated hazards | > 10 | WARN |
| Cyber-physical scenarios | > 100 | INFO |

---

## 12. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON ETL Agent | Initial version for E09 |

---

**End of Procedure PROC-123**
