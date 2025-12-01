# Commercial Facilities Sector

**Sector Code**: COMMERCIAL_FACILITIES
**Node Count**: 28,000
**Status**: ✅ Operational
**Last Updated**: 2024-11-22

[← Back to Main Index](../00_MAIN_INDEX.md) | [→ Next: Dams Sector](DAMS_SECTOR.md)

---

## 📊 Sector Overview

The Commercial Facilities Sector includes a diverse range of sites that draw large crowds for shopping, business, entertainment, or lodging. This sector encompasses retail, entertainment venues, sports stadiums, convention centers, and other facilities where people congregate.

### Key Statistics
- **Total Nodes**: 28,000
- **Commercial Buildings**: 8,000+ major facilities
- **Entertainment Venues**: 3,000+ stadiums and theaters
- **Retail Centers**: 5,000+ shopping complexes
- **Equipment Systems**: 12,000+ building systems
- **Geographic Coverage**: All 50 states + territories

---

## 🏗️ Node Types Distribution

```cypher
// Get Commercial Facilities sector node distribution
MATCH (n)
WHERE n.sector = 'COMMERCIAL_FACILITIES'
RETURN labels(n) as NodeTypes, count(*) as Count
ORDER BY Count DESC;
```

### Node Distribution
- **Equipment**: 12,000 nodes (HVAC, security, elevators, lighting)
- **Facility**: 8,000 nodes (malls, stadiums, hotels, offices)
- **Device**: 5,000 nodes (cameras, sensors, access controls)
- **Property**: 1,500 nodes (occupancy, events, tenants)
- **Measurement**: 1,500 nodes (visitor counts, energy use, revenue)

---

## 🏭 Subsectors

### Entertainment & Media (25%)
- Sports stadiums
- Concert venues
- Theaters
- Theme parks
- Convention centers

### Retail (30%)
- Shopping malls
- Big box stores
- Outlet centers
- Strip malls
- Department stores

### Lodging (20%)
- Hotels
- Resorts
- Casinos
- Conference centers
- Cruise ships

### Real Estate (15%)
- Office buildings
- Mixed-use developments
- Commercial complexes
- Business parks
- Skyscrapers

### Public Assembly (10%)
- Convention centers
- Exhibition halls
- Museums
- Auditoriums
- Religious facilities

---

## 🔧 Equipment Types

### Critical Equipment Categories
```cypher
// Get Commercial Facilities sector equipment types
MATCH (e:Equipment)
WHERE e.sector = 'COMMERCIAL_FACILITIES'
RETURN e.equipmentType as Type, count(*) as Count
ORDER BY Count DESC
LIMIT 20;
```

### Primary Equipment Types
1. **HVAC Systems** (3,000 units)
   - Central air systems
   - Chillers
   - Boilers
   - Air handlers
   - Tags: `EQUIP_TYPE_HVAC`, `FUNCTION_CLIMATE`

2. **Security Systems** (2,500 units)
   - CCTV systems
   - Access control
   - Intrusion detection
   - Metal detectors
   - Tags: `EQUIP_TYPE_SECURITY`, `OPS_CRITICALITY_HIGH`

3. **Vertical Transportation** (2,000 units)
   - Elevators
   - Escalators
   - Moving walkways
   - Service lifts
   - Tags: `EQUIP_TYPE_ELEVATOR`, `SAFETY_CRITICAL`

4. **Fire & Life Safety** (1,500 units)
   - Fire alarms
   - Sprinkler systems
   - Emergency lighting
   - Smoke control
   - Tags: `EQUIP_TYPE_FIRE_SAFETY`, `FUNCTION_SAFETY`

5. **Building Management** (1,000 units)
   - BMS/BAS systems
   - Energy management
   - Lighting controls
   - Integration platforms
   - Tags: `EQUIP_TYPE_BMS`, `FUNCTION_CONTROL`

---

## 🗺️ Geographic Distribution

```cypher
// Commercial Facilities by state
MATCH (f:Facility)
WHERE f.sector = 'COMMERCIAL_FACILITIES'
RETURN f.state as State, count(*) as Facilities
ORDER BY Facilities DESC;
```

### Major Commercial Infrastructure Locations
- **New York**: Times Square, Madison Square Garden, major hotels
- **Nevada**: Las Vegas casinos, convention centers, resorts
- **California**: Disneyland, Hollywood venues, tech campuses
- **Florida**: Disney World, cruise terminals, beach resorts
- **Texas**: AT&T Stadium, convention centers, mega malls

---

## 🔍 Key Cypher Queries

### 1. Get Major Sports Venues
```cypher
MATCH (f:Facility)
WHERE f.sector = 'COMMERCIAL_FACILITIES'
  AND f.facilityType = 'STADIUM'
  AND f.capacity > 40000
RETURN f.name, f.city, f.capacity, f.primaryUse, f.yearBuilt
ORDER BY f.capacity DESC;
```

