# AEON Entity Catalog - Complete 631 Labels
**File:** ENTITY_CATALOG_COMPLETE.md
**Created:** 2025-12-12
**Database:** OpenSPG Neo4j
**Total Labels:** 631
**Total Nodes:** 2,847,915

## Executive Summary

This catalog documents all 631 entity labels currently in the AEON knowledge graph, representing a comprehensive ontology covering:

- **Threat Intelligence** (CVEs, Vulnerabilities, Malware, Threat Actors, Attack Patterns)
- **Infrastructure & Equipment** (ICS/SCADA, Critical Infrastructure, IoT Devices)
- **Software Components** (SBOM, Dependencies, Licenses, Build Artifacts)
- **Measurements & Telemetry** (297,858 measurement nodes across all sectors)
- **Organizational & Compliance** (Organizations, Standards, Regulations)
- **Specialized Domains** (Agriculture, Healthcare, Energy, Defense, Finance)

---

## Part 1: Top 100 Labels by Node Count

### TIER 1: Massive Scale (100,000+ nodes)

#### 1. CVE (316,552 nodes)
**Category:** Vulnerability / Threat Intelligence
**Super Label:** Vulnerability
**Description:** Common Vulnerabilities and Exposures - standardized identifiers for known security vulnerabilities

**Sample Node Properties:**
```json
{
  "id": "CVE-1999-0095",
  "description": "The debug command in Sendmail is enabled, allowing attackers to execute commands as root.",
  "cvssV2BaseScore": 10.0,
  "cvssV31BaseSeverity": "HIGH",
  "epss_score": 0.0838,
  "epss_percentile": 0.91934,
  "published_date": "1988-10-01T04:00Z",
  "modified_date": "2025-04-03T01:03:51.193Z",
  "cpe_products": ["Sendmail"],
  "cpe_vendors": ["Eric Allman"],
  "priority_tier": "NEVER",
  "hierarchy_path": "TECHNICAL/Vulnerability/Unknown"
}
```

**Common Relationships:**
- `HAS_WEAKNESS` → CWE (Common Weakness Enumeration)
- `AFFECTS` → Software_Component, Equipment, Asset
- `EXPLOITED_BY` → ThreatActor, Malware, AttackPattern
- `MITIGATED_BY` → Mitigation, CourseOfAction
- `REFERENCED_IN` → Intelligence_Analysis, Indicator

**Usage Context:** Primary vulnerability tracking for risk assessment, patch prioritization, EPSS scoring, KEV identification

---

#### 2. Vulnerability (314,538 nodes)
**Category:** Threat Intelligence / Security
**Super Label:** Vulnerability
**Description:** Parent class for all vulnerability types including CVE, CWE, CAPEC, and custom vulnerabilities

**Sample Node Properties (CWE):**
```json
{
  "id": "CWE-694",
  "name": "Use of Multiple Resources with Duplicate Identifier",
  "description": "The product uses multiple resources that can have the same identifier...",
  "abstraction": "Base",
  "status": "Incomplete",
  "taxonomy": "CWE",
  "version": "v4.18",
  "hierarchy_path": "TECHNICAL/Vulnerability/Use of Multiple Resources with Duplicate Identifier"
}
```

**Common Relationships:**
- `CHILD_OF` → CWE_Category (hierarchy)
- `RELATED_TO` → Other CWE weaknesses
- `CAN_LEAD_TO` → CVE (concrete vulnerabilities)
- `ADDRESSED_BY` → Mitigation, Standard, Compliance

**Usage Context:** Weakness classification, root cause analysis, security architecture review, compliance mapping

---

#### 3. Measurement (297,858 nodes)
**Category:** Telemetry / Monitoring
**Super Label:** Measurement
**Description:** Generic measurement class for telemetry, metrics, and monitoring data across all infrastructure sectors

**Specialized Subtypes:**
- **ManufacturingMeasurement** (72,800) - Production metrics, quality control
- **NetworkMeasurement** (27,458) - Bandwidth, latency, packet loss
- **DefenseMeasurement** (25,200) - Military equipment telemetry
- **HealthcareMeasurement** (18,200) - Patient vitals, equipment status
- **RadiationMeasurement** (18,000) - Nuclear facility monitoring
- **ITMeasurement** (18,000) - Server performance, application metrics
- **ChemicalMeasurement** (4,200) - Process variables, safety metrics
- **GovernmentMeasurement** (5,600) - Facility monitoring

**Sample Properties:**
```json
{
  "measurement_type": "temperature",
  "value": 72.5,
  "unit": "fahrenheit",
  "timestamp": "2025-12-12T10:30:00Z",
  "sensor_id": "TEMP_SENSOR_001",
  "location": "Building A, Room 101",
  "status": "normal",
  "alarm_threshold": 85.0
}
```

**Common Relationships:**
- `MEASURED_BY` → Device, Sensor, Equipment
- `PART_OF` → TimeSeries, HistoricalPattern
- `TRIGGERS` → Alert, Notification, Event
- `MONITORED_IN` → Zone, Location, Facility

**Usage Context:** Real-time monitoring, anomaly detection, predictive maintenance, compliance reporting

---

#### 4. Asset (206,075 nodes)
**Category:** Infrastructure / Inventory
**Super Label:** Asset
**Description:** Physical and digital assets including equipment, software, devices, and infrastructure components

**Specialized Subtypes:**
- **CommercialAsset** (8,400) - Commercial facilities and equipment
- **MajorAsset** (449) - Critical infrastructure assets
- **MajorFacility** (150) - Large-scale facilities
- **MajorManufacturingAsset** (100) - Key manufacturing equipment
- **MajorHealthcareAsset** (20) - Critical healthcare facilities

**Common Relationships:**
- `HAS_VULNERABILITY` → CVE, Vulnerability
- `RUNS` → Software, Application, Firmware
- `LOCATED_IN` → Zone, Location, Facility
- `MONITORED_BY` → Measurement, Sensor, SAREF_Device
- `DEPENDS_ON` → Other Asset, Dependency

**Usage Context:** Asset management, vulnerability tracking, dependency mapping, risk assessment, compliance

---

#### 5. Monitoring (181,704 nodes)
**Category:** Operations / Surveillance
**Super Label:** Monitoring
**Description:** Monitoring systems, processes, and activities across infrastructure sectors

**Common Relationships:**
- `MONITORS` → Asset, Equipment, Process
- `GENERATES` → Measurement, Alert, Event
- `PART_OF` → System, Infrastructure
- `CONFIGURED_BY` → Configuration, Standard

**Usage Context:** Operational oversight, anomaly detection, compliance verification, incident response

---

#### 6. SBOM (140,000 nodes)
**Category:** Software / Supply Chain
**Super Label:** Asset
**Description:** Software Bill of Materials - detailed inventory of software components, dependencies, licenses

**Sample Node Properties:**
```json
{
  "componentID": "LIBRARY-COMP-63027",
  "name": "Library Component 6327",
  "version": "8.7.27",
  "componentType": "library",
  "purl": "pkg:library/library-6327@8.0.0",
  "license": "BSD-3-Clause",
  "supplier_name": "GitHub Inc",
  "hash_algorithm": "sha256",
  "hash_value": "abc630027def1234567890",
  "trustScore": 97.0,
  "verificationStatus": "verified",
  "endOfSupportDate": "2027-10-04T17:18:35.465Z",
  "tags": ["stable", "verified", "sbom"]
}
```

**Common Relationships:**
- `DEPENDS_ON` → Other Software_Component, Dependency
- `HAS_LICENSE` → License, LicenseCompliance
- `HAS_VULNERABILITY` → CVE, Vulnerability
- `BUILT_BY` → Build_Info, BuildSystem
- `ATTESTED_BY` → Attestation, VulnerabilityAttestation

