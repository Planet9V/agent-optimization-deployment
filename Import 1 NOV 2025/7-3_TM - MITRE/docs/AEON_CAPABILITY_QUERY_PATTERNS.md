# AEON Capability Query Patterns
**File:** AEON_CAPABILITY_QUERY_PATTERNS.md
**Created:** 2025-11-08
**Purpose:** Comprehensive Cypher query patterns for 8 key AEON capability questions
**Status:** ACTIVE

---

## Index Requirements

```cypher
// Create indexes for optimal query performance
CREATE INDEX cve_id IF NOT EXISTS FOR (c:CVE) ON (c.id);
CREATE INDEX cve_published IF NOT EXISTS FOR (c:CVE) ON (c.publishedDate);
CREATE INDEX equipment_id IF NOT EXISTS FOR (e:Equipment) ON (e.id);
CREATE INDEX equipment_type IF NOT EXISTS FOR (e:Equipment) ON (e.type);
CREATE INDEX facility_id IF NOT EXISTS FOR (f:Facility) ON (f.id);
CREATE INDEX vulnerability_id IF NOT EXISTS FOR (v:Vulnerability) ON (v.id);
CREATE INDEX application_name IF NOT EXISTS FOR (a:Application) ON (a.name);
CREATE INDEX os_name IF NOT EXISTS FOR (os:OperatingSystem) ON (os.name);
CREATE INDEX threat_actor_name IF NOT EXISTS FOR (ta:ThreatActor) ON (ta.name);
CREATE INDEX attack_technique_id IF NOT EXISTS FOR (at:AttackTechnique) ON (at.id);
CREATE INDEX software_name IF NOT EXISTS FOR (s:Software) ON (s.name);

// Composite indexes for common query patterns
CREATE INDEX equipment_facility IF NOT EXISTS FOR (e:Equipment) ON (e.facilityId, e.type);
CREATE INDEX cve_severity IF NOT EXISTS FOR (c:CVE) ON (c.severity, c.publishedDate);
```

---

## Question 1: Does this CVE impact my equipment?

### Simple Query - Direct CVE to Equipment
```cypher
// Find all equipment directly affected by a specific CVE
MATCH (cve:CVE {id: $cveId})
MATCH (cve)-[:AFFECTS]->(v:Vulnerability)
MATCH (v)-[:FOUND_IN]->(eq:Equipment)
RETURN
  cve.id AS cveId,
  cve.description AS cveDescription,
  cve.severity AS severity,
  collect(DISTINCT {
    equipmentId: eq.id,
    equipmentName: eq.name,
    equipmentType: eq.type,
    location: eq.location
  }) AS affectedEquipment,
  count(DISTINCT eq) AS totalAffectedCount
```

**Parameters:**
```json
{
  "cveId": "CVE-2023-12345"
}
```

**Expected Output:**
```json
{
  "cveId": "CVE-2023-12345",
  "cveDescription": "Buffer overflow in...",
  "severity": "CRITICAL",
  "affectedEquipment": [
    {
      "equipmentId": "EQ-001",
      "equipmentName": "Web Server 1",
      "equipmentType": "Server",
      "location": "Datacenter-A-Rack-5"
    }
  ],
  "totalAffectedCount": 3
}
```

### Intermediate Query - CVE Impact Through Software/OS
```cypher
// Find equipment affected by CVE through installed software or OS
MATCH (cve:CVE {id: $cveId})
MATCH path = (cve)-[:AFFECTS]->(v:Vulnerability)
  -[:FOUND_IN|RUNS_ON*1..3]->(eq:Equipment)
WITH cve, eq, path,
  [n IN nodes(path) WHERE n:Application OR n:OperatingSystem OR n:Software | n] AS impactedComponents
RETURN
  cve.id AS cveId,
  cve.severity AS severity,
  cve.cvssScore AS cvssScore,
  collect(DISTINCT {
    equipmentId: eq.id,
    equipmentName: eq.name,
    equipmentType: eq.type,
    facilityId: eq.facilityId,
    impactPath: [c IN impactedComponents |
      CASE
        WHEN c:Application THEN 'App: ' + c.name + ' v' + c.version
        WHEN c:OperatingSystem THEN 'OS: ' + c.name + ' ' + c.version
        WHEN c:Software THEN 'Software: ' + c.name + ' v' + c.version
      END
    ]
  }) AS affectedEquipment,
  count(DISTINCT eq) AS totalImpact
ORDER BY cve.cvssScore DESC
```

**Parameters:**
```json
{
  "cveId": "CVE-2023-12345"
}
```

### Advanced Query - Multi-Facility CVE Impact with CWE/CAPEC Context
```cypher
// Comprehensive CVE impact analysis across facilities with weakness and attack pattern context
MATCH (cve:CVE {id: $cveId})

// Get related weaknesses and attack patterns
OPTIONAL MATCH (cve)-[:EXPLOITS]->(cwe:CWE)
OPTIONAL MATCH (cwe)-[:ENABLES]->(capec:CAPEC)

// Find all affected equipment through multiple paths
MATCH path = (cve)-[:AFFECTS]->(v:Vulnerability)
  -[:FOUND_IN|RUNS_ON|INSTALLED_ON*1..4]->(eq:Equipment)

// Get facility information
OPTIONAL MATCH (eq)-[:LOCATED_IN]->(facility:Facility)

// Aggregate results
WITH cve, cwe, capec, eq, facility, path,
  [n IN nodes(path) WHERE n:Application OR n:OperatingSystem OR n:Software | n] AS components

RETURN
  cve.id AS cveId,
  cve.description AS description,
  cve.severity AS severity,
  cve.cvssScore AS cvssScore,
  cve.publishedDate AS publishedDate,

  // Weaknesses exploited
  collect(DISTINCT {
    cweId: cwe.id,
    cweName: cwe.name,
    cweType: cwe.type
  }) AS exploitedWeaknesses,

  // Attack patterns enabled
  collect(DISTINCT {
    capecId: capec.id,
    capecName: capec.name,
    capecLikelihood: capec.likelihood
  }) AS enabledAttackPatterns,

  // Affected equipment grouped by facility
  collect(DISTINCT {
    facility: {
      id: facility.id,
      name: facility.name,
      location: facility.location
    },
    equipment: {
      id: eq.id,
      name: eq.name,
      type: eq.type,
      criticality: eq.criticality
    },
    vulnerableComponents: [c IN components |
      CASE
        WHEN c:Application THEN {type: 'Application', name: c.name, version: c.version}
        WHEN c:OperatingSystem THEN {type: 'OS', name: c.name, version: c.version}
        WHEN c:Software THEN {type: 'Software', name: c.name, version: c.version}
      END
    ],
    pathLength: length(path)
  }) AS impactDetails,

  count(DISTINCT eq) AS totalEquipmentImpacted,
  count(DISTINCT facility) AS totalFacilitiesImpacted
```

---

## Question 2: Is there an attack path to vulnerability?

### Simple Query - Direct Attack Path
```cypher
// Find if there's a direct path from a threat actor to a vulnerability
MATCH (ta:ThreatActor {name: $threatActorName})
MATCH (v:Vulnerability {id: $vulnerabilityId})
MATCH path = shortestPath((ta)-[*1..5]-(v))
WHERE ALL(r IN relationships(path) WHERE
  type(r) IN ['USES', 'EXPLOITS', 'TARGETS', 'ENABLES', 'AFFECTS', 'FOUND_IN'])
RETURN
  EXISTS(path) AS attackPathExists,
  length(path) AS pathLength,
  [n IN nodes(path) | labels(n)[0] + ': ' + coalesce(n.name, n.id)] AS pathNodes
```

**Parameters:**
```json
{
  "threatActorName": "APT28",
  "vulnerabilityId": "VULN-2023-001"
}
```

### Intermediate Query - Attack Path with Techniques
```cypher
// Find attack paths including techniques and software used
MATCH (ta:ThreatActor {name: $threatActorName})
MATCH (v:Vulnerability {id: $vulnerabilityId})

// Find paths through attack techniques and software
MATCH path = (ta)-[:USES]->(at:AttackTechnique)
  -[:EXPLOITS|ENABLES*1..3]->(cwe:CWE)
  -[:ENABLES]->(capec:CAPEC)
  -[:TARGETS]->(v)

RETURN
  ta.name AS threatActor,
  v.id AS vulnerability,
  collect(DISTINCT {
    technique: at.name,
    techniqueId: at.id,
    tactic: at.tactic,
    weakness: cwe.name,
    attackPattern: capec.name,
    likelihood: capec.likelihood
  }) AS attackPaths,
  count(DISTINCT at) AS numberOfTechniques,
  min(length(path)) AS shortestPathLength
ORDER BY shortestPathLength ASC
LIMIT 10
```

**Parameters:**
```json
{
  "threatActorName": "APT28",
  "vulnerabilityId": "VULN-2023-001"
}
```

