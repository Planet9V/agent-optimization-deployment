# Neo4j ATT&CK Schema Analysis Report

**Generated:** 2025-11-08 09:12:44
**Database:** bolt://localhost:7687

---

## 1. Node Coverage

| Label | Count |
|-------|-------|
| CVE | 316,552 |
| CWE | 2,177 |
| AttackTechnique | 834 |
| AttackPattern | 815 |
| CAPEC | 613 |
| AttackTactic | 28 |

## 2. Top Relationship Types

| Relationship | Count |
|--------------|-------|
| VULNERABLE_TO | 3,107,235 |
| HAS_MEASUREMENT | 33,000 |
| HAS_ENERGY_PROPERTY | 30,000 |
| RELATED_TO | 20,901 |
| GENERATES_MEASUREMENT | 18,000 |
| CONTAINS_ENTITY | 14,645 |
| INSTALLED_AT_SUBSTATION | 10,000 |
| CONTROLLED_BY_EMS | 10,000 |
| INDICATES | 8,000 |
| HAS_PROPERTY | 6,750 |
| COMPLIES_WITH_NERC_CIP | 5,000 |
| EXTENDS_SAREF_DEVICE | 4,500 |
| CONTROLS | 3,003 |
| HAS_COMMAND | 3,000 |
| CONTAINS | 2,500 |

## 3. ATT&CK Relationships

| From | Relationship | To | Count |
|------|--------------|-----|-------|
| Threat | RELATED_TO | Threat | 14,853 |
| DetectionSignature | DETECTS | AttackPattern | 1,998 |
| AttackPattern | PART_OF_CAMPAIGN | Threat | 1,872 |
| AttackPattern | IMPLEMENTS | TTP | 1,599 |
| CourseOfAction | RELATED_TO | Threat | 1,421 |
| Threat | USES_ATTACK_PATTERN | AttackPattern | 976 |
| Mitigation | MITIGATES | AttackPattern | 911 |
| Tool | RELATED_TO | Threat | 798 |
| AttackPattern | CHILDOF | AttackPattern | 533 |
| AttackPattern | MAPS_TO_ATTACK | Threat | 270 |
| CAPEC | USES_TECHNIQUE | Threat | 270 |
| CAPEC | IMPLEMENTS | Threat | 270 |
| AttackPattern | CANPRECEDE | AttackPattern | 162 |
| AttackPattern | PEEROF | AttackPattern | 19 |
| Threat | MITIGATED_BY | CourseOfAction | 13 |
| AttackPattern | CANFOLLOW | AttackPattern | 10 |
| Threat | IMPLEMENTS | AttackTactic | 10 |
| Threat | REQUIRES_DATA_SOURCE | uco_core_UcoObject | 6 |
| Threat | LEADS_TO | Threat | 4 |
| AttackPattern | CANALSOBE | AttackPattern | 3 |

## 4. Assessment

### Current State:

- ✅ CVE nodes: 316,552
- ✅ CWE nodes: 2,177
- ✅ CAPEC nodes: 613
- ✅ AttackTechnique nodes: 834
- ✅ AttackTactic nodes: 28
- ✅ ATT&CK relationships exist

### Relationship Analysis:

**Strong Coverage:**
- ✅ **AttackPattern relationships** are well-established:
  - `CHILDOF`, `CANPRECEDE`, `CANFOLLOW`, `PEEROF` relationships support attack chain modeling
  - `USES_ATTACK_PATTERN`, `MAPS_TO_ATTACK` link threats to patterns
  - `MITIGATES` relationships connect mitigations to attack patterns

- ✅ **CAPEC Integration:**
  - 270 `CAPEC → USES_TECHNIQUE → Threat` relationships
  - 270 `CAPEC → IMPLEMENTS → Threat` relationships
  - CAPEC nodes can bridge to ATT&CK concepts via Threat nodes

**Critical Gaps Identified:**

1. **❌ Direct CVE → ATT&CK Links Missing:**
   - CVEs have 3.1M `VULNERABLE_TO` relationships but no direct path to AttackTechnique nodes
   - Current path would require: CVE → [unknown] → CWE → CAPEC → Threat → AttackTechnique
   - **Impact:** Cannot directly answer "What ATT&CK techniques can exploit CVE-XXXX-XXXXX?"