**Usage Context:** Supply chain security, license compliance, vulnerability management, build verification

---

#### 7. ManufacturingMeasurement (72,800 nodes)
**Category:** Manufacturing / Telemetry
**Super Label:** Measurement
**Description:** Manufacturing process measurements including production rates, quality metrics, equipment performance

**Common Relationships:**
- `MEASURED_BY` → ManufacturingEquipment, ProcessControlSystems
- `PART_OF` → Process, ManufacturingProcess
- `TRIGGERS` → ManufacturingAlert, QualityControl
- `ANALYZED_BY` → QualityMetric, PerformanceMetric

**Usage Context:** Production optimization, quality assurance, equipment health monitoring, OEE calculation

---

#### 8. Control (66,391 nodes)
**Category:** Automation / ICS
**Super Label:** Control
**Description:** Control systems and control logic across industrial and building automation

**Specialized Subtypes:**
- **CommercialControl** (4,200) - Building automation
- **ManufacturingControl** (1,400) - Production control
- **ITControl** (700) - IT system controls
- **FinancialControl** (600) - Transaction controls
- **GovernmentControl** (500) - Government facility controls
- **DefenseControl** (500) - Military system controls
- **HealthcareControl** (500) - Medical equipment controls

**Common Relationships:**
- `CONTROLS` → Equipment, Process, Device
- `RECEIVES` → Measurement, Sensor data
- `EXECUTES` → Command, Function
- `CONFIGURED_BY` → Configuration, Standard

**Usage Context:** Process automation, safety systems, building management, access control

---

#### 9. Property (61,700 nodes)
**Category:** Metadata / Attributes
**Super Label:** Property
**Description:** Properties and attributes of entities across all domains

**Specialized Subtypes:**
- **DefenseProperty** (7,000)
- **EnergyProperty** (6,000)
- **CommunicationsProperty** (5,000)
- **EmergencyServicesProperty** (5,000)
- **FoodAgricultureProperty** (5,000)
- **FinancialServicesProperty** (5,000)
- **GovernmentProperty** (5,000)
- **NuclearProperty** (5,000)
- **HealthcareProperty** (5,000)
- **ManufacturingProperty** (5,000)
- **ITProperty** (4,500)
- **WaterProperty** (3,000)

**Usage Context:** Entity metadata, configuration management, compliance tracking, data governance

---

#### 10. Organization (56,144 nodes)
**Category:** Organizational / Business
**Super Label:** Organization
**Description:** Organizations including government agencies, vendors, security authorities, enterprises

**Sample Node Properties:**
```json
{
  "id": "cisa",
  "name": "Cybersecurity and Infrastructure Security Agency",
  "type": "GOVERNMENT",
  "role": "SECURITY_AUTHORITY",
  "country": "USA",
  "sbom_guidance_releases": 3,
  "hierarchy_path": "ORGANIZATIONAL/Organization/CISA"
}
```

**Common Relationships:**
- `PRODUCES` → Standard, Guidance, Intelligence_Analysis
- `OPERATES` → Asset, Infrastructure, Facility
- `MEMBER_OF` → Sector, Industry
- `COLLABORATES_WITH` → Other Organization
- `ISSUES` → Alert, Advisory, Mitigation

**Usage Context:** Organizational mapping, supply chain analysis, threat attribution, compliance management

---

### TIER 2: Large Scale (20,000-100,000 nodes)

#### 11. Entity (55,569 nodes)
**Category:** Generic / Base Class
**Description:** Generic entity class for uncategorized or multi-purpose nodes

---

#### 12. Software_Component (55,000 nodes)
**Category:** Software / SBOM
**Super Label:** Asset
**Description:** Individual software components, libraries, and modules

**Common Relationships:**
- `PART_OF` → SBOM, Application, System
- `DEPENDS_ON` → Other Software_Component, Library
- `HAS_VULNERABILITY` → CVE, Vulnerability
- `LICENSED_UNDER` → License, LicensePolicy

---

#### 13. TimeSeries (51,000 nodes)
**Category:** Analytics / Temporal
**Description:** Time-series data collections for trend analysis and forecasting

**Common Relationships:**
- `CONTAINS` → Measurement, Metric
- `ANALYZED_BY` → TimeSeriesAnalysis, MLModel
- `PART_OF` → HistoricalPattern, TemporalEvent

---

#### 14. SoftwareComponent (50,000 nodes)
**Category:** Software / Development
**Description:** Software component variant with development lifecycle tracking

---

#### 15. Device (48,400 nodes)
**Category:** Hardware / IoT
**Super Label:** Device
**Description:** Physical devices including IoT, sensors, controllers, and endpoints

**Specialized Subtypes:**
- **EnergyDevice** (10,000) - Smart meters, DER devices
- **GovernmentDevice** (8,400) - Government facility equipment
- **DefenseDevice** (4,600) - Military equipment
- **EmergencyServicesDevice** (3,500) - First responder equipment
- **FoodAgricultureDevice** (3,500) - Agricultural sensors and controllers
- **FinancialServicesDevice** (3,500) - Banking equipment
- **NuclearDevice** (3,000) - Nuclear facility instrumentation
- **ITDevice** (2,800) - IT infrastructure devices
- **HealthcareDevice** (2,800) - Medical devices
- **CommunicationsDevice** (2,300) - Communication equipment
- **WaterDevice** (1,500) - Water treatment devices

**Common Relationships:**
- `GENERATES` → Measurement, Telemetry
- `CONTROLLED_BY` → Control, SCADA
- `CONNECTS_TO` → Network, NetworkSegment
- `LOCATED_IN` → Zone, Facility, Location

**Usage Context:** Device inventory, IoT management, telemetry collection, anomaly detection

---

#### 16. Equipment (48,288 nodes)
**Category:** Infrastructure / Industrial
**Super Label:** Equipment
**Description:** Industrial and commercial equipment

**Sample Node Properties:**
```json
{
  "equipmentId": "EQ_TRANS_001",
  "name": "Transformer A1",
  "equipmentType": "Transformer",
  "location": "Substation Alpha Bay 6 Panel 4",
  "status": "active",
  "latitude": 41.82308908082225,
  "longitude": -71.41049595378189,
  "elevation_meters": 11.829932,
  "customer_namespace": "northeast-power",
  "inherited_tags": [
    "OPS_substation",
    "OPS_high_voltage",
    "REG_NERC_CIP",
    "TECH_scada_rtu",
    "TECH_iec61850"
  ]
}
```

**Specialized Subtypes:**
- **ChemicalEquipment** (28,000) - Process equipment
- **DamsEquipment** (14,074) - Dam infrastructure
- **ManufacturingEquipment** (11,200) - Production equipment
- **SeparationEquipment** (4,480) - Chemical separation
- **HeatExchangeEquipment** (3,920) - Thermal systems
- **PipingAndValves** (3,920) - Fluid systems
- **PumpsAndCompressors** (3,360) - Mechanical equipment
- **EmergencyEquipment** (1,449) - Emergency response gear
- **SafetyAndMonitoringSystems** (840) - Safety equipment

**Common Relationships:**
- `HAS_MEASUREMENT` → Measurement, Telemetry
- `PART_OF` → Facility, Process, System
- `MAINTAINED_BY` → MaintenanceSchedule, Organization
- `HAS_VULNERABILITY` → CVE, Vulnerability
- `CONTROLLED_BY` → SCADA, Control

**Usage Context:** Asset management, predictive maintenance, operational monitoring, safety compliance

---

#### 17-40. Critical Infrastructure Sectors (40,759 - 27,000 nodes)

