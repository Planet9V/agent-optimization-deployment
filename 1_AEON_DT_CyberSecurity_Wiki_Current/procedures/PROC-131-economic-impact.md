# PROCEDURE: [PROC-131] Economic Impact Modeling

**Procedure ID**: PROC-131
**Version**: 1.0.0
**Created**: 2025-11-26
**Last Modified**: 2025-11-26
**Author**: AEON ETL Agent System
**Status**: APPROVED

---

## 1. METADATA

| Field | Value |
|-------|-------|
| **Category** | ANALYTICS |
| **Frequency** | MONTHLY |
| **Priority** | HIGH |
| **Estimated Duration** | 1-2 hours |
| **Risk Level** | LOW |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Calculate economic impact of cybersecurity events, quantify breach costs, assess patch/remediation ROI, and enable CFO-level decision support for security investments.

### 2.2 Business Objectives
- [x] Calculate breach cost per CVE scenario
- [x] Estimate downtime costs per equipment/sector
- [x] Calculate ROI for NOW/NEXT/NEVER prioritization
- [x] Quantify insurance/liability exposure
- [x] Enable budget justification for security programs

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q3: What do attackers know? | Economic value of exploitable vulnerabilities |
| Q5: How do we defend? | Cost-benefit analysis of defenses |
| Q8: What should we do? | ROI-ranked security investments |

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
| CVE priority assignments | `MATCH (c:CVE) WHERE c.priority IS NOT NULL RETURN count(c)` | >= 315,000 |

### 3.3 Prior Procedures Required

| Procedure ID | Procedure Name | Dependency |
|--------------|---------------|------------|
| PROC-133 | NOW/NEXT/NEVER Prioritization | CVE priorities |
| PROC-122 | RAMS Reliability | Downtime estimates |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source | Type | Location | Format |
|--------|------|----------|--------|
| Ponemon Cost of Data Breach | Research Report | Static JSON | JSON |
| IBM X-Force Breach Costs | Research Report | Static JSON | JSON |
| Equipment Asset Values | CSV/Neo4j | CSV import | Tabular |

### 4.2 Cost Model Parameters

**Breach Cost Components** (Ponemon 2023):
```json
{
  "per_record_cost": 165,
  "detection_and_escalation": 1520000,
  "notification_cost": 310000,
  "post_breach_response": 1620000,
  "lost_business_cost": 4290000,
  "average_total_cost": 4450000,
  "ransomware_avg": 5130000
}
```

**Downtime Cost Calculation**:
```
Hourly Downtime Cost = (Equipment Value × Utilization Rate) / Annual Operating Hours
Annual Operating Hours = 8760 (24/7) or 2080 (8/5)
```

**Patch ROI Calculation**:
```
ROI = (Breach Cost Avoided - Patch Cost) / Patch Cost × 100%
Example: ($4.45M - $500K) / $500K = 790% ROI
```

---

## 5. DESTINATION

### 5.1 Target Schema

#### Node Types Created

| Label | Properties | Purpose |
|-------|-----------|---------|
| EconomicImpact | scenario_id, breach_cost, downtime_cost, total_cost, probability | Cost scenarios |
| CostFactor | factor_type, unit_cost, currency | Cost parameters |
| ROI_Analysis | investment, benefit, roi_percent, payback_months | Investment analysis |

#### Relationship Types Created

| Type | Source | Target | Properties |
|------|--------|--------|------------|
| HAS_ECONOMIC_IMPACT | (:CVE or :Equipment) | (:EconomicImpact) | likelihood |
| JUSTIFIES_INVESTMENT | (:ROI_Analysis) | (:EconomicImpact) | cost_avoidance |

---

## 6. TRANSFORMATION LOGIC

### 6.1 Breach Cost Calculation

```cypher
// Calculate breach cost per CVE scenario
MATCH (cve:CVE {priority: 'NOW'})-[:AFFECTS]->(e:Equipment)
WITH cve, count(DISTINCT e) AS affected_equipment_count,
     4450000 AS avg_breach_cost
SET cve.estimated_breach_cost = avg_breach_cost * (affected_equipment_count / 100.0)
RETURN cve.cve_id, cve.estimated_breach_cost
ORDER BY cve.estimated_breach_cost DESC;
```

