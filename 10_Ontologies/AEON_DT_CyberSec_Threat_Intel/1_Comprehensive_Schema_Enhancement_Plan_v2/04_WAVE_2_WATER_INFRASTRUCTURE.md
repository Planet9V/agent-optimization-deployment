# Wave 2: Water Infrastructure Domain Extensions

**File:** 04_WAVE_2_WATER_INFRASTRUCTURE.md
**Created:** 2025-10-30 00:00:00 UTC
**Version:** v1.0.0
**Status:** ACTIVE
**Purpose:** Complete implementation specification for Wave 2 water infrastructure ontology integration extending SAREF core for water treatment, distribution, and SCADA security

---

## 1. Wave Overview

### 1.1 Objectives

Wave 2 extends the SAREF core foundation (Wave 1) with water infrastructure domain-specific ontologies, creating cyber-physical security models for water treatment plants, distribution systems, and SCADA networks. This wave focuses on:

1. **Water Device Specialization**: Extend SAREF:Device for pumps, valves, sensors, RTUs specific to water infrastructure
2. **Process Modeling**: Represent water treatment processes (filtration, chlorination, UV treatment) with security implications
3. **SCADA Integration**: Model SCADA systems controlling water infrastructure with attack surface analysis
4. **Hydraulic Property Extensions**: Water-specific properties (flow rate, pressure, chemical concentration, turbidity)
5. **Regulatory Compliance**: Map devices and processes to water safety regulations (EPA, WHO standards)
6. **Critical Infrastructure Protection**: Implement Department of Homeland Security critical infrastructure frameworks

### 1.2 Duration & Resources

- **Estimated Duration**: 7-9 weeks
- **Target Node Count**: 12,000-18,000 new nodes
- **Relationship Count**: 35,000-55,000 new relationships
- **Integration Points**: 15 connection types (8 to Wave 1 SAREF, 7 to existing CVE/ICS data)
- **Rollback Complexity**: Low-Medium (additive with Wave 1 dependencies)

### 1.3 Dependencies

**Prerequisites:**
- Wave 1 SAREF core completed and validated
- Existing AEON graph with CVE/ICS data
- Water infrastructure asset inventory
- SCADA network topology documentation

**External Dependencies:**
- EPA Water Quality Standards
- WHO Drinking Water Guidelines
- ICS-CERT water sector advisories
- Water utility SCADA documentation (Rockwell, Siemens, Schneider Electric)

**Internal Dependencies:**
- Wave 3 (Energy Grid) may reference water-energy nexus
- Wave 4 (ICS Security) will leverage water SCADA attack patterns

---

## 2. Complete Node Schemas

### 2.1 Water:WaterDevice Node (extends SAREF:Device)

**Purpose:** Represents specialized water infrastructure devices inheriting SAREF core properties with water-specific extensions.

**Inheritance:** All properties from `SAREF:Device` (Wave 1) plus:

**Additional Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| waterDeviceType | String | Yes | Water infrastructure device classification | `Pump`, `Valve`, `Sensor`, `RTU`, `Chlorinator`, `Filter` |
| flowCapacity | Float | No | Maximum flow rate (gallons/minute) | `2500.0` |
| pressureRating | Float | No | Maximum pressure (PSI) | `150.0` |
| materialComposition | String | No | Primary material | `Stainless Steel 316`, `PVC`, `Cast Iron` |
| installationDepth | Float | No | Installation depth (feet below surface) | `15.5` |
| regulatoryZone | String | Yes | Water regulatory zone | `Zone-A-Treatment`, `Zone-B-Distribution` |
| epaAssetId | String | No | EPA asset tracking identifier | `EPA-WTR-2023-00147` |
| maintenanceSchedule | String | No | Maintenance frequency | `Quarterly`, `Biannual`, `Annual` |
| lastMaintenanceDate | DateTime | No | Last maintenance performed | `2024-09-15T08:00:00Z` |
| waterQualityImpact | String | Yes | Impact on water quality if compromised | `Critical`, `High`, `Medium`, `Low` |
| cyberPhysicalRisk | String | Yes | Cyber-physical attack risk | `Critical`, `High`, `Medium`, `Low` |

**Cypher CREATE Statement:**

```cypher
// Create specialized water device inheriting from SAREF:Device
CREATE (wd:Water:WaterDevice:Device {
    // SAREF:Device inherited properties
    deviceId: 'water:device:pump-wtp-001',
    name: 'High Service Pump 1 - Water Treatment Plant',
    model: 'Grundfos CR 64-2',
    manufacturer: 'Grundfos',
    firmwareVersion: 'V3.2.1',
    serialNumber: 'GF-2023-HSP-001',
    deviceCategory: 'Actuator',
    deploymentLocation: 'Water Treatment Plant - Building A, Pump Room',
    commissionDate: datetime('2023-03-20T10:00:00Z'),
    operationalStatus: 'Active',
    ipAddress: '192.168.10.50',
    macAddress: '00:1E:4F:A2:B3:C4',
    protocol: ['Modbus/TCP', 'Profibus'],
    criticality: 'Critical',
    lastUpdated: datetime(),

    // Water-specific properties
    waterDeviceType: 'Pump',
    flowCapacity: 2500.0,
    pressureRating: 150.0,
    materialComposition: 'Stainless Steel 316',
    installationDepth: 0.0,
    regulatoryZone: 'Zone-A-Treatment',
    epaAssetId: 'EPA-WTR-2023-00147',
    maintenanceSchedule: 'Quarterly',
    lastMaintenanceDate: datetime('2024-09-15T08:00:00Z'),
    waterQualityImpact: 'Critical',
    cyberPhysicalRisk: 'Critical'
})
```

**Indexes and Constraints:**

```cypher
// Water device type index for filtering
CREATE INDEX water_device_type_idx IF NOT EXISTS
FOR (wd:WaterDevice) ON (wd.waterDeviceType);

// Regulatory zone index for compliance queries
CREATE INDEX water_regulatory_zone_idx IF NOT EXISTS
FOR (wd:WaterDevice) ON (wd.regulatoryZone);

// EPA asset ID index for regulatory reporting
CREATE INDEX water_epa_asset_idx IF NOT EXISTS
FOR (wd:WaterDevice) ON (wd.epaAssetId);

// Composite index for cyber-physical risk assessment
CREATE INDEX water_cyber_risk_idx IF NOT EXISTS
FOR (wd:WaterDevice) ON (wd.cyberPhysicalRisk, wd.waterQualityImpact);
```

---

### 2.2 Water:WaterProperty Node (extends SAREF:Property)

**Purpose:** Represents water-specific measurable properties critical for safety and security monitoring.

**Inheritance:** All properties from `SAREF:Property` (Wave 1) plus:

**Additional Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| waterPropertyCategory | String | Yes | Property category | `Hydraulic`, `Chemical`, `Physical`, `Biological` |
| regulatoryLimit | Float | No | Maximum allowable limit (EPA/WHO) | `4.0` (mg/L for chlorine) |
| actionLevel | Float | No | Level triggering corrective action | `3.5` (mg/L) |
| healthImpact | String | Yes | Health impact if exceeded | `Critical`, `High`, `Medium`, `Low` |
| samplingFrequency | String | Yes | Required sampling frequency | `Continuous`, `Hourly`, `Daily`, `Weekly` |
| epaParameter | String | No | EPA parameter code | `EPA-1005` (Free Chlorine) |

**Cypher CREATE Statement:**