**COMMUNICATIONS** (40,759)
- Telecommunications infrastructure
- Network equipment and protocols

**SECTOR_DEFENSE_INDUSTRIAL_BASE** (38,800)
- Military and defense systems
- Defense manufacturing

**ENERGY** (35,475)
- Power generation and distribution
- Energy transmission systems

**CHEMICAL** (32,200)
- Chemical processing facilities
- Process control systems

**Compliance** (30,400)
- Regulatory compliance tracking
- Standards adherence

**CriticalInfrastructure** (28,100)
- Cross-sector critical systems

**EMERGENCY_SERVICES** (28,000)
- First responder systems
- Emergency communications

**FOOD_AGRICULTURE** (28,000)
- Agricultural systems
- Food processing

**INFORMATION_TECHNOLOGY** (28,000)
- IT infrastructure
- Data centers

**FINANCIAL_SERVICES** (28,000)
- Banking systems
- Payment processing

**COMMERCIAL_FACILITIES** (28,000)
- Commercial buildings
- Shopping centers

**Healthcare** (28,000)
- Medical facilities
- Healthcare systems

**Transportation** (28,000)
- Transportation networks
- Logistics systems

**WATER** (27,200)
- Water treatment
- Distribution systems

**GOVERNMENT_FACILITIES** (27,000)
- Government buildings
- Public facilities

---

### TIER 3: Medium Scale (10,000-20,000 nodes)

#### 41-60. Specialized Infrastructure (27,458 - 10,000 nodes)

**NetworkMeasurement** (27,458)
- Network performance metrics
- Bandwidth and latency data

**Water_Treatment** (25,199)
- Treatment process monitoring
- Water quality metrics

**Energy_Transmission** (24,400)
- Power transmission lines
- Grid monitoring

**Telecom_Infrastructure** (19,851)
- Cellular networks
- Communication towers

**DefenseMeasurement** (25,200)
**SAREF_Measurement** (25,200)
**HealthcareMeasurement** (18,200)
**ITMeasurement** (18,000)
**RadiationMeasurement** (18,000)
**Energy** (17,475)
**ResponseMetric** (17,000)
**AgricultureMetric** (17,000)
**TransactionMetric** (17,000)
**Provenance** (15,000)
**Build_Info** (15,000)
**License** (15,000)
**HistoricalPattern** (14,985)
**Protocol** (13,336)
**Communications** (13,210)
**Indicator** (11,601)
**Data_Centers** (11,258)
**ThreatActor** (10,599)
**Energy_Distribution** (10,325)
**Package** (10,017)
**EnergyDevice** (10,000)
**Library** (10,000)

---

### TIER 4: Notable Scale (5,000-10,000 nodes)

#### 61-100. Diverse Categories (9,875 - 5,000 nodes)

**Threat Intelligence:**
- Threat (9,875)
- FutureThreat (8,900)
- ICS_THREAT_INTEL (9,404)
- Mitigation (5,224)
- Detection (5,000)

**Finance & Banking:**
- Banking (9,630)
- CapitalMarkets (9,329)
- PaymentSystems (9,041)

**Energy & Nuclear:**
- Nuclear (9,549)
- Reactors (5,600)

**Government & Defense:**
- GovernmentDevice (8,400)
- GovernmentProcess (7,000)
- DefenseProperty (7,000)

**Commercial:**
- CommercialAsset (8,400)
- CommercialProcess (5,600)

**Software & Build:**
- SoftwareLicense (8,300)
- DependencyTree (8,000)
- Build (8,000)
- Artifact (5,000)
- ContainerImage (5,000)
- Firmware (5,000)
- BuildSystem (5,000)
- LicenseCompliance (5,000)
- Attestation (5,000)

**ICS/SCADA:**
- ICS (7,264)
- IT_INFRASTRUCTURE (5,000)

**SAREF (Smart Appliances):**
- SAREF (5,000)
- SAREF_Core (5,000)
- SAREF_Device (4,600)

**Dams:**
- DamsProcess (5,630)

**Level 5** (5,543) - Highest automation level

**Information:**
- InformationEvent (5,001)
- InformationStream (600)

---

## Part 2: Remaining 531 Labels (Alphabetical)

### A

**Access_Control** (3,388) - Physical and logical access control systems
**ActivityTracking** (167) - User and entity activity monitoring
**Adversary** (343) - Threat actor entities
**Aerospace_Defense** (3,520) - Aerospace and defense systems
**AgricultureProcess** (1,200) - Agricultural processes
**Agriculture** (1,500) - Agricultural systems
**AirQualityStation** (100) - Air quality monitoring
**Alert** (4,100) - Security and operational alerts
**AlertSystem** (200) - Alert generation systems
**Ambulance** (201) - Emergency medical vehicles
**AnalystDiscourse** (1) - Psychoanalytic framework
**AnalyticsApp** (300) - Analytics applications
**AnalyticsStream** (80) - Analytics data streams
**Animal** (200) - Livestock tracking
**AnimalHealth** (1,263) - Animal health monitoring
**AnimalMonitor** (126) - Animal monitoring devices
**APISource** (300) - API data sources
**Application** (819) - Software applications
**APT_GROUP** (3) - Advanced Persistent Threat groups
**ArchiveSystem** (200) - Data archiving systems
**Assessment** (1) - Security assessments
**Attestation** (5,000) - Software attestations
**Attack** (0) - Attack instances
**AttackPattern** (2,070) - Attack methodologies
**AttackTactic** (28) - High-level attack strategies
**AttackTechnique** (1,657) - Specific attack techniques
**AttackTimeline** (0) - Attack sequence tracking
**AttackVector** (3) - Attack entry points
**ATT_CK_Tactic** (14) - MITRE ATT&CK tactics
**ATT_CK_Technique** (691) - MITRE ATT&CK techniques
**ATTACK_Group** (187) - MITRE attack groups
**ATTACK_Software** (0) - Attack software
**ATTACK_Tactic** (14) - Attack tactical framework
**ATTACK_Technique** (691) - Attack technique catalog

### B

**Banking** (9,630) - Banking infrastructure
**Barn** (20) - Agricultural buildings
**BAS** (1,540) - Building Automation Systems
**BatchStream** (100) - Batch data processing
**BEHAVIORAL** (57) - Behavioral patterns
**Behavioral_Pattern** (20) - Behavioral analysis
**BotNetwork** (300) - Botnet infrastructure
**Build** (8,000) - Software builds
**Build_Info** (15,000) - Build metadata
**BuildSystem** (5,000) - Build infrastructure
**BuildTool** (2,000) - Build automation tools

### C

