# CAPEC Attack Chain Creation Report

**Date**: 2025-11-07
**Task**: Create CWE→CAPEC→ATT&CK relationships from CAPEC v3.9 catalog
**Status**: ✅ COMPLETE

## Executive Summary

Successfully created complete attack chain infrastructure connecting CVE vulnerabilities through CWE weaknesses, CAPEC attack patterns, and ATT&CK techniques. The system now supports attack path analysis and threat intelligence workflows.

## Data Sources

- **CAPEC Catalog**: v3.9 XML (downloaded from https://capec.mitre.org/data/xml/capec_v3.9.xml)
- **Size**: 3.85 MB
- **Parsing Results**:
  - 1,214 CWE→CAPEC relationships extracted
  - 272 CAPEC→ATT&CK relationships extracted

## Relationships Created

### CWE → CAPEC Relationships
- **Created**: 114 relationships
- **Target**: CWE nodes with `number` property (CVE-connected nodes)
- **Relationship Type**: `ENABLES_ATTACK_PATTERN`
- **Missing CWEs**: 313 (CWE IDs not found in database)
  - Sample missing: CWE-209, CWE-1299, CWE-367, CWE-697, CWE-377
  - Reason: These CWE IDs not present in the database's CVE-connected CWE set

### CAPEC → ATT&CK Relationships
- **Created**: 271 relationships
- **Relationship Type**: `USES_TECHNIQUE`
- **Missing Techniques**: 1 (T1513 - Screen Capture)
- **Coverage**: 30.67% of CAPEC nodes (188 out of 613) now connected to ATT&CK techniques

## Complete Attack Chains

### CVE → CWE → CAPEC → ATT&CK
- **Complete Chains**: **124 chains**
- **CVEs with full attack paths**: 124 distinct vulnerabilities
- **CWEs participating**: 8 weakness types
- **CAPECs involved**: 38 attack patterns
- **ATT&CK Techniques reached**: 51 techniques

## Coverage Metrics

### CWE Coverage
- **Total CWE nodes**: 2,559
- **CWEs with CAPEC relationships**: 448
- **Coverage**: 17.51%

### CAPEC Coverage
- **Total CAPEC nodes**: 613
- **CAPECs with ATT&CK relationships**: 188
- **Coverage**: 30.67%

### Attack Chain Completeness
- **CVE nodes**: ~25,793 (from previous reports)
- **CVEs with complete attack chains**: 124
- **Chain coverage**: ~0.48%
  - Note: Low percentage expected due to:
    1. Many CVEs map to CWEs that don't have CAPEC attack patterns defined
    2. CAPEC catalog focuses on generic attack patterns, not all specific weaknesses
    3. Not all CAPEC patterns have been mapped to ATT&CK techniques

## Technical Implementation

### Data Flow
```
CAPEC v3.9 XML
    ↓
Parse Related_Weaknesses
    ↓
Extract CWE IDs → Convert to integer
    ↓
Match CWE nodes (number property)
    ↓
Create ENABLES_ATTACK_PATTERN relationships
    ↓
Parse Taxonomy_Mappings (ATTACK)
    ↓
Extract Entry_IDs → Add "T" prefix
    ↓
Match AttackTechnique nodes (techniqueId property)
    ↓
Create USES_TECHNIQUE relationships
```

### Property Matching
- **CWE Nodes**: Matched on `number` property (integer)
  - Example: CWE-79 → `{number: 79}`
- **CAPEC Nodes**: Matched on `capecId` property (string)
  - Example: CAPEC-1 → `{capecId: "CAPEC-1"}`
- **ATT&CK Nodes**: Matched on `techniqueId` property (string with "T" prefix)
  - Example: T1055.011 → `{techniqueId: "T1055.011"}`

### Challenges Resolved

1. **CWE Node Duplication**: Database contains two sets of CWE nodes
   - Set 1: `cwe_id` property (string, e.g., "1", "10")
   - Set 2: `number` property (integer, e.g., 79, 352) ← CVE-connected nodes
   - Solution: Match on `number` property for CVE→CWE connectivity

2. **ATT&CK Technique ID Format**: CAPEC XML omits "T" prefix
   - Example: XML has "1055.011", database has "T1055.011"
   - Solution: Auto-prepend "T" prefix during parsing

3. **CVE→CWE Relationship Type**: Not `HAS_WEAKNESS` as expected
   - Actual: `IS_WEAKNESS_TYPE`
   - Solution: Updated chain analysis queries

## Example Attack Chains

Sample complete chains available in the database:

```cypher
// Query complete chains
MATCH path = (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
             -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
             -[:USES_TECHNIQUE]->(tech:AttackTechnique)
RETURN cve.id, cwe.number, capec.capecId, tech.techniqueId
LIMIT 5
```

Expected results show connections like:
- CVE-XXXX → CWE-79 (XSS) → CAPEC-18 (XSS) → T1189 (Drive-by Compromise)
- CVE-YYYY → CWE-89 (SQL Injection) → CAPEC-66 (SQL Injection) → T1190 (Exploit Public-Facing Application)

## Attack Path Analysis Capabilities

With these relationships in place, the system now supports:

1. **Vulnerability-to-Technique Mapping**: Given a CVE, find all possible ATT&CK techniques attackers could use
2. **Weakness-to-Attack Pattern**: Identify attack patterns that exploit specific weakness types
3. **Reverse Analysis**: Find vulnerabilities that enable specific ATT&CK techniques
4. **Chain Length Analysis**: Calculate attack chain lengths and complexity
5. **Gap Analysis**: Identify CWEs without attack patterns or techniques

## Next Steps & Recommendations

### Immediate Improvements
1. **Expand CWE Coverage**: Import additional CWE definitions to increase overlap with CAPEC
2. **Verify Chain Quality**: Manual review of sample chains for accuracy
3. **Add Missing ATT&CK Technique**: T1513 (Screen Capture) should be added to database

### Future Enhancements
1. **Mitigation Mapping**: Link CAPEC mitigations to defensive controls
2. **Severity Propagation**: Propagate CVSS scores through attack chains
3. **Temporal Analysis**: Track evolution of attack chains over time
4. **Attack Graph Construction**: Build exploitability graphs using these chains
5. **Threat Modeling Integration**: Use chains for automated threat identification

## Files Generated

- **Script**: `/scripts/create_capec_relationships.py`
- **Downloaded Data**: `/capec_v3.9.xml` (3.85 MB)
- **Report**: `/docs/CAPEC_ATTACK_CHAIN_REPORT.md` (this file)

## Validation Queries

### Verify Relationships
```cypher
// Count all relationship types
MATCH (cwe:CWE)-[r:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
RETURN count(r) as cwe_capec_count

MATCH (capec:CAPEC)-[r:USES_TECHNIQUE]->(tech:AttackTechnique)
RETURN count(r) as capec_attack_count

// Find complete chains
MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
      -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
      -[:USES_TECHNIQUE]->(tech:AttackTechnique)
RETURN count(DISTINCT cve) as complete_chains
```

### Example Chain Queries
```cypher
// Most common techniques in chains
MATCH (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
      -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
      -[:USES_TECHNIQUE]->(tech:AttackTechnique)
RETURN tech.techniqueId, tech.name, count(DISTINCT cve) as cve_count
ORDER BY cve_count DESC
LIMIT 10

// CWEs with most attack patterns
MATCH (cwe:CWE)-[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
RETURN cwe.number, cwe.name, count(capec) as attack_pattern_count
ORDER BY attack_pattern_count DESC
LIMIT 10
```

## Conclusion

Successfully established complete attack chain infrastructure with 124 end-to-end CVE→CWE→CAPEC→ATT&CK paths. The system is now ready for:
- Attack path analysis
- Threat intelligence workflows
- Automated threat modeling
- Security assessment and prioritization

**Coverage Summary**:
- ✅ 114 CWE→CAPEC relationships
- ✅ 271 CAPEC→ATT&CK relationships
- ✅ 124 complete attack chains
- ✅ 51 unique ATT&CK techniques accessible via CVEs