```cypher
CREATE (wp:Water:WaterProperty:Property {
    // SAREF:Property inherited properties
    propertyId: 'water:property:chlorine-residual-001',
    propertyType: 'ChemicalConcentration',
    unitOfMeasure: 'mg/L',
    minValue: 0.0,
    maxValue: 4.0,
    normalRangeMin: 0.2,
    normalRangeMax: 2.0,
    criticalThresholdMin: 0.1,
    criticalThresholdMax: 4.0,
    measurementAccuracy: 0.01,
    description: 'Free chlorine residual in distribution system',
    lastCalibration: datetime('2024-08-20T09:00:00Z'),

    // Water-specific properties
    waterPropertyCategory: 'Chemical',
    regulatoryLimit: 4.0,
    actionLevel: 3.5,
    healthImpact: 'Critical',
    samplingFrequency: 'Continuous',
    epaParameter: 'EPA-1005'
})
```

**Indexes and Constraints:**

```cypher
CREATE INDEX water_property_category_idx IF NOT EXISTS
FOR (wp:WaterProperty) ON (wp.waterPropertyCategory);

CREATE INDEX water_epa_parameter_idx IF NOT EXISTS
FOR (wp:WaterProperty) ON (wp.epaParameter);

CREATE INDEX water_health_impact_idx IF NOT EXISTS
FOR (wp:WaterProperty) ON (wp.healthImpact);
```

---

### 2.3 Water:TreatmentProcess Node

**Purpose:** Represents water treatment processes with security and safety implications.

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| processId | String | Yes | Unique process identifier | `water:process:chlorination-001` |
| processName | String | Yes | Human-readable process name | `Primary Chlorination` |
| processType | String | Yes | Treatment process category | `Disinfection`, `Filtration`, `Coagulation`, `UV` |
| processStage | String | Yes | Treatment stage | `PreTreatment`, `Primary`, `Secondary`, `Final` |
| flowRate | Float | No | Design flow rate (MGD) | `5.0` |
| retentionTime | Float | No | Process retention time (minutes) | `30.0` |
| efficiency | Float | No | Process efficiency percentage | `99.5` |
| criticalityRating | String | Yes | Process criticality | `Critical`, `High`, `Medium`, `Low` |
| redundancyLevel | String | Yes | Redundancy configuration | `None`, `Standby`, `Parallel`, `N+1` |
| automationLevel | String | Yes | Automation level | `Manual`, `SemiAutomatic`, `FullyAutomatic` |
| scadaControlled | Boolean | Yes | SCADA control enabled | `true` |
| safetyInterlocks | String[] | No | Safety interlock systems | `["HighPressureShutoff", "LowFlowAlarm"]` |

**Cypher CREATE Statement:**

```cypher
CREATE (tp:Water:TreatmentProcess {
    processId: 'water:process:chlorination-001',
    processName: 'Primary Chlorination',
    processType: 'Disinfection',
    processStage: 'Primary',
    flowRate: 5.0,
    retentionTime: 30.0,
    efficiency: 99.5,
    criticalityRating: 'Critical',
    redundancyLevel: 'N+1',
    automationLevel: 'FullyAutomatic',
    scadaControlled: true,
    safetyInterlocks: ['HighPressureShutoff', 'LowFlowAlarm', 'ChlorineLeakDetection']
})
```

**Indexes and Constraints:**

```cypher
CREATE CONSTRAINT treatment_process_id_unique IF NOT EXISTS
FOR (tp:TreatmentProcess) REQUIRE tp.processId IS UNIQUE;

CREATE INDEX treatment_process_type_idx IF NOT EXISTS
FOR (tp:TreatmentProcess) ON (tp.processType);

CREATE INDEX treatment_criticality_idx IF NOT EXISTS
FOR (tp:TreatmentProcess) ON (tp.criticalityRating);

CREATE INDEX treatment_scada_idx IF NOT EXISTS
FOR (tp:TreatmentProcess) ON (tp.scadaControlled);
```

---

### 2.4 Water:DistributionZone Node

**Purpose:** Represents geographic distribution zones for water network segmentation and security.

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| zoneId | String | Yes | Unique zone identifier | `water:zone:dist-north-001` |
| zoneName | String | Yes | Human-readable zone name | `North Distribution Zone` |
| zoneType | String | Yes | Zone classification | `Treatment`, `Distribution`, `Storage`, `Transfer` |
| population | Integer | No | Population served | `45000` |
| area | Float | No | Geographic area (sq miles) | `12.5` |
| averagePressure | Float | No | Average pressure (PSI) | `65.0` |
| storageCapacity | Float | No | Storage capacity (gallons) | `2000000.0` |
| demandProfile | String | No | Demand pattern | `Residential`, `Industrial`, `Mixed` |
| vulnerabilityScore | Float | Yes | Zone vulnerability score (0-1) | `0.65` |
| criticalInfrastructure | Boolean | Yes | Contains critical infrastructure | `true` |

**Cypher CREATE Statement:**

```cypher
CREATE (dz:Water:DistributionZone {
    zoneId: 'water:zone:dist-north-001',
    zoneName: 'North Distribution Zone',
    zoneType: 'Distribution',
    population: 45000,
    area: 12.5,
    averagePressure: 65.0,
    storageCapacity: 2000000.0,
    demandProfile: 'Residential',
    vulnerabilityScore: 0.65,
    criticalInfrastructure: true
})
```

**Indexes and Constraints:**

```cypher
CREATE CONSTRAINT distribution_zone_id_unique IF NOT EXISTS
FOR (dz:DistributionZone) REQUIRE dz.zoneId IS UNIQUE;

CREATE INDEX distribution_zone_type_idx IF NOT EXISTS
FOR (dz:DistributionZone) ON (dz.zoneType);

CREATE INDEX distribution_vulnerability_idx IF NOT EXISTS
FOR (dz:DistributionZone) ON (dz.vulnerabilityScore);
```

---

### 2.5 Water:SCADASystem Node

**Purpose:** Represents SCADA systems controlling water infrastructure with detailed security attributes.

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| scadaId | String | Yes | Unique SCADA system identifier | `water:scada:wtp-master-001` |
| systemName | String | Yes | Human-readable system name | `Water Treatment Plant Master SCADA` |
| vendor | String | Yes | SCADA vendor | `Schneider Electric`, `Siemens`, `Rockwell` |
| softwareVersion | String | Yes | SCADA software version | `ClearSCADA 2023 R2` |
| hmiCount | Integer | No | Number of HMI stations | `5` |
| rtuCount | Integer | No | Number of connected RTUs | `47` |
| plcCount | Integer | No | Number of connected PLCs | `23` |
| networkArchitecture | String | Yes | Network architecture type | `Flat`, `Segmented`, `DMZ-Protected` |
| remoteAccessEnabled | Boolean | Yes | Remote access configuration | `true` |
| authenticationMethod | String | Yes | Authentication method | `LDAP`, `Local`, `MultiFactorAuth` |
| encryptionEnabled | Boolean | Yes | Data encryption status | `false` |
| logRetentionDays | Integer | No | Log retention period | `90` |
| lastSecurityAudit | DateTime | No | Last security audit date | `2024-06-15T00:00:00Z` |
| complianceFramework | String[] | No | Compliance frameworks | `["NIST-800-82", "ICS-CERT"]` |

**Cypher CREATE Statement:**