**CAD** (96) - Computer-Aided Design systems
**CADWorkstation** (267) - CAD workstations
**CAMPAIGN** (3) - Threat campaigns
**Campaign** (163) - Attack campaigns
**CAPEC** (615) - Common Attack Pattern Enumeration
**CAPECCategory** (78) - CAPEC classifications
**CAPEC_Category** (78) - CAPEC taxonomy
**CapitalMarkets** (9,329) - Financial markets
**CascadeEvent** (12) - Cascading failures
**CCTV** (1,680) - Video surveillance
**CertificationExpiration** (592) - Certification tracking
**ChemicalAlert** (0) - Chemical hazard alerts
**ChemicalControl** (0) - Chemical process controls
**ChemicalEquipment** (28,000) - Chemical processing equipment
**ChemicalMeasurement** (4,200) - Chemical process metrics
**ChemicalProcess** (0) - Chemical processes
**ChemicalProperty** (0) - Chemical properties
**ChemicalZone** (0) - Chemical facility zones
**Classified** (4,800) - Classified information
**Cloud_Infrastructure** (800) - Cloud systems
**CloudAccount** (100) - Cloud service accounts
**CloudStorageAccount** (200) - Cloud storage
**CognitiveBias** (32) - Cognitive bias patterns
**Cognitive_Bias** (7) - Bias analysis
**ColdChain** (127) - Cold chain logistics
**ColdChainBreak** (46) - Cold chain failures
**ColdChainTemp** (1,232) - Temperature monitoring
**ColdStorage** (132) - Cold storage facilities
**ColdStorageCenter** (5) - Cold storage buildings
**ColdStorageControl** (81) - Cold storage automation
**Combine** (171) - Harvesting equipment
**Command** (2,400) - System commands
**CommercialAsset** (8,400) - Commercial assets
**CommercialControl** (4,200) - Commercial controls
**CommercialLocation** (3,360) - Commercial sites
**CommercialMitigation** (1,120) - Commercial risk mitigation
**CommercialProcess** (5,600) - Commercial processes
**CommercialStandard** (560) - Commercial standards
**CommercialThreat** (2,800) - Commercial threats
**CommercialVulnerability** (1,960) - Commercial vulnerabilities
**CommunicationLatency** (2,132) - Communication delays
**CommunicationsAlert** (900) - Communication alerts
**CommunicationsDevice** (2,300) - Communication devices
**CommunicationsProperty** (5,000) - Communication properties
**CommunicationsZone** (450) - Communication zones
**ComplianceCertification** (830) - Compliance certificates
**Component** (115) - System components
**Configuration** (5,000) - System configurations
**ConfidenceScore** (4,000) - Confidence metrics
**ContainerImage** (5,000) - Container images
**ContainerInstance** (50) - Running containers
**ConveyorSystem** (81) - Material handling
**CourseOfAction** (276) - Response actions
**Critical** (50) - Critical classification
**Critical_Infrastructure_Sector** (16) - CI sectors
**CriticalInfrastructure** (28,100) - Critical systems
**Crop** (300) - Agricultural crops
**CropField** (38) - Agricultural fields
**CropProduction** (1,750) - Crop management
**CropYield** (1,181) - Harvest metrics
**CrossInfrastructureDependency** (0) - Infrastructure dependencies
**Customer** (10) - Customer entities
**CWE** (1,006) - Common Weakness Enumeration
**CWECategory** (410) - CWE classifications
**CWE_Category** (410) - CWE taxonomy
**Cybersecurity_Attack** (1) - Attack instances
**CybersecurityKB_AttackTactic** (14) - KB attack tactics
**CybersecurityKB_AttackTechnique** (823) - KB attack techniques
**CybersecurityKB_Campaign** (47) - KB campaigns
**CybersecurityKB_CourseOfAction** (268) - KB responses
**CybersecurityKB_Malware** (667) - KB malware
**CybersecurityKB_ThreatActor** (181) - KB threat actors
**CybersecurityKB_Tool** (91) - KB tools

### D

**DairyFacility** (7) - Dairy operations
**DamsEquipment** (14,074) - Dam infrastructure
**DamsIncident** (2,111) - Dam incidents
**DamsMitigation** (3,518) - Dam risk mitigation
**DamsProcess** (5,630) - Dam operations
**DamsStandard** (1,407) - Dam regulations
**DamsThreat** (4,222) - Dam threats
**DamsVulnerability** (4,222) - Dam vulnerabilities
**Dashboard** (300) - Monitoring dashboards
**Data_Centers** (11,258) - Data center facilities
**Database** (200) - Database systems
**DatabaseSource** (200) - Database sources
**DataCenterFacility** (10) - DC buildings
**DataConsumer** (1,200) - Data consumers
**DataFlow** (0) - Data flow tracking
**DataProcessor** (1,500) - Data processing
**Datastore** (200) - Data storage
**DataSource** (1,205) - Data sources
**DefenseAlert** (300) - Defense alerts
**DefenseControl** (500) - Defense controls
**DefenseDevice** (4,600) - Defense equipment
**DefenseMeasurement** (25,200) - Defense metrics
**DefenseProcess** (1,000) - Defense processes
**DefenseProperty** (7,000) - Defense properties
**DefenseZone** (150) - Defense zones
**DependencyLink** (10) - Dependency connections
**DependencyPath** (2,000) - Dependency chains
**DependencyTree** (8,000) - Dependency graphs
**Dependency** (40,000) - Software dependencies
**DeploymentRegistry** (1) - Deployment tracking
**DeploymentZone** (639) - Deployment zones
**Detection** (5,000) - Threat detection
**DetectionSignature** (1,000) - Detection rules
**DigitalTwinState** (10) - Digital twin status
**DiscoursePosition** (4) - Discourse analysis
**DisruptionEvent** (10) - Service disruptions
**Dispatch** (117) - Emergency dispatch
**DispatchCenter** (5) - Dispatch facilities
**DispatchZone** (46) - Dispatch coverage
**DistributedEnergyResource** (750) - DER systems
**Document** (118) - Documentation

### E

**EconomicMetric** (39) - Economic indicators
**EmailAddress** (0) - Email identifiers
**EMB3D** (81) - Embedded device framework
**EMB3DMitigation** (89) - Embedded mitigations
**EMB3DProperty** (118) - Embedded properties
**EMB3DThreat** (81) - Embedded threats
**EMB3D_Mitigation** (89) - Embedded defenses
**EMB3D_Property** (118) - Embedded attributes
**EMB3D_Threat** (81) - Embedded vulnerabilities
**EmergencyAlert** (400) - Emergency notifications
**EmergencyEquipment** (1,449) - Emergency gear
**EmergencyResponse** (1,200) - Emergency operations
**EmergencyServicesDevice** (3,500) - EMS equipment
**EmergencyServicesProperty** (5,000) - EMS properties
**Emergency_Systems** (1,260) - Emergency infrastructure
**EMS** (1,225) - Emergency Medical Services
**EMSDistrict** (42) - EMS coverage areas
**EMSStation** (8) - EMS facilities
**Enclosure** (100) - Physical enclosures
**Energy_Distribution** (10,325) - Power distribution
**Energy_Generation** (750) - Power generation
**Energy_Transmission** (24,400) - Power transmission
**EnergyDevice** (10,000) - Energy equipment
**EnergyManagementSystem** (25) - Energy management
**EnergyProperty** (6,000) - Energy properties
**Enricher** (200) - Data enrichment
**Entity** (55,569) - Generic entities
**EnvironmentalControl** (198) - Environmental systems
**EOC** (115) - Emergency Operations Center
**EquipmentFailure** (98) - Equipment failures
**EquipmentModel** (0) - Equipment models
**EquipmentPerformance** (1,246) - Equipment metrics
**EquipmentReadiness** (2,097) - Equipment status
**EquipmentSpec** (872) - Equipment specifications
**EquipmentStatus** (617) - Equipment state
**EquipmentYard** (33) - Equipment storage
**Event** (2,291) - System events
**EventCorrelation** (0) - Event correlation
**EventProcessor** (11) - Event processing
**EventStore** (11) - Event storage
**EventStream** (80) - Event streaming
**Evidence** (600) - Digital evidence
**Exploit** (0) - Exploit code

### F

