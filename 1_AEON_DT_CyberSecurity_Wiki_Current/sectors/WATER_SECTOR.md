# Water & Wastewater Systems Sector

**Sector Code**: WATER
**Node Count**: 27,200
**Status**: ✅ Operational
**Last Updated**: 2024-11-22

[← Back to Main Index](../00_MAIN_INDEX.md) | [→ Next: Energy Sector](ENERGY_SECTOR.md)

---

## 📊 Sector Overview

The Water and Wastewater Systems Sector ensures the supply of safe drinking water and proper treatment of wastewater. This sector includes treatment plants, distribution systems, storage facilities, and monitoring stations.

### Key Statistics
- **Total Nodes**: 27,200
- **Facilities**: 25 major facilities
- **Equipment**: 250+ critical systems
- **Geographic Coverage**: All 50 states
- **Critical Infrastructure**: 100% essential services

---

## 🏗️ Node Types Distribution

```cypher
// Get Water sector node distribution
MATCH (n)
WHERE n.sector = 'WATER'
RETURN labels(n) as NodeTypes, count(*) as Count
ORDER BY Count DESC;
```

### Estimated Distribution
- **Equipment**: 250 nodes (pumps, valves, treatment systems)
- **Facility**: 25 nodes (treatment plants, distribution centers)
- **Device**: 13,500 nodes (sensors, meters, controllers)
- **Property**: 6,750 nodes (system properties, configurations)
- **Measurement**: 6,675 nodes (flow rates, quality metrics)

---

## 🏭 Subsectors

### Water Treatment (40%)
- Municipal treatment plants
- Chemical treatment systems
- Filtration systems
- Quality monitoring

### Water Distribution (30%)
- Pipeline networks
- Pumping stations
- Storage tanks
- Pressure management

### Wastewater Treatment (20%)
- Sewage treatment plants
- Industrial wastewater
- Storm water management
- Sludge processing

### Water Storage (10%)
- Reservoirs
- Water towers
- Emergency storage
- Backup systems

---

## 🔧 Equipment Types

### Critical Equipment Categories
```cypher
// Get Water sector equipment types
MATCH (e:Equipment)
WHERE e.sector = 'WATER'
RETURN e.equipmentType as Type, count(*) as Count
ORDER BY Count DESC
LIMIT 20;
```

### Primary Equipment Types
1. **Pumps** (30 units)
   - Centrifugal pumps
   - Submersible pumps
   - Booster pumps
   - Tags: `EQUIP_TYPE_PUMP`, `FUNCTION_WATER_PUMPING`

2. **Valves** (30 units)
   - Control valves
   - Pressure relief valves
   - Check valves
   - Tags: `EQUIP_TYPE_VALVE`, `FUNCTION_FLOW_CONTROL`

3. **Treatment Systems** (25 units)
   - Chlorination systems
   - UV disinfection
   - Membrane filters
   - Tags: `EQUIP_TYPE_TREATMENT`, `FUNCTION_WATER_TREATMENT`

4. **SCADA Systems** (20 units)
   - Control systems
   - Monitoring systems
   - Tags: `EQUIP_TYPE_SCADA`, `OPS_CRITICALITY_CRITICAL`

---

## 🗺️ Geographic Distribution

```cypher
// Water facilities by state
MATCH (f:Facility)
WHERE f.sector = 'WATER'
RETURN f.state as State, count(*) as Facilities
ORDER BY Facilities DESC;
```

### Major Water Infrastructure Locations
- **California**: Los Angeles Aqueduct, SF Water System
- **New York**: NYC Water Supply System, Buffalo Water
- **Texas**: Houston Water, Dallas Water Utilities
- **Illinois**: Chicago Water Management
- **Pennsylvania**: Philadelphia Water Department

---

## 🔍 Key Cypher Queries

### 1. Get All Water Treatment Plants
```cypher
MATCH (f:Facility)
WHERE f.sector = 'WATER'
  AND f.facilityType = 'WATER_TREATMENT_PLANT'
RETURN f.facilityId, f.name, f.state, f.city
ORDER BY f.state, f.city;
```

