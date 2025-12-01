# Nuclear Sector

**Sector Code**: NUCLEAR
**Node Count**: 10,448
**Status**: ✅ Operational
**Last Updated**: 2024-11-22

[← Back to Main Index](../00_MAIN_INDEX.md) | [→ Next: Communications Sector](COMMUNICATIONS_SECTOR.md)

---

## 📊 Sector Overview

The Nuclear Sector consists of nuclear power plants, research reactors, nuclear fuel cycle facilities, and radioactive waste storage. This highly regulated sector provides approximately 20% of the nation's electricity through 93 commercial reactors.

### Key Statistics
- **Total Nodes**: 10,448 (Smallest critical infrastructure sector)
- **Nuclear Plants**: 54 operating sites
- **Reactors**: 93 commercial reactors
- **Research Reactors**: 31 facilities
- **Equipment Systems**: 5,000+ critical components
- **Geographic Coverage**: 28 states

---

## 🏗️ Node Types Distribution

```cypher
// Get Nuclear sector node distribution
MATCH (n)
WHERE n.sector = 'NUCLEAR'
RETURN labels(n) as NodeTypes, count(*) as Count
ORDER BY Count DESC;
```

### Node Distribution
- **Equipment**: 5,000 nodes (reactor systems, safety systems, control rods)
- **Facility**: 85 nodes (plants, research reactors, fuel facilities)
- **Device**: 3,000 nodes (sensors, monitors, detectors)
- **Property**: 1,200 nodes (isotopes, materials, safety parameters)
- **Measurement**: 1,163 nodes (radiation levels, temperatures, pressures)

---

## 🏭 Subsectors

### Commercial Power Generation (60%)
- Pressurized Water Reactors (PWR)
- Boiling Water Reactors (BWR)
- Power generation systems
- Spent fuel storage
- Decommissioning sites

### Research & Medical (20%)
- Research reactors
- Medical isotope production
- University reactors
- National laboratory reactors
- Test reactors

### Fuel Cycle (15%)
- Uranium enrichment
- Fuel fabrication
- Conversion facilities
- Mining and milling
- Transportation

### Waste Management (5%)
- Spent fuel storage
- Low-level waste sites
- Disposal facilities
- Processing facilities
- Transportation casks

---

## 🔧 Equipment Types

### Critical Equipment Categories
```cypher
// Get Nuclear sector equipment types
MATCH (e:Equipment)
WHERE e.sector = 'NUCLEAR'
RETURN e.equipmentType as Type, count(*) as Count
ORDER BY Count DESC
LIMIT 20;
```

### Primary Equipment Types
1. **Reactor Core Systems** (1,000 units)
   - Control rods
   - Fuel assemblies
   - Core internals
   - Neutron detectors
   - Tags: `EQUIP_TYPE_REACTOR_CORE`, `SAFETY_CRITICAL`

2. **Safety Systems** (1,500 units)
   - Emergency core cooling
   - Containment systems
   - Shutdown systems
   - Pressure relief valves
   - Tags: `EQUIP_TYPE_SAFETY`, `NRC_SAFETY_RELATED`

3. **Control & Instrumentation** (800 units)
   - Reactor protection systems
   - Control room equipment
   - Digital I&C systems
   - Safety parameter displays
   - Tags: `EQUIP_TYPE_CONTROL`, `OPS_CRITICALITY_CRITICAL`

4. **Radiation Monitoring** (700 units)
   - Area monitors
   - Process monitors
   - Effluent monitors
   - Personnel monitors
   - Tags: `EQUIP_TYPE_RADIATION_MONITOR`, `FUNCTION_MONITORING`

5. **Power Generation** (500 units)
   - Steam generators
   - Turbines
   - Generators
   - Condensers
   - Tags: `EQUIP_TYPE_POWER_GEN`, `FUNCTION_GENERATION`

---

## 🗺️ Geographic Distribution

```cypher
// Nuclear facilities by state
MATCH (f:Facility)
WHERE f.sector = 'NUCLEAR'
RETURN f.state as State, count(*) as Facilities
ORDER BY Facilities DESC;
```

### Major Nuclear Infrastructure Locations
- **Illinois**: 11 reactors at 6 plants (most nuclear capacity)
- **Pennsylvania**: 9 reactors at 5 plants
- **South Carolina**: 7 reactors at 4 plants
- **New York**: 4 reactors at 3 plants
- **Texas**: 4 reactors at 2 plants

---

## 🔍 Key Cypher Queries

### 1. Get All Nuclear Power Plants
```cypher
MATCH (f:Facility)
WHERE f.sector = 'NUCLEAR'
  AND f.facilityType = 'NUCLEAR_POWER_PLANT'
RETURN f.facilityId, f.name, f.state, f.reactorCount, f.capacity_MW
ORDER BY f.capacity_MW DESC;
```

### 2. Find Safety-Related Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'NUCLEAR'
  AND ('NRC_SAFETY_RELATED' IN e.tags OR 'SAFETY_CRITICAL' IN e.tags)
RETURN e.equipmentType,
       e.safetyClass,
       e.seismicCategory,
       count(*) as SafetySystems
