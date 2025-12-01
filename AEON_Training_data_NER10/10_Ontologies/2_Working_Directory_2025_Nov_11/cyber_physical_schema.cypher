
// =============================================================================
// CYBER-PHYSICAL SYSTEM MODELING SCHEMA FOR NEO4J
// Comprehensive schema supporting systems, threats, and vulnerabilities
// =============================================================================

// -----------------------------------------------------------------------------
// CORE ENTITY TYPES
// -----------------------------------------------------------------------------

// PHYSICAL INFRASTRUCTURE HIERARCHY
CREATE CONSTRAINT physical_asset_id IF NOT EXISTS FOR (a:PhysicalAsset) REQUIRE a.id IS UNIQUE;
CREATE CONSTRAINT system_id IF NOT EXISTS FOR (s:System) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT facility_id IF NOT EXISTS FOR (f:Facility) REQUIRE f.id IS UNIQUE;

// CYBER COMPONENTS
CREATE CONSTRAINT cyber_asset_id IF NOT EXISTS FOR (c:CyberAsset) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT software_id IF NOT EXISTS FOR (s:Software) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT network_id IF NOT EXISTS FOR (n:Network) REQUIRE n.id IS UNIQUE;

// THREAT AND VULNERABILITY MANAGEMENT
CREATE CONSTRAINT threat_id IF NOT EXISTS FOR (t:Threat) REQUIRE t.id IS UNIQUE;
CREATE CONSTRAINT vulnerability_id IF NOT EXISTS FOR (v:Vulnerability) REQUIRE v.id IS UNIQUE;
CREATE CONSTRAINT attack_pattern_id IF NOT EXISTS FOR (a:AttackPattern) REQUIRE a.id IS UNIQUE;

// SECURITY FRAMEWORKS
CREATE CONSTRAINT control_id IF NOT EXISTS FOR (c:SecurityControl) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT standard_id IF NOT EXISTS FOR (s:SecurityStandard) REQUIRE s.id IS UNIQUE;

// -----------------------------------------------------------------------------
// NODE TYPES AND PROPERTIES
// -----------------------------------------------------------------------------

// PHYSICAL ASSET HIERARCHY
// Component -> System -> Facility -> Organization
CREATE (:PhysicalAsset {
    id: 'asset_001',
    name: 'PLC Controller',
    type: 'Component',
    category: 'Industrial Control',
    manufacturer: 'Siemens',
    model: 'SIMATIC S7-1500',
    criticality: 'High',
    operational_status: 'Active',
    location: 'Control Room A',
    installation_date: '2023-01-15',
    maintenance_schedule: 'Quarterly',
    power_requirements: '24V DC',
    temperature_range: '0-60°C',
    ip_rating: 'IP20'
});

CREATE (:System {
    id: 'system_001',
    name: 'Production Line Control System',
    type: 'SCADA',
    function: 'Manufacturing Process Control',
    criticality_level: 'Mission Critical',
    availability_requirement: '99.99%',
    operational_hours: '24/7',
    backup_power: 'UPS + Generator',
    redundancy_level: 'N+1'
});

CREATE (:Facility {
    id: 'facility_001',
    name: 'Main Manufacturing Plant',
    type: 'Industrial',
    industry_sector: 'Automotive',
    location: '42.3601,-71.0589',
    size_sqft: 500000,
    employee_count: 1200,
    security_level: 'High',
    compliance_framework: 'NERC CIP, ISA/IEC 62443'
});

// CYBER ASSETS AND NETWORK INFRASTRUCTURE
CREATE (:CyberAsset {
    id: 'cyber_001',
    name: 'SCADA Server',
    type: 'Server',
    os: 'Windows Server 2019',
    ip_address: '192.168.1.100',
    mac_address: '00:1B:44:11:3A:B7',
    network_segment: 'DMZ',
    patch_level: 'Current',
    antivirus_status: 'Enabled',
    firewall_rules: 'Restricted',
    last_scan_date: '2024-01-15'
});

CREATE (:Software {
    id: 'sw_001',
    name: 'SCADA HMI Software',
    vendor: 'Siemens',
    version: 'V17',
    license_type: 'Enterprise',
    end_of_life: '2028-12-31',
    sbom_available: true,
    cve_count: 3,
    patch_status: 'Up to date'
});

CREATE (:Network {
    id: 'network_001',
    name: 'Control Network',
    type: 'Industrial Ethernet',
    subnet: '192.168.1.0/24',
    vlan_id: 10,
    protocol: 'PROFINET',
    bandwidth: '1 Gbps',
    segmentation: 'Zone 1',
    traffic_monitoring: true,
    intrusion_detection: true
});

