# Energy Sector

**Sector Code**: ENERGY
**Node Count**: 35,475
**Status**: ✅ Operational
**Last Updated**: 2024-11-22

[← Water Sector](WATER_SECTOR.md) | [← Main Index](../00_MAIN_INDEX.md) | [→ Healthcare Sector](HEALTHCARE_SECTOR.md)

---

## 📊 Sector Overview

The Energy Sector encompasses electricity generation, transmission, and distribution systems, as well as oil and natural gas infrastructure. This critical sector powers all other infrastructure sectors.

### Key Statistics
- **Total Nodes**: 35,475
- **Facilities**: 35 major facilities
- **Equipment**: 350+ critical systems
- **Geographic Coverage**: All 50 states
- **Generation Capacity**: Represents major US grid

---

## 🏗️ Node Types Distribution

```cypher
// Get Energy sector node distribution
MATCH (n)
WHERE n.sector = 'ENERGY'
RETURN labels(n) as NodeTypes, count(*) as Count
ORDER BY Count DESC;
```

### Estimated Distribution
- **Equipment**: 350 nodes (generators, transformers, control systems)
- **Facility**: 35 nodes (power plants, substations, control centers)
- **Device**: 17,500 nodes (smart meters, sensors, RTUs)
- **Property**: 8,850 nodes (configurations, settings)
- **Measurement**: 8,740 nodes (voltage, frequency, power quality)

---

## 🏭 Subsectors

### Power Generation (40%)
- Nuclear power plants
- Coal-fired plants
- Natural gas plants
- Renewable energy (solar, wind, hydro)

### Transmission (25%)
- High-voltage transmission lines
- Transmission substations
- Grid interconnections
- HVDC systems

### Distribution (25%)
- Distribution substations
- Local distribution networks
- Smart grid infrastructure
- Microgrids

### Oil & Gas (10%)
- Refineries
- Pipelines
- Storage facilities
- LNG terminals

---

## 🔧 Equipment Types

### Critical Equipment Categories
```cypher
// Get Energy sector equipment types
MATCH (e:Equipment)
WHERE e.sector = 'ENERGY'
RETURN e.equipmentType as Type, count(*) as Count
ORDER BY Count DESC
LIMIT 20;
```

### Primary Equipment Types
1. **Generators** (40 units)
   - Steam turbines
   - Gas turbines
   - Nuclear reactors
   - Solar panels
   - Wind turbines
   - Tags: `EQUIP_TYPE_GENERATOR`, `FUNCTION_POWER_GENERATION`

2. **Transformers** (40 units)
   - Step-up transformers
   - Step-down transformers
   - Distribution transformers
   - Tags: `EQUIP_TYPE_TRANSFORMER`, `FUNCTION_VOLTAGE_CONVERSION`

3. **Control Systems** (35 units)
   - SCADA systems
   - Energy Management Systems (EMS)
   - Distribution Management Systems (DMS)
   - Tags: `EQUIP_TYPE_CONTROL_SYSTEM`, `OPS_CRITICALITY_CRITICAL`

4. **Protection Equipment** (30 units)
   - Circuit breakers
   - Relays
   - Surge arresters
   - Tags: `EQUIP_TYPE_PROTECTION`, `FUNCTION_GRID_PROTECTION`

---

## 🗺️ Geographic Distribution

```cypher
// Energy facilities by state
MATCH (f:Facility)
WHERE f.sector = 'ENERGY'
RETURN f.state as State, count(*) as Facilities
ORDER BY Facilities DESC;
```

### Major Energy Infrastructure Locations
- **Texas**: ERCOT grid, wind farms, refineries
- **California**: Solar farms, natural gas plants, grid operators
- **Pennsylvania**: Nuclear plants, coal plants, Marcellus shale
- **Illinois**: Nuclear fleet, coal plants, grid interconnections
- **New York**: Hydroelectric (Niagara), Indian Point, NYC grid

---

## 🔍 Key Cypher Queries

### 1. Get All Power Plants
```cypher
MATCH (f:Facility)
WHERE f.sector = 'ENERGY'
  AND f.facilityType IN ['POWER_PLANT', 'GENERATION_FACILITY']
RETURN f.facilityId, f.name, f.state, f.facilityType
ORDER BY f.state;
```

### 2. Find Critical Energy Infrastructure
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'ENERGY'
  AND 'OPS_CRITICALITY_CRITICAL' IN e.tags
