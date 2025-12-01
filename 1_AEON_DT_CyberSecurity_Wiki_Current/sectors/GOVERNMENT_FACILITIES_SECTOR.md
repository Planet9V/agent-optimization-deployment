# Government Facilities Sector

**Sector Code**: GOVERNMENT_FACILITIES
**Node Count**: 27,000
**Status**: ✅ Operational
**Last Updated**: 2024-11-22

[← Back to Main Index](../00_MAIN_INDEX.md) | [→ Next: Nuclear Sector](NUCLEAR_SECTOR.md)

---

## 📊 Sector Overview

The Government Facilities Sector includes a wide variety of buildings owned or leased by federal, state, local, and tribal governments. This sector includes general-use office buildings, special-use military installations, embassies, courthouses, national laboratories, and structures for essential functions.

### Key Statistics
- **Total Nodes**: 27,000
- **Federal Buildings**: 9,000+ facilities
- **State/Local Facilities**: 12,000+ buildings
- **Equipment Systems**: 6,000+ critical systems
- **Security Systems**: 8,000+ protective measures
- **Geographic Coverage**: All 50 states + territories

---

## 🏗️ Node Types Distribution

```cypher
// Get Government Facilities sector node distribution
MATCH (n)
WHERE n.sector = 'GOVERNMENT_FACILITIES'
RETURN labels(n) as NodeTypes, count(*) as Count
ORDER BY Count DESC;
```

### Node Distribution
- **Facility**: 12,000 nodes (buildings, complexes, campuses)
- **Equipment**: 6,000 nodes (HVAC, security, utilities)
- **Device**: 5,000 nodes (cameras, sensors, access controls)
- **Property**: 2,000 nodes (ownership, classifications)
- **Measurement**: 2,000 nodes (occupancy, energy, security metrics)

---

## 🏭 Subsectors

### Federal Buildings (35%)
- Executive office buildings
- Congressional facilities
- Federal courthouses
- Agency headquarters
- National monuments

### State & Local (30%)
- State capitols
- City halls
- County buildings
- Municipal facilities
- Public safety buildings

### Education & Research (20%)
- National laboratories
- Research facilities
- Federal training centers
- Military academies
- Government universities

### Special Use (15%)
- Embassies and consulates
- Border crossings
- Customs facilities
- Immigration centers
- Detention facilities

---

## 🔧 Equipment Types

### Critical Equipment Categories
```cypher
// Get Government Facilities sector equipment types
MATCH (e:Equipment)
WHERE e.sector = 'GOVERNMENT_FACILITIES'
RETURN e.equipmentType as Type, count(*) as Count
ORDER BY Count DESC
LIMIT 20;
```

### Primary Equipment Types
1. **Security Systems** (2,000 units)
   - Access control systems
   - Intrusion detection
   - Video surveillance
   - Screening equipment
   - Tags: `EQUIP_TYPE_SECURITY`, `OPS_CRITICALITY_CRITICAL`

2. **HVAC Systems** (1,500 units)
   - Air handling units
   - Chillers
   - Boilers
   - Control systems
   - Tags: `EQUIP_TYPE_HVAC`, `FUNCTION_CLIMATE_CONTROL`

3. **Emergency Systems** (1,000 units)
   - Fire alarms
   - Sprinkler systems
   - Emergency lighting
   - Mass notification
   - Tags: `EQUIP_TYPE_EMERGENCY`, `SAFETY_CRITICAL`

4. **Power Systems** (800 units)
   - Backup generators
   - UPS systems
   - Transfer switches
   - Power distribution
   - Tags: `EQUIP_TYPE_POWER`, `FUNCTION_BACKUP`

5. **Communications** (700 units)
   - Phone systems
   - Data networks
   - Radio systems
   - Satellite links
   - Tags: `EQUIP_TYPE_COMMS`, `FUNCTION_COMMUNICATION`

---

## 🗺️ Geographic Distribution