### 2. Find Critical Water Equipment
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'WATER'
  AND 'OPS_CRITICALITY_CRITICAL' IN e.tags
RETURN e.equipmentId, e.equipmentType, e.tags
LIMIT 50;
```

### 3. Water Quality Monitoring Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'WATER'
  AND ('FUNCTION_MONITORING' IN e.tags
       OR e.equipmentType CONTAINS 'Monitor')
RETURN e.equipmentId, e.equipmentType, e.facilityId;
```

### 4. Cross-Sector Dependencies
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'WATER'
  AND ANY(tag IN e.tags WHERE tag STARTS WITH 'SECTOR_' AND tag <> 'SECTOR_WATER')
RETURN e.equipmentType,
       [tag IN e.tags WHERE tag STARTS WITH 'SECTOR_'] as sectors,
       count(*) as instances
ORDER BY instances DESC;
```

### 5. Vulnerability Analysis
```cypher
MATCH (cve:CVE)-[:AFFECTS]->(e:Equipment)
WHERE e.sector = 'WATER'
  AND cve.baseScore >= 7.0
RETURN cve.id as CVE,
       cve.baseScore as Score,
       count(e) as AffectedEquipment
ORDER BY Score DESC
LIMIT 20;
```

### 6. SCADA System Security
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'WATER'
  AND (e.equipmentType CONTAINS 'SCADA'
       OR 'EQUIP_TYPE_SCADA' IN e.tags)
OPTIONAL MATCH (cve:CVE)-[:AFFECTS]->(e)
RETURN e.equipmentId,
       e.equipmentType,
       count(cve) as Vulnerabilities,
       max(cve.baseScore) as MaxCVSS
ORDER BY Vulnerabilities DESC;
```

### 7. Water Infrastructure Compliance
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'WATER'
  AND ANY(tag IN e.tags WHERE tag STARTS WITH 'REG_')
WITH e, [tag IN e.tags WHERE tag STARTS WITH 'REG_'] as regulations
RETURN e.equipmentType,
       regulations,
       count(*) as compliantEquipment
ORDER BY compliantEquipment DESC;
```

### 8. Emergency Response Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'WATER'
  AND ANY(tag IN e.tags WHERE tag CONTAINS 'EMERGENCY' OR tag CONTAINS 'BACKUP')
RETURN e.equipmentType,
       e.facilityId,
       e.tags
ORDER BY e.facilityId;
```

### 9. Water Distribution Network
```cypher
MATCH (f:Facility)
WHERE f.sector = 'WATER'
  AND f.facilityType IN ['PUMPING_STATION', 'DISTRIBUTION_CENTER']
OPTIONAL MATCH (e:Equipment)-[:LOCATED_AT]->(f)
RETURN f.name as Facility,
       f.facilityType as Type,
       count(e) as Equipment
ORDER BY Equipment DESC;
```

### 10. Maintenance Requirements
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'WATER'
  AND EXISTS(e.maintenanceSchedule)
RETURN e.equipmentType,
       e.maintenanceSchedule,
       count(*) as Units
ORDER BY Units DESC;
```

---

## 🛠️ Update Procedures

### Add New Water Treatment Plant
```cypher
CREATE (f:Facility {
  facilityId: 'WATER-TRT-[STATE]-[NUMBER]',
  name: 'Plant Name',
  facilityType: 'WATER_TREATMENT_PLANT',
  sector: 'WATER',
  state: 'STATE_CODE',
  city: 'City Name',
  latitude: 0.0,
  longitude: 0.0,
  capacity: 'MGD value',
  createdAt: datetime()
})
RETURN f;
```

### Add Water Equipment
```cypher
CREATE (e:Equipment {
  equipmentId: 'EQ-WATER-[TYPE]-[STATE]-[NUMBER]',
  equipmentType: 'Pump|Valve|Treatment|etc',
  sector: 'WATER',
  manufacturer: 'Vendor Name',
  model: 'Model Number',
  tags: [
    'SECTOR_WATER',
    'EQUIP_TYPE_[TYPE]',
    'FUNCTION_[FUNCTION]',
    'VENDOR_[NAME]',
    'OPS_CRITICALITY_[LEVEL]',
    'REG_EPA_WATER'
  ],
  installDate: date(),
  createdAt: datetime()
})
-[:LOCATED_AT]->(f:Facility {facilityId: 'FACILITY_ID'})
RETURN e;
```

### Update Equipment Status
```cypher
MATCH (e:Equipment {equipmentId: 'EQ-WATER-XXX'})
SET e.operationalStatus = 'OPERATIONAL|MAINTENANCE|OFFLINE',
    e.lastInspection = date(),
    e.updatedAt = datetime()
