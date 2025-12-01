# PROCEDURE: [PROC-132] Psychohistory Demographics Integration

**Procedure ID**: PROC-132
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
| **Frequency** | QUARTERLY |
| **Priority** | MEDIUM |
| **Estimated Duration** | 1 hour |
| **Risk Level** | LOW |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Apply Asimovian psychohistory principles to model large-scale organizational and sector demographics, enabling statistical prediction of security behaviors and breach likelihood across populations.

### 2.2 Business Objectives
- [x] Segment organizations by demographic profiles
- [x] Calculate sector-level breach probability distributions
- [x] Identify population-scale security culture patterns
- [x] Forecast organizational crisis points (Seldon Crisis)
- [x] Enable macro-level security policy recommendations

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q4: Who are the attackers? | Demographics of targeted populations |
| Q6: What happened before? | Historical demographic breach patterns |
| Q7: What will happen next? | Population-level forecasting |
| Q8: What should we do? | Policy interventions for demographic segments |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification |
|-----------|---------------|--------------|
| Neo4j | Running | `docker ps \| grep neo4j` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query | Expected |
|-----------|-------------------|----------|
| Organization nodes exist | `MATCH (o:Organization) RETURN count(o)` | >= 100 |
| Sector assignments exist | `MATCH (o:Organization) WHERE o.sector IS NOT NULL RETURN count(o)` | >= 100 |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source | Type | Location | Format |
|--------|------|----------|--------|
| Organization Demographics | CSV | CSV import | Tabular |
| US Census Bureau (Sector Stats) | API/Static | JSON | JSON |
| Sector Breach Statistics | Research | CSV | Tabular |

### 4.2 Demographic Dimensions

**Organizational Demographics**:
```json
{
  "size_categories": ["<50", "50-250", "250-1000", "1000-5000", ">5000"],
  "security_maturity": ["Initial", "Managed", "Defined", "Quantitative", "Optimizing"],
  "industry_verticals": ["Energy", "Water", "Healthcare", "Finance", "Transportation", "Manufacturing", "Government", "Commercial", "Defense", "Communications", "Chemical", "Nuclear", "Dams", "Food", "Emergency Services", "IT"],
  "geographic_regions": ["Northeast", "Southeast", "Midwest", "Southwest", "West", "International"],
  "regulatory_exposure": ["NERC_CIP", "HIPAA", "PCI_DSS", "SOX", "GDPR", "None"]
}
```

**Psychohistory Variables**:
```
Population Size (N): Number of organizations in demographic segment
Breach Probability (P): Historical breach rate for segment
Cultural Inertia (I): Resistance to security change (0.0-1.0)
Crisis Susceptibility (C): Likelihood of Seldon Crisis inflection point
```

---

## 5. DESTINATION

### 5.1 Target Schema

#### Node Types Created

| Label | Properties | Purpose |
|-------|-----------|---------|
| DemographicSegment | segment_id, size, sector, maturity, population_count | Population grouping |
| PopulationMetric | metric_type, value, timestamp, confidence_interval | Aggregate statistics |
| SeldonCrisis | crisis_id, segment_id, probability, timeframe, triggers | Inflection point prediction |

#### Relationship Types Created

| Type | Source | Target | Properties |
|------|--------|--------|------------|
| BELONGS_TO_SEGMENT | (:Organization) | (:DemographicSegment) | assignment_confidence |
| HAS_POPULATION_METRIC | (:DemographicSegment) | (:PopulationMetric) | measurement_date |
| PREDICTED_CRISIS | (:DemographicSegment) | (:SeldonCrisis) | probability |

---

## 6. TRANSFORMATION LOGIC

### 6.1 Demographic Segmentation