### Advanced Query - Complete Attack Chain to Equipment
```cypher
// Find complete attack chains from threat actor through techniques to vulnerable equipment
MATCH (ta:ThreatActor)
WHERE ta.name = $threatActorName OR ta.id = $threatActorId

// Find software used by threat actor
OPTIONAL MATCH (ta)-[:USES]->(s:Software)

// Find attack techniques employed
OPTIONAL MATCH (ta)-[:USES]->(at:AttackTechnique)

// Build attack path to vulnerability
MATCH attackPath = (at)-[:EXPLOITS|ENABLES*1..4]->(cwe:CWE)
  -[:ENABLES]->(capec:CAPEC)

// Connect to actual vulnerabilities
MATCH (capec)-[:TARGETS|ENABLES*1..2]->(v:Vulnerability)

// Find affected equipment
MATCH (v)-[:FOUND_IN|RUNS_ON*1..3]->(eq:Equipment)

// Get mitigation information
OPTIONAL MATCH (at)-[:MITIGATED_BY]->(m:Mitigation)

WITH ta, s, at, cwe, capec, v, eq, m, attackPath,
  length(attackPath) AS attackComplexity

RETURN
  // Threat Actor Info
  {
    name: ta.name,
    type: ta.type,
    sophistication: ta.sophistication,
    objectives: ta.objectives
  } AS threatActor,

  // Attack Chain
  collect(DISTINCT {
    software: s.name,
    technique: {
      id: at.id,
      name: at.name,
      tactic: at.tactic,
      platforms: at.platforms
    },
    weakness: {
      id: cwe.id,
      name: cwe.name,
      type: cwe.type
    },
    attackPattern: {
      id: capec.id,
      name: capec.name,
      likelihood: capec.likelihood,
      severity: capec.severity
    },
    complexity: attackComplexity
  }) AS attackChains,

  // Target Vulnerabilities
  collect(DISTINCT {
    vulnerabilityId: v.id,
    description: v.description,
    severity: v.severity
  }) AS targetedVulnerabilities,

  // Affected Equipment
  collect(DISTINCT {
    equipmentId: eq.id,
    equipmentName: eq.name,
    equipmentType: eq.type,
    criticality: eq.criticality,
    facilityId: eq.facilityId
  }) AS vulnerableEquipment,

  // Available Mitigations
  collect(DISTINCT {
    mitigationId: m.id,
    description: m.description,
    effectiveness: m.effectiveness
  }) AS availableMitigations,

  // Metrics
  count(DISTINCT eq) AS totalVulnerableEquipment,
  count(DISTINCT at) AS numberOfTechniques,
  avg(attackComplexity) AS averageAttackComplexity,
  min(attackComplexity) AS shortestAttackPath

ORDER BY shortestAttackPath ASC, totalVulnerableEquipment DESC
```

**Parameters:**
```json
{
  "threatActorName": "APT28",
  "threatActorId": null
}
```

---

## Question 3: Does this new CVE released today impact any equipment in my facility? (with SBOMs)

### Simple Query - Today's CVEs by Facility
```cypher
// Find today's CVEs affecting a specific facility
MATCH (cve:CVE)
WHERE date(cve.publishedDate) = date($today)

MATCH (cve)-[:AFFECTS]->(v:Vulnerability)
  -[:FOUND_IN|RUNS_ON*1..3]->(eq:Equipment)
  -[:LOCATED_IN]->(f:Facility {id: $facilityId})

RETURN
  cve.id AS cveId,
  cve.severity AS severity,
  cve.cvssScore AS cvssScore,
  cve.publishedDate AS publishedDate,
  count(DISTINCT eq) AS affectedEquipmentCount,
  collect(DISTINCT eq.name) AS affectedEquipmentNames
ORDER BY cve.cvssScore DESC
```

**Parameters:**
```json
{
  "today": "2025-11-08",
  "facilityId": "FAC-001"
}
```

### Intermediate Query - Today's CVEs with SBOM Component Matching
```cypher
// Match today's CVEs against facility SBOM components
MATCH (cve:CVE)
WHERE date(cve.publishedDate) = date($today)

// Find vulnerabilities and affected software/applications
MATCH (cve)-[:AFFECTS]->(v:Vulnerability)
MATCH (v)-[:FOUND_IN]->(component)
WHERE component:Application OR component:Software OR component:OperatingSystem

// Match against facility equipment
MATCH (component)-[:INSTALLED_ON|RUNS_ON]->(eq:Equipment)
  -[:LOCATED_IN]->(f:Facility {id: $facilityId})

// Get vendor information
OPTIONAL MATCH (component)-[:MANUFACTURED_BY]->(vendor:Vendor)

RETURN
  cve.id AS cveId,
  cve.description AS description,
  cve.severity AS severity,
  cve.cvssScore AS cvssScore,
  cve.publishedDate AS publishedDate,

  collect(DISTINCT {
    componentType: labels(component)[0],
    componentName: component.name,
    componentVersion: component.version,
    vendor: vendor.name,
    equipmentId: eq.id,
    equipmentName: eq.name,
    equipmentType: eq.type,
    criticality: eq.criticality
  }) AS sbomImpact,

  count(DISTINCT eq) AS totalAffectedEquipment,
  count(DISTINCT component) AS totalAffectedComponents

ORDER BY cve.cvssScore DESC, totalAffectedEquipment DESC
```

**Parameters:**
```json
{
  "today": "2025-11-08",
  "facilityId": "FAC-001"
}
```

### Advanced Query - Multi-Facility Today's CVE Impact with Complete SBOM Analysis
```cypher
// Comprehensive analysis of today's CVEs across all or specific facilities with full SBOM correlation
MATCH (cve:CVE)
WHERE date(cve.publishedDate) = date($today)
  AND ($minSeverity IS NULL OR cve.severity IN $minSeverity)

// Get CWE and CAPEC context
OPTIONAL MATCH (cve)-[:EXPLOITS]->(cwe:CWE)
OPTIONAL MATCH (cwe)-[:ENABLES]->(capec:CAPEC)

// Find affected components (SBOM items)
MATCH (cve)-[:AFFECTS]->(v:Vulnerability)
MATCH (v)-[:FOUND_IN]->(component)
WHERE component:Application OR component:Software OR component:OperatingSystem

// Match to equipment and facilities
MATCH (component)-[:INSTALLED_ON|RUNS_ON]->(eq:Equipment)
  -[:LOCATED_IN]->(f:Facility)
WHERE $facilityIds IS NULL OR f.id IN $facilityIds

// Get vendor and version details
OPTIONAL MATCH (component)-[:MANUFACTURED_BY]->(vendor:Vendor)

// Get potential mitigations
OPTIONAL MATCH (cve)-[:MITIGATED_BY]->(mitigation:Mitigation)

// Aggregate SBOM components per equipment
WITH cve, cwe, capec, v, component, vendor, eq, f, mitigation,
  [(eq)-[:RUNS|INSTALLS*1..2]->(sbomItem)
   WHERE sbomItem:Application OR sbomItem:Software OR sbomItem:OperatingSystem |
   {
     type: labels(sbomItem)[0],
     name: sbomItem.name,
     version: sbomItem.version,
     vulnerable: EXISTS((v)-[:FOUND_IN]->(sbomItem))
   }
  ] AS fullSBOM

RETURN
  // CVE Details
  {
    id: cve.id,
    description: cve.description,
    severity: cve.severity,
    cvssScore: cve.cvssScore,
    publishedDate: cve.publishedDate,
    lastModified: cve.lastModifiedDate
  } AS cveDetails,

  // Weakness and Attack Context
  collect(DISTINCT {
    cweId: cwe.id,
    cweName: cwe.name,
    cweDescription: cwe.description,
    associatedAttackPatterns: [(cwe)-[:ENABLES]->(cap:CAPEC) |
      {id: cap.id, name: cap.name, likelihood: cap.likelihood}
    ]
  }) AS weaknessContext,

  // Facility Impact Summary
  collect(DISTINCT {
    facilityId: f.id,
    facilityName: f.name,
    facilityLocation: f.location,
    criticalityLevel: f.criticality,
    equipmentCount: count(DISTINCT eq)
  }) AS facilityImpact,

  // Detailed Equipment and SBOM Impact
  collect(DISTINCT {
    equipment: {
      id: eq.id,
      name: eq.name,
      type: eq.type,
      criticality: eq.criticality,
      facilityId: f.id
    },
    vulnerableComponent: {
      type: labels(component)[0],
      name: component.name,
      version: component.version,
      vendor: vendor.name,
      endOfLife: component.endOfLife
    },
    completeSBOM: fullSBOM,
    vulnerabilityDetails: {
      id: v.id,
      description: v.description,
      exploitable: v.exploitable
    }
  }) AS detailedImpact,

  // Mitigation Options
  collect(DISTINCT {
    mitigationId: mitigation.id,
    description: mitigation.description,
    type: mitigation.type,
    effectiveness: mitigation.effectiveness
  }) AS availableMitigations,

  // Summary Metrics
  count(DISTINCT f) AS totalFacilitiesAffected,
  count(DISTINCT eq) AS totalEquipmentAffected,
  count(DISTINCT component) AS totalSBOMComponentsAffected,
  avg(cve.cvssScore) AS avgCVSSScore

ORDER BY cve.cvssScore DESC, totalEquipmentAffected DESC
```

**Parameters:**
```json
{
  "today": "2025-11-08",
  "facilityIds": ["FAC-001", "FAC-002"],
  "minSeverity": ["CRITICAL", "HIGH"]
}
```

**Expected Output:**
```json
{
  "cveDetails": {
    "id": "CVE-2025-54321",
    "description": "Remote code execution in...",
    "severity": "CRITICAL",
    "cvssScore": 9.8,
    "publishedDate": "2025-11-08T00:00:00Z"
  },
  "facilityImpact": [
    {
      "facilityId": "FAC-001",
      "facilityName": "Data Center East",
      "equipmentCount": 15
    }
  ],
  "detailedImpact": [
    {
      "equipment": {
        "id": "EQ-WEB-001",
        "name": "Production Web Server",
        "type": "Server",
        "criticality": "HIGH"
      },
      "vulnerableComponent": {
        "type": "Application",
        "name": "Apache HTTP Server",
        "version": "2.4.51",
        "vendor": "Apache Software Foundation"
      },
      "completeSBOM": [
        {"type": "Application", "name": "Apache HTTP Server", "version": "2.4.51", "vulnerable": true},
        {"type": "OperatingSystem", "name": "Ubuntu", "version": "20.04", "vulnerable": false},
        {"type": "Software", "name": "OpenSSL", "version": "1.1.1", "vulnerable": false}
      ]
    }
  ],
  "totalEquipmentAffected": 15,
  "totalSBOMComponentsAffected": 3
}
```