### 2. Find Shopping Centers
```cypher
MATCH (f:Facility)
WHERE f.sector = 'COMMERCIAL_FACILITIES'
  AND f.facilityType IN ['MALL', 'SHOPPING_CENTER']
RETURN f.name,
       f.squareFootage,
       f.storeCount,
       f.annualVisitors_M,
       f.state
ORDER BY f.squareFootage DESC;
```

### 3. Hotel and Lodging Analysis
```cypher
MATCH (f:Facility)
WHERE f.sector = 'COMMERCIAL_FACILITIES'
  AND f.facilityType IN ['HOTEL', 'RESORT', 'CASINO']
RETURN f.brandName,
       count(*) as Properties,
       sum(f.roomCount) as TotalRooms,
       avg(f.occupancyRate) as AvgOccupancy
ORDER BY TotalRooms DESC;
```

### 4. Security System Coverage
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'COMMERCIAL_FACILITIES'
  AND 'EQUIP_TYPE_SECURITY' IN e.tags
RETURN e.securityType,
       count(*) as Systems,
       sum(e.cameraCount) as TotalCameras,
       avg(e.coverageArea_sqft) as AvgCoverage
ORDER BY Systems DESC;
```

### 5. Emergency Evacuation Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'COMMERCIAL_FACILITIES'
  AND ('EVACUATION' IN e.tags OR e.function = 'EMERGENCY_EXIT')
RETURN e.facilityType,
       e.evacuationType,
       avg(e.evacuationTime_min) as AvgEvacTime,
       count(*) as Systems
ORDER BY AvgEvacTime;
```

### 6. Entertainment Venue Technology
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'COMMERCIAL_FACILITIES'
  AND e.venueType IN ['THEATER', 'CONCERT_HALL', 'ARENA']
RETURN e.technologyType,
       e.capability,
       count(*) as Installations,
       avg(e.capacity) as AvgCapacity
ORDER BY Installations DESC;
```

### 7. Building Energy Management
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'COMMERCIAL_FACILITIES'
  AND 'FUNCTION_ENERGY' IN e.tags
RETURN e.buildingType,
       avg(e.energyIntensity_kWh_sqft) as AvgEnergyUse,
       sum(e.annualSavings_kWh) as TotalSavings,
       count(*) as Buildings
ORDER BY TotalSavings DESC;
```

### 8. Crowd Management Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'COMMERCIAL_FACILITIES'
  AND ('CROWD_CONTROL' IN e.tags OR e.function = 'PEOPLE_COUNTING')
RETURN e.systemType,
       e.venue,
       e.maxCapacity,
       e.realTimeTracking
ORDER BY e.maxCapacity DESC;
```

### 9. Point of Sale Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'COMMERCIAL_FACILITIES'
  AND e.equipmentType = 'POS_SYSTEM'
RETURN e.retailer,
       count(*) as POSTerminals,
       sum(e.dailyTransactions) as TotalTransactions,
       avg(e.transactionTime_sec) as AvgTransTime
ORDER BY TotalTransactions DESC;
```

### 10. Convention Center Infrastructure
```cypher
MATCH (f:Facility)
WHERE f.sector = 'COMMERCIAL_FACILITIES'
  AND f.facilityType = 'CONVENTION_CENTER'
RETURN f.name,
       f.exhibitSpace_sqft,
       f.meetingRooms,
       f.annualEvents,
       f.economicImpact_M
ORDER BY f.exhibitSpace_sqft DESC;
```

### 11. Smart Building Systems
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'COMMERCIAL_FACILITIES'
  AND ('SMART_BUILDING' IN e.tags OR 'IOT' IN e.tags)
RETURN e.buildingName,
       e.smartSystemType,
       count(*) as ConnectedDevices,
       e.automationLevel
ORDER BY ConnectedDevices DESC;
```

### 12. Food Service Equipment
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'COMMERCIAL_FACILITIES'
  AND e.category = 'FOOD_SERVICE'
RETURN e.venueType,
       e.kitchenType,
       count(*) as KitchenEquipment,
       sum(e.mealCapacity) as TotalMealCapacity
ORDER BY TotalMealCapacity DESC;
```

---

## 🛠️ Update Procedures

### Add New Commercial Facility
```cypher
CREATE (f:Facility {
  facilityId: 'COMM-FAC-[TYPE]-[STATE]-[NUMBER]',
  name: 'Facility Name',
  facilityType: 'MALL|STADIUM|HOTEL|OFFICE|etc',
  sector: 'COMMERCIAL_FACILITIES',
  state: 'STATE_CODE',
  city: 'City Name',
  squareFootage: 500000,
  capacity: 50000,
  yearBuilt: 2020,
  latitude: 0.0,
  longitude: 0.0,
  createdAt: datetime()
})
RETURN f;
```

