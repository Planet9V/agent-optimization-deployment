# PROCEDURE: [PROC-134] Attack Path Modeling & Graph Traversal

**Procedure ID**: PROC-134
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
| **Frequency** | WEEKLY |
| **Priority** | HIGH |
| **Estimated Duration** | 45-90 minutes |
| **Risk Level** | MEDIUM |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Model multi-hop attack paths from CVE exploitation through MITRE ATT&CK techniques to target equipment, enabling proactive defense and attack surface reduction.

### 2.2 Business Objectives
- [x] Identify exploitable attack chains (CVE → CWE → CAPEC → ATT&CK → Equipment)
- [x] Calculate path probability and impact scores
- [x] Visualize lateral movement opportunities
- [x] Prioritize choke points for defense hardening
- [x] Enable red team/blue team scenario planning

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q3: What do attackers know? | Complete attack chain visibility |
| Q4: Who are the attackers? | Threat actor TTPs mapped to paths |
| Q5: How do we defend? | Choke point identification |
| Q8: What should we do? | Path-based defense prioritization |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification |
|-----------|---------------|--------------|
| Neo4j | Running | `docker ps \| grep neo4j` |
| Graph Data Science Library | Installed | Cypher GDS procedures available |

### 3.2 Data Pre-Conditions

| Condition | Verification Query | Expected |
|-----------|-------------------|----------|
| CVE→CWE links | `MATCH (:CVE)-[:IS_WEAKNESS_TYPE]->(:CWE) RETURN count(*)` | >= 150,000 |
| CWE→CAPEC links | `MATCH (:CWE)-[:EXPLOITED_BY]->(:CAPEC) RETURN count(*)` | >= 1,000 |
| CAPEC→ATT&CK links | `MATCH (:CAPEC)-[:IMPLEMENTS]->(:AttackPattern) RETURN count(*)` | >= 500 |
| ATT&CK→Equipment | `MATCH (:AttackPattern)-[:TARGETS]->(:Equipment) RETURN count(*)` | >= 10,000 |

### 3.3 Prior Procedures Required

| Procedure ID | Procedure Name | Dependency |
|--------------|---------------|------------|
| PROC-101 | CVE Enrichment | CVE→CWE relationships |
| PROC-201 | CWE-CAPEC Linking | CWE→CAPEC relationships |
| PROC-301 | CAPEC-ATT&CK Mapping | CAPEC→ATT&CK relationships |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source | Type | Location | Format |
|--------|------|----------|--------|
| Neo4j Knowledge Graph | Graph | localhost:7687 | Cypher |
| MITRE ATT&CK Matrix | Static | JSON | JSON |

### 4.2 Attack Path Definition

**8-Hop Attack Chain**:
```
CVE (vulnerability)
  → CWE (weakness type)
    → CAPEC (attack pattern)
      → ATT&CK Technique (TTP)
        → ATT&CK Tactic (objective)
          → ThreatActor (adversary)
            → Campaign (operation)
              → Equipment (target asset)
```

**Path Probability**:
```
Path_Probability = CVE.epss × CWE.exploitability × CAPEC.likelihood × ATT&CK.prevalence
```

**Path Impact**:
```
Path_Impact = Equipment.tier_criticality × CVE.cvssV3BaseScore × ATT&CK.impact_score
```

**Path Risk Score**:
```
Path_Risk = Path_Probability × Path_Impact
```

---

## 5. DESTINATION

### 5.1 Target Schema

#### Node Types Created

| Label | Properties | Purpose |
|-------|-----------|---------|
| AttackPath | path_id, hops, probability, impact, risk_score | Complete attack chain |
| ChokePoint | node_id, centrality_score, paths_through, mitigation_priority | Defense hardening targets |

#### Relationship Types Created

| Type | Source | Target | Properties |
|------|--------|--------|------------|
| PART_OF_PATH | (Any node in chain) | (:AttackPath) | hop_number |
| IS_CHOKE_POINT | (:ChokePoint) | (Node in graph) | betweenness_centrality |

---

## 6. TRANSFORMATION LOGIC

### 6.1 Attack Path Discovery