```cypher
// Government Facilities by state
MATCH (f:Facility)
WHERE f.sector = 'GOVERNMENT_FACILITIES'
RETURN f.state as State, count(*) as Facilities
ORDER BY Facilities DESC;
```

### Major Government Infrastructure Locations
- **Washington DC**: Federal buildings, Capitol, White House
- **Virginia**: Pentagon, CIA, federal agencies
- **Maryland**: NSA, NIH, federal facilities
- **New York**: UN buildings, federal courts, state offices
- **California**: Federal buildings, national labs, state capitol

---

## 🔍 Key Cypher Queries

### 1. Get All Federal Buildings
```cypher
MATCH (f:Facility)
WHERE f.sector = 'GOVERNMENT_FACILITIES'
  AND f.ownershipLevel = 'FEDERAL'
RETURN f.facilityId, f.name, f.agency, f.state, f.securityLevel
ORDER BY f.securityLevel DESC, f.state;
```

### 2. Find High-Security Facilities
```cypher
MATCH (f:Facility)
WHERE f.sector = 'GOVERNMENT_FACILITIES'
  AND f.securityLevel IN ['TOP_SECRET', 'SECRET', 'CLASSIFIED']
RETURN f.name, f.securityLevel, f.agency, f.state
ORDER BY f.securityLevel;
```

### 3. Security Systems Analysis
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'GOVERNMENT_FACILITIES'
  AND 'EQUIP_TYPE_SECURITY' IN e.tags
RETURN e.equipmentType,
       e.securityFunction,
       count(*) as Systems,
       avg(e.coverageArea) as AvgCoverage
ORDER BY Systems DESC;
```

### 4. Emergency Preparedness Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'GOVERNMENT_FACILITIES'
  AND ('FUNCTION_EMERGENCY' IN e.tags OR 'SAFETY_CRITICAL' IN e.tags)
RETURN e.equipmentType,
       e.emergencyFunction,
       e.responseTime,
       count(*) as EmergencySystems
ORDER BY EmergencySystems DESC;
```

### 5. Cross-Agency Facilities
```cypher
MATCH (f:Facility)
WHERE f.sector = 'GOVERNMENT_FACILITIES'
  AND size(f.tenantAgencies) > 1
RETURN f.name,
       f.tenantAgencies,
       size(f.tenantAgencies) as AgencyCount,
       f.squareFootage
ORDER BY AgencyCount DESC;
```

### 6. Critical Infrastructure Protection
```cypher
MATCH (f:Facility)
WHERE f.sector = 'GOVERNMENT_FACILITIES'
  AND 'CRITICAL_INFRASTRUCTURE' IN f.tags
OPTIONAL MATCH (e:Equipment)-[:PROTECTS]->(f)
RETURN f.name,
       f.criticalityLevel,
       count(e) as ProtectiveSystems,
       collect(DISTINCT e.equipmentType)[0..5] as SecurityTypes
ORDER BY f.criticalityLevel DESC;
```

### 7. Energy Management Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'GOVERNMENT_FACILITIES'
  AND ('FUNCTION_ENERGY_MANAGEMENT' IN e.tags OR e.equipmentType CONTAINS 'BMS')
RETURN e.equipmentType,
       e.buildingArea,
       e.energySavings,
       count(*) as EnergySystems
ORDER BY EnergySystems DESC;
```

### 8. Access Control Points
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'GOVERNMENT_FACILITIES'
  AND e.equipmentType CONTAINS 'Access'
RETURN e.accessType,
       e.authenticationMethod,
       count(*) as AccessPoints,
       avg(e.throughput) as AvgThroughput
ORDER BY AccessPoints DESC;
```

### 9. Continuity of Operations (COOP)
```cypher
MATCH (f:Facility)
WHERE f.sector = 'GOVERNMENT_FACILITIES'
  AND EXISTS(f.coopStatus)
RETURN f.coopStatus,
       f.alternateF`ility,
       count(*) as COOPFacilities,
       avg(f.recoveryTime) as AvgRecoveryTime