### Add Building Equipment
```cypher
CREATE (e:Equipment {
  equipmentId: 'EQ-COMM-[TYPE]-[FACILITY]-[NUMBER]',
  equipmentType: 'HVAC|Security|Elevator|Fire|etc',
  sector: 'COMMERCIAL_FACILITIES',
  manufacturer: 'Vendor Name',
  model: 'Model Number',
  tags: [
    'SECTOR_COMMERCIAL_FACILITIES',
    'EQUIP_TYPE_[TYPE]',
    'FUNCTION_[FUNCTION]',
    'BUILDING_[TYPE]',
    'OPS_CRITICALITY_[LEVEL]'
  ],
  capacity: 'Tons/People/GPM',
  serviceArea_sqft: 10000,
  installDate: date(),
  createdAt: datetime()
})
-[:LOCATED_AT]->(f:Facility {facilityId: 'FACILITY_ID'})
RETURN e;
```

### Update Occupancy Status
```cypher
MATCH (f:Facility {facilityId: 'COMM-FAC-XXX'})
SET f.currentOccupancy = 2500,
    f.occupancyRate = 0.75,
    f.lastUpdate = datetime(),
    f.peakOccupancy = 3000,
    f.eventStatus = 'ACTIVE'
RETURN f;
```

### Create Tenant Relationship
```cypher
MATCH (f:Facility {facilityId: 'COMM-FAC-XXX'})
CREATE (t:Tenant {
  tenantId: 'TENANT-[NAME]-[NUMBER]',
  tenantName: 'Business Name',
  businessType: 'Retail|Restaurant|Office',
  leaseArea_sqft: 5000,
  leaseStart: date(),
  leaseEnd: date() + duration('P3Y')
})-[:LEASES_SPACE_IN]->(f)
RETURN t, f;
```

---

## 🔗 Related Standards & Compliance

### Regulatory Framework
- **ADA Compliance** - Tags: `REG_ADA`
- **OSHA Safety Standards** - Tags: `REG_OSHA`
- **Fire Codes (NFPA)** - Tags: `REG_NFPA`
- **Building Codes (IBC)** - Tags: `REG_IBC`
- **Energy Codes (IECC)** - Tags: `REG_IECC`

### Industry Standards
- **LEED Certification**
- **BOMA Standards**
- **ASHRAE Standards**
- **UL Safety Standards**
- **Energy Star**

### Compliance Check Query
```cypher
MATCH (e:Equipment)
WHERE e.sector = 'COMMERCIAL_FACILITIES'
WITH e,
     CASE WHEN 'REG_ADA' IN e.tags THEN 1 ELSE 0 END as ADA,
     CASE WHEN 'REG_NFPA' IN e.tags THEN 1 ELSE 0 END as NFPA,
     CASE WHEN 'REG_IBC' IN e.tags THEN 1 ELSE 0 END as IBC,
     CASE WHEN 'LEED_CERTIFIED' IN e.tags THEN 1 ELSE 0 END as LEED
RETURN 'Commercial Facilities Compliance' as Sector,
       sum(ADA) as ADA_Compliant,
       sum(NFPA) as Fire_Code_Compliant,
       sum(IBC) as Building_Code_Compliant,
       sum(LEED) as LEED_Certified,
       count(e) as TotalEquipment;
```

---

## 📁 Deployment Scripts

### Primary Deployment Script
Location: `/home/jim/2_OXOT_Projects_Dev/scripts/universal_location_migration/COMMERCIAL_FACILITIES_SECTOR_IMPLEMENTATION.cypher`

### Validation Script
```cypher
// Verify Commercial Facilities sector deployment
MATCH (n)
WHERE n.sector = 'COMMERCIAL_FACILITIES'
WITH count(n) as totalNodes
MATCH (f:Facility)
WHERE f.sector = 'COMMERCIAL_FACILITIES'
WITH totalNodes, count(f) as facilities
MATCH (e:Equipment)
WHERE e.sector = 'COMMERCIAL_FACILITIES'
RETURN 'COMMERCIAL_FACILITIES' as Sector,
       totalNodes as TotalNodes,
       facilities as Facilities,
       count(e) as Equipment,
       CASE WHEN totalNodes >= 28000 THEN 'PASS' ELSE 'FAIL' END as Status;
```

---

## 🔄 Cross-Sector Dependencies

### Energy
- Power for facilities
- HVAC operations
- Lighting systems
- Backup generators

### Communications
- WiFi and cellular
- Security communications
- POS networks
- Guest services

### Emergency Services
- Fire response
- Medical emergencies
- Security incidents
- Evacuation coordination

### Transportation
- Parking facilities
- Public transit access
- Delivery logistics
- Guest transportation

---

## 📈 Performance Metrics

### Operational KPIs
- Facility uptime: 99.5%
- Security incident response: <3 minutes
- HVAC comfort compliance: 95%
- Energy efficiency: 15% reduction target
- Customer satisfaction: >4.5/5

### Query Performance
```cypher
// Check query performance for Commercial Facilities sector
EXPLAIN
MATCH (e:Equipment)
WHERE e.sector = 'COMMERCIAL_FACILITIES'
  AND 'EQUIP_TYPE_SECURITY' IN e.tags
RETURN count(e);
```

---

**Wiki Navigation**: [← Main Index](../00_MAIN_INDEX.md) | [→ Dams Sector](DAMS_SECTOR.md) | [Queries Library](../QUERIES_LIBRARY.md)