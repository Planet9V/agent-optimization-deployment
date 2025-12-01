# SAREF Ontology Research Findings

**File:** 20_RESEARCH_FINDINGS_SAREF.md
**Created:** 2025-10-30 00:00:00 UTC
**Modified:** 2025-10-30 00:00:00 UTC
**Version:** v1.0.0
**Author:** Research Analysis Agent
**Purpose:** Comprehensive documentation of SAREF ontology ecosystem research findings
**Status:** ACTIVE

## Executive Summary

This document presents comprehensive research findings from the analysis of the Smart Applications REFerence (SAREF) ontology ecosystem, covering 13 specialized extensions. SAREF provides a standardized reference model for smart applications across multiple domains, developed by ETSI (European Telecommunications Standards Institute) and maintained as an official standard.

The research encompasses:
- SAREF Core ontology foundational concepts
- 12 domain-specific SAREF extensions
- Cross-domain integration patterns
- IoT device modeling approaches
- Property and measurement frameworks
- Service and function abstractions

**Key Findings:**
- SAREF provides comprehensive IoT device modeling applicable to OT/ICS environments
- Strong alignment with Building Management Systems (BMS) and smart infrastructure
- Extensive property and measurement schema supporting sensor integration
- Service-oriented architecture enabling function abstraction
- Cross-domain patterns applicable to cybersecurity monitoring

## 1. SAREF Core Ontology Analysis

### 1.1 Foundation Architecture

**Namespace:** `https://saref.etsi.org/core/`
**Version Analyzed:** SAREF v3.2.1 (2023)
**Primary Specification:** ETSI TS 103 264

#### Core Design Principles

1. **Device-Centric Modeling**: Focus on physical devices and their capabilities
2. **Function Abstraction**: Separation of what a device does from how it does it
3. **Interoperability**: Standardized vocabulary for cross-domain communication
4. **Modularity**: Extension mechanism for domain-specific vocabularies
5. **Measurement Focus**: Rich property and unit of measurement framework

### 1.2 Core Class Hierarchy

```turtle
saref:Device
  ├── saref:Actuator
  ├── saref:Sensor
  ├── saref:Appliance
  ├── saref:HVAC
  ├── saref:LightingDevice
  ├── saref:Meter
  ├── saref:Multimedia
  ├── saref:Network
  └── saref:SmartDevice

saref:Function
  ├── saref:ActuatingFunction
  ├── saref:SensingFunction
  ├── saref:MeteringFunction
  ├── saref:EventFunction
  └── saref:LevelControlFunction

saref:Service
  ├── saref:GetCommand
  ├── saref:SetCommand
  ├── saref:NotifyService
  └── saref:ToggleCommand

saref:Property
  ├── saref:Energy
  ├── saref:Power
  ├── saref:Temperature
  ├── saref:Humidity
  ├── saref:Light
  ├── saref:Motion
  ├── saref:Occupancy
  ├── saref:Pressure
  └── saref:Smoke

saref:State
  ├── saref:OnState
  ├── saref:OffState
  ├── saref:OpenState
  ├── saref:CloseState
  ├── saref:StartState
  └── saref:StopState
```

### 1.3 Core Object Properties

#### Device Relationships

```turtle
saref:consistsOf
  rdfs:domain saref:Device
  rdfs:range saref:Device
  rdfs:comment "Relationship to represent device composition"

saref:hasFunction
  rdfs:domain saref:Device
  rdfs:range saref:Function
  rdfs:comment "Links device to its capabilities"

saref:hasState
  rdfs:domain saref:Device
  rdfs:range saref:State
  rdfs:comment "Current operational state of device"

saref:hasProfile
  rdfs:domain saref:Device
  rdfs:range saref:Profile
  rdfs:comment "Device operational profile"

saref:controlsProperty
  rdfs:domain saref:Device
  rdfs:range saref:Property
  rdfs:comment "Property controlled by actuator"

saref:measuresProperty
  rdfs:domain saref:Device
  rdfs:range saref:Property
  rdfs:comment "Property measured by sensor"

saref:isUsedFor
  rdfs:domain saref:Device
  rdfs:range saref:Commodity
  rdfs:comment "Resource consumed or produced"
```

#### Function and Service Relationships

```turtle
saref:hasCommand
  rdfs:domain saref:Function
  rdfs:range saref:Command
  rdfs:comment "Command that triggers function"

saref:isCommandOf
  rdfs:domain saref:Command
  rdfs:range saref:Function
  rdfs:comment "Inverse of hasCommand"

saref:actsUpon
  rdfs:domain saref:Command
  rdfs:range saref:State
  rdfs:comment "State affected by command"

saref:hasDescription
  rdfs:domain saref:Service
  rdfs:range xsd:string
  rdfs:comment "Human-readable service description"

saref:hasInput
  rdfs:domain saref:Service
  rdfs:range saref:Property
  rdfs:comment "Required input parameters"

saref:hasOutput
  rdfs:domain saref:Service
  rdfs:range saref:Property
  rdfs:comment "Service output values"
```

#### Measurement and Property Relationships

```turtle
saref:hasProperty
  rdfs:domain saref:FeatureOfInterest
  rdfs:range saref:Property
  rdfs:comment "Observable property of feature"

saref:relatesToProperty
  rdfs:domain saref:Measurement
  rdfs:range saref:Property
  rdfs:comment "Property being measured"

saref:isMeasuredIn
  rdfs:domain saref:Property
  rdfs:range saref:UnitOfMeasure
  rdfs:comment "Measurement unit for property"

saref:hasTimestamp
  rdfs:domain saref:Measurement
  rdfs:range xsd:dateTime
  rdfs:comment "When measurement was taken"

saref:hasValue
  rdfs:domain saref:Measurement
  rdfs:range xsd:float
  rdfs:comment "Measured value"

saref:isMeasuredByDevice
  rdfs:domain saref:Property
  rdfs:range saref:Device
  rdfs:comment "Device performing measurement"
```

### 1.4 Core Data Properties

```turtle
saref:hasManufacturer
  rdfs:domain saref:Device
  rdfs:range xsd:string

saref:hasModel
  rdfs:domain saref:Device
  rdfs:range xsd:string

saref:hasDescription
  rdfs:domain owl:Thing
  rdfs:range xsd:string

saref:hasDeviceID
  rdfs:domain saref:Device
  rdfs:range xsd:string

saref:hasFirmwareVersion
  rdfs:domain saref:Device
  rdfs:range xsd:string

saref:hasProtocol
  rdfs:domain saref:Device
  rdfs:range xsd:string

saref:hasPowerConsumption
  rdfs:domain saref:Device
  rdfs:range xsd:float

saref:hasLocation
  rdfs:domain saref:Device
  rdfs:range xsd:string
```

### 1.5 Measurement and Units Framework

#### Unit of Measure Hierarchy

```turtle
saref:UnitOfMeasure
  ├── saref:TemperatureUnit
  │   ├── saref:Celsius
  │   ├── saref:Fahrenheit
  │   └── saref:Kelvin
  ├── saref:EnergyUnit
  │   ├── saref:KilowattHour
  │   ├── saref:Joule
  │   └── saref:WattHour
  ├── saref:PowerUnit
  │   ├── saref:Watt
  │   ├── saref:Kilowatt
  │   └── saref:Megawatt
  ├── saref:PressureUnit
  │   ├── saref:Pascal
  │   ├── saref:Bar
  │   └── saref:PSI
  └── saref:TimeUnit
      ├── saref:Second
      ├── saref:Minute
      ├── saref:Hour
      └── saref:Day
```

## 2. SAREF4WATR - Water Management Extension

### 2.1 Overview

**Namespace:** `https://saref.etsi.org/saref4watr/`
**Version:** v1.1.1
**Domain:** Water supply, distribution, and quality monitoring

#### Key Objectives
- Model water distribution networks
- Monitor water quality parameters
- Track consumption and leakage
- Integrate with smart meters
- Support water resource management

### 2.2 Water-Specific Classes

```turtle
s4watr:WaterDevice
  rdfs:subClassOf saref:Device
  ├── s4watr:WaterMeter
  ├── s4watr:WaterQualitySensor
  ├── s4watr:FlowSensor
  ├── s4watr:PressureSensor
  ├── s4watr:LeakageDetector
  ├── s4watr:Valve
  ├── s4watr:Pump
  └── s4watr:Tank

s4watr:WaterProperty
  rdfs:subClassOf saref:Property
  ├── s4watr:WaterQuality
  ├── s4watr:FlowRate
  ├── s4watr:WaterPressure
  ├── s4watr:WaterLevel
  ├── s4watr:pH
  ├── s4watr:Turbidity
  ├── s4watr:Chlorine
  ├── s4watr:Conductivity
  └── s4watr:DissolvedOxygen

s4watr:WaterNetwork
  ├── s4watr:DistributionNetwork
  ├── s4watr:SewerNetwork
  └── s4watr:IrrigationNetwork

s4watr:WaterAsset
  ├── s4watr:Pipeline
  ├── s4watr:Junction
  ├── s4watr:Reservoir
  ├── s4watr:TreatmentPlant
  └── s4watr:PumpingStation
```

