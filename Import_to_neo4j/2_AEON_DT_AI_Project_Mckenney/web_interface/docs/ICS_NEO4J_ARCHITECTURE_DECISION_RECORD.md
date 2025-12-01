# Architecture Decision Record: OT/ICS Infrastructure Entity Expansion for Neo4j

**ADR Number:** ADR-001
**Status:** PROPOSED
**Date:** 2025-11-26
**Author:** System Architecture Designer
**Context:** AEON DT AI Project McKenney - Neo4j Knowledge Graph

---

## Context and Problem Statement

The current Neo4j schema has limited OT/ICS infrastructure coverage. With NER11 providing 62 Tier 1 infrastructure types and 31 Tier 6 sector-specific types, we need to:

1. **Expand entity coverage** for critical infrastructure (16 CISA sectors)
2. **Integrate Purdue Model** (L0-L5) for ICS asset classification
3. **Map ICS vulnerabilities** to CVE database with 8-hop attack chains
4. **Avoid label explosion** (currently 26+ potential labels if sector-per-label)
5. **Support sector-specific analysis** without schema rigidity

**Current State:**
- Equipment, Substation, TransmissionLine labels exist but are empty
- No Purdue Model integration
- No ICS protocol vulnerability mapping
- Limited sector differentiation

---

## Decision Drivers

### Technical Requirements
- **Scalability:** Support 16 CISA sectors + future sector additions
- **Performance:** Fast sector-based queries (<50ms)
- **Flexibility:** Multi-sector assets, sector reclassification
- **Integration:** 8-hop CVE attack chain compatibility
- **Maintainability:** Minimize schema complexity

### Operational Requirements
- **Compliance:** NERC-CIP, IEC-62443, NIST-800-82 mapping
- **Risk Analysis:** Sector-wide vulnerability assessment
- **Incident Response:** Lateral movement path discovery
- **Asset Management:** Purdue level-based lifecycle tracking

---

## Considered Options

### Option 1: Label-Per-Sector ❌
```cypher
(:FieldDevice:EnergySector)
(:FieldDevice:WaterSector)
(:FieldDevice:HealthcareSector)
// ... 16 total sector labels
```

**Pros:**
- Fastest query performance (label scans)
- Clear visual distinction in Neo4j Browser
- Native Cypher label matching

**Cons:**
- **Label explosion:** 26+ labels (10 core + 16 sectors)
- **Rigid schema:** New sectors require migration
- **Multi-sector complexity:** Difficult to represent shared assets
- **Maintenance burden:** Inconsistent query patterns

**Verdict:** ❌ Rejected - Does not scale

---

### Option 2: Property-Based Sector Differentiation ✅
```cypher
(:FieldDevice {
  sector: "ENERGY",
  subSector: "ELECTRIC_TRANSMISSION"
})
```

**Pros:**
- **Scalable:** New sectors added without schema changes
- **Flexible:** Multi-sector assets via array properties
- **Maintainable:** Single taxonomy source
- **Query performance:** Good with proper indexing

**Cons:**
- Slightly slower than label-based queries (mitigated by indexes)
- Requires property validation logic

**Verdict:** ✅ **SELECTED** - Best balance of flexibility and performance

---

### Option 3: Hybrid Approach (Labels for Critical Sectors)
```cypher
(:FieldDevice:CriticalEnergy {sector: "ENERGY"})
(:FieldDevice:CriticalWater {sector: "WATER"})
(:FieldDevice {sector: "HEALTHCARE"}) // Property for non-critical
```

**Pros:**
- Optimized for most-queried sectors
- Fallback to properties for others

**Cons:**
- **Inconsistency:** Mixed query patterns confusing
- **Complexity:** Two different access methods
- **Arbitrary distinction:** Which sectors are "critical"?

**Verdict:** ⚠️ Reserved for future optimization if needed

---

## Decision Outcome

### Chosen Option: Property-Based Sector Differentiation