---

## Question 4: Is there a pathway for a threat actor to get to the vulnerability to exploit it?

### Simple Query - Threat Actor to Vulnerability Path Check
```cypher
// Check if threat actor has path to specific vulnerability
MATCH (ta:ThreatActor {name: $threatActorName})
MATCH (v:Vulnerability {id: $vulnerabilityId})
MATCH path = shortestPath((ta)-[*1..6]-(v))
RETURN
  EXISTS(path) AS pathwayExists,
  length(path) AS pathwayLength,
  [rel IN relationships(path) | type(rel)] AS relationshipChain,
  [n IN nodes(path) | {
    type: labels(n)[0],
    id: coalesce(n.id, n.name),
    name: n.name
  }] AS pathwayNodes
```

**Parameters:**
```json
{
  "threatActorName": "APT29",
  "vulnerabilityId": "VULN-2023-456"
}
```

### Intermediate Query - Multi-Path Analysis with Access Requirements
```cypher
// Find all possible pathways from threat actor to vulnerability with access analysis
MATCH (ta:ThreatActor)
WHERE ta.name = $threatActorName OR ta.id = $threatActorId

MATCH (v:Vulnerability {id: $vulnerabilityId})

// Find multiple paths (limit for performance)
MATCH paths = allShortestPaths((ta)-[*1..7]-(v))
WHERE ALL(r IN relationships(paths) WHERE
  type(r) IN ['USES', 'EXPLOITS', 'TARGETS', 'ENABLES', 'AFFECTS', 'FOUND_IN', 'RUNS_ON'])

WITH ta, v, paths,
  [n IN nodes(paths) WHERE n:AttackTechnique] AS techniques,
  [n IN nodes(paths) WHERE n:Software] AS software,
  [n IN nodes(paths) WHERE n:CWE] AS weaknesses,
  [n IN nodes(paths) WHERE n:CAPEC] AS attackPatterns,
  [n IN nodes(paths) WHERE n:Equipment] AS targetEquipment

RETURN
  ta.name AS threatActor,
  ta.sophistication AS actorSophistication,
  v.id AS targetVulnerability,
  v.exploitable AS isExploitable,

  collect(DISTINCT {
    pathLength: length(paths),
    requiredTechniques: [t IN techniques | {id: t.id, name: t.name, complexity: t.complexity}],
    requiredSoftware: [s IN software | {name: s.name, type: s.type}],
    exploitedWeaknesses: [w IN weaknesses | {id: w.id, name: w.name}],
    attackPatterns: [ap IN attackPatterns | {id: ap.id, name: ap.name, likelihood: ap.likelihood}],
    targetEquipment: [eq IN targetEquipment | {id: eq.id, name: eq.name, accessible: eq.networkAccessible}]
  }) AS exploitationPathways,

  count(paths) AS totalPathways,
  min(length(paths)) AS shortestPathLength,
  avg(length(paths)) AS avgPathLength

ORDER BY shortestPathLength ASC
```

**Parameters:**
```json
{
  "threatActorName": "APT29",
  "threatActorId": null,
  "vulnerabilityId": "VULN-2023-456"
}
```

### Advanced Query - Complete Threat Path with Equipment Access and Defenses
```cypher
// Comprehensive threat pathway analysis including network access, defenses, and exploitation feasibility
MATCH (ta:ThreatActor)
WHERE ta.name = $threatActorName OR ta.id = $threatActorId

// Find target vulnerability
MATCH (v:Vulnerability)
WHERE v.id = $vulnerabilityId OR v.cveId = $cveId

// Build complete attack graph
MATCH attackGraph = (ta)-[:USES]->(at:AttackTechnique)
  -[:EXPLOITS|ENABLES*1..4]->(cwe:CWE)
  -[:ENABLES]->(capec:CAPEC)

// Connect to vulnerability
MATCH (capec)-[:TARGETS|ENABLES*1..2]->(v)

// Find vulnerable equipment
MATCH (v)-[:FOUND_IN|RUNS_ON*1..3]->(eq:Equipment)

// Get facility and network context
OPTIONAL MATCH (eq)-[:LOCATED_IN]->(facility:Facility)
OPTIONAL MATCH (eq)-[:CONNECTED_TO]->(network)

// Get defensive controls
OPTIONAL MATCH (at)-[:MITIGATED_BY]->(mitigation:Mitigation)
OPTIONAL MATCH (eq)-[:PROTECTED_BY]->(defense)

// Get data sources for detection
OPTIONAL MATCH (at)-[:DETECTED_BY]->(ds:DataSource)

WITH ta, at, cwe, capec, v, eq, facility, network, mitigation, defense, ds, attackGraph,
  // Calculate attack complexity score
  CASE
    WHEN at.complexity = 'LOW' THEN 1
    WHEN at.complexity = 'MEDIUM' THEN 2
    ELSE 3
  END AS techniqueComplexity,

  // Calculate likelihood score
  CASE
    WHEN capec.likelihood = 'HIGH' THEN 3
    WHEN capec.likelihood = 'MEDIUM' THEN 2
    ELSE 1
  END AS attackLikelihood,

  // Check equipment accessibility
  CASE
    WHEN eq.networkAccessible = true THEN 'EXTERNAL'
    WHEN eq.networkAccessible = false THEN 'INTERNAL'
    ELSE 'UNKNOWN'
  END AS accessLevel

RETURN
  // Threat Actor Profile
  {
    name: ta.name,
    type: ta.type,
    sophistication: ta.sophistication,
    objectives: ta.objectives,
    knownSince: ta.firstSeen
  } AS threatActorProfile,

  // Target Vulnerability
  {
    id: v.id,
    cveId: v.cveId,
    description: v.description,
    severity: v.severity,
    exploitable: v.exploitable,
    exploitAvailable: v.exploitPublic
  } AS targetVulnerability,

  // Attack Pathways
  collect(DISTINCT {
    pathComplexity: techniqueComplexity,
    pathLikelihood: attackLikelihood,

    technique: {
      id: at.id,
      name: at.name,
      tactic: at.tactic,
      platforms: at.platforms,
      requiresPrivileges: at.permissionsRequired,
      userInteraction: at.userInteractionRequired
    },

    weakness: {
      id: cwe.id,
      name: cwe.name,
      prevalence: cwe.prevalence,
      exploitability: cwe.exploitability
    },

    attackPattern: {
      id: capec.id,
      name: capec.name,
      prerequisites: capec.prerequisites,
      skillsRequired: capec.skillsRequired,
      likelihood: capec.likelihood
    },

    targetAsset: {
      equipmentId: eq.id,
      equipmentName: eq.name,
      equipmentType: eq.type,
      criticality: eq.criticality,
      accessLevel: accessLevel,
      facility: {
        id: facility.id,
        name: facility.name,
        securityZone: facility.securityZone
      }
    },

    defensiveControls: {
      mitigations: [(at)-[:MITIGATED_BY]->(m:Mitigation) |
        {id: m.id, description: m.description, effectiveness: m.effectiveness}
      ],
      assetProtections: [(eq)-[:PROTECTED_BY]->(p) |
        {type: labels(p)[0], description: p.description}
      ],
      detectionMethods: [(at)-[:DETECTED_BY]->(d:DataSource) |
        {source: d.name, coverage: d.coverage}
      ]
    },

    feasibilityScore: (techniqueComplexity + attackLikelihood) / 2.0

  }) AS exploitationPathways,

  // Pathway Existence Assessment
  CASE
    WHEN count(at) > 0 THEN true
    ELSE false
  END AS pathwayExists,

  // Risk Metrics
  {
    totalPathways: count(DISTINCT at),
    avgComplexity: avg(techniqueComplexity),
    avgLikelihood: avg(attackLikelihood),
    criticalAssetsAtRisk: count(DISTINCT CASE WHEN eq.criticality = 'CRITICAL' THEN eq END),
    facilitiesAtRisk: count(DISTINCT facility),
    externallyAccessible: count(CASE WHEN eq.networkAccessible = true THEN 1 END),
    mitigationsAvailable: count(DISTINCT mitigation),
    detectionsAvailable: count(DISTINCT ds)
  } AS riskAssessment,

  // Overall Threat Level
  CASE
    WHEN avg(attackLikelihood) >= 2.5 AND avg(techniqueComplexity) <= 1.5 AND v.exploitable = true THEN 'CRITICAL'
    WHEN avg(attackLikelihood) >= 2 AND avg(techniqueComplexity) <= 2 THEN 'HIGH'
    WHEN avg(attackLikelihood) >= 1.5 OR avg(techniqueComplexity) <= 2.5 THEN 'MEDIUM'
    ELSE 'LOW'
  END AS overallThreatLevel

ORDER BY overallThreatLevel DESC, riskAssessment.criticalAssetsAtRisk DESC
```

**Parameters:**
```json
{
  "threatActorName": "APT29",
  "threatActorId": null,
  "vulnerabilityId": "VULN-2023-456",
  "cveId": null
}
```

**Expected Output:**
```json
{
  "threatActorProfile": {
    "name": "APT29",
    "type": "Nation State",
    "sophistication": "ADVANCED",
    "objectives": ["Espionage", "Data Theft"]
  },
  "pathwayExists": true,
  "exploitationPathways": [
    {
      "pathComplexity": 2,
      "pathLikelihood": 3,
      "technique": {
        "id": "T1190",
        "name": "Exploit Public-Facing Application",
        "tactic": "Initial Access",
        "requiresPrivileges": "None"
      },
      "targetAsset": {
        "equipmentId": "EQ-WEB-001",
        "accessLevel": "EXTERNAL",
        "criticality": "CRITICAL"
      },
      "defensiveControls": {
        "mitigations": [
          {"description": "Application Isolation", "effectiveness": 0.7}
        ],
        "detectionMethods": [
          {"source": "Network Traffic", "coverage": 0.8}
        ]
      },
      "feasibilityScore": 2.5
    }
  ],
  "riskAssessment": {
    "totalPathways": 3,
    "criticalAssetsAtRisk": 2,
    "externallyAccessible": 1,
    "mitigationsAvailable": 2
  },
  "overallThreatLevel": "HIGH"
}
```