### 2.3 Water Quality Monitoring

```turtle
s4watr:WaterQualityMeasurement
  rdfs:subClassOf saref:Measurement
  saref:relatesToProperty s4watr:WaterQuality
  s4watr:hasQualityIndicator [
    s4watr:pH
    s4watr:turbidity
    s4watr:chlorineLevel
    s4watr:bacteriaCount
    s4watr:dissolvedOxygen
    s4watr:temperature
  ]
  s4watr:hasQualityStatus [
    s4watr:Safe
    s4watr:Acceptable
    s4watr:Warning
    s4watr:Critical
  ]
```

### 2.4 Flow and Pressure Monitoring

```turtle
s4watr:FlowMeasurement
  rdfs:subClassOf saref:Measurement
  saref:relatesToProperty s4watr:FlowRate
  saref:isMeasuredIn s4watr:LitersPerSecond
  s4watr:hasFlowDirection [
    s4watr:Inbound
    s4watr:Outbound
  ]

s4watr:PressureMeasurement
  rdfs:subClassOf saref:Measurement
  saref:relatesToProperty s4watr:WaterPressure
  saref:isMeasuredIn s4watr:Bar
```

### 2.5 Leakage Detection Patterns

```turtle
s4watr:LeakageEvent
  rdfs:subClassOf s4watr:WaterEvent
  s4watr:hasLeakageRate xsd:float
  s4watr:hasLocation geo:Point
  s4watr:hasSeverity [
    s4watr:Minor
    s4watr:Moderate
    s4watr:Major
    s4watr:Critical
  ]
  s4watr:detectedBy s4watr:LeakageDetector
  s4watr:affectsPipeline s4watr:Pipeline
```

### 2.6 OT/Cybersecurity Integration Points

**Application to AEON-DT:**
1. **Network Infrastructure**: Water distribution as critical infrastructure monitoring model
2. **Sensor Networks**: Large-scale sensor deployment patterns
3. **SCADA Integration**: Industrial control system monitoring
4. **Anomaly Detection**: Flow and pressure anomaly patterns
5. **Asset Management**: Physical asset tracking and lifecycle

**Cybersecurity Relevance:**
- Critical infrastructure protection patterns
- SCADA system vulnerability modeling
- Sensor tampering detection
- Network segmentation requirements
- Access control for industrial devices

## 3. SAREF4ENER - Energy Management Extension

### 3.1 Overview

**Namespace:** `https://saref.etsi.org/saref4ener/`
**Version:** v1.1.2
**Domain:** Energy management, smart grid, demand response

#### Key Objectives
- Model energy generation and consumption
- Support demand response programs
- Enable load management
- Track renewable energy sources
- Integrate with smart grid infrastructure

### 3.2 Energy Device Classes

```turtle
s4ener:Device
  rdfs:subClassOf saref:Device
  ├── s4ener:Generator
  │   ├── s4ener:SolarPanel
  │   ├── s4ener:WindTurbine
  │   ├── s4ener:BatteryStorage
  │   └── s4ener:FuelCell
  ├── s4ener:Load
  │   ├── s4ener:FlexibleLoad
  │   ├── s4ener:CriticalLoad
  │   └── s4ener:ControllableLoad
  ├── s4ener:EnergyMeter
  │   ├── s4ener:SmartMeter
  │   ├── s4ener:SubMeter
  │   └── s4ener:ProductionMeter
  └── s4ener:PowerManagementSystem
```

### 3.3 Energy Properties and Measurements

```turtle
s4ener:EnergyProperty
  rdfs:subClassOf saref:Property
  ├── s4ener:ActivePower
  ├── s4ener:ReactivePower
  ├── s4ener:ApparentPower
  ├── s4ener:PowerFactor
  ├── s4ener:Voltage
  ├── s4ener:Current
  ├── s4ener:Frequency
  ├── s4ener:EnergyConsumption
  └── s4ener:EnergyProduction

s4ener:PowerProfile
  s4ener:hasAlternatives s4ener:Alternative
  s4ener:hasSlot s4ener:Slot
  s4ener:isExpectedBy s4ener:Device

s4ener:Slot
  s4ener:hasTimestamp xsd:dateTime
  s4ener:hasDuration xsd:duration
  s4ener:hasPower xsd:float
  s4ener:hasEnergy xsd:float
```

### 3.4 Demand Response Framework

```turtle
s4ener:DemandResponseEvent
  s4ener:hasEventType [
    s4ener:LoadShedding
    s4ener:LoadShifting
    s4ener:LoadIncrease
    s4ener:PeakShaving
  ]
  s4ener:hasStartTime xsd:dateTime
  s4ener:hasEndTime xsd:dateTime
  s4ener:hasTargetPower xsd:float
  s4ener:hasIncentive xsd:float
  s4ener:affects s4ener:Device

s4ener:LoadControlCommand
  rdfs:subClassOf saref:Command
  s4ener:targetsPowerLevel xsd:float
  s4ener:hasTimeConstraint s4ener:TimeConstraint
```

### 3.5 Renewable Energy Integration

```turtle
s4ener:RenewableGeneration
  s4ener:hasGenerationType [
    s4ener:Solar
    s4ener:Wind
    s4ener:Hydro
    s4ener:Geothermal
    s4ener:Biomass
  ]
  s4ener:hasCapacity xsd:float
  s4ener:hasCurrentProduction xsd:float
  s4ener:hasForecast s4ener:GenerationForecast

s4ener:GenerationForecast
  s4ener:hasTimeHorizon xsd:duration
  s4ener:hasConfidenceLevel xsd:float
  s4ener:hasExpectedProduction xsd:float
```

### 3.6 Power Quality Monitoring

```turtle
s4ener:PowerQualityEvent
  ├── s4ener:VoltageSag
  ├── s4ener:VoltageSwell
  ├── s4ener:Interruption
  ├── s4ener:HarmonicDistortion
  ├── s4ener:FrequencyDeviation
  └── s4ener:Imbalance

s4ener:PowerQualityMeasurement
  s4ener:hasVoltageLevel xsd:float
  s4ener:hasTHD xsd:float  # Total Harmonic Distortion
  s4ener:hasFrequency xsd:float
  s4ener:hasPowerFactor xsd:float
```

### 3.7 OT/Cybersecurity Integration

**Application to AEON-DT:**
1. **Smart Grid Monitoring**: Power grid as cyber-physical system
2. **Energy SCADA**: Industrial control system patterns
3. **Metering Infrastructure**: AMI security modeling
4. **Distributed Energy Resources**: Edge device security
5. **Demand Response**: Command and control security

**Cybersecurity Relevance:**
- Smart meter tampering detection
- False data injection attacks
- Grid stability cyber threats
- DER communication security
- SCADA protocol vulnerabilities

## 4. SAREF4GRID - Smart Grid Extension

### 4.1 Overview

**Namespace:** `https://saref.etsi.org/saref4grid/`
**Version:** v1.0.0
**Domain:** Electrical grid infrastructure, transmission, distribution

### 4.2 Grid Infrastructure Classes

```turtle
s4grid:GridDevice
  rdfs:subClassOf saref:Device
  ├── s4grid:Transformer
  │   ├── s4grid:PowerTransformer
  │   ├── s4grid:DistributionTransformer
  │   └── s4grid:MeasurementTransformer
  ├── s4grid:CircuitBreaker
  ├── s4grid:Disconnector
  ├── s4grid:Recloser
  ├── s4grid:Capacitor
  ├── s4grid:Reactor
  └── s4grid:FaultIndicator

s4grid:GridSegment
  ├── s4grid:TransmissionLine
  ├── s4grid:DistributionLine
  ├── s4grid:Substation
  ├── s4grid:Feeder
  └── s4grid:Bay

s4grid:ProtectionDevice
  ├── s4grid:OvercurrentRelay
  ├── s4grid:DifferentialRelay
  ├── s4grid:DistanceRelay
  └── s4grid:FrequencyRelay
```

### 4.3 Grid Topology Modeling

```turtle
s4grid:ConnectivityNode
  s4grid:connectsTo s4grid:Terminal
  s4grid:hasVoltageLevel xsd:float
  s4grid:isPartOf s4grid:GridSegment

s4grid:Terminal
  s4grid:belongsTo s4grid:GridDevice
  s4grid:hasPhase [
    s4grid:PhaseA
    s4grid:PhaseB
    s4grid:PhaseC
    s4grid:Neutral
  ]
```

### 4.4 Grid Operations and Control