```cypher
CREATE (ss:Water:SCADASystem {
    scadaId: 'water:scada:wtp-master-001',
    systemName: 'Water Treatment Plant Master SCADA',
    vendor: 'Schneider Electric',
    softwareVersion: 'ClearSCADA 2023 R2',
    hmiCount: 5,
    rtuCount: 47,
    plcCount: 23,
    networkArchitecture: 'Segmented',
    remoteAccessEnabled: true,
    authenticationMethod: 'LDAP',
    encryptionEnabled: false,
    logRetentionDays: 90,
    lastSecurityAudit: datetime('2024-06-15T00:00:00Z'),
    complianceFramework: ['NIST-800-82', 'ICS-CERT', 'AWWA-J100']
})
```

**Indexes and Constraints:**

```cypher
CREATE CONSTRAINT scada_system_id_unique IF NOT EXISTS
FOR (ss:SCADASystem) REQUIRE ss.scadaId IS UNIQUE;

CREATE INDEX scada_vendor_idx IF NOT EXISTS
FOR (ss:SCADASystem) ON (ss.vendor);

CREATE INDEX scada_network_architecture_idx IF NOT EXISTS
FOR (ss:SCADASystem) ON (ss.networkArchitecture);

CREATE INDEX scada_remote_access_idx IF NOT EXISTS
FOR (ss:SCADASystem) ON (ss.remoteAccessEnabled, ss.encryptionEnabled);
```

---

### 2.6 Water:WaterQualityStandard Node

**Purpose:** Represents regulatory water quality standards (EPA, WHO) for compliance monitoring.

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| standardId | String | Yes | Unique standard identifier | `water:standard:epa-mcl-chlorine` |
| regulatoryBody | String | Yes | Issuing regulatory body | `EPA`, `WHO`, `StateRegulator` |
| parameterName | String | Yes | Parameter being regulated | `Free Chlorine` |
| maximumContaminantLevel | Float | No | MCL value | `4.0` |
| maximumContaminantLevelGoal | Float | No | MCLG value | `4.0` |
| unitOfMeasure | String | Yes | Measurement unit | `mg/L` |
| healthEffect | String | Yes | Health effect description | `Eye/nose irritation, stomach discomfort` |
| monitoringFrequency | String | Yes | Required monitoring frequency | `Daily` |
| publicNotificationRequired | Boolean | Yes | Public notification if exceeded | `true` |
| regulationReference | String | Yes | Regulation citation | `40 CFR 141.74` |
| effectiveDate | DateTime | Yes | Regulation effective date | `2006-01-01T00:00:00Z` |

**Cypher CREATE Statement:**

```cypher
CREATE (wqs:Water:WaterQualityStandard {
    standardId: 'water:standard:epa-mcl-chlorine',
    regulatoryBody: 'EPA',
    parameterName: 'Free Chlorine',
    maximumContaminantLevel: 4.0,
    maximumContaminantLevelGoal: 4.0,
    unitOfMeasure: 'mg/L',
    healthEffect: 'Eye/nose irritation, stomach discomfort at high levels',
    monitoringFrequency: 'Daily',
    publicNotificationRequired: true,
    regulationReference: '40 CFR 141.74',
    effectiveDate: datetime('2006-01-01T00:00:00Z')
})
```

**Indexes and Constraints:**

```cypher
CREATE CONSTRAINT water_quality_standard_id_unique IF NOT EXISTS
FOR (wqs:WaterQualityStandard) REQUIRE wqs.standardId IS UNIQUE;

CREATE INDEX water_standard_regulatory_body_idx IF NOT EXISTS
FOR (wqs:WaterQualityStandard) ON (wqs.regulatoryBody);

CREATE INDEX water_standard_parameter_idx IF NOT EXISTS
FOR (wqs:WaterQualityStandard) ON (wqs.parameterName);
```

---

### 2.7 Water:WaterIncident Node

**Purpose:** Represents water infrastructure security/safety incidents for historical analysis and pattern recognition.

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| incidentId | String | Yes | Unique incident identifier | `water:incident:2024-047` |
| incidentType | String | Yes | Incident classification | `CyberAttack`, `Contamination`, `SystemFailure`, `PhysicalSecurity` |
| severity | String | Yes | Incident severity | `Critical`, `High`, `Medium`, `Low` |
| detectedAt | DateTime | Yes | Detection timestamp | `2024-03-15T14:23:00Z` |
| resolvedAt | DateTime | No | Resolution timestamp | `2024-03-15T18:45:00Z` |
| affectedPopulation | Integer | No | Population impacted | `12000` |
| rootCause | String | No | Root cause analysis | `Unauthorized SCADA access via stolen credentials` |
| publicNotified | Boolean | Yes | Public notification issued | `true` |
| regulatoryReported | Boolean | Yes | Reported to regulators | `true` |
| financialImpact | Float | No | Financial impact (USD) | `487000.0` |
| lessonsLearned | String | No | Lessons learned summary | `Implement MFA on all SCADA access` |

**Cypher CREATE Statement:**

```cypher
CREATE (wi:Water:WaterIncident {
    incidentId: 'water:incident:2024-047',
    incidentType: 'CyberAttack',
    severity: 'High',
    detectedAt: datetime('2024-03-15T14:23:00Z'),
    resolvedAt: datetime('2024-03-15T18:45:00Z'),
    affectedPopulation: 12000,
    rootCause: 'Unauthorized SCADA access via stolen credentials',
    publicNotified: true,
    regulatoryReported: true,
    financialImpact: 487000.0,
    lessonsLearned: 'Implement MFA on all SCADA access points and enhance credential monitoring'
})
```

**Indexes and Constraints:**

```cypher
CREATE CONSTRAINT water_incident_id_unique IF NOT EXISTS
FOR (wi:WaterIncident) REQUIRE wi.incidentId IS UNIQUE;

CREATE INDEX water_incident_type_idx IF NOT EXISTS
FOR (wi:WaterIncident) ON (wi.incidentType);

CREATE INDEX water_incident_detected_idx IF NOT EXISTS
FOR (wi:WaterIncident) ON (wi.detectedAt);

CREATE INDEX water_incident_severity_idx IF NOT EXISTS
FOR (wi:WaterIncident) ON (wi.severity);
```

---

## 3. Complete Relationship Schemas

### 3.1 PART_OF_PROCESS Relationship

**Purpose:** Links water devices to treatment processes they participate in.

**Source:** `Water:WaterDevice`
**Target:** `Water:TreatmentProcess`
**Cardinality:** Many-to-Many (1 device can be part of multiple processes, 1 process uses multiple devices)

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| role | String | Yes | Device role in process | `Primary`, `Backup`, `Monitoring`, `Control` |
| criticality | String | Yes | Role criticality | `Essential`, `Important`, `Supplementary` |
| assignedDate | DateTime | Yes | When device was assigned to process | `2023-03-20T10:00:00Z` |
| isActive | Boolean | Yes | Currently active in process | `true` |

**Cypher CREATE Statement:**

```cypher
MATCH (wd:WaterDevice {deviceId: 'water:device:pump-wtp-001'})
MATCH (tp:TreatmentProcess {processId: 'water:process:chlorination-001'})
CREATE (wd)-[r:PART_OF_PROCESS {
    role: 'Primary',
    criticality: 'Essential',
    assignedDate: datetime('2023-03-20T10:00:00Z'),
    isActive: true
}]->(tp)
```

---

### 3.2 LOCATED_IN_ZONE Relationship

**Purpose:** Connects water devices to their distribution zones.

