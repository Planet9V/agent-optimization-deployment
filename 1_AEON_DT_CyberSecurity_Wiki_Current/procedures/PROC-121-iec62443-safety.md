# PROCEDURE: [PROC-121] IEC 62443 Safety Zone Integration

**Procedure ID**: PROC-121
**Version**: 1.0.0
**Created**: 2025-11-26
**Last Modified**: 2025-11-26
**Author**: AEON ETL Agent System
**Status**: APPROVED

---

## 1. METADATA

| Field | Value |
|-------|-------|
| **Category** | ETL |
| **Frequency** | ONCE (initial) / QUARTERLY (updates) |
| **Priority** | CRITICAL |
| **Estimated Duration** | 2-4 hours |
| **Risk Level** | MEDIUM |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Integrate IEC 62443 industrial safety framework into AEON Digital Twin, mapping 29,774 equipment nodes to Purdue Model safety zones (Level 0-4) with security level requirements (SL 1-4) and foundational requirements (FR1-FR7) compliance tracking.

### 2.2 Business Objectives
- [x] Assign equipment to 5 safety zones based on Purdue Model
- [x] Map FR1-FR7 requirements to zones
- [x] Calculate security level gaps (SL-T vs SL-A)
- [x] Generate compliance reports per zone
- [x] Enable IEC 62443 compliance queries

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q2: What equipment do customers have? | Zoned equipment inventory |
| Q3: What do attackers know? | Zone-specific vulnerability exposure |
| Q5: How do we defend? | FR1-FR7 compliance requirements |
| Q8: What should we do? | Security level gap remediation planning |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running | `docker ps \| grep neo4j` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query | Expected Result |
|-----------|-------------------|-----------------|
| Equipment nodes exist | `MATCH (e:Equipment) RETURN count(e)` | >= 29,774 |
| Equipment classified by type | `MATCH (e:Equipment) WHERE e.equipment_type IS NOT NULL RETURN count(e)` | >= 29,774 |

### 3.3 Prior Procedures Required

| Procedure ID | Procedure Name | Must Complete Before |
|--------------|---------------|---------------------|
| PROC-001 | Schema Migration | Schema foundation |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source Name | Type | Location | Format |
|-------------|------|----------|--------|
| IEC 62443-3-3 FR Definitions | Markdown | Enhancement_07/iec62443-part3-3-detailed-requirements.md | Text |
| IEC 62443-3-2 Risk Assessment | Markdown | Enhancement_07/iec62443-part3.md | Text |
| Equipment Nodes | Neo4j | localhost:7687 | Graph |

### 4.2 IEC 62443 Source Details

#### Foundational Requirements (FR1-FR7)

**Source**: IEC 62443-3-3:2013

**FR Definitions**:
```
FR1: Identification and Authentication Control (IAC)
FR2: Use Control (UC)
FR3: System Integrity (SI)
FR4: Data Confidentiality (DC)
FR5: Restricted Data Flow (RDF)
FR6: Timely Response to Events (TRE)
FR7: Resource Availability (RA)
```

**Security Levels (SL1-SL4)**:
```
SL1: Protection against casual or coincidental violation
SL2: Protection against intentional violation using simple means
SL3: Protection against intentional violation using sophisticated means
SL4: Protection against intentional violation using sophisticated means with extended resources
```

#### Purdue Model Safety Zones

**Zone Definitions**:
```
Level 0: Physical Process (Field Devices, Sensors, Actuators)
Level 1: Basic Control (PLCs, RTUs, DCS Controllers)
Level 2: Supervisory Control (SCADA, HMI)
Level 3: Operations Management (Historian, MES)
Level 4: Enterprise Network (ERP, Business Systems)
```

---

## 5. DESTINATION

### 5.1 Target System

| Field | Value |
|-------|-------|
| **System** | Neo4j |
| **Database** | neo4j |
| **Schema** | IEC 62443 Layer |

### 5.2 Target Schema

#### Node Types Created

| Label | Properties | Purpose |
|-------|-----------|---------|
| SafetyZone | zone_level (0-4), name, sl_target, sl_achieved, criticality | Purdue Model zones |
| FoundationalRequirement | fr_id, name, description, security_levels | FR1-FR7 |
| SecurityLevel | sl_number (1-4), description, requirements | SL definitions |

#### Relationship Types Created

| Type | Source | Target | Properties |
|------|--------|--------|------------|
| LOCATED_IN | (:Equipment) | (:SafetyZone) | assigned_date |
| IMPLEMENTS | (:SafetyZone) | (:FoundationalRequirement) | compliance_percent |
| REQUIRES_SL | (:FoundationalRequirement) | (:SecurityLevel) | control_enhancements |

---

## 6. TRANSFORMATION LOGIC

### 6.1 Equipment-to-Zone Assignment Rules

| Equipment Type | Zone Level | Rationale |
|---------------|-----------|-----------|
| Sensor, Actuator | 0 | Physical process |
| PLC, RTU, Controller | 1 | Basic control |
| SCADA, HMI | 2 | Supervisory |
| Historian, MES | 3 | Operations |
| ERP, Business App | 4 | Enterprise |

### 6.2 Security Level Gap Calculation

```cypher
// Calculate gap (SL-T minus SL-A)
MATCH (zone:SafetyZone)
SET zone.security_level_gap = zone.sl_target - zone.sl_achieved
```

---

## 7. EXECUTION STEPS

### 7.1 Step-by-Step Execution

#### Step 1: Create Foundational Requirement Nodes

**Command**:
```cypher
CREATE (fr1:FoundationalRequirement {
  fr_id: 'FR1',
  name: 'Identification and Authentication Control',
  description: 'Ensure proper identification and authentication of users, devices, and applications',
  source: 'IEC 62443-3-3:2013'
});

CREATE (fr2:FoundationalRequirement {
  fr_id: 'FR2',
  name: 'Use Control',
  description: 'Enforce authorized access control for users and devices'
});

// ... FR3-FR7 similarly
```

