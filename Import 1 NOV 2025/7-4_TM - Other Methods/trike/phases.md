# Trike Methodology Phases
## Requirements-Driven Threat Modeling with Quantitative Risk Analysis

**Version:** 1.0 - October 2025
**Focus:** Detailed breakdown of Trike's four-phase methodology with implementation guidance
**Audience:** Security architects and requirements engineers implementing Trike

---

## Breadcrumb Navigation
[Home](../../../../index.md) > [Threat Modeling](../../../index.md) > [Methodologies](../../index.md) > [Trike](../index.md) > Phases

---

## Table of Contents

### Trike Phases
- [[#phase-1-requirements|Phase 1: Requirements Definition]]
- [[#phase-2-modeling|Phase 2: System Modeling]]
- [[#phase-3-threats|Phase 3: Threat Identification]]
- [[#phase-4-mitigation|Phase 4: Mitigation Design]]

### Implementation Support
- [[#requirements-framework|Requirements Framework]]
- [[#risk-calculations|Risk Calculations]]
- [[#traceability|Requirements Traceability]]

---

## Phase 1: Requirements Definition

**Establish security requirements and success criteria that will drive the threat modeling process**

### Objectives
- Define comprehensive security requirements
- Establish requirement priorities and dependencies
- Create requirements traceability framework
- Validate requirements against business objectives

### Key Activities

#### Security Requirements Definition
```json
{
  "securityRequirements": [
    {
      "id": "REQ-CONF-001",
      "category": "Confidentiality",
      "requirement": "All customer PII must be encrypted at rest and in transit",
      "rationale": "Protect customer privacy and comply with GDPR",
      "priority": "Critical",
      "validationCriteria": "Encryption implemented and tested",
      "traceability": {
        "businessObjective": "Customer trust and regulatory compliance",
        "compliance": ["GDPR Article 32", "PCI DSS 3.2.1"],
        "relatedRequirements": ["REQ-INTEG-001", "REQ-AVAIL-001"]
      }
    },
    {
      "id": "REQ-INTEG-002",
      "category": "Integrity",
      "requirement": "Financial transaction data must be protected from unauthorized modification",
      "rationale": "Prevent fraud and ensure transaction accuracy",
      "priority": "High",
      "validationCriteria": "Integrity checks implemented and validated",
      "traceability": {
        "businessObjective": "Financial accuracy and fraud prevention",
        "compliance": ["SOX Section 404", "PCI DSS 10.5"],
        "relatedRequirements": ["REQ-CONF-001", "REQ-AUDIT-001"]
      }
    }
  ]
}
```

#### Requirements Categories
- **Confidentiality:** Protection of sensitive information from unauthorized disclosure
- **Integrity:** Prevention of unauthorized modification of data or systems
- **Availability:** Ensuring systems remain accessible to authorized users
- **Accountability:** Ability to trace actions to responsible parties

#### Requirements Prioritization
- **Critical:** Business-critical requirements that must be satisfied
- **High:** Important requirements supporting key business functions
- **Medium:** Standard security requirements for operational security
- **Low:** Optional requirements for enhanced security

#### Requirements Dependencies
- **Preconditions:** Requirements that must be satisfied before others
- **Co-requisites:** Requirements that must be implemented together
- **Successors:** Requirements that depend on others being satisfied
- **Conflicts:** Requirements that may be mutually exclusive

### Deliverables
- Comprehensive security requirements specification
- Requirements traceability matrix
- Requirements validation criteria
- Requirements priority ranking

---

## Phase 2: System Modeling

**Create trust boundary models and component relationship diagrams**

### Objectives
- Identify system components and their capabilities
- Map trust relationships between components
- Define trust boundaries and privilege levels
- Document data flows and access patterns

### Key Activities

#### Component Identification
```json
{
  "systemComponents": [
    {
      "id": "COMP-WEB-001",
      "name": "Web Server",
      "type": "Application Server",
      "capabilities": ["Serve HTTP requests", "Process user input", "Access database"],
      "privileges": ["Network access", "File system read/write"],
      "trustLevel": "Untrusted",
      "interfaces": ["HTTP/HTTPS", "Database connection"]
    },
    {
      "id": "COMP-DB-001",
      "name": "Customer Database",
      "type": "Data Store",
      "capabilities": ["Store customer data", "Query operations", "Data backup"],
      "privileges": ["Data read/write", "Schema modifications"],
      "trustLevel": "Trusted",
      "interfaces": ["SQL queries", "Backup operations"]
    }
  ]
}
```

#### Trust Boundary Analysis
- **Trust Levels:** Untrusted, Limited Trust, Trusted, High Trust
- **Boundary Types:** Network boundaries, application boundaries, data boundaries
- **Trust Relationships:** How components trust each other
- **Privilege Escalation Paths:** Potential paths for privilege increases

#### Data Flow Modeling
- **Data Sources:** Where data originates in the system
- **Data Transformations:** How data is processed and modified
- **Data Sinks:** Where data is stored or transmitted
- **Data Classifications:** Sensitivity levels and handling requirements

### Deliverables
- Component capability matrix
- Trust boundary diagram
- Data flow diagrams (DFD)
- Privilege level definitions

---

## Phase 3: Threat Identification

**Identify threats that violate security requirements using quantitative risk analysis**

### Objectives
- Analyze each trust boundary for requirement violations
- Assess attacker capabilities and motivations
- Calculate quantitative risk scores for each threat
- Prioritize threats based on risk calculations

### Key Activities

#### Threat Analysis Framework
```json
{
  "threatAnalysis": {
    "boundaryAnalysis": [
      {
        "boundaryId": "BOUNDARY-WEB-DB",
        "components": ["Web Server", "Database"],
        "requirementsAtRisk": ["REQ-CONF-001", "REQ-INTEG-002"],
        "potentialThreats": [
          {
            "id": "THREAT-SQLI-001",
            "description": "SQL injection attack via web interface",
            "violatedRequirements": ["REQ-INTEG-002"],
            "attackerProfile": {
              "skill": "Intermediate",
              "motive": "High",
              "opportunity": "High"
            },
            "controlProfile": {
              "strength": "Medium",
              "implementation": "Good"
            },
            "riskCalculation": {
              "attackerFactor": 3 * 4 * 4, // 48
              "controlFactor": 3 * 4,       // 12
              "riskScore": 48 / 12,         // 4.0
              "riskLevel": "High"
            }
          }
        ]
      }
    ]
  }
}
```

#### Attacker Profiling
- **Skill Levels:** Novice (1), Intermediate (3), Advanced (5), Expert (7), Multiple Experts (9)
- **Motivation Levels:** None (0), Low (2), Moderate (4), High (6), Extreme (8)
- **Opportunity Levels:** None (0), Low (2), Moderate (4), High (6), Extreme (8)

#### Risk Calculation Methodology
**Risk Score Formula:**
```
Risk Score = (Attacker Skill × Attacker Motive × Attacker Opportunity) ÷ (Control Strength × Implementation Quality)
```

**Risk Level Interpretation:**
- **0-1:** Very Low Risk - Accept or ignore
- **1-2:** Low Risk - Monitor periodically
- **2-3:** Medium Risk - Plan mitigation
- **3-5:** High Risk - Implement mitigation
- **5+:** Critical Risk - Immediate action required

#### Threat Prioritization
- **Critical Threats:** Risk score > 5.0, violates critical requirements
- **High Threats:** Risk score 3.0-5.0, violates high-priority requirements
- **Medium Threats:** Risk score 2.0-3.0, violates medium-priority requirements
- **Low Threats:** Risk score < 2.0, violates low-priority requirements

### Deliverables
- Threat identification report
- Quantitative risk assessment
- Threat prioritization matrix
- Requirements-threat traceability matrix

---

## Phase 4: Mitigation Design

**Design controls that satisfy security requirements and mitigate identified threats**

### Objectives
- Develop mitigations for identified threats
- Ensure mitigation traceability to requirements
- Validate control effectiveness against requirements
- Document implementation dependencies and constraints

### Key Activities

#### Mitigation Design Framework
```json
{
  "mitigationDesign": {
    "threatMitigations": [
      {
        "threatId": "THREAT-SQLI-001",
        "mitigationId": "MITIG-SQLI-001",
        "description": "Implement prepared statements and input validation",
        "type": "Technical Control",
        "category": "Preventive",
        "satisfiedRequirements": ["REQ-INTEG-002"],
        "implementationDetails": {
          "primaryControl": "Use parameterized queries",
          "secondaryControl": "Input sanitization",
          "monitoringControl": "SQL injection detection",
          "effectivenessRating": "High"
        },
        "traceability": {
          "requirements": ["REQ-INTEG-002"],
          "threats": ["THREAT-SQLI-001"],
          "testCases": ["TC-SQLI-001", "TC-SQLI-002"]
        },
        "implementationRequirements": {
          "dependencies": ["Database connection library update"],
          "resources": ["Developer time: 2 days", "Testing time: 1 day"],
          "timeline": "2 weeks",
          "riskReduction": "80%"
        }
      }
    ]
  }
}
```

#### Control Categories
- **Preventive Controls:** Stop threats before they occur
- **Detective Controls:** Identify threats when they occur
- **Corrective Controls:** Restore systems after incidents
- **Deterrent Controls:** Discourage threat actors

#### Requirements Traceability
- **Forward Traceability:** From requirements to implemented controls
- **Backward Traceability:** From controls back to requirements
- **Coverage Analysis:** Ensuring all requirements are addressed
- **Gap Analysis:** Identifying requirements without corresponding controls

#### Control Validation
- **Effectiveness Assessment:** How well control mitigates the threat
- **Implementation Feasibility:** Technical and operational feasibility
- **Cost-Benefit Analysis:** Security value vs. implementation cost
- **Residual Risk Calculation:** Risk remaining after control implementation

### Deliverables
- Mitigation design specification
- Requirements-control traceability matrix
- Implementation roadmap
- Control validation report

---

## Requirements Framework

### Confidentiality Requirements
- **Data Protection:** Encryption, access controls, data classification
- **Transmission Security:** TLS, VPN, secure protocols
- **Storage Security:** Encryption at rest, secure key management
- **Information Handling:** Clean desk policies, screen locks

### Integrity Requirements
- **Data Integrity:** Hashing, digital signatures, integrity monitoring
- **System Integrity:** Change management, configuration management
- **Transaction Integrity:** ACID properties, rollback capabilities
- **Audit Integrity:** Tamper-proof audit logs, secure timestamps

### Availability Requirements
- **System Availability:** Redundancy, failover, disaster recovery
- **Performance Requirements:** Capacity planning, load balancing
- **Maintenance Windows:** Scheduled maintenance procedures
- **Incident Response:** Recovery time objectives, recovery point objectives

### Accountability Requirements
- **Audit Logging:** Comprehensive audit trails, log management
- **User Authentication:** Multi-factor authentication, session management
- **Access Monitoring:** Real-time access monitoring, anomaly detection
- **Non-repudiation:** Digital signatures, secure timestamps

---

## Risk Calculations

### Attacker Factor Calculations
```javascript
function calculateAttackerFactor(skill, motive, opportunity) {
  const skillValue = {
    'Novice': 1, 'Intermediate': 3, 'Advanced': 5,
    'Expert': 7, 'Multiple Experts': 9
  }[skill] || 1;

  const motiveValue = {
    'None': 0, 'Low': 2, 'Moderate': 4, 'High': 6, 'Extreme': 8
  }[motive] || 0;

  const opportunityValue = {
    'None': 0, 'Low': 2, 'Moderate': 4, 'High': 6, 'Extreme': 8
  }[opportunity] || 0;

  return skillValue * motiveValue * opportunityValue;
}
```

### Control Factor Calculations
```javascript
function calculateControlFactor(strength, implementation) {
  const strengthValue = {
    'None': 1, 'Weak': 2, 'Moderate': 3, 'Strong': 4, 'Complete': 5
  }[strength] || 1;

  const implementationValue = {
    'Poor': 1, 'Fair': 2, 'Good': 3, 'Excellent': 4, 'Perfect': 5
  }[implementation] || 1;

  return strengthValue * implementationValue;
}
```

### Risk Score Calculation
```javascript
function calculateRiskScore(attackerFactor, controlFactor) {
  if (controlFactor === 0) return Infinity;
  return attackerFactor / controlFactor;
}

function getRiskLevel(riskScore) {
  if (riskScore >= 5) return 'Critical';
  if (riskScore >= 3) return 'High';
  if (riskScore >= 2) return 'Medium';
  if (riskScore >= 1) return 'Low';
  return 'Very Low';
}
```

---

## Requirements Traceability

### Traceability Matrix Structure
| Requirement ID | Description | Threats | Mitigations | Test Cases | Status |
|----------------|-------------|---------|-------------|------------|--------|
| REQ-CONF-001 | Data encryption | THREAT-001 | MITIG-001 | TC-001 | Implemented |

### Traceability Levels
- **Level 1:** Requirements to high-level design
- **Level 2:** Requirements to detailed design
- **Level 3:** Requirements to code implementation
- **Level 4:** Requirements to test cases

### Coverage Analysis
- **Requirements Coverage:** Percentage of requirements with corresponding mitigations
- **Threat Coverage:** Percentage of threats with corresponding mitigations
- **Test Coverage:** Percentage of requirements with test validation
- **Implementation Coverage:** Percentage of mitigations successfully implemented

---

## Navigation

| Previous | Current | Next |
|----------|---------|------|
| [[../index|Trike Overview]] | Trike Phases | [[./requirements|Requirements Analysis]] |

## See Also

### Related Topics
- [[../index|Trike Methodology]] - Framework overview
- [[./requirements|Requirements Analysis]] - Security requirements framework
- [[./risk-calculation|Risk Calculation]] - Quantitative risk assessment

### Implementation Resources
- [[./template|Trike Template]] - Requirements-driven template
- [[../../../workflows/examples/compliance-monitoring|Compliance Workflows]] - Integration examples
- [[../../../resources/tools|Threat Modeling Tools]] - Trike-compatible tools

---

**Tags:** #trike-phases #requirements-driven #quantitative-risk #threat-identification #mitigation-design

**Last Updated:** October 2025
**Version:** 1.0
**Reading Time:** 25 minutes
**Difficulty:** Advanced