**Source:** `Water:WaterDevice`
**Target:** `Water:DistributionZone`
**Cardinality:** Many-to-One (many devices in one zone)

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| assignedDate | DateTime | Yes | Zone assignment date | `2023-03-20T10:00:00Z` |
| gpsCoordinates | String | No | GPS location | `40.7128,-74.0060` |

**Cypher CREATE Statement:**

```cypher
MATCH (wd:WaterDevice {deviceId: 'water:device:pump-wtp-001'})
MATCH (dz:DistributionZone {zoneId: 'water:zone:dist-north-001'})
CREATE (wd)-[r:LOCATED_IN_ZONE {
    assignedDate: datetime('2023-03-20T10:00:00Z'),
    gpsCoordinates: '40.7128,-74.0060'
}]->(dz)
```

---

### 3.3 CONTROLLED_BY_SCADA Relationship

**Purpose:** Links water devices to SCADA systems controlling them.

**Source:** `Water:WaterDevice`
**Target:** `Water:SCADASystem`
**Cardinality:** Many-to-One (many devices controlled by one SCADA system)

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| controlType | String | Yes | Control mode | `Automatic`, `Manual`, `Supervisory` |
| pollingInterval | Integer | No | Data polling interval (seconds) | `5` |
| lastCommunication | DateTime | No | Last successful communication | `2025-10-30T14:23:00Z` |
| communicationProtocol | String | Yes | Protocol used | `Modbus/TCP`, `DNP3`, `OPC-UA` |
| failsafeMode | String | No | Behavior on SCADA failure | `LastKnownGood`, `SafeShutdown`, `LocalControl` |

**Cypher CREATE Statement:**

```cypher
MATCH (wd:WaterDevice {deviceId: 'water:device:pump-wtp-001'})
MATCH (ss:SCADASystem {scadaId: 'water:scada:wtp-master-001'})
CREATE (wd)-[r:CONTROLLED_BY_SCADA {
    controlType: 'Automatic',
    pollingInterval: 5,
    lastCommunication: datetime('2025-10-30T14:23:00Z'),
    communicationProtocol: 'Modbus/TCP',
    failsafeMode: 'SafeShutdown'
}]->(ss)
```

---

### 3.4 COMPLIES_WITH_STANDARD Relationship

**Purpose:** Links water properties to regulatory standards they must meet.

**Source:** `Water:WaterProperty`
**Target:** `Water:WaterQualityStandard`
**Cardinality:** Many-to-Many (1 property may comply with multiple standards, 1 standard applies to multiple properties)

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| complianceStatus | String | Yes | Current compliance status | `Compliant`, `NonCompliant`, `UnderReview` |
| lastAssessment | DateTime | Yes | Last compliance assessment | `2024-10-15T00:00:00Z` |
| nextAssessment | DateTime | No | Next scheduled assessment | `2025-01-15T00:00:00Z` |

**Cypher CREATE Statement:**

```cypher
MATCH (wp:WaterProperty {propertyId: 'water:property:chlorine-residual-001'})
MATCH (wqs:WaterQualityStandard {standardId: 'water:standard:epa-mcl-chlorine'})
CREATE (wp)-[r:COMPLIES_WITH_STANDARD {
    complianceStatus: 'Compliant',
    lastAssessment: datetime('2024-10-15T00:00:00Z'),
    nextAssessment: datetime('2025-01-15T00:00:00Z')
}]->(wqs)
```

---

### 3.5 INVOLVED_IN_INCIDENT Relationship

**Purpose:** Links devices or processes to security/safety incidents.

**Source:** `Water:WaterDevice` OR `Water:TreatmentProcess` OR `Water:SCADASystem`
**Target:** `Water:WaterIncident`
**Cardinality:** Many-to-Many (1 device/process/system can be involved in multiple incidents, 1 incident can involve multiple entities)

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| involvement | String | Yes | Nature of involvement | `PointOfCompromise`, `AffectedAsset`, `DetectionPoint` |
| impactLevel | String | Yes | Impact on this entity | `Total`, `Partial`, `Minimal` |

**Cypher CREATE Statement:**

```cypher
MATCH (ss:SCADASystem {scadaId: 'water:scada:wtp-master-001'})
MATCH (wi:WaterIncident {incidentId: 'water:incident:2024-047'})
CREATE (ss)-[r:INVOLVED_IN_INCIDENT {
    involvement: 'PointOfCompromise',
    impactLevel: 'Partial'
}]->(wi)
```

---

### 3.6 MONITORS_PROCESS Relationship

**Purpose:** Links SCADA systems to treatment processes they monitor.

**Source:** `Water:SCADASystem`
**Target:** `Water:TreatmentProcess`
**Cardinality:** Many-to-Many (1 SCADA can monitor multiple processes, 1 process can be monitored by multiple SCADA systems)

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| monitoringMode | String | Yes | Monitoring configuration | `RealTime`, `Periodic`, `OnDemand` |
| alarmEnabled | Boolean | Yes | Alarm notifications enabled | `true` |
| dataLoggingInterval | Integer | No | Data logging frequency (seconds) | `60` |

**Cypher CREATE Statement:**

```cypher
MATCH (ss:SCADASystem {scadaId: 'water:scada:wtp-master-001'})
MATCH (tp:TreatmentProcess {processId: 'water:process:chlorination-001'})
CREATE (ss)-[r:MONITORS_PROCESS {
    monitoringMode: 'RealTime',
    alarmEnabled: true,
    dataLoggingInterval: 60
}]->(tp)
```

---

### 3.7 HAS_WATER_PROPERTY Relationship (extends HAS_PROPERTY from Wave 1)

**Purpose:** Specialized property relationship with water-specific metadata.

**Source:** `Water:WaterDevice`
**Target:** `Water:WaterProperty`
**Cardinality:** Many-to-Many

**Properties:** Inherits from `HAS_PROPERTY` plus:

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| samplePoint | String | No | Sampling location | `InfluentPoint`, `EffluentPoint`, `DistributionMain` |
| regulatoryRequired | Boolean | Yes | Regulatory requirement | `true` |

**Cypher CREATE Statement:**

```cypher
MATCH (wd:WaterDevice {deviceId: 'water:device:chlorine-analyzer-001'})
MATCH (wp:WaterProperty {propertyId: 'water:property:chlorine-residual-001'})
CREATE (wd)-[r:HAS_WATER_PROPERTY:HAS_PROPERTY {
    assignedDate: datetime('2023-03-20T10:00:00Z'),
    isActive: true,
    monitoringPriority: 'Critical',
    samplePoint: 'EffluentPoint',
    regulatoryRequired: true
}]->(wp)
```

---

### 3.8 THREATENS_WATER_INFRASTRUCTURE Relationship (extends VULNERABLE_TO)

**Purpose:** Links water devices to CVE vulnerabilities with water-specific impact assessment.

**Source:** `Water:WaterDevice`
**Target:** `CVE` (existing node)
**Cardinality:** Many-to-Many

**Properties:** Inherits from `VULNERABLE_TO` plus:

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| waterSafetyImpact | String | Yes | Impact on water safety | `DirectContamination`, `ProcessDisruption`, `MonitoringBlindness` |
| populationAtRisk | Integer | No | Population potentially affected | `45000` |
| dhsSectorAlert | String | No | DHS sector alert ID | `DHS-WATER-2024-0012` |

**Cypher CREATE Statement:**

