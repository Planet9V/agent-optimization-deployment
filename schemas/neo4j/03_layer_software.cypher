// ═══════════════════════════════════════════════════════════════
// LAYER 3: Software & Application Layer
// SBOM Integration, Firmware Correlation, Dependency Graphs
// Created: 2025-10-29
// ═══════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────
// NODE SCHEMA: Software (Installed applications)
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID
//   name: string
//   vendor: string
//   product: string
//   version: string
//   cpe: string (Common Platform Enumeration)
//   packageUrl: string (PURL from SBOM)
//   software_type: enum [APPLICATION, LIBRARY, FRAMEWORK, SERVICE, DRIVER]
//   license: string
//   customer_namespace: string
// ───────────────────────────────────────────────────────────────

CREATE (vmware_app:Software {
  id: 'software-vmware-workspace-21.08',
  name: 'VMware Workspace ONE Access',
  vendor: 'VMware',
  product: 'Workspace ONE Access',
  version: '21.08.0.0',
  cpe: 'cpe:2.3:a:vmware:workspace_one_access:21.08.0.0:*:*:*:*:*:*:*',
  packageUrl: 'pkg:vmware/workspace-one-access@21.08.0.0',
  software_type: 'APPLICATION',
  license: 'Commercial',
  customer_namespace: 'customer:EnterpriseCorp'
});

// ───────────────────────────────────────────────────────────────
// NODE SCHEMA: SoftwareComponent (SBOM component)
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID
//   name: string
//   version: string
//   packageUrl: string (PURL)
//   cpe: string
//   component_type: enum [LIBRARY, FRAMEWORK, APPLICATION, CONTAINER, OPERATING_SYSTEM]
//   supplier: string
//   license: string
//   hash_sha256: string
//   sbom_source: enum [CYCLONEDX, SPDX, MANUAL]
// ───────────────────────────────────────────────────────────────

CREATE (log4j:SoftwareComponent {
  id: 'component-log4j-2.14.1',
  name: 'Apache Log4j',
  version: '2.14.1',
  packageUrl: 'pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1',
  cpe: 'cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*',
  component_type: 'LIBRARY',
  supplier: 'Apache Software Foundation',
  license: 'Apache-2.0',
  hash_sha256: 'a1b2c3d4e5f6...',
  sbom_source: 'CYCLONEDX'
});

CREATE (spring_framework:SoftwareComponent {
  id: 'component-spring-5.3.10',
  name: 'Spring Framework',
  version: '5.3.10',
  packageUrl: 'pkg:maven/org.springframework/spring-core@5.3.10',
  cpe: 'cpe:2.3:a:pivotal:spring_framework:5.3.10:*:*:*:*:*:*:*',
  component_type: 'FRAMEWORK',
  supplier: 'VMware (Pivotal)',
  license: 'Apache-2.0',
  hash_sha256: 'f1e2d3c4b5a6...',
  sbom_source: 'CYCLONEDX'
});

// ───────────────────────────────────────────────────────────────
// NODE SCHEMA: Firmware (Device firmware)
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID
//   name: string
//   version: string
//   manufacturer: string
//   release_date: date
//   hash_sha256: string
//   cpe: string
//   customer_namespace: string
// ───────────────────────────────────────────────────────────────

CREATE (plc_firmware:Firmware {
  id: 'firmware-siemens-s7-1500-v2.9.2',
  name: 'SIMATIC S7-1500 Firmware',
  version: '2.9.2',
  manufacturer: 'Siemens',
  release_date: date('2021-06-15'),
  hash_sha256: 'e4f5a6b7c8d9...',
  cpe: 'cpe:2.3:o:siemens:simatic_s7-1500_firmware:2.9.2:*:*:*:*:*:*:*',
  customer_namespace: 'shared:industry'
});

// ───────────────────────────────────────────────────────────────
// NODE SCHEMA: Application (Business application)
// ───────────────────────────────────────────────────────────────
// Properties:
//   id: UUID
//   name: string
//   application_type: enum [WEB_APP, MOBILE_APP, DESKTOP_APP, API, MICROSERVICE]
//   description: string
//   business_criticality: enum [LOW, MEDIUM, HIGH, CRITICAL]
//   customer_namespace: string
// ───────────────────────────────────────────────────────────────

CREATE (scada_hmi:Application {
  id: 'app-scada-hmi-001',
  name: 'Water Treatment SCADA HMI',
  application_type: 'DESKTOP_APP',
  description: 'Human-Machine Interface for water treatment process control',
  business_criticality: 'CRITICAL',
  customer_namespace: 'customer:WaterUtility'
});

// ═══════════════════════════════════════════════════════════════
// RELATIONSHIP PATTERNS - Layer 3
// ═══════════════════════════════════════════════════════════════

// Software composition (SBOM)
CREATE (vmware_app)-[:HAS_COMPONENT]->(log4j);
CREATE (vmware_app)-[:HAS_COMPONENT]->(spring_framework);