```turtle
s4grid:OperationalState
  ├── s4grid:Energized
  ├── s4grid:DeEnergized
  ├── s4grid:Isolated
  ├── s4grid:MaintenanceMode
  └── s4grid:Faulty

s4grid:ControlCommand
  rdfs:subClassOf saref:Command
  ├── s4grid:SwitchingCommand
  ├── s4grid:LoadControlCommand
  ├── s4grid:VoltageControlCommand
  └── s4grid:ProtectionCommand
```

### 4.5 OT/Cybersecurity Relevance

**Critical Infrastructure Modeling:**
- Substation automation systems
- IED (Intelligent Electronic Device) networks
- SCADA command sequences
- Protection relay coordination
- Grid topology for attack surface analysis

## 5. SAREF4INMA - Manufacturing Extension

### 5.1 Overview

**Namespace:** `https://saref.etsi.org/saref4inma/`
**Version:** v1.2.0
**Domain:** Industrial manufacturing, Industry 4.0, production systems

### 5.2 Manufacturing Device Classes

```turtle
s4inma:ManufacturingDevice
  rdfs:subClassOf saref:Device
  ├── s4inma:Machine
  │   ├── s4inma:CNCMachine
  │   ├── s4inma:Robot
  │   ├── s4inma:AssemblyStation
  │   ├── s4inma:PackagingMachine
  │   └── s4inma:QualityInspection
  ├── s4inma:ProductionLine
  ├── s4inma:Warehouse
  ├── s4inma:ConveyorSystem
  └── s4inma:MaterialHandler

s4inma:Sensor
  rdfs:subClassOf saref:Sensor
  ├── s4inma:VibrationSensor
  ├── s4inma:TemperatureSensor
  ├── s4inma:PressureSensor
  ├── s4inma:ProximitySensor
  ├── s4inma:VisionSensor
  └── s4inma:ForceSensor
```

### 5.3 Production Process Modeling

```turtle
s4inma:ProductionProcess
  s4inma:hasStep s4inma:ProcessStep
  s4inma:requiresMaterial s4inma:Material
  s4inma:producesProduct s4inma:Product
  s4inma:hasKPI s4inma:PerformanceIndicator

s4inma:ProcessStep
  s4inma:hasSequenceNumber xsd:integer
  s4inma:usesMachine s4inma:Machine
  s4inma:hasDuration xsd:duration
  s4inma:hasParameter s4inma:ProcessParameter

s4inma:ProcessParameter
  ├── s4inma:Speed
  ├── s4inma:Temperature
  ├── s4inma:Pressure
  ├── s4inma:FeedRate
  └── s4inma:ToolPosition
```

### 5.4 Manufacturing KPIs

```turtle
s4inma:PerformanceIndicator
  ├── s4inma:OEE  # Overall Equipment Effectiveness
  ├── s4inma:Availability
  ├── s4inma:Performance
  ├── s4inma:Quality
  ├── s4inma:MTBF  # Mean Time Between Failures
  ├── s4inma:MTTR  # Mean Time To Repair
  ├── s4inma:Throughput
  └── s4inma:CycleTime

s4inma:OEEMeasurement
  s4inma:hasAvailability xsd:float
  s4inma:hasPerformance xsd:float
  s4inma:hasQuality xsd:float
  s4inma:calculatedOEE xsd:float
```

### 5.5 Predictive Maintenance

```turtle
s4inma:MaintenanceEvent
  ├── s4inma:PreventiveMaintenance
  ├── s4inma:PredictiveMaintenance
  ├── s4inma:CorrectiveMaintenance
  └── s4inma:EmergencyMaintenance

s4inma:HealthStatus
  s4inma:hasHealthScore xsd:float
  s4inma:hasRemainingUsefulLife xsd:duration
  s4inma:hasAnomalyScore xsd:float
  s4inma:requiresMaintenance xsd:boolean
```

### 5.6 OT/Cybersecurity Integration

**Industrial Control Systems:**
- PLC and DCS device modeling
- Industrial protocol patterns (Modbus, OPC-UA, PROFINET)
- Machine-to-machine communication
- Production network segmentation
- Safety system integration (SIS)

**Cybersecurity Applications:**
- ICS network topology mapping
- Anomaly detection in manufacturing
- Ransomware impact on production
- Supply chain cyber risks
- Industrial IoT device security

## 6. SAREF4AGRI - Agriculture Extension

### 6.1 Overview

**Namespace:** `https://saref.etsi.org/saref4agri/`
**Version:** v1.1.2
**Domain:** Precision agriculture, smart farming, livestock management

### 6.2 Agricultural Device Classes

```turtle
s4agri:FarmDevice
  rdfs:subClassOf saref:Device
  ├── s4agri:Tractor
  ├── s4agri:Harvester
  ├── s4agri:Seeder
  ├── s4agri:Sprayer
  ├── s4agri:IrrigationSystem
  ├── s4agri:WeatherStation
  ├── s4agri:SoilSensor
  └── s4agri:AnimalTracker

s4agri:Sensor
  ├── s4agri:SoilMoistureSensor
  ├── s4agri:SoilpHSensor
  ├── s4agri:WeatherSensor
  ├── s4agri:CropHealthSensor
  └── s4agri:LivestockMonitor
```

### 6.3 Crop and Field Management

```turtle
s4agri:Farm
  s4agri:hasField s4agri:Field
  s4agri:hasCrop s4agri:Crop
  s4agri:hasBuilding s4agri:Building

s4agri:Field
  s4agri:hasArea xsd:float
  s4agri:hasSoilType s4agri:SoilType
  s4agri:hasIrrigationSystem s4agri:IrrigationSystem
  s4agri:hasCrop s4agri:Crop

s4agri:Crop
  s4agri:hasCropType xsd:string
  s4agri:hasPlantingDate xsd:date
  s4agri:hasExpectedHarvestDate xsd:date
  s4agri:hasGrowthStage s4agri:GrowthStage
```

### 6.4 Livestock Management

```turtle
s4agri:Animal
  s4agri:hasAnimalID xsd:string
  s4agri:hasSpecies xsd:string
  s4agri:hasBreed xsd:string
  s4agri:hasBirthDate xsd:date
  s4agri:hasWeight xsd:float
  s4agri:hasHealthStatus s4agri:HealthStatus
  s4agri:hasLocation geo:Point

s4agri:LivestockMonitoring
  s4agri:tracksAnimal s4agri:Animal
  s4agri:measuresActivity xsd:float
  s4agri:measuresTemperature xsd:float
  s4agri:detectsAnomaly xsd:boolean
```

### 6.5 Environmental Monitoring

```turtle
s4agri:WeatherMeasurement
  s4agri:hasTemperature xsd:float
  s4agri:hasHumidity xsd:float
  s4agri:hasPrecipitation xsd:float
  s4agri:hasWindSpeed xsd:float
  s4agri:hasSolarRadiation xsd:float

s4agri:SoilMeasurement
  s4agri:hasMoisture xsd:float
  s4agri:hasTemperature xsd:float
  s4agri:haspH xsd:float
  s4agri:hasNutrientLevel s4agri:NutrientLevel
```

### 6.6 OT/Cybersecurity Relevance

**Agricultural Technology:**
- Autonomous vehicle control systems
- Precision agriculture networks
- Remote farm management systems
- Livestock tracking and monitoring
- Supply chain integration

**Security Considerations:**
- GPS spoofing risks
- Autonomous equipment hijacking
- Data integrity for compliance
- Remote access vulnerabilities
- Supply chain contamination

## 7. SAREF4CITY - Smart City Extension

### 7.1 Overview

**Namespace:** `https://saref.etsi.org/saref4city/`
**Version:** v1.1.1
**Domain:** Urban infrastructure, smart cities, municipal services

### 7.2 City Infrastructure Classes

```turtle
s4city:CityDevice
  rdfs:subClassOf saref:Device
  ├── s4city:StreetLight
  ├── s4city:ParkingSensor
  ├── s4city:TrafficLight
  ├── s4city:TrafficSensor
  ├── s4city:AirQualitySensor
  ├── s4city:NoiseSensor
  ├── s4city:WasteContainer
  ├── s4city:PublicTransportVehicle
  └── s4city:ChargingStation

s4city:PublicFacility
  ├── s4city:Park
  ├── s4city:ParkingLot
  ├── s4city:PublicBuilding
  ├── s4city:TransportStation
  └── s4city:ServicePoint
```

### 7.3 Transportation Management

```turtle
s4city:TransportationSystem
  s4city:hasVehicle s4city:Vehicle
  s4city:hasRoute s4city:Route
  s4city:hasStop s4city:TransportStop

s4city:TrafficManagement
  s4city:measuresTrafficFlow xsd:float
  s4city:measuresOccupancy xsd:float
  s4city:detectsCongestion xsd:boolean
  s4city:hasIncident s4city:TrafficIncident

s4city:ParkingManagement
  s4city:hasCapacity xsd:integer
  s4city:hasOccupancy xsd:integer
  s4city:hasAvailableSpaces xsd:integer
  s4city:hasParkingRate xsd:float
```