```cypher
// Find all 8-hop attack paths
MATCH path = (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
             -[:EXPLOITED_BY]->(capec:CAPEC)
             -[:IMPLEMENTS]->(att:AttackPattern)
             -[:USES_TACTIC]->(tactic:Tactic)
             -[:EMPLOYED_BY]->(actor:ThreatActor)
             -[:EXECUTES]->(campaign:Campaign)
             -[:TARGETS]->(equipment:Equipment)
WHERE cve.priority = 'NOW'
WITH path,
     cve.epss AS cve_prob,
     cve.cvssV3BaseScore AS cve_impact,
     CASE equipment.tier
       WHEN 'Tier 1' THEN 1.0
       WHEN 'Tier 2' THEN 0.7
       WHEN 'Tier 3' THEN 0.4
       ELSE 0.3
     END AS equipment_criticality
CREATE (ap:AttackPath {
  path_id: id(path),
  hops: length(path),
  probability: cve_prob * 0.5 * 0.3,  // Simplified
  impact: cve_impact * equipment_criticality,
  risk_score: (cve_prob * 0.5 * 0.3) * (cve_impact * equipment_criticality),
  discovered_date: date()
})
WITH ap, path
UNWIND nodes(path) AS node
CREATE (node)-[:PART_OF_PATH {hop_number: [i IN range(0, length(path)) WHERE nodes(path)[i] = node | i][0]}]->(ap);
```

### 6.2 Choke Point Identification

```cypher
// Calculate betweenness centrality to find choke points
CALL gds.graph.project(
  'attack-graph',
  ['CVE', 'CWE', 'CAPEC', 'AttackPattern', 'ThreatActor', 'Equipment'],
  ['IS_WEAKNESS_TYPE', 'EXPLOITED_BY', 'IMPLEMENTS', 'TARGETS']
);

CALL gds.betweenness.stream('attack-graph')
YIELD nodeId, score
WITH gds.util.asNode(nodeId) AS node, score
WHERE score > 100
CREATE (cp:ChokePoint {
  node_id: id(node),
  node_label: labels(node)[0],
  centrality_score: score,
  mitigation_priority: CASE
    WHEN score > 1000 THEN 'CRITICAL'
    WHEN score > 500 THEN 'HIGH'
    ELSE 'MEDIUM'
  END
})
CREATE (cp)-[:IS_CHOKE_POINT]->(node);
```

---

## 7. EXECUTION STEPS

### 7.1 Step-by-Step Execution

#### Step 1: Verify Attack Chain Completeness

**Command**:
```cypher
// Check each hop in the chain exists
MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
RETURN 'CVE→CWE' AS hop, count(*) AS relationship_count
UNION
MATCH (cwe:CWE)-[:EXPLOITED_BY]->(capec:CAPEC)
RETURN 'CWE→CAPEC' AS hop, count(*) AS relationship_count
UNION
MATCH (capec:CAPEC)-[:IMPLEMENTS]->(att:AttackPattern)
RETURN 'CAPEC→ATT&CK' AS hop, count(*) AS relationship_count
UNION
MATCH (att:AttackPattern)-[:TARGETS]->(e:Equipment)
RETURN 'ATT&CK→Equipment' AS hop, count(*) AS relationship_count;
```

**Expected**: All hops > 0

#### Step 2: Create Graph Projection for GDS

**Command**:
```cypher
CALL gds.graph.project.cypher(
  'attack-path-graph',
  'MATCH (n) WHERE n:CVE OR n:CWE OR n:CAPEC OR n:AttackPattern OR n:Equipment RETURN id(n) AS id',
  'MATCH (a)-[r]->(b) WHERE type(r) IN ["IS_WEAKNESS_TYPE", "EXPLOITED_BY", "IMPLEMENTS", "TARGETS"] RETURN id(a) AS source, id(b) AS target'
);
```

#### Step 3: Find Critical Attack Paths

**Command**:
```cypher
// Find paths from NOW priority CVEs to Tier 1 equipment
MATCH path = (cve:CVE {priority: 'NOW'})-[*4..8]-(equipment:Equipment {tier: 'Tier 1'})
WHERE ALL(r IN relationships(path) WHERE type(r) IN ['IS_WEAKNESS_TYPE', 'EXPLOITED_BY', 'IMPLEMENTS', 'TARGETS'])
WITH path,
     cve.epss AS epss,
     cve.cvssV3BaseScore AS cvss,
     length(path) AS hop_count
WHERE hop_count >= 4 AND hop_count <= 8
CREATE (ap:AttackPath {
  path_id: toString(id(path)),
  source_cve: cve.cve_id,
  target_equipment: equipment.equipment_id,
  hops: hop_count,
  probability: epss * 0.5,
  impact: cvss * 1.0,
  risk_score: (epss * 0.5) * (cvss * 1.0),
  discovered_date: date()
})
WITH ap, path
UNWIND nodes(path) AS node
MERGE (node)-[:PART_OF_PATH {hop_number: [i IN range(0, length(path)) WHERE nodes(path)[i] = node | i][0]}]->(ap)
RETURN count(ap) AS paths_created;
```