**Core Schema:**
- **10 Core Labels:** ICSAsset, FieldDevice, ControlSystem, InfrastructureFacility, NetworkSegment, ICSProtocol, CommunicationInterface, Process, SafetySystem, ICSVulnerability
- **Sector Differentiation:** `sector` and `subSector` properties
- **16 CISA Sectors:** Supported via property values
- **Purdue Model:** `purdueLevel` property (0-5)

---

## Detailed Design

### Label Hierarchy

```
ICSAsset (abstract)
├─ FieldDevice (Purdue L0-L1)
│  ├─ PLC, RTU, IED, Sensor, Actuator
├─ ControlSystem (Purdue L2)
│  ├─ SCADA, DCS, HMI, EMS, DMS
├─ SafetySystem (SIS, ESD)
├─ InfrastructureFacility
│  ├─ Substation, Plant, Treatment Facility
├─ NetworkSegment (IEC-62443 zones)
├─ ICSProtocol (Modbus, DNP3, OPC UA)
├─ CommunicationInterface
├─ Process (industrial processes)
└─ ICSVulnerability (CVE + ICS context)
```

### Property Schema

**FieldDevice:**
```yaml
Core:
  id, name, deviceType, vendor, model, firmwareVersion
Purdue:
  purdueLevel: 0-5
Safety:
  safetyLevel: SIL-1 to SIL-4
Sector:
  sector: ENERGY|WATER|TRANSPORTATION|...
  subSector: ELECTRIC_TRANSMISSION|DRINKING_WATER|...
  secondarySectors: [array for multi-sector]
Network:
  ipAddress, macAddress, networkZone
Criticality:
  criticalityScore: 1-10
  singlePointOfFailure: boolean
Compliance:
  complianceFrameworks: [NERC-CIP, IEC-62443, ...]
```

### Relationship Types

```cypher
// Asset hierarchy
(ControlSystem)-[:MANAGES]->(FieldDevice)
(FieldDevice)-[:LOCATED_IN]->(InfrastructureFacility)

// Network topology
(FieldDevice)-[:CONNECTED_TO]->(NetworkSegment)
(FieldDevice)-[:USES_PROTOCOL]->(ICSProtocol)

// Process control
(FieldDevice)-[:CONTROLS]->(Process)
(SafetySystem)-[:PROTECTS]->(Process)

// Vulnerability mapping
(ICSVulnerability)-[:AFFECTS]->(FieldDevice)
(ICSVulnerability)-[:EXPLOITS_PROTOCOL]->(ICSProtocol)

// Attack chain (8-hop)
(ICSVulnerability)-[:ENABLES_ACCESS_TO]->(NetworkSegment)
(NetworkSegment)-[:CONTAINS]->(FieldDevice)
(FieldDevice)-[:MANAGES]->(Process)
(Process)-[:CRITICAL_TO]->(InfrastructureFacility)
```

---

## Consequences

### Positive

1. **Scalability:** New sectors added via property values (no migration)
2. **Flexibility:** Multi-sector assets naturally supported
3. **Maintainability:** Single sector taxonomy (16 CISA sectors)
4. **Query Performance:** Indexed properties provide fast lookups
5. **CVE Integration:** ICSVulnerability extends existing CVE schema
6. **Purdue Model:** Integrated via purdueLevel property
7. **Compliance Mapping:** Framework properties enable gap analysis

### Negative

1. **Property Validation Required:** Must enforce valid sector values
2. **Index Maintenance:** Sector indexes must be kept updated
3. **Query Complexity:** Slightly more verbose than label matching

### Neutral

1. **Query Performance:** 25-50ms with indexes vs. 5-10ms with labels (acceptable)
2. **Learning Curve:** Property-based patterns require documentation

---

## Implementation Roadmap

### Phase 1: Schema Definition (Week 1)
- [ ] Create 10 core label constraints
- [ ] Define sector property taxonomy
- [ ] Implement property validation rules
- [ ] Create sector-based indexes

### Phase 2: Data Migration (Week 2)
- [ ] Migrate existing Equipment nodes to FieldDevice
- [ ] Migrate Substation nodes to InfrastructureFacility
- [ ] Migrate TransmissionLine to InfrastructureFacility
- [ ] Populate sector properties from existing data