```cypher
// Segment organizations by sector + size + maturity
MATCH (o:Organization)
WITH o.sector AS sector,
     o.employee_count AS size,
     o.security_maturity AS maturity,
     CASE
       WHEN o.employee_count < 50 THEN 'Small'
       WHEN o.employee_count < 250 THEN 'Medium'
       WHEN o.employee_count < 1000 THEN 'Large'
       ELSE 'Enterprise'
     END AS size_category
MERGE (segment:DemographicSegment {
  sector: sector,
  size_category: size_category,
  maturity: maturity
})
ON CREATE SET segment.population_count = 0
WITH segment
MATCH (o:Organization)
WHERE o.sector = segment.sector
  AND CASE
        WHEN o.employee_count < 50 THEN 'Small'
        WHEN o.employee_count < 250 THEN 'Medium'
        WHEN o.employee_count < 1000 THEN 'Large'
        ELSE 'Enterprise'
      END = segment.size_category
  AND o.security_maturity = segment.maturity
MERGE (o)-[:BELONGS_TO_SEGMENT {assignment_confidence: 0.95}]->(segment)
WITH segment, count(o) AS pop_count
SET segment.population_count = pop_count;
```

### 6.2 Breach Probability Calculation

```cypher
// Calculate historical breach rate per segment
MATCH (segment:DemographicSegment)<-[:BELONGS_TO_SEGMENT]-(o:Organization)
OPTIONAL MATCH (o)-[:EXPERIENCED_BREACH]->(b:BreachEvent)
WHERE b.breach_date > date() - duration('P365D')
WITH segment,
     count(DISTINCT o) AS total_orgs,
     count(DISTINCT b) AS breaches_last_year
MERGE (metric:PopulationMetric {
  segment_id: segment.segment_id,
  metric_type: 'breach_probability'
})
SET metric.value = toFloat(breaches_last_year) / total_orgs,
    metric.timestamp = datetime()
CREATE (segment)-[:HAS_POPULATION_METRIC]->(metric);
```

---

## 7. EXECUTION STEPS

### 7.1 Step-by-Step Execution

#### Step 1: Import Organization Demographics

**Command**:
```cypher
LOAD CSV WITH HEADERS FROM 'file:///organization_demographics.csv' AS row
MERGE (o:Organization {org_id: row.org_id})
SET o.sector = row.sector,
    o.employee_count = toInteger(row.employee_count),
    o.annual_revenue = toFloat(row.annual_revenue),
    o.security_maturity = row.security_maturity,
    o.geographic_region = row.region;
```

#### Step 2: Create Demographic Segments

**Command**:
```cypher
// Create segments based on sector + size + maturity combinations
MATCH (o:Organization)
WITH DISTINCT o.sector AS sector,
              CASE
                WHEN o.employee_count < 50 THEN 'Small'
                WHEN o.employee_count < 250 THEN 'Medium'
                WHEN o.employee_count < 1000 THEN 'Large'
                ELSE 'Enterprise'
              END AS size_category,
              o.security_maturity AS maturity
CREATE (segment:DemographicSegment {
  segment_id: sector + '_' + size_category + '_' + maturity,
  sector: sector,
  size_category: size_category,
  maturity: maturity,
  created_date: date()
});
```

#### Step 3: Assign Organizations to Segments

**Command**:
```cypher
MATCH (o:Organization), (segment:DemographicSegment)
WHERE o.sector = segment.sector
  AND CASE
        WHEN o.employee_count < 50 THEN 'Small'
        WHEN o.employee_count < 250 THEN 'Medium'
        WHEN o.employee_count < 1000 THEN 'Large'
        ELSE 'Enterprise'
      END = segment.size_category
  AND o.security_maturity = segment.maturity
MERGE (o)-[:BELONGS_TO_SEGMENT {assignment_confidence: 0.95}]->(segment);

// Update population counts
MATCH (segment:DemographicSegment)<-[:BELONGS_TO_SEGMENT]-(o:Organization)
WITH segment, count(o) AS pop_count
SET segment.population_count = pop_count;
```

#### Step 4: Calculate Population Metrics