RETURN e.equipmentId, e.equipmentType,
       [tag IN e.tags WHERE tag STARTS WITH 'SUBSECTOR_'] as subsector
LIMIT 50;
```

### 3. Grid Control Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'ENERGY'
  AND (e.equipmentType CONTAINS 'SCADA'
       OR e.equipmentType CONTAINS 'EMS'
       OR 'FUNCTION_GRID_CONTROL' IN e.tags)
RETURN e.equipmentId, e.equipmentType, e.tags;
```

### 4. Renewable Energy Equipment
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'ENERGY'
  AND ANY(tag IN e.tags WHERE tag IN ['SUBSECTOR_RENEWABLE', 'SUBSECTOR_SOLAR', 'SUBSECTOR_WIND'])
RETURN e.equipmentType,
       [tag IN e.tags WHERE tag STARTS WITH 'SUBSECTOR_'] as subsectors,
       count(*) as count
ORDER BY count DESC;
```

### 5. Energy Sector Vulnerabilities
```cypher
MATCH (cve:CVE)-[:AFFECTS]->(e:Equipment)
WHERE e.sector = 'ENERGY'
  AND cve.baseScore >= 7.0
RETURN cve.id as CVE,
       cve.baseScore as Score,
       e.equipmentType as AffectedType,
       count(e) as AffectedCount
ORDER BY Score DESC, AffectedCount DESC
LIMIT 25;
```

### 6. Transmission Infrastructure
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'ENERGY'
  AND ('SUBSECTOR_TRANSMISSION' IN e.tags
       OR e.equipmentType CONTAINS 'Transmission')
RETURN e.equipmentType,
       e.facilityId,
       [tag IN e.tags WHERE tag STARTS WITH 'TECH_'] as technologies
ORDER BY e.equipmentType;
```

### 7. Energy Grid Compliance
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'ENERGY'
  AND ANY(tag IN e.tags WHERE tag STARTS WITH 'REG_')
WITH e, [tag IN e.tags WHERE tag STARTS WITH 'REG_'] as regulations
RETURN e.equipmentType,
       regulations,
       count(*) as compliantEquipment
ORDER BY size(regulations) DESC, compliantEquipment DESC;
```

### 8. Smart Grid Components
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'ENERGY'
  AND ANY(tag IN e.tags WHERE tag CONTAINS 'SMART' OR tag CONTAINS 'AMI')
RETURN e.equipmentType,
       e.tags,
       count(*) as smartDevices
ORDER BY smartDevices DESC;
```

### 9. Critical Generation Capacity
```cypher
MATCH (f:Facility)
WHERE f.sector = 'ENERGY'
  AND f.facilityType = 'POWER_PLANT'
OPTIONAL MATCH (e:Equipment)-[:LOCATED_AT]->(f)
WHERE e.equipmentType CONTAINS 'Generator'
RETURN f.name as PowerPlant,
       f.state as State,
       count(e) as GeneratorCount,
       collect(DISTINCT e.equipmentType) as GeneratorTypes
ORDER BY GeneratorCount DESC;
```

### 10. Grid Interconnections
```cypher
MATCH (e1:Equipment)-[:CONNECTS_TO]->(e2:Equipment)
WHERE e1.sector = 'ENERGY' AND e2.sector = 'ENERGY'
  AND e1.facilityId <> e2.facilityId
RETURN e1.facilityId as Facility1,
       e2.facilityId as Facility2,
       count(*) as Connections
ORDER BY Connections DESC
LIMIT 20;
```

---

## 🛠️ Update Procedures

### Add New Power Plant
```cypher
CREATE (f:Facility {
  facilityId: 'ENERGY-PWR-[STATE]-[NUMBER]',
  name: 'Plant Name Power Plant',
  facilityType: 'POWER_PLANT',
  sector: 'ENERGY',
  state: 'STATE_CODE',
  city: 'City Name',
  capacity: 'MW value',
  fuelType: 'Nuclear|Coal|Gas|Solar|Wind',
  latitude: 0.0,
  longitude: 0.0,
  createdAt: datetime()
})
RETURN f;
```