```cypher
MATCH (wd:WaterDevice {deviceId: 'water:device:pump-wtp-001'})
MATCH (cve:CVE {cveId: 'CVE-2023-98765'})
CREATE (wd)-[r:THREATENS_WATER_INFRASTRUCTURE:VULNERABLE_TO {
    discoveredDate: datetime('2024-03-15T00:00:00Z'),
    affectedFirmwareVersions: ['V3.2.0', 'V3.2.1'],
    patchAvailable: true,
    patchVersion: 'V3.3.0',
    exploitabilityScore: 3.9,
    impactScore: 5.9,
    isExploited: false,
    mitigationStatus: 'Unpatched',
    waterSafetyImpact: 'ProcessDisruption',
    populationAtRisk: 45000,
    dhsSectorAlert: 'DHS-WATER-2024-0012'
}]->(cve)
```

---

## 4. Integration Patterns

### 4.1 Integration with Wave 1 SAREF Core

Wave 2 extends Wave 1 through inheritance and relationship augmentation:

#### Integration Point 1: Device Inheritance

**Query to create water device inheriting from SAREF:Device:**

```cypher
// Create water device with full SAREF inheritance
CREATE (wd:Water:WaterDevice:Device {
    // All SAREF:Device properties automatically available
    deviceId: 'water:device:valve-dist-north-025',
    name: 'Distribution Zone North - Control Valve 25',
    model: 'Cla-Val 90-01',
    manufacturer: 'Cla-Val',
    firmwareVersion: 'V2.1.4',
    deviceCategory: 'Actuator',
    criticality: 'High',

    // Water-specific extensions
    waterDeviceType: 'Valve',
    flowCapacity: 1200.0,
    pressureRating: 200.0,
    regulatoryZone: 'Zone-B-Distribution',
    waterQualityImpact: 'Medium',
    cyberPhysicalRisk: 'High'
})

// Verify inheritance - query works for both SAREF and Water layers
MATCH (d:Device)
WHERE d.criticality = 'High'
RETURN d.deviceId, d.name, labels(d)

// Returns both SAREF:Device and Water:WaterDevice:Device nodes
```

**Validation:**
```cypher
// Verify water devices appear in SAREF device queries
MATCH (d:Device)
WHERE d:WaterDevice
RETURN count(d) as waterDevicesInSAREF

// Expected: All water devices (1,500-2,000 nodes)
```

---

#### Integration Point 2: Property Extension

**Query linking water properties to SAREF measurement framework:**

```cypher
// Water property extends SAREF property
MATCH (wp:WaterProperty {propertyId: 'water:property:flow-rate-001'})

// Inherits SAREF measurement generation
MATCH (wp)-[:GENERATES_MEASUREMENT]->(m:Measurement)
WHERE m.timestamp > datetime() - duration({hours: 24})

// Water-specific analysis
WITH wp, m
WHERE m.value < wp.normalRangeMin OR m.value > wp.normalRangeMax
RETURN wp.propertyId,
       wp.waterPropertyCategory,
       wp.healthImpact,
       count(m) as abnormalMeasurements,
       collect(m.value)[..5] as sampleValues

// Demonstrates seamless integration: water properties use SAREF measurement infrastructure
```

---

#### Integration Point 3: Service Architecture Extension

**Query showing water devices inheriting SAREF service model:**

```cypher
// Water device offers SAREF services
MATCH (wd:WaterDevice)-[o:OFFERS_SERVICE]->(s:Service)
WHERE s.protocol IN ['Modbus/TCP', 'DNP3']

// Add water-specific service context
WITH wd, s
MATCH (wd)-[:CONTROLLED_BY_SCADA]->(scada:SCADASystem)

RETURN wd.deviceId,
       wd.waterDeviceType,
       s.serviceName,
       s.protocol,
       s.authenticationRequired,
       s.encryptionEnabled,
       scada.systemName,
       scada.vendor,
       CASE
         WHEN s.authenticationRequired = false AND wd.cyberPhysicalRisk = 'Critical'
         THEN 'ImmediateAction'
         WHEN s.encryptionEnabled = false AND wd.waterQualityImpact = 'Critical'
         THEN 'HighPriority'
         ELSE 'Monitor'
       END as remediationPriority

// Demonstrates SAREF service model extended with water safety context
```

---

### 4.2 Integration with Existing CVE/ICS Data

#### Integration Point 4: Water-Specific CVE Mapping

**Query connecting water devices to relevant CVEs from existing graph:**

```cypher
// Match existing CVE nodes affecting water infrastructure
MATCH (cve:CVE)
WHERE cve.description CONTAINS 'water'
   OR cve.description CONTAINS 'SCADA'
   OR cve.description CONTAINS 'pump'
   OR cve.description CONTAINS 'valve'
   OR cve.affectedProducts CONTAINS 'Grundfos'
   OR cve.affectedProducts CONTAINS 'Cla-Val'
   OR cve.affectedProducts CONTAINS 'Schneider'

// Match water devices potentially affected
MATCH (wd:WaterDevice)
WHERE wd.manufacturer IN ['Grundfos', 'Cla-Val', 'Schneider Electric']
  AND (
    cve.affectedProducts CONTAINS wd.model
    OR cve.affectedProducts CONTAINS wd.manufacturer
  )

// Calculate water-specific impact
WITH wd, cve,
     CASE wd.waterQualityImpact
       WHEN 'Critical' THEN 'DirectContamination'
       WHEN 'High' THEN 'ProcessDisruption'
       ELSE 'MonitoringBlindness'
     END as waterSafetyImpact

// Match distribution zone to determine population at risk
MATCH (wd)-[:LOCATED_IN_ZONE]->(dz:DistributionZone)

// Create water-specific vulnerability relationship
CREATE (wd)-[r:THREATENS_WATER_INFRASTRUCTURE:VULNERABLE_TO {
    discoveredDate: cve.publishedDate,
    affectedFirmwareVersions: [wd.firmwareVersion],
    patchAvailable: CASE WHEN cve.patchStatus = 'Available' THEN true ELSE false END,
    exploitabilityScore: cve.exploitabilityScore,
    impactScore: cve.impactScore,
    isExploited: cve.exploitedInWild,
    mitigationStatus: 'Unpatched',
    waterSafetyImpact: waterSafetyImpact,
    populationAtRisk: dz.population,
    dhsSectorAlert: CASE
      WHEN cve.cvssScore >= 9.0 THEN 'DHS-WATER-' + substring(cve.cveId, 4, 4) + '-' + substring(cve.cveId, 9)
      ELSE null
    END
}]->(cve)

RETURN count(r) as waterVulnerabilitiesLinked
```

**Expected Results:** 1,200-1,800 water-specific CVE links

---

#### Integration Point 5: SCADA CVE Correlation

**Query linking SCADA systems to known vulnerabilities:**

