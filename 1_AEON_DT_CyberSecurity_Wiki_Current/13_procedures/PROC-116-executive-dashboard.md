# PROCEDURE: [PROC-116] Executive Dashboard Data Aggregation

**Procedure ID**: PROC-116
**Version**: 1.0.0
**Created**: 2025-11-26
**Last Modified**: 2025-11-26
**Author**: AEON ETL Agent System
**Status**: APPROVED

---

## 1. METADATA

| Field | Value |
|-------|-------|
| **Category** | AGGREGATION |
| **Frequency** | HOURLY (metrics) / DAILY (summaries) |
| **Priority** | HIGH |
| **Estimated Duration** | 5-10 minutes |
| **Risk Level** | LOW |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Aggregate multi-layer knowledge graph data into executive-level metrics and dashboards for strategic decision support across McKenney Questions Q1-Q8.

### 2.2 Business Objectives
- [x] Create real-time threat landscape summary
- [x] Calculate equipment at-risk counts by sector
- [x] Generate CVE prioritization metrics (NOW/NEXT/NEVER)
- [x] Provide attack path visibility summaries
- [x] Enable C-level decision-making with visual dashboards

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q1: What equipment do we have? | Equipment inventory counts by sector/tier |
| Q2: What equipment do customers have? | Customer deployment aggregates |
| Q3: What do attackers know? | CVE exposure summary with CVSS/EPSS |
| Q4: Who are the attackers? | Threat actor activity summaries |
| Q5: How do we defend? | Recommended action counts (NOW/NEXT/NEVER) |
| Q6: What happened before? | Historical pattern trending |
| Q7: What will happen next? | Prediction summary with confidence bands |
| Q8: What should we do? | Prioritized recommendation feed |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running, populated | `docker ps \| grep neo4j` |
| OpenSPG Server | Healthy | `curl http://localhost:8887/health` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query/Command | Expected Result |
|-----------|---------------------------|-----------------|
| Equipment nodes exist | `MATCH (e:Equipment) RETURN count(e)` | >= 29,774 |
| CVE nodes exist | `MATCH (c:CVE) RETURN count(c)` | >= 315,000 |
| Tier assignments exist | `MATCH (e:Equipment) WHERE e.tier IS NOT NULL RETURN count(e)` | >= 29,774 |

### 3.3 Prior Procedures Required

| Procedure ID | Procedure Name | Must Complete Before |
|--------------|---------------|---------------------|
| PROC-001 | Schema Migration | Constraint integrity |
| PROC-101 | CVE Enrichment | CVSS scores available |
| PROC-133 | NOW/NEXT/NEVER Prioritization | Priority assignments |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source Name | Type | Location | Format | Update Frequency |
|-------------|------|----------|--------|------------------|
| Neo4j Layer 0-6 | Graph Database | localhost:7687 | Cypher | Real-time |

### 4.2 Source Details

#### Source 1: Equipment Inventory (Layer 0 + Layer 1)

**Connection Information**:
```
Type: Neo4j Cypher Query
Database: neo4j
Labels: Equipment, CustomerEquipment
```

**Extraction Query**:
```cypher
MATCH (e:Equipment)
OPTIONAL MATCH (e)-[:DEPLOYED_AT]->(c:Customer)
RETURN
  e.sector AS sector,
  e.tier AS tier,
  count(DISTINCT e) AS equipment_count,
  count(DISTINCT c) AS customer_count
```

#### Source 2: CVE Risk Exposure (Layer 2)

**Extraction Query**:
```cypher
MATCH (e:Equipment)<-[:AFFECTS]-(cve:CVE)
WHERE cve.priority IN ['NOW', 'NEXT', 'NEVER']
RETURN
  cve.priority AS priority,
  cve.cvssV3Severity AS severity,
  count(DISTINCT cve) AS cve_count,
  count(DISTINCT e) AS affected_equipment_count
```

#### Source 3: Threat Actor Activity (Layer 3)

**Extraction Query**:
```cypher
MATCH (actor:ThreatActor)-[:USES]->(technique:AttackPattern)
MATCH (technique)-[:EXPLOITS]->(cve:CVE)
RETURN
  actor.name AS threat_actor,
  count(DISTINCT technique) AS technique_count,
  count(DISTINCT cve) AS cve_count,
  max(cve.published) AS latest_activity
```

---

## 5. DESTINATION

### 5.1 Target System

| Field | Value |
|-------|-------|
| **System** | Neo4j (Dashboard Materialized Views) |
| **Container** | openspg-neo4j |
| **Host** | localhost |
| **Port** | 7687 (Bolt), 7474 (HTTP) |
| **Database** | neo4j |

### 5.2 Target Schema

#### Node Types Created/Modified

| Label | Properties | Purpose |
|-------|-----------|---------|
| DashboardMetric | metric_type, value, timestamp, sector | Real-time KPI storage |
| ExecutiveSummary | summary_date, total_equipment, at_risk_count, priority_counts_json | Daily rollup |