### Add Energy Equipment
```cypher
CREATE (e:Equipment {
  equipmentId: 'EQ-ENERGY-[TYPE]-[STATE]-[NUMBER]',
  equipmentType: 'Generator|Transformer|Control',
  sector: 'ENERGY',
  manufacturer: 'Vendor Name',
  model: 'Model Number',
  tags: [
    'SECTOR_ENERGY',
    'EQUIP_TYPE_[TYPE]',
    'FUNCTION_[FUNCTION]',
    'VENDOR_[NAME]',
    'OPS_CRITICALITY_[LEVEL]',
    'REG_NERC_CIP',
    'SUBSECTOR_[GENERATION|TRANSMISSION|DISTRIBUTION]'
  ],
  capacity: 'MW|MVA value',
  voltage: 'kV value',
  installDate: date(),
  createdAt: datetime()
})
-[:LOCATED_AT]->(f:Facility {facilityId: 'FACILITY_ID'})
RETURN e;
```

### Update Grid Status
```cypher
MATCH (e:Equipment {equipmentId: 'EQ-ENERGY-XXX'})
SET e.gridStatus = 'ONLINE|OFFLINE|MAINTENANCE',
    e.lastSync = datetime(),
    e.frequency = 60.0,
    e.voltage = 'actual_voltage',
    e.updatedAt = datetime()
RETURN e;
```

---

## 🔗 Related Standards & Compliance

### Regulatory Framework
- **NERC CIP Standards** - Tags: `REG_NERC_CIP`
- **FERC Orders** - Tags: `REG_FERC`
- **EPA Clean Power Plan** - Tags: `REG_EPA_POWER`
- **IEEE Standards** - Tags: `STANDARD_IEEE_[NUMBER]`
- **IEC 61850** - Tags: `STANDARD_IEC61850`

### Grid Security Standards
- **NERC CIP-002 through CIP-014**
- **DOE C2M2 (Cybersecurity Capability Maturity Model)**
- **NIST Framework for Grid Cybersecurity**

### Compliance Check Query
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'ENERGY'
WITH e,
     CASE WHEN 'REG_NERC_CIP' IN e.tags THEN 1 ELSE 0 END as NERC,
     CASE WHEN 'REG_FERC' IN e.tags THEN 1 ELSE 0 END as FERC,
     CASE WHEN 'STANDARD_IEEE' IN e.tags THEN 1 ELSE 0 END as IEEE,
     CASE WHEN 'STANDARD_IEC61850' IN e.tags THEN 1 ELSE 0 END as IEC
RETURN 'Energy Compliance' as Sector,
       sum(NERC) as NERC_Compliant,
       sum(FERC) as FERC_Compliant,
       sum(IEEE) as IEEE_Compliant,
       sum(IEC) as IEC61850_Compliant,
       count(e) as TotalEquipment;
```

---

## 📁 Deployment Scripts

### Primary Deployment Script
Location: `/home/jim/2_OXOT_Projects_Dev/scripts/deploy_energy_expansion_sector.cypher`

### Validation Script
```cypher
// Verify Energy sector deployment
MATCH (n)
WHERE n.sector = 'ENERGY'
WITH count(n) as totalNodes
MATCH (f:Facility)
WHERE f.sector = 'ENERGY'
WITH totalNodes, count(f) as facilities
MATCH (e:Equipment)
WHERE e.sector = 'ENERGY'
RETURN 'ENERGY' as Sector,
       totalNodes as TotalNodes,
       facilities as Facilities,
       count(e) as Equipment,
       CASE WHEN totalNodes >= 35000 THEN 'PASS' ELSE 'FAIL' END as Status;
```

---

## 🔄 Cross-Sector Dependencies

### Water Sector
- Power for water treatment plants
- Cooling water for power plants
- Hydroelectric generation

### Communications
- SCADA communications
- Smart grid networks
- Remote monitoring systems

### Transportation
- Fuel transportation (coal, oil, gas)
- Electric vehicle charging infrastructure
- Pipeline operations

### Critical Manufacturing
- Power for manufacturing facilities
- Industrial load management
- Cogeneration facilities

---

## 📈 Performance Metrics

### Operational KPIs
- Grid reliability: 99.98% uptime
- Frequency stability: 60Hz ± 0.05Hz
- Voltage stability: ±5% nominal
- Response time: <4 seconds for frequency events

### Resilience Metrics
- N-1 contingency coverage: 100%
- Black start capability: Major regions
- Restoration time: <24 hours for 95% load
- Cybersecurity maturity: Level 3+ (C2M2)

---

**Wiki Navigation**: [← Water](WATER_SECTOR.md) | [← Main Index](../00_MAIN_INDEX.md) | [→ Healthcare](HEALTHCARE_SECTOR.md)