**FacilityCapacity** (650) - Facility capacity
**FacilityCertification** (868) - Facility certificates
**Facility** (279) - Physical facilities
**Farm** (200) - Agricultural operations
**FarmHeadquarters** (9) - Farm management
**FarmManagementSystem** (600) - Farm software
**FarmZone** (250) - Farm zones
**FeedDelivery** (125) - Feed distribution
**FeedIntake** (1,232) - Animal feeding
**FeedMixer** (138) - Feed preparation
**Field** (400) - Agricultural fields
**FieldCharacteristics** (828) - Field properties
**FinancialAlert** (400) - Financial alerts
**FinancialControl** (600) - Financial controls
**FinancialProcess** (1,200) - Financial processes
**FinancialServicesDevice** (3,500) - Financial equipment
**FinancialServicesProperty** (5,000) - Financial properties
**FinancialZone** (250) - Financial zones
**Fire_Safety** (1,680) - Fire protection
**FireApparatus** (466) - Fire vehicles
**FireContainment** (2,060) - Fire suppression
**FireDistrict** (52) - Fire coverage
**FireServices** (1,400) - Fire departments
**FireStation** (12) - Fire facilities
**FireSuppression** (110) - Fire suppression
**Firmware** (5,000) - Firmware images
**FirstResponse** (113) - First responder operations
**FMIS** (71) - Farm Management Information Systems
**FoodAgricultureAlert** (400) - Agriculture alerts
**FoodAgricultureDevice** (3,500) - Agriculture equipment
**FoodAgricultureProperty** (5,000) - Agriculture properties
**FoodProcessing** (830) - Food processing
**FoodProduct** (50) - Food products
**FoodSafety** (1,220) - Food safety
**FoodSafetyHazard** (50) - Food hazards
**FoodSafetyMonitor** (77) - Food monitoring
**FoodSafetyViolation** (42) - Food violations
**Function** (1,300) - System functions
**FutureThreat** (8,900) - Predicted threats

### G

**Geography** (250) - Geographic entities
**GeopoliticalEvent** (501) - Geopolitical events
**Governance** (600) - Governance frameworks
**GovernmentAlert** (300) - Government alerts
**GovernmentControl** (500) - Government controls
**GovernmentDevice** (8,400) - Government equipment
**GovernmentMeasurement** (5,600) - Government metrics
**GovernmentProcess** (7,000) - Government processes
**GovernmentProperty** (5,000) - Government properties
**GovernmentZone** (150) - Government zones
**GrainBin** (197) - Grain storage
**GrainBinHazard** (48) - Grain hazards
**GrainBinMonitor** (77) - Grain monitoring
**GrainDryer** (177) - Grain drying
**GrainElevator** (5) - Grain facilities
**GrainStorage** (24) - Grain storage
**GreenhouseComplex** (7) - Greenhouse facilities
**Ground_Systems** (1,740) - Ground control

### H

**Harvesting** (123) - Crop harvesting
**Hash** (0) - Hash values
**HazmatAlert** (46) - Hazmat alerts
**HazmatResponse** (106) - Hazmat operations
**HealthcareAlert** (200) - Healthcare alerts
**HealthcareControl** (500) - Healthcare controls
**HealthcareDevice** (2,800) - Medical devices
**HealthcareMeasurement** (18,200) - Healthcare metrics
**HealthcareProcess** (1,200) - Healthcare processes
**HealthcareProperty** (5,000) - Healthcare properties
**HealthcareZone** (80) - Healthcare zones
**HealthMetric** (500) - Health metrics
**HealthMonitor** (132) - Health monitoring
**Health_Monitor** (1,500) - Health systems
**HeatExchangeEquipment** (3,920) - Heat exchangers
**HerdComposition** (769) - Livestock herds
**HistoricalPattern** (14,985) - Historical analysis
**HistoricalSnapshot** (10) - Historical states
**HMISession** (0) - HMI interactions
**HospitalDiversion** (58) - Hospital capacity
**Human** (0) - Human entities
**Humidity** (1,200) - Humidity monitoring
**HVAC** (2,100) - HVAC systems
**HVAC_BMS** (1,260) - Building management
**Hypervisor** (100) - Virtualization
**HystericDiscourse** (1) - Psychoanalytic framework

### I

**ICS** (7,264) - Industrial Control Systems
**ICS_Asset** (16) - ICS assets
**ICS_FRAMEWORK** (137) - ICS frameworks
**ICS_Protocol** (10) - ICS protocols
**ICS_Tactic** (12) - ICS attack tactics
**ICS_Technique** (83) - ICS attack techniques
**ICS_THREAT_INTEL** (9,404) - ICS threat intelligence
**Identity** (0) - Identity entities
**ImaginaryRegister** (1) - Psychoanalytic concept
**ImpactAssessment** (0) - Impact analysis
**ImplementationPattern** (7) - Implementation patterns
**Incident** (2,112) - Security incidents
**IncidentCommand** (134) - Incident command
**IncidentCommandSystem** (600) - ICS structure
**IncidentDispatch** (38) - Incident response
**IncidentResolution** (2,090) - Incident resolution
**Indicator** (11,601) - Threat indicators
**Infrastructure** (50) - Infrastructure entities
**Insider_Threat_Indicator** (11) - Insider threats
**IntegrationStream** (100) - Integration data
**Intelligence_Analysis** (4,000) - Intelligence products
**IntelligenceSource** (600) - Intelligence sources
**IntrusionSet** (0) - Intrusion campaigns
**Intrusion_Detection** (1,260) - IDS systems
**Investigation** (0) - Investigations
**Investigation_Case** (10) - Investigation cases
**IPAddress** (0) - IP addresses
**Irrigation** (121) - Irrigation systems
**IrrigationControl** (75) - Irrigation automation
**IrrigationController** (188) - Irrigation devices
**IrrigationFlow** (1,180) - Water flow
**IrrigationMalfunction** (56) - Irrigation failures
**IrrigationZone** (21) - Irrigation zones
**IT** (9,300) - Information Technology
**ITAlert** (400) - IT alerts
**ITControl** (700) - IT controls
**ITDevice** (2,800) - IT equipment
**ITMeasurement** (18,000) - IT metrics
**ITProcess** (1,200) - IT processes
**ITProperty** (4,500) - IT properties
**ITZone** (200) - IT zones
**IT_Hardware** (1,100) - IT hardware
**IT_Infrastructure** (229) - IT infrastructure
**IT_INFRASTRUCTURE** (5,000) - IT systems
**IT_Software** (2,100) - IT software

### K

**KEV** (10) - Known Exploited Vulnerabilities
**KnowledgeBaseStats** (1) - KB statistics
**KubernetesCluster** (100) - K8s clusters

### L

**LawEnforcement** (875) - Law enforcement
**Level5** (5,543) - Automation Level 5
**Library** (10,000) - Software libraries
**License** (15,000) - Software licenses
**LicenseCompliance** (5,000) - License compliance
**LicensePolicy** (2,000) - License policies
**Livestock** (1,050) - Livestock management
**LivestockBarn** (4) - Livestock facilities
**LivestockFeeding** (127) - Feeding systems
**LivestockManagement** (74) - Livestock operations
**Location** (4,830) - Geographic locations
**LOG_ANALYSIS** (0) - Log analysis
**LogSource** (300) - Log sources

### M

**MajorAsset** (449) - Major assets
**MajorChemicalAsset** (0) - Major chemical assets
**MajorFacility** (150) - Major facilities
**MajorHealthcareAsset** (20) - Major healthcare assets
**MajorManufacturingAsset** (100) - Major manufacturing assets
**MaliciousPackage** (3) - Malicious packages
**Malware** (1,016) - Malware samples
**MALWARE** (3) - Malware entities
**ManufacturingAlert** (400) - Manufacturing alerts
**ManufacturingControl** (1,400) - Manufacturing controls
**ManufacturingEquipment** (11,200) - Manufacturing equipment
**ManufacturingMeasurement** (72,800) - Manufacturing metrics
**ManufacturingProcess** (2,800) - Manufacturing processes
**ManufacturingProperty** (5,000) - Manufacturing properties
**ManufacturingZone** (200) - Manufacturing zones
**MassCasualty** (58) - Mass casualty events
**MasterDiscourse** (1) - Psychoanalytic framework
**MeatProcessingPlant** (6) - Meat processing
**MedicalTreatment** (114) - Medical care
**Metadata** (65) - Metadata entities
**Middleware** (200) - Middleware systems
**MilkingSystem** (151) - Milking automation
**Milking** (129) - Milking operations
**MilkProduction** (1,221) - Milk metrics
**Mitigation** (5,224) - Risk mitigations
**MLModel** (200) - Machine learning models
**MobileCommand** (93) - Mobile command units
**MobileDevice** (200) - Mobile devices
**Motivation_Factor** (4) - Motivation analysis
**MutualAid** (110) - Mutual aid
**MutualAidCoordination** (91) - Mutual aid coordination
**MutualAidRequest** (52) - Mutual aid requests
**MutualAidZone** (56) - Mutual aid zones

