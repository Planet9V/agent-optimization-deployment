# Integration Patterns
**File:** 16_INTEGRATION_PATTERNS.md
**Created:** 2025-10-30 00:00:00 UTC
**Modified:** 2025-10-30 00:00:00 UTC
**Version:** v1.0.0
**Author:** AEON FORGE Implementation Team
**Purpose:** Complete integration patterns for cross-domain entity linking with Cypher implementations
**Status:** ACTIVE

## Executive Summary

This document provides comprehensive integration patterns for linking CVE, ThreatActor, ATT&CK, SAREF, ICS, UCO, and SBOM entities within the AEON Digital Twin Cybersecurity Threat Intelligence schema. Each pattern includes complete Cypher query examples, relationship semantics, property mappings, and validation queries.

### Integration Architecture

The AEON schema enhancement creates a **multi-layer knowledge graph** with cross-domain integration:

1. **Vulnerability Layer**: CVE nodes enhanced with SAREF, ICS, SBOM, and UCO context
2. **Threat Intelligence Layer**: ThreatActor nodes enhanced with psychometrics, STIX, and ICS targeting
3. **Attack Pattern Layer**: ATT&CK techniques linked to CVEs, ICS components, and UCO observables
4. **Asset Layer**: SAREF devices, ICS components, and SBOM packages linked to vulnerabilities
5. **Forensics Layer**: UCO observables linked to CVEs, threat actors, and attack patterns

## 1. CVE Enhancement Patterns

### 1.1 CVE → SAREF Device Integration

**Pattern:** Link CVE vulnerabilities to SAREF IoT device types and functions they affect.

**Complete Cypher Implementation:**

```cypher
// ===============================================
// CVE → SAREF Device Integration Pattern
// ===============================================

// Step 1: Create SAREF Device Categories if not exist
MERGE (sensor:SAREFDevice {
  id: 'saref:Sensor',
  name: 'Sensor Device',
  device_category: 'sensor',
  description: 'Device that measures physical properties'
})

MERGE (actuator:SAREFDevice {
  id: 'saref:Actuator',
  name: 'Actuator Device',
  device_category: 'actuator',
  description: 'Device that performs physical actions'
})

MERGE (appliance:SAREFDevice {
  id: 'saref:Appliance',
  name: 'Smart Appliance',
  device_category: 'appliance',
  description: 'Household or industrial appliance with smart capabilities'
})

MERGE (meter:SAREFDevice {
  id: 'saref:Meter',
  name: 'Metering Device',
  device_category: 'meter',
  description: 'Device that measures consumption or usage'
});

// Step 2: Link CVEs to SAREF Devices based on description patterns
// Example: Sensor vulnerabilities
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(sensor|temperature|humidity|pressure|motion|proximity).*'
  OR c.description =~ '(?i).*(IoT|internet of things).*sensor.*'
  OR c.vulnerability_type IN ['sensor_spoofing', 'measurement_tampering']
WITH c
MATCH (saref:SAREFDevice {device_category: 'sensor'})
MERGE (c)-[r:AFFECTS_SAREF_DEVICE]->(saref)
SET
  r.device_category = 'sensor',
  r.vulnerability_context = CASE
    WHEN c.description =~ '(?i).*firmware.*' THEN 'firmware'
    WHEN c.description =~ '(?i).*protocol.*' THEN 'protocol'
    WHEN c.description =~ '(?i).*authentication.*' THEN 'authentication'
    ELSE 'configuration'
  END,
  r.exposure_level = CASE
    WHEN c.cvss_score >= 9.0 THEN 'direct'
    WHEN c.cvss_score >= 7.0 THEN 'indirect'
    ELSE 'transitive'
  END,
  r.remediation_priority = CASE
    WHEN c.severity = 'CRITICAL' AND c.cvss_score >= 9.0 THEN 'critical'
    WHEN c.severity IN ['CRITICAL', 'HIGH'] THEN 'high'
    WHEN c.severity = 'MEDIUM' THEN 'medium'
    ELSE 'low'
  END,
  r.created_at = datetime(),
  r.confidence_score = 0.85;

// Example: Actuator vulnerabilities
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(actuator|motor|valve|switch|relay|controller).*'
  OR c.description =~ '(?i).*(industrial control|SCADA).*actuator.*'
WITH c
MATCH (saref:SAREFDevice {device_category: 'actuator'})
MERGE (c)-[r:AFFECTS_SAREF_DEVICE]->(saref)
SET
  r.device_category = 'actuator',
  r.vulnerability_context = CASE
    WHEN c.description =~ '(?i).*command injection.*' THEN 'command_injection'
    WHEN c.description =~ '(?i).*unauthorized control.*' THEN 'access_control'
    ELSE 'configuration'
  END,
  r.exposure_level = 'direct',  // Actuator vulnerabilities typically direct
  r.remediation_priority = CASE
    WHEN c.cvss_score >= 9.0 THEN 'critical'
    WHEN c.cvss_score >= 7.0 THEN 'high'
    ELSE 'medium'
  END,
  r.created_at = datetime(),
  r.confidence_score = 0.90;

// Example: Smart Appliance vulnerabilities
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(smart home|appliance|thermostat|refrigerator|washing machine|oven).*'
  OR c.description =~ '(?i).*(HomeKit|Google Home|Alexa|smart speaker).*'
WITH c
MATCH (saref:SAREFDevice {device_category: 'appliance'})
MERGE (c)-[r:AFFECTS_SAREF_DEVICE]->(saref)
SET
  r.device_category = 'appliance',
  r.vulnerability_context = 'consumer_iot',
  r.exposure_level = CASE
    WHEN c.description =~ '(?i).*remote.*' THEN 'direct'
    ELSE 'indirect'
  END,
  r.remediation_priority = CASE
    WHEN c.cvss_score >= 8.0 THEN 'high'
    ELSE 'medium'
  END,
  r.created_at = datetime(),
  r.confidence_score = 0.80;

// Step 3: Add SAREF-specific properties to CVE nodes
MATCH (c:CVE)-[r:AFFECTS_SAREF_DEVICE]->()
WITH c, collect(DISTINCT r.device_category) AS device_types
SET
  c.saref_device_types = device_types,
  c.iot_exploitation_vector = CASE
    WHEN 'sensor' IN device_types THEN 'measurement_spoofing'
    WHEN 'actuator' IN device_types THEN 'unauthorized_control'
    WHEN 'appliance' IN device_types THEN 'remote_access'
    ELSE 'general_iot'
  END;

// Step 4: Validation query
MATCH (c:CVE)-[r:AFFECTS_SAREF_DEVICE]->(saref:SAREFDevice)
RETURN
  saref.device_category AS device_category,
  count(c) AS affected_cves,
  avg(c.cvss_score) AS avg_cvss,
  collect(DISTINCT r.vulnerability_context)[0..5] AS sample_contexts
ORDER BY affected_cves DESC;
```

### 1.2 CVE → SAREF Function Integration

**Pattern:** Link CVE vulnerabilities to specific SAREF function types (sensing, actuating, metering).

**Complete Cypher Implementation:**