#### Relationship Types Created/Modified

| Type | Source | Target | Properties |
|------|--------|--------|------------|
| HAS_METRIC | (:ExecutiveSummary) | (:DashboardMetric) | metric_category |

---

## 6. TRANSFORMATION LOGIC

### 6.1 Aggregation Rules

| Metric | Calculation | Update Frequency |
|--------|-------------|------------------|
| Equipment at Risk | COUNT(Equipment)-[:AFFECTED_BY]->(:CVE {priority:'NOW'}) | Hourly |
| CVE Priority Distribution | COUNT(:CVE) GROUP BY priority | Hourly |
| Sector Risk Score | AVG(CVE.cvssV3BaseScore) per sector | Daily |
| Threat Actor Activity | COUNT(ThreatActor)-[:ACTIVE_IN]->(Campaign) WHERE published > 30 days | Daily |

### 6.2 Dashboard Calculations

```cypher
// Equipment at Risk Summary
CREATE (metric:DashboardMetric {
  metric_type: 'equipment_at_risk',
  value: equipment_count,
  timestamp: datetime(),
  sector: sector_name
})
```

---

## 7. EXECUTION STEPS

### 7.1 Step-by-Step Execution

#### Step 1: Calculate Equipment Risk Metrics

**Command**:
```cypher
MATCH (e:Equipment)<-[:AFFECTS]-(cve:CVE {priority: 'NOW'})
WITH e.sector AS sector, count(DISTINCT e) AS at_risk_count
MERGE (m:DashboardMetric {metric_type: 'equipment_at_risk_now', sector: sector})
SET m.value = at_risk_count, m.timestamp = datetime()
RETURN sector, at_risk_count
ORDER BY at_risk_count DESC;
```

**Expected Output**:
```
| sector | at_risk_count |
|--------|---------------|
| Energy | 1,245         |
| Water  | 892           |
| ...    | ...           |
```

#### Step 2: Generate CVE Priority Distribution

**Command**:
```cypher
MATCH (cve:CVE)
WHERE cve.priority IS NOT NULL
WITH cve.priority AS priority, count(cve) AS count
MERGE (m:DashboardMetric {metric_type: 'cve_priority_distribution', priority: priority})
SET m.value = count, m.timestamp = datetime()
RETURN priority, count;
```

#### Step 3: Create Executive Summary Node

**Command**:
```cypher
MATCH (e:Equipment)
OPTIONAL MATCH (e)<-[:AFFECTS]-(cve:CVE {priority: 'NOW'})
WITH count(DISTINCT e) AS total_equipment,
     count(DISTINCT cve) AS now_cves
CREATE (summary:ExecutiveSummary {
  summary_date: date(),
  total_equipment: total_equipment,
  now_cves: now_cves,
  timestamp: datetime()
})
RETURN summary;
```

---

## 8. POST-EXECUTION

### 8.1 Verification Queries

#### Verify Dashboard Metrics Created

```cypher
MATCH (m:DashboardMetric)
WHERE m.timestamp > datetime() - duration('PT1H')
RETURN m.metric_type, count(m) AS metric_count
ORDER BY metric_type;
```

**Expected Result**: >= 10 metrics updated

#### Verify Executive Summary

```cypher
MATCH (s:ExecutiveSummary)
WHERE s.summary_date = date()
RETURN s.total_equipment, s.now_cves;
```

### 8.2 Success Criteria

| Criterion | Measurement | Threshold | Actual |
|-----------|-------------|-----------|--------|
| Metrics updated | Count of DashboardMetric nodes | >= 10 | [To fill] |
| Summary created | ExecutiveSummary node exists | = 1 | [To fill] |
| Execution time | Minutes | < 10 | [To fill] |

---

## 9. ROLLBACK PROCEDURE

### 9.1 Rollback Steps

```cypher
// Remove metrics from this run
MATCH (m:DashboardMetric)
WHERE m.timestamp > datetime('2025-11-26T00:00:00')
DELETE m;

// Remove executive summary
MATCH (s:ExecutiveSummary)
WHERE s.summary_date = date()
DELETE s;
```

---

## 10. SCHEDULING & AUTOMATION

### 10.1 Cron Schedule

```cron
# Hourly metrics update
0 * * * * /home/jim/scripts/etl/proc_116_dashboard.sh metrics >> /var/log/aeon/proc_116.log 2>&1

# Daily executive summary at 6 AM
0 6 * * * /home/jim/scripts/etl/proc_116_dashboard.sh summary >> /var/log/aeon/proc_116.log 2>&1
```

---

## 11. MONITORING & ALERTING

### 11.1 Metrics to Monitor

| Metric | Threshold | Alert |
|--------|-----------|-------|
| Metrics missing | > 1 hour stale | WARN |
| Summary missing | > 24 hours | ERROR |
| Execution failure | Any error | ERROR |

---

## 12. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON ETL Agent | Initial version based on E06a requirements |

---

**End of Procedure PROC-116**