```cypher
// Match SCADA systems with known vulnerable software
MATCH (ss:SCADASystem)

// Match CVEs affecting SCADA vendors
MATCH (cve:CVE)
WHERE cve.description CONTAINS ss.vendor
   OR cve.affectedProducts CONTAINS ss.softwareVersion

// Create SCADA-specific vulnerability tracking
CREATE (ss)-[r:HAS_SCADA_VULNERABILITY {
    discoveredDate: cve.publishedDate,
    softwareVersion: ss.softwareVersion,
    patchAvailable: CASE WHEN cve.patchStatus = 'Available' THEN true ELSE false END,
    cvssScore: cve.cvssScore,
    remoteExploitable: cve.accessVector = 'Network',
    systemsAffected: ss.hmiCount + ss.rtuCount + ss.plcCount,
    mitigationPriority: CASE
      WHEN ss.remoteAccessEnabled = true AND cve.cvssScore >= 9.0 THEN 'Critical'
      WHEN ss.remoteAccessEnabled = true AND cve.cvssScore >= 7.0 THEN 'High'
      WHEN cve.cvssScore >= 7.0 THEN 'Medium'
      ELSE 'Low'
    END
}]->(cve)

RETURN ss.systemName,
       ss.vendor,
       ss.networkArchitecture,
       ss.remoteAccessEnabled,
       count(cve) as vulnerabilityCount,
       collect(cve.cveId)[..5] as topCVEs
ORDER BY vulnerabilityCount DESC
```

**Expected Results:** 400-600 SCADA vulnerability links

---

### 4.3 Additive Enhancement Verification

#### Example 1: Water Device Enriching Existing Asset Data

**Before Wave 2:**
```cypher
// Generic asset from existing graph
(asset:Asset {
    assetId: 'ASSET-PUMP-WTP-001',
    type: 'IndustrialPump',
    location: 'Water Treatment Plant'
})

// SAREF device from Wave 1
(d:Device {
    deviceId: 'saref:device:pump-wtp-001',
    name: 'High Service Pump 1'
})-[:REPRESENTS_ASSET]->(asset)
```

**After Wave 2:**
```cypher
// Same generic asset and SAREF device, now enriched with water domain semantics
(wd:WaterDevice:Device {
    deviceId: 'saref:device:pump-wtp-001',
    // All SAREF properties plus water extensions
    waterDeviceType: 'Pump',
    flowCapacity: 2500.0,
    regulatoryZone: 'Zone-A-Treatment',
    waterQualityImpact: 'Critical'
})-[:REPRESENTS_ASSET]->(asset)

// Now supports water-specific queries
MATCH (asset:Asset {assetId: 'ASSET-PUMP-WTP-001'})
MATCH (wd:WaterDevice)-[:REPRESENTS_ASSET]->(asset)
MATCH (wd)-[:PART_OF_PROCESS]->(tp:TreatmentProcess)
MATCH (wd)-[:VULNERABLE_TO]->(cve:CVE)
RETURN asset.assetId,
       wd.waterDeviceType,
       wd.flowCapacity,
       tp.processName,
       count(cve) as vulnerabilities

// Additive enrichment: existing asset unchanged, new water semantics layered on top
```

**Verification:**
```cypher
// Verify existing asset properties unchanged
MATCH (asset:Asset {assetId: 'ASSET-PUMP-WTP-001'})
RETURN properties(asset)
// Should return exact same properties as before Wave 2
```

---

#### Example 2: SCADA System Adding Context to Existing Network Data

**Before Wave 2:**
```cypher
// Generic network node from existing graph
(network:NetworkSegment {
    segmentId: 'NET-SCADA-WTP',
    ipRange: '192.168.10.0/24',
    vlan: 10
})
```

**After Wave 2:**
```cypher
// Network segment unchanged, new SCADA context added
(ss:SCADASystem {
    scadaId: 'water:scada:wtp-master-001',
    systemName: 'Water Treatment Plant Master SCADA',
    vendor: 'Schneider Electric',
    networkArchitecture: 'Segmented'
})

// Link SCADA to existing network
MATCH (network:NetworkSegment {segmentId: 'NET-SCADA-WTP'})
MATCH (ss:SCADASystem {scadaId: 'water:scada:wtp-master-001'})
CREATE (ss)-[:DEPLOYED_ON_NETWORK {
    deploymentDate: datetime('2023-01-15T00:00:00Z'),
    isolationLevel: 'VLAN-Segmented'
}]->(network)

// Now supports integrated network + SCADA security queries
MATCH (network:NetworkSegment)--(ss:SCADASystem)
MATCH (ss)-[:CONTROLLED_BY_SCADA]-(wd:WaterDevice)
MATCH (wd)-[:VULNERABLE_TO]->(cve:CVE)
WHERE cve.accessVector = 'Network'
RETURN network.segmentId,
       ss.systemName,
       count(DISTINCT wd) as devicesOnNetwork,
       count(DISTINCT cve) as networkExploitableCVEs,
       ss.networkArchitecture,
       CASE
         WHEN ss.networkArchitecture = 'Flat' AND count(cve) > 0 THEN 'Critical'
         WHEN ss.networkArchitecture = 'Segmented' AND count(cve) > 5 THEN 'High'
         ELSE 'Medium'
       END as networkRisk

// Additive: existing network data preserved, new SCADA security context added
```

---

### 4.4 CVE Preservation Verification

#### Verification Query 1: CVE Node Count Unchanged

```cypher
// Verify CVE count identical to pre-Wave 2
MATCH (cve:CVE)
RETURN count(cve) as totalCVEs

// Expected: Same count as after Wave 1 (no CVEs added/removed)
// If baseline was 45,672 CVEs, should still be 45,672
```

#### Verification Query 2: CVE Properties Intact

```cypher
// Sample CVEs linked to water infrastructure
MATCH (cve:CVE)<-[:THREATENS_WATER_INFRASTRUCTURE]-(wd:WaterDevice)
WITH cve LIMIT 50
RETURN cve.cveId,
       cve.cvssScore,
       cve.publishedDate,
       cve.description,
       size(keys(properties(cve))) as propertyCount
ORDER BY cve.cveId

// Verify property counts match pre-Wave 2 baseline for these CVEs
```

#### Verification Query 3: Original CVE Relationships Preserved

```cypher
// Verify existing CVE relationships unchanged (excluding new Wave 2 relationships)
MATCH (cve:CVE)-[r]->(target)
WHERE type(r) <> 'THREATENS_WATER_INFRASTRUCTURE'
  AND type(r) <> 'HAS_SCADA_VULNERABILITY'
WITH type(r) as relType, count(r) as relCount
RETURN relType, relCount
ORDER BY relType

// Compare to pre-Wave 2 baseline - should match exactly
```

---

## 5. Validation Criteria

### 5.1 Acceptance Tests

#### Test 1: Node Creation Completeness

```cypher
CALL {
    MATCH (wd:WaterDevice) RETURN 'WaterDevice' as nodeType, count(wd) as nodeCount
    UNION
    MATCH (wp:WaterProperty) RETURN 'WaterProperty' as nodeType, count(wp) as nodeCount
    UNION
    MATCH (tp:TreatmentProcess) RETURN 'TreatmentProcess' as nodeType, count(tp) as nodeCount
    UNION
    MATCH (dz:DistributionZone) RETURN 'DistributionZone' as nodeType, count(dz) as nodeCount
    UNION
    MATCH (ss:SCADASystem) RETURN 'SCADASystem' as nodeType, count(ss) as nodeCount
    UNION
    MATCH (wqs:WaterQualityStandard) RETURN 'WaterQualityStandard' as nodeType, count(wqs) as nodeCount
    UNION
    MATCH (wi:WaterIncident) RETURN 'WaterIncident' as nodeType, count(wi) as nodeCount
}
RETURN nodeType, nodeCount
ORDER BY nodeType
```

**Acceptance Criteria:**
- WaterDevice: 1,500-2,000 nodes
- WaterProperty: 4,000-6,000 nodes
- TreatmentProcess: 500-800 nodes
- DistributionZone: 100-200 nodes
- SCADASystem: 20-40 nodes
- WaterQualityStandard: 50-100 nodes
- WaterIncident: 100-200 nodes (historical)

