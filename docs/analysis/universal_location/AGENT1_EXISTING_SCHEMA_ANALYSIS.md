# Equipment and Location Schema Analysis Report

**Analysis Date**: 2025-11-13
**Analyst**: Agent 1 - Schema Pattern Analysis
**Project**: OXOT Universal Location Architecture

---

## 1. Current Equipment Node Properties

### Device Node (ICS/SCADA Equipment, IT Hardware)
**Label**: `Device`

**Properties Identified**:
- `id`: UUID (unique identifier)
- `name`: string (human-readable name)
- `manufacturer`: string (equipment manufacturer)
- `model`: string (model designation)
- `serialNumber`: string (physical serial number)
- `cpe`: string (Common Platform Enumeration for vulnerability matching)
- `firmwareVersion`: string (firmware/software version)
- `criticalityLevel`: enum [LOW, MEDIUM, HIGH, CRITICAL]
- `deviceType`: enum [PLC, HMI, RTU, SCADA_SERVER, WORKSTATION, SENSOR, ACTUATOR, NETWORK_SWITCH, FIREWALL]
- `customer_namespace`: string (multi-tenant isolation)
- `is_shared`: boolean (industry model vs customer-specific)
- `installation_date`: date (commissioning date)
- `last_maintenance`: date (maintenance tracking)

**Source**: `/schemas/neo4j/01_layer_physical_asset.cypher` lines 32-48

### HardwareComponent Node (Modules, Cards, Interfaces)
**Label**: `HardwareComponent`

**Properties Identified**:
- `id`: UUID
- `name`: string
- `componentType`: enum [CPU_MODULE, IO_MODULE, COMMUNICATION_MODULE, POWER_SUPPLY, NETWORK_CARD, SENSOR, ACTUATOR]
- `manufacturer`: string
- `partNumber`: string
- `cpe`: string
- `firmwareVersion`: string
- `interface_type`: string (e.g., "Profibus", "Modbus TCP", "Ethernet/IP")

**Source**: `/schemas/neo4j/01_layer_physical_asset.cypher` lines 66-77

### PhysicalAsset Node (Top-Level Container)
**Label**: `PhysicalAsset`

**Properties Identified**:
- `id`: UUID
- `name`: string
- `type`: enum [BUILDING, VEHICLE, FACILITY, INFRASTRUCTURE, FLEET]
- `customer_namespace`: string
- `is_shared`: boolean
- `location`: {lat: float, lon: float, address: string} ⚠️ **EMBEDDED LOCATION DATA**
- `commissioning_date`: date
- `operational_status`: enum [OPERATIONAL, MAINTENANCE, DECOMMISSIONED]

**Source**: `/schemas/neo4j/01_layer_physical_asset.cypher` lines 8-19

---

## 2. Current Location Node Properties

### Location Node (Physical/Geographic Placement)
**Label**: `Location`

**Properties Identified**:
- `id`: UUID (unique identifier)
- `name`: string (location name)
- `locationType`: enum [BUILDING, ROOM, RACK, ZONE, GEOGRAPHIC]
- `coordinates`: {lat: float, lon: float} (geographic coordinates)
- `address`: string (physical address)
- `parent_location`: UUID (hierarchical location support)

**Source**: `/schemas/neo4j/01_layer_physical_asset.cypher` lines 92-101

**Usage Example** (line 103-108):
```cypher
CREATE (control_room:Location {
  id: 'location-control-room-001',
  name: 'Main Control Room',
  locationType: 'ROOM',
  address: 'Building A, Floor 2, Room 201'
});
```

---

## 3. Existing Relationships Involving Equipment/Location

### From Physical Asset Layer Schema:

**Equipment-to-Location Relationships**:
1. **`LOCATED_AT`** - Device to Location
   - Pattern: `(plc:Device)-[:LOCATED_AT]->(control_room:Location)`
   - Source: Line 117
   - Purpose: Physical placement of devices

**Equipment Hierarchy Relationships**:
2. **`CONTAINS_DEVICE`** - PhysicalAsset to Device
   - Pattern: `(plant:PhysicalAsset)-[:CONTAINS_DEVICE]->(plc:Device)`
   - Source: Line 115
   - Purpose: Asset containment hierarchy

3. **`HAS_COMPONENT`** - Device to HardwareComponent
   - Pattern: `(plc:Device)-[:HAS_COMPONENT]->(comm_module:HardwareComponent)`
   - Source: Line 116
   - Purpose: Component composition

4. **`INSTALLED_IN`** - HardwareComponent to Device
   - Pattern: `(brake_controller:HardwareComponent)-[:INSTALLED_IN]->(brake_system:Device)`
   - Source: Line 171
   - Purpose: Component installation