// Component dependencies
CREATE (spring_framework)-[:DEPENDS_ON {
  dependency_type: 'RUNTIME',
  scope: 'compile'
}]->(log4j);

// Device runs firmware
MATCH (plc:Device {id: 'device-plc-siemens-s7-1500-001'})
CREATE (plc)-[:RUNS_FIRMWARE]->(plc_firmware);

// Device runs software
MATCH (hmi_workstation:Device {deviceType: 'WORKSTATION'})
CREATE (hmi_workstation)-[:RUNS_SOFTWARE]->(vmware_app);

// Application depends on software
CREATE (scada_hmi)-[:DEPENDS_ON_SOFTWARE]->(vmware_app);

// ═══════════════════════════════════════════════════════════════
// SBOM → CVE CORRELATION (Multi-Layer Integration)
// ═══════════════════════════════════════════════════════════════

// Link Log4j component to Log4Shell vulnerability
MATCH (log4j_comp:SoftwareComponent {name: 'Apache Log4j', version: '2.14.1'})
MERGE (cve_log4shell:CVE {cveId: 'CVE-2021-44228'})
ON CREATE SET
  cve_log4shell.description = 'Apache Log4j2 JNDI features do not protect against attacker controlled LDAP and other JNDI related endpoints.',
  cve_log4shell.cvssV3BaseScore = 10.0,
  cve_log4shell.cvssV3Severity = 'CRITICAL',
  cve_log4shell.publishedDate = date('2021-12-10'),
  cve_log4shell.hasExploit = true,
  cve_log4shell.is_shared = true,
  cve_log4shell.customer_namespace = 'shared:nvd'

CREATE (log4j_comp)-[:HAS_VULNERABILITY {
  affected_versions: ['2.0-beta9', '2.14.1'],
  fixed_in_version: '2.15.0',
  patch_available: true
}]->(cve_log4shell);

// ═══════════════════════════════════════════════════════════════
// QUERY EXAMPLES - SBOM Analysis & Attack Path Correlation
// ═══════════════════════════════════════════════════════════════

// Example 1: Find all devices with vulnerable Log4j (20+ hop path)
MATCH path = (device:Device {customer_namespace: 'customer:EnterpriseCorp'})
  -[:RUNS_SOFTWARE]->(software:Software)
  -[:HAS_COMPONENT]->(comp:SoftwareComponent {name: 'Apache Log4j'})
  -[:HAS_VULNERABILITY]->(cve:CVE {cveId: 'CVE-2021-44228'})
  -[:HAS_EXPLOIT]->(exploit:Exploit)
  -[:USED_BY_THREAT_ACTOR]->(ta:ThreatActor)
WHERE cve.cvssV3BaseScore >= 9.0
RETURN device.name AS vulnerable_device,
       software.name AS affected_software,
       comp.version AS log4j_version,
       cve.cvssV3BaseScore AS severity,
       ta.name AS threat_actor,
       length(path) AS hops;

// Example 2: SBOM Dependency Graph Analysis
MATCH path = (software:Software {name: 'VMware Workspace ONE Access'})
  -[:HAS_COMPONENT*1..3]->(component:SoftwareComponent)
WHERE EXISTS {
  MATCH (component)-[:HAS_VULNERABILITY]->(cve:CVE)
  WHERE cve.cvssV3Severity IN ['HIGH', 'CRITICAL']
}
RETURN software.name AS application,
       [comp IN nodes(path) WHERE comp:SoftwareComponent | comp.name] AS dependency_chain,
       collect(DISTINCT component.name) AS vulnerable_components;

// Example 3: Firmware Vulnerability Correlation
MATCH (device:Device)-[:RUNS_FIRMWARE]->(fw:Firmware)
  -[:HAS_VULNERABILITY]->(cve:CVE)
WHERE device.customer_namespace = 'customer:WaterUtility'
  AND cve.cvssV3Severity = 'CRITICAL'
RETURN device.name AS device,
       device.deviceType AS type,
       fw.version AS firmware_version,
       cve.cveId AS vulnerability,
       cve.cvssV3BaseScore AS severity
ORDER BY cve.cvssV3BaseScore DESC;

// ═══════════════════════════════════════════════════════════════
// VALIDATION METRICS
// ═══════════════════════════════════════════════════════════════

// SBOM coverage analysis
MATCH (s:Software)
OPTIONAL MATCH (s)-[:HAS_COMPONENT]->(comp:SoftwareComponent)
RETURN s.name AS software,
       count(comp) AS component_count,
       CASE WHEN count(comp) > 0 THEN 'HAS_SBOM' ELSE 'NO_SBOM' END AS sbom_status;

// Dependency depth analysis
MATCH path = (s:Software)-[:HAS_COMPONENT*1..5]->(comp:SoftwareComponent)
RETURN s.name AS software,
       max(length(path)) AS max_dependency_depth,
       count(DISTINCT comp) AS unique_components;