### 7.4 Environmental Monitoring

```turtle
s4city:AirQuality
  s4city:measuresPM25 xsd:float
  s4city:measuresPM10 xsd:float
  s4city:measuresNO2 xsd:float
  s4city:measuresO3 xsd:float
  s4city:measuresCO xsd:float
  s4city:hasAQI xsd:integer  # Air Quality Index

s4city:NoiseLevel
  s4city:measuresDecibels xsd:float
  s4city:hasNoiseType [
    s4city:Traffic
    s4city:Construction
    s4city:Industrial
    s4city:Recreation
  ]
```

### 7.5 Waste Management

```turtle
s4city:WasteManagement
  s4city:hasContainer s4city:WasteContainer
  s4city:hasCollectionRoute s4city:Route
  s4city:hasSchedule s4city:Schedule

s4city:WasteContainer
  s4city:hasFillLevel xsd:float
  s4city:hasCapacity xsd:float
  s4city:hasWasteType [
    s4city:General
    s4city:Recyclable
    s4city:Organic
    s4city:Hazardous
  ]
  s4city:requiresCollection xsd:boolean
```

### 7.6 OT/Cybersecurity Integration

**Smart City Infrastructure:**
- Traffic management systems
- Intelligent transportation systems (ITS)
- Street lighting SCADA
- Environmental monitoring networks
- Public safety systems

**Cybersecurity Applications:**
- Critical infrastructure interdependencies
- Traffic signal tampering
- Surveillance system security
- Public Wi-Fi network risks
- IoT device proliferation risks

## 8. SAREF4BLDG - Building Management Extension

### 8.1 Overview

**Namespace:** `https://saref.etsi.org/saref4bldg/`
**Version:** v1.1.2
**Domain:** Building automation, HVAC, lighting, access control

**Key Standards Alignment:**
- IFC (Industry Foundation Classes)
- BACnet protocol
- LON (LonWorks) protocol
- KNX building automation

### 8.2 Building Device Hierarchy

```turtle
s4bldg:BuildingDevice
  rdfs:subClassOf saref:Device
  ├── s4bldg:HVAC
  │   ├── s4bldg:AirConditioner
  │   ├── s4bldg:Boiler
  │   ├── s4bldg:Chiller
  │   ├── s4bldg:FanCoil
  │   ├── s4bldg:HeatPump
  │   ├── s4bldg:VentilationUnit
  │   └── s4bldg:Thermostat
  ├── s4bldg:LightingDevice
  │   ├── s4bldg:Lamp
  │   ├── s4bldg:LightController
  │   └── s4bldg:OccupancySensor
  ├── s4bldg:SecurityDevice
  │   ├── s4bldg:AccessController
  │   ├── s4bldg:AlarmSystem
  │   ├── s4bldg:Camera
  │   └── s4bldg:MotionDetector
  ├── s4bldg:EnergyDevice
  │   ├── s4bldg:EnergyMeter
  │   ├── s4bldg:SubMeter
  │   └── s4bldg:LoadController
  └── s4bldg:Actuator
      ├── s4bldg:Damper
      ├── s4bldg:Valve
      └── s4bldg:Switch
```

### 8.3 Building Spaces and Zones

```turtle
s4bldg:Building
  s4bldg:hasStorey s4bldg:BuildingStorey
  s4bldg:hasSpace s4bldg:BuildingSpace
  s4bldg:hasZone s4bldg:Zone

s4bldg:BuildingSpace
  s4bldg:hasSpaceType [
    s4bldg:Office
    s4bldg:MeetingRoom
    s4bldg:Corridor
    s4bldg:Lobby
    s4bldg:TechnicalRoom
  ]
  s4bldg:hasArea xsd:float
  s4bldg:hasOccupancy xsd:integer
  s4bldg:hasDevice s4bldg:BuildingDevice

s4bldg:Zone
  s4bldg:includesSpace s4bldg:BuildingSpace
  s4bldg:hasZoneType [
    s4bldg:ThermalZone
    s4bldg:LightingZone
    s4bldg:SecurityZone
    s4bldg:FireZone
  ]
```

### 8.4 HVAC System Modeling

```turtle
s4bldg:HVACSystem
  s4bldg:hasComponent s4bldg:HVAC
  s4bldg:servesZone s4bldg:ThermalZone
  s4bldg:hasSetpoint s4bldg:Setpoint
  s4bldg:hasSchedule s4bldg:OperatingSchedule

s4bldg:ThermalZone
  s4bldg:hasTemperature xsd:float
  s4bldg:hasHumidity xsd:float
  s4bldg:hasTargetTemperature xsd:float
  s4bldg:hasOccupancy xsd:integer
  s4bldg:hasComfortLevel xsd:float

s4bldg:AirFlowMeasurement
  s4bldg:hasFlowRate xsd:float
  s4bldg:hasTemperature xsd:float
  s4bldg:hasPressure xsd:float
  s4bldg:hasHumidity xsd:float
  s4bldg:hasCO2Level xsd:float
```

### 8.5 Lighting Control Systems

```turtle
s4bldg:LightingSystem
  s4bldg:hasLightingDevice s4bldg:LightingDevice
  s4bldg:servesZone s4bldg:LightingZone
  s4bldg:hasLightingMode [
    s4bldg:Automatic
    s4bldg:Manual
    s4bldg:PresenceBased
    s4bldg:DaylightHarvesting
    s4bldg:SceneMode
  ]

s4bldg:IlluminanceMeasurement
  s4bldg:hasLightLevel xsd:float
  s4bldg:measuredIn s4bldg:Lux
  s4bldg:hasLocation geo:Point
```

### 8.6 Access Control and Security

```turtle
s4bldg:AccessControlSystem
  s4bldg:hasAccessPoint s4bldg:AccessController
  s4bldg:managesZone s4bldg:SecurityZone
  s4bldg:hasAccessPolicy s4bldg:AccessPolicy

s4bldg:AccessEvent
  s4bldg:hasTimestamp xsd:dateTime
  s4bldg:hasUser s4bldg:User
  s4bldg:hasAccessPoint s4bldg:AccessController
  s4bldg:hasResult [
    s4bldg:Granted
    s4bldg:Denied
    s4bldg:Alarm
  ]
  s4bldg:hasCredentialType [
    s4bldg:Card
    s4bldg:PIN
    s4bldg:Biometric
    s4bldg:Mobile
  ]
```

### 8.7 Energy Management in Buildings

```turtle
s4bldg:EnergyManagementSystem
  s4bldg:monitorsMeter s4bldg:EnergyMeter
  s4bldg:controlsLoad s4bldg:LoadController
  s4bldg:hasEnergyStrategy [
    s4bldg:LoadShedding
    s4bldg:DemandResponse
    s4bldg:PeakShaving
    s4bldg:OptimalStart
  ]

s4bldg:EnergyConsumption
  s4bldg:hasConsumptionType [
    s4bldg:Heating
    s4bldg:Cooling
    s4bldg:Lighting
    s4bldg:Equipment
    s4bldg:Total
  ]
  s4bldg:hasValue xsd:float
  s4bldg:hasPeriod xsd:duration
```

### 8.8 OT/Cybersecurity Integration

**Building Management Systems (BMS):**
- BACnet protocol security
- Building network segmentation
- Integration with IT networks
- Cloud-connected building systems
- Physical-cyber convergence

**Critical Cybersecurity Applications:**
- HVAC as network pivot point
- Access control system vulnerabilities
- Video surveillance security
- Fire and life safety systems
- Remote building management risks

**High Relevance to AEON-DT:**
Building automation systems represent significant cyber-physical integration with:
- Multiple network protocols (BACnet, Modbus, LON)
- Legacy system integration
- Physical security integration
- Energy infrastructure connection
- Cloud service integration

## 9. SAREF4AUTO - Automotive Extension

### 9.1 Overview

**Namespace:** `https://saref.etsi.org/saref4auto/`
**Version:** v1.0.1
**Domain:** Connected vehicles, automotive systems, V2X communication

### 9.2 Vehicle Device Classes

```turtle
s4auto:Vehicle
  rdfs:subClassOf saref:Device
  s4auto:hasVehicleType [
    s4auto:PassengerCar
    s4auto:Truck
    s4auto:Bus
    s4auto:Motorcycle
  ]
  s4auto:hasSystem s4auto:VehicleSystem
  s4auto:hasComponent s4auto:VehicleComponent

s4auto:VehicleSystem
  ├── s4auto:Powertrain
  │   ├── s4auto:Engine
  │   ├── s4auto:Transmission
  │   └── s4auto:Battery
  ├── s4auto:Chassis
  │   ├── s4auto:Suspension
  │   ├── s4auto:Braking
  │   └── s4auto:Steering
  ├── s4auto:Body
  │   ├── s4auto:Doors
  │   ├── s4auto:Windows
  │   └── s4auto:Lighting
  └── s4auto:Electronics
      ├── s4auto:ECU
      ├── s4auto:Infotainment
      └── s4auto:ADAS
```