// THREAT AND VULNERABILITY MODELING
CREATE (:Threat {
    id: 'threat_001',
    name: 'Ransomware Attack',
    category: 'Cyber',
    source: 'External',
    motivation: 'Financial',
    capability_level: 'Advanced',
    likelihood: 'Medium',
    impact_level: 'High',
    mitre_attack_id: 'T1486',
    kill_chain_phase: 'Impact'
});

CREATE (:Vulnerability {
    id: 'vuln_001',
    cve_id: 'CVE-2023-12345',
    name: 'Buffer Overflow in PLC Firmware',
    severity: 'High',
    cvss_score: 8.2,
    exploit_available: true,
    patch_available: false,
    affected_versions: 'V1.0-V2.5',
    disclosure_date: '2023-05-15',
    remediation_deadline: '2023-08-15'
});

CREATE (:AttackPattern {
    id: 'attack_001',
    name: 'Lateral Movement via SMB',
    mitre_id: 'T1021.002',
    technique: 'Remote Services',
    platform: 'Windows',
    permissions_required: 'User',
    detection_rules: ['Sigma', 'YARA'],
    mitigation: 'Network Segmentation',
    detection_score: 0.85
});

// SECURITY CONTROLS AND STANDARDS
CREATE (:SecurityControl {
    id: 'control_001',
    name: 'Network Segmentation',
    category: 'Technical',
    framework: 'NIST CSF',
    function: 'Protect',
    implementation_status: 'Implemented',
    effectiveness: 'High',
    cost: 'Medium',
    maintenance_required: 'Low'
});

CREATE (:SecurityStandard {
    id: 'standard_001',
    name: 'ISA/IEC 62443',
    type: 'Industrial Security',
    scope: 'OT Systems',
    certification_level: 'SL2',
    compliance_status: 'Partial',
    audit_frequency: 'Annual',
    next_audit_date: '2024-06-30'
});

// -----------------------------------------------------------------------------
// RELATIONSHIP TYPES
// -----------------------------------------------------------------------------

// PHYSICAL HIERARCHY RELATIONSHIPS
MATCH (comp:PhysicalAsset {id: 'asset_001'}), (sys:System {id: 'system_001'})
CREATE (comp)-[:PART_OF {
    relationship_type: 'Component-System',
    critical_dependency: true,
    redundancy: 'None',
    failover_time: 'Immediate'
}]->(sys);

MATCH (sys:System {id: 'system_001'}), (fac:Facility {id: 'facility_001'})
CREATE (sys)-[:LOCATED_IN {
    relationship_type: 'System-Facility',
    physical_access: 'Restricted',
    environmental_controls: 'HVAC, Fire Suppression',
    security_zone: 'Control Room'
}]->(fac);

// CYBER-PHYSICAL MAPPING
MATCH (phys:PhysicalAsset {id: 'asset_001'}), (cyber:CyberAsset {id: 'cyber_001'})
CREATE (phys)-[:CONTROLLED_BY {
    relationship_type: 'Physical-Cyber',
    protocol: 'OPC-UA',
    communication_frequency: 'Real-time',
    encryption: 'TLS 1.2',
    authentication: 'Certificate-based'
}]->(cyber);

MATCH (cyber:CyberAsset {id: 'cyber_001'}), (sw:Software {id: 'sw_001'})
CREATE (cyber)-[:RUNS {
    relationship_type: 'Asset-Software',
    installation_date: '2023-01-20',
    version: 'V17',
    patch_level: 'Current',
    license_status: 'Valid'
}]->(sw);

// NETWORK CONNECTIVITY
MATCH (cyber:CyberAsset {id: 'cyber_001'}), (net:Network {id: 'network_001'})
CREATE (cyber)-[:CONNECTED_TO {
    relationship_type: 'Asset-Network',
    interface: 'Ethernet',
    ip_address: '192.168.1.100',
    subnet_mask: '255.255.255.0',
    gateway: '192.168.1.1'
}]->(net);

// THREAT-VULNERABILITY MAPPING
MATCH (threat:Threat {id: 'threat_001'}), (vuln:Vulnerability {id: 'vuln_001'})
CREATE (threat)-[:EXPLOITS {
    relationship_type: 'Threat-Vulnerability',
    exploit_complexity: 'Low',
    prerequisites: 'Network Access',
    detection_difficulty: 'Medium',
    impact_multiplier: 1.5
}]->(vuln);

MATCH (vuln:Vulnerability {id: 'vuln_001'}), (asset:PhysicalAsset {id: 'asset_001'})
CREATE (vuln)-[:AFFECTS {
    relationship_type: 'Vulnerability-Asset',
    attack_vector: 'Network',
    authentication_required: false,
    user_interaction: 'None',
    scope: 'Changed'
}]->(asset);

