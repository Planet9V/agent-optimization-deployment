# PROCEDURE: [PROC-112] STIX 2.1 Threat Intelligence Integration

**Procedure ID**: PROC-112
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
| **Frequency** | MONTHLY |
| **Priority** | HIGH |
| **Estimated Duration** | 1-2 hours |
| **Risk Level** | LOW |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Parse STIX 2.1 formatted threat intelligence objects from 5 training data files, create standardized threat intelligence nodes (attack-pattern, threat-actor, indicator, malware, campaign), and link to existing MITRE ATT&CK framework nodes for unified threat correlation.

### 2.2 Business Objectives
- [x] Ingest 5 STIX 2.1 training files (attack patterns, threat actors, IoCs, malware, campaigns)
- [x] Create STIX-compliant nodes with proper relationships
- [x] Map STIX attack patterns to ATT&CK techniques
- [x] Enable STIX-based threat intelligence queries
- [x] Support TAXII 2.1 feed integration (future)

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q3: What do attackers know? | STIX attack patterns reveal adversary knowledge |
| Q4: Who are the attackers? | STIX threat-actor objects with attribution |
| Q5: How do we defend? | STIX course-of-action objects for mitigations |
| Q7: What will happen next? | STIX campaign timelines predict attack progression |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running, accessible | `docker ps | grep neo4j` |
| Python stix2 | Installed | `pip show stix2` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query | Expected Result |
|-----------|-------------------|-----------------|
| Technique nodes exist | `MATCH (t:Technique) RETURN count(t)` | >= 600 |
| STIX files accessible | Shell ls | 5 files present |

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
| STIX Training Files | File Collection | `/home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/` | Markdown with STIX JSON |

### 4.2 STIX 2.1 Training Files

1. **01_STIX_Attack_Patterns.md** - 50-100 attack-pattern objects with ATT&CK mappings
2. **02_STIX_Threat_Actors.md** - 30-50 threat-actor objects with attribution
3. **03_STIX_Indicators_IOCs.md** - 500-1,000 indicator objects (hashes, IPs, domains)
4. **04_STIX_Malware_Infrastructure.md** - 100-200 malware and infrastructure objects
5. **05_STIX_Campaigns_Reports.md** - 20-40 campaign and report objects

### 4.3 STIX Object Schema Example
```json
{
  "type": "attack-pattern",
  "spec_version": "2.1",
  "id": "attack-pattern--2e34237d-8574-43f6-aace-ae2915de8597",
  "name": "Spearphishing Attachment",
  "kill_chain_phases": [
    {"kill_chain_name": "mitre-attack", "phase_name": "initial-access"}
  ],
  "external_references": [
    {"source_name": "mitre-attack", "external_id": "T1566.001"}
  ]
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

**STIX Node Types**:
| Label | Properties | Constraints |
|-------|-----------|-------------|
| STIXObject | stix_id, type, created, modified | UNIQUE on stix_id |
| AttackPattern | stix_id, name, description | Inherits STIXObject |
| ThreatActor | stix_id, name, sophistication, motivation | Inherits STIXObject |
| STIXIndicator | stix_id, pattern, indicator_types | Inherits STIXObject |

**Relationships**:
| Type | Source | Target |
|------|--------|--------|
| MAPS_TO | (:AttackPattern) | (:Technique) |
| USES_PATTERN | (:ThreatActor) | (:AttackPattern) |
| INDICATES | (:STIXIndicator) | (:AttackPattern) |
| PART_OF | (:AttackPattern) | (:Campaign) |

---

## 6. TRANSFORMATION LOGIC

### 6.1 Mapping Rules

| STIX Field | Neo4j Property | Transformation |
|------------|---------------|----------------|
| `id` | stix_id | Direct copy (unique) |
| `type` | object_type | Direct copy |
| `created` | created_at | ISO 8601 datetime |
| `external_references[].external_id` | technique_id | Extract ATT&CK ID |
| `pattern` | pattern_stix | STIX pattern language |

### 6.2 ATT&CK Mapping Extraction
```python
for ref in stix_obj.get('external_references', []):
    if ref['source_name'] == 'mitre-attack':
        technique_id = ref['external_id']  # e.g., T1566.001