---

## Question 5: For this CVE released today, is there a pathway for threat actor to get to vulnerability?

### Simple Query - Today's CVE Threat Actor Pathway
```cypher
// Check if threat actors have pathways to today's CVEs
MATCH (cve:CVE)
WHERE date(cve.publishedDate) = date($today)

MATCH (cve)-[:AFFECTS]->(v:Vulnerability)

// Find any threat actors with paths to this vulnerability
OPTIONAL MATCH path = shortestPath((ta:ThreatActor)-[*1..6]-(v))

RETURN
  cve.id AS cveId,
  cve.severity AS severity,
  cve.cvssScore AS cvssScore,
  v.id AS vulnerabilityId,

  CASE
    WHEN ta IS NOT NULL THEN true
    ELSE false
  END AS threatActorPathwayExists,

  collect(DISTINCT {
    actorName: ta.name,
    actorType: ta.type,
    pathLength: length(path)
  }) AS threateningActors,

  count(DISTINCT ta) AS numberOfThreats

ORDER BY cve.cvssScore DESC, numberOfThreats DESC
```

**Parameters:**
```json
{
  "today": "2025-11-08"
}
```

### Intermediate Query - Today's CVEs with Active Threat Actor Campaigns
```cypher
// Identify today's CVEs with active threat actor exploitation pathways
MATCH (cve:CVE)
WHERE date(cve.publishedDate) = date($today)
  AND cve.severity IN ['CRITICAL', 'HIGH']

MATCH (cve)-[:EXPLOITS]->(cwe:CWE)
MATCH (cwe)-[:ENABLES]->(capec:CAPEC)
MATCH (cve)-[:AFFECTS]->(v:Vulnerability)

// Find threat actors using techniques that exploit these weaknesses
MATCH (ta:ThreatActor)-[:USES]->(at:AttackTechnique)
  -[:EXPLOITS]->(cwe)

// Check if vulnerability is in equipment
OPTIONAL MATCH (v)-[:FOUND_IN|RUNS_ON*1..3]->(eq:Equipment)

RETURN
  cve.id AS cveId,
  cve.description AS cveDescription,
  cve.severity AS severity,
  cve.cvssScore AS cvssScore,
  cve.publishedDate AS releasedToday,

  collect(DISTINCT {
    threatActor: ta.name,
    actorType: ta.type,
    sophistication: ta.sophistication,
    activeCampaigns: ta.activeCampaigns,
    techniques: collect(DISTINCT {
      techniqueId: at.id,
      techniqueName: at.name,
      tactic: at.tactic
    }),
    exploitedWeakness: {
      cweId: cwe.id,
      cweName: cwe.name,
      exploitability: cwe.exploitability
    },
    attackPattern: {
      capecId: capec.id,
      capecName: capec.name,
      likelihood: capec.likelihood
    }
  }) AS activeThreatActors,

  count(DISTINCT eq) AS vulnerableEquipmentCount,
  count(DISTINCT ta) AS numberOfActiveThreatActors,

  // Risk indicator
  CASE
    WHEN count(DISTINCT ta) > 0 AND cve.severity = 'CRITICAL' THEN 'IMMEDIATE ACTION REQUIRED'
    WHEN count(DISTINCT ta) > 0 AND cve.severity = 'HIGH' THEN 'HIGH PRIORITY'
    WHEN count(DISTINCT ta) > 0 THEN 'MONITOR'
    ELSE 'LOW RISK'
  END AS riskLevel

ORDER BY numberOfActiveThreatActors DESC, cve.cvssScore DESC
```

**Parameters:**
```json
{
  "today": "2025-11-08"
}
```

### Advanced Query - Today's CVE Complete Threat Landscape Analysis
```cypher
// Comprehensive analysis of today's CVEs with complete threat actor exploitation pathways and asset impact
MATCH (cve:CVE)
WHERE date(cve.publishedDate) = date($today)
  AND ($severityFilter IS NULL OR cve.severity IN $severityFilter)
  AND ($minCVSS IS NULL OR cve.cvssScore >= $minCVSS)

// Get vulnerability and weakness context
MATCH (cve)-[:AFFECTS]->(v:Vulnerability)
OPTIONAL MATCH (cve)-[:EXPLOITS]->(cwe:CWE)
OPTIONAL MATCH (cwe)-[:ENABLES]->(capec:CAPEC)

// Find ALL threat actors with techniques that could exploit these weaknesses
OPTIONAL MATCH threatPath = (ta:ThreatActor)-[:USES]->(at:AttackTechnique)
  -[:EXPLOITS*1..3]->(cwe)

// Find software used by threat actors
OPTIONAL MATCH (ta)-[:USES]->(malware:Software)
WHERE malware.type = 'MALWARE'

// Find vulnerable equipment and facilities
OPTIONAL MATCH assetPath = (v)-[:FOUND_IN|RUNS_ON|INSTALLED_ON*1..4]->(eq:Equipment)
  -[:LOCATED_IN]->(facility:Facility)

// Get available mitigations and detections
OPTIONAL MATCH (at)-[:MITIGATED_BY]->(mitigation:Mitigation)
OPTIONAL MATCH (at)-[:DETECTED_BY]->(dataSource:DataSource)

// Get related CVEs (same CWE)
OPTIONAL MATCH (cwe)<-[:EXPLOITS]-(relatedCVE:CVE)
WHERE relatedCVE.id <> cve.id

WITH cve, v, cwe, capec, ta, at, malware, eq, facility, mitigation, dataSource, relatedCVE,
  threatPath, assetPath,

  // Calculate threat capability score
  CASE
    WHEN ta.sophistication = 'ADVANCED' THEN 3
    WHEN ta.sophistication = 'INTERMEDIATE' THEN 2
    ELSE 1
  END AS threatCapability,

  // Calculate attack feasibility
  CASE
    WHEN capec.likelihood = 'HIGH' AND at.complexity = 'LOW' THEN 3
    WHEN capec.likelihood = 'MEDIUM' OR at.complexity = 'MEDIUM' THEN 2
    ELSE 1
  END AS attackFeasibility,

  // Calculate asset criticality
  CASE
    WHEN eq.criticality = 'CRITICAL' THEN 3
    WHEN eq.criticality = 'HIGH' THEN 2
    ELSE 1
  END AS assetCriticality

RETURN
  // CVE Information
  {
    id: cve.id,
    description: cve.description,
    severity: cve.severity,
    cvssScore: cve.cvssScore,
    publishedDate: cve.publishedDate,
    exploitAvailable: cve.exploitPublic,
    references: cve.references
  } AS cveDetails,

  // Vulnerability Context
  {
    id: v.id,
    description: v.description,
    exploitable: v.exploitable,
    patchAvailable: v.patchAvailable,
    patchDate: v.patchDate
  } AS vulnerabilityDetails,

  // Weakness and Attack Pattern Context
  collect(DISTINCT {
    weakness: {
      id: cwe.id,
      name: cwe.name,
      description: cwe.description,
      prevalence: cwe.prevalence,
      exploitability: cwe.exploitability
    },
    attackPatterns: [(cwe)-[:ENABLES]->(cap:CAPEC) | {
      id: cap.id,
      name: cap.name,
      likelihood: cap.likelihood,
      severity: cap.severity,
      prerequisites: cap.prerequisites,
      skillsRequired: cap.skillsRequired
    }],
    relatedCVEs: count(DISTINCT relatedCVE)
  }) AS weaknessContext,

  // Threat Actor Analysis
  collect(DISTINCT {
    actor: {
      name: ta.name,
      type: ta.type,
      sophistication: ta.sophistication,
      objectives: ta.objectives,
      activeCampaigns: ta.activeCampaigns,
      targetedSectors: ta.targetedSectors
    },
    capabilities: {
      techniques: collect(DISTINCT {
        id: at.id,
        name: at.name,
        tactic: at.tactic,
        complexity: at.complexity,
        platforms: at.platforms,
        requiresPrivileges: at.permissionsRequired
      }),
      malware: collect(DISTINCT {
        name: malware.name,
        type: malware.type,
        description: malware.description
      }),
      threatCapabilityScore: threatCapability
    },
    exploitationPathway: {
      pathExists: threatPath IS NOT NULL,
      pathLength: length(threatPath),
      feasibilityScore: attackFeasibility,
      estimatedTimeToExploit: CASE
        WHEN attackFeasibility = 3 THEN '< 1 day'
        WHEN attackFeasibility = 2 THEN '1-7 days'
        ELSE '> 7 days'
      END
    }
  }) AS threatActorAnalysis,

  // Asset Impact Assessment
  collect(DISTINCT {
    equipment: {
      id: eq.id,
      name: eq.name,
      type: eq.type,
      criticality: eq.criticality,
      networkAccessible: eq.networkAccessible,
      assetCriticalityScore: assetCriticality
    },
    facility: {
      id: facility.id,
      name: facility.name,
      location: facility.location,
      securityZone: facility.securityZone,
      criticality: facility.criticality
    },
    exploitPath: {
      pathLength: length(assetPath),
      pathNodes: [n IN nodes(assetPath) WHERE n <> v AND n <> eq |
        {type: labels(n)[0], name: coalesce(n.name, n.id)}
      ]
    }
  }) AS assetImpactAssessment,

  // Defensive Posture
  {
    availableMitigations: collect(DISTINCT {
      id: mitigation.id,
      description: mitigation.description,
      type: mitigation.type,
      effectiveness: mitigation.effectiveness,
      implementationCost: mitigation.implementationCost
    }),

    detectionCapabilities: collect(DISTINCT {
      dataSource: dataSource.name,
      dataComponent: dataSource.component,
      coverage: dataSource.coverage,
      detectsActivity: dataSource.detectsActivity
    }),

    patchingStatus: CASE
      WHEN v.patchAvailable = true THEN 'PATCH AVAILABLE'
      WHEN v.patchAvailable = false THEN 'NO PATCH'
      ELSE 'UNKNOWN'
    END,

    mitigationCount: count(DISTINCT mitigation),
    detectionCount: count(DISTINCT dataSource)
  } AS defensivePosture,

  // Risk Calculations
  {
    pathwayExists: CASE WHEN count(ta) > 0 THEN true ELSE false END,
    numberOfThreatActors: count(DISTINCT ta),
    numberOfTechniques: count(DISTINCT at),
    vulnerableAssets: count(DISTINCT eq),
    criticalAssetsAtRisk: count(DISTINCT CASE WHEN eq.criticality = 'CRITICAL' THEN eq END),
    facilitiesAtRisk: count(DISTINCT facility),
    externallyAccessibleAssets: count(DISTINCT CASE WHEN eq.networkAccessible = true THEN 1 END),

    avgThreatCapability: avg(threatCapability),
    avgAttackFeasibility: avg(attackFeasibility),
    avgAssetCriticality: avg(assetCriticality),

    compositeRiskScore: (
      avg(threatCapability) * 0.3 +
      avg(attackFeasibility) * 0.4 +
      avg(assetCriticality) * 0.3
    ),

    riskLevel: CASE
      WHEN count(ta) > 0 AND cve.severity = 'CRITICAL' AND avg(attackFeasibility) >= 2.5 THEN 'CRITICAL'
      WHEN count(ta) > 0 AND cve.severity IN ['CRITICAL', 'HIGH'] THEN 'HIGH'
      WHEN count(ta) > 0 THEN 'MEDIUM'
      ELSE 'LOW'
    END,

    recommendedAction: CASE
      WHEN count(ta) > 0 AND cve.severity = 'CRITICAL' AND avg(attackFeasibility) >= 2.5
        THEN 'IMMEDIATE PATCHING/MITIGATION REQUIRED'
      WHEN count(ta) > 0 AND cve.severity IN ['CRITICAL', 'HIGH']
        THEN 'URGENT: PATCH WITHIN 24-48 HOURS'
      WHEN count(ta) > 0
        THEN 'MONITOR AND PLAN REMEDIATION'
      ELSE 'STANDARD PATCHING SCHEDULE'
    END
  } AS riskAssessment,

  // Temporal Context
  duration.between(
    date(cve.publishedDate),
    date()
  ).hours AS hoursSinceRelease

ORDER BY
  riskAssessment.compositeRiskScore DESC,
  cve.cvssScore DESC,
  riskAssessment.criticalAssetsAtRisk DESC
```