**Multi-Hop Fleet Relationships**:
5. **`PART_OF_SUBSYSTEM`** - Device to PhysicalAsset
   - Pattern: `(brake_system:Device)-[:PART_OF_SUBSYSTEM]->(train_car:PhysicalAsset)`
   - Source: Line 172

6. **`PART_OF_CONSIST`** - PhysicalAsset to PhysicalAsset
   - Pattern: `(train_car:PhysicalAsset)-[:PART_OF_CONSIST]->(train_consist:PhysicalAsset)`
   - Source: Line 173

7. **`PART_OF_FLEET`** - PhysicalAsset to PhysicalAsset
   - Pattern: `(train_consist:PhysicalAsset)-[:PART_OF_FLEET]->(fleet:PhysicalAsset)`
   - Source: Line 174

### From GAP-004 Relationship Patterns:

**Cyber-Physical Monitoring** (gap004_relationships.cypher):
- `MODELS_ASSET` - DigitalTwinState to Device/Component
- `MONITORS_ASSET` - PhysicalSensor to Device/Component
- `CONTROLS_ASSET` - PhysicalActuator to Device/Component
- `CONSTRAINS_ASSET` - PhysicsConstraint to Device/Component
- `DETECTED_ON` - StateDeviation to Device/Component
- `PROTECTS_ASSET` - SafetyFunction to Device/Component

**Location-Related** (None currently defined in GAP-004):
- ⚠️ **NO EXPLICIT LOCATION RELATIONSHIPS** in UC2, UC3, R6, CG-9, or UC1 patterns

---

## 4. Current Constraints on Equipment/Location

### Equipment Constraints
**Source**: `/scripts/gap004_schema_constraints.cypher`

**No constraints found for**:
- `Device` node
- `HardwareComponent` node
- `PhysicalAsset` node
- `Location` node

**GAP-004 Constraints** (35 new node types):
All constraints follow pattern: `FOR (n:NodeType) REQUIRE n.{id_field} IS UNIQUE`

Examples:
- DigitalTwinState: `stateId IS UNIQUE` (line 17)
- PhysicalSensor: `sensorId IS UNIQUE` (line 21)
- PhysicalActuator: `actuatorId IS UNIQUE` (line 24)
- CascadeEvent: `eventId IS UNIQUE` (line 53)

⚠️ **CRITICAL GAP**: No unique constraints defined for core equipment nodes (Device, HardwareComponent, PhysicalAsset, Location)

---

## 5. Current Indexes on Equipment/Location

### Equipment Indexes
**Source**: `/scripts/gap004_schema_indexes.cypher`

**No indexes found for**:
- `Device` node
- `HardwareComponent` node
- `PhysicalAsset` node
- `Location` node

**GAP-004 Indexes** (70+ indexes):

**Multi-Tenant Isolation** (Section 1, lines 17-61):
- All 35 new node types have `customer_namespace` index
- Pattern: `CREATE INDEX {node}_namespace FOR (n:{NodeType}) ON (n.customer_namespace)`

**Temporal Query Optimization** (Section 2, lines 69-87):
- `timestamp` indexes for real-time event nodes
- `retentionUntil` for 90-day window management
- Bitemporal versioning indexes (validFrom, validTo, nodeType)

**Asset Relationship Lookups** (Section 3, lines 94-108):
- Asset-centric queries: `assetId` indexes on DigitalTwinState, PhysicalSensor, PhysicalActuator, etc.
- Example: `CREATE INDEX sensor_asset FOR (n:PhysicalSensor) ON (n.assetId)`

**Severity/Priority Filtering** (Section 4, lines 115-124):
- `severity` indexes for StateDeviation, CascadeEvent, TemporalEvent, DisruptionEvent
- `silLevel` for SafetyFunction
- `criticality` for DependencyLink, CrossInfrastructureDependency

**Categorical Filtering** (Section 5, lines 132-152):
- `sensorType`, `actuatorType`, `eventType` indexes
- Dependency source/target indexes

**Composite Indexes** (Section 6, lines 160-173):
- `(assetId, timestamp)` for historical analysis
- `(eventType, timestamp)` for temporal events
- `(simulationId, sequenceNumber)` for cascades

**Full-Text Search** (Section 7, lines 180-193):
- Natural language search on CascadeEvent, DisruptionEvent, TemporalEvent, SafetyFunction

⚠️ **CRITICAL GAP**: No performance indexes for core equipment nodes

---

## 6. Gap Analysis: Missing for Universal Location Support

