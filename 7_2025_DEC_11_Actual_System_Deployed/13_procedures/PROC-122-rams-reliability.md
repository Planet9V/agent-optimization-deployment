# PROCEDURE: [PROC-122] RAMS Reliability Analysis Integration

**Procedure ID**: PROC-122
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
| **Frequency** | QUARTERLY |
| **Priority** | HIGH |
| **Estimated Duration** | 1-2 hours |
| **Risk Level** | LOW |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Integrate RAMS (Reliability, Availability, Maintainability, Safety) metrics for industrial equipment, enabling failure prediction, MTBF/MTTR tracking, and maintenance optimization.

### 2.2 Business Objectives
- [x] Calculate MTBF (Mean Time Between Failures) per equipment type
- [x] Track MTTR (Mean Time To Repair) for maintenance planning
- [x] Assign reliability scores (0.0-1.0) to equipment
- [x] Identify high-failure equipment requiring replacement
- [x] Enable predictive maintenance scheduling

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q1: What equipment do we have? | Equipment with reliability metrics |
| Q6: What happened before? | Historical failure patterns |
| Q7: What will happen next? | Failure predictions based on MTBF |
| Q8: What should we do? | Maintenance and replacement recommendations |

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
| Historical incidents | `MATCH (i:Incident) RETURN count(i)` | >= 100 |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source | Type | Location | Format |
|--------|------|----------|--------|
| Equipment Failure History | Neo4j/External | localhost:7687 or CSV | Graph/CSV |
| Maintenance Records | CMMS/External | CSV import | Tabular |
| Vendor MTBF Data | Vendor specs | Static JSON | JSON |

### 4.2 RAMS Metrics Definitions

**MTBF (Mean Time Between Failures)**:
```
MTBF = Total Operating Hours / Number of Failures
Units: hours
Example: 8760 hours (1 year uptime)
```

**MTTR (Mean Time To Repair)**:
```
MTTR = Total Repair Time / Number of Repairs
Units: hours
Example: 4 hours (average repair time)
```

**Availability**:
```
Availability = MTBF / (MTBF + MTTR)
Units: percentage (0.0-1.0)
Target: >= 0.99 (99% uptime)
```

**Reliability Score**:
```
R(t) = e^(-t/MTBF)
Where t = operating time since last maintenance
```

---

## 5. DESTINATION

### 5.1 Target Schema

#### Node Types Created

| Label | Properties | Purpose |
|-------|-----------|---------|
| RAMSMetric | equipment_id, mtbf, mttr, availability, reliability_score, last_failure_date | Equipment reliability tracking |
| FailureEvent | event_id, equipment_id, failure_type, downtime_hours, repair_cost | Failure history |

#### Relationship Types Created

| Type | Source | Target | Properties |
|------|--------|--------|------------|
| HAS_RAMS_METRIC | (:Equipment) | (:RAMSMetric) | calculated_date |
| EXPERIENCED_FAILURE | (:Equipment) | (:FailureEvent) | failure_date |

---

## 6. TRANSFORMATION LOGIC

### 6.1 MTBF Calculation

```cypher
// Calculate MTBF per equipment
MATCH (e:Equipment)<-[:EXPERIENCED_FAILURE]-(f:FailureEvent)
WHERE f.failure_date > date() - duration('P365D')
WITH e, count(f) AS failure_count, 8760 AS annual_hours
MERGE (rams:RAMSMetric {equipment_id: e.equipment_id})
SET rams.mtbf = annual_hours / failure_count,
    rams.calculated_date = date()
```

### 6.2 Reliability Score Calculation

```cypher
// Calculate reliability score
MATCH (e:Equipment)-[:HAS_RAMS_METRIC]->(rams:RAMSMetric)
WITH e, rams, duration.between(rams.last_failure_date, date()).hours AS hours_since_failure
SET rams.reliability_score = exp(-hours_since_failure / rams.mtbf)
```

---

## 7. EXECUTION STEPS

### 7.1 Step-by-Step Execution

#### Step 1: Import Failure History