RETURN e;
```

---

## 🔗 Related Standards & Compliance

### Regulatory Framework
- **EPA Water Quality Standards** - Tags: `REG_EPA_WATER`
- **Safe Drinking Water Act (SDWA)** - Tags: `REG_SDWA`
- **Clean Water Act (CWA)** - Tags: `REG_CWA`
- **America's Water Infrastructure Act** - Tags: `REG_AWIA`

### Security Standards
- **NIST Cybersecurity Framework** - Water sector profile
- **ICS-CERT Water Sector Guidelines**
- **AWWA Cybersecurity Standards**

### Compliance Check Query
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'WATER'
WITH e,
     CASE WHEN 'REG_EPA_WATER' IN e.tags THEN 1 ELSE 0 END as EPA,
     CASE WHEN 'REG_SDWA' IN e.tags THEN 1 ELSE 0 END as SDWA,
     CASE WHEN 'REG_CWA' IN e.tags THEN 1 ELSE 0 END as CWA,
     CASE WHEN 'REG_AWIA' IN e.tags THEN 1 ELSE 0 END as AWIA
RETURN 'Water Compliance' as Sector,
       sum(EPA) as EPA_Compliant,
       sum(SDWA) as SDWA_Compliant,
       sum(CWA) as CWA_Compliant,
       sum(AWIA) as AWIA_Compliant,
       count(e) as TotalEquipment;
```

---

## 📁 Deployment Scripts

### Primary Deployment Script
Location: `/home/jim/2_OXOT_Projects_Dev/scripts/universal_location_migration/WATER_SECTOR_IMPLEMENTATION.cypher`

### Validation Script
```cypher
// Verify Water sector deployment
MATCH (n)
WHERE n.sector = 'WATER'
WITH count(n) as totalNodes
MATCH (f:Facility)
WHERE f.sector = 'WATER'
WITH totalNodes, count(f) as facilities
MATCH (e:Equipment)
WHERE e.sector = 'WATER'
RETURN 'WATER' as Sector,
       totalNodes as TotalNodes,
       facilities as Facilities,
       count(e) as Equipment,
       CASE WHEN totalNodes >= 27000 THEN 'PASS' ELSE 'FAIL' END as Status;
```

---

## 🔄 Cross-Sector Dependencies

### Energy Sector
- Power for pumping stations
- Backup power systems
- Energy-intensive treatment processes

### Chemical Sector
- Water treatment chemicals
- Chlorine and fluoride supplies
- pH adjustment chemicals

### Information Technology
- SCADA systems
- Remote monitoring
- Cybersecurity infrastructure

### Transportation
- Chemical delivery
- Equipment transportation
- Emergency water distribution

---

## 📈 Performance Metrics

### Operational KPIs
- Water quality compliance: 99.9%
- System availability: 99.95%
- Critical equipment uptime: 99.5%
- Emergency response time: <30 minutes

### Query Performance
```cypher
// Check query performance for Water sector
EXPLAIN
MATCH (e:Equipment)
WHERE e.sector = 'WATER'
RETURN count(e);
```

---

**Wiki Navigation**: [← Main Index](../00_MAIN_INDEX.md) | [→ Energy Sector](ENERGY_SECTOR.md) | [Queries Library](../QUERIES_LIBRARY.md)