```cypher
// ===============================================
// CVE → SAREF Function Integration Pattern
// ===============================================

// Step 1: Create SAREF Function nodes
MERGE (sensing:SAREFFunction {
  id: 'saref:SensingFunction',
  name: 'Sensing Function',
  function_category: 'sensing',
  description: 'Function for measuring physical properties'
})

MERGE (actuating:SAREFFunction {
  id: 'saref:ActuatingFunction',
  name: 'Actuating Function',
  function_category: 'actuating',
  description: 'Function for performing physical actions'
})

MERGE (metering:SAREFFunction {
  id: 'saref:MeteringFunction',
  name: 'Metering Function',
  function_category: 'metering',
  description: 'Function for measuring consumption or usage'
});

// Step 2: Link CVEs to SAREF Functions with impact assessment
// Sensing Function vulnerabilities
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(sensor|sensing|measurement|detection|monitoring).*'
  AND (c.description =~ '(?i).*(tamper|spoof|manipulate|falsify|corrupt).*'
       OR c.vulnerability_type IN ['measurement_tampering', 'sensor_spoofing'])
WITH c
MATCH (func:SAREFFunction {function_category: 'sensing'})
MERGE (c)-[r:IMPACTS_SAREF_FUNCTION]->(func)
SET
  r.function_category = 'sensing',
  r.impact_severity = CASE
    WHEN c.description =~ '(?i).*complete.*loss.*' THEN 'complete_loss'
    WHEN c.description =~ '(?i).*(degrade|intermittent).*' THEN 'degradation'
    ELSE 'intermittent'
  END,
  r.affected_properties = CASE
    WHEN c.description =~ '(?i).*temperature.*' THEN ['saref:Temperature']
    WHEN c.description =~ '(?i).*humidity.*' THEN ['saref:Humidity']
    WHEN c.description =~ '(?i).*pressure.*' THEN ['saref:Pressure']
    WHEN c.description =~ '(?i).*motion.*' THEN ['saref:Motion']
    ELSE ['saref:Measurement']
  END,
  r.detection_difficulty = CASE
    WHEN c.cvss_score >= 9.0 THEN 'trivial'
    WHEN c.cvss_score >= 7.0 THEN 'moderate'
    ELSE 'sophisticated'
  END,
  r.created_at = datetime();

// Actuating Function vulnerabilities
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(actuate|actuator|control|command|execute|operate).*'
  AND (c.description =~ '(?i).*(unauthorized|injection|bypass|escalation).*'
       OR c.vulnerability_type IN ['command_injection', 'access_control_bypass'])
WITH c
MATCH (func:SAREFFunction {function_category: 'actuating'})
MERGE (c)-[r:IMPACTS_SAREF_FUNCTION]->(func)
SET
  r.function_category = 'actuating',
  r.impact_severity = CASE
    WHEN c.severity = 'CRITICAL' THEN 'complete_loss'
    WHEN c.severity = 'HIGH' THEN 'degradation'
    ELSE 'intermittent'
  END,
  r.affected_properties = ['saref:OnOffState', 'saref:OpenCloseState'],
  r.safety_concern = c.cvss_score >= 8.0,
  r.created_at = datetime();

// Metering Function vulnerabilities
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(meter|metering|consumption|usage|billing|energy).*'
  AND (c.description =~ '(?i).*(tamper|manipulate|fraud|bypass).*'
       OR c.vulnerability_type IN ['metering_fraud', 'consumption_tampering'])
WITH c
MATCH (func:SAREFFunction {function_category: 'metering'})
MERGE (c)-[r:IMPACTS_SAREF_FUNCTION]->(func)
SET
  r.function_category = 'metering',
  r.impact_severity = 'complete_loss',  // Metering fraud is always severe
  r.affected_properties = ['saref:Power', 'saref:Energy', 'saref:Consumption'],
  r.financial_impact = true,
  r.created_at = datetime();

// Step 3: Add function impact properties to CVE nodes
MATCH (c:CVE)-[r:IMPACTS_SAREF_FUNCTION]->()
WITH c, collect(DISTINCT r.function_category) AS function_impacts
SET c.saref_function_impact = function_impacts;

// Step 4: Create SAREF Measurement corruption relationships
MATCH (c:CVE)-[:IMPACTS_SAREF_FUNCTION]->(func:SAREFFunction {function_category: 'sensing'})
MERGE (measurement:SAREFMeasurement {
  id: 'saref:Measurement',
  name: 'Generic Measurement',
  measurement_type: 'generic'
})
MERGE (c)-[r:CORRUPTS_MEASUREMENT]->(measurement)
SET
  r.manipulation_type = CASE
    WHEN c.description =~ '(?i).*spoof.*' THEN 'spoofing'
    WHEN c.description =~ '(?i).*tamper.*' THEN 'tampering'
    WHEN c.description =~ '(?i).*replay.*' THEN 'replay'
    ELSE 'injection'
  END,
  r.detection_difficulty = CASE
    WHEN c.cvss_score < 5.0 THEN 'sophisticated'
    WHEN c.cvss_score < 7.0 THEN 'moderate'
    ELSE 'trivial'
  END,
  r.created_at = datetime();

// Step 5: Validation query
MATCH (c:CVE)-[r:IMPACTS_SAREF_FUNCTION]->(func:SAREFFunction)
RETURN
  func.function_category AS function,
  count(c) AS affected_cves,
  collect(DISTINCT r.impact_severity) AS impact_levels,
  avg(c.cvss_score) AS avg_cvss
ORDER BY affected_cves DESC;
```

### 1.3 CVE → ICS Component Integration

**Pattern:** Link CVE vulnerabilities to ICS/OT component types (PLC, HMI, SCADA, DCS, RTU) with Purdue Model levels.

**Complete Cypher Implementation:**