ORDER BY COOPFacilities DESC;
```

### 10. Courthouse Security Systems
```cypher
MATCH (f:Facility)
WHERE f.sector = 'GOVERNMENT_FACILITIES'
  AND f.facilityType = 'COURTHOUSE'
OPTIONAL MATCH (e:Equipment)-[:LOCATED_AT]->(f)
WHERE 'EQUIP_TYPE_SECURITY' IN e.tags
RETURN f.name,
       f.state,
       f.courtLevel,
       count(e) as SecurityEquipment
ORDER BY SecurityEquipment DESC;
```

### 11. Laboratory Facilities
```cypher
MATCH (f:Facility)
WHERE f.sector = 'GOVERNMENT_FACILITIES'
  AND f.facilityType IN ['NATIONAL_LAB', 'RESEARCH_FACILITY']
RETURN f.name,
       f.researchFocus,
       f.securityClearance,
       f.annualBudget
ORDER BY f.annualBudget DESC;
```

### 12. Multi-Tenant Building Analysis
```cypher
MATCH (f:Facility)
WHERE f.sector = 'GOVERNMENT_FACILITIES'
OPTIONAL MATCH (t:Tenant)-[:OCCUPIES]->(f)
RETURN f.name as Building,
       count(t) as TenantCount,
       sum(t.squareFootage) as TotalOccupied,
       f.totalSquareFootage as BuildingSize,
       toFloat(sum(t.squareFootage)) / f.totalSquareFootage * 100 as OccupancyRate
ORDER BY TenantCount DESC;
```

---

## 🛠️ Update Procedures

### Add New Government Facility
```cypher
CREATE (f:Facility {
  facilityId: 'GOV-FAC-[LEVEL]-[STATE]-[NUMBER]',
  name: 'Facility Name',
  facilityType: 'OFFICE|COURTHOUSE|LAB|etc',
  sector: 'GOVERNMENT_FACILITIES',
  ownershipLevel: 'FEDERAL|STATE|LOCAL|TRIBAL',
  agency: 'Agency Name',
  state: 'STATE_CODE',
  city: 'City Name',
  securityLevel: 'PUBLIC|SENSITIVE|CLASSIFIED',
  squareFootage: 50000,
  occupancy: 500,
  latitude: 0.0,
  longitude: 0.0,
  createdAt: datetime()
})
RETURN f;
```

### Add Facility Equipment
```cypher
CREATE (e:Equipment {
  equipmentId: 'EQ-GOV-[TYPE]-[FACILITY]-[NUMBER]',
  equipmentType: 'Security|HVAC|Power|Emergency|etc',
  sector: 'GOVERNMENT_FACILITIES',
  manufacturer: 'Vendor Name',
  model: 'Model Number',
  tags: [
    'SECTOR_GOVERNMENT_FACILITIES',
    'EQUIP_TYPE_[TYPE]',
    'FUNCTION_[FUNCTION]',
    'VENDOR_[NAME]',
    'OPS_CRITICALITY_[LEVEL]',
    'REG_FPS',
    'REG_ISC'
  ],
  installDate: date(),
  lastInspection: date(),
  createdAt: datetime()
})
-[:LOCATED_AT]->(f:Facility {facilityId: 'FACILITY_ID'})
RETURN e;
```

### Update Security Posture
```cypher
MATCH (f:Facility {facilityId: 'GOV-FAC-XXX'})
SET f.securityLevel = 'UPGRADED_LEVEL',
    f.lastSecurityAudit = date(),
    f.nextAuditDue = date() + duration('P365D'),
    f.complianceStatus = 'COMPLIANT',
    f.updatedAt = datetime()