#### Step 4: Calculate Betweenness Centrality

**Command**:
```cypher
CALL gds.betweenness.write('attack-path-graph', {
  writeProperty: 'betweenness_centrality'
})
YIELD centralityDistribution
RETURN centralityDistribution;
```

#### Step 5: Identify Top Choke Points

**Command**:
```cypher
MATCH (n)
WHERE n.betweenness_centrality > 100
CREATE (cp:ChokePoint {
  node_id: id(n),
  node_label: labels(n)[0],
  node_name: coalesce(n.cve_id, n.id, n.name),
  centrality_score: n.betweenness_centrality,
  paths_through: n.betweenness_centrality,
  mitigation_priority: CASE
    WHEN n.betweenness_centrality > 1000 THEN 'CRITICAL'
    WHEN n.betweenness_centrality > 500 THEN 'HIGH'
    WHEN n.betweenness_centrality > 100 THEN 'MEDIUM'
    ELSE 'LOW'
  END,
  identified_date: date()
})
MERGE (cp)-[:IS_CHOKE_POINT]->(n)
RETURN cp.node_label, cp.node_name, cp.centrality_score, cp.mitigation_priority
ORDER BY cp.centrality_score DESC
LIMIT 20;
```

---

## 8. POST-EXECUTION

### 8.1 Verification Queries

#### Verify Attack Paths Created

```cypher
MATCH (ap:AttackPath)
RETURN count(ap) AS total_paths,
       avg(ap.hops) AS avg_hops,
       max(ap.risk_score) AS max_risk
```

**Expected**: >= 100 paths

#### Top 10 Highest Risk Attack Paths

```cypher
MATCH (ap:AttackPath)
MATCH (cve:CVE)-[:PART_OF_PATH]->(ap)
MATCH (equipment:Equipment)-[:PART_OF_PATH]->(ap)
RETURN cve.cve_id, equipment.equipment_id, ap.hops, ap.risk_score
ORDER BY ap.risk_score DESC
LIMIT 10;
```

#### Critical Choke Points for Defense

```cypher
MATCH (cp:ChokePoint)
WHERE cp.mitigation_priority = 'CRITICAL'
MATCH (cp)-[:IS_CHOKE_POINT]->(n)
RETURN labels(n)[0] AS node_type,
       coalesce(n.cve_id, n.id, n.name) AS node_identifier,
       cp.centrality_score,
       cp.paths_through
ORDER BY cp.centrality_score DESC
LIMIT 10;
```

### 8.2 Success Criteria

| Criterion | Measurement | Threshold | Actual |
|-----------|-------------|-----------|--------|
| Attack paths discovered | Count of AttackPath | >= 100 | [To fill] |
| Average path length | avg(hops) | 4-8 | [To fill] |
| Choke points identified | Count of ChokePoint | >= 20 | [To fill] |
| Critical choke points | ChokePoint {priority='CRITICAL'} | >= 5 | [To fill] |

---

## 9. ROLLBACK PROCEDURE

```cypher
// Remove attack path artifacts
MATCH (ap:AttackPath)
WHERE ap.discovered_date = date()
DETACH DELETE ap;

MATCH (cp:ChokePoint)
WHERE cp.identified_date = date()
DETACH DELETE cp;

// Drop GDS graph projection
CALL gds.graph.drop('attack-path-graph');
```

---

## 10. SCHEDULING & AUTOMATION

```cron
# Weekly attack path analysis on Sundays at 3 AM
0 3 * * 0 /home/jim/scripts/etl/proc_134_attack_paths.sh >> /var/log/aeon/proc_134.log 2>&1
```

---

## 11. MONITORING & ALERTING

| Metric | Threshold | Alert |
|--------|-----------|-------|
| New critical paths | > 50 | CRITICAL |
| Choke point centrality | > 2000 | WARN (single point of failure) |
| Paths to Tier 1 equipment | > 100 | INFO |

---

## 12. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON ETL Agent | Initial version for E13 |

---

**End of Procedure PROC-134**