```cypher
// ===============================================
// CVE → ICS Component Integration Pattern
// ===============================================

// Step 1: Create ICS Component Type nodes
MERGE (plc:ICSComponent {
  id: 'ics:PLC',
  name: 'Programmable Logic Controller',
  component_type: 'PLC',
  purdue_level: 1,  // Field Controller
  description: 'Industrial automation controller'
})

MERGE (hmi:ICSComponent {
  id: 'ics:HMI',
  name: 'Human-Machine Interface',
  component_type: 'HMI',
  purdue_level: 2,  // Supervisory Control
  description: 'Operator interface for industrial processes'
})

MERGE (scada:ICSComponent {
  id: 'ics:SCADA',
  name: 'SCADA System',
  component_type: 'SCADA',
  purdue_level: 3,  // Site Operations
  description: 'Supervisory Control and Data Acquisition system'
})

MERGE (dcs:ICSComponent {
  id: 'ics:DCS',
  name: 'Distributed Control System',
  component_type: 'DCS',
  purdue_level: 2,  // Supervisory Control
  description: 'Distributed process control system'
})

MERGE (rtu:ICSComponent {
  id: 'ics:RTU',
  name: 'Remote Terminal Unit',
  component_type: 'RTU',
  purdue_level: 1,  // Field Controller
  description: 'Remote data acquisition and control unit'
});

// Step 2: Link CVEs to ICS Components with criticality assessment
// PLC vulnerabilities
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(PLC|programmable logic controller|ladder logic|control logic).*'
  OR EXISTS(c.cwe_id) AND c.cwe_id IN ['CWE-94', 'CWE-502', 'CWE-306']  // Code injection, deserialization, authentication
WITH c
MATCH (ics:ICSComponent {component_type: 'PLC'})
MERGE (c)-[r:AFFECTS_ICS_COMPONENT]->(ics)
SET
  r.component_type = 'PLC',
  r.criticality_level = CASE
    WHEN c.description =~ '(?i).*(safety|emergency shutdown|ESD|SIS).*' THEN 'safety_critical'
    WHEN c.cvss_score >= 9.0 THEN 'production_critical'
    ELSE 'monitoring'
  END,
  r.ics_impact = CASE
    WHEN c.description =~ '(?i).*(shutdown|halt|stop production).*' THEN 'process_disruption'
    WHEN c.description =~ '(?i).*(safety|hazard|dangerous).*' THEN 'safety_hazard'
    ELSE 'data_corruption'
  END,
  r.purdue_level = [1],  // PLCs at Level 1
  r.exploit_complexity = CASE
    WHEN c.cvss_vector =~ '.*AV:N.*' THEN 'network_accessible'  // Network attack vector
    WHEN c.cvss_vector =~ '.*AV:A.*' THEN 'adjacent_network'
    ELSE 'local_access'
  END,
  r.created_at = datetime(),
  r.confidence_score = 0.95;

// HMI vulnerabilities
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(HMI|human machine interface|operator interface|SCADA client).*'
  OR c.description =~ '(?i).*(Wonderware|Ignition|FactoryTalk|WinCC).*'  // Common HMI platforms
WITH c
MATCH (ics:ICSComponent {component_type: 'HMI'})
MERGE (c)-[r:AFFECTS_ICS_COMPONENT]->(ics)
SET
  r.component_type = 'HMI',
  r.criticality_level = CASE
    WHEN c.cvss_score >= 9.0 THEN 'production_critical'
    ELSE 'monitoring'
  END,
  r.ics_impact = CASE
    WHEN c.description =~ '(?i).*(unauthorized control|command injection).*' THEN 'process_disruption'
    WHEN c.description =~ '(?i).*(display|visualization|data integrity).*' THEN 'data_corruption'
    ELSE 'monitoring'
  END,
  r.purdue_level = [2],  // HMIs at Level 2
  r.created_at = datetime(),
  r.confidence_score = 0.90;

// SCADA vulnerabilities
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(SCADA|supervisory control|data acquisition).*'
  OR c.description =~ '(?i).*(OSIsoft|PI System|ClearSCADA).*'
WITH c
MATCH (ics:ICSComponent {component_type: 'SCADA'})
MERGE (c)-[r:AFFECTS_ICS_COMPONENT]->(ics)
SET
  r.component_type = 'SCADA',
  r.criticality_level = 'production_critical',  // SCADA always critical
  r.ics_impact = 'process_disruption',
  r.purdue_level = [2, 3],  // SCADA spans Levels 2-3
  r.created_at = datetime(),
  r.confidence_score = 0.95;

// DCS vulnerabilities
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(DCS|distributed control system|process control).*'
  OR c.description =~ '(?i).*(Honeywell|Emerson DeltaV|ABB).*'
WITH c
MATCH (ics:ICSComponent {component_type: 'DCS'})
MERGE (c)-[r:AFFECTS_ICS_COMPONENT]->(ics)
SET
  r.component_type = 'DCS',
  r.criticality_level = 'production_critical',
  r.ics_impact = CASE
    WHEN c.description =~ '(?i).*safety.*' THEN 'safety_hazard'
    ELSE 'process_disruption'
  END,
  r.purdue_level = [1, 2],  // DCS spans Levels 1-2
  r.created_at = datetime(),
  r.confidence_score = 0.90;

// RTU vulnerabilities
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(RTU|remote terminal unit|field device).*'
  OR c.description =~ '(?i).*(Modbus RTU|DNP3 outstation).*'
WITH c
MATCH (ics:ICSComponent {component_type: 'RTU'})
MERGE (c)-[r:AFFECTS_ICS_COMPONENT]->(ics)
SET
  r.component_type = 'RTU',
  r.criticality_level = CASE
    WHEN c.cvss_score >= 9.0 THEN 'production_critical'
    ELSE 'monitoring'
  END,
  r.ics_impact = 'data_corruption',
  r.purdue_level = [0, 1],  // RTUs at Levels 0-1 (field level)
  r.created_at = datetime(),
  r.confidence_score = 0.85;

// Step 3: Add ICS-specific properties to CVE nodes
MATCH (c:CVE)-[r:AFFECTS_ICS_COMPONENT]->()
WITH c,
  collect(DISTINCT r.component_type) AS component_types,
  collect(DISTINCT r.criticality_level) AS criticality_levels,
  apoc.coll.flatten(collect(r.purdue_level)) AS purdue_levels
SET
  c.ics_applicable = true,
  c.ics_component_types = component_types,
  c.purdue_levels = apoc.coll.toSet(purdue_levels),
  c.safety_impact = CASE
    WHEN ANY(level IN criticality_levels WHERE level = 'safety_critical') THEN 'CRITICAL'
    WHEN ANY(level IN criticality_levels WHERE level = 'production_critical') THEN 'HIGH'
    ELSE 'LOW'
  END,
  c.process_impact = CASE
    WHEN 'PLC' IN component_types OR 'DCS' IN component_types THEN 'direct_control'
    WHEN 'SCADA' IN component_types OR 'HMI' IN component_types THEN 'supervisory'
    ELSE 'monitoring'
  END;

// Step 4: Validation query
MATCH (c:CVE)-[r:AFFECTS_ICS_COMPONENT]->(ics:ICSComponent)
RETURN
  ics.component_type AS component,
  count(c) AS affected_cves,
  collect(DISTINCT r.criticality_level) AS criticality_levels,
  apoc.coll.flatten(collect(r.purdue_level)) AS purdue_levels,
  avg(c.cvss_score) AS avg_cvss
ORDER BY affected_cves DESC;
```

### 1.4 CVE → Industrial Protocol Integration

**Pattern:** Link CVE vulnerabilities to industrial communication protocols.

**Complete Cypher Implementation:**