**Parameters:**
```json
{
  "today": "2025-11-08",
  "severityFilter": ["CRITICAL", "HIGH"],
  "minCVSS": 7.0
}
```

**Expected Output:**
```json
{
  "cveDetails": {
    "id": "CVE-2025-11111",
    "severity": "CRITICAL",
    "cvssScore": 9.8,
    "publishedDate": "2025-11-08T00:00:00Z",
    "exploitAvailable": false
  },
  "threatActorAnalysis": [
    {
      "actor": {
        "name": "APT29",
        "type": "Nation State",
        "sophistication": "ADVANCED",
        "activeCampaigns": true
      },
      "exploitationPathway": {
        "pathExists": true,
        "pathLength": 4,
        "feasibilityScore": 3,
        "estimatedTimeToExploit": "< 1 day"
      }
    }
  ],
  "assetImpactAssessment": [
    {
      "equipment": {
        "id": "EQ-WEB-001",
        "name": "Production Web Server",
        "criticality": "CRITICAL",
        "networkAccessible": true
      },
      "facility": {
        "id": "FAC-001",
        "name": "Primary Data Center"
      }
    }
  ],
  "riskAssessment": {
    "pathwayExists": true,
    "numberOfThreatActors": 2,
    "criticalAssetsAtRisk": 3,
    "compositeRiskScore": 2.8,
    "riskLevel": "CRITICAL",
    "recommendedAction": "IMMEDIATE PATCHING/MITIGATION REQUIRED"
  },
  "hoursSinceRelease": 6
}
```

---

## Question 6: How many pieces of a type of equipment do I have?

### Simple Query - Equipment Count by Type
```cypher
// Count equipment by type
MATCH (eq:Equipment)
WHERE eq.type = $equipmentType
RETURN
  eq.type AS equipmentType,
  count(eq) AS totalCount,
  collect(eq.name) AS equipmentNames
```

**Parameters:**
```json
{
  "equipmentType": "Server"
}
```

### Intermediate Query - Equipment Inventory with Facility Breakdown
```cypher
// Equipment count by type with facility and status breakdown
MATCH (eq:Equipment)
WHERE $equipmentType IS NULL OR eq.type = $equipmentType

OPTIONAL MATCH (eq)-[:LOCATED_IN]->(f:Facility)

RETURN
  eq.type AS equipmentType,
  count(eq) AS totalCount,

  collect(DISTINCT {
    facilityId: f.id,
    facilityName: f.name,
    facilityLocation: f.location,
    equipmentInFacility: count(eq)
  }) AS facilityBreakdown,

  collect(DISTINCT {
    status: eq.status,
    count: count(eq)
  }) AS statusBreakdown,

  collect(DISTINCT {
    criticality: eq.criticality,
    count: count(eq)
  }) AS criticalityBreakdown

ORDER BY totalCount DESC
```

**Parameters:**
```json
{
  "equipmentType": "Server"
}
```

### Advanced Query - Comprehensive Equipment Inventory Analysis
```cypher
// Complete equipment inventory with vulnerabilities, applications, and maintenance status
MATCH (eq:Equipment)
WHERE $equipmentType IS NULL OR eq.type = $equipmentType
  AND ($facilityId IS NULL OR EXISTS((eq)-[:LOCATED_IN]->(:Facility {id: $facilityId})))
  AND ($criticalityLevel IS NULL OR eq.criticality = $criticalityLevel)

// Get facility information
OPTIONAL MATCH (eq)-[:LOCATED_IN]->(f:Facility)

// Get installed software and applications
OPTIONAL MATCH (eq)<-[:INSTALLED_ON|RUNS_ON]-(software)
WHERE software:Application OR software:OperatingSystem OR software:Software

// Get vendor information
OPTIONAL MATCH (eq)-[:MANUFACTURED_BY]->(vendor:Vendor)

// Get vulnerabilities
OPTIONAL MATCH (eq)<-[:FOUND_IN|RUNS_ON*1..3]-(v:Vulnerability)
OPTIONAL MATCH (v)<-[:AFFECTS]-(cve:CVE)

// Aggregate by equipment type
WITH eq.type AS equipmentType,
  eq, f, vendor, software, v, cve,

  // Calculate age
  duration.between(date(eq.installDate), date()).days AS ageInDays,

  // Determine maintenance status
  CASE
    WHEN date(eq.lastMaintenanceDate) < date() - duration({days: 90}) THEN 'OVERDUE'
    WHEN date(eq.lastMaintenanceDate) < date() - duration({days: 30}) THEN 'DUE_SOON'
    ELSE 'CURRENT'
  END AS maintenanceStatus

RETURN
  equipmentType,
  count(DISTINCT eq) AS totalCount,

  // Summary Statistics
  {
    avgAge: avg(ageInDays),
    oldestEquipment: max(ageInDays),
    newestEquipment: min(ageInDays)
  } AS ageStatistics,

  // Facility Distribution
  collect(DISTINCT {
    facilityId: f.id,
    facilityName: f.name,
    location: f.location,
    count: count(DISTINCT eq)
  }) AS facilityDistribution,

  // Status Breakdown
  {
    operational: count(DISTINCT CASE WHEN eq.status = 'OPERATIONAL' THEN eq END),
    maintenance: count(DISTINCT CASE WHEN eq.status = 'MAINTENANCE' THEN eq END),
    decommissioned: count(DISTINCT CASE WHEN eq.status = 'DECOMMISSIONED' THEN eq END),
    offline: count(DISTINCT CASE WHEN eq.status = 'OFFLINE' THEN eq END)
  } AS statusBreakdown,

  // Criticality Breakdown
  {
    critical: count(DISTINCT CASE WHEN eq.criticality = 'CRITICAL' THEN eq END),
    high: count(DISTINCT CASE WHEN eq.criticality = 'HIGH' THEN eq END),
    medium: count(DISTINCT CASE WHEN eq.criticality = 'MEDIUM' THEN eq END),
    low: count(DISTINCT CASE WHEN eq.criticality = 'LOW' THEN eq END)
  } AS criticalityBreakdown,

  // Vendor Distribution
  collect(DISTINCT {
    vendor: vendor.name,
    count: count(DISTINCT eq),
    models: collect(DISTINCT eq.model)
  }) AS vendorDistribution,

  // Software Inventory
  {
    totalApplications: count(DISTINCT CASE WHEN software:Application THEN software END),
    totalOS: count(DISTINCT CASE WHEN software:OperatingSystem THEN software END),
    totalSoftware: count(DISTINCT CASE WHEN software:Software THEN software END),
    softwareList: collect(DISTINCT {
      type: labels(software)[0],
      name: software.name,
      version: software.version,
      equipmentCount: count(DISTINCT eq)
    })
  } AS softwareInventory,

  // Vulnerability Assessment
  {
    totalVulnerabilities: count(DISTINCT v),
    criticalVulnerabilities: count(DISTINCT CASE WHEN cve.severity = 'CRITICAL' THEN v END),
    highVulnerabilities: count(DISTINCT CASE WHEN cve.severity = 'HIGH' THEN v END),
    equipmentWithVulnerabilities: count(DISTINCT CASE WHEN v IS NOT NULL THEN eq END),
    vulnerabilityRate: CASE
      WHEN count(DISTINCT eq) > 0
      THEN toFloat(count(DISTINCT CASE WHEN v IS NOT NULL THEN eq END)) / count(DISTINCT eq)
      ELSE 0.0
    END
  } AS vulnerabilityAssessment,

  // Maintenance Status
  {
    current: count(DISTINCT CASE WHEN maintenanceStatus = 'CURRENT' THEN eq END),
    dueSoon: count(DISTINCT CASE WHEN maintenanceStatus = 'DUE_SOON' THEN eq END),
    overdue: count(DISTINCT CASE WHEN maintenanceStatus = 'OVERDUE' THEN eq END)
  } AS maintenanceStatusBreakdown,

  // Network Accessibility
  {
    externallyAccessible: count(DISTINCT CASE WHEN eq.networkAccessible = true THEN eq END),
    internalOnly: count(DISTINCT CASE WHEN eq.networkAccessible = false THEN eq END),
    unknown: count(DISTINCT CASE WHEN eq.networkAccessible IS NULL THEN eq END)
  } AS networkAccessibility,

  // Detailed Equipment List (optional, can be large)
  collect(DISTINCT {
    equipmentId: eq.id,
    name: eq.name,
    model: eq.model,
    serialNumber: eq.serialNumber,
    status: eq.status,
    criticality: eq.criticality,
    facilityId: f.id,
    facilityName: f.name,
    vendor: vendor.name,
    installDate: eq.installDate,
    ageInDays: ageInDays,
    maintenanceStatus: maintenanceStatus,
    lastMaintenance: eq.lastMaintenanceDate,
    vulnerabilityCount: count(DISTINCT v),
    criticalVulnerabilities: count(DISTINCT CASE WHEN cve.severity = 'CRITICAL' THEN v END)
  }) AS detailedInventory

ORDER BY totalCount DESC
```

