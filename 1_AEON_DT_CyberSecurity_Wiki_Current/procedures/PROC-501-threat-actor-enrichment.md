# PROCEDURE: [PROC-501] Threat Actor Enrichment

**Procedure ID**: PROC-501
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
| **Frequency** | MONTHLY / ON-DEMAND |
| **Priority** | HIGH |
| **Estimated Duration** | 60-120 minutes |
| **Risk Level** | LOW |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Create and enrich ThreatActor nodes with behavioral profiles, technique usage patterns, and McKenney-Lacan psychometric attributes by loading MITRE ATT&CK group data and creating USES relationships to techniques.

### 2.2 Business Objectives
- [x] Create ThreatActor nodes (~150+ groups)
- [x] Create ThreatActor→Technique USES relationships (~2,000+)
- [x] Add McKenney-Lacan psychometric profiles
- [x] Enable predictive threat modeling (Q7)

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q3: What do attackers know? | Via technique proficiency |
| Q4: Who are the attackers? | **PRIMARY** - Actor profiles |
| Q5: How do we defend? | Counter-techniques based on TTPs |
| Q7: What will happen next? | Predictive modeling from profiles |
| Q8: What should we do? | Prioritize based on threat targeting |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running | `docker ps \| grep neo4j` |
| Network | Access to MITRE ATT&CK | `curl -I https://raw.githubusercontent.com/mitre/cti` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query | Expected Result |
|-----------|-------------------|-----------------|
| Technique nodes exist | `MATCH (t:Technique) RETURN count(t)` | >= 600 |
| CAPEC→Technique exists | `MATCH ()-[r:USES_TECHNIQUE]->() RETURN count(r)` | >= 1,000 |

### 3.3 Prior Procedures Required

| Procedure ID | Procedure Name |
|--------------|---------------|
| PROC-001 | Schema Migration |
| PROC-301 | CAPEC-ATT&CK Mapping |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source Name | Type | Location | Format |
|-------------|------|----------|--------|
| ATT&CK STIX | File | https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json | STIX JSON |

### 4.2 STIX Intrusion Set Schema

```json
{
  "type": "intrusion-set",
  "id": "intrusion-set--2e290bfe-93b5-48ce-97d6-edcd6d32b7cf",
  "name": "APT29",
  "aliases": ["CozyBear", "The Dukes"],
  "external_references": [{"source_name": "mitre-attack", "external_id": "G0016"}],
  "resource_level": "government",
  "primary_motivation": "espionage"
}
```

### 4.3 STIX Relationship Schema

```json
{
  "type": "relationship",
  "relationship_type": "uses",
  "source_ref": "intrusion-set--...",
  "target_ref": "attack-pattern--..."
}
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

| Label | Key Properties |
|-------|---------------|
| ThreatActor | actor_id, name, aliases, resource_level, motivation |
| ThreatActorProfile | profile_id, sophistication, aggression, persistence |

| Relationship | Source | Target |
|--------------|--------|--------|
| USES | ThreatActor | Technique |
| HAS_PROFILE | ThreatActor | ThreatActorProfile |

---

## 6. TRANSFORMATION LOGIC

### 6.1 Mapping Rules

| Source Field | Target Property |
|--------------|-----------------|
| external_id | ThreatActor.actor_id |
| name | ThreatActor.name |
| aliases | ThreatActor.aliases |
| resource_level | ThreatActor.resource_level |
| primary_motivation | ThreatActor.motivation |

### 6.2 McKenney-Lacan Psychometric Calculation

```python
def calculate_psychometrics(group_data, relationships):
    techniques_used = len(relationships)
    return {
        'sophistication': min(1.0, techniques_used / 50),
        'persistence': min(1.0, years_active / 10),
        'resource_access': {'government': 1.0, 'organization': 0.8}.get(resource_level, 0.5),
        'aggression': {'espionage': 0.6, 'financial-gain': 0.8}.get(motivation, 0.5)
    }
```

---

## 7. EXECUTION STEPS

### Step 1: Download ATT&CK STIX
```bash
mkdir -p /tmp/aeon_etl
curl -o /tmp/aeon_etl/enterprise-attack.json \
  https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json
```

### Step 2: Create Constraints
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "CREATE CONSTRAINT actor_id_unique IF NOT EXISTS FOR (a:ThreatActor) REQUIRE a.actor_id IS UNIQUE"
```

### Step 3: Run Enrichment Script
```bash
python3 /home/jim/2_OXOT_Projects_Dev/scripts/etl/proc_501_threat_actor_enrichment.py \
  --attack-stix /tmp/aeon_etl/enterprise-attack.json \
  --neo4j-uri bolt://localhost:7687 \
  --neo4j-user neo4j \
  --neo4j-pass "neo4j@openspg" \
  --enable-psychometrics
```

### Step 4: Verify Full Attack Chain
```cypher
MATCH path = (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
              <-[:EXPLOITS_WEAKNESS]-(capec:CAPEC)
              -[:USES_TECHNIQUE]->(tech:Technique)
              <-[:USES]-(actor:ThreatActor)
WHERE cve.cvssV3Severity = 'CRITICAL'
RETURN cve.cve_id, actor.name LIMIT 5;
```

---

## 8. POST-EXECUTION VERIFICATION

```cypher
MATCH (a:ThreatActor)-[r:USES]->(t:Technique)
RETURN count(a) AS actors, count(r) AS uses_relationships;
```

### Success Criteria

| Criterion | Threshold |
|-----------|-----------|
| ThreatActors created | >= 130 |
| USES relationships | >= 2,000 |
| Full chain works | Returns rows |

---

## 9. ROLLBACK PROCEDURE

```cypher
MATCH (p:ThreatActorProfile) DETACH DELETE p;
MATCH ()-[r:USES]->() DELETE r;
MATCH (a:ThreatActor) DETACH DELETE a;
```

---

## 10. SCHEDULING

```cron
# Monthly on 15th at 3 AM
0 3 15 * * /home/jim/2_OXOT_Projects_Dev/scripts/etl/proc_501_threat_actor_enrichment.sh
```

### Pipeline Position
```
PROC-301 (CAPEC-ATT&CK) → PROC-501 (THIS) → PROC-901 (Chain Validation)
```

---

## 11. CHANGE HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-26 | Initial version |

---

**End of Procedure PROC-501**
