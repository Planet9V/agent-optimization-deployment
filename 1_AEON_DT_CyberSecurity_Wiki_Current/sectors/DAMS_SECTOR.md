# Dams Sector

**Sector Code**: DAMS
**Node Count**: 35,184
**Status**: ✅ Operational
**Last Updated**: 2024-11-22

[← Back to Main Index](../00_MAIN_INDEX.md)

---

## 📊 Sector Overview

The Dams Sector comprises dam projects, navigation locks, levees, hurricane barriers, mine tailings, and other similar water retention and control structures. This sector manages critical water resources for power generation, water supply, flood control, and navigation.

### Key Statistics
- **Total Nodes**: 35,184
- **Major Dams**: 91,000+ dams (3,000+ high hazard)
- **Levee Systems**: 100,000+ miles
- **Equipment Systems**: 15,000+ control and monitoring systems
- **Hydroelectric Capacity**: 80 GW
- **Geographic Coverage**: All 50 states

---

## 🏗️ Node Types Distribution

```cypher
// Get Dams sector node distribution
MATCH (n)
WHERE n.sector = 'DAMS'
RETURN labels(n) as NodeTypes, count(*) as Count
ORDER BY Count DESC;
```

### Node Distribution
- **Equipment**: 15,000 nodes (gates, turbines, pumps, controls)
- **Facility**: 3,000 nodes (dams, levees, locks, spillways)
- **Device**: 10,000 nodes (sensors, gauges, monitors)
- **Property**: 4,184 nodes (water levels, flow rates, structural data)
- **Measurement**: 3,000 nodes (discharge, pressure, seismic)

---

## 🏭 Subsectors

### Hydroelectric Dams (35%)
- Power generation dams
- Pumped storage facilities
- Run-of-river projects
- Small hydro installations
- Turbine generators

### Flood Control (30%)
- Flood control dams
- Levee systems
- Floodwalls
- Storm surge barriers
- Detention basins

### Water Supply (20%)
- Municipal water reservoirs
- Irrigation dams
- Agricultural water storage
- Industrial water supply
- Aquifer recharge

### Navigation (10%)
- Navigation locks
- Canal systems
- River navigation
- Port infrastructure
- Lock and dam combinations

### Tailings & Industrial (5%)
- Mine tailings dams
- Industrial waste impoundments
- Ash pond dams
- Chemical retention
- Treatment facilities

---

## 🔧 Equipment Types

### Critical Equipment Categories
```cypher
// Get Dams sector equipment types
MATCH (e:Equipment)
WHERE e.sector = 'DAMS'
RETURN e.equipmentType as Type, count(*) as Count
ORDER BY Count DESC
LIMIT 20;
```

### Primary Equipment Types
1. **Spillway Gates** (3,000 units)
   - Radial gates
   - Vertical lift gates
   - Drum gates
   - Emergency gates
   - Tags: `EQUIP_TYPE_GATE`, `SAFETY_CRITICAL`

2. **Turbine Generators** (2,500 units)
   - Francis turbines
   - Kaplan turbines
   - Pelton wheels
   - Pump turbines
   - Tags: `EQUIP_TYPE_TURBINE`, `FUNCTION_GENERATION`

3. **Control Systems** (2,000 units)
   - SCADA systems
   - Gate controls
   - Water level controls
   - Emergency systems
   - Tags: `EQUIP_TYPE_CONTROL`, `OPS_CRITICALITY_CRITICAL`

4. **Monitoring Equipment** (2,000 units)
   - Piezometers
   - Strain gauges
   - Seismic monitors
   - Water quality sensors
   - Tags: `EQUIP_TYPE_MONITORING`, `FUNCTION_SAFETY`

5. **Pumping Systems** (1,500 units)
   - Drainage pumps
   - Dewatering pumps
   - Fish passage pumps
   - Irrigation pumps
   - Tags: `EQUIP_TYPE_PUMP`, `FUNCTION_WATER_CONTROL`

---

## 🗺️ Geographic Distribution

```cypher
// Dams facilities by state
MATCH (f:Facility)
WHERE f.sector = 'DAMS'
RETURN f.state as State, count(*) as Facilities
ORDER BY Facilities DESC;
```

### Major Dam Infrastructure Locations
- **California**: 1,400+ dams, Oroville Dam, Shasta Dam
- **Texas**: 7,000+ dams, extensive flood control
- **Washington**: Grand Coulee Dam, major hydroelectric
- **Tennessee**: TVA system, 29 hydroelectric dams
- **Colorado**: 1,800+ dams, major water storage

---

## 🔍 Key Cypher Queries

### 1. Get High Hazard Dams
```cypher
MATCH (f:Facility)
WHERE f.sector = 'DAMS'
  AND f.hazardClassification = 'HIGH'
RETURN f.damId, f.name, f.state, f.height_ft, f.storageCapacity_AF
ORDER BY f.height_ft DESC;
```