```cypher
// ===============================================
// CVE → Industrial Protocol Integration Pattern
// ===============================================

// Step 1: Create Industrial Protocol nodes
MERGE (modbus:IndustrialProtocol {
  id: 'protocol:Modbus',
  name: 'Modbus',
  protocol_name: 'Modbus',
  protocol_type: 'fieldbus',
  osi_layer: 'application',
  common_ports: [502],
  description: 'Legacy industrial communication protocol'
})

MERGE (dnp3:IndustrialProtocol {
  id: 'protocol:DNP3',
  name: 'DNP3',
  protocol_name: 'DNP3',
  protocol_type: 'SCADA',
  osi_layer: 'application',
  common_ports: [20000],
  description: 'Distributed Network Protocol for SCADA'
})

MERGE (opcua:IndustrialProtocol {
  id: 'protocol:OPC-UA',
  name: 'OPC Unified Architecture',
  protocol_name: 'OPC-UA',
  protocol_type: 'industrial_iot',
  osi_layer: 'application',
  common_ports: [4840],
  security_features: ['encryption', 'authentication', 'authorization'],
  description: 'Modern secure industrial communication protocol'
})

MERGE (ethernetip:IndustrialProtocol {
  id: 'protocol:EtherNetIP',
  name: 'EtherNet/IP',
  protocol_name: 'EtherNet/IP',
  protocol_type: 'industrial_ethernet',
  osi_layer: 'application',
  common_ports: [44818, 2222],
  description: 'Industrial Protocol for Ethernet networks'
})

MERGE (profinet:IndustrialProtocol {
  id: 'protocol:PROFINET',
  name: 'PROFINET',
  protocol_name: 'PROFINET',
  protocol_type: 'industrial_ethernet',
  osi_layer: 'data_link',
  description: 'Siemens industrial Ethernet protocol'
})

MERGE (bacnet:IndustrialProtocol {
  id: 'protocol:BACnet',
  name: 'BACnet',
  protocol_name: 'BACnet',
  protocol_type: 'building_automation',
  osi_layer: 'application',
  common_ports: [47808],
  description: 'Building Automation and Control networks protocol'
});

// Step 2: Link CVEs to Industrial Protocols
// Modbus vulnerabilities
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(modbus|modbus tcp|modbus rtu).*'
  OR c.cwe_id IN ['CWE-306', 'CWE-319']  // Missing authentication, cleartext
WITH c
MATCH (proto:IndustrialProtocol {protocol_name: 'Modbus'})
MERGE (c)-[r:EXPLOITS_PROTOCOL]->(proto)
SET
  r.protocol_name = 'Modbus',
  r.attack_vector = CASE
    WHEN c.cvss_vector =~ '.*AV:N.*' THEN 'network'
    WHEN c.cvss_vector =~ '.*AV:A.*' THEN 'adjacent'
    ELSE 'local'
  END,
  r.exploit_complexity = CASE
    WHEN c.cvss_vector =~ '.*AC:L.*' THEN 'low'
    WHEN c.cvss_vector =~ '.*AC:H.*' THEN 'high'
    ELSE 'medium'
  END,
  r.authentication_required = false,  // Modbus lacks authentication
  r.encryption_available = false,  // Modbus lacks encryption
  r.created_at = datetime(),
  r.confidence_score = 0.95;

// DNP3 vulnerabilities
MATCH (c:CVE)
WHERE c.description =~ '(?i).*(dnp3|distributed network protocol).*'
WITH c
MATCH (proto:IndustrialProtocol {protocol_name: 'DNP3'})
MERGE (c)-[r:EXPLOITS_PROTOCOL]->(proto)
SET
  r.protocol_name = 'DNP3',
  r.attack_vector = 'network',
  r.exploit_complexity = 'medium',
  r.created_at = datetime(),
  r.confidence_score = 0.90;

// OPC-UA vulnerabilities
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(OPC UA|OPC-UA|OPC unified architecture).*'
WITH c
MATCH (proto:IndustrialProtocol {protocol_name: 'OPC-UA'})
MERGE (c)-[r:EXPLOITS_PROTOCOL]->(proto)
SET
  r.protocol_name = 'OPC-UA',
  r.attack_vector = CASE
    WHEN c.cvss_vector =~ '.*AV:N.*' THEN 'network'
    ELSE 'local'
  END,
  r.exploit_complexity = CASE
    WHEN c.description =~ '(?i).*(encryption|certificate|authentication).*' THEN 'high'
    ELSE 'medium'
  END,
  r.authentication_required = true,  // OPC-UA has authentication
  r.encryption_available = true,  // OPC-UA has encryption
  r.security_feature_bypassed = c.description =~ '(?i).*(bypass|circumvent|disable).*',
  r.created_at = datetime(),
  r.confidence_score = 0.92;

// EtherNet/IP vulnerabilities
MATCH (c:CVE)
WHERE c.description =~ '(?i).*(ethernet/ip|ethernetip|CIP).*'
WITH c
MATCH (proto:IndustrialProtocol {protocol_name: 'EtherNet/IP'})
MERGE (c)-[r:EXPLOITS_PROTOCOL]->(proto)
SET
  r.protocol_name = 'EtherNet/IP',
  r.attack_vector = 'network',
  r.exploit_complexity = 'low',
  r.created_at = datetime(),
  r.confidence_score = 0.88;

// PROFINET vulnerabilities
MATCH (c:CVE)
WHERE c.description =~ '(?i).*(profinet|profibus).*'
WITH c
MATCH (proto:IndustrialProtocol {protocol_name: 'PROFINET'})
MERGE (c)-[r:EXPLOITS_PROTOCOL]->(proto)
SET
  r.protocol_name = 'PROFINET',
  r.attack_vector = 'adjacent',  // Usually adjacent network
  r.exploit_complexity = 'medium',
  r.created_at = datetime(),
  r.confidence_score = 0.85;

// BACnet vulnerabilities
MATCH (c:CVE)
WHERE c.description =~ '(?i).*(bacnet|building automation).*'
WITH c
MATCH (proto:IndustrialProtocol {protocol_name: 'BACnet'})
MERGE (c)-[r:EXPLOITS_PROTOCOL]->(proto)
SET
  r.protocol_name = 'BACnet',
  r.attack_vector = 'network',
  r.exploit_complexity = 'low',
  r.created_at = datetime(),
  r.confidence_score = 0.87;

// Step 3: Add protocol properties to CVE nodes
MATCH (c:CVE)-[r:EXPLOITS_PROTOCOL]->()
WITH c, collect(DISTINCT r.protocol_name) AS protocols
SET c.industrial_protocols = protocols;

// Step 4: Validation query
MATCH (c:CVE)-[r:EXPLOITS_PROTOCOL]->(proto:IndustrialProtocol)
RETURN
  proto.protocol_name AS protocol,
  count(c) AS affected_cves,
  collect(DISTINCT r.attack_vector) AS attack_vectors,
  avg(c.cvss_score) AS avg_cvss
ORDER BY affected_cves DESC;
```

### 1.5 CVE → SBOM Component Integration

**Pattern:** Link CVE vulnerabilities to Software Bill of Materials (SBOM) components and packages.

**Complete Cypher Implementation:**

```cypher
// ===============================================
// CVE → SBOM Component Integration Pattern
// ===============================================

// Step 1: Create or match SBOM Component nodes from existing package data
// (Assumes SBOM components already exist or are created from CPE data)

// Example: Link CVEs to npm packages
MATCH (c:CVE)
WHERE c.description =~ '(?i).*(npm|node.js package|javascript package).*'
  OR EXISTS((c)-[:AFFECTS]->(:Product)) AND ANY(p IN [(c)-[:AFFECTS]->(prod:Product) | prod.name] WHERE p =~ '(?i).*node.*')
WITH c
// Create or match SBOM component
MERGE (sbom:SBOMComponent {
  id: 'sbom:npm:' + toLower(split(c.description, ' ')[0]),
  component_type: 'library',
  package_manager: 'npm',
  ecosystem: 'npm'
})
ON CREATE SET
  sbom.name = split(c.description, ' ')[0],
  sbom.created_at = datetime()
MERGE (c)-[r:AFFECTS_SBOM_COMPONENT]->(sbom)
SET
  r.component_name = sbom.name,
  r.package_manager = 'npm',
  r.ecosystem = 'npm',
  r.scope = CASE
    WHEN c.description =~ '(?i).*(development|dev dependency).*' THEN 'development'
    ELSE 'required'
  END,
  r.direct_dependency = true,  // Assume direct unless specified
  r.created_at = datetime();

// Example: Link CVEs to Maven packages
MATCH (c:CVE)
WHERE c.description =~ '(?i).*(maven|java package|artifact).*'
WITH c
MERGE (sbom:SBOMComponent {
  id: 'sbom:maven:' + toLower(split(c.description, ' ')[0]),
  component_type: 'library',
  package_manager: 'maven',
  ecosystem: 'maven'
})
ON CREATE SET
  sbom.name = split(c.description, ' ')[0],
  sbom.created_at = datetime()
MERGE (c)-[r:AFFECTS_SBOM_COMPONENT]->(sbom)
SET
  r.component_name = sbom.name,
  r.package_manager = 'maven',
  r.ecosystem = 'maven',
  r.scope = 'required',
  r.created_at = datetime();

// Step 2: Link CVEs to Software Packages with version information
MATCH (c:CVE)-[:AFFECTS]->(prod:Product)
WHERE prod.name IS NOT NULL
WITH c, prod
MERGE (pkg:SoftwarePackage {
  name: prod.name,
  package_type: 'software_product'
})
ON CREATE SET
  pkg.created_at = datetime()
MERGE (c)-[r:IMPACTS_PACKAGE]->(pkg)
SET
  r.package_name = prod.name,
  r.affected_versions = CASE
    WHEN EXISTS((c)-[:AFFECTS]->(:Product)) THEN
      [(c)-[:AFFECTS]->(p:Product) | p.version]
    ELSE []
  END,
  r.patch_available = EXISTS((c)-[:FIXED_BY]->(:Patch)),
  r.created_at = datetime();

// Step 3: Create dependency chain tracking
// (Requires existing dependency data)
MATCH (c:CVE)-[:AFFECTS_SBOM_COMPONENT]->(sbom:SBOMComponent)
OPTIONAL MATCH (sbom)-[:DEPENDS_ON*1..5]->(dep:SBOMComponent)
WITH c, sbom, collect(DISTINCT dep) AS dependencies, count(dep) AS dep_depth
WHERE dep_depth > 0
MERGE (chain:DependencyChain {
  id: 'depchain:' + c.id + ':' + sbom.id,
  source_cve: c.id,
  root_component: sbom.id
})
ON CREATE SET
  chain.chain_depth = dep_depth,
  chain.created_at = datetime()
MERGE (c)-[r:PROPAGATES_THROUGH]->(chain)
SET
  r.chain_depth = dep_depth,
  r.direct_dependency = (dep_depth = 1),
  r.transitive_impact = CASE
    WHEN dep_depth = 1 THEN 'high'
    WHEN dep_depth <= 3 THEN 'medium'
    ELSE 'low'
  END,
  r.created_at = datetime();

// Step 4: Add SBOM-specific properties to CVE nodes
MATCH (c:CVE)-[r:AFFECTS_SBOM_COMPONENT]->()
WITH c,
  collect(DISTINCT r.package_manager) AS package_managers,
  count(DISTINCT r) AS component_count
SET
  c.sbom_component_count = component_count,
  c.package_ecosystems = package_managers,
  c.supply_chain_risk = CASE
    WHEN component_count >= 10 THEN 'high'
    WHEN component_count >= 5 THEN 'medium'
    ELSE 'low'
  END;

// Optional: Link to Package URLs (PURL)
MATCH (c:CVE)-[r:AFFECTS_SBOM_COMPONENT]->(sbom:SBOMComponent)
WHERE sbom.package_manager IS NOT NULL AND sbom.name IS NOT NULL
SET
  r.purl = 'pkg:' + sbom.package_manager + '/' + sbom.name,
  sbom.purl = 'pkg:' + sbom.package_manager + '/' + sbom.name;

// Step 5: Validation query
MATCH (c:CVE)-[r:AFFECTS_SBOM_COMPONENT]->(sbom:SBOMComponent)
RETURN
  sbom.package_manager AS ecosystem,
  count(DISTINCT c) AS affected_cves,
  count(DISTINCT sbom) AS affected_components,
  avg(c.cvss_score) AS avg_cvss
ORDER BY affected_cves DESC;
```