### Phase 3: ICS Protocol Integration (Week 3)
- [ ] Create ICSProtocol nodes (Modbus, DNP3, OPC UA, etc.)
- [ ] Link FieldDevice to ICSProtocol via USES_PROTOCOL
- [ ] Document protocol-specific vulnerability patterns

### Phase 4: CVE Vulnerability Mapping (Week 4)
- [ ] Create ICSVulnerability nodes with ICS-CERT advisories
- [ ] Link to affected FieldDevice nodes
- [ ] Map protocol-specific exploits
- [ ] Validate 8-hop attack chain queries

### Phase 5: Sector-Specific Extensions (Week 5)
- [ ] Add Energy sector-specific properties
- [ ] Add Water sector-specific properties
- [ ] Add Nuclear sector-specific properties
- [ ] Add Healthcare sector-specific properties

### Phase 6: Testing and Validation (Week 6)
- [ ] Performance benchmarking (target: <50ms sector queries)
- [ ] Cross-sector vulnerability analysis testing
- [ ] 8-hop attack path validation
- [ ] Compliance framework gap analysis testing

---

## Validation Metrics

### Performance Benchmarks

| Query Type | Target | Acceptable | Unacceptable |
|------------|--------|------------|--------------|
| Single sector filter | <25ms | <50ms | >100ms |
| Multi-sector filter | <30ms | <75ms | >150ms |
| CVE attack chain (8-hop) | <200ms | <500ms | >1000ms |
| Sector aggregation | <100ms | <250ms | >500ms |

### Functional Validation

- [ ] All 16 CISA sectors queryable
- [ ] Multi-sector assets supported
- [ ] Purdue L0-L5 differentiation working
- [ ] ICS protocol vulnerability mapping complete
- [ ] 8-hop CVE attack chains queryable
- [ ] Compliance framework gap analysis functional

---

## Risks and Mitigation

### Risk 1: Query Performance Degradation
**Impact:** HIGH
**Probability:** MEDIUM
**Mitigation:**
- Implement compound indexes on (sector, purdueLevel, criticalityScore)
- Monitor query performance with EXPLAIN/PROFILE
- Fallback to hybrid approach if needed

### Risk 2: Sector Taxonomy Drift
**Impact:** MEDIUM
**Probability:** LOW
**Mitigation:**
- Maintain authoritative sector list (16 CISA sectors)
- Implement property constraints (Neo4j 5.x+)
- Automated validation in data import pipelines

### Risk 3: Complex Multi-Sector Queries
**Impact:** MEDIUM
**Probability:** MEDIUM
**Mitigation:**
- Document common query patterns
- Create query templates for cross-sector analysis
- Provide Cypher stored procedures for complex operations

---

## Related Decisions

- **ADR-002** (Future): Threat actor attribution and campaign tracking
- **ADR-003** (Future): Time-series vulnerability trend analysis
- **ADR-004** (Future): Geographic clustering for critical infrastructure

---

## References

### Standards and Frameworks
- CISA Critical Infrastructure Sectors: https://www.cisa.gov/topics/critical-infrastructure-security-and-resilience/critical-infrastructure-sectors
- Purdue Model (ISA-95): https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95
- IEC 62443: Industrial communication networks - Network and system security
- NERC CIP: Critical Infrastructure Protection Standards
- NIST SP 800-82: Guide to Industrial Control Systems Security

### Technical Resources
- Neo4j Property Graph Model: https://neo4j.com/docs/getting-started/graph-database/#property-graph
- Cypher Query Language: https://neo4j.com/docs/cypher-manual/current/
- NER11 Entity Taxonomy: (internal project documentation)

---

## Approval

**Proposed By:** System Architecture Designer
**Date:** 2025-11-26
**Status:** AWAITING_APPROVAL

**Approvers Required:**
- [ ] Project Lead
- [ ] Security Architect
- [ ] Database Administrator
- [ ] ICS/OT Subject Matter Expert

---