### 2. Find Hydroelectric Facilities
```cypher
MATCH (f:Facility)
WHERE f.sector = 'DAMS'
  AND f.primaryPurpose = 'HYDROELECTRIC'
RETURN f.name,
       f.installedCapacity_MW,
       f.annualGeneration_GWh,
       f.turbineCount,
       f.operator
ORDER BY f.installedCapacity_MW DESC;
```

### 3. Spillway Gate Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'DAMS'
  AND 'EQUIP_TYPE_GATE' IN e.tags
RETURN e.gateType,
       e.dimensions,
       e.dischargeCapacity_cfs,
       count(*) as GateCount
ORDER BY e.dischargeCapacity_cfs DESC;
```

### 4. Dam Safety Monitoring
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'DAMS'
  AND ('MONITORING' IN e.tags OR e.function = 'DAM_SAFETY')
RETURN e.monitoringType,
       e.measurementParameter,
       count(*) as Instruments,
       avg(e.readingFrequency_min) as AvgFrequency
ORDER BY Instruments DESC;
```

### 5. Levee System Analysis
```cypher
MATCH (f:Facility)
WHERE f.sector = 'DAMS'
  AND f.facilityType = 'LEVEE'
RETURN f.leveeSystem,
       sum(f.length_miles) as TotalMiles,
       avg(f.height_ft) as AvgHeight,
       f.protectedPopulation
ORDER BY TotalMiles DESC;
```

### 6. Emergency Action Plans
```cypher
MATCH (f:Facility)
WHERE f.sector = 'DAMS'
  AND EXISTS(f.emergencyActionPlan)
RETURN f.hazardClassification,
       count(*) as DamsWithEAP,
       avg(f.inundationArea_sqmi) as AvgInundationArea,
       sum(f.populationAtRisk) as TotalPopulationAtRisk
ORDER BY f.hazardClassification;
```

### 7. Water Supply Reservoirs
```cypher
MATCH (f:Facility)
WHERE f.sector = 'DAMS'
  AND 'WATER_SUPPLY' IN f.purposes
RETURN f.name,
       f.storageCapacity_AF,
       f.currentStorage_AF,
       f.percentFull,
       f.servesPopulation
ORDER BY f.storageCapacity_AF DESC;
```

### 8. SCADA Control Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'DAMS'
  AND (e.equipmentType = 'SCADA' OR 'SCADA' IN e.tags)
OPTIONAL MATCH (cve:CVE)-[:AFFECTS]->(e)
RETURN e.damName,
       e.scadaVendor,
       count(cve) as Vulnerabilities,
       max(cve.baseScore) as MaxCVSS
ORDER BY Vulnerabilities DESC;
```

### 9. Turbine Generator Performance
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'DAMS'
  AND 'EQUIP_TYPE_TURBINE' IN e.tags
RETURN e.turbineType,
       avg(e.efficiency) as AvgEfficiency,
       sum(e.ratedCapacity_MW) as TotalCapacity_MW,
       count(*) as TurbineCount
ORDER BY TotalCapacity_MW DESC;
```

### 10. Navigation Lock Operations
```cypher
MATCH (f:Facility)
WHERE f.sector = 'DAMS'
  AND f.facilityType = 'LOCK'
RETURN f.lockName,
       f.riverSystem,
       f.liftHeight_ft,
       f.annualLockages,
       f.tonnageTransited_M
ORDER BY f.tonnageTransited_M DESC;
```

### 11. Seismic Monitoring Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'DAMS'
  AND e.monitoringType = 'SEISMIC'
RETURN e.damName,
       e.accelerometerCount,
       e.seismicZone,
       e.peakGroundAcceleration
ORDER BY e.seismicZone DESC;
```

### 12. Multi-Purpose Dam Analysis
```cypher
MATCH (f:Facility)
WHERE f.sector = 'DAMS'
  AND size(f.purposes) > 1
RETURN f.name,
       f.purposes,
       f.primaryPurpose,
       f.yearCompleted,
       f.federalProject
ORDER BY size(f.purposes) DESC;
```

---

## 🛠️ Update Procedures

### Add New Dam Facility
```cypher
CREATE (f:Facility {
  facilityId: 'DAM-[STATE]-[ID_NUMBER]',
  damId: 'NID_ID',
  name: 'Dam Name',
  facilityType: 'DAM',
  sector: 'DAMS',
  state: 'STATE_CODE',
  river: 'River Name',
  hazardClassification: 'HIGH|SIGNIFICANT|LOW',
  height_ft: 100,
  length_ft: 500,
  storageCapacity_AF: 50000,
  purposes: ['HYDROELECTRIC', 'FLOOD_CONTROL', 'WATER_SUPPLY'],
  yearCompleted: 1950,
  latitude: 0.0,
  longitude: 0.0,
  createdAt: datetime()
})
RETURN f;
```

### Add Dam Equipment
```cypher
CREATE (e:Equipment {
  equipmentId: 'EQ-DAM-[TYPE]-[DAM]-[NUMBER]',
  equipmentType: 'Gate|Turbine|Pump|Monitor|etc',
  sector: 'DAMS',
  manufacturer: 'Vendor Name',
  model: 'Model Number',
  tags: [
    'SECTOR_DAMS',
    'EQUIP_TYPE_[TYPE]',
    'FUNCTION_[FUNCTION]',
    'SAFETY_[LEVEL]',
    'OPS_CRITICALITY_[LEVEL]'
  ],
  capacity: 'CFS/MW/GPM',
  installYear: 1975,
  lastInspection: date(),
  createdAt: datetime()
})
-[:LOCATED_AT]->(f:Facility {facilityId: 'DAM-XXX'})
RETURN e;
```

### Update Dam Water Level
```cypher
MATCH (f:Facility {facilityId: 'DAM-XXX'})
SET f.currentElevation_ft = 1250.5,
    f.currentStorage_AF = 45000,
    f.percentFull = 90,
    f.inflowRate_cfs = 5000,
    f.releaseRate_cfs = 3000,
    f.lastUpdate = datetime()
