# Chemical Sector

**Sector Code**: CHEMICAL
**Node Count**: 32,200
**Status**: ✅ Operational
**Last Updated**: 2024-11-22

[← Back to Main Index](../00_MAIN_INDEX.md) | [→ Next: Critical Manufacturing Sector](CRITICAL_MANUFACTURING_SECTOR.md)

---

## 📊 Sector Overview

The Chemical Sector manufactures, stores, and distributes chemicals essential to other critical infrastructure sectors. This includes basic chemicals, specialty chemicals, agricultural chemicals, pharmaceuticals, and consumer products.

### Key Statistics
- **Total Nodes**: 32,200
- **Chemical Plants**: 3,000+ facilities
- **Storage Facilities**: 2,500+ sites
- **Equipment**: 15,000+ critical systems
- **Pipeline Miles**: 25,000+ miles
- **Geographic Coverage**: All 50 states

---

## 🏗️ Node Types Distribution

```cypher
// Get Chemical sector node distribution
MATCH (n)
WHERE n.sector = 'CHEMICAL'
RETURN labels(n) as NodeTypes, count(*) as Count
ORDER BY Count DESC;
```

### Node Distribution
- **Equipment**: 15,000 nodes (reactors, storage tanks, processing units)
- **Facility**: 3,000 nodes (plants, warehouses, terminals)
- **Device**: 8,000 nodes (sensors, valves, controllers)
- **Property**: 3,200 nodes (chemical properties, safety data)
- **Measurement**: 3,000 nodes (pressure, temperature, flow rates)

---

## 🏭 Subsectors

### Basic Chemicals (35%)
- Petrochemicals
- Industrial gases
- Synthetic dyes
- Pigments
- Alkalies and chlorine

### Specialty Chemicals (30%)
- Adhesives and sealants
- Catalysts
- Coatings
- Electronic chemicals
- Water treatment chemicals

### Agricultural Chemicals (20%)
- Fertilizers
- Pesticides
- Herbicides
- Growth regulators
- Soil conditioners

### Consumer Products (15%)
- Soaps and detergents
- Cosmetics
- Paints
- Cleaning products
- Personal care products

---

## 🔧 Equipment Types

### Critical Equipment Categories
```cypher
// Get Chemical sector equipment types
MATCH (e:Equipment)
WHERE e.sector = 'CHEMICAL'
RETURN e.equipmentType as Type, count(*) as Count
ORDER BY Count DESC
LIMIT 20;
```

### Primary Equipment Types
1. **Chemical Reactors** (2,000 units)
   - Batch reactors
   - Continuous flow reactors
   - Catalytic reactors
   - Polymerization reactors
   - Tags: `EQUIP_TYPE_REACTOR`, `OPS_CRITICALITY_CRITICAL`

2. **Storage Tanks** (3,500 units)
   - Atmospheric tanks
   - Pressure vessels
   - Cryogenic tanks
   - Underground storage
   - Tags: `EQUIP_TYPE_STORAGE`, `FUNCTION_CONTAINMENT`

3. **Process Control Systems** (1,500 units)
   - DCS systems
   - SCADA systems
   - Safety instrumented systems
   - Emergency shutdown systems
   - Tags: `EQUIP_TYPE_CONTROL`, `SAFETY_CRITICAL`

4. **Distillation Columns** (1,000 units)
   - Fractionation columns
   - Stripping columns
   - Absorption columns
   - Tags: `EQUIP_TYPE_DISTILLATION`, `FUNCTION_SEPARATION`

5. **Safety Systems** (2,000 units)
   - Gas detection systems
   - Fire suppression
   - Pressure relief valves
   - Containment systems
   - Tags: `EQUIP_TYPE_SAFETY`, `REG_EPA_RMP`

---

## 🗺️ Geographic Distribution

```cypher
// Chemical facilities by state
MATCH (f:Facility)
WHERE f.sector = 'CHEMICAL'
RETURN f.state as State, count(*) as Facilities
ORDER BY Facilities DESC;
```

### Major Chemical Infrastructure Locations
- **Texas**: Houston Ship Channel, Gulf Coast petrochemicals
- **Louisiana**: Mississippi River chemical corridor
- **New Jersey**: Pharmaceutical and specialty chemicals
- **Ohio**: Polymer and plastic production
- **Illinois**: Industrial chemicals and refining

---

## 🔍 Key Cypher Queries

### 1. Get All Chemical Plants
```cypher
MATCH (f:Facility)
WHERE f.sector = 'CHEMICAL'
  AND f.facilityType = 'CHEMICAL_PLANT'
RETURN f.facilityId, f.name, f.state, f.city, f.productTypes
ORDER BY f.state, f.city;
```

### 2. Find High-Risk Chemical Storage
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'CHEMICAL'
  AND e.equipmentType CONTAINS 'Storage'
  AND ('HAZMAT_CLASS_1' IN e.tags OR 'HAZMAT_TOXIC' IN e.tags)