### 🚨 Critical Gaps Identified

#### 6.1 Schema Design Issues

**G1: Embedded Location Data in PhysicalAsset**
- **Current**: `location: {lat: float, lon: float, address: string}` embedded in PhysicalAsset node
- **Issue**: Violates normalization, prevents location reuse, limits location hierarchy
- **Impact**: Cannot model multi-level location hierarchies (Site → Building → Floor → Room → Rack)

**G2: Limited Location Hierarchy Support**
- **Current**: `parent_location: UUID` property only
- **Issue**: No formal relationship type for location hierarchy
- **Missing**: `PARENT_OF`, `CONTAINS_LOCATION`, `LOCATED_WITHIN` relationships

**G3: No Location Constraints or Indexes**
- **Current**: Zero constraints on Location node
- **Missing**:
  - Unique constraint on `Location.id`
  - Index on `customer_namespace` (multi-tenant isolation)
  - Index on `locationType` (query filtering)
  - Index on `parent_location` (hierarchy traversal)

#### 6.2 Equipment-Location Relationship Gaps

**G4: Single Relationship Type Only**
- **Current**: Only `LOCATED_AT` relationship exists
- **Missing**:
  - `INSTALLED_AT` - for permanent equipment installation
  - `DEPLOYED_TO` - for mobile/temporary equipment
  - `SHIPPED_TO` - for equipment in transit
  - `STORED_AT` - for inventory/warehouse
  - `MAINTAINED_AT` - for maintenance location tracking

**G5: No Temporal Location Tracking**
- **Current**: No timestamp on `LOCATED_AT` relationship
- **Missing**:
  - `installed_date`, `removal_date` relationship properties
  - Historical location tracking (where was equipment on specific date)
  - Location change event tracking

**G6: No Location Validation**
- **Missing**:
  - Equipment criticality vs location security level validation
  - Physical constraints (rack capacity, power limits)
  - Environmental conditions (temperature, humidity requirements)

#### 6.3 Multi-Tenant Isolation Gaps

**G7: Location Namespace Isolation Missing**
- **Current**: No `customer_namespace` property on Location nodes
- **Issue**: Cannot enforce tenant isolation for locations
- **Risk**: Customer A could see Customer B's facility locations

**G8: No Location Access Control**
- **Missing**:
  - Location visibility scope (private, shared, public)
  - Cross-tenant location sharing capabilities
  - Location access audit trail

#### 6.4 Query Performance Gaps

**G9: No Geospatial Indexing**
- **Current**: `coordinates: {lat: float, lon: float}` as simple properties
- **Missing**:
  - Neo4j spatial point type (`point({latitude: x, longitude: y})`)
  - Spatial indexes for proximity queries
  - Distance calculations and radius searches

**G10: No Location Query Optimization**
- **Missing Indexes**:
  - Location hierarchy traversal index
  - Equipment-by-location lookup index
  - Multi-hop location path index (Fleet → Consist → Car → Rack → Device)

#### 6.5 Integration Gaps with GAP-004 Nodes

**G11: No Location Integration in UC2 (Cyber-Physical)**
- **Missing**: PhysicalSensor/PhysicalActuator location tracking
- **Need**: "Where is sensor S123 physically located for field verification?"

**G12: No Location in UC3 (Cascading Failures)**
- **Missing**: CascadeEvent geographic spread analysis
- **Need**: "Which geographic regions are affected by cascade?"

**G13: No Location in CG-9 (Operational Impact)**
- **Missing**: DisruptionEvent location-based impact assessment
- **Need**: "Financial impact by facility location"

**G14: No Location in UC1 (SCADA Attack)**
- **Missing**: SCADAEvent physical location correlation
- **Need**: "Suspicious HMI access from unauthorized location"

#### 6.6 Mobile Equipment Gaps

**G15: No Dynamic Location Support**
- **Current**: Static `LOCATED_AT` relationship
- **Missing**:
  - Real-time location updates for trains/vehicles
  - Location change event stream
  - GPS coordinate tracking with timestamps

**G16: No Route/Path Modeling**
- **Missing**:
  - Travel routes between locations
  - Expected vs actual location validation
  - Geofencing and boundary violations

#### 6.7 Documentation and Standards Gaps

**G17: No Location Type Standardization**
- **Current**: Hardcoded enum [BUILDING, ROOM, RACK, ZONE, GEOGRAPHIC]
- **Missing**:
  - Industry standard location types (ISA-95, IEC 62443 zones)
  - Custom location type extension mechanism
  - Location type hierarchy (Zone → Conduit → Level)

