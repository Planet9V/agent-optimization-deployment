# PASTA Methodology Phases
## Detailed 8-Phase Risk-Centric Threat Modeling Process

**Version:** 1.0 - October 2025
**Focus:** Comprehensive breakdown of all 8 PASTA phases with implementation guidance
**Audience:** Security professionals implementing PASTA methodology

---

## Breadcrumb Navigation
[Home](../../../../index.md) > [Threat Modeling](../../../index.md) > [Methodologies](../../index.md) > [PASTA](../index.md) > Phases

---

## Table of Contents

### PASTA Phases
- [[#phase-1-define-business-objectives|Phase 1: Define Business Objectives]]
- [[#phase-2-define-technical-scope|Phase 2: Define Technical Scope]]
- [[#phase-3-application-decomposition|Phase 3: Application Decomposition]]
- [[#phase-4-threat-analysis|Phase 4: Threat Analysis]]
- [[#phase-5-vulnerability-analysis|Phase 5: Vulnerability Analysis]]
- [[#phase-6-attack-modeling|Phase 6: Attack Modeling]]
- [[#phase-7-risk-analysis|Phase 7: Risk Analysis]]
- [[#phase-8-residual-risk-analysis|Phase 8: Residual Risk Analysis]]

### Implementation Support
- [[#phase-artifacts|Phase Artifacts & Deliverables]]
- [[#success-criteria|Success Criteria]]
- [[#common-challenges|Common Challenges & Solutions]]

---

## Phase 1: Define Business Objectives

**Establish the business context and derive security requirements from business needs**

### Objectives
- Understand business goals and success criteria
- Identify regulatory and compliance requirements
- Determine risk tolerance and security priorities
- Establish stakeholder expectations

### Key Activities

#### Business Objective Analysis
```json
{
  "businessObjectives": [
    {
      "objective": "Process 1000 transactions per minute",
      "priority": "Critical",
      "securityImpact": "Availability requirements",
      "compliance": ["PCI-DSS", "SOX"]
    },
    {
      "objective": "Protect customer PII data",
      "priority": "High",
      "securityImpact": "Confidentiality requirements",
      "compliance": ["GDPR", "CCPA"]
    }
  ]
}
```

#### Security Objective Derivation
- **Confidentiality:** Protect sensitive business information
- **Integrity:** Ensure accuracy and trustworthiness of business data
- **Availability:** Maintain business operations and service levels
- **Compliance:** Meet regulatory requirements and standards

#### Risk Tolerance Assessment
- **Risk Appetite:** Acceptable level of risk exposure
- **Risk Capacity:** Maximum risk the organization can absorb
- **Risk Tolerance:** Specific risk thresholds for different scenarios

### Deliverables
- Business objective documentation
- Security objective mapping
- Compliance requirement analysis
- Stakeholder risk tolerance statement

---

## Phase 2: Define Technical Scope

**Determine the technical boundaries and constraints of the analysis**

### Objectives
- Identify system components and architecture
- Define trust boundaries and security domains
- Establish technical constraints and assumptions
- Document scope limitations and exclusions

### Key Activities

#### System Boundary Definition
```json
{
  "inScope": {
    "components": ["Web Server", "Application Server", "Database"],
    "networks": ["DMZ", "Internal Network"],
    "dataTypes": ["Customer Data", "Transaction Data"]
  },
  "outOfScope": {
    "components": ["Third-party APIs", "Legacy Systems"],
    "networks": ["Partner Networks"],
    "dataTypes": ["Archived Data"]
  }
}
```

#### Trust Boundary Analysis
- **Network Boundaries:** DMZ, internal, external networks
- **Application Boundaries:** User interface, business logic, data layer
- **Data Boundaries:** Public, internal, confidential, restricted data

#### Technical Constraint Documentation
- **Platform Limitations:** Operating system, hardware constraints
- **Integration Requirements:** Third-party system dependencies
- **Performance Requirements:** Throughput, latency, scalability needs

### Deliverables
- Technical scope document
- System architecture diagram
- Trust boundary map
- Assumption and constraint log

---

## Phase 3: Application Decomposition

**Break down the application into analyzable components and data flows**

### Objectives
- Identify all application components and interfaces
- Map data flows and trust relationships
- Define privilege levels and access patterns
- Document component interactions and dependencies

### Key Activities

#### Component Inventory
```json
{
  "components": [
    {
      "name": "WebServer",
      "type": "web_application",
      "trustLevel": "internet_facing",
      "entryPoints": ["HTTP/HTTPS ports"],
      "exitPoints": ["Database connections"],
      "privileges": ["user_authentication"]
    },
    {
      "name": "Database",
      "type": "data_store",
      "trustLevel": "internal",
      "dataSensitivity": "high",
      "accessPatterns": ["read/write"],
      "encryption": "at_rest"
    }
  ]
}
```

#### Data Flow Analysis
- **Entry Points:** User inputs, API calls, file uploads
- **Exit Points:** Database writes, external API calls, log outputs
- **Transformation Points:** Data processing and validation
- **Storage Points:** Data persistence and caching

#### Trust Level Definition
- **Public:** Internet-facing, no authentication required
- **Authenticated:** User login required, basic access
- **Privileged:** Administrative access, elevated permissions
- **System:** Internal system-to-system communication

### Deliverables
- Component inventory spreadsheet
- Data flow diagrams (DFD)
- Trust boundary diagrams
- Privilege level matrix

---

## Phase 4: Threat Analysis

**Identify potential threat actors and their capabilities**

### Objectives
- Analyze threat actor motivations and capabilities
- Assess threat actor sophistication levels
- Map threats to business impact scenarios
- Determine threat actor resources and persistence

### Key Activities

#### Threat Actor Profiling
```json
{
  "threatActors": [
    {
      "name": "External Hacker",
      "motivation": "Financial Gain",
      "capability": "Advanced",
      "resources": "High",
      "persistence": "Opportunistic",
      "targets": ["Customer Data", "Financial Systems"]
    },
    {
      "name": "Insider Threat",
      "motivation": "Sabotage",
      "capability": "Moderate",
      "resources": "Internal Access",
      "persistence": "Targeted",
      "targets": ["System Integrity", "Business Operations"]
    }
  ]
}
```

#### Threat Actor Categories
- **Script Kiddies:** Basic tools, opportunistic attacks
- **Organized Crime:** Financial motivation, moderate sophistication
- **Nation States:** Advanced persistent threats, strategic objectives
- **Insider Threats:** Authorized access, varied motivations
- **Hacktivists:** Ideological motivation, technical skills

#### Attack Vector Analysis
- **External Attacks:** Network-based, web application attacks
- **Internal Attacks:** Privilege abuse, data exfiltration
- **Supply Chain Attacks:** Third-party compromise, dependency attacks
- **Physical Attacks:** Facility access, hardware tampering

### Deliverables
- Threat actor profiles
- Attack vector analysis
- Threat motivation mapping
- Actor capability assessment

---

## Phase 5: Vulnerability Analysis

**Discover weaknesses that threat actors can exploit**

### Objectives
- Identify technical vulnerabilities and weaknesses
- Assess vulnerability exploitability and detection
- Evaluate existing security controls effectiveness
- Prioritize vulnerabilities based on threat exposure

### Key Activities

#### Vulnerability Assessment
```json
{
  "vulnerabilities": [
    {
      "id": "VULN-001",
      "component": "WebServer",
      "type": "SQL Injection",
      "severity": "High",
      "exploitability": "Easy",
      "detection": "Moderate",
      "existingControls": ["Input Validation"],
      "threatActors": ["External Hacker"]
    },
    {
      "id": "VULN-002",
      "component": "Database",
      "type": "Weak Encryption",
      "severity": "Critical",
      "exploitability": "Moderate",
      "detection": "Low",
      "existingControls": ["None"],
      "threatActors": ["Insider Threat", "External Hacker"]
    }
  ]
}
```

#### Vulnerability Types
- **Technical Vulnerabilities:** Software bugs, misconfigurations
- **Process Vulnerabilities:** Weak procedures, inadequate training
- **Human Vulnerabilities:** Social engineering susceptibility
- **Physical Vulnerabilities:** Inadequate physical security

#### Exploitability Factors
- **Technical Complexity:** Required attacker skill level
- **Resource Requirements:** Tools, time, and access needed
- **Detection Risk:** Likelihood of detection during exploitation
- **Remediation Difficulty:** Time and effort to fix

### Deliverables
- Vulnerability inventory
- Exploitability assessment
- Control effectiveness evaluation
- Vulnerability prioritization matrix

---

## Phase 6: Attack Modeling

**Simulate attack scenarios and exploitation paths**

### Objectives
- Develop detailed attack scenarios and progression
- Model attack trees and decision points
- Assess attack success probabilities
- Identify critical attack paths and choke points

### Key Activities

#### Attack Tree Development
```json
{
  "attackTree": {
    "root": "Data Breach",
    "children": [
      {
        "node": "Web Application Compromise",
        "probability": 0.7,
        "children": [
          {
            "node": "SQL Injection",
            "probability": 0.8,
            "mitigations": ["Input Validation", "Parameterized Queries"]
          },
          {
            "node": "XSS Attack",
            "probability": 0.6,
            "mitigations": ["Output Encoding", "CSP"]
          }
        ]
      },
      {
        "node": "Insider Attack",
        "probability": 0.3,
        "children": [
          {
            "node": "Privilege Abuse",
            "probability": 0.9,
            "mitigations": ["Access Monitoring", "Least Privilege"]
          }
        ]
      }
    ]
  }
}
```

#### Attack Scenario Development
- **Initial Access:** How attacker gains entry
- **Privilege Escalation:** Moving from basic to elevated access
- **Lateral Movement:** Expanding access within the environment
- **Data Exfiltration:** Extracting sensitive information
- **Impact Achievement:** Accomplishing attack objectives

#### Success Probability Calculation
- **Technical Feasibility:** Based on vulnerability exploitability
- **Detection Avoidance:** Likelihood of evading security controls
- **Resource Requirements:** Attacker capability vs. required resources
- **Time Windows:** Available exploitation windows

### Deliverables
- Attack trees and scenarios
- Attack path analysis
- Success probability assessments
- Critical path identification

---

## Phase 7: Risk Analysis

**Quantify risks and assess business impact**

### Objectives
- Calculate quantitative risk scores
- Assess likelihood and impact combinations
- Prioritize risks based on business impact
- Generate risk mitigation recommendations

### Key Activities

#### Risk Calculation Framework
```json
{
  "riskCalculation": {
    "factors": {
      "likelihood": {
        "Very Low": 1, "Low": 2, "Medium": 3, "High": 4, "Very High": 5
      },
      "impact": {
        "Very Low": 1, "Low": 2, "Medium": 3, "High": 4, "Very High": 5
      },
      "exploitability": {
        "Very Difficult": 1, "Difficult": 2, "Moderate": 3, "Easy": 4, "Very Easy": 5
      }
    },
    "formula": "Risk Score = (Likelihood × Impact × Exploitability) / 27",
    "interpretation": {
      "1-3": "Low Risk",
      "4-7": "Medium Risk",
      "8-12": "High Risk",
      "13-15": "Critical Risk"
    }
  }
}
```

#### Risk Assessment Matrix
| Likelihood →<br>Impact ↓ | Very Low (1) | Low (2) | Medium (3) | High (4) | Very High (5) |
|---------------------------|-------------|---------|-----------|----------|---------------|
| **Very Low (1)** | 1 (Low) | 2 (Low) | 3 (Low) | 4 (Med) | 5 (Med) |
| **Low (2)** | 2 (Low) | 4 (Med) | 6 (Med) | 8 (High) | 10 (High) |
| **Medium (3)** | 3 (Low) | 6 (Med) | 9 (High) | 12 (High) | 15 (Crit) |
| **High (4)** | 4 (Med) | 8 (High) | 12 (High) | 16 (Crit) | 20 (Crit) |
| **Very High (5)** | 5 (Med) | 10 (High) | 15 (Crit) | 20 (Crit) | 25 (Crit) |

#### Business Impact Assessment
- **Financial Impact:** Revenue loss, recovery costs, fines
- **Operational Impact:** Downtime, productivity loss, service degradation
- **Reputational Impact:** Brand damage, customer trust loss
- **Compliance Impact:** Regulatory violations, legal consequences

### Deliverables
- Quantitative risk scores
- Risk prioritization matrix
- Business impact analysis
- Mitigation recommendations

---

## Phase 8: Residual Risk Analysis

**Evaluate remaining risk after implementing mitigations**

### Objectives
- Assess effectiveness of proposed security controls
- Calculate residual risk levels after mitigation
- Determine risk acceptance criteria
- Develop ongoing monitoring and management strategies

### Key Activities

#### Residual Risk Calculation
```json
{
  "residualRisk": {
    "originalRisk": {
      "score": 15,
      "level": "Critical"
    },
    "mitigations": [
      {
        "control": "Input Validation",
        "effectiveness": 0.8,
        "residualRisk": 3
      },
      {
        "control": "Web Application Firewall",
        "effectiveness": 0.9,
        "residualRisk": 1.5
      }
    ],
    "finalResidualRisk": 1.5,
    "finalRiskLevel": "Low"
  }
}
```

#### Risk Acceptance Criteria
- **Accept:** Risk below organizational tolerance threshold
- **Mitigate:** Risk above tolerance, feasible controls available
- **Transfer:** Risk transferred to third party (insurance, outsourcing)
- **Avoid:** Risk unacceptable, activity discontinued

#### Ongoing Risk Management
- **Monitoring:** Continuous risk level tracking
- **Review Cycles:** Periodic reassessment of risk posture
- **Change Management:** Risk evaluation for system changes
- **Reporting:** Stakeholder communication of risk status

### Deliverables
- Residual risk assessment
- Risk treatment decisions
- Monitoring and review plan
- Risk management documentation

---

## Phase Artifacts & Deliverables

### Documentation Requirements
- **Phase 1:** Business objective analysis, security objective mapping
- **Phase 2:** Technical scope document, system architecture diagrams
- **Phase 3:** Component inventory, data flow diagrams, trust boundary maps
- **Phase 4:** Threat actor profiles, attack vector analysis
- **Phase 5:** Vulnerability inventory, exploitability assessments
- **Phase 6:** Attack trees, attack scenarios, success probability analysis
- **Phase 7:** Risk scores, prioritization matrix, business impact analysis
- **Phase 8:** Residual risk assessment, risk treatment plan

### Review and Approval
- **Peer Review:** Technical accuracy and completeness
- **Stakeholder Review:** Business alignment and risk tolerance
- **Management Approval:** Risk acceptance and resource commitment
- **Audit Trail:** Documentation of decisions and rationale

---

## Success Criteria

### Phase Completion Criteria
- **Phase 1:** Business objectives clearly defined and security objectives derived
- **Phase 2:** Technical scope documented with clear boundaries and assumptions
- **Phase 3:** All components identified and data flows mapped
- **Phase 4:** Threat actors profiled and motivations understood
- **Phase 5:** Vulnerabilities identified and exploitability assessed
- **Phase 6:** Attack scenarios developed and critical paths identified
- **Phase 7:** Risks quantified and prioritized based on business impact
- **Phase 8:** Residual risks assessed and treatment decisions made

### Quality Assurance
- **Completeness:** All required artifacts delivered
- **Accuracy:** Technical and business information correct
- **Consistency:** Methodology applied consistently across phases
- **Traceability:** Clear links between phases and decisions

---

## Common Challenges & Solutions

### Challenge: Business Stakeholder Engagement
**Solution:** Regular meetings, clear communication of security-business linkage, executive sponsorship

### Challenge: Technical Complexity
**Solution:** Break down complex systems into manageable components, use experienced architects

### Challenge: Resource Constraints
**Solution:** Prioritize high-risk components, use iterative approach, leverage existing artifacts

### Challenge: Changing Requirements
**Solution:** Establish change control process, regular scope reviews, flexible methodology adaptation

### Challenge: Risk Quantification
**Solution:** Use industry-standard scales, involve risk management experts, validate with historical data

---

## Navigation

| Previous | Current | Next |
|----------|---------|------|
| [[../index|PASTA Overview]] | PASTA Phases | [[./implementation|Implementation Guide]] |

## See Also

### Related Topics
- [[../index|PASTA Framework]] - Framework overview
- [[./risk-analysis|Risk Analysis Framework]] - Detailed risk calculation
- [[./business-alignment|Business Alignment]] - Linking security to business objectives

### Implementation Resources
- [[./template|PASTA Template]] - Ready-to-use template
- [[../../../workflows/examples/risk-assessment|Risk Assessment Workflows]] - Automation examples
- [[../../../resources/tools|Threat Modeling Tools]] - PASTA-compatible tools

---

**Tags:** #pasta-phases #threat-modeling-methodology #risk-analysis #business-alignment #enterprise-security

**Last Updated:** October 2025
**Version:** 1.0
**Reading Time:** 25 minutes
**Difficulty:** Advanced