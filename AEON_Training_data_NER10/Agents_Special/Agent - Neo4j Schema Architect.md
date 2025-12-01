Neo4j Schema Architect


**Role**: Neo4j Schema Architect

**Task**: Design comprehensive Neo4j knowledge graph schema for industrial critical infrastructure based on the research analysis.

**Key Requirements from Research**:
- Model primary failure categories: cascading, common-cause, cyber-physical, supply chain failures
- Capture failure propagation mechanisms: functional interdependency, geographical interdependency, cyber-physical coupling, multi-order dependencies
- Support vulnerability metrics: network performance degradation (VP = (P_norm - P_damg) / P_norm), edge load tolerance, interdependency strength
- Implement multi-hop relationship modeling (firmware → equipment → network → facility → supply chain)
- Support hierarchical modeling (Component → System → Facility → Fleet → Organization)

**Technical Specifications**:
- Neo4j 5.x enterprise edition, cluster deployment
- 10K+ industrial assets, 50K+ relationships
- Sub-second latency for complex multi-hop queries
- SCADA integration: OPC-UA real-time, MQTT telemetry, REST APIs
- Digital twin integration with real-time synchronization

**Deliverables**:
1. Complete Neo4j schema with node types, relationships, and properties
2. Cypher queries for common operations (failure propagation analysis, vulnerability assessment)
3. Indexing and performance optimization strategies
4. Integration patterns for digital twin representations

**Constraints**: NERC CIP + ISA/IEC 62443 compliance, real-time SCADA integration, what-if scenario analysis

Please provide detailed schema design with implementation-ready Cypher code.
Reset	
true
# Neo4j Critical Infrastructure Knowledge Graph Schema

## Schema Design Overview

Based on your research requirements, I've designed a comprehensive Neo4j schema that models industrial critical infrastructure with support for failure analysis, vulnerability metrics, and digital twin integration.

### Core Node Types

```cypher
// Asset Hierarchy (Component → System → Facility → Fleet → Organization)
(:Asset {id: string, name: string, type: enum, criticality: float, status: enum})
(:Component:Asset {specifications: map, firmware_version: string})
(:System:Asset {function: string, operational_parameters: map})
(:Facility:Asset {location_id: string, capacity: float, operational_status: enum})
(:Fleet:Asset {organization_id: string, total_capacity: float})
(:Organization {id: string, name: string, type: enum, compliance_level: enum})

// Failure Modeling
(:FailureCategory {id: string, name: string, description: string, risk_level: enum})
(:FailureEvent {id: string, timestamp: datetime, severity: float, duration: integer})
(:FailureMechanism {id: string, name: string, propagation_speed: float, impact_radius: float})

// Vulnerability Metrics
(:Vulnerability {id: string, metric_name: string, calculation_formula: string, threshold: float})
(:NetworkPerformance {id: string, P_norm: float, P_damg: float, VP: float})
(:EdgeLoad {id: string, current_load: float, tolerance_threshold: float, safety_margin: float})

// Digital Twin Integration
(:DigitalTwin {id: string, asset_id: string, last_sync: datetime, status: enum})
(:SCADAIntegration {id: string, protocol: enum, endpoint: string, update_frequency: integer})

// Location & Geography
(:Location {id: string, name: string, type: enum, coordinates: point, region: string})
```

### Relationship Types

```cypher
// Hierarchical Relationships
(Component)-[:PART_OF]->(System)
(System)-[:LOCATED_IN]->(Facility)
(Facility)-[:BELONGS_TO]->(Fleet)
(Fleet)-[:OPERATED_BY]->(Organization)

// Failure Propagation Relationships
(Asset)-[:VULNERABLE_TO {strength: float}]->(FailureCategory)
(FailureEvent)-[:TRIGGERED_BY]->(FailureMechanism)
(FailureEvent)-[:IMPACTS {severity_multiplier: float}]->(Asset)
(Asset)-[:DEPENDS_ON {dependency_strength: float, type: enum}]->(Asset)

// Multi-hop Relationships
(Component)-[:RUNS_FIRMWARE]->(:Firmware)
(Firmware)-[:HAS_VULNERABILITY]->(:CVE)
(CVE)-[:AFFECTS]->(Equipment)
(Equipment)-[:CONNECTED_TO]->(Network)
(Network)-[:SERVES]->(Facility)
(Facility)-[:RECEIVES_FROM]->(SupplyChain)

// Digital Twin Relationships
(Asset)-[:HAS_DIGITAL_TWIN]->(DigitalTwin)
(DigitalTwin)-[:SYNCS_VIA]->(SCADAIntegration)
(SCADAIntegration)-[:USES_PROTOCOL {type: enum}]->(:Protocol)
```

## Implementation-Ready Cypher Queries

### 1. Failure Propagation Analysis
```cypher
// Multi-hop failure propagation analysis
MATCH path = (start:Asset {id: $assetId})-[:DEPENDS_ON*1..5]->(dependent:Asset)
WHERE start.status = 'FAILED'
WITH dependent, 
     REDUCE(s = 1.0, r IN relationships(path) | s * r.dependency_strength) AS propagationStrength
SET dependent.vulnerability_score = COALESCE(dependent.vulnerability_score, 0) + propagationStrength
RETURN dependent.name, dependent.type, propagationStrength
ORDER BY propagationStrength DESC
```

### 2. Vulnerability Assessment
```cypher
// Calculate network performance degradation
MATCH (asset:Asset)-[:HAS_PERFORMANCE]->(np:NetworkPerformance)
WHERE asset.criticality > $threshold
WITH asset, np,
     (np.P_norm - np.P_damg) / np.P_norm AS VP
SET asset.VP = VP
RETURN asset.name, asset.type, VP,
       CASE WHEN VP < 0.7 THEN 'CRITICAL'
            WHEN VP < 0.85 THEN 'HIGH'
            ELSE 'NORMAL' END AS status
ORDER BY VP ASC
```