**Parameters:**
```json
{
  "equipmentType": "Server",
  "facilityId": null,
  "criticalityLevel": null
}
```

**Expected Output:**
```json
{
  "equipmentType": "Server",
  "totalCount": 45,
  "ageStatistics": {
    "avgAge": 730,
    "oldestEquipment": 1825,
    "newestEquipment": 30
  },
  "facilityDistribution": [
    {
      "facilityId": "FAC-001",
      "facilityName": "Primary Data Center",
      "location": "New York, NY",
      "count": 30
    },
    {
      "facilityId": "FAC-002",
      "facilityName": "Backup Data Center",
      "count": 15
    }
  ],
  "statusBreakdown": {
    "operational": 42,
    "maintenance": 2,
    "decommissioned": 0,
    "offline": 1
  },
  "criticalityBreakdown": {
    "critical": 15,
    "high": 20,
    "medium": 8,
    "low": 2
  },
  "vulnerabilityAssessment": {
    "totalVulnerabilities": 127,
    "criticalVulnerabilities": 12,
    "equipmentWithVulnerabilities": 38,
    "vulnerabilityRate": 0.844
  },
  "maintenanceStatusBreakdown": {
    "current": 30,
    "dueSoon": 10,
    "overdue": 5
  }
}
```

---

## Question 7: Do I have a specific application or operating system?

### Simple Query - Check Application/OS Existence
```cypher
// Check if specific application or OS exists
MATCH (software)
WHERE (software:Application OR software:OperatingSystem)
  AND software.name = $softwareName
  AND ($version IS NULL OR software.version = $version)

RETURN
  EXISTS((software)) AS exists,
  count(software) AS instanceCount,
  labels(software)[0] AS softwareType,
  collect(DISTINCT software.version) AS versionsFound
```

**Parameters:**
```json
{
  "softwareName": "Apache HTTP Server",
  "version": null
}
```

### Intermediate Query - Application/OS Inventory with Equipment Mapping
```cypher
// Find application or OS with equipment and facility details
MATCH (software)
WHERE (software:Application OR software:OperatingSystem OR software:Software)
  AND ($softwareName IS NULL OR software.name CONTAINS $softwareName)
  AND ($version IS NULL OR software.version = $version)
  AND ($vendor IS NULL OR EXISTS((software)-[:MANUFACTURED_BY]->(:Vendor {name: $vendor})))

// Get installation locations
OPTIONAL MATCH (software)-[:INSTALLED_ON|RUNS_ON]->(eq:Equipment)
OPTIONAL MATCH (eq)-[:LOCATED_IN]->(f:Facility)

// Get vendor
OPTIONAL MATCH (software)-[:MANUFACTURED_BY]->(vendor:Vendor)

RETURN
  labels(software)[0] AS softwareType,
  software.name AS name,
  software.version AS version,
  vendor.name AS vendor,

  count(DISTINCT eq) AS installedOnCount,

  collect(DISTINCT {
    equipmentId: eq.id,
    equipmentName: eq.name,
    equipmentType: eq.type,
    facilityId: f.id,
    facilityName: f.name,
    installDate: software.installDate,
    licenseStatus: software.licenseStatus
  }) AS installations,

  collect(DISTINCT f.name) AS facilities

ORDER BY installedOnCount DESC
```

**Parameters:**
```json
{
  "softwareName": "Apache",
  "version": null,
  "vendor": null
}
```

### Advanced Query - Complete Software Asset Inventory with Vulnerabilities
```cypher
// Comprehensive software inventory with vulnerabilities, licensing, and EOL status
MATCH (software)
WHERE (software:Application OR software:OperatingSystem OR software:Software)
  AND ($softwareName IS NULL OR software.name CONTAINS $softwareName)
  AND ($version IS NULL OR software.version = $version)
  AND ($softwareType IS NULL OR $softwareType IN labels(software))

// Get vendor information
OPTIONAL MATCH (software)-[:MANUFACTURED_BY]->(vendor:Vendor)

// Get installation locations
OPTIONAL MATCH (software)-[:INSTALLED_ON|RUNS_ON]->(eq:Equipment)
OPTIONAL MATCH (eq)-[:LOCATED_IN]->(f:Facility)

// Get vulnerabilities
OPTIONAL MATCH (software)<-[:FOUND_IN]-(v:Vulnerability)
OPTIONAL MATCH (v)<-[:AFFECTS]-(cve:CVE)

// Get dependencies
OPTIONAL MATCH (software)-[:DEPENDS_ON]->(dependency)
WHERE dependency:Application OR dependency:Software OR dependency:OperatingSystem

// Calculate EOL status
WITH software, vendor, eq, f, v, cve, dependency,
  CASE
    WHEN software.endOfLife IS NOT NULL AND date(software.endOfLife) < date() THEN 'EOL'
    WHEN software.endOfLife IS NOT NULL AND date(software.endOfLife) < date() + duration({months: 6}) THEN 'APPROACHING_EOL'
    WHEN software.endOfLife IS NOT NULL THEN 'SUPPORTED'
    ELSE 'UNKNOWN'
  END AS eolStatus,

  CASE
    WHEN software.licenseExpiration IS NOT NULL AND date(software.licenseExpiration) < date() THEN 'EXPIRED'
    WHEN software.licenseExpiration IS NOT NULL AND date(software.licenseExpiration) < date() + duration({months: 3}) THEN 'EXPIRING_SOON'
    WHEN software.licenseExpiration IS NOT NULL THEN 'VALID'
    ELSE 'UNKNOWN'
  END AS licenseStatus

RETURN
  // Software Details
  {
    type: labels(software)[0],
    name: software.name,
    version: software.version,
    vendor: vendor.name,
    releaseDate: software.releaseDate,
    latestVersion: software.latestVersion,
    architecture: software.architecture,
    language: software.language
  } AS softwareDetails,

  // Lifecycle Status
  {
    eolStatus: eolStatus,
    endOfLifeDate: software.endOfLife,
    daysUntilEOL: CASE
      WHEN software.endOfLife IS NOT NULL
      THEN duration.between(date(), date(software.endOfLife)).days
      ELSE null
    END,
    licenseStatus: licenseStatus,
    licenseExpiration: software.licenseExpiration,
    licenseType: software.licenseType,
    supportLevel: software.supportLevel
  } AS lifecycleStatus,

  // Installation Summary
  {
    totalInstallations: count(DISTINCT eq),
    facilities: count(DISTINCT f),
    facilityList: collect(DISTINCT {
      facilityId: f.id,
      facilityName: f.name,
      installationCount: count(DISTINCT eq)
    }),
    criticalSystems: count(DISTINCT CASE WHEN eq.criticality = 'CRITICAL' THEN eq END),
    productionSystems: count(DISTINCT CASE WHEN eq.environment = 'PRODUCTION' THEN eq END)
  } AS installationSummary,

  // Vulnerability Assessment
  {
    totalVulnerabilities: count(DISTINCT v),
    criticalVulns: count(DISTINCT CASE WHEN cve.severity = 'CRITICAL' THEN v END),
    highVulns: count(DISTINCT CASE WHEN cve.severity = 'HIGH' THEN v END),
    mediumVulns: count(DISTINCT CASE WHEN cve.severity = 'MEDIUM' THEN v END),
    lowVulns: count(DISTINCT CASE WHEN cve.severity = 'LOW' THEN v END),
    vulnerabilitiesList: collect(DISTINCT {
      vulnerabilityId: v.id,
      cveId: cve.id,
      severity: cve.severity,
      cvssScore: cve.cvssScore,
      publishedDate: cve.publishedDate,
      patchAvailable: v.patchAvailable
    })[0..10]  // Limit to top 10
  } AS vulnerabilityAssessment,

  // Dependencies
  {
    dependencyCount: count(DISTINCT dependency),
    dependencies: collect(DISTINCT {
      type: labels(dependency)[0],
      name: dependency.name,
      version: dependency.version,
      required: dependency.required
    })
  } AS dependencyInfo,

  // Detailed Installations
  collect(DISTINCT {
    equipment: {
      id: eq.id,
      name: eq.name,
      type: eq.type,
      criticality: eq.criticality,
      environment: eq.environment
    },
    facility: {
      id: f.id,
      name: f.name,
      location: f.location
    },
    installDetails: {
      installDate: software.installDate,
      installedBy: software.installedBy,
      purpose: software.purpose,
      configurationProfile: software.configProfile
    },
    vulnerabilityCount: count(DISTINCT v),
    criticalVulns: count(DISTINCT CASE WHEN cve.severity = 'CRITICAL' THEN v END)
  }) AS detailedInstallations,

  // Compliance and Risk
  {
    complianceStatus: software.complianceStatus,
    regulatoryRequirements: software.regulatoryRequirements,
    riskScore: CASE
      WHEN eolStatus = 'EOL' THEN 10
      WHEN eolStatus = 'APPROACHING_EOL' THEN 7
      WHEN count(DISTINCT CASE WHEN cve.severity = 'CRITICAL' THEN v END) > 0 THEN 8
      WHEN count(DISTINCT CASE WHEN cve.severity = 'HIGH' THEN v END) > 0 THEN 6
      ELSE 3
    END,
    recommendedAction: CASE
      WHEN eolStatus = 'EOL' THEN 'IMMEDIATE UPGRADE REQUIRED'
      WHEN eolStatus = 'APPROACHING_EOL' THEN 'PLAN UPGRADE'
      WHEN count(DISTINCT CASE WHEN cve.severity = 'CRITICAL' THEN v END) > 0 THEN 'PATCH IMMEDIATELY'
      WHEN licenseStatus = 'EXPIRED' THEN 'RENEW LICENSE'
      ELSE 'MONITOR'
    END
  } AS complianceAndRisk

ORDER BY
  complianceAndRisk.riskScore DESC,
  installationSummary.totalInstallations DESC
```