### 9.3 Vehicle-to-Everything (V2X) Communication

```turtle
s4auto:V2XCommunication
  ├── s4auto:V2V  # Vehicle-to-Vehicle
  ├── s4auto:V2I  # Vehicle-to-Infrastructure
  ├── s4auto:V2P  # Vehicle-to-Pedestrian
  └── s4auto:V2N  # Vehicle-to-Network

s4auto:V2XMessage
  s4auto:hasMessageType [
    s4auto:CAM  # Cooperative Awareness Message
    s4auto:DENM  # Decentralized Environmental Notification
    s4auto:BSM  # Basic Safety Message
    s4auto:SPaT  # Signal Phase and Timing
  ]
  s4auto:hasPosition geo:Point
  s4auto:hasVelocity xsd:float
  s4auto:hasHeading xsd:float
```

### 9.4 Advanced Driver Assistance Systems (ADAS)

```turtle
s4auto:ADAS
  ├── s4auto:AdaptiveCruiseControl
  ├── s4auto:LaneKeepingAssist
  ├── s4auto:AutomaticEmergencyBraking
  ├── s4auto:BlindSpotDetection
  ├── s4auto:ParkingAssist
  └── s4auto:TrafficSignRecognition

s4auto:ADASEvent
  s4auto:hasEventType [
    s4auto:Warning
    s4auto:Intervention
    s4auto:Override
  ]
  s4auto:hasSeverity xsd:integer
  s4auto:hasTimestamp xsd:dateTime
```

### 9.5 Vehicle Diagnostics

```turtle
s4auto:DiagnosticTroubleCode
  s4auto:hasDTCCode xsd:string
  s4auto:hasDescription xsd:string
  s4auto:affectsSystem s4auto:VehicleSystem
  s4auto:hasSeverity [
    s4auto:Critical
    s4auto:Major
    s4auto:Minor
    s4auto:Informational
  ]

s4auto:VehicleHealth
  s4auto:hasOdometerReading xsd:float
  s4auto:hasFuelLevel xsd:float
  s4auto:hasBatteryStatus xsd:float
  s4auto:hasMaintenanceStatus s4auto:MaintenanceStatus
```

### 9.6 OT/Cybersecurity Relevance

**Automotive Cybersecurity:**
- CAN bus vulnerabilities
- Telematics system security
- Over-the-air (OTA) updates
- ECU network segmentation
- V2X communication security

**Connected Vehicle Risks:**
- Remote vehicle hijacking
- Infotainment system attacks
- GPS spoofing
- Keyless entry vulnerabilities
- Supply chain attacks on components

## 10. SAREF4ENVI - Environment Extension

### 10.1 Overview

**Namespace:** `https://saref.etsi.org/saref4envi/`
**Version:** v1.0.0
**Domain:** Environmental monitoring, air/water quality, weather

### 10.2 Environmental Monitoring Classes

```turtle
s4envi:EnvironmentalSensor
  rdfs:subClassOf saref:Sensor
  ├── s4envi:AirQualitySensor
  ├── s4envi:WaterQualitySensor
  ├── s4envi:SoilSensor
  ├── s4envi:NoiseSensor
  ├── s4envi:RadiationSensor
  └── s4envi:WeatherSensor

s4envi:EnvironmentalProperty
  rdfs:subClassOf saref:Property
  ├── s4envi:AirQuality
  ├── s4envi:WaterQuality
  ├── s4envi:NoiseLevel
  ├── s4envi:Temperature
  ├── s4envi:Humidity
  ├── s4envi:AtmosphericPressure
  └── s4envi:WindSpeed
```

### 10.3 Air Quality Monitoring

```turtle
s4envi:AirQualityMeasurement
  s4envi:measuresPollutant [
    s4envi:PM25
    s4envi:PM10
    s4envi:NO2
    s4envi:SO2
    s4envi:CO
    s4envi:O3
    s4envi:VOC
  ]
  s4envi:hasConcentration xsd:float
  s4envi:hasAQI xsd:integer
  s4envi:hasHealthImpact [
    s4envi:Good
    s4envi:Moderate
    s4envi:UnhealthyForSensitive
    s4envi:Unhealthy
    s4envi:VeryUnhealthy
    s4envi:Hazardous
  ]
```

### 10.4 Weather and Climate Monitoring

```turtle
s4envi:WeatherMeasurement
  s4envi:hasTemperature xsd:float
  s4envi:hasHumidity xsd:float
  s4envi:hasPressure xsd:float
  s4envi:hasWindSpeed xsd:float
  s4envi:hasWindDirection xsd:float
  s4envi:hasPrecipitation xsd:float
  s4envi:hasVisibility xsd:float
  s4envi:hasSolarRadiation xsd:float
```

### 10.5 OT/Cybersecurity Applications

**Environmental Monitoring Networks:**
- Large-scale sensor deployments
- Remote station security
- Data integrity for compliance
- Early warning systems
- Industrial emission monitoring

## 11. SAREF4HEALTH - Healthcare Extension

### 11.1 Overview

**Namespace:** `https://saref.etsi.org/saref4health/`
**Version:** v1.0.0
**Domain:** Healthcare devices, patient monitoring, medical systems

### 11.2 Medical Device Classes

```turtle
s4health:MedicalDevice
  rdfs:subClassOf saref:Device
  ├── s4health:DiagnosticDevice
  │   ├── s4health:BloodPressureMonitor
  │   ├── s4health:Thermometer
  │   ├── s4health:PulseOximeter
  │   ├── s4health:ECG
  │   └── s4health:GlucoseMeter
  ├── s4health:TherapeuticDevice
  │   ├── s4health:InfusionPump
  │   ├── s4health:Ventilator
  │   ├── s4health:Defibrillator
  │   └── s4health:PaceMaker
  └── s4health:MonitoringDevice
      ├── s4health:PatientMonitor
      ├── s4health:WearableDevice
      └── s4health:ActivityTracker
```

### 11.3 Health Measurements

```turtle
s4health:VitalSign
  ├── s4health:HeartRate
  ├── s4health:BloodPressure
  ├── s4health:BodyTemperature
  ├── s4health:RespiratoryRate
  ├── s4health:OxygenSaturation
  └── s4health:BloodGlucose

s4health:HealthMeasurement
  s4health:measuresVitalSign s4health:VitalSign
  s4health:hasValue xsd:float
  s4health:hasUnit saref:UnitOfMeasure
  s4health:hasTimestamp xsd:dateTime
  s4health:relatesTo s4health:Patient
```

### 11.4 Patient Monitoring

```turtle
s4health:Patient
  s4health:hasPatientID xsd:string
  s4health:hasAge xsd:integer
  s4health:hasCondition s4health:MedicalCondition
  s4health:isMonitoredBy s4health:MonitoringDevice
  s4health:hasAlert s4health:HealthAlert

s4health:HealthAlert
  s4health:hasAlertType [
    s4health:Critical
    s4health:Warning
    s4health:Information
  ]
  s4health:hasParameter s4health:VitalSign
  s4health:hasThreshold xsd:float
  s4health:triggeredAt xsd:dateTime
```

### 11.5 OT/Cybersecurity in Healthcare

**Medical Device Security:**
- Infusion pump vulnerabilities
- Pacemaker/ICD remote access
- Hospital network segmentation
- DICOM protocol security
- HL7 FHIR integration security

**Critical Vulnerabilities:**
- Life-safety system attacks
- Patient data integrity
- Remote medical device control
- Pharmaceutical manufacturing systems
- Hospital building automation

## 12. SAREF4LIFT - Elevator Extension

### 12.1 Overview

**Namespace:** `https://saref.etsi.org/saref4lift/`
**Version:** v1.0.0
**Domain:** Elevator systems, vertical transportation

### 12.2 Elevator System Classes

```turtle
s4lift:Elevator
  rdfs:subClassOf saref:Device
  s4lift:hasLiftType [
    s4lift:Passenger
    s4lift:Freight
    s4lift:Service
    s4lift:Hydraulic
    s4lift:Traction
  ]
  s4lift:servesFloor s4lift:Floor
  s4lift:hasCapacity xsd:integer
  s4lift:hasMaxLoad xsd:float

s4lift:ElevatorComponent
  ├── s4lift:Car
  ├── s4lift:Door
  ├── s4lift:Motor
  ├── s4lift:Controller
  ├── s4lift:SafetySystem
  └── s4lift:CallPanel
```

### 12.3 Elevator Operations

