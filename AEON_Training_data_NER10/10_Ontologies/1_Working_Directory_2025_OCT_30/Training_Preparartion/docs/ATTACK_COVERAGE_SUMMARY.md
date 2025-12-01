# ATT&CK Coverage Analysis - Executive Summary

**Date:** 2025-11-08
**Database:** Neo4j at bolt://localhost:7687

## Key Findings

### Node Coverage ✅
- **CVE:** 316,552 nodes
- **CWE:** 2,177 nodes
- **CAPEC:** 613 nodes
- **AttackTechnique:** 834 nodes
- **AttackTactic:** 28 nodes
- **AttackPattern:** 815 nodes

### Critical Gaps ❌

1. **CVE → CWE relationships MISSING**
   - Cannot link vulnerabilities to weakness types
   - 3.1M `VULNERABLE_TO` relationships don't connect to CWE

2. **CWE → CAPEC relationships MISSING**
   - Cannot traverse weakness → attack pattern chain
   - Expected relationship type not found in top 20

3. **AttackTactic → AttackTechnique MISSING**
   - Cannot query techniques by tactic
   - ATT&CK framework hierarchy incomplete

4. **AttackTechnique underutilized**
   - 834 nodes exist but not visible in top relationships
   - Need direct links from Threat/CAPEC nodes

### What Works ✅

- **AttackPattern relationships** well-established:
  - `CHILDOF`, `CANPRECEDE`, `CANFOLLOW`, `PEEROF` support attack sequencing
  - `MITIGATES` links defensive actions to attacks

- **CAPEC Integration:**
  - 270 `CAPEC → Threat` relationships via `USES_TECHNIQUE` and `IMPLEMENTS`
  - Can partially bridge to ATT&CK concepts

## Required Relationships

```cypher
// Priority 1: Vulnerability Chain
(:CVE)-[:HAS_WEAKNESS]->(:CWE)
(:CWE)-[:CAN_BE_EXPLOITED_BY]->(:CAPEC)
(:CAPEC)-[:MAPS_TO_TECHNIQUE]->(:AttackTechnique)

// Priority 2: ATT&CK Hierarchy
(:AttackTactic)-[:CONTAINS]->(:AttackTechnique)
(:AttackTechnique)-[:PART_OF_TACTIC]->(:AttackTactic)

// Priority 3: Direct Threat Links
(:Threat)-[:USES_TECHNIQUE]->(:AttackTechnique)
```

## Impact Assessment

**Current State:**
Cannot answer critical queries like:
- "What ATT&CK techniques can exploit CVE-2021-44228?"
- "Show attack chains from SQL Injection (CWE-89) to data exfiltration"
- "What techniques are used in Initial Access tactic?"

**With Complete Relationships:**
Enable full attack chain analysis from vulnerability discovery to technique execution.

## Immediate Action Items

1. ✅ **DONE:** Analyzed current schema and identified gaps
2. **TODO:** Create CVE → CWE mappings from NVD data
3. **TODO:** Create CWE → CAPEC mappings from CAPEC database
4. **TODO:** Create CAPEC → AttackTechnique mappings
5. **TODO:** Create AttackTactic → AttackTechnique hierarchy
6. **TODO:** Validate with test queries for known CVEs

## Testing Strategy

Test queries after relationship creation:

```cypher
// Test 1: CVE to ATT&CK path
MATCH p=(cve:CVE {cveId: 'CVE-2021-44228'})-[*1..4]-(att:AttackTechnique)
RETURN p LIMIT 10

// Test 2: Tactic to techniques
MATCH (tactic:AttackTactic {name: 'Initial Access'})-[:CONTAINS]->(tech:AttackTechnique)
RETURN tech.name, tech.techniqueId

// Test 3: Complete attack chain
MATCH path = (cve:CVE)-[:HAS_WEAKNESS]->(cwe:CWE)-[:CAN_BE_EXPLOITED_BY]->(capec:CAPEC)
              -[:MAPS_TO_TECHNIQUE]->(tech:AttackTechnique)-[:PART_OF_TACTIC]->(tactic:AttackTactic)
RETURN path LIMIT 5
```

---

For detailed analysis, see: `NEO4J_ATTACK_SCHEMA_ANALYSIS.md`