### N

**NATION_STATE** (3) - Nation state actors
**Naval_Systems** (1,340) - Naval systems
**NERCCIPStandard** (100) - NERC CIP standards
**NetworkDevice** (348) - Network devices
**NetworkManagementSystem** (1,500) - Network management
**NetworkMeasurement** (27,458) - Network metrics
**NetworkSegment** (13) - Network segments
**Notification** (400) - Notifications
**Nuclear** (9,549) - Nuclear facilities
**NuclearAlert** (600) - Nuclear alerts
**NuclearDevice** (3,000) - Nuclear equipment
**NuclearProperty** (5,000) - Nuclear properties
**NuclearZone** (299) - Nuclear zones
**Nutrients** (1,224) - Nutrient monitoring

### O

**Observable** (0) - Observable entities
**OfficerSafety** (49) - Officer safety
**OperatingSystem** (200) - Operating systems
**OperationalMetric** (10) - Operational metrics
**OperationalParameter** (833) - Operational parameters
**Organization** (56,144) - Organizations
**OWASPCategory** (39) - OWASP categories

### P

**P25Radio** (891) - P25 radio systems
**Package** (10,017) - Software packages
**PackagingSystem** (79) - Packaging automation
**ParkingSpace** (200) - Parking management
**Pasture** (39) - Pasture management
**PatientTransport** (136) - Patient transport
**PaymentSystems** (9,041) - Payment systems
**PerformanceMetric** (500) - Performance metrics
**PeripheralDevice** (100) - Peripheral devices
**Personality_Trait** (20) - Personality analysis
**PersonnelAvailability** (2,133) - Personnel status
**PersonnelCertification** (664) - Personnel certs
**PestControl** (98) - Pest management
**PestOutbreak** (53) - Pest outbreaks
**pH** (1,197) - pH monitoring
**PhysicalAccessControl** (28) - Physical access
**PhysicalActuator** (10) - Physical actuators
**PhysicalSensor** (10) - Physical sensors
**PhysicalServer** (400) - Physical servers
**PhysicsConstraint** (10) - Physics constraints
**PHYSICAL_SECURITY** (286) - Physical security
**PipingAndValves** (3,920) - Piping systems
**Planter** (188) - Planting equipment
**Planting** (119) - Planting operations
**PLCStateChange** (0) - PLC state changes
**PoliceDistrict** (54) - Police districts
**PoliceStation** (10) - Police facilities
**PoliceVehicle** (226) - Police vehicles
**PrecisionAg** (241) - Precision agriculture
**Process** (34,504) - Processes
**ProcessControlSystems** (1,680) - Process control
**ProcessingArea** (40) - Processing areas
**ProcessingLine** (97) - Processing lines
**ProcessingPlant** (7) - Processing facilities
**ProcessingSCADA** (69) - Processing SCADA
**ProcessLoop** (0) - Process loops
**Project** (1) - Projects
**PropagationRule** (0) - Propagation rules
**Property** (61,700) - Properties
**Protocol** (13,336) - Communication protocols
**Provenance** (15,000) - Data provenance
**PsychologicalPattern** (6) - Psychological patterns
**PsychTrait** (161) - Psychological traits
**PumpsAndCompressors** (3,360) - Pumps and compressors

### Q

**QualityControl** (198) - Quality control
**QualityMetric** (500) - Quality metrics

### R

**RadiationMeasurement** (18,000) - Radiation metrics
**Reactors** (5,600) - Nuclear reactors
**ReactorControlSystem** (1,000) - Reactor controls
**ReactorProcess** (2,000) - Reactor processes
**RealRegister** (1) - Psychoanalytic concept
**RealTimeStream** (120) - Real-time data
**Region** (3) - Geographic regions
**Register** (3) - Registers
**Registry** (3) - Registries
**Relationship** (40,000) - Relationships
**RemediationPlan** (0) - Remediation plans
**RescueOperation** (135) - Rescue operations
**ResourceAllocation** (125) - Resource allocation
**ResourceAvailability** (2,124) - Resource availability
**ResourceInventory** (610) - Resource inventory
**ResourceManagement** (97) - Resource management
**ResourceShortage** (47) - Resource shortages
**ResponseMetric** (17,000) - Response metrics
**ResponseTime** (2,266) - Response times
**RevenueModel** (10) - Revenue models
**Role** (15) - Roles
**Router** (300) - Network routers
**RoutingProcess** (3,000) - Routing processes
**RTUCommunication** (0) - RTU communications

### S

**SafetyAndMonitoringSystems** (840) - Safety systems
**SafetyFunction** (10) - Safety functions
**SafetyInterlock** (0) - Safety interlocks
**Sanitation** (114) - Sanitation systems
**SanitationSystem** (101) - Sanitation infrastructure
**SAREF** (5,000) - Smart appliances
**SAREF_Actuator** (500) - Smart actuators
**SAREF_Core** (5,000) - SAREF core
**SAREF_Device** (4,600) - Smart devices
**SAREF_Measurement** (25,200) - Smart measurements
**Satellite_Systems** (3,649) - Satellite systems
**SBOM** (140,000) - Software Bill of Materials
**SBOMStandard** (5) - SBOM standards
**SBOMTool** (13) - SBOM tools
**SCADA** (82) - SCADA systems
**SCADAEvent** (0) - SCADA events
**SCADASystem** (300) - SCADA infrastructure
**Sector** (71) - Infrastructure sectors
**SecurityStream** (100) - Security data streams
**Sensor** (150) - Sensors
**SensorSource** (400) - Sensor sources
**SeparationEquipment** (4,480) - Separation equipment
**Server** (158) - Servers
**ServerlessFunction** (200) - Serverless functions
**Service** (2,100) - Services
**ServiceLevel** (10) - Service levels
**ServiceZone** (250) - Service zones
**SLA** (300) - Service level agreements
**SleepAnalysis** (167) - Sleep analysis
**Smart_City** (1,000) - Smart city infrastructure
**SocialMediaAccount** (400) - Social media accounts
**SocialMediaPost** (600) - Social media posts
**SocialNetwork** (600) - Social networks
**Social_Engineering_Tactic** (7) - Social engineering
**Social_Media_Intelligence** (1,600) - Social media intel
**SOCIAL_MEDIA** (0) - Social media
**Software** (1,694) - Software
**SoftwareComponent** (50,000) - Software components
**SoftwareLicense** (8,300) - Software licenses
**Software_Component** (55,000) - Software components
**SoilMeasurement** (200) - Soil measurements
**SoilMoisture** (1,225) - Soil moisture
**SoilSensor** (187) - Soil sensors
**Sprayer** (151) - Spraying equipment
**Standard** (2,567) - Standards
**State** (100) - States
**StateDeviation** (10) - State deviations
**STIX_Cyber_Observable** (18) - STIX observables
**STIX_Domain_Object** (12) - STIX domain objects
**STIX_Object** (30) - STIX objects
**StorageArray** (200) - Storage arrays
**StorageTanks** (4,200) - Storage tanks
**StreetLight** (300) - Street lights
**Substation** (200) - Electrical substations
**SupportContract** (0) - Support contracts
**Surveillance** (1,429) - Surveillance systems
**SurveillanceSystem** (29) - Surveillance infrastructure
**SymbolicRegister** (1) - Psychoanalytic concept
**System** (38) - Systems
**SystemResilience** (10) - System resilience

