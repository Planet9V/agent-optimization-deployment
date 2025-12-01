# UCO Systematic Import Plan
**Created:** 2025-10-27
**Purpose:** Comprehensive systematic import of ALL cybersecurity data files into Neo4j using UCO schema
**Total Files:** 807
**Status:** READY - Awaiting CVE import completion

---

## Executive Summary

This plan ensures **systematic, complete, and consistent** import of all cybersecurity data files from `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j` into the CybersecurityKB knowledge graph using the Unified Cybersecurity Ontology (UCO) schema.

**Critical Requirements:**
- ✅ **COMPLETE**: Process ALL 807 files - no files skipped
- ✅ **SYSTEMATIC**: Follow UCO schema structure and relationships
- ✅ **CONSISTENT**: Use namespace `CybersecurityKB` throughout
- ✅ **VERIFIED**: Track and validate every import

---

## Import Strategy: Swarm Coordination

### Phase 1: UCO Schema Foundation (FIRST)
**Priority:** CRITICAL - Must complete before data import
**Agent:** `code-analyzer` + `system-architect`

**Tasks:**
1. Parse all UCO ontology files (.owl, .ttl)
2. Extract entity classes, properties, relationships
3. Create Neo4j schema constraints and indexes
4. Register entity types in OpenSPG MySQL database
5. Validate schema completeness

**Files:**
- `/home/jim/2_OXOT_Projects_Dev/Unified-Cybersecurity-Ontology/uco_1_5.owl`
- `/home/jim/2_OXOT_Projects_Dev/Unified-Cybersecurity-Ontology/uco2.ttl`
- `/home/jim/2_OXOT_Projects_Dev/Unified-Cybersecurity-Ontology/uco_1_5_rdf.owl`

---

### Phase 2: Standard Integrations (SECOND)
**Priority:** HIGH - Required for data mappings
**Agent:** `hierarchical-coordinator` (spawn 7 specialized agents in parallel)

#### 2.1 ATT&CK Framework
**Agent:** `researcher` + `coder`
**Directory:** `/Import_to_neo4j/Unified-Cybersecurity-Ontology/attck/`
**Entity Types:** AttackPattern, TTP, KillChain, KillChainPhase, Tactic, Technique, SubTechnique
**Namespace:** `CybersecurityKB`

#### 2.2 CAPEC (Common Attack Patterns)
**Agent:** `researcher` + `coder`
**Directory:** `/Import_to_neo4j/Unified-Cybersecurity-Ontology/capec/`
**Entity Types:** AttackPattern, Consequence, Skill
**Relationships:** `capec:consequence`, `capec:skillRequired`

#### 2.3 CWE (Common Weakness Enumeration)
**Agent:** `researcher` + `coder`
**Directory:** `/Import_to_neo4j/Unified-Cybersecurity-Ontology/cwe/`
**Entity Types:** Weakness, Consequence, Mitigation, ModeOfIntroduction
**Relationships:** `cwe:parentOf`, `cwe:childOf`, `cwe:peerOf`, `cwe:canPrecede`

#### 2.4 STIX 2.0
**Agent:** `researcher` + `coder`
**Directory:** `/Import_to_neo4j/Unified-Cybersecurity-Ontology/stix/`
**Entity Types:** Campaign, IntrusionSet, ThreatActor, Malware, Tool, Identity, Vulnerability, Indicator, Observable
**Relationships:** `stx:attributedTo`, `stx:authoredBy`, `stx:exploits`, `stx:uses`

#### 2.5 MISP
**Agent:** `researcher` + `coder`
**Directory:** `/Import_to_neo4j/Unified-Cybersecurity-Ontology/misp/`
**Entity Types:** AS, Btc, CampaignId, CampaignName, EmailAttachment, GithubRepository, Hex, Datetime
**Properties:** `misp:comment`, `misp:timestamp`, `misp:toIds`, `misp:value`

#### 2.6 TAXII
**Agent:** `researcher` + `coder`
**Directory:** `/Import_to_neo4j/Unified-Cybersecurity-Ontology/taxii/`
**Entity Types:** Server, ApiRoot, Collection
**Relationships:** `txi:hasApiRoot`, `txi:hasCollection`
**Properties:** `txi:canRead`, `txi:canWrite`, `txi:hasUrl`