ORDER BY SafetySystems DESC;
```

### 3. NRC Regulated Equipment
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'NUCLEAR'
  AND ANY(tag IN e.tags WHERE tag STARTS WITH 'NRC_')
RETURN e.equipmentType,
       [tag IN e.tags WHERE tag STARTS WITH 'NRC_'] as nrcRequirements,
       count(*) as RegulatedEquipment
ORDER BY RegulatedEquipment DESC;
```

### 4. Emergency Planning Zone Analysis
```cypher
MATCH (f:Facility)
WHERE f.sector = 'NUCLEAR'
  AND f.facilityType = 'NUCLEAR_POWER_PLANT'
RETURN f.name,
       f.epzRadius_miles,
       f.populationWithinEPZ,
       f.emergencyResponseTime
ORDER BY f.populationWithinEPZ DESC;
```

### 5. Digital I&C Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'NUCLEAR'
  AND ('DIGITAL_IC' IN e.tags OR e.equipmentType CONTAINS 'Digital')
OPTIONAL MATCH (cve:CVE)-[:AFFECTS]->(e)
RETURN e.equipmentType,
       e.cyberSecurityLevel,
       count(DISTINCT e) as DigitalSystems,
       count(cve) as Vulnerabilities
ORDER BY DigitalSystems DESC;
```

### 6. Spent Fuel Storage
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'NUCLEAR'
  AND (e.equipmentType CONTAINS 'Spent Fuel' OR 'FUNCTION_FUEL_STORAGE' IN e.tags)
RETURN e.equipmentType,
       e.storageType,
       e.capacity,
       e.currentInventory
ORDER BY e.currentInventory DESC;
```

### 7. Radiation Detection Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'NUCLEAR'
  AND 'EQUIP_TYPE_RADIATION_MONITOR' IN e.tags
RETURN e.monitorType,
       e.detectionRange,
       e.alarmSetpoint,
       count(*) as Monitors
ORDER BY Monitors DESC;
```

### 8. Emergency Diesel Generators
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'NUCLEAR'
  AND e.equipmentType CONTAINS 'Emergency Diesel'
RETURN e.equipmentId,
       e.capacity_MW,
       e.fuelCapacity_hours,
       e.lastTestDate,
       e.reliability
ORDER BY e.capacity_MW DESC;
```

### 9. Research Reactor Inventory
```cypher
MATCH (f:Facility)
WHERE f.sector = 'NUCLEAR'
  AND f.facilityType = 'RESEARCH_REACTOR'
RETURN f.name,
       f.thermalPower_MW,
       f.researchFocus,
       f.operator,
       f.licenseExpiration
ORDER BY f.thermalPower_MW DESC;
```

### 10. Control Rod Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'NUCLEAR'
  AND (e.equipmentType CONTAINS 'Control Rod' OR 'FUNCTION_REACTIVITY_CONTROL' IN e.tags)
RETURN e.equipmentType,
       e.rodType,
       e.insertionTime_seconds,
       count(*) as ControlSystems
ORDER BY ControlSystems DESC;
```

### 11. Seismic Qualified Equipment
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'NUCLEAR'
  AND EXISTS(e.seismicCategory)
  AND e.seismicCategory IN ['I', 'II']
RETURN e.seismicCategory,
       e.equipmentType,
       count(*) as SeismicEquipment
ORDER BY e.seismicCategory, SeismicEquipment DESC;
```

### 12. Cyber Security Controls
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'NUCLEAR'
  AND EXISTS(e.cyberSecurityLevel)
WITH e.cyberSecurityLevel as Level,
     count(*) as Systems,
     collect(DISTINCT e.equipmentType)[0..5] as TopEquipment
RETURN Level, Systems, TopEquipment
ORDER BY Level;
```

---

## 🛠️ Update Procedures

### Add New Nuclear Facility
```cypher
CREATE (f:Facility {
  facilityId: 'NUC-FAC-[TYPE]-[STATE]-[NUMBER]',
  name: 'Facility Name',
  facilityType: 'NUCLEAR_POWER_PLANT|RESEARCH_REACTOR|FUEL_FACILITY',
  sector: 'NUCLEAR',
  state: 'STATE_CODE',
  nrcDocket: 'Docket Number',
  licenseNumber: 'License Number',
  reactorType: 'PWR|BWR|etc',
  capacity_MW: 1000,
  commercialOperation: date('YYYY-MM-DD'),
  latitude: 0.0,
  longitude: 0.0,
  createdAt: datetime()
})
RETURN f;
```

### Add Nuclear Equipment
```cypher
CREATE (e:Equipment {
  equipmentId: 'EQ-NUC-[TYPE]-[PLANT]-[NUMBER]',
  equipmentType: 'Reactor|Safety|Control|Monitor|etc',
  sector: 'NUCLEAR',
  manufacturer: 'Vendor Name',
  model: 'Model Number',
  safetyClass: '1|2|3|Non-Safety',
  seismicCategory: 'I|II|III',
  tags: [
    'SECTOR_NUCLEAR',
    'EQUIP_TYPE_[TYPE]',
    'NRC_SAFETY_RELATED',
    'SAFETY_CLASS_[1|2|3]',
    'SEISMIC_CAT_[I|II|III]',
    'REG_10CFR50_APP_B'
  ],
  qualificationLife: 40,
  installDate: date(),
  createdAt: datetime()
})
-[:LOCATED_AT]->(f:Facility {facilityId: 'FACILITY_ID'})
RETURN e;
```

### Update Equipment Qualification
```cypher
MATCH (e:Equipment {equipmentId: 'EQ-NUC-XXX'})
SET e.lastQualificationTest = date(),
    e.nextQualificationDue = date() + duration('P2Y'),
    e.qualificationStatus = 'QUALIFIED',
    e.remainingLife = 20,
    e.updatedAt = datetime()