**Parameters:**
```json
{
  "softwareName": "Apache",
  "version": null,
  "softwareType": null
}
```

**Expected Output:**
```json
{
  "softwareDetails": {
    "type": "Application",
    "name": "Apache HTTP Server",
    "version": "2.4.51",
    "vendor": "Apache Software Foundation",
    "releaseDate": "2021-10-07"
  },
  "lifecycleStatus": {
    "eolStatus": "SUPPORTED",
    "endOfLifeDate": "2026-12-31",
    "daysUntilEOL": 418,
    "licenseStatus": "VALID",
    "licenseType": "Apache 2.0"
  },
  "installationSummary": {
    "totalInstallations": 23,
    "facilities": 3,
    "criticalSystems": 8,
    "productionSystems": 20
  },
  "vulnerabilityAssessment": {
    "totalVulnerabilities": 5,
    "criticalVulns": 1,
    "highVulns": 2,
    "vulnerabilitiesList": [
      {
        "cveId": "CVE-2023-12345",
        "severity": "CRITICAL",
        "cvssScore": 9.8,
        "patchAvailable": true
      }
    ]
  },
  "complianceAndRisk": {
    "riskScore": 8,
    "recommendedAction": "PATCH IMMEDIATELY"
  }
}
```

---

## Question 8: Tell me the location (on what asset) is a specific application, vulnerability, OS, or library?

### Simple Query - Find Asset Locations
```cypher
// Find where a specific software component is located
MATCH (item)
WHERE (item:Application OR item:OperatingSystem OR item:Software OR item:Vulnerability)
  AND (item.name = $itemName OR item.id = $itemId)

MATCH (item)-[:INSTALLED_ON|RUNS_ON|FOUND_IN*1..2]->(eq:Equipment)

RETURN
  labels(item)[0] AS itemType,
  coalesce(item.name, item.id) AS itemIdentifier,
  item.version AS version,

  collect(DISTINCT {
    equipmentId: eq.id,
    equipmentName: eq.name,
    equipmentType: eq.type,
    location: eq.location
  }) AS assetLocations,

  count(DISTINCT eq) AS totalAssets
```

**Parameters:**
```json
{
  "itemName": "Apache HTTP Server",
  "itemId": null
}
```

### Intermediate Query - Asset Location with Facility Details
```cypher
// Find asset locations with complete facility and network context
MATCH (item)
WHERE (item:Application OR item:OperatingSystem OR item:Software OR item:Vulnerability)
  AND (
    item.name CONTAINS $searchTerm OR
    item.id = $searchTerm OR
    item.cveId = $searchTerm
  )

// Find equipment
MATCH path = (item)-[:INSTALLED_ON|RUNS_ON|FOUND_IN*1..3]->(eq:Equipment)

// Get facility
OPTIONAL MATCH (eq)-[:LOCATED_IN]->(f:Facility)

// Get network zone
OPTIONAL MATCH (eq)-[:IN_ZONE]->(zone:NetworkZone)

// Get vendor if applicable
OPTIONAL MATCH (item)-[:MANUFACTURED_BY]->(vendor:Vendor)

RETURN
  {
    type: labels(item)[0],
    name: item.name,
    id: item.id,
    version: item.version,
    vendor: vendor.name
  } AS itemDetails,

  collect(DISTINCT {
    equipment: {
      id: eq.id,
      name: eq.name,
      type: eq.type,
      model: eq.model,
      serialNumber: eq.serialNumber,
      ipAddress: eq.ipAddress,
      status: eq.status,
      criticality: eq.criticality
    },
    physicalLocation: {
      facilityId: f.id,
      facilityName: f.name,
      facilityAddress: f.location,
      building: eq.building,
      floor: eq.floor,
      room: eq.room,
      rack: eq.rack,
      rackUnit: eq.rackUnit
    },
    networkLocation: {
      zone: zone.name,
      zoneType: zone.type,
      vlan: eq.vlan,
      subnet: eq.subnet,
      networkAccessible: eq.networkAccessible
    },
    installationPath: [n IN nodes(path) |
      {
        type: labels(n)[0],
        name: coalesce(n.name, n.id)
      }
    ]
  }) AS locations,

  count(DISTINCT eq) AS totalAssets,
  count(DISTINCT f) AS totalFacilities

ORDER BY itemDetails.name
```

**Parameters:**
```json
{
  "searchTerm": "Apache"
}
```

