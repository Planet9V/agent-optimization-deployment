# Trike Threat Modeling Template
## Requirements-Driven Security Analysis with Quantitative Risk Assessment

**Version:** 1.0 - October 2025
**Focus:** Complete Trike methodology template with requirements traceability
**Audience:** Security architects and requirements engineers conducting Trike assessments

---

## Breadcrumb Navigation
[Home](../../../../index.md) > [Threat Modeling](../../../index.md) > [Methodologies](../../index.md) > [Trike](../index.md) > Template

---

## Table of Contents

### Template Structure
- [[#executive-summary|Executive Summary]]
- [[#phase-1-requirements|Phase 1: Requirements Definition]]
- [[#phase-2-system-modeling|Phase 2: System Modeling]]
- [[#phase-3-threat-identification|Phase 3: Threat Identification]]
- [[#phase-4-mitigation-design|Phase 4: Mitigation Design]]

---

## Trike Threat Model Template

```markdown
# Trike Threat Model: [System Name]

## Executive Summary

### Assessment Overview
- **System Name:** [Name of the system being modeled]
- **Assessment Date:** [Date of threat model creation]
- **Methodology:** Trike (Requirements-driven, risk-based threat modeling)
- **Lead Analyst:** [Name and role of person conducting analysis]
- **Requirements Source:** [Document or system where requirements are defined]

### Key Findings
- **Total Requirements Analyzed:** [Number]
- **Critical Requirements:** [Number]
- **Threats Identified:** [Number]
- **High-Risk Threats:** [Number]
- **Mitigations Designed:** [Number]

### Risk Summary
- **Overall Risk Level:** [Critical/High/Medium/Low]
- **Highest Risk Category:** [Confidentiality/Integrity/Availability/Accountability]
- **Requirements Coverage:** [Percentage of requirements addressed]
- **Implementation Priority:** [Immediate/Short-term/Long-term]

### Recommendations
1. [Top recommendation based on risk analysis]
2. [Second priority recommendation]
3. [Third priority recommendation]

---

## Phase 1: Requirements Definition

### Security Requirements Inventory

| Requirement ID | Category | Description | Priority | Rationale | Validation Criteria | Status |
|----------------|----------|-------------|----------|-----------|---------------------|--------|
| REQ-CONF-001 | Confidentiality | [Specific requirement description] | [Critical/High/Medium/Low] | [Business justification] | [How to verify requirement is met] | [Defined/Validated/Implemented] |

### Requirements Categories Summary

#### Confidentiality Requirements
| ID | Description | Priority | Related Business Requirements |
|----|-------------|----------|-------------------------------|
| REQ-CONF-001 | [Description] | [Priority] | [Business requirement link] |

#### Integrity Requirements
| ID | Description | Priority | Related Business Requirements |
|----|-------------|----------|-------------------------------|
| REQ-INTEG-001 | [Description] | [Priority] | [Business requirement link] |

#### Availability Requirements
| ID | Description | Priority | Related Business Requirements |
|----|-------------|----------|-------------------------------|
| REQ-AVAIL-001 | [Description] | [Priority] | [Business requirement link] |

#### Accountability Requirements
| ID | Description | Priority | Related Business Requirements |
|----|-------------|----------|-------------------------------|
| REQ-ACCT-001 | [Description] | [Priority] | [Business requirement link] |

### Requirements Dependencies

| Requirement ID | Depends On | Dependent Requirements | Rationale |
|----------------|------------|----------------------|-----------|
| REQ-CONF-001 | [Prerequisite requirements] | [Requirements that depend on this one] | [Why this dependency exists] |

### Requirements Traceability Matrix

| Requirement ID | Description | Source Document | Business Objective | Test Cases | Implementation Status |
|----------------|-------------|-----------------|-------------------|------------|---------------------|
| REQ-CONF-001 | [Description] | [Document reference] | [Business objective] | [Test case IDs] | [Not Started/In Progress/Complete] |

---

## Phase 2: System Modeling

### System Components

| Component ID | Component Name | Type | Trust Level | Description | Interfaces | Criticality |
|--------------|----------------|------|-------------|-------------|------------|-------------|
| COMP-001 | [Component Name] | [Web Server/Database/API/etc.] | [Untrusted/Limited/Trusted/High] | [Purpose and function] | [HTTP/API/Database] | [High/Medium/Low] |

### Trust Boundaries

| Boundary ID | Component 1 | Component 2 | Trust Level 1 | Trust Level 2 | Interaction Type | Security Requirements |
|-------------|-------------|-------------|---------------|---------------|------------------|----------------------|
| BOUNDARY-001 | [Component 1] | [Component 2] | [Trust level] | [Trust level] | [Network/Application/Data] | [Authentication/Encryption/etc.] |

### Data Flows

| Flow ID | Source Component | Target Component | Data Type | Sensitivity | Encryption | Authentication | Trust Boundary Crossed |
|---------|------------------|------------------|-----------|-------------|------------|----------------|----------------------|
| FLOW-001 | [Source] | [Target] | [User data/PII/Financial] | [High/Medium/Low] | [Yes/No] | [Yes/No] | [Yes/No] |

### Privilege Levels

| Level | Description | Permissions | User Types | Access Scope |
|-------|-------------|-------------|------------|--------------|
| Public | [Unauthenticated users] | [Read public data] | [Visitors, crawlers] | [Limited to public resources] |
| User | [Authenticated users] | [Read/write own data] | [Customers, employees] | [User-specific resources] |
| Admin | [System administrators] | [Full system access] | [IT administrators] | [All system resources] |

### Component Capabilities Matrix

| Component ID | Capability | Description | Trust Boundary Impact | Security Implications |
|--------------|------------|-------------|----------------------|----------------------|
| COMP-001 | [Capability] | [Description] | [Boundary crossed] | [Security considerations] |

---

## Phase 3: Threat Identification

### Threat Analysis Results

| Threat ID | Boundary ID | Category | Description | Violated Requirements | Attacker Skill | Attacker Motive | Attacker Opportunity | Control Strength | Implementation Quality | Risk Score | Risk Level |
|-----------|-------------|----------|-------------|----------------------|----------------|-----------------|----------------------|------------------|----------------------|------------|------------|
| THREAT-001 | BOUNDARY-001 | [Confidentiality/Integrity/Availability/Accountability] | [Threat description] | [REQ-XXX, REQ-YYY] | [1-9] | [0-8] | [0-8] | [1-5] | [1-5] | [Calculated] | [Critical/High/Medium/Low/Very Low] |

### Risk Calculation Details

#### Attacker Factor Calculations
**Formula:** Attacker Skill × Attacker Motive × Attacker Opportunity

| Threat ID | Skill Level | Skill Value | Motive Level | Motive Value | Opportunity Level | Opportunity Value | Attacker Factor |
|-----------|-------------|-------------|--------------|--------------|-------------------|-------------------|----------------|
| THREAT-001 | [Novice/Intermediate/Advanced/Expert/Multiple Experts] | [1/3/5/7/9] | [None/Low/Moderate/High/Extreme] | [0/2/4/6/8] | [None/Low/Moderate/High/Extreme] | [0/2/4/6/8] | [Calculated] |

#### Control Factor Calculations
**Formula:** Control Strength × Implementation Quality

| Threat ID | Control Strength | Strength Value | Implementation Quality | Quality Value | Control Factor |
|-----------|------------------|----------------|------------------------|---------------|----------------|
| THREAT-001 | [None/Weak/Moderate/Strong/Complete] | [1/2/3/4/5] | [Poor/Fair/Good/Excellent/Perfect] | [1/2/3/4/5] | [Calculated] |

#### Risk Score Calculations
**Formula:** Attacker Factor ÷ Control Factor

| Threat ID | Attacker Factor | Control Factor | Risk Score | Risk Level | Interpretation |
|-----------|-----------------|----------------|------------|------------|----------------|
| THREAT-001 | [Value] | [Value] | [Calculated] | [Level] | [Accept/Monitor/Mitigate/Address Immediately] |

### Threat Prioritization

| Priority | Risk Level | Threat Count | Description | Recommended Action |
|----------|------------|--------------|-------------|-------------------|
| 1 | Critical | [Count] | Risk score ≥ 5.0 | Immediate mitigation required |
| 2 | High | [Count] | Risk score 3.0-4.9 | Mitigation within 30 days |
| 3 | Medium | [Count] | Risk score 2.0-2.9 | Mitigation within 90 days |
| 4 | Low | [Count] | Risk score 1.0-1.9 | Monitor and review |
| 5 | Very Low | [Count] | Risk score < 1.0 | Accept current risk level |

### Requirements-Threat Traceability

| Requirement ID | Description | Related Threats | Threat Count | Coverage Status |
|----------------|-------------|-----------------|--------------|----------------|
| REQ-CONF-001 | [Description] | [THREAT-001, THREAT-002] | [Count] | [Fully Covered/Partially Covered/Not Covered] |

---

## Phase 4: Mitigation Design

### Mitigation Specifications

| Mitigation ID | Threat ID | Description | Type | Category | Satisfied Requirements | Implementation Approach | Effectiveness Rating | Dependencies | Timeline | Cost Estimate |
|---------------|-----------|-------------|------|----------|----------------------|----------------------|---------------------|--------------|----------|--------------|
| MITIG-001 | THREAT-001 | [Mitigation description] | [Technical/Operational/Administrative] | [Preventive/Detective/Corrective/Deterrent] | [REQ-XXX, REQ-YYY] | [Specific implementation steps] | [High/Medium/Low] | [Prerequisite mitigations] | [Duration] | [Cost range] |

### Requirements-Mitigation Traceability

| Requirement ID | Description | Mitigation ID | Mitigation Description | Validation Method | Status |
|----------------|-------------|---------------|----------------------|------------------|--------|
| REQ-CONF-001 | [Description] | MITIG-001 | [Description] | [Test case/Review/Audit] | [Designed/Implemented/Validated] |

### Implementation Plan

#### Immediate Actions (0-30 days)
| Mitigation ID | Description | Owner | Resources Required | Success Criteria | Dependencies |
|---------------|-------------|-------|-------------------|------------------|--------------|
| MITIG-001 | [Description] | [Person/Team] | [Budget/Personnel/Tools] | [Measurable criteria] | [Prerequisites] |

#### Short-term Actions (1-3 months)
| Mitigation ID | Description | Owner | Resources Required | Success Criteria | Dependencies |
|---------------|-------------|-------|-------------------|------------------|--------------|
| MITIG-002 | [Description] | [Person/Team] | [Budget/Personnel/Tools] | [Measurable criteria] | [Prerequisites] |

#### Long-term Actions (3-6 months)
| Mitigation ID | Description | Owner | Resources Required | Success Criteria | Dependencies |
|---------------|-------------|-------|-------------------|------------------|--------------|
| MITIG-003 | [Description] | [Person/Team] | [Budget/Personnel/Tools] | [Measurable criteria] | [Prerequisites] |

### Control Validation Framework

| Mitigation ID | Validation Method | Test Case ID | Expected Result | Success Criteria | Review Frequency |
|---------------|-------------------|--------------|-----------------|------------------|------------------|
| MITIG-001 | [Manual Testing/Automated Testing/Code Review] | [TC-001] | [Expected behavior] | [Pass criteria] | [Daily/Weekly/Monthly] |

### Residual Risk Assessment

| Threat ID | Original Risk Score | Mitigation ID | Expected Risk Reduction | Residual Risk Score | Residual Risk Level | Monitoring Requirements |
|-----------|---------------------|---------------|------------------------|-------------------|-------------------|----------------------|
| THREAT-001 | [Original] | MITIG-001 | [Percentage reduction] | [Calculated] | [Level] | [Monitoring approach] |

---

## Analysis Summary

### Coverage Analysis

#### Requirements Coverage
- **Total Requirements:** [Number]
- **Requirements with Mitigations:** [Number]
- **Coverage Percentage:** [Percentage]
- **Gaps Identified:** [Number of requirements without mitigations]

#### Threat Coverage
- **Total Threats Identified:** [Number]
- **Threats with Mitigations:** [Number]
- **Coverage Percentage:** [Percentage]
- **Unmitigated Threats:** [Number]

#### Implementation Coverage
- **Total Mitigations Designed:** [Number]
- **Mitigations Implemented:** [Number]
- **Implementation Percentage:** [Percentage]
- **Pending Implementations:** [Number]

### Risk Distribution

| Risk Level | Threat Count | Percentage | Mitigation Status | Business Impact |
|------------|--------------|------------|-------------------|-----------------|
| Critical | [Count] | [Percentage] | [All mitigated/Partial mitigation/None] | [High business impact] |
| High | [Count] | [Percentage] | [All mitigated/Partial mitigation/None] | [Moderate business impact] |
| Medium | [Count] | [Percentage] | [All mitigated/Partial mitigation/None] | [Low business impact] |
| Low | [Count] | [Percentage] | [All mitigated/Partial mitigation/None] | [Minimal business impact] |

### Success Metrics

| Metric Category | Metric | Baseline | Target | Current Status | Measurement Method |
|-----------------|--------|----------|--------|----------------|-------------------|
| Requirements | Requirements coverage | [Baseline %] | [Target %] | [Current %] | [Measurement approach] |
| Threats | Threats mitigated | [Baseline count] | [Target count] | [Current count] | [Measurement approach] |
| Risk | Risk score reduction | [Baseline score] | [Target score] | [Current score] | [Measurement approach] |

---

## Recommendations

### Immediate Priorities (Next 30 Days)
1. **Implement Critical Mitigations**
   - Address all threats with risk scores ≥ 5.0
   - Focus on confidentiality and integrity violations
   - Validate mitigation effectiveness immediately

2. **Update Requirements Traceability**
   - Ensure all mitigations are linked to requirements
   - Update traceability matrix with implementation status
   - Establish automated traceability reporting

3. **Establish Monitoring Baseline**
   - Implement monitoring for critical controls
   - Set up alerting for security violations
   - Document normal operational patterns

### Short-term Actions (1-3 Months)
1. **Complete High-Risk Mitigations**
   - Address threats with risk scores 3.0-4.9
   - Implement layered security controls
   - Conduct security testing and validation

2. **Enhance Security Monitoring**
   - Deploy comprehensive logging and monitoring
   - Implement security information and event management (SIEM)
   - Establish incident response procedures

3. **Security Awareness Training**
   - Train development teams on secure coding practices
   - Educate operations staff on security monitoring
   - Establish security champions program

### Long-term Strategies (3-6 Months)
1. **Process Integration**
   - Integrate Trike methodology into SDLC
   - Establish automated threat modeling workflows
   - Create security requirements templates

2. **Technology Investments**
   - Implement security tooling and automation
   - Upgrade infrastructure security controls
   - Deploy advanced threat detection capabilities

3. **Continuous Improvement**
   - Establish regular threat model updates
   - Conduct annual comprehensive reassessments
   - Monitor threat landscape evolution

---

## Review and Approval

### Analysis Review Checklist
- [ ] All security requirements clearly defined and categorized
- [ ] System components and trust boundaries properly modeled
- [ ] Threats identified for all trust boundary crossings
- [ ] Risk calculations performed using correct formulas
- [ ] Mitigations designed for all high and critical risks
- [ ] Requirements traceability maintained throughout
- [ ] Implementation plan includes timelines and owners
- [ ] Residual risk assessment completed
- [ ] Recommendations prioritized and actionable

### Stakeholder Sign-off

| Role | Name | Signature | Date | Comments |
|------|------|-----------|------|----------|
| Security Lead | [Name] | _______________ | ____ | [Comments] |
| Requirements Owner | [Name] | _______________ | ____ | [Comments] |
| System Owner | [Name] | _______________ | ____ | [Comments] |
| Business Owner | [Name] | _______________ | ____ | [Comments] |

### Document Control
- **Version:** 1.0
- **Next Review Date:** [Date - typically 6 months after implementation]
- **Document Owner:** [Security Team]
- **Distribution:** [Authorized personnel only]
- **Classification:** [Internal/Confidential]

---

## Appendices

### Appendix A: Detailed Risk Calculations
[Complete risk calculation worksheets with all formulas and assumptions]

### Appendix B: Requirements Traceability Matrix
[Complete traceability matrix showing all links between requirements, threats, and mitigations]

### Appendix C: System Architecture Diagrams
[Visual representations of system components and trust boundaries]

### Appendix D: Threat Analysis Details
[Detailed analysis of each threat including attacker profiles and control assessments]

### Appendix E: Mitigation Implementation Details
[Detailed implementation plans for each mitigation including code examples and testing procedures]

### Appendix F: Test Cases and Validation Procedures
[Complete test cases for validating mitigation effectiveness]

### Appendix G: Assumptions and Limitations
[All assumptions made during analysis and limitations of the threat model]

### Appendix H: Glossary and Definitions
[Definitions of all technical terms and acronyms used in the document]
```

---

## Template Usage Guide

### Preparation Phase
1. **Requirements Gathering:** Collect all security requirements from stakeholders
2. **System Documentation:** Gather architecture diagrams and component details
3. **Team Assembly:** Identify analysts and reviewers for the assessment
4. **Tool Setup:** Prepare spreadsheets for risk calculations

### Analysis Execution
1. **Phase 1:** Define and categorize all security requirements
2. **Phase 2:** Model system components and trust boundaries
3. **Phase 3:** Identify threats and calculate quantitative risks
4. **Phase 4:** Design mitigations with requirements traceability

### Quality Assurance
1. **Peer Review:** Have security experts review threat analysis
2. **Requirements Validation:** Confirm all requirements are properly addressed
3. **Risk Validation:** Verify risk calculations and assumptions
4. **Traceability Audit:** Ensure all links are maintained and accurate

---

## Navigation

| Previous | Current | Next |
|----------|---------|------|
| [[./implementation|Implementation Guide]] | Trike Template | [[./case-studies|Case Studies]] |

## See Also

### Related Templates
- [[../../stride/template|STRIDE Template]] - Technical threat identification
- [[../../pasta/template|PASTA Template]] - Business risk-focused template
- [[../../octave/template|OCTAVE Template]] - Organizational assessment template

### Implementation Resources
- [[./phases|Trike Phases]] - Detailed methodology breakdown
- [[./requirements|Requirements Analysis]] - Security requirements framework
- [[../../../workflows/examples/compliance-monitoring|Compliance Workflows]] - Integration examples

---

**Tags:** #trike-template #requirements-driven #quantitative-risk #threat-modeling-template #security-analysis

**Last Updated:** October 2025
**Version:** 1.0
**Reading Time:** 30 minutes
**Difficulty:** Advanced