**Command**:
```cypher
// Breach probability per segment
MATCH (segment:DemographicSegment)<-[:BELONGS_TO_SEGMENT]-(o:Organization)
OPTIONAL MATCH (o)-[:EXPERIENCED_BREACH]->(b:BreachEvent)
WITH segment, count(DISTINCT o) AS total, count(b) AS breaches
CREATE (metric:PopulationMetric {
  segment_id: segment.segment_id,
  metric_type: 'breach_probability',
  value: toFloat(breaches) / total,
  timestamp: datetime()
})
CREATE (segment)-[:HAS_POPULATION_METRIC]->(metric);
```

#### Step 5: Predict Seldon Crises

**Command**:
```cypher
// Identify segments approaching crisis inflection points
MATCH (segment:DemographicSegment)-[:HAS_POPULATION_METRIC]->(metric:PopulationMetric {metric_type: 'breach_probability'})
WHERE metric.value > 0.15
  AND segment.population_count >= 100
WITH segment, metric.value AS breach_prob
CREATE (crisis:SeldonCrisis {
  crisis_id: 'CRISIS_' + segment.segment_id,
  segment_id: segment.segment_id,
  probability: breach_prob * 1.5,
  timeframe: '6-12 months',
  crisis_type: 'Security Maturity Inflection',
  triggers: 'Population-scale breach threshold reached',
  prediction_date: date()
})
CREATE (segment)-[:PREDICTED_CRISIS {probability: breach_prob}]->(crisis)
RETURN crisis.crisis_id, crisis.probability, segment.sector, segment.population_count;
```

---

## 8. POST-EXECUTION

### 8.1 Verification Queries

#### Verify Demographic Segments Created

```cypher
MATCH (segment:DemographicSegment)
RETURN segment.sector, segment.size_category, segment.maturity, segment.population_count
ORDER BY segment.population_count DESC
LIMIT 20;
```

#### Population Metrics Summary

```cypher
MATCH (segment:DemographicSegment)-[:HAS_POPULATION_METRIC]->(metric:PopulationMetric)
RETURN segment.sector,
       avg(metric.value) AS avg_breach_prob,
       max(metric.value) AS max_breach_prob
ORDER BY avg_breach_prob DESC;
```

#### Seldon Crisis Predictions

```cypher
MATCH (crisis:SeldonCrisis)
WHERE crisis.probability > 0.20
RETURN crisis.segment_id, crisis.probability, crisis.timeframe
ORDER BY crisis.probability DESC;
```

### 8.2 Success Criteria

| Criterion | Measurement | Threshold | Actual |
|-----------|-------------|-----------|--------|
| Segments created | Count of DemographicSegment | >= 50 | [To fill] |
| Orgs assigned | % orgs with BELONGS_TO_SEGMENT | >= 90% | [To fill] |
| Metrics calculated | Count of PopulationMetric | >= 50 | [To fill] |
| Crises predicted | Count of SeldonCrisis | >= 5 | [To fill] |

---

## 9. ROLLBACK PROCEDURE

```cypher
// Remove psychohistory artifacts
MATCH (segment:DemographicSegment)
WHERE segment.created_date = date()
DETACH DELETE segment;

MATCH (metric:PopulationMetric)
WHERE metric.timestamp > datetime() - duration('PT24H')
DELETE metric;

MATCH (crisis:SeldonCrisis)
WHERE crisis.prediction_date = date()
DELETE crisis;
```

---

## 10. SCHEDULING & AUTOMATION

```cron
# Quarterly demographics update on 1st of Q1,Q2,Q3,Q4 at 8 AM
0 8 1 1,4,7,10 * /home/jim/scripts/etl/proc_132_psychohistory.sh >> /var/log/aeon/proc_132.log 2>&1
```

---

## 11. MONITORING & ALERTING

| Metric | Threshold | Alert |
|--------|-----------|-------|
| Segments with >20% breach prob | > 10 | CRITICAL |
| Predicted crises | > 20 | WARN |

---

## 12. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON ETL Agent | Initial version for E11 |

---

**End of Procedure PROC-132**