### 1.6 CVE → UCO Cyber-Observable Integration

**Pattern:** Link CVE vulnerabilities to UCO (Unified Cyber Ontology) observables for forensic analysis.

**Complete Cypher Implementation:**

```cypher
// ===============================================
// CVE → UCO Observable Integration Pattern
// ===============================================

// Step 1: Create UCO Observable types
MERGE (fileObs:UCOObservable {
  id: 'uco:FileObservable',
  name: 'File Observable',
  observable_type: 'file',
  description: 'File system artifacts'
})

MERGE (processObs:UCOObservable {
  id: 'uco:ProcessObservable',
  name: 'Process Observable',
  observable_type: 'process',
  description: 'Process execution artifacts'
})

MERGE (networkObs:UCOObservable {
  id: 'uco:NetworkObservable',
  name: 'Network Observable',
  observable_type: 'network',
  description: 'Network communication artifacts'
})

MERGE (registryObs:UCOObservable {
  id: 'uco:RegistryObservable',
  name: 'Registry Observable',
  observable_type: 'registry',
  description: 'Windows registry artifacts'
});

// Step 2: Link CVEs to UCO Observables based on exploitation artifacts
// File observables
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(file|malicious file|uploaded file|path traversal|arbitrary file).*'
  OR c.cwe_id IN ['CWE-22', 'CWE-434', 'CWE-73']  // Path traversal, file upload, external file control
WITH c
MATCH (obs:UCOObservable {observable_type: 'file'})
MERGE (c)-[r:CREATES_OBSERVABLE]->(obs)
SET
  r.observable_type = 'file',
  r.exploitation_artifact = true,
  r.detection_relevance = CASE
    WHEN c.cvss_score >= 9.0 THEN 'high'
    WHEN c.cvss_score >= 7.0 THEN 'medium'
    ELSE 'low'
  END,
  r.artifact_patterns = CASE
    WHEN c.description =~ '(?i).*malicious.*' THEN ['malicious_file_creation', 'file_hash_analysis']
    WHEN c.description =~ '(?i).*upload.*' THEN ['uploaded_file_location', 'file_permission_analysis']
    ELSE ['file_modification', 'timestamp_analysis']
  END,
  r.forensic_value = 'critical',
  r.created_at = datetime();

// Process observables
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(command execution|code execution|remote code|process injection|arbitrary commands).*'
  OR c.cwe_id IN ['CWE-78', 'CWE-94', 'CWE-502']  // OS command injection, code injection, deserialization
WITH c
MATCH (obs:UCOObservable {observable_type: 'process'})
MERGE (c)-[r:CREATES_OBSERVABLE]->(obs)
SET
  r.observable_type = 'process',
  r.exploitation_artifact = true,
  r.detection_relevance = 'high',
  r.artifact_patterns = ['process_creation', 'parent_child_relationships', 'command_line_arguments'],
  r.forensic_value = 'critical',
  r.created_at = datetime();

// Network observables
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(network|remote|external connection|data exfiltration|C2|command and control).*'
  OR c.cvss_vector =~ '.*AV:N.*'  // Network attack vector
WITH c
MATCH (obs:UCOObservable {observable_type: 'network'})
MERGE (c)-[r:CREATES_OBSERVABLE]->(obs)
SET
  r.observable_type = 'network',
  r.exploitation_artifact = true,
  r.detection_relevance = CASE
    WHEN c.description =~ '(?i).*(exfiltration|C2|backdoor).*' THEN 'high'
    ELSE 'medium'
  END,
  r.artifact_patterns = ['network_connections', 'dns_queries', 'http_requests', 'packet_analysis'],
  r.forensic_value = 'important',
  r.created_at = datetime();

// Registry observables (Windows-specific)
MATCH (c:CVE)
WHERE
  c.description =~ '(?i).*(registry|regedit|HKEY|persistence mechanism).*'
  OR c.cwe_id IN ['CWE-732']  // Incorrect permission assignment
WITH c
MATCH (obs:UCOObservable {observable_type: 'registry'})
MERGE (c)-[r:CREATES_OBSERVABLE]->(obs)
SET
  r.observable_type = 'registry',
  r.exploitation_artifact = true,
  r.detection_relevance = 'high',
  r.artifact_patterns = ['registry_key_creation', 'registry_value_modification', 'autorun_entries'],
  r.forensic_value = 'important',
  r.created_at = datetime();

// Step 3: Create UCO Action relationships
MATCH (c:CVE)-[:CREATES_OBSERVABLE]->(obs:UCOObservable)
WITH c, obs
MERGE (action:UCOAction {
  id: 'uco:action:' + obs.observable_type,
  action_type: CASE obs.observable_type
    WHEN 'file' THEN 'create'
    WHEN 'process' THEN 'execute'
    WHEN 'network' THEN 'communicate'
    WHEN 'registry' THEN 'modify'
    ELSE 'unknown'
  END,
  observable_type: obs.observable_type
})
ON CREATE SET action.created_at = datetime()
MERGE (c)-[r:TRIGGERS_ACTION]->(action)
SET
  r.action_type = action.action_type,
  r.forensic_value = CASE
    WHEN action.action_type IN ['execute', 'create'] THEN 'critical'
    ELSE 'important'
  END,
  r.created_at = datetime();

// Step 4: Add UCO properties to CVE nodes
MATCH (c:CVE)-[r:CREATES_OBSERVABLE]->()
WITH c, collect(DISTINCT r.observable_type) AS observable_types
SET
  c.uco_observable_types = observable_types,
  c.forensic_artifacts = CASE
    WHEN 'process' IN observable_types THEN ['process_tree', 'command_line']
    WHEN 'file' IN observable_types THEN ['file_hashes', 'file_metadata']
    WHEN 'network' IN observable_types THEN ['network_flows', 'connection_logs']
    ELSE ['generic_artifacts']
  END,
  c.investigation_priority = CASE
    WHEN size(observable_types) >= 3 THEN 'high'
    WHEN size(observable_types) >= 2 THEN 'medium'
    ELSE 'low'
  END;

// Step 5: Validation query
MATCH (c:CVE)-[r:CREATES_OBSERVABLE]->(obs:UCOObservable)
RETURN
  obs.observable_type AS observable,
  count(DISTINCT c) AS affected_cves,
  collect(DISTINCT r.forensic_value)[0..5] AS forensic_values,
  avg(c.cvss_score) AS avg_cvss
ORDER BY affected_cves DESC;
```

## 2. ThreatActor Enhancement Patterns

### 2.1 ThreatActor → Psychometric Profile Integration

