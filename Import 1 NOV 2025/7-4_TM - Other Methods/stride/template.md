# STRIDE Threat Modeling Template
## Ready-to-Use Template for Systematic Threat Analysis

**Version:** 1.0 - October 2025
**Focus:** Complete STRIDE threat modeling template with examples
**Audience:** Security professionals conducting threat modeling exercises

---

## Breadcrumb Navigation
[Home](../../../../index.md) > [Threat Modeling](../../../index.md) > [Methodologies](../../index.md) > [STRIDE](../index.md) > Template

---

## Template Overview

This template provides a structured approach to conducting STRIDE threat modeling. It includes all necessary sections for comprehensive threat analysis and mitigation planning.

### Template Structure
1. **System Overview** - Basic system information
2. **System Description** - Detailed system context
3. **System Components** - Component inventory
4. **Data Flows** - Data movement analysis
5. **Trust Boundaries** - Security domain boundaries
6. **Threat Analysis** - STRIDE-based threat identification
7. **Risk Assessment** - Threat prioritization
8. **Mitigation Strategy** - Control implementation
9. **Recommendations** - Additional guidance
10. **Review Process** - Quality assurance

---

## STRIDE Threat Model Template

```markdown
# STRIDE Threat Model: [System Name]

## 1. System Overview
- **System Name:** [Name of the system being modeled]
- **Version:** [System version or release]
- **Date:** [Date of threat model creation]
- **Modeler:** [Name and role of person creating the model]
- **Reviewers:** [Names and roles of reviewers]
- **Scope:** [What parts of the system are included in this model]

## 2. System Description
[Provide a brief description of the system and its purpose]

**Key Features:**
- [Feature 1]
- [Feature 2]
- [Feature 3]

**Architecture Overview:**
- [High-level architecture description]
- [Technology stack]
- [Deployment model (on-premises, cloud, hybrid)]

**Security Requirements:**
- [Confidentiality requirements]
- [Integrity requirements]
- [Availability requirements]
- [Authentication requirements]
- [Authorization requirements]

## 3. System Components
| Component | Type | Description | Trust Level | Criticality |
|-----------|------|-------------|-------------|-------------|
| [Component Name] | [Web Server/API/Database/etc.] | [Purpose and function] | [Internet/Intranet/Internal] | [High/Medium/Low] |

**Component Types Legend:**
- **External Entity:** Users, systems, or services outside the system boundary
- **Process:** Application logic, business rules, data processing
- **Data Store:** Databases, file systems, caches, configuration stores
- **Data Flow:** Communication between components
- **Trust Boundary:** Security domain boundaries
- **Interaction:** User interface elements

## 4. Data Flows
| Source Component | Target Component | Data Type | Protocol | Authentication | Encryption | Trust Boundary Crossed |
|------------------|------------------|-----------|----------|----------------|------------|----------------------|
| [Source] | [Target] | [User data/PII/Financial/etc.] | [HTTP/HTTPS/TCP/etc.] | [Yes/No] | [Yes/No] | [Yes/No] |

**Data Classification:**
- **Public:** No restrictions on disclosure
- **Internal:** Limited to organization employees
- **Confidential:** Limited disclosure, business impact if compromised
- **Restricted:** Severe impact if compromised (PII, financial data, etc.)

## 5. Trust Boundaries
[List and describe all trust boundaries in the system]

### Boundary 1: [Boundary Name]
- **Description:** [What separates the boundary]
- **Components on each side:** [List components]
- **Security controls:** [Authentication, authorization, encryption]
- **Crossing points:** [APIs, network segments, etc.]

### Boundary 2: [Boundary Name]
- **Description:** [What separates the boundary]
- **Components on each side:** [List components]
- **Security controls:** [Authentication, authorization, encryption]
- **Crossing points:** [APIs, network segments, etc.]

## 6. Threats Identified

### Spoofing Threats
**STRIDE Category: Spoofing (Authentication Violation)**

| ID | Component | Threat Description | Impact | Likelihood | Risk Level | Mitigations |
|----|-----------|-------------------|--------|------------|------------|-------------|
| STRIDE_S_001 | [Component] | [Description] | [High/Med/Low] | [High/Med/Low] | [Critical/High/Med/Low] | [List of controls] |

### Tampering Threats
**STRIDE Category: Tampering (Integrity Violation)**

| ID | Component | Threat Description | Impact | Likelihood | Risk Level | Mitigations |
|----|-----------|-------------------|--------|------------|------------|-------------|
| STRIDE_T_001 | [Component] | [Description] | [High/Med/Low] | [High/Med/Low] | [Critical/High/Med/Low] | [List of controls] |

### Repudiation Threats
**STRIDE Category: Repudiation (Non-repudiation Violation)**

| ID | Component | Threat Description | Impact | Likelihood | Risk Level | Mitigations |
|----|-----------|-------------------|--------|------------|------------|-------------|
| STRIDE_R_001 | [Component] | [Description] | [High/Med/Low] | [High/Med/Low] | [Critical/High/Med/Low] | [List of controls] |

### Information Disclosure Threats
**STRIDE Category: Information Disclosure (Confidentiality Violation)**

| ID | Component | Threat Description | Impact | Likelihood | Risk Level | Mitigations |
|----|-----------|-------------------|--------|------------|------------|-------------|
| STRIDE_I_001 | [Component] | [Description] | [High/Med/Low] | [High/Med/Low] | [Critical/High/Med/Low] | [List of controls] |

### Denial of Service Threats
**STRIDE Category: Denial of Service (Availability Violation)**

| ID | Component | Threat Description | Impact | Likelihood | Risk Level | Mitigations |
|----|-----------|-------------------|--------|------------|------------|-------------|
| STRIDE_D_001 | [Component] | [Description] | [High/Med/Low] | [High/Med/Low] | [Critical/High/Med/Low] | [List of controls] |

### Elevation of Privilege Threats
**STRIDE Category: Elevation of Privilege (Authorization Violation)**

| ID | Component | Threat Description | Impact | Likelihood | Risk Level | Mitigations |
|----|-----------|-------------------|--------|------------|------------|-------------|
| STRIDE_E_001 | [Component] | [Description] | [High/Med/Low] | [High/Med/Low] | [Critical/High/Med/Low] | [List of controls] |

## 7. Risk Assessment

### Risk Scoring Methodology
- **Impact Levels:**
  - **Critical:** System compromise, data breach, regulatory violation
  - **High:** Significant functionality impairment, partial data exposure
  - **Medium:** Limited functionality impact, minor data exposure
  - **Low:** Minimal impact, easily mitigated

- **Likelihood Levels:**
  - **High:** Well-known attack vectors, common vulnerabilities
  - **Medium:** Possible but requires specific conditions
  - **Low:** Requires advanced knowledge or specific circumstances

- **Risk Level Calculation:**
  - **Critical:** High impact + High/Medium likelihood
  - **High:** High impact + Low likelihood OR Medium impact + High likelihood
  - **Medium:** Medium impact + Medium likelihood OR other combinations
  - **Low:** Low impact regardless of likelihood

### Overall Assessment
- **Total Threats Identified:** [Count]
- **Critical Threats:** [Count]
- **High Threats:** [Count]
- **Medium Threats:** [Count]
- **Low Threats:** [Count]
- **Overall Risk Level:** [Critical/High/Medium/Low]

## 8. Mitigation Strategy

### Implementation Priorities

#### Priority 1 (Critical) - Implement Immediately
1. [Critical mitigation 1]
   - **Rationale:** [Why this is critical]
   - **Implementation:** [How to implement]
   - **Timeline:** [When to complete]
   - **Owner:** [Responsible person/team]

2. [Critical mitigation 2]
   - **Rationale:** [Why this is critical]
   - **Implementation:** [How to implement]
   - **Timeline:** [When to complete]
   - **Owner:** [Responsible person/team]

#### Priority 2 (High) - Implement This Sprint/Release
1. [High mitigation 1]
   - **Rationale:** [Why this is high priority]
   - **Implementation:** [How to implement]
   - **Timeline:** [When to complete]
   - **Owner:** [Responsible person/team]

#### Priority 3 (Medium) - Plan for Next Sprint/Release
1. [Medium mitigation 1]
   - **Rationale:** [Why this is medium priority]
   - **Implementation:** [How to implement]
   - **Timeline:** [When to complete]
   - **Owner:** [Responsible person/team]

### Mitigation Categories

#### Preventive Controls
- [List preventive measures]

#### Detective Controls
- [List detection measures]

#### Corrective Controls
- [List correction measures]

#### Deterrent Controls
- [List deterrent measures]

## 9. Recommendations

### Immediate Actions (Next Sprint)
1. [Recommendation 1]
2. [Recommendation 2]

### Short-term Actions (Next Quarter)
1. [Recommendation 1]
2. [Recommendation 2]

### Long-term Actions (Next Year)
1. [Recommendation 1]
2. [Recommendation 2]

### Process Improvements
1. [Process recommendation 1]
2. [Process recommendation 2]

## 10. Next Steps

### Implementation Plan
1. **Week 1:** [Activities]
2. **Week 2:** [Activities]
3. **Week 3:** [Activities]
4. **Week 4:** [Activities]

### Monitoring and Validation
- [How to validate mitigations]
- [Monitoring approach]
- [Success metrics]

### Review Schedule
- **Monthly Reviews:** [What to review]
- **Quarterly Assessments:** [What to assess]
- **Annual Updates:** [When to update the model]

## 11. Review and Approval

### Review Checklist
- [ ] All system components identified
- [ ] Data flows documented
- [ ] Trust boundaries defined
- [ ] STRIDE categories applied to all components
- [ ] Risk levels assigned appropriately
- [ ] Mitigations identified for critical/high risks
- [ ] Implementation plan defined
- [ ] Stakeholders consulted

### Approval Signatures
- **Model Created By:** ____________________ Date: ________
- **Technical Review By:** ____________________ Date: ________
- **Security Review By:** ____________________ Date: ________
- **Business Approval By:** ____________________ Date: ________

### Document Control
- **Version:** 1.0
- **Next Review Date:** [Date - typically 6-12 months]
- **Document Owner:** [Name/Team]
- **Distribution:** [Who should receive this document]
```