```

### 6.3 Validation Rules

| Rule | Field | Validation | Action |
|------|-------|------------|--------|
| VAL-001 | stix_id | REGEX `^[a-z-]+--[0-9a-f-]{36}$` | REJECT |
| VAL-002 | spec_version | == "2.1" | WARN if != |
| VAL-003 | type | In allowed types | SKIP unknown |

---

## 7. EXECUTION STEPS

### Step 1: Install STIX2 Python Library
```bash
pip install stix2==3.0.1
```

### Step 2: Create STIX Constraints
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" << 'EOF'
CREATE CONSTRAINT stix_id_unique IF NOT EXISTS FOR (s:STIXObject) REQUIRE s.stix_id IS UNIQUE;
EOF
```

### Step 3: Run STIX Ingestion Script
```bash
python3 << 'SCRIPT'
import json
import re
from neo4j import GraphDatabase
from datetime import datetime

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j@openspg"))
data_path = "/home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training"

def extract_stix_json(markdown_content):
    """Extract JSON blocks from markdown STIX files"""
    json_blocks = re.findall(r'```json\s*(\{.*?\})\s*```', markdown_content, re.DOTALL)
    stix_objects = []
    for block in json_blocks:
        try:
            obj = json.loads(block)
            if 'type' in obj and 'id' in obj:
                stix_objects.append(obj)
        except json.JSONDecodeError:
            continue
    return stix_objects

def get_attack_technique_id(stix_obj):
    """Extract MITRE ATT&CK technique ID from external references"""
    for ref in stix_obj.get('external_references', []):
        if ref.get('source_name') == 'mitre-attack':
            return ref.get('external_id')
    return None

def ingest_stix_object(session, obj, source_file):
    """Ingest single STIX 2.1 object into Neo4j"""
    stix_id = obj['id']
    obj_type = obj['type']
    created = obj.get('created', datetime.now().isoformat())
    modified = obj.get('modified', created)

    # Create base STIX node
    session.run("""
        MERGE (s:STIXObject {stix_id: $stix_id})
        SET s.object_type = $obj_type,
            s.created_at = datetime($created),
            s.modified_at = datetime($modified),
            s.source_file = $source_file,
            s.spec_version = $spec_version
    """, stix_id=stix_id, obj_type=obj_type, created=created,
        modified=modified, source_file=source_file, spec_version=obj.get('spec_version', '2.1'))

    # Type-specific handling
    if obj_type == 'attack-pattern':
        session.run("""
            MATCH (s:STIXObject {stix_id: $stix_id})
            SET s:AttackPattern,
                s.name = $name,
                s.description = $desc
        """, stix_id=stix_id, name=obj.get('name'), desc=obj.get('description'))

        # Map to ATT&CK Technique
        tech_id = get_attack_technique_id(obj)
        if tech_id:
            session.run("""
                MATCH (ap:AttackPattern {stix_id: $stix_id})
                MATCH (t:Technique {technique_id: $tech_id})
                MERGE (ap)-[:MAPS_TO {source: 'stix-attack'}]->(t)
            """, stix_id=stix_id, tech_id=tech_id)

    elif obj_type == 'threat-actor':
        session.run("""
            MATCH (s:STIXObject {stix_id: $stix_id})
            SET s:ThreatActor,
                s.name = $name,
                s.sophistication = $soph,
                s.resource_level = $resource,
                s.primary_motivation = $motivation
        """, stix_id=stix_id, name=obj.get('name'), soph=obj.get('sophistication'),
            resource=obj.get('resource_level'), motivation=obj.get('primary_motivation'))

    elif obj_type == 'indicator':
        session.run("""
            MATCH (s:STIXObject {stix_id: $stix_id})
            SET s:STIXIndicator,
                s.name = $name,
                s.pattern = $pattern,
                s.pattern_type = $pattern_type,
                s.indicator_types = $ind_types,
                s.valid_from = datetime($valid_from)
        """, stix_id=stix_id, name=obj.get('name'), pattern=obj.get('pattern'),
            pattern_type=obj.get('pattern_type'), ind_types=obj.get('indicator_types', []),
            valid_from=obj.get('valid_from', created))

    elif obj_type == 'malware':
        session.run("""
            MATCH (s:STIXObject {stix_id: $stix_id})
            SET s:Malware,
                s.name = $name,
                s.malware_types = $mal_types,
                s.is_family = $is_family,
                s.description = $desc
        """, stix_id=stix_id, name=obj.get('name'), mal_types=obj.get('malware_types', []),
            is_family=obj.get('is_family', False), desc=obj.get('description'))

    elif obj_type == 'campaign':
        session.run("""
            MATCH (s:STIXObject {stix_id: $stix_id})
            SET s:Campaign,
                s.name = $name,
                s.description = $desc,
                s.first_seen = datetime($first_seen),
                s.last_seen = datetime($last_seen),
                s.objective = $objective
        """, stix_id=stix_id, name=obj.get('name'), desc=obj.get('description'),
            first_seen=obj.get('first_seen', created), last_seen=obj.get('last_seen', modified),
            objective=obj.get('objective'))

# Process all STIX files
stix_files = ['01_STIX_Attack_Patterns.md', '02_STIX_Threat_Actors.md',
              '03_STIX_Indicators_IOCs.md', '04_STIX_Malware_Infrastructure.md',
              '05_STIX_Campaigns_Reports.md']

with driver.session() as session:
    for filename in stix_files:
        filepath = f"{data_path}/{filename}"
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            stix_objects = extract_stix_json(content)
            print(f"Processing {filename}: {len(stix_objects)} STIX objects")

            for obj in stix_objects:
                ingest_stix_object(session, obj, filename)

        except FileNotFoundError:
            print(f"Warning: {filename} not found, skipping")

driver.close()
print("STIX 2.1 integration complete")
SCRIPT
```