### T

**Tactic** (40) - Tactics
**Tag** (9) - Tags
**TARGET_SECTOR** (6) - Target sectors
**Technique** (4,360) - Techniques
**Temperature** (1,215) - Temperature monitoring
**TemporalEvent** (10) - Temporal events
**TemporalPattern** (0) - Temporal patterns
**TEST** (1) - Test entities
**Threat** (9,875) - Threats
**ThreatActor** (10,599) - Threat actors
**ThreatActorSocialProfile** (400) - Actor profiles
**ThreatFeed** (4) - Threat feeds
**ThreatModel** (1) - Threat models
**Threat_Actor_Analysis** (400) - Actor analysis
**THREAT_INTEL_SHARING** (55) - Intel sharing
**TimeSeries** (51,000) - Time series
**TimeSeriesAnalysis** (10) - Time series analysis
**Tool** (92) - Tools
**TOOL** (3) - Tool entities
**Tractor** (163) - Tractors
**TrafficLight** (150) - Traffic lights
**TrafficSensor** (150) - Traffic sensors
**TrainingFacility** (9) - Training facilities
**TrainingLevel** (620) - Training levels
**TransactionMetric** (17,000) - Transaction metrics
**Transformer** (400) - Transformers
**TransmissionLine** (400) - Transmission lines
**Transportation** (28,000) - Transportation
**TreatmentEffectiveness** (2,098) - Treatment metrics
**TreatmentProcess** (500) - Treatment processes
**TTP** (536) - Tactics, Techniques, Procedures

### U

**uco_core_UcoObject** (39) - UCO objects
**UCOClass** (0) - UCO classes
**UCO_Observable** (15) - UCO observables
**UnitOfMeasure** (100) - Units of measure
**UniversityDiscourse** (1) - Psychoanalytic framework
**URL** (0) - URLs

### V

**Validator** (300) - Validators
**Vendor** (0) - Vendors
**VentilationController** (131) - Ventilation systems
**VersionedNode** (10) - Versioned nodes
**VirtualMachine** (600) - Virtual machines
**VirtualMachineInstance** (300) - VM instances
**VirtualNetwork** (200) - Virtual networks
**Virtualization** (1,000) - Virtualization
**VULNERABILITY** (3) - Vulnerability entities
**VulnerabilityAttestation** (2,000) - Vulnerability attestations

### W

**WasteContainer** (100) - Waste containers
**WasteManager** (119) - Waste management
**WaterAlert** (500) - Water alerts
**WaterDevice** (1,500) - Water devices
**WaterProperty** (3,000) - Water properties
**WaterZone** (200) - Water zones
**Water_Distribution** (2,001) - Water distribution
**Water_Treatment** (25,199) - Water treatment
**WeatherData** (1,218) - Weather data
**WeatherStation** (170) - Weather stations
**WeatherWarning** (55) - Weather warnings
**WearableDevice** (500) - Wearable devices
**WearableSecurity** (166) - Wearable security
**Weakness** (0) - Weaknesses
**WebApplication** (100) - Web applications
**WhatIfScenario** (524) - Scenario analysis
**Workflow** (1,200) - Workflows
**Workstation** (300) - Workstations

### Z

**Zone** (2,070) - Zones

---

## Part 3: Domain Organization

### Domain 1: Threat Intelligence (389,929 nodes)

**Primary Labels:**
- CVE (316,552)
- Vulnerability (314,538)
- ThreatActor (10,599)
- Threat (9,875)
- ICS_THREAT_INTEL (9,404)
- FutureThreat (8,900)
- Mitigation (5,224)
- Detection (5,000)
- Technique (4,360)
- AttackPattern (2,070)
- AttackTechnique (1,657)
- Malware (1,016)
- CWE (1,006)
- ATT_CK_Technique (691)
- CybersecurityKB_Malware (667)
- CAPEC (615)
- TTP (536)
- CourseOfAction (276)
- CybersecurityKB_ThreatActor (181)
- Campaign (163)

**Usage:** Comprehensive threat intelligence covering vulnerabilities, attack patterns, threat actors, malware, and defensive measures across both IT and OT environments.

---

### Domain 2: Infrastructure & Equipment (345,527 nodes)

**Critical Infrastructure Sectors:**
- COMMUNICATIONS (40,759)
- SECTOR_DEFENSE_INDUSTRIAL_BASE (38,800)
- ENERGY (35,475)
- CHEMICAL (32,200)
- EMERGENCY_SERVICES (28,000)
- FOOD_AGRICULTURE (28,000)
- INFORMATION_TECHNOLOGY (28,000)
- FINANCIAL_SERVICES (28,000)
- COMMERCIAL_FACILITIES (28,000)
- Healthcare (28,000)
- Transportation (28,000)
- WATER (27,200)
- GOVERNMENT_FACILITIES (27,000)

**Equipment Types:**
- Equipment (48,288)
- ChemicalEquipment (28,000)
- DamsEquipment (14,074)
- ManufacturingEquipment (11,200)
- Device (48,400)
- EnergyDevice (10,000)

**Usage:** Complete infrastructure asset inventory across 16 critical infrastructure sectors with specialized equipment tracking.

---

### Domain 3: Software & Supply Chain (304,317 nodes)

**Primary Labels:**
- SBOM (140,000)
- Software_Component (55,000)
- SoftwareComponent (50,000)
- Dependency (40,000)
- Provenance (15,000)
- Build_Info (15,000)
- License (15,000)
- Package (10,017)
- Library (10,000)
- SoftwareLicense (8,300)
- DependencyTree (8,000)
- Build (8,000)
- Artifact (5,000)
- ContainerImage (5,000)
- Firmware (5,000)
- BuildSystem (5,000)
- LicenseCompliance (5,000)
- Attestation (5,000)
- DependencyPath (2,000)
- BuildTool (2,000)
- LicensePolicy (2,000)
- VulnerabilityAttestation (2,000)

**Usage:** Complete software supply chain visibility including components, dependencies, licenses, builds, and attestations.

---

### Domain 4: Measurements & Telemetry (297,858 nodes)

**Measurement Types:**
- Measurement (297,858 base)
- ManufacturingMeasurement (72,800)
- NetworkMeasurement (27,458)
- DefenseMeasurement (25,200)
- SAREF_Measurement (25,200)
- HealthcareMeasurement (18,200)
- ITMeasurement (18,000)
- RadiationMeasurement (18,000)
- ResponseMetric (17,000)
- AgricultureMetric (17,000)
- TransactionMetric (17,000)
- GovernmentMeasurement (5,600)
- ChemicalMeasurement (4,200)

**Specialized Metrics:**
- TimeSeries (51,000)
- HistoricalPattern (14,985)
- EquipmentPerformance (1,246)
- ColdChainTemp (1,232)
- FeedIntake (1,232)
- SoilMoisture (1,225)
- Nutrients (1,224)
- MilkProduction (1,221)
- FoodSafety (1,220)
- WeatherData (1,218)
- Temperature (1,215)
- Humidity (1,200)
- pH (1,197)
- CropYield (1,181)
- IrrigationFlow (1,180)