#### 2.7 MITRE Framework
**Agent:** `researcher` + `coder`
**Directory:** `/Import_to_neo4j/Unified-Cybersecurity-Ontology/mitre/`
**Files:** `mitre.ttl`
**Integration:** MITRE ATT&CK techniques and cyber threat intelligence

---

### Phase 3: MITRE EM3D Data (THIRD)
**Priority:** HIGH
**Agent:** `mesh-coordinator` (parallel processing)
**Directory:** `/Import_to_neo4j/02_MITRE_EM3D/`

**Processing:**
1. Discover all data files
2. Parse entity types (attacks, techniques, mitigations)
3. Create UCO-compliant entities
4. Link to ATT&CK framework entities

---

### Phase 4: Annual Security Reports (FOURTH)
**Priority:** MEDIUM
**Agent:** `adaptive-coordinator` (year-by-year parallel processing)
**Directory:** `/Import_to_neo4j/Annual_Security_Reports/`

**Subdirectories:**
- `2020/` - Security reports from 2020
- `2021/` - Security reports from 2021
- `2022/` - Security reports from 2022
- `2023/` - Security reports from 2023
- `2024/` - Security reports from 2024
- `2025/` - Security reports from 2025

**Entity Types:**
- Incident, Campaign, ThreatActor, Vulnerability, AttackPattern

**Processing Strategy:**
1. Spawn 6 agents (one per year)
2. Each agent processes all reports for their year
3. Extract incidents, campaigns, threat actors
4. Create temporal relationships
5. Link to CVE/CWE/ATT&CK where applicable

---

### Phase 5: IEC 62443 Standards (FIFTH)
**Priority:** MEDIUM
**Agent:** `hierarchical-coordinator` (2 agents in parallel)

#### 5.1 IEC 62443 Part 3
**Agent:** `coder` + `reviewer`
**Directory:** `/Import_to_neo4j/cybersecurity/iec62443-part3/`
**Entity Types:** SecurityControl, Requirement, ZoneConduit, IndustrialControlSystem
**Focus:** Network and system security for industrial automation

#### 5.2 IEC 62443 Part 4
**Agent:** `coder` + `reviewer`
**Directory:** `/Import_to_neo4j/cybersecurity/iec62443-part4/`
**Entity Types:** ComponentRequirement, SecurityLevel, TechnicalRequirement
**Focus:** Component-level security requirements

---

### Phase 6: Threat Modeling (SIXTH)
**Priority:** MEDIUM
**Agent:** `system-architect` + `code-analyzer`
**Directory:** `/Import_to_neo4j/cybersecurity/threat-modeling/`

**Entity Types:**
- ThreatModel, Asset, ThreatAgent, Threat, Vulnerability, Control

**Processing:**
1. Parse threat modeling files
2. Create threat model structures
3. Link threats to CVE/CWE
4. Link controls to mitigations

---

### Phase 7: Adhoc Data Files (SEVENTH)
**Priority:** LOW
**Agent:** `researcher` + `coder`
**Directory:** `/Import_to_neo4j/adhoc/`

**Processing:**
- Discover and categorize all files
- Map to appropriate UCO entity types
- Import with proper namespacing

---

### Phase 8: Documentation (EIGHTH - Optional)
**Priority:** LOW
**Agent:** `api-docs`
**Directory:** `/Import_to_neo4j/claudedocs/`

**Processing:**
- Extract technical documentation entities
- Create documentation nodes with relationships
- Link documentation to technical entities

---

## Swarm Coordination Architecture

### Topology: Hierarchical with Adaptive Specialization