```turtle
s4lift:ElevatorState
  ├── s4lift:Idle
  ├── s4lift:Moving
  ├── s4lift:Loading
  ├── s4lift:Maintenance
  └── s4lift:Emergency

s4lift:ElevatorEvent
  s4lift:hasEventType [
    s4lift:CallRegistered
    s4lift:DoorOpened
    s4lift:DoorClosed
    s4lift:FloorReached
    s4lift:EmergencyStop
    s4lift:Overload
  ]
  s4lift:atFloor s4lift:Floor
  s4lift:hasTimestamp xsd:dateTime
```

### 12.4 Safety and Monitoring

```turtle
s4lift:SafetySystem
  s4lift:hasOverloadDetection xsd:boolean
  s4lift:hasEmergencyBrake xsd:boolean
  s4lift:hasFireService xsd:boolean
  s4lift:hasEarthquakeMode xsd:boolean

s4lift:MaintenanceMonitoring
  s4lift:hasDoorCycles xsd:integer
  s4lift:hasTripCount xsd:integer
  s4lift:hasOperatingHours xsd:float
  s4lift:requiresMaintenance xsd:boolean
```

### 12.5 OT/Cybersecurity Relevance

**Elevator Control Systems:**
- Building integration vulnerabilities
- Remote monitoring systems
- Emergency override security
- Physical safety implications
- Access control integration

## 13. SAREF4WEAR - Wearables Extension

### 13.1 Overview

**Namespace:** `https://saref.etsi.org/saref4wear/`
**Version:** v1.0.0
**Domain:** Wearable devices, personal health tracking

### 13.2 Wearable Device Classes

```turtle
s4wear:WearableDevice
  rdfs:subClassOf saref:Device
  ├── s4wear:Smartwatch
  ├── s4wear:FitnessTracker
  ├── s4wear:SmartGlasses
  ├── s4wear:HeartRateMonitor
  ├── s4wear:SmartClothing
  └── s4wear:HealthPatch

s4wear:WearableProperty
  rdfs:subClassOf saref:Property
  ├── s4wear:StepCount
  ├── s4wear:HeartRate
  ├── s4wear:CaloriesBurned
  ├── s4wear:SleepQuality
  ├── s4wear:StressLevel
  └── s4wear:ActivityLevel
```

### 13.3 Activity Tracking

```turtle
s4wear:ActivityMeasurement
  s4wear:hasActivityType [
    s4wear:Walking
    s4wear:Running
    s4wear:Cycling
    s4wear:Swimming
    s4wear:Sleeping
  ]
  s4wear:hasDuration xsd:duration
  s4wear:hasIntensity xsd:float
  s4wear:hasDistance xsd:float
```

### 13.4 OT/Cybersecurity Context

**Wearable Security:**
- Personal data privacy
- Bluetooth vulnerabilities
- Location tracking risks
- Health data integrity
- Integration with medical devices

## 14. Cross-Domain Integration Patterns

### 14.1 Common Integration Approaches

**Pattern 1: Device Composition**
```turtle
# Complex device made of multiple SAREF devices
:IndustrialFacility a saref:Device ;
  saref:consistsOf :HVACSystem ;
  saref:consistsOf :LightingSystem ;
  saref:consistsOf :AccessControlSystem ;
  saref:consistsOf :EnergyManagementSystem .

:HVACSystem a s4bldg:HVACSystem ;
  s4bldg:hasComponent :Boiler1 ;
  s4bldg:hasComponent :Chiller1 .

:Boiler1 a s4bldg:Boiler ;
  saref:measuresProperty :Temperature ;
  saref:consumesEnergy :NaturalGas .
```

**Pattern 2: Property Sharing**
```turtle
# Same property measured by different domain devices
:Temperature a saref:Property ;
  saref:isMeasuredByDevice :ThermostatBldg ;
  saref:isMeasuredByDevice :WeatherStationCity ;
  saref:isMeasuredByDevice :SoilSensorAgri .

:ThermostatBldg a s4bldg:Thermostat .
:WeatherStationCity a s4city:WeatherStation .
:SoilSensorAgri a s4agri:SoilSensor .
```

**Pattern 3: Unified Measurement Framework**
```turtle
# Consistent measurement approach across domains
:TempMeasurement1 a saref:Measurement ;
  saref:relatesToProperty :Temperature ;
  saref:hasValue "22.5"^^xsd:float ;
  saref:isMeasuredIn :DegreeCelsius ;
  saref:hasTimestamp "2025-10-30T12:00:00Z"^^xsd:dateTime .
```

### 14.2 Multi-Domain Facility Modeling

**Smart Building + Energy + Water Integration:**
```turtle
:CorporateHeadquarters a s4bldg:Building ;
  saref:consistsOf :FloorSystem ;
  s4ener:hasEnergyManagement :EMSystem ;
  s4watr:hasWaterManagement :WaterSystem .

:EMSystem a s4ener:PowerManagementSystem ;
  s4ener:monitors :MainMeter ;
  s4ener:controls :HVACLoads ;
  s4ener:participatesIn :DemandResponseProgram .

:WaterSystem a s4watr:WaterManagement ;
  s4watr:monitors :WaterMeter ;
  s4watr:detectsLeakage :LeakageDetector1 ;
  s4watr:measuresQuality :WaterQualitySensor1 .
```

### 14.3 Industrial Facility Integration

**Manufacturing + Energy + Building:**
```turtle
:ManufacturingPlant a s4inma:Factory ;
  saref:consistsOf :ProductionLine1 ;
  saref:consistsOf :WarehouseArea ;
  s4bldg:hasHVACSystem :IndustrialHVAC ;
  s4ener:hasEnergyManagement :PlantEMS .

:ProductionLine1 a s4inma:ProductionLine ;
  s4inma:hasStep :AssemblyStep ;
  s4inma:hasStep :TestingStep ;
  s4inma:hasStep :PackagingStep .

:AssemblyStep a s4inma:ProcessStep ;
  s4inma:usesMachine :Robot1 ;
  s4inma:hasEnergyConsumption :EnergyProfile1 .

:Robot1 a s4inma:Robot ;
  saref:hasState :OperatingState ;
  s4inma:hasHealthStatus :HealthMonitor1 .
```

### 14.4 Smart City Infrastructure Integration

**City + Transportation + Energy + Environment:**
```turtle
:SmartCity a s4city:City ;
  s4city:hasDistrict :DowntownDistrict ;
  s4city:hasTransportSystem :PublicTransit ;
  s4grid:hasElectricalGrid :CityGrid ;
  s4envi:hasEnvironmentalMonitoring :AirQualityNetwork .

:DowntownDistrict a s4city:District ;
  s4city:hasStreetLighting :LEDSystem ;
  s4city:hasParking :SmartParkingSystem ;
  s4city:hasTrafficManagement :TrafficControlCenter .

:LEDSystem a s4city:StreetLightingSystem ;
  s4bldg:hasLightingDevice :StreetLight001 ;
  s4ener:hasEnergyConsumption :LightingEnergy ;
  s4city:adaptsToDaylight true .
```

## 15. OT/ICS Cybersecurity Application Framework

### 15.1 SAREF Device Security Modeling

**Extending SAREF for Cybersecurity:**
```turtle
# Proposed SAREF extensions for security
saref:hasSecurityProfile
  rdfs:domain saref:Device
  rdfs:range cyber:SecurityProfile

saref:hasCommunicationProtocol
  rdfs:domain saref:Device
  rdfs:range cyber:Protocol

saref:hasVulnerability
  rdfs:domain saref:Device
  rdfs:range cyber:Vulnerability

saref:hasNetworkInterface
  rdfs:domain saref:Device
  rdfs:range cyber:NetworkInterface
```

### 15.2 Critical Infrastructure Device Mapping

**Building Devices to ICS Components:**
```turtle
:HVACController a s4bldg:Thermostat ;
  saref:hasManufacturer "Siemens" ;
  saref:hasModel "RDF600" ;
  saref:hasFirmwareVersion "3.2.1" ;
  saref:hasCommunicationProtocol cyber:BACnet ;
  cyber:hasIPAddress "192.168.10.50" ;
  cyber:exposedToNetwork cyber:BuildingNetwork ;
  cyber:hasVulnerability cyber:CVE-2023-12345 .
```

**Manufacturing Devices to ICS:**
```turtle
:PLC1 a s4inma:Machine ;
  saref:hasManufacturer "Allen-Bradley" ;
  saref:hasModel "ControlLogix 5580" ;
  saref:hasFirmwareVersion "32.011" ;
  saref:hasCommunicationProtocol cyber:EtherNetIP ;
  cyber:hasIPAddress "192.168.100.10" ;
  cyber:connectedTo :SCADA_Server ;
  cyber:hasVulnerability cyber:CVE-2024-54321 .
```

### 15.3 Network Segmentation Modeling

