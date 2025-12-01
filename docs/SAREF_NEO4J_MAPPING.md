# SAREF to Neo4j Critical Infrastructure Mapping

**File:** SAREF_NEO4J_MAPPING.md
**Created:** 2025-10-29
**Version:** 1.0.0
**Purpose:** Map SAREF ontologies to Neo4j graph database schema for critical infrastructure vulnerability tracking
**Status:** ACTIVE

## Executive Summary

This document provides comprehensive mappings from SAREF (Smart Applications REFerence) ontologies to Neo4j graph database schema for critical infrastructure systems. The mappings integrate SAREF-Core, SAREF-Water, SAREF-Energy, SAREF-Grid, SAREF-Manufacturing, SAREF-City, and SAREF-Building ontologies with existing vulnerability tracking infrastructure.

## Table of Contents

1. [SAREF-Core Mapping](#saref-core-mapping)
2. [SAREF-Water Mapping](#saref-water-mapping)
3. [SAREF-Energy Mapping](#saref-energy-mapping)
4. [SAREF-Grid Mapping](#saref-grid-mapping)
5. [SAREF-Manufacturing Mapping](#saref-manufacturing-mapping)
6. [SAREF-City Mapping](#saref-city-mapping)
7. [Integration Strategy](#integration-strategy)
8. [Critical Infrastructure Node Designs](#critical-infrastructure-node-designs)

---

## SAREF-Core Mapping

### Core Device Classes

#### Node: `SAREFDevice`
```cypher
(:SAREFDevice {
  device_id: String,           // Unique identifier
  device_kind: String,         // DeviceKind classification
  manufacturer: String,
  model: String,
  serial_number: String,
  firmware_version: String,
  location: Point,             // GeoSpatial coordinates
  commissioning_date: DateTime,
  operational_status: String,  // operational|maintenance|offline
  saref_uri: String           // Original SAREF ontology URI
})
```

**Subclasses (Node Labels):**
- `:Sensor` - Devices that observe properties
- `:Actuator` - Devices that act on commands
- `:Meter` - Devices that measure consumption
- `:Appliance` - End-user devices

#### Relationships from SAREFDevice:
```cypher
// Core SAREF relationships
(:SAREFDevice)-[:HAS_FUNCTION]->(:Function)
(:SAREFDevice)-[:HAS_STATE]->(:State)
(:SAREFDevice)-[:OBSERVES]->(:Property)
(:SAREFDevice)-[:MEASURES]->(:Property)
(:SAREFDevice)-[:OFFERS]->(:Service)
(:SAREFDevice)-[:CONSISTS_OF]->(:SAREFDevice)  // Composite devices
(:SAREFDevice)-[:IS_USED_FOR]->(:Task)
(:SAREFDevice)-[:CONTROLS]->(:FeatureOfInterest)

// Integration with existing vulnerability schema
(:SAREFDevice)-[:HAS_VULNERABILITY]->(:Vulnerability)
(:SAREFDevice)-[:LOCATED_IN]->(:Infrastructure)
(:SAREFDevice)-[:PART_OF_SYSTEM]->(:System)
```

### Property Observation Model

#### Node: `Property`
```cypher
(:Property {
  property_id: String,
  property_type: String,      // Temperature|Pressure|Flow|Energy
  unit_of_measure: String,
  measurement_range_min: Float,
  measurement_range_max: Float,
  critical_threshold: Float,
  saref_uri: String
})
```

#### Node: `Observation`
```cypher
(:Observation {
  observation_id: String,
  timestamp: DateTime,
  value: Float,
  unit: String,
  quality: String,           // good|uncertain|bad
  result_time: DateTime,
  phenomenon_time: DateTime,
  saref_uri: String
})
```

```cypher
(:Sensor)-[:MADE_OBSERVATION]->(:Observation)
(:Observation)-[:OBSERVED_PROPERTY]->(:Property)
(:Observation)-[:HAS_FEATURE_OF_INTEREST]->(:FeatureOfInterest)
```

### Command and Control Model

#### Node: `Command`
```cypher
(:Command {
  command_id: String,
  command_type: String,       // OnCommand|OffCommand|SetLevelCommand
  description: String,
  parameters: Map,           // JSON object with command parameters
  execution_time: Duration,
  saref_uri: String
})
```

#### Node: `Service`
```cypher
(:Service {
  service_id: String,
  service_name: String,
  service_type: String,
  endpoint: String,
  protocol: String,
  saref_uri: String
})
```

```cypher
(:Service)-[:REPRESENTS]->(:Function)
(:Service)-[:HAS_OPERATION]->(:Operation)
(:Operation)-[:EXECUTES]->(:Command)
(:Actuator)-[:ACTS_UPON]->(:Command)
```

---

## SAREF-Water Mapping

### Water Infrastructure Classes

#### Node: `WaterInfrastructure`
```cypher
(:WaterInfrastructure {
  infrastructure_id: String,
  infrastructure_type: String,  // TreatmentPlant|DistributionSystem|MonitoringInfrastructure
  water_kind: String,           // DrinkingWater|RawWater|Wastewater|Stormwater
  water_use: String,            // Domestic|Industry|Agriculture|Aquaculture|Recreation
  capacity: Float,              // m³/day
  service_population: Integer,
  location: Point,
  commissioned_date: DateTime,
  operational_status: String,
  saref_uri: String
})
```

**Subclass Labels:**
- `:TreatmentPlant` - Water/wastewater treatment facilities
- `:DistributionSystem` - Water distribution networks
- `:StorageInfrastructure` - Water storage facilities
- `:MonitoringInfrastructure` - Gauging stations and monitoring systems

#### Node: `WaterAsset`
```cypher
(:WaterAsset {
  asset_id: String,
  asset_type: String,          // Pipe|Pump|Valve|Tank|Reservoir|Manhole
  material: String,            // Steel|PVC|Concrete|Cast Iron
  installation_date: DateTime,
  diameter: Float,             // mm for pipes
  length: Float,               // m for pipes
  pressure_rating: Float,      // Bar
  location: Point,
  geometry: LineString,        // For pipes/mains
  saref_uri: String
})
```

**Subclass Labels:**
- `:Pipe` - Water pipes (closed conduit)
- `:Channel` - Open conduits
- `:Pump` - Water pumps (also actuator)
- `:Valve` - Control valves (also actuator)
- `:Tank` - Storage tanks
- `:Reservoir` - Water reservoirs
- `:FireHydrant` - Fire protection infrastructure
- `:WaterMeter` - Metering devices
- `:Manhole` - Access points

#### Node: `WaterProperty`
```cypher
(:WaterProperty {
  property_id: String,
  property_category: String,    // Chemical|Microbial|Acceptability|Environmental
  property_name: String,        // Chlorine|pH|Turbidity|Temperature|EscherichiaColi
  regulatory_limit: Float,
  measurement_unit: String,
  monitoring_frequency: Duration,
  saref_uri: String
})
```

**Property Categories:**
- `ChemicalProperty` - Chlorine, Fluoride, Lead, Mercury, Nitrate, Iron, etc.
- `MicrobialProperty` - E.coli, Coliform bacteria, Enterococci, etc.
- `AcceptabilityProperty` - pH, Turbidity, Color, Odor, Taste, Temperature
- `EnvironmentalProperty` - Atmospheric pressure, Humidity, Precipitation

#### Node: `WaterMeter`
```cypher
(:WaterMeter:Meter:WaterDevice {
  meter_id: String,
  fabrication_number: String,
  firmware_version: String,
  hardware_version: String,
  radio_frequency: Float,      // MHz
  power_requirement: Float,    // Watts
  installation_date: DateTime,
  location: Point,
  saref_uri: String
})
```

```cypher
(:WaterMeter)-[:OBSERVES]->(:WaterFlowProperty)
(:WaterMeter)-[:APPLIES_TARIFF]->(:Tariff)
```

#### Node: `Tariff`
```cypher
(:Tariff {
  tariff_id: String,
  tariff_type: String,          // TimeBasedTariff|ConsumptionBasedTariff|ThresholdBasedTariff
  billing_period: Duration,
  start_timestamp: DateTime,
  duration: Duration,
  rate: Float,
  currency: String,
  saref_uri: String
})
```

### Water Source/Sink Assets

```cypher
// Source assets
(:SourceAsset {
  asset_id: String,
  source_type: String,          // Lake|River|Aquifer|Glacier|Lagoon
  capacity: Float,              // m³
  water_quality: String,
  location: Point,
  geometry: Polygon,
  saref_uri: String
})

// Sink assets
(:SinkAsset {
  asset_id: String,
  sink_type: String,            // River|Sea|Ocean|Estuary
  location: Point,
  geometry: Polygon,
  saref_uri: String
})
```

### Water Infrastructure Relationships

```cypher
// Infrastructure composition
(:WaterInfrastructure)-[:CONTAINS_ASSET]->(:WaterAsset)
(:WaterAsset)-[:CONNECTS_TO]->(:WaterAsset)
(:Pipe)-[:CONNECTS]->(:Pump|:Valve|:Tank)

// Water flow relationships
(:SourceAsset)-[:SUPPLIES]->(:Intake)
(:Intake)-[:FEEDS]->(:TreatmentPlant)
(:TreatmentPlant)-[:DISTRIBUTES_TO]->(:DistributionSystem)
(:DistributionSystem)-[:DELIVERS_TO]->(:Consumer)
(:Consumer)-[:DISCHARGES_TO]->(:SinkAsset)

// Monitoring and control
(:MonitoringInfrastructure)-[:MONITORS]->(:WaterAsset)
(:WaterMeter)-[:MEASURES_FLOW_IN]->(:Pipe)
(:Pump|:Valve)-[:CONTROLS_FLOW_IN]->(:Pipe)

// Water quality
(:WaterAsset)-[:HAS_PROPERTY]->(:WaterProperty)
(:GaugingStation)-[:MEASURES]->(:WaterProperty)

// Integration with vulnerability tracking
(:WaterInfrastructure)-[:HAS_VULNERABILITY]->(:Vulnerability)
(:WaterAsset)-[:EXPOSED_TO_CVE]->(:CVE)
(:WaterMeter)-[:COMMUNICATES_VIA]->(:Protocol)
(:Protocol)-[:HAS_VULNERABILITY]->(:Vulnerability)
```

---

## SAREF-Energy Mapping

### Energy Device Model

#### Node: `EnergyDevice`
```cypher
(:EnergyDevice:SAREFDevice {
  device_id: String,
  device_category: String,      // Generator|Storage|Load
  rated_power: Float,           // kW
  energy_source: String,        // Solar|Wind|Hydro|Fossil|Nuclear|Battery
  efficiency: Float,            // Percentage
  location: Point,
  grid_connection_point: String,
  saref_uri: String
})
```

**Subclass Labels:**
- `:PowerProfile` - Device power profiles
- `:LoadControl` - Demand response capable devices
- `:EnergyStorage` - Battery systems
- `:Generator` - Power generation units

#### Node: `PowerProfile`
```cypher
(:PowerProfile {
  profile_id: String,
  profile_type: String,         // Absolute|Relative|Predicted
  total_time: Duration,
  start_time: DateTime,
  end_time: DateTime,
  energy_forecast: Float,       // kWh
  saref_uri: String
})
```

#### Node: `PowerSequence`
```cypher
(:PowerSequence {
  sequence_id: String,
  sequence_number: Integer,
  duration: Duration,
  min_power: Float,             // W
  max_power: Float,             // W
  avg_power: Float,             // W
  interruptible: Boolean,
  saref_uri: String
})
```

```cypher
(:PowerProfile)-[:HAS_SEQUENCE]->(:PowerSequence)
(:EnergyDevice)-[:HAS_POWER_PROFILE]->(:PowerProfile)
```

### Energy Storage Model

```cypher
(:EnergyStorage:EnergyDevice {
  storage_id: String,
  storage_type: String,         // Battery|Pumped Hydro|Compressed Air|Flywheel
  capacity: Float,              // kWh
  charge_rate: Float,           // kW
  discharge_rate: Float,        // kW
  state_of_charge: Float,       // Percentage
  depth_of_discharge: Float,    // Percentage
  round_trip_efficiency: Float, // Percentage
  cycle_count: Integer,
  location: Point,
  saref_uri: String
})
```

---

## SAREF-Grid Mapping

### Smart Grid Components

#### Node: `GridMeter`
```cypher
(:GridMeter:Meter:SAREFDevice {
  meter_id: String,
  meter_type: String,           // Smart Meter|AMR|AMI
  obis_code: String,            // Object Identification System code
  firmware_version: String,
  mac_address: String,
  communication_protocol: String, // DLMS/COSEM|Modbus|DNP3
  installation_date: DateTime,
  location: Point,
  phase: String,                // Single|Three-phase
  voltage_rating: Float,        // V
  current_rating: Float,        // A
  saref_uri: String
})
```

#### Node: `Clock`
```cypher
(:Clock {
  clock_id: String,
  time: DateTime,
  timezone: Integer,            // Minutes from UTC
  status: Integer,              // Status code
  clock_base: Integer,          // 0=undefined, 1=crystal, 2=50Hz, 3=60Hz, 4=GPS, 5=radio
  daylight_savings_enabled: Boolean,
  daylight_savings_begin: DateTime,
  daylight_savings_end: DateTime,
  daylight_savings_deviation: Integer,  // Minutes
  saref_uri: String
})
```

```cypher
(:GridMeter)-[:HAS_CLOCK]->(:Clock)
```

#### Node: `ActivityCalendar`
```cypher
(:ActivityCalendar {
  calendar_id: String,
  active_calendar_name: String,
  passive_calendar_name: String,
  activate_passive_time: DateTime,
  saref_uri: String
})
```

```cypher
(:GridMeter)-[:HAS_ACTIVITY_CALENDAR]->(:ActivityCalendar)
(:ActivityCalendar)-[:HAS_ACTIVE_SEASON]->(:SeasonProfile)
(:ActivityCalendar)-[:HAS_PASSIVE_SEASON]->(:SeasonProfile)
```

#### Node: `SeasonProfile`
```cypher
(:SeasonProfile {
  profile_id: String,
  season_name: String,
  season_start: DateTime,
  saref_uri: String
})
```

```cypher
(:SeasonProfile)-[:HAS_MONDAY_PROFILE]->(:DayProfile)
(:SeasonProfile)-[:HAS_TUESDAY_PROFILE]->(:DayProfile)
(:SeasonProfile)-[:HAS_WEDNESDAY_PROFILE]->(:DayProfile)
(:SeasonProfile)-[:HAS_THURSDAY_PROFILE]->(:DayProfile)
(:SeasonProfile)-[:HAS_FRIDAY_PROFILE]->(:DayProfile)
(:SeasonProfile)-[:HAS_SATURDAY_PROFILE]->(:DayProfile)
(:SeasonProfile)-[:HAS_SUNDAY_PROFILE]->(:DayProfile)
(:SeasonProfile)-[:HAS_SPECIAL_DAY_PROFILE]->(:SpecialDayProfile)
```

#### Node: `ProfileGeneric`
```cypher
(:ProfileGeneric {
  profile_id: String,
  capture_period: Integer,      // Seconds (0 = manual/event triggered)
  obis_code: String,
  saref_uri: String
})
```

```cypher
(:GridMeter)-[:HAS_PROFILE_GENERIC]->(:ProfileGeneric)
(:ProfileGeneric)-[:CAPTURES_OBSERVATION]->(:Observation)
(:ProfileGeneric)-[:CAPTURES_PROPERTY_VALUE]->(:PropertyValue)
(:ProfileGeneric)-[:RELATED_CLOCK]->(:Clock)
```

#### Node: `BreakerState`
```cypher
(:BreakerState:State {
  state_id: String,
  output_state: Boolean,        // true=connected, false=disconnected
  control_state: Integer,       // 0=disconnected, 1=connected, 2=ready for reconnection
  control_mode: Integer,        // Configuration for state transitions
  saref_uri: String
})
```

### Grid Energy Properties

```cypher
(:EnergyAndPowerProperty:Property {
  property_id: String,
  property_type: String         // ActiveEnergy|ReactivyEnergy|ActivePower|ReactivePower|
                                // ApparentPower|Voltage|Current|PowerFactor
})

(:QualityProperty:Property {
  property_id: String,
  property_type: String         // VoltageSag|VoltageSwell|LongPowerFailure
})

(:MeterProperty:Property {
  property_id: String,
  property_type: String         // BillingPeriod|Phase|PowerLimit|Manufacturer
})
```

### Grid Operations (COSEM Model)

```cypher
// Get, Set, Action operations following DLMS/COSEM standard
(:GetService:Service)-[:HAS_OPERATION]->(:GetOperation:Operation)
(:SetService:Service)-[:HAS_OPERATION]->(:SetOperation:Operation)
(:ActionService:Service)-[:HAS_OPERATION]->(:ActionOperation:Operation)

(:GetOperation)-[:HAS_INPUT]->(:GetOperationPropertyInput)
(:GetOperation)-[:HAS_OUTPUT]->(:GetOperationDataOutput|:GetOperationObjectOutput)

(:SetOperation)-[:HAS_INPUT]->(:SetOperationDataInput|:SetOperationObjectInput)

(:ActionOperation)-[:HAS_INPUT]->(:SimpleActionOperationInput|:ComplexActionOperationInput)
```

---

## SAREF-Manufacturing Mapping

### Manufacturing Infrastructure

#### Node: `ProductionEquipment`
```cypher
(:ProductionEquipment:SAREFDevice {
  equipment_id: String,
  equipment_category: String,   // LaserCuttingMachine|MillingMachine|WeldingMachine|
                                // MouldingMachine|AssemblyRobot
  manufacturer: String,
  model_number: String,
  serial_number: String,
  production_capacity: Float,
  location: Point,
  work_center: String,
  commissioning_date: DateTime,
  maintenance_schedule: String,
  saref_uri: String
})
```

**Subclass Labels:**
- `:WorkCenter` - Equipment element under an area
- `:ProductionLine` - Series of equipment for production process

#### Node: `Factory`
```cypher
(:Factory:Building {
  factory_id: String,
  factory_name: String,
  location: Point,
  geometry: Polygon,
  total_area: Float,            // m²
  production_capacity: Float,
  employee_count: Integer,
  saref_uri: String
})
```

#### Node: `Site`
```cypher
(:Site:BuildingSpace {
  site_id: String,
  site_name: String,
  location: Point,
  geometry: Polygon,
  saref_uri: String
})
```

#### Node: `Area`
```cypher
(:Area:BuildingSpace {
  area_id: String,
  area_name: String,
  area_type: String,            // Production|Assembly|Quality Control|Warehouse
  location: Point,
  geometry: Polygon,
  saref_uri: String
})
```

### Manufacturing Product Tracking

#### Node: `ItemCategory`
```cypher
(:ItemCategory {
  category_id: String,
  gtin12_id: String,            // Global Trade Item Number
  gtin13_id: String,
  gtin14_id: String,
  gtin8_id: String,
  irdi_id: String,              // International Registration Data Identifier
  uuid: String,
  model_number: String,
  description: String,
  specifications: Map,
  saref_uri: String
})
```

#### Node: `ItemBatch`
```cypher
(:ItemBatch:Batch {
  batch_id: String,
  batch_number: String,
  production_date: DateTime,
  batch_size: Integer,
  quality_status: String,
  saref_uri: String
})
```

#### Node: `Item`
```cypher
(:Item {
  item_id: String,
  serial_number: String,
  gtin_code: String,
  production_timestamp: DateTime,
  quality_check_status: String,
  saref_uri: String
})
```

```cypher
(:ItemCategory)-[:CATEGORY_OF]->(:ItemBatch)
(:ItemBatch)-[:CONTAINS_ITEM]->(:Item)
(:Item)-[:BELONGS_TO_BATCH]->(:ItemBatch)
(:Item)-[:CONSISTS_OF]->(:Item)  // Sub-assemblies
```

#### Node: `MaterialBatch`
```cypher
(:MaterialBatch:Batch {
  batch_id: String,
  material_type: String,
  quantity: Float,
  unit: String,
  certificate_number: String,   // Quality certificate (e.g., NEN 10204:2004 3.1)
  supplier: String,
  received_date: DateTime,
  saref_uri: String
})
```

```cypher
(:MaterialCategory)-[:CATEGORY_OF]->(:MaterialBatch)
(:ItemBatch)-[:USES_MATERIAL]->(:MaterialBatch)
```

### Manufacturing Process Tracking

```cypher
(:ProductionEquipment)-[:PRODUCES]->(:ItemCategory)
(:ProductionEquipmentCategory)-[:PRODUCES]->(:ItemCategory)
(:ItemBatch)-[:NEEDS_EQUIPMENT]->(:ProductionEquipment)
(:Factory)-[:CONTAINS_SITE]->(:Site)
(:Site)-[:CONTAINS_AREA]->(:Area)
(:Area)-[:CONTAINS_WORK_CENTER]->(:WorkCenter:ProductionEquipment)

// Integration with vulnerability tracking
(:ProductionEquipment)-[:HAS_VULNERABILITY]->(:Vulnerability)
(:ProductionEquipment)-[:RUNS_SOFTWARE]->(:Software)
(:Software)-[:HAS_CVE]->(:CVE)
```

---

## SAREF-City Mapping

### City Infrastructure

#### Node: `AdministrativeArea`
```cypher
(:AdministrativeArea:Feature {
  area_id: String,
  area_name: String,
  area_type: String,            // Country|City|District|Neighbourhood
  population: Integer,
  location: Point,
  geometry: Polygon,
  saref_uri: String
})
```

**Subclass Labels:**
- `:Country` - National level
- `:City` - Urban settlement
- `:District` - Administrative division
- `:Neighbourhood` - Localized community

#### Node: `CityObject`
```cypher
(:CityObject:Feature {
  object_id: String,
  object_type: String,
  name: String,
  location: Point,
  geometry: Point|LineString|Polygon,
  saref_uri: String
})
```

#### Node: `Facility`
```cypher
(:Facility:Feature {
  facility_id: String,
  facility_type: String,        // Hospital|School|ParkingLot|Library|Stadium|Airport
  name: String,
  capacity: Integer,
  location: Point,
  geometry: Polygon,
  operational_hours: String,
  accessibility: [String],      // wheelchair|elevator|braille|audio
  saref_uri: String
})
```

#### Node: `PublicService`
```cypher
(:PublicService {
  service_id: String,
  service_name: String,
  service_type: String,         // Healthcare|Education|Transportation|Waste|Emergency
  description: String,
  available_languages: [String],
  contact_info: Map,
  saref_uri: String
})
```

```cypher
(:Facility)-[:PROVIDES]->(:PublicService)
(:PublicService)-[:INVOLVES_FACILITY]->(:Facility)
(:PublicService)-[:PHYSICALLY_AVAILABLE_AT]->(:AdministrativeArea)
(:Agent)-[:PROVIDES]->(:PublicService)
(:Agent)-[:USES]->(:PublicService)
```

#### Node: `Event`
```cypher
(:Event {
  event_id: String,
  event_name: String,
  event_type: String,           // Festival|Conference|Sports|Emergency
  description: String,
  start_time: DateTime,
  end_time: DateTime,
  location: Point,
  accessibility_modes: [String],
  capacity: Integer,
  saref_uri: String
})
```

```cypher
(:Event)-[:TAKES_PLACE_AT_FACILITY]->(:Facility)
(:Event)-[:TAKES_PLACE_AT_TIME]->(:TemporalEntity)
(:Event)-[:ORGANIZED_BY]->(:Agent)
(:Event)-[:IS_SUBEVENT_OF]->(:Event)
```

### Key Performance Indicators

#### Node: `KeyPerformanceIndicator`
```cypher
(:KeyPerformanceIndicator {
  kpi_id: String,
  kpi_name: String,
  description: String,
  category: String,             // Efficiency|Quality|Availability|Sustainability
  calculation_period: Duration,
  target_value: Float,
  threshold_warning: Float,
  threshold_critical: Float,
  saref_uri: String
})
```

#### Node: `KPIAssessment`
```cypher
(:KPIAssessment {
  assessment_id: String,
  value: Float,
  unit: String,
  creation_date: DateTime,
  expiration_date: DateTime,
  last_update_date: DateTime,
  status: String,               // good|warning|critical
  saref_uri: String
})
```

```cypher
(:FeatureOfInterest)-[:HAS_KPI]->(:KeyPerformanceIndicator)
(:KPIAssessment)-[:QUANTIFIES_KPI]->(:KeyPerformanceIndicator)
(:KPIAssessment)-[:ASSESSES]->(:FeatureOfInterest)
(:KPIAssessment)-[:REFERS_TO_FEATURE]->(:Feature)
(:KPIAssessment)-[:REFERS_TO_TIME]->(:TemporalEntity)
(:KPIAssessment)-[:IS_ASSESSED_BY]->(:Agent)
(:KPIAssessment)-[:IS_DERIVED_FROM]->(:Observation)
```

---

## Integration Strategy

### 1. Unified Device Model

All SAREF devices integrate into a unified hierarchy:

```cypher
(:Device)                           // Top-level abstract node
  ├─ (:SAREFDevice)                // Core SAREF devices
  │   ├─ (:Sensor)
  │   ├─ (:Actuator)
  │   └─ (:Meter)
  ├─ (:WaterDevice)                // Water domain devices
  │   ├─ (:WaterMeter)
  │   ├─ (:Pump)
  │   └─ (:Valve)
  ├─ (:EnergyDevice)               // Energy domain devices
  │   ├─ (:Generator)
  │   └─ (:EnergyStorage)
  ├─ (:GridMeter)                  // Smart grid meters
  └─ (:ProductionEquipment)        // Manufacturing equipment
```

### 2. Cross-Domain Property Model

Properties from all domains share common structure:

```cypher
(:Property)
  ├─ (:WaterProperty)
  │   ├─ (:ChemicalProperty)
  │   ├─ (:MicrobialProperty)
  │   └─ (:AcceptabilityProperty)
  ├─ (:EnergyAndPowerProperty)
  ├─ (:QualityProperty)
  └─ (:MeterProperty)
```

### 3. Vulnerability Integration

Connect SAREF devices to existing vulnerability schema:

```cypher
// CVE tracking for SAREF devices
(:SAREFDevice)-[:HAS_VULNERABILITY]->(:Vulnerability)
(:Vulnerability)-[:REFERENCES_CVE]->(:CVE)

// Protocol vulnerabilities
(:SAREFDevice)-[:USES_PROTOCOL]->(:Protocol)
(:Protocol)-[:HAS_VULNERABILITY]->(:Vulnerability)

// Software vulnerabilities
(:SAREFDevice)-[:RUNS_SOFTWARE]->(:Software)
(:Software)-[:HAS_VERSION]->(:SoftwareVersion)
(:SoftwareVersion)-[:AFFECTED_BY]->(:CVE)

// Network exposure
(:SAREFDevice)-[:CONNECTED_TO]->(:Network)
(:Network)-[:HAS_SECURITY_ZONE]->(:SecurityZone)
```

### 4. Infrastructure Hierarchy

Integrate spatial and organizational hierarchies:

```cypher
// Geographic hierarchy
(:Country)-[:CONTAINS]->(:City)
(:City)-[:CONTAINS]->(:District)
(:District)-[:CONTAINS]->(:Neighbourhood)

// Physical infrastructure hierarchy
(:Factory)-[:CONTAINS_SITE]->(:Site)
(:Site)-[:CONTAINS_AREA]->(:Area)
(:Area)-[:CONTAINS_WORK_CENTER]->(:WorkCenter)

// Water infrastructure hierarchy
(:WaterInfrastructure)-[:CONTAINS_ASSET]->(:WaterAsset)
(:WaterAsset)-[:CONNECTS_TO]->(:WaterAsset)

// Spatial containment
(:Building)-[:CONTAINS]->(:BuildingSpace)
(:BuildingSpace)-[:CONTAINS]->(:SAREFDevice)
```

### 5. Observation and Monitoring

Unified observation model across all domains:

```cypher
(:Sensor|:Meter|:MonitoringInfrastructure)-[:MADE_OBSERVATION]->(:Observation)
(:Observation)-[:OBSERVED_PROPERTY]->(:Property)
(:Observation)-[:HAS_RESULT]->(:PropertyValue)
(:Observation)-[:OBSERVED_BY]->(:Sensor|:Meter)
(:Observation)-[:PHENOMENON_TIME]->(:TemporalEntity)

// Quality assurance
(:Observation)-[:HAS_QUALITY_FLAG]->(:QualityFlag)
(:Observation)-[:VALIDATED_BY]->(:Agent)
```

---

## Critical Infrastructure Node Designs

### Water Treatment Plant Node

```cypher
CREATE (plant:TreatmentPlant:WaterInfrastructure:CriticalInfrastructure {
  infrastructure_id: "WTP-001",
  name: "Municipal Water Treatment Plant Alpha",
  infrastructure_type: "TreatmentPlant",
  water_kind: "DrinkingWater",
  capacity: 50000000.0,           // 50 million liters/day
  service_population: 125000,
  location: point({longitude: -122.4194, latitude: 37.7749}),
  commissioned_date: datetime("2010-03-15"),
  operational_status: "operational",
  criticality_level: "HIGH",
  consequence_of_failure: "SEVERE",
  saref_uri: "https://saref.etsi.org/saref4watr/TreatmentPlant#WTP-001"
})

// Treatment stages
CREATE (intake:Intake:WaterAsset {
  asset_id: "WTP-001-INTAKE",
  location: point({longitude: -122.4200, latitude: 37.7755}),
  flow_rate: 580.0               // L/s
})

CREATE (clarifier:WaterAsset {
  asset_id: "WTP-001-CLARIFIER",
  asset_type: "Clarifier",
  capacity: 2000000.0            // 2 million liters
})

CREATE (filter:WaterAsset {
  asset_id: "WTP-001-FILTER",
  asset_type: "RapidSandFilter",
  filtration_rate: 200.0         // m³/h
})

CREATE (disinfection:WaterAsset {
  asset_id: "WTP-001-DISINFECTION",
  asset_type: "ChlorinationSystem",
  chlorine_dose: 2.5             // mg/L
})

// SCADA system
CREATE (scada:SAREFDevice:ControlSystem {
  device_id: "WTP-001-SCADA",
  manufacturer: "Siemens",
  model: "SIMATIC PCS 7",
  firmware_version: "9.1SP2",
  communication_protocol: "Modbus TCP"
})

// Sensors and meters
CREATE (ph_sensor:Sensor:WaterDevice {
  device_id: "WTP-001-PH-001",
  sensor_type: "pH",
  measurement_range_min: 0.0,
  measurement_range_max: 14.0,
  critical_threshold: 6.5
})

CREATE (turbidity_sensor:Sensor:WaterDevice {
  device_id: "WTP-001-TURB-001",
  sensor_type: "Turbidity",
  measurement_unit: "NTU"
})

CREATE (chlorine_analyzer:Sensor:WaterDevice {
  device_id: "WTP-001-CL2-001",
  sensor_type: "Chlorine Residual",
  measurement_unit: "mg/L"
})

CREATE (flow_meter:WaterMeter:Meter {
  meter_id: "WTP-001-FLOW-001",
  meter_type: "Electromagnetic",
  diameter: 600.0,               // mm
  measurement_unit: "L/s"
})

// Actuators
CREATE (chlorine_pump:Pump:Actuator:WaterDevice {
  device_id: "WTP-001-CLPUMP-001",
  pump_type: "Dosing Pump",
  flow_rate: 50.0,               // L/h
  motor_power: 0.75              // kW
})

// Relationships
CREATE (plant)-[:CONTAINS_ASSET]->(intake)
CREATE (plant)-[:CONTAINS_ASSET]->(clarifier)
CREATE (plant)-[:CONTAINS_ASSET]->(filter)
CREATE (plant)-[:CONTAINS_ASSET]->(disinfection)
CREATE (plant)-[:CONTROLLED_BY]->(scada)

CREATE (intake)-[:FEEDS]->(clarifier)
CREATE (clarifier)-[:FEEDS]->(filter)
CREATE (filter)-[:FEEDS]->(disinfection)

CREATE (ph_sensor)-[:MONITORS]->(filter)
CREATE (turbidity_sensor)-[:MONITORS]->(clarifier)
CREATE (chlorine_analyzer)-[:MONITORS]->(disinfection)
CREATE (flow_meter)-[:MEASURES_FLOW_IN]->(disinfection)

CREATE (scada)-[:CONTROLS]->(chlorine_pump)
CREATE (chlorine_pump)-[:DOSES_INTO]->(disinfection)

// Vulnerabilities
CREATE (cve_modbus:CVE {
  cve_id: "CVE-2023-1234",
  description: "Modbus TCP authentication bypass",
  cvss_score: 9.8,
  cvss_vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
})

CREATE (scada)-[:HAS_VULNERABILITY]->(:Vulnerability {
  vuln_id: "VULN-WTP-001-001",
  title: "Unpatched SCADA system with Modbus vulnerability",
  severity: "CRITICAL",
  impact: "Unauthorized control of water treatment processes"
})-[:REFERENCES_CVE]->(cve_modbus)

CREATE (scada)-[:USES_PROTOCOL]->(:Protocol {
  protocol_name: "Modbus TCP",
  port: 502,
  encryption: false
})-[:HAS_VULNERABILITY]->(:Vulnerability {
  vuln_id: "VULN-PROTOCOL-MODBUS",
  title: "Lack of authentication in Modbus protocol",
  severity: "HIGH"
})
```

### Energy Grid Substation Node

```cypher
CREATE (substation:EnergyInfrastructure:CriticalInfrastructure {
  infrastructure_id: "SUB-042",
  name: "Westside Distribution Substation",
  voltage_primary: 115000.0,     // V
  voltage_secondary: 13800.0,    // V
  capacity: 45000.0,             // kVA
  location: point({longitude: -122.4100, latitude: 37.7850}),
  commissioned_date: datetime("2015-06-20"),
  operational_status: "operational",
  criticality_level: "CRITICAL",
  consequence_of_failure: "CATASTROPHIC",
  saref_uri: "https://example.org/energy#SUB-042"
})

// Grid meters (smart meters)
CREATE (meter:GridMeter:Meter {
  meter_id: "SUB-042-MTR-001",
  meter_type: "Smart Meter",
  obis_code: "1-0:1.8.0*255",
  firmware_version: "3.2.1",
  mac_address: "00:1B:44:11:3A:B7",
  communication_protocol: "DLMS/COSEM",
  phase: "Three-phase",
  voltage_rating: 13800.0,
  current_rating: 2000.0
})

// Breaker control
CREATE (breaker:Actuator {
  device_id: "SUB-042-BRK-001",
  actuator_type: "Circuit Breaker",
  rated_current: 1200.0,         // A
  rated_voltage: 115000.0        // V
})

CREATE (breaker_state:BreakerState:State {
  state_id: "SUB-042-BRK-001-STATE",
  output_state: true,            // Connected
  control_state: 1,              // Connected
  control_mode: 0                // Automatic
})

// RTU (Remote Terminal Unit)
CREATE (rtu:SAREFDevice:ControlSystem {
  device_id: "SUB-042-RTU-001",
  manufacturer: "ABB",
  model: "RTU560",
  firmware_version: "12.3.0",
  communication_protocol: "DNP3"
})

// Power sensors
CREATE (voltage_sensor:Sensor {
  device_id: "SUB-042-VOLT-001",
  sensor_type: "Voltage Transducer",
  measurement_range_max: 120000.0
})

CREATE (current_sensor:Sensor {
  device_id: "SUB-042-CURR-001",
  sensor_type: "Current Transformer",
  measurement_range_max: 2500.0
})

CREATE (power_sensor:Sensor {
  device_id: "SUB-042-PWR-001",
  sensor_type: "Power Transducer"
})

// Relationships
CREATE (substation)-[:CONTAINS_DEVICE]->(meter)
CREATE (substation)-[:CONTAINS_DEVICE]->(breaker)
CREATE (substation)-[:CONTAINS_DEVICE]->(rtu)
CREATE (substation)-[:CONTAINS_DEVICE]->(voltage_sensor)
CREATE (substation)-[:CONTAINS_DEVICE]->(current_sensor)
CREATE (substation)-[:CONTAINS_DEVICE]->(power_sensor)

CREATE (rtu)-[:CONTROLS]->(breaker)
CREATE (breaker)-[:HAS_STATE]->(breaker_state)

CREATE (meter)-[:OBSERVES]->(:EnergyAndPowerProperty {property_type: "ActiveEnergy"})
CREATE (voltage_sensor)-[:OBSERVES]->(:EnergyAndPowerProperty {property_type: "Voltage"})
CREATE (current_sensor)-[:OBSERVES]->(:EnergyAndPowerProperty {property_type: "Current"})
CREATE (power_sensor)-[:OBSERVES]->(:EnergyAndPowerProperty {property_type: "ActivePower"})

// Vulnerabilities
CREATE (cve_dnp3:CVE {
  cve_id: "CVE-2022-5678",
  description: "DNP3 protocol buffer overflow",
  cvss_score: 8.6
})

CREATE (rtu)-[:HAS_VULNERABILITY]->(:Vulnerability {
  vuln_id: "VULN-SUB-042-001",
  title: "RTU firmware vulnerable to remote code execution",
  severity: "CRITICAL",
  impact: "Complete control of substation operations"
})-[:REFERENCES_CVE]->(cve_dnp3)
```

### Manufacturing Facility Node

```cypher
CREATE (factory:Factory:Building:CriticalInfrastructure {
  factory_id: "FAC-ALPHA",
  factory_name: "Advanced Manufacturing Center",
  location: point({longitude: -122.3900, latitude: 37.7650}),
  total_area: 25000.0,           // m²
  production_capacity: 100000.0, // units/month
  employee_count: 450,
  criticality_level: "HIGH",
  saref_uri: "https://saref.etsi.org/saref4inma/Factory#FAC-ALPHA"
})

CREATE (site:Site:BuildingSpace {
  site_id: "FAC-ALPHA-SITE-01",
  site_name: "Main Production Site"
})

CREATE (area:Area:BuildingSpace {
  area_id: "FAC-ALPHA-AREA-01",
  area_name: "Assembly Line Area",
  area_type: "Production"
})

// Production equipment
CREATE (robot:ProductionEquipment:SAREFDevice {
  equipment_id: "FAC-ALPHA-ROBOT-01",
  equipment_category: "AssemblyRobot",
  manufacturer: "FANUC",
  model_number: "M-20iD/25",
  serial_number: "F-123456",
  production_capacity: 500.0     // units/day
})

CREATE (cnc:ProductionEquipment:WorkCenter:SAREFDevice {
  equipment_id: "FAC-ALPHA-CNC-01",
  equipment_category: "MillingMachine",
  manufacturer: "Haas",
  model_number: "VF-4SS"
})

CREATE (plc:SAREFDevice:ControlSystem {
  device_id: "FAC-ALPHA-PLC-01",
  manufacturer: "Siemens",
  model: "S7-1500",
  firmware_version: "V2.9.3",
  communication_protocol: "S7Comm"
})

// Product tracking
CREATE (item_cat:ItemCategory {
  category_id: "PROD-WIDGET-A",
  gtin13_id: "1234567890123",
  model_number: "WDG-A-2023",
  description: "Industrial Widget Type A"
})

CREATE (batch:ItemBatch {
  batch_id: "BATCH-2023-10-001",
  batch_number: "B-231001",
  production_date: datetime("2023-10-01"),
  batch_size: 1000
})

// Relationships
CREATE (factory)-[:CONTAINS_SITE]->(site)
CREATE (site)-[:CONTAINS_AREA]->(area)
CREATE (area)-[:CONTAINS_WORK_CENTER]->(cnc)
CREATE (area)-[:CONTAINS_EQUIPMENT]->(robot)
CREATE (area)-[:CONTAINS_EQUIPMENT]->(plc)

CREATE (plc)-[:CONTROLS]->(robot)
CREATE (plc)-[:CONTROLS]->(cnc)

CREATE (robot)-[:PRODUCES]->(item_cat)
CREATE (item_cat)-[:CATEGORY_OF]->(batch)

// Vulnerabilities
CREATE (robot)-[:HAS_VULNERABILITY]->(:Vulnerability {
  vuln_id: "VULN-FAC-ALPHA-001",
  title: "Unpatched robot controller firmware",
  severity: "HIGH",
  impact: "Potential for unauthorized robot movements causing safety hazards"
})

CREATE (plc)-[:RUNS_SOFTWARE]->(:Software {
  software_name: "Siemens TIA Portal",
  version: "V16"
})-[:HAS_CVE]->(:CVE {
  cve_id: "CVE-2023-9999",
  description: "S7Comm protocol authentication bypass",
  cvss_score: 9.1
})
```

---

## Query Examples

### Find all critical infrastructure with high severity vulnerabilities

```cypher
MATCH (infra:CriticalInfrastructure)-[:HAS_VULNERABILITY]->(v:Vulnerability)
WHERE v.severity IN ['HIGH', 'CRITICAL']
  AND infra.criticality_level = 'CRITICAL'
RETURN infra.name,
       infra.infrastructure_type,
       collect(v.title) as vulnerabilities,
       infra.consequence_of_failure
ORDER BY v.cvss_score DESC
```

### Trace water quality from source to consumer

```cypher
MATCH path = (source:SourceAsset)-[:SUPPLIES|FEEDS|DISTRIBUTES_TO*]->(consumer)
MATCH (sensor:Sensor)-[:MONITORS]-(waterAsset:WaterAsset)
WHERE waterAsset IN nodes(path)
RETURN path,
       collect(sensor.device_id) as monitoring_sensors,
       [prop IN collect(sensor.sensor_type) | prop] as measured_properties
```

### Find all smart grid devices with outdated firmware

```cypher
MATCH (device:GridMeter|EnergyDevice)
WHERE device.firmware_version < "3.0.0"
OPTIONAL MATCH (device)-[:HAS_VULNERABILITY]->(v:Vulnerability)
RETURN device.device_id,
       device.manufacturer,
       device.model,
       device.firmware_version,
       collect(v.title) as known_vulnerabilities
```

### Map manufacturing production chain with equipment dependencies

```cypher
MATCH (factory:Factory)-[:CONTAINS_SITE|CONTAINS_AREA|CONTAINS_WORK_CENTER*]->(equipment:ProductionEquipment)
MATCH (equipment)-[:PRODUCES]->(category:ItemCategory)
OPTIONAL MATCH (equipment)-[:NEEDS_MATERIAL]->(material:MaterialBatch)
RETURN factory.factory_name,
       equipment.equipment_id,
       equipment.equipment_category,
       category.model_number,
       collect(material.material_type) as required_materials
```

### Identify cross-domain infrastructure dependencies

```cypher
// Find water infrastructure dependent on electrical grid
MATCH (water:WaterInfrastructure)-[:CONTAINS_ASSET|CONTROLLED_BY*]->(device:SAREFDevice)
MATCH (device)-[:REQUIRES_POWER]->(:EnergyDevice)
MATCH (energy:EnergyInfrastructure)-[:SUPPLIES_POWER]->(device)
RETURN water.name as water_facility,
       energy.name as power_source,
       collect(device.device_id) as dependent_devices
```

---

## Implementation Roadmap

### Phase 1: Core SAREF Integration (Weeks 1-2)
- [ ] Implement base SAREF-Core device model
- [ ] Create unified property and observation model
- [ ] Integrate with existing vulnerability schema
- [ ] Establish spatial relationships (GeoSpatial indexing)

### Phase 2: Domain Extensions (Weeks 3-5)
- [ ] Implement SAREF-Water infrastructure nodes
- [ ] Implement SAREF-Energy and SAREF-Grid models
- [ ] Implement SAREF-Manufacturing tracking
- [ ] Create SAREF-City administrative hierarchy

### Phase 3: Cross-Domain Integration (Weeks 6-7)
- [ ] Establish infrastructure dependencies
- [ ] Create unified KPI assessment model
- [ ] Implement observation data pipelines
- [ ] Develop cascading failure analysis queries

### Phase 4: Vulnerability Enrichment (Week 8)
- [ ] Link SAREF devices to CVE database
- [ ] Map protocol vulnerabilities across domains
- [ ] Create attack surface analysis queries
- [ ] Implement risk scoring algorithms

---

## References

### SAREF Ontology Sources
- SAREF Core v4.1.1: https://saref.etsi.org/core/v4.1.1/
- SAREF4Water v2.1.1: https://saref.etsi.org/saref4watr/v2.1.1/
- SAREF4Energy v2.1.1: https://saref.etsi.org/saref4ener/v2.1.1/
- SAREF4Grid v2.1.1: https://saref.etsi.org/saref4grid/v2.1.1/
- SAREF4Manufacturing v2.1.1: https://saref.etsi.org/saref4inma/v2.1.1/
- SAREF4City v2.1.1: https://saref.etsi.org/saref4city/v2.1.1/
- SAREF4Building v2.1.1: https://saref.etsi.org/saref4bldg/v2.1.1/

### Standards References
- DLMS/COSEM (IEC 62056)
- Modbus Protocol Specification
- DNP3 (IEEE 1815-2012)
- OBIS (Object Identification System - IEC 62056-61)
- IEC 61512 (Batch Control)
- IEC 62264 (Enterprise-Control System Integration)

---

**Document Status:** Complete
**Next Review Date:** 2025-11-29
**Maintained By:** OXOT Project Team