**Total Target:** 6,270-9,340 core nodes (plus measurements bringing to 12,000-18,000 total)

---

#### Test 2: Relationship Integrity

```cypher
CALL {
    MATCH ()-[r:PART_OF_PROCESS]->() RETURN 'PART_OF_PROCESS' as relType, count(r) as relCount
    UNION
    MATCH ()-[r:LOCATED_IN_ZONE]->() RETURN 'LOCATED_IN_ZONE' as relType, count(r) as relCount
    UNION
    MATCH ()-[r:CONTROLLED_BY_SCADA]->() RETURN 'CONTROLLED_BY_SCADA' as relType, count(r) as relCount
    UNION
    MATCH ()-[r:COMPLIES_WITH_STANDARD]->() RETURN 'COMPLIES_WITH_STANDARD' as relType, count(r) as relCount
    UNION
    MATCH ()-[r:INVOLVED_IN_INCIDENT]->() RETURN 'INVOLVED_IN_INCIDENT' as relType, count(r) as relCount
    UNION
    MATCH ()-[r:MONITORS_PROCESS]->() RETURN 'MONITORS_PROCESS' as relType, count(r) as relCount
    UNION
    MATCH ()-[r:HAS_WATER_PROPERTY]->() RETURN 'HAS_WATER_PROPERTY' as relType, count(r) as relCount
    UNION
    MATCH ()-[r:THREATENS_WATER_INFRASTRUCTURE]->() RETURN 'THREATENS_WATER_INFRASTRUCTURE' as relType, count(r) as relCount
}
RETURN relType, relCount
ORDER BY relType
```

**Acceptance Criteria:**
- PART_OF_PROCESS: 3,000-5,000
- LOCATED_IN_ZONE: 1,500-2,000
- CONTROLLED_BY_SCADA: 1,500-2,000
- COMPLIES_WITH_STANDARD: 4,000-6,000
- INVOLVED_IN_INCIDENT: 200-400
- MONITORS_PROCESS: 100-200
- HAS_WATER_PROPERTY: 6,000-9,000
- THREATENS_WATER_INFRASTRUCTURE: 1,200-1,800

**Total Target:** 17,500-26,400 new relationships

---

#### Test 3: Integration with Wave 1 Validation

```cypher
// Verify water devices inherit SAREF properties
MATCH (wd:WaterDevice)
WHERE wd:Device  // Must also be labeled as SAREF:Device
WITH count(wd) as waterDevicesWithSAREF

MATCH (wd:WaterDevice)
WITH waterDevicesWithSAREF, count(wd) as totalWaterDevices

RETURN waterDevicesWithSAREF,
       totalWaterDevices,
       CASE
         WHEN waterDevicesWithSAREF = totalWaterDevices THEN 'PASS'
         ELSE 'FAIL'
       END as inheritanceTest

// Expected: PASS (all water devices must inherit from SAREF:Device)


// Verify water properties extend SAREF measurement framework
MATCH (wp:WaterProperty)-[:GENERATES_MEASUREMENT]->(m:Measurement)
WITH count(DISTINCT wp) as waterPropertiesGeneratingMeasurements

MATCH (wp:WaterProperty)
WHERE wp:Property  // Must also be labeled as SAREF:Property
WITH waterPropertiesGeneratingMeasurements, count(wp) as totalWaterProperties

RETURN waterPropertiesGeneratingMeasurements,
       totalWaterProperties,
       round((toFloat(waterPropertiesGeneratingMeasurements) / totalWaterProperties) * 100) as percentageWithMeasurements

// Expected: > 80% of water properties generating measurements
```

---

#### Test 4: Water Safety Validation

```cypher
// Verify all critical water devices have quality impact assessments
MATCH (wd:WaterDevice)
WHERE wd.criticality IN ['Critical', 'High']
  AND (wd.waterQualityImpact IS NULL OR wd.cyberPhysicalRisk IS NULL)
RETURN count(wd) as criticalDevicesWithoutAssessment

// Acceptance: 0 critical devices without water quality/cyber-physical risk assessment


// Verify all water properties have regulatory compliance links
MATCH (wp:WaterProperty)
WHERE wp.waterPropertyCategory = 'Chemical'
OPTIONAL MATCH (wp)-[:COMPLIES_WITH_STANDARD]->(wqs:WaterQualityStandard)
WITH wp, wqs
WHERE wqs IS NULL
RETURN count(wp) as chemicalPropertiesWithoutStandards

// Acceptance: 0 chemical properties without regulatory standard links
```

---

### 5.2 Performance Benchmarks

#### Benchmark 1: Critical Infrastructure Query Performance

```cypher
// Query 1: Find all vulnerable water devices serving >10K population (≤ 800ms)
PROFILE
MATCH (wd:WaterDevice)-[:LOCATED_IN_ZONE]->(dz:DistributionZone)
WHERE dz.population > 10000
MATCH (wd)-[t:THREATENS_WATER_INFRASTRUCTURE]->(cve:CVE)
WHERE cve.cvssScore >= 7.0
  AND t.mitigationStatus = 'Unpatched'
RETURN wd.deviceId,
       wd.waterDeviceType,
       dz.zoneName,
       t.populationAtRisk,
       cve.cveId,
       cve.cvssScore,
       t.waterSafetyImpact
ORDER BY t.populationAtRisk DESC, cve.cvssScore DESC
LIMIT 20

// Performance target: ≤ 800ms


// Query 2: SCADA security audit across all systems (≤ 1200ms)
PROFILE
MATCH (ss:SCADASystem)
OPTIONAL MATCH (ss)-[:HAS_SCADA_VULNERABILITY]->(cve:CVE)
WHERE cve.cvssScore >= 9.0
OPTIONAL MATCH (ss)-[:CONTROLLED_BY_SCADA]-(wd:WaterDevice)
WHERE wd.cyberPhysicalRisk = 'Critical'
RETURN ss.systemName,
       ss.vendor,
       ss.networkArchitecture,
       ss.remoteAccessEnabled,
       ss.authenticationMethod,
       count(DISTINCT cve) as criticalVulnerabilities,
       count(DISTINCT wd) as criticalDevicesControlled,
       CASE
         WHEN ss.remoteAccessEnabled = true AND count(cve) > 0 THEN 'ImmediateThreat'
         WHEN ss.networkArchitecture = 'Flat' AND count(cve) > 0 THEN 'HighRisk'
         ELSE 'Monitor'
       END as threatLevel
ORDER BY threatLevel, criticalVulnerabilities DESC

// Performance target: ≤ 1200ms
```

**Acceptance Criteria:**
- All benchmark queries complete within target time
- Query performance degradation ≤ 15% compared to Wave 1
- Index hit rate > 90% for water-specific queries

---

### 5.3 Data Integrity Checks

#### Integrity Check 1: Referential Integrity

```cypher
// Check for water devices without zone assignment
MATCH (wd:WaterDevice)
WHERE NOT EXISTS((wd)-[:LOCATED_IN_ZONE]->(:DistributionZone))
RETURN count(wd) as devicesWithoutZone

// Acceptance: ≤ 5% of devices (some may be in transit/storage)


// Check for treatment processes without monitoring SCADA
MATCH (tp:TreatmentProcess)
WHERE tp.scadaControlled = true
  AND NOT EXISTS((:SCADASystem)-[:MONITORS_PROCESS]->(tp))
RETURN count(tp) as scadaProcessesWithoutMonitoring

// Acceptance: 0 SCADA-controlled processes without monitoring links
```