**Pattern:** Enhance ThreatActor nodes with psychological and behavioral profiles.

**Complete Cypher Implementation:**

```cypher
// ===============================================
// ThreatActor → Psychometric Profile Pattern
// ===============================================

// Step 1: Add psychometric properties to existing ThreatActor nodes
MATCH (ta:ThreatActor)
SET
  ta.psychometric_profile = CASE ta.motivation
    WHEN 'financial' THEN 'opportunistic_pragmatist'
    WHEN 'espionage' THEN 'strategic_collector'
    WHEN 'ideology' THEN 'mission_driven_activist'
    WHEN 'destruction' THEN 'nihilistic_disruptor'
    ELSE 'unclassified'
  END,
  ta.risk_tolerance = CASE ta.sophistication
    WHEN 'high' THEN 'calculated_risk_taker'
    WHEN 'medium' THEN 'moderate_risk_taker'
    ELSE 'high_risk_taker'
  END,
  ta.operational_tempo = CASE
    WHEN EXISTS((ta)-[:CONDUCTS]->(:Campaign)) THEN
      CASE size([(ta)-[:CONDUCTS]->(c:Campaign) | c])
        WHEN 1 THEN 'slow_methodical'
        WHEN 2 THEN 'moderate_pace'
        ELSE 'high_tempo'
      END
    ELSE 'unknown'
  END,
  ta.target_selection = CASE
    WHEN EXISTS((ta)-[:TARGETS]->(:Sector)) THEN
      CASE size([(ta)-[:TARGETS]->(s:Sector) | s])
        WHEN 1 THEN 'focused_specialist'
        ELSE 'opportunistic_generalist'
      END
    ELSE 'unknown'
  END;

// Step 2: Create capability assessment based on techniques used
MATCH (ta:ThreatActor)-[:USES_TECHNIQUE]->(tech:AttackTechnique)
WITH ta, collect(tech) AS techniques
SET
  ta.technical_capability = CASE
    WHEN size(techniques) >= 20 THEN 'advanced_persistent'
    WHEN size(techniques) >= 10 THEN 'intermediate'
    ELSE 'basic'
  END,
  ta.ttp_diversity_score = size(techniques) * 1.0 / 50.0;  // Normalized to 50 max techniques

// Step 3: Enhance CVE → ThreatActor relationships with psychometric context
MATCH (c:CVE)<-[r:EXPLOITED_BY_ACTOR]-(ta:ThreatActor)
SET
  r.exploitation_motivation = ta.motivation,
  r.actor_capability_match = CASE
    WHEN c.cvss_score >= 9.0 AND ta.sophistication = 'high' THEN 0.95
    WHEN c.cvss_score >= 7.0 AND ta.sophistication IN ['high', 'medium'] THEN 0.85
    WHEN c.cvss_score < 5.0 AND ta.sophistication = 'low' THEN 0.80
    ELSE 0.70
  END,
  r.typical_campaign_phase = CASE ta.psychometric_profile
    WHEN 'strategic_collector' THEN 'reconnaissance'
    WHEN 'opportunistic_pragmatist' THEN 'exploitation'
    WHEN 'mission_driven_activist' THEN 'impact'
    ELSE 'weaponization'
  END,
  r.attribution_confidence = CASE
    WHEN EXISTS((ta)-[:ASSOCIATED_WITH]->(:Campaign)-[:USES_CVE]->(c)) THEN 0.90
    WHEN ta.sophistication = 'high' AND c.cvss_score >= 9.0 THEN 0.75
    ELSE 0.60
  END;

// Step 4: Validation query
MATCH (ta:ThreatActor)
RETURN
  ta.psychometric_profile AS profile,
  count(ta) AS actor_count,
  collect(ta.motivation)[0..5] AS sample_motivations,
  avg(ta.ttp_diversity_score) AS avg_ttp_diversity
ORDER BY actor_count DESC;
```

### 2.2 ThreatActor → STIX Indicator Integration

**Pattern:** Link ThreatActor nodes to STIX (Structured Threat Information Expression) indicators.

**Complete Cypher Implementation:**

```cypher
// ===============================================
// ThreatActor → STIX Indicator Pattern
// ===============================================

// Step 1: Create STIX Indicator nodes
MERGE (stix:STIXIndicator {
  id: 'stix:indicator:generic',
  indicator_type: 'vulnerability-signature',
  stix_version: '2.1'
})
ON CREATE SET
  stix.name = 'Generic Vulnerability Indicator',
  stix.created_at = datetime();

// Step 2: Link CVEs to STIX Indicators
MATCH (c:CVE)
WHERE c.cvss_score >= 7.0  // High/Critical CVEs get STIX indicators
WITH c
MERGE (stix:STIXIndicator {
  id: 'stix:indicator:' + c.id,
  indicator_type: 'vulnerability-signature',
  stix_version: '2.1'
})
ON CREATE SET
  stix.name = 'CVE Indicator: ' + c.id,
  stix.description = c.description,
  stix.pattern = '(software:cve = "' + c.id + '")',
  stix.valid_from = c.published_date,
  stix.created_at = datetime()
MERGE (c)-[r:HAS_STIX_INDICATOR]->(stix)
SET
  r.indicator_type = 'vulnerability-signature',
  r.detection_pattern = stix.pattern,
  r.valid_from = c.published_date,
  r.confidence = CASE
    WHEN c.status = 'PUBLISHED' THEN 0.95
    ELSE 0.75
  END,
  r.created_at = datetime();

// Step 3: Link ThreatActors to STIX Indicators via CVEs
MATCH (ta:ThreatActor)-[:EXPLOITED_BY_ACTOR]->(c:CVE)-[:HAS_STIX_INDICATOR]->(stix:STIXIndicator)
MERGE (ta)-[r:ASSOCIATED_WITH_STIX]->(stix)
SET
  r.association_type = 'exploitation',
  r.confidence = 0.85,
  r.first_seen = datetime(),
  r.created_at = datetime();

// Step 4: Add STIX indicator count to CVE nodes
MATCH (c:CVE)-[:HAS_STIX_INDICATOR]->()
WITH c, count(*) AS indicator_count
SET c.stix_indicator_count = indicator_count;

// Step 5: Validation query
MATCH (c:CVE)-[r:HAS_STIX_INDICATOR]->(stix:STIXIndicator)
RETURN
  stix.indicator_type AS indicator_type,
  count(DISTINCT c) AS cve_count,
  count(stix) AS indicator_count
ORDER BY cve_count DESC;
```

### 2.3 ThreatActor → ICS Targeting Integration

**Pattern:** Link ThreatActor nodes to ICS components they specifically target.

**Complete Cypher Implementation:**

```cypher
// ===============================================
// ThreatActor → ICS Targeting Pattern
// ===============================================

// Step 1: Identify ThreatActors with ICS targeting based on CVE exploitation
MATCH (ta:ThreatActor)-[:EXPLOITED_BY_ACTOR]->(c:CVE)-[:AFFECTS_ICS_COMPONENT]->(ics:ICSComponent)
WITH ta, ics, count(c) AS cve_count
WHERE cve_count >= 2  // Require at least 2 CVEs targeting same ICS component
MERGE (ta)-[r:TARGETS_ICS_COMPONENT]->(ics)
SET
  r.cve_exploitation_count = cve_count,
  r.targeting_confidence = CASE
    WHEN cve_count >= 10 THEN 0.95
    WHEN cve_count >= 5 THEN 0.85
    ELSE 0.75
  END,
  r.targeting_intent = CASE ta.motivation
    WHEN 'espionage' THEN 'intelligence_collection'
    WHEN 'destruction' THEN 'sabotage'
    WHEN 'financial' THEN 'ransomware'
    ELSE 'disruption'
  END,
  r.created_at = datetime();

// Step 2: Add ICS targeting properties to ThreatActor nodes
MATCH (ta:ThreatActor)-[r:TARGETS_ICS_COMPONENT]->()
WITH ta, collect(DISTINCT r) AS ics_targets
SET
  ta.ics_focused = true,
  ta.ics_target_count = size(ics_targets),
  ta.ics_threat_level = CASE
    WHEN size(ics_targets) >= 5 THEN 'critical'
    WHEN size(ics_targets) >= 3 THEN 'high'
    ELSE 'medium'
  END;

// Step 3: Link ThreatActors to ICS ATT&CK techniques
MATCH (ta:ThreatActor)-[:EXPLOITED_BY_ACTOR]->(c:CVE)-[:ENABLES_ICS_TECHNIQUE]->(tech:ICSAttackTechnique)
MERGE (ta)-[r:USES_ICS_TECHNIQUE]->(tech)
SET
  r.technique_id = tech.technique_id,
  r.usage_frequency = 'observed',
  r.confidence = 0.80,
  r.created_at = datetime();

// Step 4: Validation query
MATCH (ta:ThreatActor)-[r:TARGETS_ICS_COMPONENT]->(ics:ICSComponent)
RETURN
  ta.name AS threat_actor,
  collect(ics.component_type) AS targeted_components,
  ta.ics_threat_level AS threat_level,
  avg(r.targeting_confidence) AS avg_confidence
ORDER BY ta.ics_target_count DESC;
```

