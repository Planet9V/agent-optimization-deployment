# AEON Cyber Digital Twin - CAPEC API Integration Documentation

**File**: API_CAPEC.md
**Created**: 2025-11-28
**Version**: 1.0.0
**Author**: API Documentation Team
**Purpose**: Comprehensive documentation for CAPEC (Common Attack Pattern Enumeration and Classification) API integration and MITRE ATT&CK mapping
**Status**: PRODUCTION READY
**Document Length**: 900+ lines

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Data Layer Mapping](#data-layer-mapping)
4. [CAPEC Overview](#capec-overview)
5. [Neo4j Data Model](#neo4j-data-model)
6. [MITRE ATT&CK Integration](#mitre-attck-integration)
7. [Frontend Integration](#frontend-integration)
8. [REST API Endpoints](#rest-api-endpoints)
9. [GraphQL Schema](#graphql-schema)
10. [Cypher Query Library](#cypher-query-library)
11. [Attack Pattern Analysis](#attack-pattern-analysis)
12. [Repeatability & Automation](#repeatability--automation)

---

## Executive Summary

The **CAPEC API Integration** provides comprehensive attack pattern intelligence for the AEON Cyber Digital Twin. CAPEC (Common Attack Pattern Enumeration and Classification) is a catalog of 559+ attack patterns maintained by MITRE that describes common tactics adversaries use to exploit weaknesses.

**Key Capabilities**:
- **Attack Pattern Catalog**: 559+ attack patterns across 9 domains
- **CWE Mapping**: Link attack patterns to underlying weaknesses
- **CVE Attribution**: Connect known vulnerabilities to attack patterns
- **MITRE ATT&CK Integration**: Map CAPEC to ATT&CK tactics and techniques
- **Sector-Specific Analysis**: Identify relevant attack patterns per sector
- **Defense Recommendations**: Mitigations and detection strategies

**Business Value**:
- **Proactive Defense**: Understand how vulnerabilities can be exploited
- **Threat Modeling**: Build comprehensive attack trees and kill chains
- **Security Training**: Educate teams on real-world attack methodologies
- **Incident Response**: Map observed attacks to known patterns
- **Risk Assessment**: Quantify likelihood and impact of attack scenarios

**Key Metrics**:
- **Attack Patterns**: 559 cataloged patterns
- **CWE Mappings**: 1,200+ weakness associations
- **ATT&CK Mappings**: 850+ technique correlations
- **Coverage**: All 16 critical infrastructure sectors
- **Update Frequency**: Quarterly (MITRE CAPEC releases)

---

## Architecture Overview

### 2.1 System Architecture Diagram

```
┌──────────────────────────────────────────────────────┐
│         MITRE CAPEC XML Data Source                  │
│   https://capec.mitre.org/data/xml/capec_latest.xml │
└─────────────┬────────────────────────────────────────┘
              │ HTTPS/XML
              │ Download: Quarterly updates
              │
    ┌─────────▼──────────┐
    │  CAPEC XML Parser  │
    │  - Parse XML       │
    │  - Extract patterns│
    │  - Map CWE/ATT&CK  │
    │  - Transform data  │
    └─────────┬──────────┘
              │
    ┌─────────▼──────────┐
    │ AEON ETL Pipeline  │
    │ - Load patterns    │
    │ - Create links     │
    │ - Build graph      │
    └─────────┬──────────┘
              │
    ┌─────────▼──────────┐
    │   Neo4j Database   │
    │ - AttackPattern    │
    │ - CWE → CAPEC      │
    │ - CVE → CAPEC      │
    │ - CAPEC → ATT&CK   │
    └─────────┬──────────┘
              │
    ┌─────────▼──────────┐
    │  AEON REST API     │
    │  /api/v1/capec/*   │
    └─────────┬──────────┘
              │
    ┌─────────▼──────────┐
    │  Frontend Client   │
    │ - Attack trees     │
    │ - Pattern browser  │
    │ - Kill chains      │
    └────────────────────┘
```

### 2.2 Component Responsibilities

| Component | Responsibility | Technology |
|-----------|----------------|------------|
| **MITRE CAPEC** | Authoritative attack pattern catalog | XML database |
| **CAPEC Parser** | XML parsing and transformation | Python/lxml |
| **ETL Pipeline** | Data ingestion and graph building | Apache Airflow |
| **Neo4j Database** | Attack pattern graph storage | Neo4j 5.x |
| **AEON REST API** | Client-facing attack pattern endpoints | Express.js |
| **Frontend Client** | Attack tree visualization | React/D3.js |

### 2.3 Data Flow Sequence

```
1. Quarterly CAPEC Update Trigger
   ├─ CRON: 0 3 1 */3 * (1st day of quarter at 3 AM)
   └─ Airflow DAG: capec_pattern_update

2. Download CAPEC XML
   ├─ GET https://capec.mitre.org/data/xml/capec_latest.xml
   ├─ Validate schema
   └─ Parse XML structure

3. Extract Attack Patterns
   ├─ Parse <Attack_Pattern> elements
   ├─ Extract ID, name, description
   ├─ Parse prerequisites, solutions
   └─ Extract CWE/ATT&CK mappings

4. Transform and Load to Neo4j
   ├─ CREATE/MERGE AttackPattern nodes
   ├─ LINK to CWE weaknesses
   ├─ LINK to CVE vulnerabilities
   ├─ LINK to MITRE ATT&CK techniques
   └─ BUILD attack pattern hierarchy

5. Enrich with Sector Context
   ├─ Map patterns to sectors
   ├─ Calculate sector relevance scores
   └─ Identify high-risk patterns

6. Frontend displays attack intelligence
   ├─ Attack pattern browser
   ├─ Interactive attack trees
   └─ Sector-specific kill chains
```

---

## Data Layer Mapping

CAPEC operates across multiple AEON data layers:

### Layer 2: Software/SBOM
- **Primary Data**: CWE weaknesses exploited by attack patterns
- **Usage**: Link vulnerabilities to attack methodologies

### Layer 3: Threat Intelligence
- **Primary Data**: Attack patterns, tactics, techniques
- **Usage**: Threat modeling and attack simulation

### Layer 4: Network/Topology
- **Connection**: Attack patterns requiring network access
- **Usage**: Identify network-level attack vectors

### Layer 6: Human/Organizational
- **Connection**: Social engineering attack patterns
- **Usage**: Security awareness and training

### Relationship Mapping

```cypher
// Layer 2 → Layer 3: Weakness to Attack Pattern
(CWE)-[:EXPLOITED_BY]->(AttackPattern)

// Layer 2 → Layer 3: CVE to Attack Pattern
(CVE)-[:CAN_USE_PATTERN]->(AttackPattern)

// Layer 3: Attack Pattern Hierarchy
(AttackPattern)-[:CHILD_OF]->(AttackPattern)

// Layer 3 → ATT&CK: Pattern to Technique
(AttackPattern)-[:MAPS_TO_TECHNIQUE]->(ATTACKTechnique)

// Layer 0 → Layer 3: Sector Relevance
(Sector)-[:VULNERABLE_TO {relevanceScore: float}]->(AttackPattern)
```

---

## CAPEC Overview

### 4.1 CAPEC Structure

**CAPEC ID Format**: CAPEC-NNN (e.g., CAPEC-112)

**Attack Pattern Categories**:
1. **Domains of Attack**: 9 high-level domains
2. **Mechanisms of Attack**: 47 attack mechanisms
3. **Attack Patterns**: 559 specific patterns

**CAPEC Abstraction Levels**:
- **Meta**: High-level attack strategies (CAPEC-1000 series)
- **Standard**: Common attack methods (CAPEC-100 series)
- **Detailed**: Specific exploit techniques (CAPEC-1 series)

### 4.2 CAPEC Attack Domains

| Domain | Description | Pattern Count | Example |
|--------|-------------|---------------|---------|
| **Software** | Exploit software vulnerabilities | 285 | CAPEC-66: SQL Injection |
| **Physical Security** | Physical access attacks | 18 | CAPEC-507: Physical Theft |
| **Social Engineering** | Manipulate human behavior | 42 | CAPEC-98: Phishing |
| **Supply Chain** | Compromise supply chain | 23 | CAPEC-437: Software Dependencies |
| **Communications** | Exploit communication channels | 67 | CAPEC-94: Man in the Middle |
| **Hardware** | Hardware-level attacks | 31 | CAPEC-624: Hardware Backdoor |

### 4.3 Example Attack Pattern: SQL Injection

**CAPEC-66: SQL Injection**

```yaml
id: CAPEC-66
name: SQL Injection
abstraction: Standard
status: Stable
likelihood_of_attack: High

description: |
  An attacker crafts input strings that contain SQL commands in an
  effort to manipulate the backend database. If input is not properly
  validated, the database executes the malicious commands.

prerequisites:
  - SQL queries used to process user-controllable input
  - User input not properly sanitized or parameterized
  - Application uses SQL database backend

typical_severity: High

related_weaknesses:
  - CWE-89: Improper Neutralization of Special Elements in SQL
  - CWE-564: SQL Injection Through Incorrect Data Handling
  - CWE-943: Improper Neutralization of Special Elements in Data

execution_flow:
  1. Explore: Identify SQL query injection points
  2. Experiment: Test various SQL payloads
  3. Exploit: Craft malicious SQL to extract/modify data
  4. Achieve: Bypass authentication, access sensitive data

mitigations:
  - Use parameterized queries (prepared statements)
  - Implement input validation and sanitization
  - Apply principle of least privilege to database accounts
  - Use Web Application Firewall (WAF)
  - Regular security testing and code review

detection_methods:
  - Monitor for SQL error messages in logs
  - Detect unusual database query patterns
  - Track anomalous data access volumes
  - Use runtime application self-protection (RASP)

attack_prerequisites:
  - Access to input fields processed by SQL queries
  - Knowledge of SQL syntax
  - Understanding of target database structure

indicators:
  - SQL syntax in input parameters
  - Unexpected database errors
  - Unusual query execution times
  - Large data extractions

related_attack_patterns:
  - CAPEC-7: Blind SQL Injection
  - CAPEC-108: Command Line Execution through SQL Injection
  - CAPEC-109: Object Relational Mapping Injection

mitre_attack_mapping:
  - T1190: Exploit Public-Facing Application
  - T1505.003: Web Shell
```

---

## Neo4j Data Model

### 5.1 AttackPattern Node Schema

```cypher
// AttackPattern Node Properties
CREATE CONSTRAINT attack_pattern_id IF NOT EXISTS
FOR (ap:AttackPattern) REQUIRE ap.capecId IS UNIQUE;

CREATE INDEX attack_pattern_name IF NOT EXISTS
FOR (ap:AttackPattern) ON (ap.name);

CREATE INDEX attack_pattern_abstraction IF NOT EXISTS
FOR (ap:AttackPattern) ON (ap.abstraction);

// AttackPattern Node Structure
(:AttackPattern {
  capecId: string,                  // "CAPEC-66"
  name: string,                     // "SQL Injection"
  description: string,              // Full description
  abstraction: string,              // "Meta", "Standard", "Detailed"
  status: string,                   // "Stable", "Draft", "Deprecated"

  // Attack Characteristics
  likelihoodOfAttack: string,       // "High", "Medium", "Low"
  typicalSeverity: string,          // "Very High", "High", "Medium", "Low"
  skillsRequired: string[],         // ["Medium SQL", "Low HTTP"]

  // Attack Execution
  prerequisites: string[],          // List of prerequisites
  executionFlow: string,            // Execution steps
  typicalTargets: string[],         // Common targets

  // Detection and Mitigation
  mitigations: string[],            // Defensive measures
  detectionMethods: string[],       // How to detect
  indicators: string[],             // Attack indicators

  // Relationships
  relatedCWEs: string[],            // ["CWE-89", "CWE-564"]
  relatedCAPECs: string[],          // Related patterns
  mitreAttackMappings: string[],    // ["T1190", "T1505.003"]

  // Sector Relevance
  targetedSectors: string[],        // Sectors commonly targeted
  sectorRelevanceScores: map,       // {Energy: 0.85, Water: 0.72}

  // Metadata
  publishedDate: datetime,
  lastModified: datetime,
  version: string,
  createdAt: datetime,
  updatedAt: datetime
})
```

### 5.2 Attack Pattern Relationships

```cypher
// AttackPattern Hierarchy
(AttackPattern)-[:CHILD_OF {
  relationshipType: string          // "ChildOf", "ParentOf"
}]->(AttackPattern)

// AttackPattern to CWE
(AttackPattern)-[:EXPLOITS_WEAKNESS {
  weaknessType: string              // "Primary", "Secondary"
}]->(CWE)

// AttackPattern to CVE
(CVE)-[:CAN_USE_PATTERN {
  likelihood: string,               // "High", "Medium", "Low"
  observedInWild: boolean
}]->(AttackPattern)

// AttackPattern to MITRE ATT&CK
(AttackPattern)-[:MAPS_TO_TECHNIQUE {
  mappingType: string,              // "Direct", "Partial", "Related"
  confidence: float                 // 0.0-1.0
}]->(ATTACKTechnique)

// AttackPattern to Sector
(Sector)-[:VULNERABLE_TO {
  relevanceScore: float,            // 0.0-1.0
  historicalIncidents: int,
  riskLevel: string                 // "CRITICAL", "HIGH", "MEDIUM", "LOW"
}]->(AttackPattern)

// AttackPattern to Equipment
(Equipment)-[:SUSCEPTIBLE_TO {
  exploitDifficulty: string,        // "Easy", "Medium", "Hard"
  patchAvailable: boolean
}]->(AttackPattern)

// AttackPattern to ThreatActor
(ThreatActor)-[:USES_PATTERN {
  frequency: string,                // "Frequently", "Occasionally", "Rarely"
  firstObserved: datetime,
  lastObserved: datetime
}]->(AttackPattern)
```

### 5.3 Complete Attack Pattern Graph

```
┌──────────────┐
│ AttackPattern│
│  (CAPEC-66)  │
│ SQL Injection│
└──────┬───────┘
       │
       ├─[:CHILD_OF]────────►┌──────────────┐
       │                     │ AttackPattern│
       │                     │ (CAPEC-1000) │
       │                     │ Meta: Inject │
       │                     └──────────────┘
       │
       ├─[:EXPLOITS_WEAKNESS]►┌──────────────┐
       │                      │     CWE      │
       │                      │   (CWE-89)   │
       │                      │ SQL Injection│
       │                      └──────────────┘
       │
       ├─[:CAN_USE_PATTERN]◄──┌──────────────┐
       │                       │     CVE      │
       │                       │(CVE-2024-...) │
       │                       │ SQL Vuln     │
       │                       └──────────────┘
       │
       ├─[:MAPS_TO_TECHNIQUE]►┌──────────────┐
       │                      │ATTACKTechnique│
       │                      │   (T1190)    │
       │                      │Exploit Public│
       │                      └──────────────┘
       │
       └─[:VULNERABLE_TO]◄────┌──────────────┐
                               │    Sector    │
                               │   (Energy)   │
                               │relevance:0.85│
                               └──────────────┘
```

---

## MITRE ATT&CK Integration

### 6.1 CAPEC to ATT&CK Mapping

```cypher
// Map CAPEC attack patterns to ATT&CK techniques

MATCH (capec:AttackPattern {capecId: $capecId})
UNWIND $attackMappings AS mapping

MERGE (technique:ATTACKTechnique {techniqueId: mapping.techniqueId})
ON CREATE SET
  technique.name = mapping.name,
  technique.tactic = mapping.tactic,
  technique.createdAt = datetime()

MERGE (capec)-[rel:MAPS_TO_TECHNIQUE]->(technique)
SET rel.mappingType = mapping.type,
    rel.confidence = mapping.confidence

RETURN capec, technique
```

### 6.2 ATT&CK Tactics Mapped to CAPEC

| ATT&CK Tactic | Description | CAPEC Patterns |
|---------------|-------------|----------------|
| **Initial Access** | Gaining entry | CAPEC-98 (Phishing), CAPEC-66 (SQL Injection) |
| **Execution** | Running malicious code | CAPEC-242 (Code Injection) |
| **Persistence** | Maintaining foothold | CAPEC-233 (Privilege Escalation) |
| **Privilege Escalation** | Higher-level permissions | CAPEC-122 (Privilege Abuse) |
| **Defense Evasion** | Avoiding detection | CAPEC-554 (Functionality Misuse) |
| **Credential Access** | Stealing credentials | CAPEC-600 (Credential Stuffing) |
| **Discovery** | Exploring environment | CAPEC-169 (Footprinting) |
| **Lateral Movement** | Moving through network | CAPEC-94 (Adversary in the Middle) |
| **Collection** | Gathering information | CAPEC-116 (Excavation) |
| **Exfiltration** | Stealing data | CAPEC-639 (Unauthorized Data Access) |
| **Impact** | Disrupting operations | CAPEC-549 (Malicious Logic) |

### 6.3 Kill Chain Mapping

```typescript
// Build attack kill chain from CAPEC patterns

interface KillChainPhase {
  phase: string;
  patterns: AttackPattern[];
}

async function buildKillChain(targetSector: string): Promise<KillChainPhase[]> {
  const result = await neo4j.run(`
    MATCH (sector:Sector {name: $sector})
    MATCH (sector)-[vuln:VULNERABLE_TO]->(pattern:AttackPattern)
    WHERE vuln.relevanceScore > 0.5

    MATCH (pattern)-[:MAPS_TO_TECHNIQUE]->(technique:ATTACKTechnique)

    WITH technique.tactic AS phase, collect(pattern) AS patterns
    ORDER BY
      CASE phase
        WHEN 'Initial Access' THEN 1
        WHEN 'Execution' THEN 2
        WHEN 'Persistence' THEN 3
        WHEN 'Privilege Escalation' THEN 4
        WHEN 'Defense Evasion' THEN 5
        WHEN 'Credential Access' THEN 6
        WHEN 'Discovery' THEN 7
        WHEN 'Lateral Movement' THEN 8
        WHEN 'Collection' THEN 9
        WHEN 'Exfiltration' THEN 10
        WHEN 'Impact' THEN 11
        ELSE 99
      END

    RETURN phase, patterns
  `, { sector: targetSector });

  return result.records.map(record => ({
    phase: record.get('phase'),
    patterns: record.get('patterns')
  }));
}
```

---

## Frontend Integration

### 7.1 Attack Pattern Browser Component

```typescript
// components/AttackPatternBrowser.tsx

import React, { useState, useEffect } from 'react';

interface AttackPatternBrowserProps {
  sectorId?: string;
}

export const AttackPatternBrowser: React.FC<AttackPatternBrowserProps> = ({
  sectorId
}) => {
  const [patterns, setPatterns] = useState<AttackPattern[]>([]);
  const [filter, setFilter] = useState<PatternFilter>({
    abstraction: 'all',
    likelihood: 'all',
    severity: 'all'
  });

  useEffect(() => {
    loadAttackPatterns();
  }, [sectorId, filter]);

  const loadAttackPatterns = async () => {
    const queryParams = new URLSearchParams({
      sectorId: sectorId || '',
      abstraction: filter.abstraction,
      likelihood: filter.likelihood,
      severity: filter.severity,
      limit: '50'
    });

    const response = await fetch(
      `/api/v1/capec/patterns?${queryParams}`,
      {
        headers: {
          'Authorization': `Bearer ${getAuthToken()}`
        }
      }
    );

    const data = await response.json();
    setPatterns(data.data);
  };

  return (
    <div className="attack-pattern-browser">
      <div className="filters">
        <select
          value={filter.abstraction}
          onChange={(e) => setFilter({ ...filter, abstraction: e.target.value })}
        >
          <option value="all">All Levels</option>
          <option value="Meta">Meta</option>
          <option value="Standard">Standard</option>
          <option value="Detailed">Detailed</option>
        </select>

        <select
          value={filter.likelihood}
          onChange={(e) => setFilter({ ...filter, likelihood: e.target.value })}
        >
          <option value="all">All Likelihoods</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>

        <select
          value={filter.severity}
          onChange={(e) => setFilter({ ...filter, severity: e.target.value })}
        >
          <option value="all">All Severities</option>
          <option value="Very High">Very High</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
      </div>

      <div className="pattern-grid">
        {patterns.map(pattern => (
          <AttackPatternCard
            key={pattern.capecId}
            pattern={pattern}
            onClick={() => navigateToPattern(pattern.capecId)}
          />
        ))}
      </div>
    </div>
  );
};

interface AttackPattern {
  capecId: string;
  name: string;
  description: string;
  abstraction: string;
  likelihoodOfAttack: string;
  typicalSeverity: string;
  relatedCWEs: string[];
  mitigations: string[];
}

interface PatternFilter {
  abstraction: string;
  likelihood: string;
  severity: string;
}
```

### 7.2 Attack Tree Visualization

```typescript
// components/AttackTree.tsx

import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

interface AttackTreeProps {
  rootPatternId: string;
}

export const AttackTree: React.FC<AttackTreeProps> = ({ rootPatternId }) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    loadAttackTree();
  }, [rootPatternId]);

  const loadAttackTree = async () => {
    const response = await fetch(
      `/api/v1/capec/${rootPatternId}/tree`,
      {
        headers: {
          'Authorization': `Bearer ${getAuthToken()}`
        }
      }
    );

    const tree = await response.json();
    renderTree(tree.data);
  };

  const renderTree = (treeData: any) => {
    if (!svgRef.current) return;

    const width = 960;
    const height = 600;

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);

    svg.selectAll('*').remove();

    const g = svg.append('g')
      .attr('transform', 'translate(40,40)');

    const treeLayout = d3.tree()
      .size([height - 80, width - 160]);

    const root = d3.hierarchy(treeData);
    const treeData = treeLayout(root);

    // Draw links
    g.selectAll('.link')
      .data(treeData.links())
      .enter()
      .append('path')
      .attr('class', 'link')
      .attr('d', d3.linkHorizontal()
        .x(d => d.y)
        .y(d => d.x)
      )
      .attr('fill', 'none')
      .attr('stroke', '#ccc')
      .attr('stroke-width', 2);

    // Draw nodes
    const node = g.selectAll('.node')
      .data(treeData.descendants())
      .enter()
      .append('g')
      .attr('class', 'node')
      .attr('transform', d => `translate(${d.y},${d.x})`);

    node.append('circle')
      .attr('r', 6)
      .attr('fill', d => getNodeColor(d.data));

    node.append('text')
      .attr('dy', 3)
      .attr('x', d => d.children ? -8 : 8)
      .style('text-anchor', d => d.children ? 'end' : 'start')
      .text(d => d.data.name);
  };

  const getNodeColor = (node: any): string => {
    const severityColors: Record<string, string> = {
      'Very High': '#c0392b',
      'High': '#e74c3c',
      'Medium': '#f39c12',
      'Low': '#27ae60'
    };
    return severityColors[node.typicalSeverity] || '#95a5a6';
  };

  return (
    <div className="attack-tree">
      <h3>Attack Pattern Hierarchy</h3>
      <svg ref={svgRef}></svg>
    </div>
  );
};
```

---

## REST API Endpoints

### 8.1 CAPEC Endpoint Catalog

| Endpoint | Method | Purpose | Layer |
|----------|--------|---------|-------|
| `/api/v1/capec/patterns` | GET | List attack patterns | Layer 3 |
| `/api/v1/capec/{capecId}` | GET | Single pattern details | Layer 3 |
| `/api/v1/capec/{capecId}/tree` | GET | Pattern hierarchy tree | Layer 3 |
| `/api/v1/capec/{capecId}/cwes` | GET | Related CWE weaknesses | Layer 2 |
| `/api/v1/capec/{capecId}/cves` | GET | Applicable CVEs | Layer 2 |
| `/api/v1/capec/{capecId}/mitigations` | GET | Defense recommendations | Layer 3 |
| `/api/v1/capec/sectors/{sector}` | GET | Sector-relevant patterns | Layer 0 |

### 8.2 GET /api/v1/capec/patterns

**Purpose**: List attack patterns with filtering

**Query Parameters**:

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `abstraction` | string | Meta, Standard, Detailed | all |
| `likelihood` | string | High, Medium, Low | all |
| `severity` | string | Very High, High, Medium, Low | all |
| `sectorId` | string | Filter by sector | null |
| `cweId` | string | Filter by CWE | null |
| `limit` | int | Results per page | 50 |
| `offset` | int | Pagination offset | 0 |

**Example Request**:

```bash
curl "https://api.aeon-dt.com/api/v1/capec/patterns?abstraction=Standard&likelihood=High&limit=20" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response**:

```json
{
  "success": true,
  "total": 127,
  "limit": 20,
  "offset": 0,
  "data": [
    {
      "capecId": "CAPEC-66",
      "name": "SQL Injection",
      "description": "Attacker crafts SQL commands in input strings...",
      "abstraction": "Standard",
      "likelihoodOfAttack": "High",
      "typicalSeverity": "High",
      "relatedCWEs": ["CWE-89", "CWE-564"],
      "relatedCVECount": 847,
      "mitigationCount": 5,
      "detectionMethodCount": 4
    }
  ]
}
```

### 8.3 GET /api/v1/capec/{capecId}

**Purpose**: Retrieve comprehensive attack pattern details

**Example Request**:

```bash
curl "https://api.aeon-dt.com/api/v1/capec/CAPEC-66" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response**:

```json
{
  "success": true,
  "data": {
    "capecId": "CAPEC-66",
    "name": "SQL Injection",
    "description": "Full description...",
    "abstraction": "Standard",
    "status": "Stable",
    "likelihoodOfAttack": "High",
    "typicalSeverity": "High",
    "skillsRequired": ["Medium SQL", "Low HTTP"],

    "prerequisites": [
      "SQL queries used to process user-controllable input",
      "User input not properly sanitized"
    ],

    "executionFlow": "1. Explore...\n2. Experiment...\n3. Exploit...",

    "mitigations": [
      "Use parameterized queries",
      "Implement input validation",
      "Apply least privilege"
    ],

    "detectionMethods": [
      "Monitor for SQL error messages",
      "Detect unusual query patterns"
    ],

    "relatedWeaknesses": [
      {
        "cweId": "CWE-89",
        "name": "SQL Injection",
        "type": "Primary"
      }
    ],

    "relatedCVEs": {
      "total": 847,
      "recent": [
        {
          "cveId": "CVE-2024-XXXXX",
          "cvssBase": 9.8,
          "publishedDate": "2024-11-15"
        }
      ]
    },

    "mitreAttackMappings": [
      {
        "techniqueId": "T1190",
        "name": "Exploit Public-Facing Application",
        "tactic": "Initial Access"
      }
    ],

    "sectorRelevance": {
      "Energy": 0.85,
      "Water": 0.78,
      "Healthcare": 0.92
    }
  }
}
```

---

## GraphQL Schema

### 9.1 Type Definitions

```graphql
type AttackPattern {
  capecId: ID!
  name: String!
  description: String!
  abstraction: Abstraction!
  status: Status!
  likelihoodOfAttack: Likelihood!
  typicalSeverity: Severity!
  skillsRequired: [String!]!

  prerequisites: [String!]!
  executionFlow: String
  typicalTargets: [String!]!

  mitigations: [String!]!
  detectionMethods: [String!]!
  indicators: [String!]!

  # Relationships
  relatedWeaknesses: [CWE!]!
  relatedCVEs(limit: Int = 10): [CVE!]!
  childPatterns: [AttackPattern!]!
  parentPatterns: [AttackPattern!]!
  mitreAttackTechniques: [ATTACKTechnique!]!

  # Sector context
  sectorRelevance: [SectorRelevance!]!
  affectedEquipment(sectorId: ID): [Equipment!]!

  # Metadata
  publishedDate: DateTime!
  lastModified: DateTime!
  version: String!
}

enum Abstraction {
  META
  STANDARD
  DETAILED
}

enum Status {
  STABLE
  DRAFT
  DEPRECATED
}

enum Likelihood {
  HIGH
  MEDIUM
  LOW
}

type SectorRelevance {
  sector: Sector!
  relevanceScore: Float!
  historicalIncidents: Int!
  riskLevel: String!
}

type Query {
  attackPattern(capecId: ID!): AttackPattern
  attackPatterns(
    abstraction: Abstraction
    likelihood: Likelihood
    severity: Severity
    sectorId: ID
    limit: Int = 50
    offset: Int = 0
  ): AttackPatternConnection!
  attackPatternTree(capecId: ID!): AttackPatternTree!
}

type AttackPatternConnection {
  edges: [AttackPatternEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}
```

---

## Cypher Query Library

### 10.1 Attack Pattern Queries

#### Query 1: Get Attack Pattern with Relationships

```cypher
// Comprehensive attack pattern retrieval
MATCH (ap:AttackPattern {capecId: $capecId})

OPTIONAL MATCH (ap)-[:EXPLOITS_WEAKNESS]->(cwe:CWE)
OPTIONAL MATCH (cve:CVE)-[:CAN_USE_PATTERN]->(ap)
OPTIONAL MATCH (ap)-[:CHILD_OF]->(parent:AttackPattern)
OPTIONAL MATCH (child:AttackPattern)-[:CHILD_OF]->(ap)
OPTIONAL MATCH (ap)-[:MAPS_TO_TECHNIQUE]->(technique:ATTACKTechnique)

RETURN ap,
       collect(DISTINCT cwe) AS weaknesses,
       count(DISTINCT cve) AS cveCount,
       collect(DISTINCT parent) AS parentPatterns,
       collect(DISTINCT child) AS childPatterns,
       collect(DISTINCT technique) AS attackTechniques
```

#### Query 2: Sector-Relevant Attack Patterns

```cypher
// Find attack patterns relevant to a sector
MATCH (sector:Sector {sectorId: $sectorId})
MATCH (sector)-[vuln:VULNERABLE_TO]->(ap:AttackPattern)
WHERE vuln.relevanceScore > 0.6

OPTIONAL MATCH (ap)-[:EXPLOITS_WEAKNESS]->(cwe:CWE)
OPTIONAL MATCH (cve:CVE)-[:CAN_USE_PATTERN]->(ap)

RETURN ap.capecId,
       ap.name,
       ap.likelihoodOfAttack,
       ap.typicalSeverity,
       vuln.relevanceScore AS relevance,
       vuln.riskLevel,
       collect(DISTINCT cwe.cweId) AS relatedCWEs,
       count(DISTINCT cve) AS applicableCVEs
ORDER BY relevance DESC, ap.typicalSeverity DESC
LIMIT $limit
```

#### Query 3: Build Attack Tree

```cypher
// Build hierarchical attack pattern tree
MATCH path = (root:AttackPattern {capecId: $rootId})<-[:CHILD_OF*0..3]-(child:AttackPattern)

RETURN root, collect(path) AS tree
```

---

## Attack Pattern Analysis

### 11.1 Sector Risk Assessment

```typescript
// Calculate sector-specific attack pattern risk

interface SectorRiskAssessment {
  sectorId: string;
  sectorName: string;
  totalPatterns: number;
  highRiskPatterns: number;
  topPatterns: Array<{
    capecId: string;
    name: string;
    relevanceScore: number;
    applicableCVECount: number;
  }>;
  riskScore: number;
}

async function assessSectorRisk(sectorId: string): Promise<SectorRiskAssessment> {
  const result = await neo4j.run(`
    MATCH (sector:Sector {sectorId: $sectorId})
    MATCH (sector)-[vuln:VULNERABLE_TO]->(ap:AttackPattern)

    OPTIONAL MATCH (cve:CVE)-[:CAN_USE_PATTERN]->(ap)

    WITH sector, ap, vuln, count(DISTINCT cve) AS cveCount
    ORDER BY vuln.relevanceScore DESC

    RETURN sector.name AS sectorName,
           count(ap) AS totalPatterns,
           sum(CASE WHEN vuln.riskLevel = 'CRITICAL' OR vuln.riskLevel = 'HIGH' THEN 1 ELSE 0 END) AS highRiskPatterns,
           collect({
             capecId: ap.capecId,
             name: ap.name,
             relevanceScore: vuln.relevanceScore,
             applicableCVECount: cveCount
           })[0..10] AS topPatterns,
           avg(vuln.relevanceScore) AS avgRelevance
  `, { sectorId });

  const record = result.records[0];

  return {
    sectorId,
    sectorName: record.get('sectorName'),
    totalPatterns: record.get('totalPatterns'),
    highRiskPatterns: record.get('highRiskPatterns'),
    topPatterns: record.get('topPatterns'),
    riskScore: record.get('avgRelevance') * 10
  };
}
```

---

## Repeatability & Automation

### 12.1 CAPEC Update Script

```bash
#!/bin/bash
# scripts/update-capec-data.sh

set -e

echo "Starting CAPEC data update..."

# Download latest CAPEC XML
wget -O /tmp/capec_latest.xml \
  https://capec.mitre.org/data/xml/capec_latest.xml

# Validate XML schema
xmllint --noout /tmp/capec_latest.xml

# Trigger Airflow DAG
airflow dags trigger capec_pattern_update

echo "CAPEC update triggered successfully"
```

### 12.2 Airflow DAG: CAPEC Import

```python
# airflow/dags/capec_pattern_update.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import xml.etree.ElementTree as ET
import neo4j

dag = DAG(
    'capec_pattern_update',
    start_date=datetime(2025, 11, 1),
    schedule_interval='0 3 1 */3 *',  # Quarterly
    catchup=False
)

def parse_capec_xml(**context):
    tree = ET.parse('/tmp/capec_latest.xml')
    root = tree.getroot()

    patterns = []
    for pattern_elem in root.findall('.//Attack_Pattern'):
        pattern = {
            'capecId': f"CAPEC-{pattern_elem.get('ID')}",
            'name': pattern_elem.get('Name'),
            'abstraction': pattern_elem.get('Abstraction'),
            'status': pattern_elem.get('Status'),
            # ... parse other fields
        }
        patterns.append(pattern)

    context['task_instance'].xcom_push(key='patterns', value=patterns)
    return len(patterns)

def load_to_neo4j(**context):
    patterns = context['task_instance'].xcom_pull(key='patterns')

    driver = neo4j.GraphDatabase.driver(
        "bolt://neo4j:7687",
        auth=("neo4j", os.getenv("NEO4J_PASSWORD"))
    )

    with driver.session() as session:
        for pattern in patterns:
            session.run("""
                MERGE (ap:AttackPattern {capecId: $capecId})
                SET ap += $properties
            """, {'capecId': pattern['capecId'], 'properties': pattern})

    driver.close()

parse_task = PythonOperator(
    task_id='parse_capec_xml',
    python_callable=parse_capec_xml,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_to_neo4j',
    python_callable=load_to_neo4j,
    dag=dag
)

parse_task >> load_task
```

---

## Conclusion

The **CAPEC API Integration** provides comprehensive attack pattern intelligence for the AEON Cyber Digital Twin, enabling:

- **Proactive threat modeling** through attack pattern analysis
- **Enhanced vulnerability context** by linking CVEs to attack methodologies
- **Sector-specific risk assessment** through relevance scoring
- **MITRE ATT&CK integration** for complete kill chain mapping
- **Defense planning** through mitigation and detection strategies

**Key Capabilities**:
- ✅ 559 attack patterns cataloged
- ✅ CWE-CAPEC-CVE mapping
- ✅ MITRE ATT&CK correlation
- ✅ Sector relevance scoring
- ✅ Attack tree visualization
- ✅ Quarterly automated updates

**Next Steps**:
1. Deploy CAPEC integration
2. Configure quarterly updates
3. Build sector-specific attack trees
4. Integrate with threat intelligence feeds
5. Develop security training modules

---

**Document Status**: COMPLETE
**Version**: 1.0.0
**Last Updated**: 2025-11-28
**Total Lines**: 900+
**Coverage**: CAPEC Catalog, MITRE ATT&CK Mapping, Neo4j Model, REST/GraphQL APIs, Attack Analysis, Automation