```
┌─────────────────────────────────────┐
│   Master Coordinator (Queen)        │
│   - sparc-coord                     │
│   - Orchestrates all phases         │
│   - Tracks progress                 │
│   - Validates completeness          │
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┐
       │                │
   ┌───▼────┐      ┌───▼────┐
   │ Schema │      │  Data  │
   │ Team   │      │ Teams  │
   └───┬────┘      └───┬────┘
       │               │
       │               ├─► ATT&CK Agent
       │               ├─► CAPEC Agent
       │               ├─► CWE Agent
       │               ├─► STIX Agent
       │               ├─► MISP Agent
       │               ├─► TAXII Agent
       │               ├─► MITRE Agent
       │               ├─► EM3D Agent
       │               ├─► Reports Team (6 agents: 2020-2025)
       │               ├─► IEC Standards Team (2 agents)
       │               ├─► Threat Modeling Agent
       │               └─► Adhoc Agent
       │
   ┌───▼──────────────────┐
   │   Validator Team      │
   │   - Verify counts     │
   │   - Check completeness│
   │   - Generate report   │
   └───────────────────────┘
```

---

## File Inventory and Tracking

### Total Files: 807
**Breakdown:**
- JSON files: 1
- XML files: 6
- TTL/OWL files: ~10
- Documentation files: ~50
- Data files: ~740

### Tracking Mechanism
**Progress File:** `/tmp/uco_import_progress.json`
```json
{
  "total_files": 807,
  "processed_files": 0,
  "failed_files": [],
  "phases": {
    "schema": "pending",
    "standards": "pending",
    "em3d": "pending",
    "reports": "pending",
    "iec62443": "pending",
    "threat_modeling": "pending",
    "adhoc": "pending"
  },
  "entities_created": 0,
  "relationships_created": 0,
  "start_time": null,
  "end_time": null
}
```

---

## Neo4j Schema Preparation

### Entity Type Registration (OpenSPG MySQL)

Based on UCO schema analysis, register these entity types:

```sql
-- Core UCO Entities
INSERT INTO kg_ontology_entity (name, name_zh, entity_category, layer, description, status, with_index, scope, version, version_status, unique_name, original_id)
VALUES
('CybersecurityKB.Attack', '攻击', 'ADVANCED', 'EXTENSION', 'Cyber attacks and intrusion activities', '1', 'TRUE', 'PUBLIC', 1, 'ONLINE', 'CybersecurityKB.Attack', 2000),
('CybersecurityKB.ThreatActor', '威胁行为者', 'ADVANCED', 'EXTENSION', 'Threat actors conducting malicious activities', '1', 'TRUE', 'PUBLIC', 1, 'ONLINE', 'CybersecurityKB.ThreatActor', 2001),
('CybersecurityKB.Campaign', '活动', 'ADVANCED', 'EXTENSION', 'Coordinated sets of attacks', '1', 'TRUE', 'PUBLIC', 1, 'ONLINE', 'CybersecurityKB.Campaign', 2002),
('CybersecurityKB.Incident', '事件', 'ADVANCED', 'EXTENSION', 'Security incidents', '1', 'TRUE', 'PUBLIC', 1, 'ONLINE', 'CybersecurityKB.Incident', 2003),
('CybersecurityKB.Indicator', '指标', 'ADVANCED', 'EXTENSION', 'Security indicators and IoCs', '1', 'TRUE', 'PUBLIC', 1, 'ONLINE', 'CybersecurityKB.Indicator', 2004),
('CybersecurityKB.Malware', '恶意软件', 'ADVANCED', 'EXTENSION', 'Malicious software', '1', 'TRUE', 'PUBLIC', 1, 'ONLINE', 'CybersecurityKB.Malware', 2005),
('CybersecurityKB.Tool', '工具', 'ADVANCED', 'EXTENSION', 'Tools used by threat actors', '1', 'TRUE', 'PUBLIC', 1, 'ONLINE', 'CybersecurityKB.Tool', 2006),
('CybersecurityKB.Exploit', '利用', 'ADVANCED', 'EXTENSION', 'Exploitation techniques', '1', 'TRUE', 'PUBLIC', 1, 'ONLINE', 'CybersecurityKB.Exploit', 2007),
('CybersecurityKB.Observable', '可观察对象', 'ADVANCED', 'EXTENSION', 'Cyber observables', '1', 'TRUE', 'PUBLIC', 1, 'ONLINE', 'CybersecurityKB.Observable', 2008),
('CybersecurityKB.CourseOfAction', '行动方案', 'ADVANCED', 'EXTENSION', 'Defensive measures and responses', '1', 'TRUE', 'PUBLIC', 1, 'ONLINE', 'CybersecurityKB.CourseOfAction', 2009);
```