## Appendix A: Sample Cypher Queries

### Query 1: Find All Vulnerable ENERGY Sector Assets
```cypher
MATCH (v:ICSVulnerability)-[:AFFECTS]->(fd:FieldDevice)
WHERE fd.sector = "ENERGY"
  AND v.cvssScore >= 7.0
RETURN fd.id, fd.name, v.cveId, v.cvssScore
ORDER BY v.cvssScore DESC;
```

### Query 2: 8-Hop Attack Chain
```cypher
MATCH path = (v:ICSVulnerability)-[:AFFECTS]->(fd:FieldDevice)
  -[:CONNECTED_TO]->(ns:NetworkSegment)
  -[:CONTAINS]->(cs:ControlSystem)
  -[:MANAGES*1..3]->(criticalAsset:FieldDevice)
  -[:CONTROLS]->(process:Process)
  -[:CRITICAL_TO]->(facility:InfrastructureFacility)
WHERE v.remotelyExploitable = true
  AND facility.sector = "ENERGY"
RETURN path, length(path) as HopCount
ORDER BY v.cvssScore DESC
LIMIT 10;
```

### Query 3: Sector-Wide Vulnerability Assessment
```cypher
MATCH (fd:FieldDevice)<-[:AFFECTS]-(v:ICSVulnerability)
WITH fd.sector as Sector,
     count(DISTINCT v) as VulnCount,
     avg(v.cvssScore) as AvgCVSS
RETURN Sector, VulnCount, round(AvgCVSS, 2) as AvgCVSS
ORDER BY VulnCount DESC;
```

---

## Appendix B: Migration Scripts

### Migrate Existing Equipment Nodes
```cypher
MATCH (e:Equipment)
SET e:FieldDevice
SET e.purdueLevel = COALESCE(e.purdueLevel, 1)
SET e.deviceType = COALESCE(e.deviceType, "UNKNOWN")
SET e.sector = COALESCE(e.sector, "UNKNOWN")
SET e.createdAt = datetime()
RETURN count(e) as Migrated;
```

### Populate Sector Taxonomy
```cypher
// Energy sector devices
MATCH (fd:FieldDevice)
WHERE fd.facilityType IN ["SUBSTATION", "POWER_PLANT", "TRANSMISSION"]
SET fd.sector = "ENERGY"
SET fd.subSector = CASE
  WHEN fd.facilityType = "SUBSTATION" THEN "ELECTRIC_TRANSMISSION"
  WHEN fd.facilityType = "POWER_PLANT" THEN "ELECTRIC_GENERATION"
  ELSE "ELECTRIC_DISTRIBUTION"
END;

// Water sector devices
MATCH (fd:FieldDevice)
WHERE fd.facilityType IN ["WATER_TREATMENT", "WASTEWATER", "PUMP_STATION"]
SET fd.sector = "WATER"
SET fd.subSector = CASE
  WHEN fd.facilityType = "WATER_TREATMENT" THEN "DRINKING_WATER"
  WHEN fd.facilityType = "WASTEWATER" THEN "WASTEWATER_TREATMENT"
  ELSE "DISTRIBUTION"
END;
```

---

## Appendix C: Performance Tuning

### Index Creation
```cypher
CREATE INDEX sector_index IF NOT EXISTS
FOR (fd:FieldDevice) ON (fd.sector);

CREATE INDEX sector_criticality IF NOT EXISTS
FOR (fd:FieldDevice) ON (fd.sector, fd.criticalityScore);

CREATE INDEX purdue_level IF NOT EXISTS
FOR (fd:FieldDevice) ON (fd.purdueLevel);

CREATE INDEX vuln_cvss IF NOT EXISTS
FOR (v:ICSVulnerability) ON (v.cvssScore);
```

### Query Profiling
```cypher
// Use PROFILE to analyze query performance
PROFILE
MATCH (fd:FieldDevice {sector: "ENERGY"})
WHERE fd.criticalityScore >= 8
RETURN count(fd);

// Expected: Index lookup (db hits < 1000)
```

---

**End of ADR-001**