RETURN e;
```

### Record Maintenance Activity
```cypher
MATCH (e:Equipment {equipmentId: 'EQ-NUC-XXX'})
CREATE (m:Maintenance {
  maintenanceId: 'MAINT-[NUMBER]',
  maintenanceType: 'PREVENTIVE|CORRECTIVE|SURVEILLANCE',
  workOrder: 'WO-NUMBER',
  performedDate: date(),
  nextDue: date() + duration('P18M'),
  safetySignificance: 'HIGH|MEDIUM|LOW'
})-[:PERFORMED_ON]->(e)
RETURN m, e;
```

---

## 🔗 Related Standards & Compliance

### Regulatory Framework
- **10 CFR Part 50 - Domestic Licensing** - Tags: `REG_10CFR50`
- **10 CFR Part 73 - Physical Security** - Tags: `REG_10CFR73`
- **10 CFR Part 26 - Fitness for Duty** - Tags: `REG_10CFR26`
- **10 CFR 50 Appendix B - Quality Assurance** - Tags: `REG_10CFR50_APP_B`
- **NEI 08-09 Cyber Security Plan** - Tags: `REG_NEI_08_09`

### Industry Standards
- **ASME Boiler and Pressure Vessel Code**
- **IEEE Nuclear Standards**
- **ANS (American Nuclear Society) Standards**
- **INPO (Institute of Nuclear Power Operations) Guidelines**

### Compliance Check Query
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'NUCLEAR'
WITH e,
     CASE WHEN 'REG_10CFR50' IN e.tags THEN 1 ELSE 0 END as CFR50,
     CASE WHEN 'REG_10CFR50_APP_B' IN e.tags THEN 1 ELSE 0 END as AppB,
     CASE WHEN 'REG_10CFR73' IN e.tags THEN 1 ELSE 0 END as CFR73,
     CASE WHEN 'REG_NEI_08_09' IN e.tags THEN 1 ELSE 0 END as Cyber
RETURN 'Nuclear Compliance' as Sector,
       sum(CFR50) as Part50_Compliant,
       sum(AppB) as AppendixB_Compliant,
       sum(CFR73) as Security_Compliant,
       sum(Cyber) as CyberSecurity_Compliant,
       count(e) as TotalEquipment;
```

---

## 📁 Deployment Scripts

### Primary Deployment Script
Location: `/home/jim/2_OXOT_Projects_Dev/scripts/universal_location_migration/NUCLEAR_SECTOR_IMPLEMENTATION.cypher`

### Validation Script
```cypher
// Verify Nuclear sector deployment
MATCH (n)
WHERE n.sector = 'NUCLEAR'
WITH count(n) as totalNodes
MATCH (f:Facility)
WHERE f.sector = 'NUCLEAR'
WITH totalNodes, count(f) as facilities
MATCH (e:Equipment)
WHERE e.sector = 'NUCLEAR'
RETURN 'NUCLEAR' as Sector,
       totalNodes as TotalNodes,
       facilities as Facilities,
       count(e) as Equipment,
       CASE WHEN totalNodes >= 10448 THEN 'PASS' ELSE 'FAIL' END as Status;
```

---

## 🔄 Cross-Sector Dependencies

### Energy Sector
- Electricity generation
- Grid integration
- Transmission infrastructure
- Load balancing

### Water Sector
- Cooling water intake
- Circulating water systems
- Service water
- Fire protection water

### Chemical Sector
- Water treatment chemicals
- Boric acid for reactivity control
- Lubricants and sealants
- Decontamination chemicals

### Transportation
- Spent fuel transportation
- Fresh fuel delivery
- Emergency response vehicles
- Material shipments

---

## 📈 Performance Metrics

### Operational KPIs
- Capacity factor: >90%
- Forced outage rate: <2%
- Safety system availability: >99%
- Unplanned scrams: <1 per year
- Radiation exposure: ALARA (As Low As Reasonably Achievable)

### Query Performance
```cypher
// Check query performance for Nuclear sector
EXPLAIN
MATCH (e:Equipment)
WHERE e.sector = 'NUCLEAR'
  AND 'NRC_SAFETY_RELATED' IN e.tags
RETURN count(e);
```

---

**Wiki Navigation**: [← Main Index](../00_MAIN_INDEX.md) | [→ Communications Sector](COMMUNICATIONS_SECTOR.md) | [Queries Library](../QUERIES_LIBRARY.md)