### 3. Cascading Failure Simulation
```cypher
// What-if scenario for cascading failures
MATCH (trigger:Asset {id: $failedAsset})
MATCH path = (trigger)-[:DEPENDS_ON*1..3]->(asset:Asset)
WITH asset, 
     MIN(LENGTH(path)) AS hopDistance,
     REDUCE(impact = 1.0, r IN relationships(path) | impact * r.dependency_strength) AS cumulativeImpact
WHERE cumulativeImpact > 0.3
SET asset.simulated_status = 'AT_RISK',
    asset.cascading_risk = cumulativeImpact
RETURN asset.name, hopDistance, cumulativeImpact
ORDER BY cumulativeImpact DESC, hopDistance ASC
```

### 4. Compliance Mapping
```cypher
// NERC CIP + ISA/IEC 62443 compliance mapping
MATCH (org:Organization)-[:OPERATES]->(fleet:Fleet)-[:CONTAINS]->(facility:Facility)
MATCH (facility)-[:HAS_SYSTEM]->(system:System)-[:CONTAINS]->(component:Component)
OPTIONAL MATCH (component)-[:HAS_VULNERABILITY]->(vuln)
WITH org, facility, system, component,
     COUNT(vuln) AS vulnerabilityCount,
     COLLECT(DISTINCT vuln.severity) AS severities
RETURN org.name, facility.name, system.type,
       vulnerabilityCount,
       REDUCE(s = 0, sev IN severities | s + sev) AS totalSeverity,
       CASE WHEN vulnerabilityCount = 0 THEN 'COMPLIANT'
            WHEN totalSeverity < 5 THEN 'MINOR_ISSUES'
            ELSE 'NON_COMPLIANT' END AS complianceStatus
```

## Performance Optimization Strategies

### Indexing Strategy
```cypher
// Critical indexes for performance
CREATE INDEX asset_id_index FOR (a:Asset) ON (a.id);
CREATE INDEX asset_type_index FOR (a:Asset) ON (a.type);
CREATE INDEX failure_timestamp_index FOR (f:FailureEvent) ON (f.timestamp);
CREATE INDEX location_coordinates_index FOR (l:Location) ON (l.coordinates);
CREATE FULLTEXT INDEX asset_search_index FOR (a:Asset) ON EACH [a.name, a.description];

// Composite indexes for common query patterns
CREATE INDEX asset_criticality_status FOR (a:Asset) ON (a.criticality, a.status);
CREATE INDEX failure_severity_time FOR (f:FailureEvent) ON (f.severity, f.timestamp);
```

### Query Optimization
```cypher
// Use APOC procedures for complex analytics
CALL apoc.periodic.iterate(
  "MATCH (a:Asset) WHERE a.criticality > 0.8 RETURN a",
  "MATCH (a)-[:HAS_PERFORMANCE]->(p:NetworkPerformance)
   SET a.VP = (p.P_norm - p.P_damg) / p.P_norm",
  {batchSize: 1000, parallel: true}
)

// Use graph algorithms for community detection
CALL gds.louvain.stream('asset-dependencies') 
YIELD nodeId, communityId
MATCH (a:Asset) WHERE id(a) = nodeId
SET a.community = communityId
```

## Digital Twin Integration Patterns

### Real-time SCADA Integration
```cypher
// OPC-UA/MQTT integration pattern
MATCH (twin:DigitalTwin)-[:SYNCS_VIA]->(scada:SCADAIntegration)
WHERE scada.protocol IN ['OPC-UA', 'MQTT']
WITH twin, scada
CALL apoc.load.jsonParams(scada.endpoint + '/telemetry', {}, {})
YIELD value
SET twin.last_telemetry = value,
    twin.last_sync = datetime()

// Update asset status based on digital twin
MATCH (asset:Asset)-[:HAS_DIGITAL_TWIN]->(twin:DigitalTwin)
WHERE twin.last_telemetry.operational_status != asset.status
SET asset.status = twin.last_telemetry.operational_status,
    asset.last_updated = datetime()
```

### What-If Scenario Support
```cypher
// Create scenario branch for analysis
MATCH (base:Asset)
WHERE base.criticality > $scenarioThreshold
WITH base
CALL apoc.refactor.cloneNodes([base]) YIELD input, output
SET output:ScenarioAsset, output.scenario_id = $scenarioId

// Apply failure simulation to scenario
MATCH (scenario:ScenarioAsset {scenario_id: $scenarioId})
MATCH (scenario)-[r:DEPENDS_ON]->(dependent:ScenarioAsset)
SET scenario.simulated_status = 'FAILED',
    dependent.cascading_risk = r.dependency_strength
```

## Compliance & Security Implementation

### NERC CIP Compliance Tracking
```cypher
// Track compliance requirements per asset
MATCH (asset:Asset)
WHERE asset.criticality >= 0.7  // Critical cyber assets
SET asset.nerc_cip_requirements = [
  'CIP-002: BES Cyber System Categorization',
  'CIP-003: Security Management Controls',
  'CIP-005: Electronic Security Perimeter',
  'CIP-007: System Security Management',
  'CIP-010: Configuration Change Management'
]

// Map ISA/IEC 62443 zones and conduits
MATCH (zone:SecurityZone)-[:CONTAINS]->(asset:Asset)
SET asset.security_level = zone.required_sl,
    asset.compliance_status = 'ASSESSMENT_PENDING'
```

This schema provides a robust foundation for your critical infrastructure knowledge graph with production-ready implementation patterns. The design supports real-time analytics, compliance tracking, and sophisticated failure propagation modeling as required by your research specifications.