RETURN f;
```

### Record Safety Inspection
```cypher
MATCH (f:Facility {facilityId: 'DAM-XXX'})
CREATE (i:Inspection {
  inspectionId: 'INSP-[DATE]-[TYPE]',
  inspectionType: 'PERIODIC|SPECIAL|EMERGENCY',
  inspectionDate: date(),
  overallCondition: 'SATISFACTORY|FAIR|POOR|UNSATISFACTORY',
  deficiencies: ['list', 'of', 'findings'],
  recommendations: ['corrective', 'actions'],
  nextInspectionDue: date() + duration('P5Y')
})-[:INSPECTED]->(f)
RETURN i, f;
```

---

## 🔗 Related Standards & Compliance

### Regulatory Framework
- **FERC Dam Safety** - Tags: `REG_FERC`
- **USACE Safety Program** - Tags: `REG_USACE`
- **Federal Guidelines** - Tags: `REG_FEMA_GUIDELINES`
- **State Dam Safety** - Tags: `REG_STATE_DAM_SAFETY`
- **EPA Water Quality** - Tags: `REG_EPA_WATER`

### Industry Standards
- **ASDSO Dam Safety Guidelines**
- **ICOLD Standards**
- **USBR Design Standards**
- **FEMA Risk Guidelines**
- **NPDP Inspection Standards**

### Compliance Check Query
```cypher
MATCH (f:Facility)
WHERE f.sector = 'DAMS'
WITH f,
     CASE WHEN f.hasEAP = true THEN 1 ELSE 0 END as HasEAP,
     CASE WHEN f.lastInspection > date() - duration('P5Y') THEN 1 ELSE 0 END as CurrentInspection,
     CASE WHEN 'REG_FERC' IN f.tags THEN 1 ELSE 0 END as FERC,
     CASE WHEN f.hazardClassification IS NOT NULL THEN 1 ELSE 0 END as Classified
RETURN 'Dams Compliance' as Sector,
       sum(HasEAP) as WithEmergencyPlans,
       sum(CurrentInspection) as CurrentInspections,
       sum(FERC) as FERC_Regulated,
       sum(Classified) as Hazard_Classified,
       count(f) as TotalDams;
```

---

## 📁 Deployment Scripts

### Primary Deployment Script
Location: `/home/jim/2_OXOT_Projects_Dev/scripts/universal_location_migration/DAMS_SECTOR_IMPLEMENTATION.cypher`

### Validation Script
```cypher
// Verify Dams sector deployment
MATCH (n)
WHERE n.sector = 'DAMS'
WITH count(n) as totalNodes
MATCH (f:Facility)
WHERE f.sector = 'DAMS'
WITH totalNodes, count(f) as facilities
MATCH (e:Equipment)
WHERE e.sector = 'DAMS'
RETURN 'DAMS' as Sector,
       totalNodes as TotalNodes,
       facilities as Facilities,
       count(e) as Equipment,
       CASE WHEN totalNodes >= 35184 THEN 'PASS' ELSE 'FAIL' END as Status;
```

---

## 🔄 Cross-Sector Dependencies

### Energy
- Hydroelectric power generation
- Grid integration
- Pumped storage
- Black start capability

### Water
- Municipal water supply
- Industrial water
- Irrigation systems
- Water treatment

### Transportation
- Navigation locks
- Barge traffic
- Recreation boating
- Port operations

### Agriculture
- Irrigation water
- Flood protection
- Drought management
- Soil moisture control

---

## 📈 Performance Metrics

### Operational KPIs
- Dam safety rating: >95% satisfactory
- Gate availability: 99.9%
- Turbine efficiency: >90%
- Inspection compliance: 100%
- Emergency plan currency: 100%

### Query Performance
```cypher
// Check query performance for Dams sector
EXPLAIN
MATCH (e:Equipment)
WHERE e.sector = 'DAMS'
  AND 'SAFETY_CRITICAL' IN e.tags
RETURN count(e);
```

---

**Wiki Navigation**: [← Main Index](../00_MAIN_INDEX.md) | [Queries Library](../QUERIES_LIBRARY.md)