2. **❌ CWE → CAPEC Connection Unclear:**
   - CWE nodes exist (2,177) but relationship to CAPEC/ATT&CK not visible in top relationships
   - Expected: `CWE → RELATED_TO → CAPEC` or `CWE → CAN_BE_EXPLOITED_BY → CAPEC`
   - **Impact:** Cannot traverse vulnerability weakness → attack pattern chain

3. **❌ AttackTactic → AttackTechnique Hierarchy Missing:**
   - AttackTactic nodes exist (28) but no visible relationships to AttackTechnique nodes
   - Expected: `AttackTactic → CONTAINS → AttackTechnique` or `AttackTechnique → PART_OF → AttackTactic`
   - **Impact:** Cannot query "Show all techniques for Initial Access tactic"

4. **⚠️ AttackTechnique Underutilized:**
   - 834 AttackTechnique nodes but no relationships visible in top 20
   - Threat nodes (via AttackPattern) are more connected than AttackTechnique
   - **Recommendation:** Establish direct links: `Threat → USES_TECHNIQUE → AttackTechnique`

### Required for Complete Attack Chains:

1. **CVE → CWE → CAPEC → ATT&CK** relationship chain:
   - ✅ CVE nodes exist
   - ✅ CWE nodes exist
   - ✅ CAPEC nodes exist
   - ❌ **MISSING:** `CVE → CWE` relationships
   - ❌ **MISSING:** `CWE → CAPEC` relationships
   - ✅ `CAPEC → Threat` exists (270 links)
   - ❌ **MISSING:** `Threat → AttackTechnique` direct links

2. **ATT&CK Internal Hierarchy:**
   - ✅ AttackPattern has `CHILDOF`, `CANPRECEDE`, `CANFOLLOW`
   - ❌ **MISSING:** `AttackTactic → AttackTechnique` relationships
   - ❌ **MISSING:** `AttackTechnique → Sub-technique` relationships (if sub-techniques exist)

3. **Bidirectional Traversal:**
   - ✅ Many relationships appear bidirectional (RELATED_TO)
   - ⚠️ Need to verify inverse relationships exist for attack chain queries

4. **Metadata Properties:**
   - ⚠️ Unknown - need to inspect relationship properties for:
     - Confidence scores
     - Data source attribution
     - Timestamps/versions
     - STIX properties

### Missing Relationship Types Needed:

```cypher
// CVE to CWE
(:CVE)-[:HAS_WEAKNESS]->(:CWE)
(:CVE)-[:CATEGORIZED_AS]->(:CWE)

// CWE to CAPEC
(:CWE)-[:CAN_BE_EXPLOITED_BY]->(:CAPEC)
(:CWE)-[:EXPLOITED_USING]->(:CAPEC)

// CAPEC to ATT&CK Technique (currently via Threat)
(:CAPEC)-[:MAPS_TO_TECHNIQUE]->(:AttackTechnique)

// ATT&CK Hierarchy
(:AttackTactic)-[:CONTAINS]->(:AttackTechnique)
(:AttackTechnique)-[:PART_OF_TACTIC]->(:AttackTactic)
(:AttackTechnique)-[:HAS_SUBTECHNIQUE]->(:AttackTechnique)

// Threat to ATT&CK
(:Threat)-[:USES_TECHNIQUE]->(:AttackTechnique)
```

### Next Steps:

**Priority 1 - Critical Path Establishment:**
1. Create `CVE → CWE` relationships using CVE weakness data
2. Create `CWE → CAPEC` relationships using CAPEC mappings
3. Create `CAPEC → AttackTechnique` direct mappings

**Priority 2 - ATT&CK Hierarchy:**
4. Create `AttackTactic → AttackTechnique` relationships
5. Verify AttackTechnique coverage matches MITRE ATT&CK framework

**Priority 3 - Validation:**
6. Test end-to-end path: `MATCH p=(cve:CVE)-[*1..5]-(att:AttackTechnique) RETURN p LIMIT 10`
7. Verify path exists for sample CVEs: CVE-2021-44228 (Log4Shell), CVE-2017-0144 (EternalBlue)

**Priority 4 - Performance:**
8. Create indexes: `CREATE INDEX FOR (n:AttackTechnique) ON (n.techniqueId)`
9. Create indexes: `CREATE INDEX FOR (n:CVE) ON (n.cveId)`
10. Add relationship indexes for common traversal patterns

**Priority 5 - Metadata:**
11. Add confidence scores to inferred relationships
12. Add provenance metadata (data sources, timestamps)
13. Add STIX compliance properties where applicable

---

*Analysis completed: 2025-11-08 09:12:44*