RETURN e.equipmentId, e.chemicalStored, e.capacity, e.hazardClass
ORDER BY e.capacity DESC;
```

### 3. EPA RMP Regulated Facilities
```cypher
MATCH (f:Facility)
WHERE f.sector = 'CHEMICAL'
  AND 'REG_EPA_RMP' IN f.tags
RETURN f.name, f.rmpId, f.worstCaseRadius, f.alternateRadius
ORDER BY f.worstCaseRadius DESC;
```

### 4. Process Safety Management Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'CHEMICAL'
  AND 'REG_OSHA_PSM' IN e.tags
RETURN e.equipmentType,
       e.psmElement,
       count(*) as PSMEquipment
ORDER BY PSMEquipment DESC;
```

### 5. Cross-Sector Chemical Distribution
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'CHEMICAL'
  AND ANY(tag IN e.tags WHERE tag STARTS WITH 'SUPPLIES_SECTOR_')
RETURN e.chemicalType,
       [tag IN e.tags WHERE tag STARTS WITH 'SUPPLIES_'] as suppliesSectors,
       count(*) as instances
ORDER BY instances DESC;
```

### 6. Chemical Transportation Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'CHEMICAL'
  AND (e.equipmentType CONTAINS 'Pipeline'
       OR e.equipmentType CONTAINS 'Rail'
       OR e.equipmentType CONTAINS 'Tank')
RETURN e.equipmentType,
       e.transportMode,
       e.hazmatClass,
       count(*) as Systems
ORDER BY Systems DESC;
```

### 7. Emergency Response Equipment
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'CHEMICAL'
  AND ('FUNCTION_EMERGENCY' IN e.tags
       OR e.equipmentType CONTAINS 'Safety'
       OR e.equipmentType CONTAINS 'Shutdown')
RETURN e.equipmentType,
       e.responseTime,
       count(*) as Units
ORDER BY Units DESC;
```

### 8. Chemical Process Monitoring
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'CHEMICAL'
  AND 'FUNCTION_MONITORING' IN e.tags
RETURN e.equipmentType,
       e.parameterMonitored,
       e.alarmLimits,
       count(*) as Sensors
ORDER BY Sensors DESC;
```

### 9. Waste Treatment Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'CHEMICAL'
  AND (e.equipmentType CONTAINS 'Waste'
       OR 'FUNCTION_WASTE_TREATMENT' IN e.tags)
RETURN e.equipmentType,
       e.treatmentMethod,
       e.capacity,
       count(*) as Systems
ORDER BY Systems DESC;
```

### 10. Chemical Inventory Tracking
```cypher
MATCH (f:Facility)
WHERE f.sector = 'CHEMICAL'
OPTIONAL MATCH (i:ChemicalInventory)-[:STORED_AT]->(f)
RETURN f.name as Facility,
       count(DISTINCT i.chemicalName) as ChemicalTypes,
       sum(i.quantity) as TotalInventory,
       max(i.hazardLevel) as MaxHazardLevel
ORDER BY TotalInventory DESC;
```

### 11. Cybersecurity for Chemical ICS
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'CHEMICAL'
  AND (e.equipmentType CONTAINS 'SCADA'
       OR e.equipmentType CONTAINS 'DCS'
       OR 'EQUIP_TYPE_CONTROL' IN e.tags)
OPTIONAL MATCH (cve:CVE)-[:AFFECTS]->(e)
RETURN e.equipmentType,
       count(DISTINCT e) as ControlSystems,
       count(DISTINCT cve) as Vulnerabilities,
       max(cve.baseScore) as MaxCVSS
ORDER BY Vulnerabilities DESC;
```

### 12. Chemical Supply Chain
```cypher
MATCH (source:Facility)
WHERE source.sector = 'CHEMICAL'
OPTIONAL MATCH (source)-[:SUPPLIES]->(dest:Facility)
RETURN source.name as ChemicalSupplier,
       dest.sector as CustomerSector,
       count(dest) as Customers
ORDER BY Customers DESC
LIMIT 20;
```

---

## 🛠️ Update Procedures

### Add New Chemical Plant
```cypher
CREATE (f:Facility {
  facilityId: 'CHEM-PLANT-[STATE]-[NUMBER]',
  name: 'Plant Name',
  facilityType: 'CHEMICAL_PLANT',
  sector: 'CHEMICAL',
  state: 'STATE_CODE',
  city: 'City Name',
  productTypes: ['Basic', 'Specialty', 'Agricultural'],
  rmpId: 'RMP-NUMBER',
  tierIIReporting: true,
  latitude: 0.0,
  longitude: 0.0,
  createdAt: datetime()
})
RETURN f;
```

