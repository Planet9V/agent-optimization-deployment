# PASTA Threat Modeling Template
## Business-Aligned Risk-Centric Threat Analysis Template

**Version:** 1.0 - October 2025
**Focus:** Complete PASTA methodology template with business alignment
**Audience:** Security professionals conducting enterprise threat modeling

---

## Breadcrumb Navigation
[Home](../../../../index.md) > [Threat Modeling](../../../index.md) > [Methodologies](../../index.md) > [PASTA](../index.md) > Template

---

## Table of Contents

### Template Structure
- [[#phase-1-business-objectives|Phase 1: Define Business Objectives]]
- [[#phase-2-technical-scope|Phase 2: Define Technical Scope]]
- [[#phase-3-application-decomposition|Phase 3: Application Decomposition]]
- [[#phase-4-threat-analysis|Phase 4: Threat Analysis]]
- [[#phase-5-vulnerability-analysis|Phase 5: Vulnerability Analysis]]
- [[#phase-6-attack-modeling|Phase 6: Attack Modeling]]
- [[#phase-7-risk-analysis|Phase 7: Risk Analysis]]
- [[#phase-8-residual-risk|Phase 8: Residual Risk Analysis]]

---

## PASTA Threat Model Template

```markdown
# PASTA Threat Model: [Application Name]

## Executive Summary
[Provide a high-level overview of the threat modeling exercise, key findings, and recommendations]

**Application Name:** [Name of the application/system]
**Business Owner:** [Business stakeholder name]
**Security Lead:** [Security team lead]
**Date:** [Date of threat model creation]
**Review Date:** [Date for next review]

### Business Context
[Brief description of the application's business purpose and criticality]

### Key Findings
- **Overall Risk Level:** [Critical/High/Medium/Low]
- **Critical Risks:** [Number of critical risks identified]
- **High Risks:** [Number of high risks identified]
- **Primary Recommendations:** [Top 3 recommendations]

---

## Phase 1: Define Business Objectives

### Business Objectives
| Objective | Description | Priority | Success Metrics | Compliance Requirements |
|-----------|-------------|----------|-----------------|------------------------|
| [Objective 1] | [Description] | [Critical/High/Medium] | [Measurable metrics] | [GDPR, SOX, etc.] |

### Derived Security Objectives
| Security Objective | Business Alignment | Priority | Rationale |
|-------------------|-------------------|----------|-----------|
| [Security Objective] | [Linked business objective] | [Critical/High/Medium] | [Why this security objective matters] |

### Compliance Requirements
- [ ] [Compliance Framework 1] - [Specific requirements]
- [ ] [Compliance Framework 2] - [Specific requirements]

---

## Phase 2: Define Technical Scope

### System Overview
**Architecture Type:** [Web Application, API, Mobile App, etc.]
**Technology Stack:** [Languages, frameworks, databases]
**Deployment Model:** [On-premises, Cloud, Hybrid]
**User Base:** [Number of users, types of users]

### In-Scope Components
| Component | Type | Description | Trust Level | Criticality |
|-----------|------|-------------|-------------|-------------|
| [Component Name] | [Web Server/API/Database] | [Purpose and function] | [Internet/Intranet/Internal] | [High/Medium/Low] |

### Out-of-Scope Components
| Component | Reason for Exclusion | Risk Consideration |
|-----------|---------------------|-------------------|
| [Component Name] | [Reason] | [Risk if compromised] |

### Technical Constraints
- **Platform Limitations:** [Operating system, hardware constraints]
- **Integration Requirements:** [Third-party dependencies]
- **Performance Requirements:** [Availability, response time]
- **Compliance Constraints:** [Specific technical controls required]

### Assumptions
1. [Assumption 1 and potential impact if incorrect]
2. [Assumption 2 and potential impact if incorrect]

---

## Phase 3: Application Decomposition

### Entry Points
| Entry Point | Component | Authentication | Input Validation | Trust Level |
|-------------|-----------|----------------|------------------|-------------|
| [Entry Point] | [Component] | [Type of auth] | [Validation level] | [Trust level] |

### Exit Points
| Exit Point | Component | Data Type | Encryption | Trust Level |
|------------|-----------|-----------|------------|-------------|
| [Exit Point] | [Component] | [Data classification] | [Encryption method] | [Trust level] |

### Trust Boundaries
| Boundary Name | Source | Target | Security Controls | Crossing Points |
|---------------|--------|--------|------------------|----------------|
| [Boundary] | [Source component/level] | [Target component/level] | [Controls in place] | [APIs, networks, etc.] |

### Data Flows
| Source | Target | Data Type | Sensitivity | Encryption | Authentication |
|--------|--------|-----------|-------------|------------|----------------|
| [Source] | [Target] | [User data/PII/Financial] | [High/Medium/Low] | [TLS/None/Encrypted] | [Session/JWT/None] |

### Privilege Levels
| Level | Permissions | Description | User Types |
|-------|-------------|-------------|------------|
| Public | [Read public data] | [Unauthenticated users] | [Visitors, crawlers] |
| User | [Read, write own data] | [Authenticated users] | [Customers, employees] |
| Admin | [Full access] | [System administrators] | [IT staff, managers] |

---

## Phase 4: Threat Analysis

### Threat Actor Profiles
| Actor Name | Type | Motivation | Capability | Resources | Likelihood |
|------------|------|------------|------------|-----------|------------|
| [Actor] | [External/Internal] | [Financial/Espionage] | [High/Medium/Low] | [High/Medium/Low] | [High/Medium/Low] |

### Attack Vectors
| Attack Vector | Entry Point | Techniques | Prerequisites | Detection Difficulty |
|---------------|-------------|------------|----------------|-------------------|
| [Vector] | [Entry point] | [SQLi, XSS, etc.] | [Requirements] | [High/Medium/Low] |

### Attack Motivations
| Motivation | Description | Business Impact | Likelihood |
|------------|-------------|-----------------|------------|
| [Motivation] | [Description] | [Financial, Reputational] | [High/Medium/Low] |

### Actor Capabilities
| Actor | Technical Skills | Available Resources | Persistence | Detection Evasion |
|-------|-----------------|---------------------|-------------|------------------|
| [Actor] | [Skill level] | [Time, tools, money] | [Opportunistic/Targeted] | [High/Medium/Low] |

---

## Phase 5: Vulnerability Analysis

### Identified Vulnerabilities
| ID | Component | Vulnerability Type | Severity | CWE | Description |
|----|-----------|-------------------|----------|-----|-------------|
| VULN-001 | [Component] | [SQL Injection] | [Critical/High/Medium] | [CWE-89] | [Description] |

### Exploitability Assessment
| Vulnerability ID | Technical Complexity | Resource Requirements | Detection Risk | Remediation Time |
|------------------|---------------------|----------------------|----------------|------------------|
| VULN-001 | [High/Medium/Low] | [High/Medium/Low] | [High/Medium/Low] | [Days/Weeks/Months] |

### Existing Security Controls
| Control Type | Control Name | Coverage | Effectiveness | Gaps Identified |
|--------------|--------------|----------|----------------|----------------|
| [Preventive/Detective] | [Control name] | [Components covered] | [High/Medium/Low] | [Identified gaps] |

### Control Gaps
| Gap | Affected Components | Risk Impact | Remediation Priority |
|-----|-------------------|-------------|---------------------|
| [Gap description] | [Components] | [High/Medium/Low] | [Critical/High/Medium] |

---

## Phase 6: Attack Modeling

### Attack Trees

#### Primary Attack Tree: [Main Attack Goal]
```
[Attack Goal]
├── [Attack Vector 1] (Probability: X%)
│   ├── [Sub-technique 1.1] (Probability: Y%)
│   └── [Sub-technique 1.2] (Probability: Z%)
└── [Attack Vector 2] (Probability: A%)
    ├── [Sub-technique 2.1] (Probability: B%)
    └── [Sub-technique 2.2] (Probability: C%)
```

### Attack Scenarios
| Scenario ID | Description | Entry Point | Attack Progression | Success Probability |
|-------------|-------------|-------------|-------------------|-------------------|
| ATTACK-001 | [Scenario description] | [Entry point] | [Step-by-step progression] | [High/Medium/Low] |

### Critical Attack Paths
| Path ID | Description | Components Involved | Required Skills | Estimated Time |
|---------|-------------|-------------------|----------------|----------------|
| PATH-001 | [Path description] | [Components] | [Skill requirements] | [Time estimate] |

### Attack Success Factors
- **Technical Feasibility:** [Assessment of technical requirements]
- **Resource Availability:** [Attacker resources vs. requirements]
- **Detection Avoidance:** [Likelihood of detection during attack]
- **Time Windows:** [Available exploitation windows]

---

## Phase 7: Risk Analysis

### Risk Scoring Methodology
**Formula:** Risk Score = (Likelihood × Impact × Exploitability) ÷ 27

**Scale Interpretation:**
- **1-2:** Low Risk - Monitor and accept
- **3-4:** Medium Risk - Plan mitigation
- **5-7:** High Risk - Implement mitigation
- **8-9:** Critical Risk - Immediate action required

### Risk Assessment Matrix
| Scenario | Likelihood | Impact | Exploitability | Risk Score | Risk Level | Business Impact |
|----------|------------|--------|---------------|------------|------------|-----------------|
| [Scenario] | [1-5] | [1-5] | [1-5] | [Calculated] | [Level] | [Financial, Reputational] |

### Risk Prioritization
| Priority | Risk Scenarios | Count | Mitigation Timeline | Business Justification |
|----------|----------------|-------|-------------------|----------------------|
| Critical | [List scenarios] | [Count] | [Immediate] | [Business impact] |
| High | [List scenarios] | [Count] | [Within 90 days] | [Business impact] |
| Medium | [List scenarios] | [Count] | [Within 6 months] | [Business impact] |

### Business Impact Analysis
| Risk Scenario | Financial Impact | Operational Impact | Reputational Impact | Compliance Impact |
|---------------|------------------|-------------------|-------------------|------------------|
| [Scenario] | [Cost estimate] | [Downtime, productivity] | [Brand damage] | [Violation consequences] |

---

## Phase 8: Residual Risk Analysis

### Original vs. Residual Risk
| Risk Scenario | Original Risk | Mitigation Applied | Residual Risk | Risk Reduction |
|---------------|---------------|-------------------|---------------|----------------|
| [Scenario] | [Original level] | [Control implemented] | [Residual level] | [Percentage reduction] |

### Risk Treatment Decisions
| Risk Scenario | Treatment | Rationale | Owner | Timeline |
|---------------|-----------|-----------|-------|----------|
| [Scenario] | [Accept/Mitigate/Transfer/Avoid] | [Justification] | [Responsible person] | [Implementation timeline] |

### Monitoring and Review Plan
| Risk Scenario | Monitoring Method | Frequency | Responsible Party | Escalation Criteria |
|---------------|-------------------|-----------|-------------------|-------------------|
| [Scenario] | [Logs, alerts, testing] | [Daily/Weekly/Monthly] | [Team/Person] | [When to escalate] |

### Risk Acceptance Criteria
- **Acceptable Risk Levels:** [Define acceptable thresholds]
- **Review Triggers:** [When to reassess risk levels]
- **Change Management:** [How changes affect risk assessment]
- **Reporting Requirements:** [Stakeholder communication frequency]

---

## Recommendations

### Immediate Actions (Next 30 Days)
1. **Priority 1:** [Critical mitigation action]
   - **Rationale:** [Why this is critical]
   - **Owner:** [Responsible person/team]
   - **Resources Required:** [Budget, personnel, tools]
   - **Success Criteria:** [How to measure completion]

2. **Priority 2:** [High-priority mitigation action]
   - **Rationale:** [Why this is high priority]
   - **Owner:** [Responsible person/team]
   - **Resources Required:** [Budget, personnel, tools]
   - **Success Criteria:** [How to measure completion]

### Short-term Actions (30-90 Days)
1. [Medium-priority action 1]
2. [Medium-priority action 2]
3. [Medium-priority action 3]

### Long-term Actions (90+ Days)
1. [Process improvement 1]
2. [Technology investment 1]
3. [Training requirement 1]

### Process Improvements
- **Threat Modeling Integration:** [How to incorporate into SDLC]
- **Training Requirements:** [Skills development needed]
- **Tool Acquisition:** [Security tools to implement]
- **Metrics and Reporting:** [Success measurement approach]

---

## Implementation Roadmap

### Phase 1: Immediate (Weeks 1-4)
| Week | Activity | Owner | Status |
|------|----------|-------|--------|
| 1 | [Activity 1] | [Owner] | [Not Started/In Progress/Complete] |
| 2 | [Activity 2] | [Owner] | [Not Started/In Progress/Complete] |
| 3 | [Activity 3] | [Owner] | [Not Started/In Progress/Complete] |
| 4 | [Activity 4] | [Owner] | [Not Started/In Progress/Complete] |

### Phase 2: Short-term (Months 2-3)
| Month | Activity | Owner | Status |
|-------|----------|-------|--------|
| 2 | [Activity 1] | [Owner] | [Not Started/In Progress/Complete] |
| 3 | [Activity 2] | [Owner] | [Not Started/In Progress/Complete] |

### Phase 3: Long-term (Months 4-6)
| Month | Activity | Owner | Status |
|-------|----------|-------|--------|
| 4 | [Activity 1] | [Owner] | [Not Started/In Progress/Complete] |
| 5 | [Activity 2] | [Owner] | [Not Started/In Progress/Complete] |
| 6 | [Activity 3] | [Owner] | [Not Started/In Progress/Complete] |

---

## Review and Approval

### Review Checklist
- [ ] Business objectives clearly defined and aligned with security objectives
- [ ] Technical scope properly bounded with clear assumptions
- [ ] Application decomposition complete with all components identified
- [ ] Threat analysis covers relevant actor types and motivations
- [ ] Vulnerability analysis includes exploitability assessments
- [ ] Attack modeling provides realistic scenarios and probabilities
- [ ] Risk analysis uses quantitative methods with business impact
- [ ] Residual risk analysis includes monitoring and review plans
- [ ] Recommendations are prioritized and actionable
- [ ] Implementation roadmap includes timelines and owners

### Stakeholder Sign-off
| Role | Name | Date | Comments |
|------|------|------|----------|
| Business Owner | [Name] | [Date] | [Comments] |
| Security Lead | [Name] | [Date] | [Comments] |
| Technical Lead | [Name] | [Date] | [Comments] |
| Compliance Officer | [Name] | [Date] | [Comments] |

### Document Control
- **Version:** 1.0
- **Next Review Date:** [Date - typically 6-12 months]
- **Document Owner:** [Security Team]
- **Distribution:** [Authorized personnel only]
- **Classification:** [Internal/Confidential]

---

## Appendices

### Appendix A: Detailed Risk Calculations
[Include detailed risk score calculations and assumptions]

### Appendix B: Attack Tree Diagrams
[Include visual attack tree diagrams]

### Appendix C: Compliance Mapping
[Map security controls to specific compliance requirements]

### Appendix D: Assumptions and Constraints
[Detailed list of all assumptions made during analysis]

### Appendix E: Glossary
[Definitions of technical terms and acronyms used]
```

---

## Template Usage Guide

### Getting Started
1. **Copy the template** to a new file with your application name
2. **Fill Phase 1** with business stakeholders to ensure alignment
3. **Complete Phase 2** with technical team for scope definition
4. **Work through Phases 3-7** systematically with security team
5. **Finalize Phase 8** with risk acceptance decisions

### Best Practices
- **Business First:** Always start with business objectives, not technical details
- **Iterative Approach:** Don't try to complete all phases at once
- **Stakeholder Involvement:** Include business owners throughout the process
- **Quantitative Analysis:** Use actual numbers for likelihood and impact
- **Actionable Results:** Focus on recommendations that can be implemented

### Common Pitfalls
- **Technical Focus:** Don't get lost in technical details without business context
- **Over-Analysis:** Avoid analysis paralysis - make decisions and move forward
- **Scope Creep:** Stick to defined boundaries and assumptions
- **Generic Threats:** Use specific, realistic threats based on your environment
- **No Follow-through:** Ensure recommendations lead to actual implementation

---

## Navigation

| Previous | Current | Next |
|----------|---------|------|
| [[./implementation|Implementation Guide]] | PASTA Template | [[./case-studies|Case Studies]] |

## See Also

### Related Templates
- [[../../stride/template|STRIDE Template]] - Technical threat identification
- [[../../octave/template|OCTAVE Template]] - Organizational risk assessment
- [[../../trike/template|Trike Template]] - Requirements-driven analysis

### Implementation Resources
- [[./phases|PASTA Phases]] - Detailed methodology breakdown
- [[./risk-analysis|Risk Analysis Framework]] - Quantitative risk methods
- [[../../../workflows/examples/risk-assessment|Risk Assessment Workflows]] - Automation examples

---

**Tags:** #pasta-template #threat-modeling-template #business-alignment #risk-analysis #enterprise-security

**Last Updated:** October 2025
**Version:** 1.0
**Reading Time:** 30 minutes
**Difficulty:** Advanced