**SAREF Devices in Network Zones:**
```turtle
:ProductionZone a cyber:NetworkZone ;
  cyber:hasSecurityLevel cyber:Level3_ICS ;
  cyber:containsDevice :PLC1 ;
  cyber:containsDevice :Robot1 ;
  cyber:containsDevice :VisionSystem1 ;
  cyber:isolatedFrom :EnterpriseZone .

:BuildingZone a cyber:NetworkZone ;
  cyber:hasSecurityLevel cyber:Level2_BMS ;
  cyber:containsDevice :HVACController ;
  cyber:containsDevice :LightingController ;
  cyber:containsDevice :AccessControlPanel ;
  cyber:bridgedTo :EnterpriseZone .
```

### 15.4 Anomaly Detection Patterns

**SAREF Measurement Anomalies:**
```turtle
:TemperatureAnomaly a cyber:Anomaly ;
  cyber:affectsDevice :Boiler1 ;
  cyber:affectsProperty saref:Temperature ;
  cyber:expectedRange "70-90"^^xsd:string ;
  cyber:observedValue "150.0"^^xsd:float ;
  cyber:anomalyType cyber:OutOfRange ;
  cyber:severity cyber:High ;
  cyber:timestamp "2025-10-30T14:23:11Z"^^xsd:dateTime .

:FlowRateAnomaly a cyber:Anomaly ;
  cyber:affectsDevice :WaterMeter1 ;
  cyber:affectsProperty s4watr:FlowRate ;
  cyber:expectedPattern cyber:NormalDiurnal ;
  cyber:observedPattern cyber:ContinuousHighFlow ;
  cyber:anomalyType cyber:PossibleLeakage ;
  cyber:severity cyber:Medium .
```

### 15.5 State-Based Security Monitoring

**Device State Transitions:**
```turtle
:UnauthorizedStateChange a cyber:SecurityEvent ;
  cyber:affectsDevice :AccessControlPanel ;
  cyber:previousState saref:LockedState ;
  cyber:newState saref:UnlockedState ;
  cyber:triggeredBy cyber:UnknownSource ;
  cyber:lacksAuthorization true ;
  cyber:timestamp "2025-10-30T02:15:33Z"^^xsd:dateTime .

:SuspiciousCommand a cyber:SecurityEvent ;
  cyber:affectsDevice :IndustrialValve ;
  cyber:commandType saref:SetCommand ;
  cyber:commandSource cyber:UnauthorizedIP ;
  cyber:violatesPolicy true ;
  cyber:blocked true .
```

## 16. SAREF-Based Threat Intelligence Integration

### 16.1 Device Vulnerability Tracking

**CVE Mapping to SAREF Devices:**
```turtle
:CVE-2023-12345 a cyber:Vulnerability ;
  cyber:affectsManufacturer "Siemens" ;
  cyber:affectsModel "RDF600" ;
  cyber:affectsFirmwareVersion "3.2.1" ;
  cyber:cvssScore "7.5"^^xsd:float ;
  cyber:exploitAvailable true .

# Query vulnerable devices
SELECT ?device WHERE {
  ?device a s4bldg:Thermostat ;
          saref:hasManufacturer "Siemens" ;
          saref:hasModel "RDF600" ;
          saref:hasFirmwareVersion "3.2.1" .
}
```

### 16.2 Threat Actor TTPs Mapping

**ATT&CK Techniques on SAREF Devices:**
```turtle
:T0836_ModifyParameter a attack:Technique ;
  attack:appliesToDeviceType s4bldg:HVAC ;
  attack:appliesToDeviceType s4inma:Machine ;
  attack:modifiesProperty saref:SetPoint ;
  attack:potentialImpact [
    cyber:PhysicalDamage
    cyber:ProcessDisruption
    cyber:SafetyHazard
  ] .

:AttackScenario1 a cyber:AttackScenario ;
  cyber:usesTool attack:Metasploit ;
  cyber:targetsTechnique :T0836_ModifyParameter ;
  cyber:targetsDevice :HVACController ;
  cyber:impactScore "8.0"^^xsd:float .
```

### 16.3 Sensor Data Integrity Monitoring

**SAREF Measurement Validation:**
```turtle
:DataIntegrityCheck a cyber:IntegrityValidation ;
  cyber:validatesDevice :FlowSensor1 ;
  cyber:validatesProperty s4watr:FlowRate ;
  cyber:checksForAnomaly [
    cyber:OutOfRangeValue
    cyber:ImpossibleRate
    cyber:SensorDrift
    cyber:DataInjection
  ] ;
  cyber:hasBaselineModel :FlowNormalBehavior .

:FlowNormalBehavior a cyber:BehavioralModel ;
  cyber:learnedFromHistorical true ;
  cyber:hasConfidenceInterval "95%"^^xsd:string ;
  cyber:validityPeriod "P30D"^^xsd:duration .
```

## 17. Implementation Recommendations for AEON-DT

### 17.1 Priority SAREF Extensions

**High Priority (Direct OT/ICS Relevance):**
1. **SAREF4BLDG**: Building automation = BMS/BAS cybersecurity
2. **SAREF4INMA**: Manufacturing = ICS/SCADA core domain
3. **SAREF4ENER**: Energy management = critical infrastructure
4. **SAREF4GRID**: Electrical grid = power system security

**Medium Priority (Infrastructure Context):**
5. **SAREF4WATR**: Water systems = critical infrastructure
6. **SAREF4CITY**: Smart city = integrated infrastructure
7. **SAREF Core**: Foundational device/property modeling

**Lower Priority (Specialized Domains):**
8. SAREF4AGRI, SAREF4AUTO, SAREF4ENVI, SAREF4HEALTH, SAREF4LIFT, SAREF4WEAR

### 17.2 Integration Architecture

**Layered Approach:**
```
Layer 1: SAREF Core
  ├── Device, Function, Property, Measurement foundation

Layer 2: Domain Extensions
  ├── SAREF4BLDG (Building automation)
  ├── SAREF4INMA (Manufacturing)
  ├── SAREF4ENER (Energy management)
  └── SAREF4GRID (Electrical grid)

Layer 3: Cybersecurity Extensions (Custom)
  ├── Vulnerability mapping
  ├── Threat intelligence
  ├── Network topology
  ├── Security events
  └── Anomaly detection

Layer 4: Integration with Existing Ontologies
  ├── UCO (forensics)
  ├── MITRE ATT&CK (tactics/techniques)
  ├── STIX (threat intelligence)
  └── ICS-SEC-KG (ICS security)
```

### 17.3 Device Modeling Strategy

**SAREF as Device Registry:**
```turtle
# Use SAREF for comprehensive device inventory
:DeviceInventory a owl:Ontology ;
  imports <https://saref.etsi.org/core/> ;
  imports <https://saref.etsi.org/saref4bldg/> ;
  imports <https://saref.etsi.org/saref4inma/> .

# Each physical device instance
:Device_001 a s4bldg:Thermostat ;
  saref:hasManufacturer "Honeywell" ;
  saref:hasModel "T6 Pro" ;
  saref:hasDeviceID "THM-001" ;
  saref:hasFirmwareVersion "2.1.3" ;
  saref:hasLocation :Room_205 ;
  saref:controlsProperty :RoomTemperature ;
  # Cybersecurity extensions
  cyber:hasIPAddress "192.168.20.15" ;
  cyber:hasNetworkSegment :BMS_VLAN ;
  cyber:lastScanned "2025-10-30T08:00:00Z"^^xsd:dateTime ;
  cyber:vulnerabilityStatus cyber:Patched .
```

### 17.4 Property-Based Monitoring

**Unified Sensor/Actuator Monitoring:**
```turtle
# All measurements follow same pattern
:Measurement_12345 a saref:Measurement ;
  saref:relatesToProperty :RoomTemperature ;
  saref:hasValue "22.3"^^xsd:float ;
  saref:isMeasuredIn :DegreeCelsius ;
  saref:hasTimestamp "2025-10-30T12:34:56Z"^^xsd:dateTime ;
  saref:isMeasuredByDevice :Device_001 ;
  # Anomaly detection
  cyber:withinExpectedRange true ;
  cyber:anomalyScore "0.05"^^xsd:float .
```

### 17.5 Function and Command Security

**Securing Device Functions:**
```turtle
:ThermostatFunction a saref:Function ;
  saref:hasCommand :SetTemperatureCommand ;
  # Security controls
  cyber:requiresAuthentication true ;
  cyber:requiresAuthorization :HVAC_Operator_Role ;
  cyber:loggedAction true ;
  cyber:rateLimit "5/minute"^^xsd:string .

:SetTemperatureCommand a saref:SetCommand ;
  saref:actsUpon :TargetTemperature ;
  saref:hasInput :TemperatureValue ;
  # Command validation
  cyber:validRange "15-30"^^xsd:string ;
  cyber:requiresApproval :Supervisor_Role .
```

## 18. SAREF Gaps and Custom Extensions Needed

### 18.1 Missing Cybersecurity Concepts