---

### 5.4 Rollback Verification

```cypher
// Phase 1: Delete Wave 2 relationships
MATCH ()-[r:PART_OF_PROCESS]->() DELETE r;
MATCH ()-[r:LOCATED_IN_ZONE]->() DELETE r;
MATCH ()-[r:CONTROLLED_BY_SCADA]->() DELETE r;
MATCH ()-[r:COMPLIES_WITH_STANDARD]->() DELETE r;
MATCH ()-[r:INVOLVED_IN_INCIDENT]->() DELETE r;
MATCH ()-[r:MONITORS_PROCESS]->() DELETE r;
MATCH ()-[r:HAS_WATER_PROPERTY]->() DELETE r;
MATCH ()-[r:THREATENS_WATER_INFRASTRUCTURE]->() DELETE r;

// Phase 2: Delete Wave 2 nodes
MATCH (wd:WaterDevice) DETACH DELETE wd;
MATCH (wp:WaterProperty) DETACH DELETE wp;
MATCH (tp:TreatmentProcess) DELETE tp;
MATCH (dz:DistributionZone) DELETE dz;
MATCH (ss:SCADASystem) DELETE ss;
MATCH (wqs:WaterQualityStandard) DELETE wqs;
MATCH (wi:WaterIncident) DELETE wi;

// Phase 3: Verify Wave 1 SAREF nodes intact
MATCH (d:Device) WHERE NOT d:WaterDevice
RETURN count(d) as sarefDevicesRemaining

// Expected: Same count as end of Wave 1

// Phase 4: Verify CVE data intact
MATCH (cve:CVE)
RETURN count(cve) as cveCount

// Expected: Same count as before Wave 2 (45,672 or baseline)
```

**Acceptance Criteria:**
- 100% of Wave 2 additions removed
- 100% of Wave 1 and pre-existing data preserved
- Rollback completes in ≤ 15 minutes

---

## 6. Example Queries

### 6.1 Water Safety Queries

#### Query 1: Population at Risk from Unpatched Vulnerabilities

```cypher
MATCH (wd:WaterDevice)-[:LOCATED_IN_ZONE]->(dz:DistributionZone)
MATCH (wd)-[t:THREATENS_WATER_INFRASTRUCTURE]->(cve:CVE)
WHERE t.mitigationStatus = 'Unpatched'
  AND cve.cvssScore >= 7.0
  AND t.waterSafetyImpact IN ['DirectContamination', 'ProcessDisruption']
WITH dz.zoneName as zone,
     sum(DISTINCT dz.population) as totalPopulation,
     count(DISTINCT wd) as vulnerableDevices,
     count(DISTINCT cve) as uniqueVulnerabilities,
     collect(DISTINCT cve.cveId)[..5] as topCVEs
RETURN zone,
       totalPopulation,
       vulnerableDevices,
       uniqueVulnerabilities,
       topCVEs
ORDER BY totalPopulation DESC
LIMIT 10
```

**Expected Results:** Top 10 zones with population-weighted vulnerability exposure

**Performance:** ≤ 900ms

---

#### Query 2: Regulatory Compliance Dashboard

```cypher
MATCH (wp:WaterProperty)-[c:COMPLIES_WITH_STANDARD]->(wqs:WaterQualityStandard)
WHERE wqs.regulatoryBody IN ['EPA', 'WHO']
WITH wqs.parameterName as parameter,
     wqs.regulatoryBody as regulator,
     count(wp) as monitoringPoints,
     sum(CASE WHEN c.complianceStatus = 'Compliant' THEN 1 ELSE 0 END) as compliantCount,
     sum(CASE WHEN c.complianceStatus = 'NonCompliant' THEN 1 ELSE 0 END) as nonCompliantCount
RETURN parameter,
       regulator,
       monitoringPoints,
       compliantCount,
       nonCompliantCount,
       round((toFloat(compliantCount) / monitoringPoints) * 100) as compliancePercentage
ORDER BY compliancePercentage ASC, nonCompliantCount DESC
```

**Expected Results:** Compliance status by parameter

**Performance:** ≤ 600ms

---

### 6.2 SCADA Security Queries

#### Query 3: SCADA Attack Surface Analysis

```cypher
MATCH (ss:SCADASystem)
OPTIONAL MATCH (ss)-[:CONTROLLED_BY_SCADA]-(wd:WaterDevice)
WHERE wd.cyberPhysicalRisk IN ['Critical', 'High']
OPTIONAL MATCH (ss)-[:HAS_SCADA_VULNERABILITY]->(cve:CVE)
WHERE cve.accessVector = 'Network'
WITH ss,
     count(DISTINCT wd) as criticalDevices,
     count(DISTINCT cve) as networkVulnerabilities,
     CASE
       WHEN ss.remoteAccessEnabled = true AND ss.authenticationMethod = 'Local' THEN 10
       WHEN ss.remoteAccessEnabled = true AND ss.authenticationMethod = 'LDAP' THEN 7
       WHEN ss.remoteAccessEnabled = false THEN 3
       ELSE 5
     END as authScore,
     CASE ss.networkArchitecture
       WHEN 'Flat' THEN 10
       WHEN 'Segmented' THEN 5
       WHEN 'DMZ-Protected' THEN 2
       ELSE 7
     END as networkScore
RETURN ss.systemName,
       ss.vendor,
       ss.networkArchitecture,
       ss.remoteAccessEnabled,
       ss.authenticationMethod,
       criticalDevices,
       networkVulnerabilities,
       (authScore + networkScore + (networkVulnerabilities * 2)) as attackSurfaceScore
ORDER BY attackSurfaceScore DESC
LIMIT 10
```

**Expected Results:** SCADA systems ranked by attack surface

**Performance:** ≤ 1000ms

---

## 7. Implementation Roadmap

### Week 1-2: Water Device & Property Schema
- Create WaterDevice and WaterProperty nodes
- Establish inheritance from SAREF core
- Implement water-specific indexes

### Week 3-4: Treatment Process & SCADA Integration
- Create TreatmentProcess and SCADASystem nodes
- Build process-device-SCADA relationships
- Integrate with existing network topology

### Week 5-6: Regulatory & Distribution Zones
- Create WaterQualityStandard and DistributionZone nodes
- Link properties to regulatory compliance
- Map devices to geographic zones

### Week 7: CVE Integration & Testing
- Link water devices to existing CVEs
- Create THREATENS_WATER_INFRASTRUCTURE relationships
- Execute all acceptance tests

### Week 8-9: Validation & Deployment
- Performance benchmarking
- Data integrity validation
- Production deployment
- Documentation finalization

---

## 8. Dependencies for Wave 3

Wave 3 (Energy Grid) will reference Wave 2 patterns:

1. **SCADA Architecture**: Energy SCADA systems use similar models
2. **Critical Infrastructure**: Water-energy nexus relationships
3. **Regulatory Compliance**: Similar compliance framework patterns
4. **Cyber-Physical Risk**: Shared risk assessment methodologies

**Critical Handoff:** Wave 2 SCADA security patterns serve as template for Wave 3 energy SCADA systems.

---

**Wave 2 Status:** SPECIFICATION COMPLETE
**Next Wave:** Wave 3 - Energy Grid Integration
**Integration Status:** Additive enhancement extending Wave 1, preserving all existing data
**Rollback Safety:** Complete rollback script provided