### 6.2 Downtime Cost Calculation

```cypher
// Calculate hourly downtime cost per equipment
MATCH (e:Equipment)-[:HAS_RAMS_METRIC]->(rams:RAMSMetric)
WITH e, e.asset_value AS value, rams.mttr AS mttr_hours
SET e.hourly_downtime_cost = (value * 0.85) / 8760,
    e.mttr_cost = ((value * 0.85) / 8760) * mttr_hours
RETURN e.equipment_id, e.hourly_downtime_cost, e.mttr_cost;
```

### 6.3 ROI Calculation for Patch Program

```cypher
// Calculate ROI for patching NOW priority CVEs
MATCH (cve:CVE {priority: 'NOW'})
WITH count(cve) AS now_cve_count,
     500000 AS patch_program_cost,
     4450000 AS avg_breach_cost_avoided
WITH now_cve_count, patch_program_cost,
     avg_breach_cost_avoided * (now_cve_count / 127.0) AS total_benefit
CREATE (roi:ROI_Analysis {
  investment: patch_program_cost,
  benefit: total_benefit,
  roi_percent: ((total_benefit - patch_program_cost) / patch_program_cost) * 100,
  payback_months: (patch_program_cost / (total_benefit / 12)),
  analysis_date: date()
})
RETURN roi;
```

---

## 7. EXECUTION STEPS

### 7.1 Step-by-Step Execution

#### Step 1: Import Cost Factor Library

**Command**:
```cypher
CREATE (cf1:CostFactor {
  factor_type: 'per_record_breach',
  unit_cost: 165,
  currency: 'USD',
  source: 'Ponemon 2023'
});

CREATE (cf2:CostFactor {
  factor_type: 'average_breach_total',
  unit_cost: 4450000,
  currency: 'USD'
});

CREATE (cf3:CostFactor {
  factor_type: 'ransomware_average',
  unit_cost: 5130000,
  currency: 'USD'
});
```

#### Step 2: Assign Asset Values to Equipment

**Command**:
```cypher
LOAD CSV WITH HEADERS FROM 'file:///equipment_asset_values.csv' AS row
MATCH (e:Equipment {equipment_id: row.equipment_id})
SET e.asset_value = toFloat(row.asset_value),
    e.replacement_cost = toFloat(row.replacement_cost),
    e.annual_revenue_impact = toFloat(row.annual_revenue_impact);
```

#### Step 3: Calculate CVE Breach Costs

**Command**:
```cypher
MATCH (cve:CVE {priority: 'NOW'})-[:AFFECTS]->(e:Equipment)
WITH cve, sum(e.asset_value) AS total_asset_at_risk,
     count(DISTINCT e) AS equipment_count
MATCH (cf:CostFactor {factor_type: 'average_breach_total'})
CREATE (impact:EconomicImpact {
  scenario_id: 'CVE_' + cve.cve_id,
  breach_cost: cf.unit_cost,
  asset_at_risk: total_asset_at_risk,
  total_cost: cf.unit_cost + (total_asset_at_risk * 0.3),
  probability: cve.epss,
  calculated_date: date()
})
CREATE (cve)-[:HAS_ECONOMIC_IMPACT {likelihood: cve.epss}]->(impact);
```

#### Step 4: Calculate Sector-Wide Impact

**Command**:
```cypher
MATCH (e:Equipment)
WITH e.sector AS sector,
     sum(e.asset_value) AS total_sector_assets,
     count(e) AS equipment_count
MATCH (e2:Equipment {sector: sector})<-[:AFFECTS]-(cve:CVE {priority: 'NOW'})
WITH sector, total_sector_assets, equipment_count,
     count(DISTINCT cve) AS now_cves
CREATE (impact:EconomicImpact {
  scenario_id: 'SECTOR_' + sector,
  sector: sector,
  total_assets: total_sector_assets,
  cves_at_risk: now_cves,
  estimated_exposure: total_sector_assets * 0.15 * (now_cves / 100.0),
  calculated_date: date()
})
RETURN sector, impact.estimated_exposure
ORDER BY impact.estimated_exposure DESC;
```