---

## Template Usage Guide

### Getting Started
1. **Copy the template** to a new file
2. **Fill in system information** in Section 1
3. **Document your system** in Sections 2-5
4. **Apply STRIDE analysis** in Section 6
5. **Complete risk assessment** in Section 7
6. **Develop mitigation strategy** in Section 8
7. **Get approvals** in Section 11

### Best Practices
- **Be Specific:** Use concrete examples, not generic descriptions
- **Include Evidence:** Reference diagrams, code, or documentation
- **Quantify Risks:** Use specific metrics for impact and likelihood
- **Prioritize Realistically:** Focus on threats that matter to your business
- **Keep it Current:** Update the model as the system evolves

### Common Pitfalls
- **Too Generic:** "SQL injection" vs "SQL injection in user login form"
- **Missing Context:** Include business impact and technical details
- **Over-Mitigating:** Don't implement controls for low-risk threats
- **Static Model:** Threat models should evolve with the system

---

## Navigation

| Previous | Current | Next |
|----------|---------|------|
| [[../index|STRIDE Overview]] | STRIDE Template | [[./examples|Case Studies]] |

## See Also

### Related Templates
- [[../../pasta/template|PASTA Template]] - Business risk-focused template
- [[../../octave/template|OCTAVE Template]] - Organizational risk template
- [[../../trike/template|Trike Template]] - Requirements-driven template

### Implementation Resources
- [[./implementation|Implementation Guide]] - Code examples and automation
- [[../../../workshops/beginner|Beginner Workshop]] - Hands-on template usage
- [[../../../resources/tools|Threat Modeling Tools]] - Template-compatible tools

---

**Tags:** #stride-template #threat-modeling-template #security-assessment #risk-analysis

**Last Updated:** October 2025
**Version:** 1.0
**Reading Time:** 25 minutes
**Difficulty:** Intermediate