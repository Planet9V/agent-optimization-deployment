# VAST Methodology Phases
## Four-Phase Agile Threat Modeling Process

**Version:** 1.0 - October 2025
**Focus:** Iterative threat identification and mitigation in agile environments
**Duration:** 1-2 hours per sprint

---

## Breadcrumb Navigation
[Home](../../../../index.md) > [Threat Modeling](../../../index.md) > [Methodologies](../../index.md) > [VAST](../index.md) > Phases

---

## Table of Contents

### Phase Details
- [[#phase-1-asset-identification|Phase 1: Asset Identification]] - Identify critical assets in scope
- [[#phase-2-threat-identification|Phase 2: Threat Identification]] - Rapid threat identification
- [[#phase-3-mitigation-planning|Phase 3: Mitigation Planning]] - Develop practical mitigation strategies
- [[#phase-4-validation|Phase 4: Validation]] - Quick validation and iteration planning

### Supporting Elements
- [[#phase-timing|Phase Timing]] - Time allocation per phase
- [[#phase-artifacts|Phase Artifacts]] - Deliverables and outputs
- [[#phase-participants|Phase Participants]] - Who should be involved

---

## 🎯 VAST Phase Overview

VAST follows a streamlined four-phase process designed specifically for agile development cycles. Each phase builds on the previous one, with an emphasis on speed, practicality, and actionable results.

### Phase Flow
```
Asset Identification → Threat Identification → Mitigation Planning → Validation
        ↓                     ↓                     ↓                     ↓
   20 minutes           25 minutes           30 minutes           15 minutes
```

---

## Phase 1: Asset Identification
**Duration:** 20 minutes
**Goal:** Quickly identify critical assets in the current sprint scope

### Activities

#### 1. Sprint Backlog Review
**Focus on user stories and features in current sprint**
- Review sprint backlog items
- Identify user stories with security implications
- Note data flows and external dependencies
- Document acceptance criteria with security requirements

#### 2. Asset Categorization
**Classify assets by type and criticality**

##### Functional Assets
- **Features and capabilities** being developed
- **User interactions** and workflows
- **Business processes** supported by the system
- **Integration points** with other systems

##### Data Assets
- **User data** processed or stored
- **Configuration data** affecting system behavior
- **Audit logs** and security events
- **Backup and recovery data**

##### Technical Assets
- **Application components** (APIs, services, databases)
- **Infrastructure elements** (servers, networks, containers)
- **Third-party services** and dependencies
- **Development and deployment tools**

#### 3. Criticality Assessment
**Determine business impact and security requirements**
- **High:** Payment processing, user authentication, sensitive data handling
- **Medium:** User profile management, content display, basic CRUD operations
- **Low:** Static content, help systems, administrative utilities

### Deliverables
- **Asset Inventory:** List of functional, data, and technical assets
- **Criticality Ratings:** High/Medium/Low classification for each asset
- **Initial Scope:** Clear boundaries for threat modeling exercise

---

## Phase 2: Threat Identification
**Duration:** 25 minutes
**Goal:** Rapid identification of most important threats using visual techniques

### Activities

#### 1. Threat Category Application
**Apply simplified threat categories to identified assets**

##### Core Threat Categories
- **Spoofing:** Impersonation and identity theft
- **Tampering:** Unauthorized data modification
- **Repudiation:** Action denial and non-repudiation failures
- **Information Disclosure:** Unwanted data exposure
- **Denial of Service:** Availability disruption
- **Elevation of Privilege:** Unauthorized access escalation

#### 2. Asset-Based Threat Analysis
**Identify threats for each asset type**

##### Functional Asset Threats
- Unauthorized feature access
- Business logic manipulation
- Workflow disruption
- Feature abuse for malicious purposes

##### Data Asset Threats
- Data interception during transmission
- Unauthorized data access or modification
- Data integrity violations
- Privacy breaches and compliance violations

##### Technical Asset Threats
- Component compromise through vulnerabilities
- Service disruption and availability attacks
- Configuration manipulation
- Supply chain and dependency attacks

#### 3. Sprint Context Integration
**Consider current development context**
- New features being added
- Existing functionality being modified
- Third-party integrations being implemented
- Infrastructure changes in progress

### Deliverables
- **Threat List:** Identified threats for each asset
- **Threat Scenarios:** High-level attack narratives
- **Visual Threat Map:** Simple diagram showing threats against assets

---

## Phase 3: Mitigation Planning
**Duration:** 30 minutes
**Goal:** Develop practical mitigation strategies with implementation priorities

### Activities

#### 1. Existing Controls Assessment
**Identify security controls already in place**
- Authentication and authorization mechanisms
- Encryption and data protection
- Input validation and sanitization
- Monitoring and logging capabilities
- Network security controls

#### 2. Mitigation Strategy Development
**Design practical, implementable security measures**

##### Mitigation Categories
- **Preventive Controls:** Stop threats before they occur
- **Detective Controls:** Identify threats when they happen
- **Corrective Controls:** Respond to and recover from incidents
- **Deterrent Controls:** Discourage threat actors

#### 3. Effort vs. Risk Analysis
**Balance implementation cost with security benefit**

##### Risk-Based Prioritization
- **Critical:** Must-fix before sprint completion
- **High:** Address within current sprint
- **Medium:** Plan for next sprint
- **Low:** Monitor and address as capacity allows

##### Effort Estimation
- **Story Points:** 1-2 (quick fixes), 3-5 (moderate changes), 8-13 (significant work)
- **Implementation Time:** Hours to days for completion
- **Testing Requirements:** Unit tests, integration tests, security tests

### Deliverables
- **Mitigation Plans:** Specific security controls for each threat
- **Implementation Backlog:** User stories and tasks for development team
- **Acceptance Criteria:** Testable security requirements

---

## Phase 4: Validation
**Duration:** 15 minutes
**Goal:** Quick validation and planning for next iteration

### Activities

#### 1. Completeness Check
**Validate threat model against sprint goals**
- All critical assets identified and analyzed
- Major threats addressed with mitigation plans
- Security requirements documented and testable
- No obvious gaps in coverage

#### 2. Gap Analysis
**Identify areas needing more analysis**
- High-risk assets without adequate protection
- New threat vectors not considered
- Integration points requiring additional scrutiny
- Compliance requirements not addressed

#### 3. Next Iteration Planning
**Plan security activities for upcoming sprints**
- Follow-up threat modeling sessions
- Security testing and validation activities
- Compliance and audit preparation
- Continuous improvement opportunities

### Deliverables
- **Validation Report:** Completeness assessment and gap analysis
- **Action Items:** Follow-up activities for next sprint
- **Lessons Learned:** Process improvements for future sessions

---

## Phase Timing Guidelines

### Total Session Time: 90 minutes
- **Phase 1:** 20 minutes (22% of time)
- **Phase 2:** 25 minutes (28% of time)
- **Phase 3:** 30 minutes (33% of time)
- **Phase 4:** 15 minutes (17% of time)

### Time Management Tips
- **Keep moving:** Use time-boxing to maintain momentum
- **Defer details:** Focus on high-level analysis, not deep dives
- **Parallel work:** Have team members work on different assets simultaneously
- **Quick decisions:** Make security decisions quickly, revisit if needed

---

## Phase Artifacts

### Required Deliverables
- **Asset Inventory Spreadsheet/List**
- **Threat Identification Matrix**
- **Mitigation Action Items**
- **Security User Stories**

### Optional Supporting Materials
- **Visual Diagrams:** Simple asset/threat/mitigation maps
- **Risk Assessment Matrix:** Likelihood vs. impact ratings
- **Security Test Cases:** Acceptance criteria for validation

---

## Phase Participants

### Core Team (Required)
- **Product Owner:** Business context and priorities
- **Development Lead:** Technical feasibility and implementation
- **Security Representative:** Threat expertise and best practices

### Extended Team (Recommended)
- **QA/Test Engineer:** Testing implications and validation
- **DevOps Engineer:** Infrastructure and deployment security
- **Business Analyst:** Requirements and user story context

### Facilitator Role
- **Scrum Master** or **Agile Coach:** Process facilitation and time management
- **Security Champion:** Team member trained in basic threat modeling

---

## Navigation

| Previous | Current | Next |
|----------|---------|------|
| [[../index|VAST Overview]] | VAST Phases | [[./implementation|VAST Implementation]] |

## See Also

### Related Topics
- [[../stride/phases|STRIDE Phases]] - Technical threat identification
- [[../pasta/phases|PASTA Phases]] - Risk-centric analysis
- [[../../../agile-security|Agile Security Practices]] - Security in agile

### Implementation Resources
- [[./implementation|VAST Implementation]] - Code examples and automation
- [[./template|VAST Template]] - Ready-to-use agile template
- [[../../../workflows/examples/devsecops|DevSecOps Workflows]] - Automation examples

---

**Tags:** #vast-phases #agile-threat-modeling #sprint-security #threat-identification #mitigation-planning

**Last Updated:** October 2025
**Version:** 1.0
**Reading Time:** 12 minutes
**Difficulty:** Intermediate