RETURN f;
```

### Link Tenant to Facility
```cypher
MATCH (f:Facility {facilityId: 'GOV-FAC-XXX'})
CREATE (t:Tenant {
  tenantId: 'TENANT-[AGENCY]-[NUMBER]',
  agencyName: 'Agency Name',
  squareFootage: 10000,
  floors: '[2,3,4]',
  employeeCount: 100,
  moveInDate: date()
})-[:OCCUPIES]->(f)
RETURN t, f;
```

---

## 🔗 Related Standards & Compliance

### Regulatory Framework
- **Federal Protective Service (FPS) Standards** - Tags: `REG_FPS`
- **Interagency Security Committee (ISC) Standards** - Tags: `REG_ISC`
- **Public Building Service (PBS) Requirements** - Tags: `REG_PBS`
- **HSPD-12 PIV Requirements** - Tags: `REG_HSPD12`
- **Federal Energy Management Program (FEMP)** - Tags: `REG_FEMP`

### Security Standards
- **ISC Risk Management Process**
- **FPS Facility Security Level Determinations**
- **CISA Protective Security Advisors Program**
- **GSA Physical Security Standards**

### Compliance Check Query
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'GOVERNMENT_FACILITIES'
WITH e,
     CASE WHEN 'REG_FPS' IN e.tags THEN 1 ELSE 0 END as FPS,
     CASE WHEN 'REG_ISC' IN e.tags THEN 1 ELSE 0 END as ISC,
     CASE WHEN 'REG_HSPD12' IN e.tags THEN 1 ELSE 0 END as HSPD12,
     CASE WHEN 'REG_FEMP' IN e.tags THEN 1 ELSE 0 END as FEMP
RETURN 'Government Facilities Compliance' as Sector,
       sum(FPS) as FPS_Compliant,
       sum(ISC) as ISC_Compliant,
       sum(HSPD12) as HSPD12_Compliant,
       sum(FEMP) as FEMP_Compliant,
       count(e) as TotalEquipment;
```

---

## 📁 Deployment Scripts

### Primary Deployment Script
Location: `/home/jim/2_OXOT_Projects_Dev/scripts/universal_location_migration/GOVERNMENT_FACILITIES_SECTOR_IMPLEMENTATION.cypher`

### Validation Script
```cypher
// Verify Government Facilities sector deployment
MATCH (n)
WHERE n.sector = 'GOVERNMENT_FACILITIES'
WITH count(n) as totalNodes
MATCH (f:Facility)
WHERE f.sector = 'GOVERNMENT_FACILITIES'
WITH totalNodes, count(f) as facilities
MATCH (e:Equipment)
WHERE e.sector = 'GOVERNMENT_FACILITIES'
RETURN 'GOVERNMENT_FACILITIES' as Sector,
       totalNodes as TotalNodes,
       facilities as Facilities,
       count(e) as Equipment,
       CASE WHEN totalNodes >= 27000 THEN 'PASS' ELSE 'FAIL' END as Status;
```

---

## 🔄 Cross-Sector Dependencies

### Energy Sector
- Power supply for facilities
- Backup power systems
- Energy management
- Grid connections

### Information Technology
- Data centers
- Network infrastructure
- Cybersecurity systems
- Cloud services

### Communications
- Emergency communications
- Interagency networks
- Public safety systems
- Satellite communications

### Emergency Services
- First responder coordination
- Emergency management centers
- Disaster response
- Public safety integration

---

## 📈 Performance Metrics

### Operational KPIs
- Facility availability: 99.9%
- Security system uptime: 99.95%
- Energy efficiency: 30% reduction target
- Space utilization: 85%
- Emergency response time: <5 minutes

### Query Performance
```cypher
// Check query performance for Government Facilities sector
EXPLAIN
MATCH (e:Equipment)
WHERE e.sector = 'GOVERNMENT_FACILITIES'
  AND 'EQUIP_TYPE_SECURITY' IN e.tags
RETURN count(e);
```

---

**Wiki Navigation**: [← Main Index](../00_MAIN_INDEX.md) | [→ Nuclear Sector](NUCLEAR_SECTOR.md) | [Queries Library](../QUERIES_LIBRARY.md)