## 3. Cross-Domain Integration Patterns

### 3.1 SAREF → CVE → Mitigation Chain

**Pattern:** Complete chain from SAREF device vulnerability to mitigation strategy.

**Complete Cypher Implementation:**

```cypher
// ===============================================
// SAREF → CVE → Mitigation Chain Pattern
// ===============================================

// Query 1: Find SAREF devices with critical vulnerabilities and mitigations
MATCH path = (saref:SAREFDevice)<-[:AFFECTS_SAREF_DEVICE]-(c:CVE)-[:MITIGATED_BY]->(m:Mitigation)
WHERE c.severity = 'CRITICAL' AND c.cvss_score >= 9.0
RETURN
  saref.device_category AS device_type,
  c.id AS cve_id,
  c.cvss_score AS severity,
  c.description AS vulnerability,
  m.description AS mitigation,
  m.implementation_cost AS cost,
  path;

// Query 2: SAREF device vulnerability surface analysis
MATCH (saref:SAREFDevice)<-[r:AFFECTS_SAREF_DEVICE]-(c:CVE)
WITH saref, count(c) AS vulnerability_count, collect(c) AS cves
OPTIONAL MATCH (cve:CVE)-[:MITIGATED_BY]->(m:Mitigation)
WHERE cve IN cves
WITH saref, vulnerability_count,
  count(DISTINCT m) AS mitigation_count,
  avg(cve.cvss_score) AS avg_severity
RETURN
  saref.device_category AS device_type,
  vulnerability_count,
  mitigation_count,
  avg_severity,
  (mitigation_count * 100.0 / vulnerability_count) AS mitigation_coverage_percent
ORDER BY vulnerability_count DESC;

// Query 3: SAREF function impact with remediation paths
MATCH (saref:SAREFDevice)<-[:AFFECTS_SAREF_DEVICE]-(c:CVE)-[:IMPACTS_SAREF_FUNCTION]->(func:SAREFFunction)
OPTIONAL MATCH (c)-[:MITIGATED_BY]->(m:Mitigation)
RETURN
  saref.device_category AS device,
  func.function_category AS function,
  collect(DISTINCT c.id) AS vulnerable_cves,
  collect(DISTINCT m.description) AS available_mitigations
ORDER BY device, function;
```

### 3.2 ICS → ATT&CK → CVE → Mitigation Chain

**Pattern:** Complete ICS attack chain from component to technique to vulnerability to mitigation.

**Complete Cypher Implementation:**

```cypher
// ===============================================
// ICS → ATT&CK → CVE → Mitigation Chain Pattern
// ===============================================

// Query 1: Complete ICS attack chain analysis
MATCH path = (ics:ICSComponent)<-[:AFFECTS_ICS_COMPONENT]-(c:CVE)-[:ENABLES_ICS_TECHNIQUE]->(tech:ICSAttackTechnique)
OPTIONAL MATCH (c)-[:MITIGATED_BY]->(m:Mitigation)
RETURN
  ics.component_type AS ics_component,
  tech.technique_id AS attack_technique,
  tech.tactic AS attack_tactic,
  c.id AS cve_id,
  c.cvss_score AS severity,
  collect(DISTINCT m.description) AS mitigations,
  path;

// Query 2: ICS component vulnerability and attack surface
MATCH (ics:ICSComponent)<-[r:AFFECTS_ICS_COMPONENT]-(c:CVE)
WITH ics, collect(c) AS cves
OPTIONAL MATCH (cve:CVE)-[:ENABLES_ICS_TECHNIQUE]->(tech:ICSAttackTechnique)
WHERE cve IN cves
WITH ics, cves,
  collect(DISTINCT tech.tactic) AS attack_tactics,
  collect(DISTINCT tech.technique_id) AS techniques
RETURN
  ics.component_type AS component,
  ics.purdue_level AS purdue_level,
  size(cves) AS vulnerability_count,
  avg([cve IN cves | cve.cvss_score]) AS avg_cvss,
  attack_tactics,
  size(techniques) AS technique_count;

// Query 3: Purdue Model level vulnerability analysis
MATCH (ics:ICSComponent)<-[r:AFFECTS_ICS_COMPONENT]-(c:CVE)
WHERE r.criticality_level IN ['safety_critical', 'production_critical']
WITH r.purdue_level AS purdue_levels, collect(c) AS cves
UNWIND purdue_levels AS level
WITH level, cves
OPTIONAL MATCH (cve:CVE)-[:MITIGATED_BY]->(m:Mitigation)
WHERE cve IN cves
RETURN
  level AS purdue_level,
  count(DISTINCT cves) AS critical_cves,
  count(DISTINCT m) AS available_mitigations,
  avg([c IN cves | c.cvss_score]) AS avg_severity
ORDER BY purdue_level;

// Query 4: ICS-specific threat actor targeting analysis
MATCH (ta:ThreatActor)-[:TARGETS_ICS_COMPONENT]->(ics:ICSComponent)
MATCH (ta)-[:EXPLOITED_BY_ACTOR]->(c:CVE)-[:AFFECTS_ICS_COMPONENT]->(ics)
OPTIONAL MATCH (c)-[:ENABLES_ICS_TECHNIQUE]->(tech:ICSAttackTechnique)
RETURN
  ta.name AS threat_actor,
  ta.motivation AS motivation,
  ics.component_type AS targeted_component,
  collect(DISTINCT c.id) AS exploited_cves,
  collect(DISTINCT tech.technique_id) AS ics_techniques,
  ta.ics_threat_level AS threat_level;
```

### 3.3 SBOM → CVE → Dependency Chain → Mitigation

**Pattern:** Software supply chain vulnerability tracking with transitive dependency analysis.

**Complete Cypher Implementation:**