### Add Chemical Equipment
```cypher
CREATE (e:Equipment {
  equipmentId: 'EQ-CHEM-[TYPE]-[STATE]-[NUMBER]',
  equipmentType: 'Reactor|Tank|Column|etc',
  sector: 'CHEMICAL',
  manufacturer: 'Vendor Name',
  model: 'Model Number',
  capacity: 'Volume/Flow rate',
  tags: [
    'SECTOR_CHEMICAL',
    'EQUIP_TYPE_[TYPE]',
    'FUNCTION_[FUNCTION]',
    'REG_EPA_RMP',
    'REG_OSHA_PSM',
    'HAZMAT_CLASS_[1-9]',
    'OPS_CRITICALITY_CRITICAL'
  ],
  installDate: date(),
  lastInspection: date(),
  createdAt: datetime()
})
-[:LOCATED_AT]->(f:Facility {facilityId: 'FACILITY_ID'})
RETURN e;
```

### Update Safety System Status
```cypher
MATCH (e:Equipment {equipmentId: 'EQ-CHEM-XXX'})
WHERE 'EQUIP_TYPE_SAFETY' IN e.tags
SET e.lastTestDate = date(),
    e.testResult = 'PASS|FAIL',
    e.nextTestDue = date() + duration('P90D'),
    e.updatedAt = datetime()
RETURN e;
```

---

## 🔗 Related Standards & Compliance

### Regulatory Framework
- **EPA Risk Management Program (RMP)** - Tags: `REG_EPA_RMP`
- **OSHA Process Safety Management (PSM)** - Tags: `REG_OSHA_PSM`
- **DHS Chemical Facility Anti-Terrorism Standards (CFATS)** - Tags: `REG_DHS_CFATS`
- **EPA Tier II Reporting** - Tags: `REG_EPA_TIER_II`
- **DOT Hazmat Transportation** - Tags: `REG_DOT_HAZMAT`

### Industry Standards
- **American Chemistry Council Responsible Care**
- **ISO 14001 Environmental Management**
- **API Standards for Chemical Equipment**
- **NFPA Fire and Chemical Safety Codes**

### Compliance Check Query
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'CHEMICAL'
WITH e,
     CASE WHEN 'REG_EPA_RMP' IN e.tags THEN 1 ELSE 0 END as RMP,
     CASE WHEN 'REG_OSHA_PSM' IN e.tags THEN 1 ELSE 0 END as PSM,
     CASE WHEN 'REG_DHS_CFATS' IN e.tags THEN 1 ELSE 0 END as CFATS,
     CASE WHEN 'REG_DOT_HAZMAT' IN e.tags THEN 1 ELSE 0 END as DOT
RETURN 'Chemical Compliance' as Sector,
       sum(RMP) as EPA_RMP_Compliant,
       sum(PSM) as OSHA_PSM_Compliant,
       sum(CFATS) as DHS_CFATS_Compliant,
       sum(DOT) as DOT_Hazmat_Compliant,
       count(e) as TotalEquipment;
```

---

## 📁 Deployment Scripts

### Primary Deployment Script
Location: `/home/jim/2_OXOT_Projects_Dev/scripts/universal_location_migration/CHEMICAL_SECTOR_IMPLEMENTATION.cypher`

### Validation Script
```cypher
// Verify Chemical sector deployment
MATCH (n)
WHERE n.sector = 'CHEMICAL'
WITH count(n) as totalNodes
MATCH (f:Facility)
WHERE f.sector = 'CHEMICAL'
WITH totalNodes, count(f) as facilities
MATCH (e:Equipment)
WHERE e.sector = 'CHEMICAL'
RETURN 'CHEMICAL' as Sector,
       totalNodes as TotalNodes,
       facilities as Facilities,
       count(e) as Equipment,
       CASE WHEN totalNodes >= 32200 THEN 'PASS' ELSE 'FAIL' END as Status;
```

---

## 🔄 Cross-Sector Dependencies

### Energy Sector
- Power for chemical processes
- Natural gas feedstock
- Steam generation
- Cogeneration facilities

### Transportation
- Pipeline networks
- Rail tank cars
- Tank trucks
- Marine vessels

### Water Sector
- Process water supply
- Cooling water
- Wastewater treatment
- Steam generation

### Manufacturing
- Chemical inputs for production
- Industrial gases
- Specialty chemicals
- Coatings and adhesives

---

## 📈 Performance Metrics

### Operational KPIs
- Safety incident rate: <0.5 per 200,000 hours
- Process uptime: 95%
- RMP compliance: 100%
- Emergency response time: <10 minutes
- Environmental compliance: 99.9%

### Query Performance
```cypher
// Check query performance for Chemical sector
EXPLAIN
MATCH (e:Equipment)
WHERE e.sector = 'CHEMICAL'
  AND 'REG_EPA_RMP' IN e.tags
RETURN count(e);
```

---

**Wiki Navigation**: [← Main Index](../00_MAIN_INDEX.md) | [→ Critical Manufacturing](CRITICAL_MANUFACTURING_SECTOR.md) | [Queries Library](../QUERIES_LIBRARY.md)