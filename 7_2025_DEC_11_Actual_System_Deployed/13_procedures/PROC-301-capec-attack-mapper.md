# PROCEDURE: [PROC-301] CAPEC-ATT&CK Technique Mapper

**Procedure ID**: PROC-301
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
| **Frequency** | QUARTERLY / ON-DEMAND |
| **Priority** | CRITICAL |
| **Estimated Duration** | 45-90 minutes |
| **Risk Level** | LOW |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Map CAPEC attack patterns to MITRE ATT&CK techniques by extracting taxonomy mappings from CAPEC data and creating USES_TECHNIQUE relationships, completing the critical link between abstract attack patterns and specific adversary techniques in the 8-hop attack chain.

### 2.2 Business Objectives
- [x] Create USES_TECHNIQUE relationships (~1,500+ expected)
- [x] Enable CAPEC→ATT&CK traversal for threat intelligence
- [x] Link attack patterns to documented adversary behaviors
- [x] Support McKenney Q4 "Who are the attackers?" queries

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q3: What do attackers know? | Techniques show attacker TTPs |
| Q4: Who are the attackers? | ATT&CK links to threat actor profiles |
| Q5: How do we defend? | Technique mitigations from ATT&CK |
| Q7: What will happen next? | Predict techniques from CWEs exploited |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running, accessible | `docker ps \| grep neo4j` |
| Network | Access to MITRE | `curl -I https://capec.mitre.org` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query | Expected Result |
|-----------|-------------------|-----------------|
| CAPEC nodes exist | `MATCH (c:CAPEC) RETURN count(c)` | >= 700 |
| Technique nodes exist | `MATCH (t:Technique) RETURN count(t)` | >= 600 |
| CWE→CAPEC exists | `MATCH ()-[r:EXPLOITS_WEAKNESS]->() RETURN count(r)` | >= 2,500 |

### 3.3 Prior Procedures Required

| Procedure ID | Procedure Name |
|--------------|---------------|
| PROC-001 | Schema Migration |
| PROC-201 | CWE-CAPEC Linking |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source Name | Type | Location | Format |
|-------------|------|----------|--------|
| CAPEC XML | File | https://capec.mitre.org/data/xml/capec_latest.xml | XML |
| ATT&CK STIX | File | https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json | JSON |

### 4.2 CAPEC Taxonomy Mapping Schema

```xml
<Attack_Pattern ID="242" Name="Code Injection">
  <Taxonomy_Mappings>
    <Taxonomy_Mapping Taxonomy_Name="ATTACK">
      <Entry_ID>T1059</Entry_ID>
      <Entry_Name>Command and Scripting Interpreter</Entry_Name>
    </Taxonomy_Mapping>
  </Taxonomy_Mappings>
</Attack_Pattern>
```

---

## 5. DESTINATION

### 5.1 Target System

| Field | Value |
|-------|-------|
| **System** | Neo4j |
| **Container** | openspg-neo4j |
| **Port** | 7687 (Bolt) |
| **Volume** | active_neo4j_data |

### 5.2 Target Schema

| Type | Source | Target | Properties |
|------|--------|--------|------------|
| USES_TECHNIQUE | (:CAPEC) | (:Technique) | source, created_timestamp |

---

## 6. TRANSFORMATION LOGIC

### 6.1 Mapping Rules

| Source Field | Target Property | Transformation |
|--------------|-----------------|----------------|
| Entry_ID | Technique.technique_id | Direct (T1234) |
| Entry_Name | Technique.name | Direct |
| Attack_Pattern/@ID | CAPEC.capec_id | Lookup existing |

### 6.2 Validation Rules

| Rule | Field | Validation | Action |
|------|-------|------------|--------|
| VAL-001 | Entry_ID | REGEX `^T\d{4}(\.\\d{3})?$` | SKIP |
| VAL-002 | Taxonomy_Name | == "ATTACK" | SKIP non-ATT&CK |

---

## 7. EXECUTION STEPS

### Step 1: Download CAPEC XML
```bash
mkdir -p /tmp/aeon_etl
curl -o /tmp/aeon_etl/capec_latest.xml https://capec.mitre.org/data/xml/capec_latest.xml
```

### Step 2: Create Technique Constraint
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "CREATE CONSTRAINT technique_id_unique IF NOT EXISTS FOR (t:Technique) REQUIRE t.technique_id IS UNIQUE"
```

### Step 3: Run Mapper Script
```bash
python3 /home/jim/2_OXOT_Projects_Dev/scripts/etl/proc_301_capec_attack_mapper.py \
  --capec-xml /tmp/aeon_etl/capec_latest.xml \
  --neo4j-uri bolt://localhost:7687 \
  --neo4j-user neo4j \
  --neo4j-pass "neo4j@openspg"
```

### Step 4: Verify Results
```cypher
MATCH (capec:CAPEC)-[r:USES_TECHNIQUE]->(t:Technique)
RETURN count(r) AS rel_count, count(DISTINCT capec) AS capec_mapped;
```

---

## 8. POST-EXECUTION VERIFICATION

```cypher
// Test 4-hop chain
MATCH path = (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
              <-[:EXPLOITS_WEAKNESS]-(capec:CAPEC)
              -[:USES_TECHNIQUE]->(tech:Technique)
WHERE cve.cvssV3Severity = 'CRITICAL'
RETURN cve.cve_id, cwe.id, capec.capec_id, tech.technique_id
LIMIT 10;
```

### Success Criteria

| Criterion | Threshold |
|-----------|-----------|
| Relationships created | >= 1,000 |
| CAPEC mapped | >= 300 |
| 4-hop chain works | Returns rows |

---

## 9. ROLLBACK PROCEDURE

```cypher
MATCH (capec:CAPEC)-[r:USES_TECHNIQUE]->(t:Technique)
WHERE r.source = 'capec:mitre-attack'
DELETE r;
```

---

## 10. SCHEDULING

```cron
# Quarterly on 1st of Jan/Apr/Jul/Oct at 5 AM
0 5 1 1,4,7,10 * /home/jim/2_OXOT_Projects_Dev/scripts/etl/proc_301_capec_attack_mapper.sh
```

### Pipeline Position
```
PROC-201 (CWE-CAPEC) → PROC-301 (THIS) → PROC-501 (Threat Actors)
```

---

## 11. CHANGE HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-26 | Initial version |

---

**End of Procedure PROC-301**