**Usage:** Comprehensive telemetry and metrics across all infrastructure sectors for monitoring, analysis, and predictive maintenance.

---

### Domain 5: Organizational & Compliance (112,311 nodes)

**Primary Labels:**
- Organization (56,144)
- Compliance (30,400)
- Control (66,391)
- Standard (2,567)
- NERCCIPStandard (100)
- ComplianceCertification (830)
- FacilityCertification (868)
- PersonnelCertification (664)
- CertificationExpiration (592)
- Governance (600)

**Usage:** Organizational structures, compliance tracking, regulatory standards, and certification management.

---

### Domain 6: Specialized Domains

#### Agriculture (53,000+ nodes)
- FOOD_AGRICULTURE (28,000)
- AgricultureMetric (17,000)
- FoodAgricultureProperty (5,000)
- FoodAgricultureDevice (3,500)
- CropProduction (1,750)
- Agriculture (1,500)
- AnimalHealth (1,263)
- FeedIntake (1,232)
- SoilMoisture (1,225)
- Nutrients (1,224)
- MilkProduction (1,221)
- FoodSafety (1,220)
- CropYield (1,181)
- IrrigationFlow (1,180)
- Livestock (1,050)
- Farm (200)

#### Healthcare (75,200+ nodes)
- Healthcare (28,000)
- HealthcareMeasurement (18,200)
- HealthcareProperty (5,000)
- HealthcareDevice (2,800)
- HealthcareProcess (1,200)
- Health_Monitor (1,500)
- HealthMetric (500)
- HealthcareControl (500)
- HealthcareAlert (200)
- HealthcareZone (80)
- MajorHealthcareAsset (20)

#### Energy (125,000+ nodes)
- ENERGY (35,475)
- Energy_Transmission (24,400)
- Energy (17,475)
- Energy_Distribution (10,325)
- EnergyDevice (10,000)
- EnergyProperty (6,000)
- Energy_Generation (750)
- DistributedEnergyResource (750)
- Transformer (400)
- TransmissionLine (400)
- Substation (200)

#### Defense (92,340+ nodes)
- SECTOR_DEFENSE_INDUSTRIAL_BASE (38,800)
- DefenseMeasurement (25,200)
- DefenseProperty (7,000)
- DefenseDevice (4,600)
- Aerospace_Defense (3,520)
- Naval_Systems (1,340)
- DefenseProcess (1,000)
- DefenseControl (500)
- DefenseAlert (300)
- DefenseZone (150)

#### Finance (56,000+ nodes)
- FINANCIAL_SERVICES (28,000)
- TransactionMetric (17,000)
- Banking (9,630)
- CapitalMarkets (9,329)
- PaymentSystems (9,041)
- FinancialServicesProperty (5,000)
- FinancialServicesDevice (3,500)
- FinancialProcess (1,200)
- FinancialControl (600)
- FinancialAlert (400)
- FinancialZone (250)

---

## Part 4: Usage Statistics

### Entity Distribution by Tier

**TIER 1 (TECHNICAL):** 650,000+ nodes
- Vulnerabilities, Threats, Infrastructure

**TIER 2 (ASSET):** 400,000+ nodes
- Equipment, Software, Components

**TIER 3 (ORGANIZATIONAL):** 112,000+ nodes
- Organizations, Compliance, Standards

**TIER 4 (OPERATIONAL):** 297,858+ nodes
- Measurements, Telemetry, Monitoring

### Super Label Distribution

**Vulnerability:** 314,538 nodes
**Asset:** 206,075 nodes
**Measurement:** 297,858 nodes
**Equipment:** 48,288 nodes
**Device:** 48,400 nodes
**ThreatActor:** 10,599 nodes
**Technique:** 4,360 nodes
**Organization:** 56,144 nodes

### Key Relationships

**Most Connected Entities:**
1. CVE → Affects assets, exploited by threats
2. Equipment → Has measurements, controlled by systems
3. Software_Component → Has dependencies, vulnerabilities
4. Measurement → Generated by devices, triggers alerts
5. ThreatActor → Uses techniques, deploys malware

---

## Part 5: Comprehensive Label Index

### Zero-Count Labels (Placeholder/Future)

These 50 labels exist in the schema but have no nodes currently:

**Threat & Attack:**
- IntrusionSet, Attack, Exploit, AttackTimeline, EventCorrelation

**UCO & STIX:**
- UCOClass, Observable, IPAddress, Domain, URL, EmailAddress, File, Hash, Identity, Human

**ICS/SCADA:**
- ProcessLoop, SafetyInterlock, PropagationRule, SCADAEvent, HMISession, PLCStateChange, RTUCommunication, DataFlow

**Chemical:**
- ChemicalProperty, ChemicalProcess, ChemicalControl, ChemicalAlert, ChemicalZone

**Intelligence:**
- SOCIAL_MEDIA, LOG_ANALYSIS, Investigation

**Infrastructure:**
- ImpactAssessment, CrossInfrastructureDependency, TemporalPattern, AlertRule, RemediationPlan, Weakness, ATTACK_Software

**Supply Chain:**
- Vendor, EquipmentModel, SupportContract

**EMB3D:**
- EMB3D_Threat, EMB3D_Property

**Others:**
- MajorChemicalAsset

**Usage:** These labels are defined in the ontology for future expansion or specialized use cases not yet populated.

---

## Appendix A: Relationship Patterns

### Common Relationship Types

1. **HAS_** - Ownership/Containment
   - HAS_VULNERABILITY
   - HAS_MEASUREMENT
   - HAS_LICENSE
   - HAS_WEAKNESS

2. **PART_OF** - Hierarchy/Composition
   - Component PART_OF System
   - Measurement PART_OF TimeSeries
   - Zone PART_OF Facility

3. **DEPENDS_ON** - Dependencies
   - Software DEPENDS_ON Library
   - Service DEPENDS_ON Infrastructure
   - Process DEPENDS_ON Equipment

4. **CONTROLS** - Control relationships
   - SCADA CONTROLS Equipment
   - Control CONTROLS Process
   - Automation CONTROLS Device

5. **MONITORS** - Monitoring
   - Sensor MONITORS Equipment
   - Monitoring MONITORS Asset
   - Alert MONITORS Threshold

6. **EXPLOITED_BY** - Threat relationships
   - Vulnerability EXPLOITED_BY ThreatActor
   - Weakness EXPLOITED_BY Malware
   - System EXPLOITED_BY AttackPattern

7. **MITIGATED_BY** - Defense
   - Vulnerability MITIGATED_BY Mitigation
   - Threat MITIGATED_BY CourseOfAction
   - Risk MITIGATED_BY Control

---

## Appendix B: Enrichment Status

### Enrichment Timestamps

**Recent Enrichments:**
- kaggle_enriched: 2025-12-12
- cpe_enriched: 2025-11-02
- uco_enriched_date: 2025-10-27
- created_date: 2025-10-31

### Validation Status
- VALIDATED: 90%+
- VERIFIED: 5%
- PENDING: 3%
- UNVERIFIED: 2%

---

## Conclusion

This catalog documents all 631 entity labels in the AEON knowledge graph, representing:

- **2,847,915 total nodes**
- **16 critical infrastructure sectors**
- **316,552 CVE vulnerabilities**
- **140,000 SBOM components**
- **297,858 measurements**
- **Complete threat intelligence coverage**
- **Comprehensive supply chain visibility**
- **Multi-sector operational monitoring**

The ontology provides a unified framework for cybersecurity, infrastructure management, supply chain security, and operational intelligence across all critical infrastructure domains.

---

**Document Status:** COMPLETE
**Last Updated:** 2025-12-12
**Next Review:** Quarterly
**Maintained By:** AEON Integration Team