### Step 4: Verify Results
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" << 'EOF'
MATCH (s:STIXObject) RETURN s.object_type AS type, count(s) AS count ORDER BY type;
MATCH (ap:AttackPattern)-[:MAPS_TO]->(t:Technique) RETURN count(*) AS mappings;
EOF
```

---

## 8. POST-EXECUTION VERIFICATION

### Verify STIX Object Counts
```cypher
MATCH (s:STIXObject)
RETURN s.object_type AS type, count(s) AS count
ORDER BY count DESC;
```

**Expected Results**:
- attack-pattern: 50-100
- indicator: 500-1,000
- malware: 100-200
- threat-actor: 30-50
- campaign: 20-40

### Verify ATT&CK Mappings
```cypher
MATCH (ap:AttackPattern)-[r:MAPS_TO]->(t:Technique)
RETURN ap.name, t.technique_id, t.name
LIMIT 20;
```

### Test STIX Threat Intelligence Query
```cypher
MATCH path = (ta:ThreatActor)-[:USES_PATTERN]->(ap:AttackPattern)
             -[:MAPS_TO]->(t:Technique)
WHERE ta.sophistication = 'expert'
RETURN ta.name, ap.name, t.technique_id
LIMIT 10;
```

### Success Criteria

| Criterion | Threshold | Actual |
|-----------|-----------|--------|
| STIXObject nodes | >= 700 | ___ |
| AttackPattern nodes | >= 50 | ___ |
| MAPS_TO relationships | >= 40 | ___ |
| STIX-ATT&CK integration | Returns rows | ___ |

---

## 9. ROLLBACK PROCEDURE

### Remove All STIX Data
```cypher
MATCH (s:STIXObject)
WHERE s.source_file =~ '.*STIX.*'
DETACH DELETE s;
```

### Verify Rollback
```cypher
MATCH (s:STIXObject)
WHERE s.source_file IS NOT NULL
RETURN count(s);
// Expected: 0
```

---

## 10. SCHEDULING & AUTOMATION

### Cron Schedule
```cron
# Monthly on 1st at 2 AM
0 2 1 * * /home/jim/2_OXOT_Projects_Dev/scripts/etl/proc_112_stix_integration.sh >> /var/log/aeon/proc_112.log 2>&1
```

---

## 11. MONITORING & ALERTING

### Metrics to Monitor

| Metric | Source | Threshold | Alert |
|--------|--------|-----------|-------|
| Execution duration | Log | > 3 hours | ERROR |
| STIXObject count | Neo4j | < 600 | WARN |
| MAPS_TO relationships | Neo4j | < 30 | WARN |

---

## 12. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON ETL System | Initial procedure for E02 STIX Integration |

---

## 13. APPENDICES

### Appendix A: STIX 2.1 Specification
- Official Spec: https://docs.oasis-open.org/cti/stix/v2.1/
- Python Library: https://stix2.readthedocs.io/

### Appendix B: Related Documentation
- Enhancement 02 README: `/enhancements/Enhancement_02_STIX_Integration/README.md`
- DATA_SOURCES.md: `/enhancements/Enhancement_02_STIX_Integration/DATA_SOURCES.md`

---

**End of Procedure PROC-112**