```cypher
// ===============================================
// SBOM → CVE → Dependency Chain Pattern
// ===============================================

// Query 1: Direct SBOM component vulnerabilities
MATCH (sbom:SBOMComponent)<-[r:AFFECTS_SBOM_COMPONENT]-(c:CVE)
OPTIONAL MATCH (c)-[:MITIGATED_BY]->(m:Mitigation)
RETURN
  sbom.name AS component,
  sbom.package_manager AS ecosystem,
  r.component_version AS version,
  collect(c.id) AS vulnerabilities,
  avg(c.cvss_score) AS avg_severity,
  collect(DISTINCT m.description) AS mitigations
ORDER BY avg_severity DESC;

// Query 2: Transitive dependency vulnerability propagation
MATCH (root:SBOMComponent)<-[:AFFECTS_SBOM_COMPONENT]-(c:CVE)-[r:PROPAGATES_THROUGH]->(chain:DependencyChain)
WHERE r.transitive_impact = 'high'
RETURN
  root.name AS root_component,
  c.id AS cve,
  r.chain_depth AS dependency_depth,
  r.transitive_impact AS impact,
  c.cvss_score AS severity
ORDER BY dependency_depth DESC, severity DESC;

// Query 3: Package ecosystem vulnerability analysis
MATCH (c:CVE)-[r:AFFECTS_SBOM_COMPONENT]->(sbom:SBOMComponent)
WITH sbom.package_manager AS ecosystem, collect(c) AS cves
RETURN
  ecosystem,
  count(DISTINCT cves) AS total_cves,
  size([c IN cves WHERE c.cvss_score >= 9.0]) AS critical_cves,
  size([c IN cves WHERE c.cvss_score >= 7.0]) AS high_cves,
  avg([c IN cves | c.cvss_score]) AS avg_cvss
ORDER BY total_cves DESC;

// Query 4: Supply chain risk assessment
MATCH (c:CVE)
WHERE c.supply_chain_risk IN ['high', 'medium']
MATCH (c)-[:AFFECTS_SBOM_COMPONENT]->(sbom:SBOMComponent)
OPTIONAL MATCH (c)-[:PROPAGATES_THROUGH]->(chain:DependencyChain)
RETURN
  c.id AS cve,
  c.supply_chain_risk AS risk_level,
  collect(DISTINCT sbom.name) AS affected_components,
  count(DISTINCT chain) AS dependency_chains,
  c.cvss_score AS severity
ORDER BY risk_level DESC, severity DESC;
```

### 3.4 ThreatActor → CVE → UCO Observable → Forensics

**Pattern:** Threat attribution through CVE exploitation to forensic artifacts.

**Complete Cypher Implementation:**

```cypher
// ===============================================
// ThreatActor → CVE → UCO Observable Pattern
// ===============================================

// Query 1: Threat actor exploitation with forensic artifacts
MATCH (ta:ThreatActor)-[r:EXPLOITED_BY_ACTOR]->(c:CVE)-[:CREATES_OBSERVABLE]->(obs:UCOObservable)
RETURN
  ta.name AS threat_actor,
  ta.motivation AS motivation,
  c.id AS exploited_cve,
  c.cvss_score AS severity,
  collect(DISTINCT obs.observable_type) AS forensic_artifacts,
  r.attribution_confidence AS confidence
ORDER BY severity DESC;

// Query 2: Campaign-level forensic intelligence
MATCH (campaign:Campaign)<-[:USED_IN_CAMPAIGN]-(c:CVE)-[:CREATES_OBSERVABLE]->(obs:UCOObservable)
OPTIONAL MATCH (campaign)<-[:CONDUCTS]-(ta:ThreatActor)
RETURN
  campaign.name AS campaign,
  ta.name AS attributed_actor,
  collect(DISTINCT c.id) AS exploited_cves,
  collect(DISTINCT obs.observable_type) AS observable_types,
  collect(DISTINCT obs.artifact_patterns) AS forensic_patterns;

// Query 3: UCO action chains for investigation
MATCH (c:CVE)-[:TRIGGERS_ACTION]->(action:UCOAction)
MATCH (c)<-[:EXPLOITED_BY_ACTOR]-(ta:ThreatActor)
RETURN
  ta.name AS threat_actor,
  c.id AS cve,
  action.action_type AS action,
  action.forensic_value AS forensic_value,
  c.investigation_priority AS priority
ORDER BY priority DESC, forensic_value DESC;

// Query 4: Multi-stage attack reconstruction
MATCH path = (ta:ThreatActor)-[:EXPLOITED_BY_ACTOR]->(c1:CVE)-[:CREATES_OBSERVABLE]->(obs1:UCOObservable),
             (ta)-[:EXPLOITED_BY_ACTOR]->(c2:CVE)-[:CREATES_OBSERVABLE]->(obs2:UCOObservable)
WHERE c1 <> c2
  AND obs1.observable_type = 'network'
  AND obs2.observable_type = 'process'
RETURN
  ta.name AS threat_actor,
  c1.id AS initial_cve,
  obs1.observable_type AS initial_observable,
  c2.id AS followup_cve,
  obs2.observable_type AS followup_observable,
  path;
```

## 4. Advanced Integration Queries

### 4.1 Multi-Domain Threat Landscape Query

**Pattern:** Comprehensive threat analysis across all domains.

```cypher
// ===============================================
// Multi-Domain Threat Landscape Analysis
// ===============================================

MATCH (ta:ThreatActor)-[:EXPLOITED_BY_ACTOR]->(c:CVE)
OPTIONAL MATCH (c)-[:AFFECTS_SAREF_DEVICE]->(saref:SAREFDevice)
OPTIONAL MATCH (c)-[:AFFECTS_ICS_COMPONENT]->(ics:ICSComponent)
OPTIONAL MATCH (c)-[:AFFECTS_SBOM_COMPONENT]->(sbom:SBOMComponent)
OPTIONAL MATCH (c)-[:CREATES_OBSERVABLE]->(uco:UCOObservable)
OPTIONAL MATCH (c)-[:MITIGATED_BY]->(m:Mitigation)
RETURN
  ta.name AS threat_actor,
  ta.motivation AS motivation,
  count(DISTINCT c) AS exploited_cves,
  count(DISTINCT saref) AS iot_targets,
  count(DISTINCT ics) AS ics_targets,
  count(DISTINCT sbom) AS supply_chain_targets,
  collect(DISTINCT uco.observable_type) AS forensic_artifacts,
  count(DISTINCT m) AS available_mitigations,
  avg(c.cvss_score) AS avg_severity
ORDER BY exploited_cves DESC;
```

### 4.2 Critical Asset Protection Query

**Pattern:** Identify critical assets (SAREF + ICS) with unmitigated vulnerabilities.

```cypher
// ===============================================
// Critical Asset Protection Analysis
// ===============================================

MATCH (c:CVE)
WHERE c.severity = 'CRITICAL' AND c.cvss_score >= 9.0
OPTIONAL MATCH (c)-[:AFFECTS_SAREF_DEVICE]->(saref:SAREFDevice)
OPTIONAL MATCH (c)-[:AFFECTS_ICS_COMPONENT]->(ics:ICSComponent)
OPTIONAL MATCH (c)-[:MITIGATED_BY]->(m:Mitigation)
WITH c, saref, ics, m
WHERE saref IS NOT NULL OR ics IS NOT NULL
RETURN
  c.id AS critical_cve,
  c.cvss_score AS severity,
  COALESCE(saref.device_category, ics.component_type) AS asset_type,
  CASE
    WHEN saref IS NOT NULL THEN 'IoT Device'
    WHEN ics IS NOT NULL THEN 'ICS Component'
  END AS domain,
  CASE
    WHEN m IS NULL THEN 'UNMITIGATED'
    ELSE 'Mitigated'
  END AS mitigation_status,
  m.description AS mitigation
ORDER BY severity DESC, mitigation_status;
```

## 5. Conclusion

This document provides comprehensive integration patterns for the AEON Digital Twin Cybersecurity Threat Intelligence schema enhancement. Each pattern includes:

- **Complete Cypher implementations** with no truncation
- **Relationship semantics** and property mappings
- **Validation queries** for data integrity
- **Cross-domain integration** examples

These patterns enable rich, multi-dimensional threat intelligence analysis across CVE vulnerabilities, IoT devices (SAREF), ICS/OT systems, software supply chains (SBOM), cyber-observables (UCO), threat actors, and attack patterns (ATT&CK).

**Implementation Checklist:**
- [ ] Review all Cypher queries for project-specific adjustments
- [ ] Test pattern queries on sample data before production
- [ ] Validate relationship property assignments
- [ ] Verify index creation for query performance
- [ ] Document any custom property additions
- [ ] Establish monitoring for integration quality

---

**Document Version:** v1.0.0
**Last Updated:** 2025-10-30
**Next Review:** During Wave Implementation
**Owner:** AEON FORGE Implementation Team