**Command**:
```cypher
LOAD CSV WITH HEADERS FROM 'file:///failure_history.csv' AS row
MATCH (e:Equipment {equipment_id: row.equipment_id})
CREATE (f:FailureEvent {
  event_id: row.event_id,
  failure_type: row.failure_type,
  failure_date: date(row.failure_date),
  downtime_hours: toFloat(row.downtime_hours),
  repair_cost: toFloat(row.repair_cost)
})
CREATE (e)-[:EXPERIENCED_FAILURE]->(f);
```

#### Step 2: Calculate MTBF/MTTR

**Command**:
```cypher
MATCH (e:Equipment)<-[:EXPERIENCED_FAILURE]-(f:FailureEvent)
WHERE f.failure_date > date() - duration('P365D')
WITH e,
     count(f) AS failure_count,
     sum(f.downtime_hours) AS total_downtime,
     8760 AS annual_hours
MERGE (rams:RAMSMetric {equipment_id: e.equipment_id})
SET rams.mtbf = annual_hours / failure_count,
    rams.mttr = total_downtime / failure_count,
    rams.availability = (annual_hours - total_downtime) / annual_hours,
    rams.last_calculated = datetime()
CREATE (e)-[:HAS_RAMS_METRIC]->(rams);
```

#### Step 3: Calculate Reliability Scores

**Command**:
```cypher
MATCH (e:Equipment)-[:HAS_RAMS_METRIC]->(rams:RAMSMetric)
OPTIONAL MATCH (e)-[:EXPERIENCED_FAILURE]->(f:FailureEvent)
WITH e, rams, max(f.failure_date) AS last_failure
WITH e, rams, duration.between(coalesce(last_failure, date() - duration('P730D')), date()).hours AS hours_since_failure
SET rams.reliability_score = exp(-hours_since_failure / rams.mtbf),
    rams.last_failure_date = last_failure
```

#### Step 4: Identify High-Risk Equipment

**Command**:
```cypher
MATCH (e:Equipment)-[:HAS_RAMS_METRIC]->(rams:RAMSMetric)
WHERE rams.availability < 0.95 OR rams.mtbf < 1000
SET e.maintenance_priority = 'HIGH',
    e.replacement_candidate = true
RETURN e.equipment_id, rams.mtbf, rams.availability
ORDER BY rams.availability ASC
LIMIT 50;
```

---

## 8. POST-EXECUTION

### 8.1 Verification Queries

#### Verify RAMS Metrics Created

```cypher
MATCH (rams:RAMSMetric)
RETURN count(rams) AS metrics_created,
       avg(rams.mtbf) AS avg_mtbf,
       avg(rams.availability) AS avg_availability;
```

**Expected**: Metrics created >= 29,774, Avg availability >= 0.95

#### Identify Maintenance Priorities

```cypher
MATCH (e:Equipment)-[:HAS_RAMS_METRIC]->(rams:RAMSMetric)
WHERE rams.availability < 0.99
RETURN e.equipment_id, e.sector, rams.mtbf, rams.mttr, rams.availability
ORDER BY rams.availability ASC
LIMIT 20;
```

### 8.2 Success Criteria

| Criterion | Measurement | Threshold | Actual |
|-----------|-------------|-----------|--------|
| RAMS metrics created | Count of RAMSMetric nodes | >= 29,774 | [To fill] |
| MTBF calculated | % with non-null MTBF | >= 95% | [To fill] |
| Reliability scores | % with reliability_score | >= 90% | [To fill] |

---

## 9. ROLLBACK PROCEDURE

```cypher
// Remove RAMS artifacts
MATCH (rams:RAMSMetric)
WHERE rams.last_calculated > datetime('2025-11-26T00:00:00')
DETACH DELETE rams;

MATCH (f:FailureEvent)
WHERE f.imported_date = date()
DETACH DELETE f;
```

---

## 10. SCHEDULING & AUTOMATION

```cron
# Quarterly RAMS update on 1st of Q1,Q2,Q3,Q4 at 4 AM
0 4 1 1,4,7,10 * /home/jim/scripts/etl/proc_122_rams.sh >> /var/log/aeon/proc_122.log 2>&1
```

---

## 11. MONITORING & ALERTING

| Metric | Threshold | Alert |
|--------|-----------|-------|
| Equipment availability | < 0.95 | WARN |
| Critical equipment MTBF | < 500 hours | CRITICAL |

---

## 12. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON ETL Agent | Initial version for E08 |

---

**End of Procedure PROC-122**