#### Step 5: Generate ROI Analysis for Security Investments

**Command**:
```cypher
MATCH (cve:CVE)
WHERE cve.priority IS NOT NULL
WITH cve.priority AS priority, count(cve) AS cve_count,
     CASE cve.priority
       WHEN 'NOW' THEN 500000
       WHEN 'NEXT' THEN 200000
       WHEN 'NEVER' THEN 0
     END AS patch_cost
MATCH (cf:CostFactor {factor_type: 'average_breach_total'})
WITH priority, cve_count, patch_cost,
     cf.unit_cost * (cve_count / 127.0) AS breach_cost_avoided
CREATE (roi:ROI_Analysis {
  priority_category: priority,
  cve_count: cve_count,
  investment: patch_cost,
  benefit: breach_cost_avoided,
  roi_percent: ((breach_cost_avoided - patch_cost) / CASE WHEN patch_cost > 0 THEN patch_cost ELSE 1 END) * 100,
  net_benefit: breach_cost_avoided - patch_cost,
  analysis_date: date()
})
RETURN priority, roi.roi_percent, roi.net_benefit
ORDER BY roi.roi_percent DESC;
```

---

## 8. POST-EXECUTION

### 8.1 Verification Queries

#### Verify Economic Impact Nodes Created

```cypher
MATCH (impact:EconomicImpact)
RETURN count(impact) AS impact_scenarios,
       sum(impact.total_cost) AS total_exposure;
```

#### Top 10 Highest Economic Impact CVEs

```cypher
MATCH (cve:CVE)-[:HAS_ECONOMIC_IMPACT]->(impact:EconomicImpact)
RETURN cve.cve_id, cve.cvssV3Severity, impact.total_cost, impact.probability
ORDER BY impact.total_cost DESC
LIMIT 10;
```

#### ROI Summary for Patch Program

```cypher
MATCH (roi:ROI_Analysis)
WHERE roi.analysis_date = date()
RETURN roi.priority_category,
       roi.investment,
       roi.benefit,
       roi.roi_percent,
       roi.net_benefit
ORDER BY roi.roi_percent DESC;
```

**Example Expected Output**:
```
| priority_category | investment | benefit    | roi_percent | net_benefit |
|-------------------|------------|------------|-------------|-------------|
| NOW               | $500,000   | $4,450,000 | 790%        | $3,950,000  |
| NEXT              | $200,000   | $890,000   | 345%        | $690,000    |
| NEVER             | $0         | $0         | N/A         | $0          |
```

### 8.2 Success Criteria

| Criterion | Measurement | Threshold | Actual |
|-----------|-------------|-----------|--------|
| Economic impacts calculated | Count of EconomicImpact nodes | >= 100 | [To fill] |
| ROI analyses created | Count of ROI_Analysis nodes | >= 3 | [To fill] |
| Asset values assigned | % equipment with asset_value | >= 80% | [To fill] |

---

## 9. ROLLBACK PROCEDURE

```cypher
// Remove economic artifacts
MATCH (impact:EconomicImpact)
WHERE impact.calculated_date = date()
DETACH DELETE impact;

MATCH (roi:ROI_Analysis)
WHERE roi.analysis_date = date()
DELETE roi;
```

---

## 10. SCHEDULING & AUTOMATION

```cron
# Monthly economic analysis on 1st at 7 AM
0 7 1 * * /home/jim/scripts/etl/proc_131_economic_impact.sh >> /var/log/aeon/proc_131.log 2>&1
```

---

## 11. MONITORING & ALERTING

| Metric | Threshold | Alert |
|--------|-----------|-------|
| Total exposure | > $10M | WARN |
| ROI for NOW category | < 500% | WARN |

---

## 12. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON ETL Agent | Initial version for E10 |

---

**End of Procedure PROC-131**
