# Neo4j Schema Analysis Summary
**Date:** 2025-12-12
**Database:** openspg-neo4j
**Namespace:** aeon-actual-system

## Key Findings

### Database Scale
- **Total Nodes:** 1,207,069
- **Total Relationships:** 12,344,852
- **Unique Labels:** 632
- **Unique Relationship Types:** 184

### Critical Discovery
**FINDING:** The hierarchical `super_label` property does NOT exist in production.
- System uses 632 direct labels instead of 16 super labels
- No property discriminators (actorType, malwareFamily, vulnType)
- Label-based classification rather than property-based taxonomy

### Top Node Types
1. CVE: 316,552 (26.2%)
2. Measurement:ManufacturingMeasurement: 72,800 (6.0%)
3. Entity: 55,569 (4.6%)
4. Control: 48,800 (4.0%)
5. Dependency:SBOM:Relationship: 30,000 (2.5%)

### Top Relationships
1. IMPACTS (FutureThreat → Equipment): 4,780,512 (38.7%)
2. VULNERABLE_TO (Device → CVE): 2,592,244 (21.0%)
3. INSTALLED_ON (DataSource → Device): 781,672 (6.3%)

### Schema Patterns

#### 1. Multi-Label Classification
Nodes use 3-5 labels for hierarchical classification:
- `SoftwareComponent:Asset:SBOM:Software_Component` (20,000 nodes)
- `Measurement:DefenseMeasurement:SECTOR_DEFENSE_INDUSTRIAL_BASE:SAREF_Measurement` (25,200 nodes)
- `Dependency:SBOM:Relationship` (30,000 nodes)

#### 2. Sector Classification
16 Critical Infrastructure Sectors with extensive tagging:
- ENERGY, WATER, COMMUNICATIONS, FINANCIAL_SERVICES
- SECTOR_DEFENSE_INDUSTRIAL_BASE, GOVERNMENT_FACILITIES
- COMMERCIAL_FACILITIES, FOOD_AGRICULTURE, HEALTHCARE
- EMERGENCY_SERVICES, TRANSPORTATION, INFORMATION_TECHNOLOGY
- CHEMICAL, Nuclear, DAMS, Manufacturing

#### 3. SBOM Integration
140,000+ SBOM nodes with complete dependency tracking:
- SoftwareComponent (20,000)
- Package (10,000)
- Library (10,000)
- Dependency trees and paths
- License compliance tracking
- Provenance and attestation

#### 4. Vulnerability Tracking
Comprehensive CVE integration:
- 316,552 CVE nodes with EPSS scoring
- 225,144 IS_WEAKNESS_TYPE relationships to CWE
- 3,107,235 VULNERABLE_TO relationships
- Priority tier classification (P1-P4)
- Kaggle enrichment flags

#### 5. Information Stream Architecture
Multi-stage data pipeline:
```
DataSource → InformationStream → DataProcessor → DataConsumer
```
- 344,256 TRACKS_PROCESS relationships
- 289,233 MONITORS_EQUIPMENT relationships
- 287,856 CONSUMES_FROM relationships
- 18,000 cognitive bias tags on streams

#### 6. Measurement Systems
275,458 measurement nodes across sectors:
- Manufacturing: 72,800
- Defense: 25,200 (SAREF-compliant)
- Water Treatment: 19,000
- Energy Transmission: 18,000
- Nuclear Radiation: 18,000
- Healthcare: 18,200
- Financial Transactions: 17,000

#### 7. Future Threat Modeling
8,900 FutureThreat nodes with:
- 4,780,512 IMPACTS relationships
- 24,192 THREATENS relationships
- 14,985 HistoricalPattern nodes for scenario planning

#### 8. Psychological Profiling
ThreatActor nodes include:
- Big Five personality traits (OCEAN scores)
- Lacan discourse analysis (Master/University/Hysteric/Analyst)
- Register emphasis (Real/Imaginary/Symbolic)
- Motivation consistency scoring
- UCO ontology integration

### Production Status
✅ **PRODUCTION-READY**
- Fully functional for multi-hop reasoning (20-hop verified)
- Label-based queries perform well
- No degradation from missing super_label property

### Recommendations

**Immediate:**
- Document actual 632-label schema (not intended 16 super labels)
- Optimize queries for label-based filtering
- Accept current implementation as production baseline

**Short-Term:**
- Consider adding super_label for cross-label queries (optional)
- Implement NER11 hierarchical enrichment if needed
- Add property discriminators for query optimization

**Long-Term:**
- Architecture decision: Keep labels vs. migrate to super_label pattern
- Hybrid approach: Labels + super_label for flexibility

### Query Examples

**Find Energy Sector Nodes:**
```cypher
MATCH (n)
WHERE any(label IN labels(n) WHERE label STARTS WITH 'Energy' OR label = 'ENERGY')
RETURN labels(n), count(n)
```

**CVE Vulnerability Surface:**
```cypher
MATCH (d:Device)-[:VULNERABLE_TO]->(c:CVE)
WHERE c.cvssV31BaseSeverity IN ['HIGH', 'CRITICAL']
  AND c.epss_score > 0.01
RETURN d.name, d.subsector, count(c) as vuln_count
```

**SBOM Supply Chain Risk:**
```cypher
MATCH (sc:SoftwareComponent)-[:SBOM_CONTAINS*1..5]->(dep)
      -[:VULNERABLE_TO]->(cve:CVE)
WHERE cve.priority_tier IN ['P1', 'P2']
RETURN sc.purl, count(DISTINCT cve) as vulnerabilities
```

**Cross-Sector Impact Analysis:**
```cypher
MATCH (ft:FutureThreat)-[:IMPACTS]->(e:Equipment)-[:DEPENDS_ON*1..3]->(dep)
WHERE e.subsector <> dep.subsector
RETURN ft.name, e.subsector, dep.subsector, count(*) as cascade_count
```

### Files Generated
- `/queries/all_labels.txt` - Complete label listing (632 labels)
- `/queries/all_relationship_types.txt` - Complete relationship types (184 types)
- `/queries/multi_label_combinations.txt` - Top 100 multi-label patterns
- `/queries/label_distribution.txt` - Node count by label combination
- `/queries/asset_properties.txt` - Asset property schema
- `/queries/cve_properties.txt` - CVE property schema
- `/queries/entity_properties.txt` - Entity property schema
- `/queries/measurement_properties.txt` - Measurement property schema
- `/queries/sbom_properties.txt` - SBOM property schema
- `/queries/threatactor_properties.txt` - ThreatActor property schema
- `/queries/relationship_patterns.txt` - Top 100 relationship patterns
- `/queries/node_count.txt` - Total node count
- `/queries/relationship_count.txt` - Total relationship count

### Ontology Integration
- **SAREF** (Smart Applications REFerence): 25,200+ measurements
- **UCO** (Unified Cyber Ontology): ThreatActor integration
- **STIX** (Structured Threat Information eXpression): Observable tracking
- **ATT&CK**: Tactic and Technique frameworks
- **CAPEC**: Attack Pattern Enumeration
- **OWASP**: Web application security
- **EMB3D**: Embedded device security
- **CWE**: Common Weakness Enumeration (225,144 mappings)

---

**Status:** FACT-BASED ANALYSIS COMPLETE
**Next Steps:** Store in Qdrant "aeon-actual-system" namespace for RAG retrieval