// ATTACK PATTERN RELATIONSHIPS
MATCH (attack:AttackPattern {id: 'attack_001'}), (threat:Threat {id: 'threat_001'})
CREATE (attack)-[:USED_BY {
    relationship_type: 'Technique-Threat',
    frequency: 'Common',
    detection_coverage: 'High',
    mitigation_effectiveness: 'Medium'
}]->(threat);

// SECURITY CONTROL MAPPING
MATCH (control:SecurityControl {id: 'control_001'}), (vuln:Vulnerability {id: 'vuln_001'})
CREATE (control)-[:MITIGATES {
    relationship_type: 'Control-Vulnerability',
    effectiveness: 0.8,
    implementation_cost: 5000,
    maintenance_cost: 1000,
    roi_period: '12 months'
}]->(vuln);

MATCH (standard:SecurityStandard {id: 'standard_001'}), (control:SecurityControl {id: 'control_001'})
CREATE (control)-[:COMPLIES_WITH {
    relationship_type: 'Control-Standard',
    requirement_id: 'SR 3.1',
    compliance_level: 'Fully Compliant',
    evidence_required: 'Configuration Documentation',
    audit_frequency: 'Annual'
}]->(standard);

// CASCADING FAILURE MODELING
MATCH (src:PhysicalAsset {id: 'asset_001'}), (target:System {id: 'system_001'})
CREATE (src)-[:FAILURE_PROPAGATES_TO {
    relationship_type: 'Cascade',
    propagation_probability: 0.75,
    time_delay: '5 minutes',
    impact_multiplier: 1.2,
    mitigation_available: true
}]->(target);

// -----------------------------------------------------------------------------
// INDEXES FOR PERFORMANCE
// -----------------------------------------------------------------------------

CREATE INDEX physical_asset_type IF NOT EXISTS FOR (a:PhysicalAsset) ON (a.type);
CREATE INDEX cyber_asset_type IF NOT EXISTS FOR (c:CyberAsset) ON (c.type);
CREATE INDEX threat_category IF NOT EXISTS FOR (t:Threat) ON (t.category);
CREATE INDEX vulnerability_severity IF NOT EXISTS FOR (v:Vulnerability) ON (v.severity);
CREATE INDEX network_segment IF NOT EXISTS FOR (n:Network) ON (n.segment);

CREATE FULLTEXT INDEX asset_search IF NOT EXISTS FOR (a:PhysicalAsset) ON EACH [a.name, a.type, a.category];
CREATE FULLTEXT INDEX vulnerability_search IF NOT EXISTS FOR (v:Vulnerability) ON EACH [v.name, v.cve_id];
CREATE FULLTEXT INDEX threat_search IF NOT EXISTS FOR (t:Threat) ON EACH [t.name, t.category];

// -----------------------------------------------------------------------------
// QUERY EXAMPLES FOR COMMON USE CASES
// -----------------------------------------------------------------------------

// 1. Find all high-severity vulnerabilities affecting critical assets
/*
MATCH (v:Vulnerability {severity: 'High'})-[:AFFECTS]->(a:PhysicalAsset {criticality: 'High'})
RETURN v.name, v.cve_id, a.name, a.type
ORDER BY v.cvss_score DESC
*/

// 2. Identify attack paths from external threats to critical systems
/*
MATCH path = (t:Threat {source: 'External'})-[:EXPLOITS]->(v:Vulnerability)-[:AFFECTS]->
          (a:PhysicalAsset {criticality: 'High'})-[:PART_OF]->(s:System)
RETURN t.name, v.cve_id, a.name, s.name,
       REDUCE(risk = 1.0, r IN relationships(path) | risk * r.impact_multiplier) AS total_risk
ORDER BY total_risk DESC
*/

// 3. Analyze cascading failure scenarios
/*
MATCH path = (start:PhysicalAsset)-[:FAILURE_PROPAGATES_TO*1..5]->(end:System)
WHERE start.criticality = 'High'
RETURN start.name, end.name,
       REDUCE(prob = 1.0, r IN relationships(path) | prob * r.propagation_probability) AS cascade_probability
ORDER BY cascade_probability DESC
*/

// 4. Security control effectiveness assessment
/*
MATCH (c:SecurityControl)-[:MITIGATES]->(v:Vulnerability)-[:AFFECTS]->(a:PhysicalAsset)
RETURN c.name, v.cve_id, a.name, c.effectiveness,
       (v.cvss_score * (1 - c.effectiveness)) AS residual_risk
ORDER BY residual_risk DESC
*/