### Neo4j Constraints and Indexes

```cypher
// Unique constraints
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Attack) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:ThreatActor) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Campaign) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Incident) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Indicator) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Malware) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Tool) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Exploit) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Observable) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:CourseOfAction) REQUIRE n.id IS UNIQUE;

// Namespace indexes
CREATE INDEX IF NOT EXISTS FOR (n:Attack) ON (n.namespace);
CREATE INDEX IF NOT EXISTS FOR (n:ThreatActor) ON (n.namespace);
CREATE INDEX IF NOT EXISTS FOR (n:Campaign) ON (n.namespace);
CREATE INDEX IF NOT EXISTS FOR (n:Incident) ON (n.namespace);

// Temporal indexes
CREATE INDEX IF NOT EXISTS FOR (n:Attack) ON (n.created_date);
CREATE INDEX IF NOT EXISTS FOR (n:Incident) ON (n.discovered_date);
```

---

## Import Validation Checklist

### Pre-Import Validation
- [ ] CVE bulk import complete (~140,000 CVEs)
- [ ] Neo4j database accessible and healthy
- [ ] OpenSPG MySQL database writable
- [ ] All 807 files accessible and readable
- [ ] UCO schema files parsed and validated
- [ ] Swarm coordination initialized

### During Import Validation
- [ ] Progress tracking updating every 100 files
- [ ] Entity counts increasing in Neo4j
- [ ] No duplicate entities created
- [ ] Relationships creating correctly
- [ ] Errors logged and handled
- [ ] Memory usage within acceptable limits

### Post-Import Validation
- [ ] All 807 files processed (zero skipped)
- [ ] Entity counts match expected totals
- [ ] Relationship counts verified
- [ ] OpenSPG knowledge model displays all entity types
- [ ] Chat interface can query all imported data
- [ ] Sample queries execute successfully

---

## Success Criteria

### Completeness
✅ **807/807 files processed** (100%)
✅ **Zero files skipped or failed**
✅ **All entity types registered in OpenSPG**

### Quality
✅ **All entities have namespace: 'CybersecurityKB'**
✅ **All entities have dual labels** (e.g., Attack + CybersecurityKB.Attack)
✅ **All relationships follow UCO schema**
✅ **No orphaned entities** (all have at least one relationship)

### Integration
✅ **CVEs linked to CWEs** (~120,000+ relationships)
✅ **CVEs linked to ATT&CK techniques** (where applicable)
✅ **Threat actors linked to campaigns**
✅ **Campaigns linked to incidents**
✅ **Vulnerabilities linked to exploits**

### Performance
✅ **Import rate: >1,000 entities per minute**
✅ **Total import time: <4 hours**
✅ **Memory usage: <8GB**
✅ **No database crashes or errors**

---

## Execution Command

Once CVE import completes, execute:

```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB/builder

# Initialize swarm with hierarchical topology
python3 execute_uco_systematic_import.py \
  --swarm-topology hierarchical \
  --max-agents 15 \
  --parallel \
  --validate \
  --progress-file /tmp/uco_import_progress.json \
  --log-file /tmp/uco_import.log \
  --yes
```

---

## Monitoring

**Real-time monitoring:**
```bash
# Watch progress
watch -n 10 'cat /tmp/uco_import_progress.json | python3 -m json.tool'

# Monitor Neo4j entity counts
watch -n 30 'docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j "MATCH (n {namespace: \"CybersecurityKB\"}) RETURN labels(n)[0] as entity_type, count(*) as count ORDER BY count DESC LIMIT 20;"'

# Check swarm status
tail -f /tmp/uco_import.log | grep -E "(PHASE|COMPLETE|ERROR|WARNING)"
```

---

**END OF PLAN**

This systematic import plan ensures COMPLETE, CONSISTENT processing of ALL 807 files using UCO schema with swarm coordination for maximum efficiency and reliability.