**G18: No Location Metadata**
- **Missing**:
  - Physical dimensions (floor area, rack units, ceiling height)
  - Environmental conditions (temperature range, humidity)
  - Capacity limits (power, cooling, network ports)
  - Safety/security classification (IEC 62443 security levels)

---

## 7. Recommendations for Universal Location Architecture

### Immediate Actions (High Priority)

1. **Add Location Constraints** (gap004_schema_constraints.cypher):
   ```cypher
   CREATE CONSTRAINT location_id IF NOT EXISTS
   FOR (n:Location) REQUIRE n.id IS UNIQUE;
   ```

2. **Add Location Indexes** (gap004_schema_indexes.cypher):
   ```cypher
   CREATE INDEX location_namespace IF NOT EXISTS
   FOR (n:Location) ON (n.customer_namespace);

   CREATE INDEX location_type IF NOT EXISTS
   FOR (n:Location) ON (n.locationType);

   CREATE INDEX location_parent IF NOT EXISTS
   FOR (n:Location) ON (n.parent_location);

   CREATE INDEX location_spatial IF NOT EXISTS
   FOR (n:Location) ON (n.coordinates);
   ```

3. **Normalize PhysicalAsset Location Data**:
   - Remove embedded `location` property from PhysicalAsset
   - Enforce `LOCATED_AT` relationship to Location node
   - Migrate existing embedded data to Location nodes

4. **Define Location Hierarchy Relationships**:
   ```cypher
   (site:Location {locationType: 'SITE'})
     -[:CONTAINS_LOCATION]->
   (building:Location {locationType: 'BUILDING'})
     -[:CONTAINS_LOCATION]->
   (floor:Location {locationType: 'FLOOR'})
     -[:CONTAINS_LOCATION]->
   (room:Location {locationType: 'ROOM'})
     -[:CONTAINS_LOCATION]->
   (rack:Location {locationType: 'RACK'})
   ```

### Medium-Term Enhancements

5. **Temporal Location Tracking**:
   - Add `installed_at`, `removed_at` properties to `LOCATED_AT` relationship
   - Create LocationHistory node for historical tracking

6. **Equipment-Location Relationship Types**:
   - Define semantic relationship types: INSTALLED_AT, DEPLOYED_TO, STORED_AT, etc.
   - Add relationship properties: timestamp, installation_type, certification_status

7. **Geospatial Enhancement**:
   - Convert `coordinates` to Neo4j spatial point type
   - Implement spatial indexes for proximity queries
   - Add geofencing capabilities

### Long-Term Architecture

8. **Integration with GAP-004 Use Cases**:
   - UC2: Add location to PhysicalSensor/PhysicalActuator nodes
   - UC3: Add geographic impact to CascadeEvent
   - CG-9: Add location-based impact to DisruptionEvent
   - UC1: Add physical location to SCADAEvent

9. **Mobile Equipment Support**:
   - Dynamic location updates for vehicles/trains
   - GPS tracking integration
   - Real-time location event stream

10. **Location Metadata Enhancement**:
    - Physical dimensions and capacity
    - Environmental conditions
    - Security/safety classifications (IEC 62443 zones)
    - Compliance and certification tracking

---

## 8. Summary Statistics

| Category | Count | Status |
|----------|-------|--------|
| **Equipment Node Types** | 3 | Device, HardwareComponent, PhysicalAsset |
| **Location Node Types** | 1 | Location |
| **Equipment-Location Relationships** | 1 | LOCATED_AT only |
| **Equipment Constraints** | 0 | ⚠️ NONE DEFINED |
| **Location Constraints** | 0 | ⚠️ NONE DEFINED |
| **Equipment Indexes** | 0 | ⚠️ NONE DEFINED |
| **Location Indexes** | 0 | ⚠️ NONE DEFINED |
| **GAP-004 New Node Types** | 35 | All with constraints and indexes |
| **Critical Gaps Identified** | 18 | G1-G18 documented above |

---

## 9. Next Steps for Universal Location Architecture

1. **Agent 2**: Define canonical location hierarchy model (Site → Building → Floor → Room → Rack)
2. **Agent 3**: Specify relationship types and properties for equipment-location linking
3. **Agent 4**: Design multi-tenant isolation strategy for locations
4. **Agent 5**: Create migration plan for embedded location data
5. **Agent 6**: Implement geospatial indexing and query patterns
6. **Agent 7**: Integrate location tracking with GAP-004 use cases

---

**Analysis Complete**: 2025-11-13
**File**: `/docs/analysis/universal_location/AGENT1_EXISTING_SCHEMA_ANALYSIS.md`
**Coordination**: Findings stored in memory namespace `universal_location_architecture`