**Required Extensions:**
1. **Network Security**: IP addresses, protocols, ports, firewalls
2. **Authentication**: User credentials, access control, authorization
3. **Vulnerabilities**: CVEs, patches, security updates
4. **Incidents**: Security events, alerts, forensics
5. **Threats**: Threat actors, campaigns, TTPs
6. **Risk**: Risk scores, impact assessment, mitigation

### 18.2 Proposed SAREF4SECURITY Extension

**Core Security Classes:**
```turtle
s4sec:SecurityDevice
  rdfs:subClassOf saref:Device
  ├── s4sec:Firewall
  ├── s4sec:IDS
  ├── s4sec:IPS
  ├── s4sec:SIEM
  └── s4sec:SecurityGateway

s4sec:SecurityProperty
  rdfs:subClassOf saref:Property
  ├── s4sec:ThreatLevel
  ├── s4sec:RiskScore
  ├── s4sec:VulnerabilityCount
  └── s4sec:SecurityPosture

s4sec:SecurityEvent
  ├── s4sec:IntrusionAttempt
  ├── s4sec:MalwareDetection
  ├── s4sec:AnomalousBehavior
  ├── s4sec:UnauthorizedAccess
  └── s4sec:DataExfiltration

s4sec:SecurityControl
  ├── s4sec:AccessControl
  ├── s4sec:Encryption
  ├── s4sec:NetworkSegmentation
  ├── s4sec:Monitoring
  └── s4sec:IncidentResponse
```

### 18.3 ICS-Specific Extensions

**SAREF4ICS Proposal:**
```turtle
s4ics:ICSDevice
  rdfs:subClassOf saref:Device
  ├── s4ics:PLC
  ├── s4ics:DCS
  ├── s4ics:RTU
  ├── s4ics:HMI
  ├── s4ics:Historian
  └── s4ics:EngineeringWorkstation

s4ics:IndustrialProtocol
  ├── s4ics:Modbus
  ├── s4ics:OPCUA
  ├── s4ics:DNP3
  ├── s4ics:IEC61850
  ├── s4ics:BACnet
  └── s4ics:PROFINET

s4ics:SafetySystem
  rdfs:subClassOf s4ics:ICSDevice
  ├── s4ics:EmergencyShutdown
  ├── s4ics:SafetyPLC
  ├── s4ics:FireSuppression
  └── s4ics:SafetyInterlock
```

## 19. SPARQL Query Patterns for Cybersecurity

### 19.1 Device Inventory Queries

**Find All Critical Devices:**
```sparql
PREFIX saref: <https://saref.etsi.org/core/>
PREFIX s4bldg: <https://saref.etsi.org/saref4bldg/>
PREFIX s4inma: <https://saref.etsi.org/saref4inma/>
PREFIX cyber: <http://aeon-dt.org/cybersecurity#>

SELECT ?device ?type ?manufacturer ?model ?ipAddress WHERE {
  ?device a ?type ;
          saref:hasManufacturer ?manufacturer ;
          saref:hasModel ?model ;
          cyber:hasIPAddress ?ipAddress .

  FILTER (?type IN (s4bldg:HVAC, s4inma:PLC, s4bldg:AccessController))
}
```

**Find Vulnerable Devices:**
```sparql
PREFIX saref: <https://saref.etsi.org/core/>
PREFIX cyber: <http://aeon-dt.org/cybersecurity#>

SELECT ?device ?vulnerability ?cvssScore WHERE {
  ?device a saref:Device ;
          saref:hasManufacturer ?mfr ;
          saref:hasModel ?model ;
          saref:hasFirmwareVersion ?firmware .

  ?vulnerability a cyber:CVE ;
                 cyber:affectsManufacturer ?mfr ;
                 cyber:affectsModel ?model ;
                 cyber:affectsFirmwareVersion ?firmware ;
                 cyber:cvssScore ?cvssScore .

  FILTER (?cvssScore >= 7.0)
}
ORDER BY DESC(?cvssScore)
```

### 19.2 Anomaly Detection Queries

**Detect Abnormal Measurements:**
```sparql
PREFIX saref: <https://saref.etsi.org/core/>
PREFIX cyber: <http://aeon-dt.org/cybersecurity#>

SELECT ?measurement ?device ?property ?value ?anomalyScore WHERE {
  ?measurement a saref:Measurement ;
               saref:relatesToProperty ?property ;
               saref:hasValue ?value ;
               saref:hasTimestamp ?time ;
               saref:isMeasuredByDevice ?device ;
               cyber:anomalyScore ?anomalyScore .

  FILTER (?anomalyScore > 0.8)
  FILTER (?time > "2025-10-30T00:00:00Z"^^xsd:dateTime)
}
ORDER BY DESC(?anomalyScore)
```

### 19.3 Network Topology Queries

**Find Device Communication Paths:**
```sparql
PREFIX saref: <https://saref.etsi.org/core/>
PREFIX cyber: <http://aeon-dt.org/cybersecurity#>

SELECT ?sourceDevice ?targetDevice ?protocol WHERE {
  ?sourceDevice a saref:Device ;
                cyber:communicatesWith ?targetDevice ;
                cyber:usesProtocol ?protocol .

  ?targetDevice a saref:Device .
}
```

### 19.4 Command Authorization Queries

**Find Unauthorized Commands:**
```sparql
PREFIX saref: <https://saref.etsi.org/core/>
PREFIX cyber: <http://aeon-dt.org/cybersecurity#>

SELECT ?command ?device ?user ?timestamp WHERE {
  ?command a saref:Command ;
           cyber:executedOn ?device ;
           cyber:executedBy ?user ;
           cyber:timestamp ?timestamp ;
           cyber:authorized false .
}
ORDER BY DESC(?timestamp)
```

## 20. Summary and Key Takeaways

### 20.1 SAREF Strengths for AEON-DT

**Excellent Foundation:**
1. **Standardized Vocabulary**: ETSI-maintained, widely adopted
2. **Device-Centric**: Perfect for OT/ICS device modeling
3. **Extensible**: Clear extension mechanism for custom domains
4. **Multi-Domain**: Covers building, manufacturing, energy, water, city infrastructure
5. **Property Framework**: Unified measurement and sensing approach
6. **Function Abstraction**: Separates capabilities from implementation

### 20.2 Direct Applications

**High-Value Use Cases:**
1. **Device Inventory**: Comprehensive OT/ICS asset management
2. **Network Mapping**: Physical device network topology
3. **Anomaly Detection**: Property measurement baselines
4. **Vulnerability Management**: Device-CVE mapping
5. **Access Control**: Function-based authorization
6. **Incident Investigation**: Device state forensics

### 20.3 Integration Requirements

**Must Integrate With:**
1. **UCO**: Forensic investigation of device incidents
2. **MITRE ATT&CK**: Threat techniques on devices
3. **STIX**: Threat intelligence about device vulnerabilities
4. **ICS-SEC-KG**: ICS-specific security knowledge
5. **Schema.org**: IT infrastructure context

### 20.4 Custom Extensions Needed

**Priority Gaps:**
1. **SAREF4SECURITY**: Security device and property classes
2. **SAREF4ICS**: Industrial control system specifics
3. **Network Integration**: IP, protocols, communication patterns
4. **Security Events**: Incidents, alerts, forensics
5. **Threat Intelligence**: Vulnerabilities, exploits, TTPs

### 20.5 Implementation Strategy

**Phased Approach:**

**Phase 1: Core Integration**
- Import SAREF Core, SAREF4BLDG, SAREF4INMA
- Create device inventory
- Model basic properties and measurements

**Phase 2: Cybersecurity Extensions**
- Define SAREF4SECURITY concepts
- Map vulnerabilities to devices
- Implement anomaly detection

**Phase 3: Threat Intelligence**
- Integrate with MITRE ATT&CK
- Map CVEs to device models
- Create attack scenario models

**Phase 4: Operational Integration**
- Connect to live SIEM/IDS systems
- Implement real-time monitoring
- Deploy forensic investigation tools

### 20.6 Technical Debt Considerations

**Challenges:**
1. **Complexity**: 13 extensions = large vocabulary
2. **Overlap**: Some concepts duplicated across extensions
3. **Gaps**: Missing cybersecurity primitives
4. **Maintenance**: ETSI update cycle coordination
5. **Tool Support**: Limited reasoner performance with full stack

**Mitigation:**
- Use only relevant extensions (BLDG, INMA, ENER, GRID)
- Create custom SAREF4SECURITY extension
- Document mappings clearly
- Implement modular import structure

## Version History

- v1.0.0 (2025-10-30): Initial comprehensive research findings

## References

1. ETSI TS 103 264 - SAREF Core Specification
2. SAREF Portal: https://saref.etsi.org/
3. SAREF4BLDG Specification v1.1.2
4. SAREF4INMA Specification v1.2.0
5. SAREF4ENER Specification v1.1.2
6. SAREF4GRID Specification v1.0.0
7. Individual SAREF extension specifications (all versions as noted)

---

*Document Complete - 13 SAREF Extensions Analyzed*