#### Step 2: Create Security Level Nodes

**Command**:
```cypher
CREATE (sl1:SecurityLevel {
  sl_number: 1,
  description: 'Protection against casual violation',
  controls: ['Basic authentication', 'Simple access control']
});

// ... SL2-SL4 similarly
```

#### Step 3: Create Safety Zone Nodes

**Command**:
```cypher
CREATE (zone0:SafetyZone {
  zone_level: 0,
  name: 'Physical Process',
  sl_target: 2,
  sl_achieved: 1,
  criticality: 'HIGH',
  description: 'Field devices, sensors, actuators'
});

CREATE (zone1:SafetyZone {
  zone_level: 1,
  name: 'Basic Control',
  sl_target: 3,
  sl_achieved: 2,
  criticality: 'CRITICAL'
});

// ... Zones 2-4 similarly
```

#### Step 4: Assign Equipment to Zones

**Command**:
```cypher
// Assign Level 0 equipment (sensors, actuators)
MATCH (e:Equipment)
WHERE e.equipment_type IN ['Sensor', 'Actuator', 'Field Device']
MATCH (zone:SafetyZone {zone_level: 0})
MERGE (e)-[:LOCATED_IN {assigned_date: date()}]->(zone);

// Assign Level 1 equipment (controllers)
MATCH (e:Equipment)
WHERE e.equipment_type IN ['PLC', 'RTU', 'Controller', 'DCS']
MATCH (zone:SafetyZone {zone_level: 1})
MERGE (e)-[:LOCATED_IN]->(zone);

// ... Continue for zones 2-4
```

#### Step 5: Link Zones to FR Requirements

**Command**:
```cypher
// All zones must implement all FRs
MATCH (zone:SafetyZone), (fr:FoundationalRequirement)
MERGE (zone)-[:IMPLEMENTS {compliance_percent: 0.0}]->(fr);
```

#### Step 6: Calculate Security Level Gaps

**Command**:
```cypher
MATCH (zone:SafetyZone)
SET zone.security_level_gap = zone.sl_target - zone.sl_achieved
RETURN zone.name, zone.sl_target, zone.sl_achieved, zone.security_level_gap;
```

---

## 8. POST-EXECUTION

### 8.1 Verification Queries

#### Verify Zone Creation

```cypher
MATCH (zone:SafetyZone)
RETURN zone.zone_level, zone.name, zone.sl_target, zone.sl_achieved
ORDER BY zone.zone_level;
```

**Expected**: 5 zones (levels 0-4)

#### Verify Equipment Assignment

```cypher
MATCH (zone:SafetyZone)<-[:LOCATED_IN]-(e:Equipment)
RETURN zone.zone_level, zone.name, count(e) AS equipment_count
ORDER BY zone.zone_level;
```

**Expected**: Total = 29,774 equipment across all zones

#### Verify FR Implementation

```cypher
MATCH (zone:SafetyZone)-[:IMPLEMENTS]->(fr:FoundationalRequirement)
RETURN count(*) AS total_fr_links;
```

**Expected**: 35 links (5 zones × 7 FRs)

#### McKenney Question Q5 Example Query

```cypher
// What compliance controls are required?
MATCH (zone:SafetyZone {zone_level: 1})-[:IMPLEMENTS]->(fr:FoundationalRequirement)
WHERE zone.security_level_gap > 0
RETURN fr.fr_id, fr.name, zone.security_level_gap AS gap
ORDER BY gap DESC;
```

### 8.2 Success Criteria

| Criterion | Measurement | Threshold | Actual |
|-----------|-------------|-----------|--------|
| Zones created | Count of SafetyZone nodes | = 5 | [To fill] |
| Equipment assigned | % equipment with LOCATED_IN | 100% | [To fill] |
| FRs created | Count of FoundationalRequirement | = 7 | [To fill] |
| SLs created | Count of SecurityLevel | = 4 | [To fill] |

---

## 9. ROLLBACK PROCEDURE

### 9.1 Rollback Steps

```cypher
// Remove all IEC 62443 artifacts
MATCH (zone:SafetyZone)
DETACH DELETE zone;

MATCH (fr:FoundationalRequirement)
DETACH DELETE fr;

MATCH (sl:SecurityLevel)
DETACH DELETE sl;

// Remove equipment zone assignments
MATCH (e:Equipment)-[r:LOCATED_IN]->()
WHERE r.assigned_date = date()
DELETE r;
```

---

## 10. SCHEDULING & AUTOMATION

### 10.1 Cron Schedule

```cron
# Quarterly compliance assessment on 1st of Q1,Q2,Q3,Q4 at 3 AM
0 3 1 1,4,7,10 * /home/jim/scripts/etl/proc_121_iec62443.sh >> /var/log/aeon/proc_121.log 2>&1
```

---

## 11. MONITORING & ALERTING

### 11.1 Metrics to Monitor

| Metric | Threshold | Alert |
|--------|-----------|-------|
| Unassigned equipment | > 0 | ERROR |
| Security level gap | > 2 | WARN |
| Compliance % | < 70% | CRITICAL |

---

## 12. RELATED ENHANCEMENTS

### Integration Points

| Enhancement | Integration |
|-------------|-------------|
| E08 - RAMS Reliability | Safety zone failure rates |
| E09 - Hazard & FMEA | Zone-specific hazards |
| E10 - Economic Impact | Zone remediation costs |

---

## 13. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON ETL Agent | Initial version based on E07 TASKMASTER |

---

**End of Procedure PROC-121**