### Advanced Query - Complete Asset Location Mapping with Context
```cypher
// Comprehensive asset location mapping with vulnerabilities, dependencies, and relationships
MATCH (item)
WHERE (item:Application OR item:OperatingSystem OR item:Software OR item:Vulnerability)
  AND (
    ($itemName IS NOT NULL AND item.name CONTAINS $itemName) OR
    ($itemId IS NOT NULL AND (item.id = $itemId OR item.cveId = $itemId)) OR
    ($version IS NOT NULL AND item.version = $version)
  )

// Find all equipment where this item exists
MATCH installPath = (item)-[:INSTALLED_ON|RUNS_ON|FOUND_IN*1..4]->(eq:Equipment)

// Get facility and zone information
OPTIONAL MATCH (eq)-[:LOCATED_IN]->(facility:Facility)
OPTIONAL MATCH (eq)-[:IN_ZONE]->(zone:NetworkZone)

// Get vendor
OPTIONAL MATCH (item)-[:MANUFACTURED_BY]->(vendor:Vendor)

// If it's a vulnerability, get the CVE
OPTIONAL MATCH (item:Vulnerability)<-[:AFFECTS]-(cve:CVE)

// If it's software, get vulnerabilities
OPTIONAL MATCH (item)<-[:FOUND_IN]-(vuln:Vulnerability)
OPTIONAL MATCH (vuln)<-[:AFFECTS]-(vulnCve:CVE)

// Get dependencies
OPTIONAL MATCH (item)-[:DEPENDS_ON]->(dep)
WHERE dep:Application OR dep:Software OR dep:OperatingSystem

// Get dependent items (what depends on this)
OPTIONAL MATCH (dependent)-[:DEPENDS_ON]->(item)
WHERE dependent:Application OR dependent:Software OR dependent:OperatingSystem

// Get co-located items on same equipment
OPTIONAL MATCH (eq)<-[:INSTALLED_ON|RUNS_ON]-(colocated)
WHERE colocated <> item
  AND (colocated:Application OR colocated:OperatingSystem OR colocated:Software)

WITH item, vendor, cve, vuln, vulnCve, dep, dependent, colocated,
  eq, facility, zone, installPath,

  // Calculate criticality score
  CASE
    WHEN eq.criticality = 'CRITICAL' THEN 4
    WHEN eq.criticality = 'HIGH' THEN 3
    WHEN eq.criticality = 'MEDIUM' THEN 2
    ELSE 1
  END AS criticalityScore,

  // Determine environment
  CASE
    WHEN eq.environment = 'PRODUCTION' THEN 'PROD'
    WHEN eq.environment = 'STAGING' THEN 'STAGE'
    WHEN eq.environment = 'DEVELOPMENT' THEN 'DEV'
    ELSE 'UNKNOWN'
  END AS envType

RETURN
  // Item Information
  {
    type: labels(item)[0],
    name: item.name,
    id: item.id,
    version: item.version,
    vendor: vendor.name,
    description: item.description,

    // For vulnerabilities
    cveId: cve.id,
    severity: cve.severity,
    cvssScore: cve.cvssScore,
    exploitable: item.exploitable,

    // Lifecycle
    releaseDate: item.releaseDate,
    endOfLife: item.endOfLife,
    supportStatus: item.supportStatus
  } AS itemDetails,

  // Asset Locations - Grouped by facility
  collect(DISTINCT {
    facility: {
      id: facility.id,
      name: facility.name,
      address: facility.location,
      type: facility.type,
      securityZone: facility.securityZone,
      coordinates: {
        latitude: facility.latitude,
        longitude: facility.longitude
      }
    },

    equipment: {
      id: eq.id,
      name: eq.name,
      type: eq.type,
      model: eq.model,
      serialNumber: eq.serialNumber,
      manufacturer: eq.manufacturer,
      criticality: eq.criticality,
      environment: envType,
      status: eq.status,
      owner: eq.owner,
      managedBy: eq.managedBy
    },

    physicalLocation: {
      building: eq.building,
      floor: eq.floor,
      room: eq.room,
      rack: eq.rack,
      rackUnit: eq.rackUnit,
      position: eq.position,
      coordinates: eq.coordinates
    },

    networkLocation: {
      ipAddress: eq.ipAddress,
      macAddress: eq.macAddress,
      hostname: eq.hostname,
      domain: eq.domain,
      zone: zone.name,
      zoneType: zone.type,
      vlan: eq.vlan,
      subnet: eq.subnet,
      gateway: eq.gateway,
      networkAccessible: eq.networkAccessible,
      publiclyAccessible: eq.publiclyAccessible,
      firewallRules: eq.firewallRules
    },

    installationDetails: {
      installDate: item.installDate,
      installedBy: item.installedBy,
      installMethod: item.installMethod,
      configurationProfile: item.configProfile,
      purpose: item.purpose,
      pathToItem: [n IN nodes(installPath) |
        {
          type: labels(n)[0],
          name: coalesce(n.name, n.id),
          version: n.version
        }
      ],
      pathLength: length(installPath)
    },

    colocatedSoftware: collect(DISTINCT {
      type: labels(colocated)[0],
      name: colocated.name,
      version: colocated.version,
      purpose: colocated.purpose
    })[0..5],  // Limit to 5 most relevant

    criticalityScore: criticalityScore

  }) AS assetLocations,

  // Vulnerability Context (if item is software)
  {
    hasVulnerabilities: count(DISTINCT vuln) > 0,
    totalVulnerabilities: count(DISTINCT vuln),
    criticalVulns: count(DISTINCT CASE WHEN vulnCve.severity = 'CRITICAL' THEN vuln END),
    highVulns: count(DISTINCT CASE WHEN vulnCve.severity = 'HIGH' THEN vuln END),
    vulnerabilities: collect(DISTINCT {
      vulnId: vuln.id,
      cveId: vulnCve.id,
      severity: vulnCve.severity,
      cvssScore: vulnCve.cvssScore,
      description: vulnCve.description,
      publishedDate: vulnCve.publishedDate,
      patchAvailable: vuln.patchAvailable
    })[0..10]  // Top 10
  } AS vulnerabilityContext,

  // Dependency Information
  {
    dependencies: collect(DISTINCT {
      type: labels(dep)[0],
      name: dep.name,
      version: dep.version,
      required: dep.required,
      minVersion: dep.minVersion
    }),
    dependencyCount: count(DISTINCT dep),

    dependents: collect(DISTINCT {
      type: labels(dependent)[0],
      name: dependent.name,
      version: dependent.version
    }),
    dependentCount: count(DISTINCT dependent)
  } AS dependencyInfo,

  // Summary Statistics
  {
    totalAssets: count(DISTINCT eq),
    totalFacilities: count(DISTINCT facility),
    criticalAssets: count(DISTINCT CASE WHEN eq.criticality = 'CRITICAL' THEN eq END),
    productionAssets: count(DISTINCT CASE WHEN eq.environment = 'PRODUCTION' THEN eq END),
    externallyAccessible: count(DISTINCT CASE WHEN eq.publiclyAccessible = true THEN eq END),

    facilitiesList: collect(DISTINCT facility.name),
    assetTypeDistribution: collect(DISTINCT {
      type: eq.type,
      count: count(eq)
    }),

    highestCriticality: max(criticalityScore),
    avgCriticality: avg(criticalityScore)
  } AS summary,

  // Risk Assessment
  {
    overallRiskScore: CASE
      WHEN count(DISTINCT CASE WHEN vulnCve.severity = 'CRITICAL' THEN vuln END) > 0
        AND max(criticalityScore) >= 3 THEN 10
      WHEN count(DISTINCT CASE WHEN vulnCve.severity = 'HIGH' THEN vuln END) > 0
        AND max(criticalityScore) >= 3 THEN 8
      WHEN count(DISTINCT vuln) > 0 THEN 6
      ELSE 3
    END,

    riskFactors: [
      CASE WHEN count(DISTINCT CASE WHEN vulnCve.severity = 'CRITICAL' THEN vuln END) > 0
        THEN 'Critical vulnerabilities present' ELSE null END,
      CASE WHEN count(DISTINCT CASE WHEN eq.publiclyAccessible = true THEN eq END) > 0
        THEN 'Externally accessible assets' ELSE null END,
      CASE WHEN max(criticalityScore) >= 3
        THEN 'High-criticality assets affected' ELSE null END,
      CASE WHEN item.endOfLife IS NOT NULL AND date(item.endOfLife) < date()
        THEN 'Software past end-of-life' ELSE null END
    ],

    recommendedActions: [
      CASE WHEN count(DISTINCT CASE WHEN vulnCve.severity = 'CRITICAL' THEN vuln END) > 0
        THEN 'Immediate patching required' ELSE null END,
      CASE WHEN item.endOfLife IS NOT NULL AND date(item.endOfLife) < date()
        THEN 'Upgrade to supported version' ELSE null END,
      CASE WHEN count(DISTINCT CASE WHEN eq.publiclyAccessible = true THEN eq END) > 0
        THEN 'Review external access requirements' ELSE null END
    ]
  } AS riskAssessment

ORDER BY
  riskAssessment.overallRiskScore DESC,
  summary.totalAssets DESC
```

**Parameters:**
```json
{
  "itemName": "Apache",
  "itemId": null,
  "version": null
}
```

**Expected Output:**
```json
{
  "itemDetails": {
    "type": "Application",
    "name": "Apache HTTP Server",
    "version": "2.4.51",
    "vendor": "Apache Software Foundation",
    "endOfLife": "2026-12-31"
  },
  "assetLocations": [
    {
      "facility": {
        "id": "FAC-001",
        "name": "Primary Data Center",
        "address": "123 Server Lane, New York, NY"
      },
      "equipment": {
        "id": "EQ-WEB-001",
        "name": "Production Web Server 1",
        "type": "Server",
        "model": "Dell PowerEdge R740",
        "criticality": "CRITICAL",
        "environment": "PROD",
        "status": "OPERATIONAL"
      },
      "physicalLocation": {
        "building": "Building A",
        "floor": "2",
        "room": "Server Room 2A",
        "rack": "Rack-12",
        "rackUnit": "U15-U17"
      },
      "networkLocation": {
        "ipAddress": "10.0.1.50",
        "hostname": "web01.internal.example.com",
        "zone": "DMZ",
        "vlan": "VLAN-100",
        "subnet": "10.0.1.0/24",
        "networkAccessible": true,
        "publiclyAccessible": true
      },
      "colocatedSoftware": [
        {"type": "OperatingSystem", "name": "Ubuntu", "version": "20.04"},
        {"type": "Application", "name": "PHP", "version": "8.1"},
        {"type": "Software", "name": "OpenSSL", "version": "1.1.1"}
      ]
    }
  ],
  "vulnerabilityContext": {
    "hasVulnerabilities": true,
    "totalVulnerabilities": 5,
    "criticalVulns": 1,
    "highVulns": 2,
    "vulnerabilities": [
      {
        "cveId": "CVE-2023-12345",
        "severity": "CRITICAL",
        "cvssScore": 9.8,
        "patchAvailable": true
      }
    ]
  },
  "summary": {
    "totalAssets": 23,
    "totalFacilities": 3,
    "criticalAssets": 8,
    "productionAssets": 20,
    "externallyAccessible": 5
  },
  "riskAssessment": {
    "overallRiskScore": 10,
    "riskFactors": [
      "Critical vulnerabilities present",
      "Externally accessible assets",
      "High-criticality assets affected"
    ],
    "recommendedActions": [
      "Immediate patching required",
      "Review external access requirements"
    ]
  }
}
```

---

## Performance Optimization Tips

### 1. Use Bi-Directional Relationships
```cypher
// Instead of this (slower):
MATCH (a)-[:REL]->(b)
MATCH (b)-[:REL]->(c)

// Use this (faster with bi-directional):
MATCH (a)-[:REL]-(b)-[:REL]-(c)
WHERE // add direction constraints in WHERE if needed
```

### 2. Index Strategy
- Create indexes on frequently queried properties
- Use composite indexes for common query patterns
- Monitor query performance and add indexes as needed

### 3. Parameterize Queries
- Always use parameters ($param) instead of hard-coded values
- Enables query plan caching and reuse

### 4. Limit Results
- Use `LIMIT` for exploratory queries
- Aggregate early in the query pipeline
- Use `collect()[0..10]` to limit collections

### 5. Profile Queries
```cypher
PROFILE [your query]
// Analyze db hits and optimize accordingly
```

---

## Query Execution Examples

### Running Queries with Parameters

```bash
# Using cypher-shell
cypher-shell -u neo4j -p password -d neo4j \
  --param "cveId => 'CVE-2023-12345'" \
  --param "facilityId => 'FAC-001'" \
  -f query.cypher

# Using Neo4j Browser
:param cveId => 'CVE-2023-12345';
:param facilityId => 'FAC-001';
[paste query]

# Using Python Driver
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

with driver.session(database="neo4j") as session:
    result = session.run("""
        [your query here]
    """, cveId="CVE-2023-12345", facilityId="FAC-001")

    for record in result:
        print(record)
```

---

**END OF QUERY PATTERNS**
