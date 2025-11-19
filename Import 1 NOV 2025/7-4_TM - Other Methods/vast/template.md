# VAST Threat Modeling Template
## Agile Threat Modeling for Sprint Planning

**Version:** 1.0 - October 2025
**Duration:** 90 minutes
**Participants:** Development Team + Product Owner + Security Rep

---

## Breadcrumb Navigation
[Home](../../../../index.md) > [Threat Modeling](../../../index.md) > [Methodologies](../../index.md) > [VAST](../index.md) > Template

---

## Table of Contents

### Template Sections
- [[#session-header|Session Header]] - Basic session information
- [[#phase-1-assets|Phase 1: Asset Identification]] - Asset inventory template
- [[#phase-2-threats|Phase 2: Threat Identification]] - Threat analysis template
- [[#phase-3-mitigations|Phase 3: Mitigation Planning]] - Mitigation planning template
- [[#phase-4-validation|Phase 4: Validation]] - Validation checklist

### Supporting Materials
- [[#visual-diagrams|Visual Diagrams]] - Diagram templates
- [[#user-stories|Security User Stories]] - Story templates
- [[#checklist|Session Checklist]] - Preparation and execution guide

---

## 🎯 Template Overview

This template guides teams through a complete VAST threat modeling session. Fill out each section during the corresponding phase, then use the results to create actionable backlog items.

### Session Preparation
- **Duration:** 90 minutes (4 phases × 15-30 minutes each)
- **Participants:** 3-7 people (developers, product owner, security)
- **Materials:** Whiteboard, sticky notes, or digital collaboration tool
- **Prerequisites:** Sprint backlog review, system architecture diagram

---

## Session Header

| Field | Value |
|-------|--------|
| **System Name** | |
| **Sprint** | Sprint # |
| **Date** | YYYY-MM-DD |
| **Facilitator** | |
| **Participants** | 1.<br>2.<br>3.<br>4.<br>5. |
| **Sprint Focus** | |
| **Key Deliverables** | |

**Session Goal:** [Brief description of what this threat modeling session aims to achieve]

---

## Phase 1: Asset Identification
**Duration:** 20 minutes
**Goal:** Identify critical assets in current sprint scope

### Functional Assets (Features & Capabilities)

| Asset Name | Description | Criticality | Users | Dependencies |
|------------|-------------|-------------|-------|--------------|
| | | ☐ High ☐ Medium ☐ Low | | |
| | | ☐ High ☐ Medium ☐ Low | | |
| | | ☐ High ☐ Medium ☐ Low | | |
| | | ☐ High ☐ Medium ☐ Low | | |
| | | ☐ High ☐ Medium ☐ Low | | |

### Data Assets (Information & Storage)

| Data Type | Description | Sensitivity | Volume | Access Level | Regulations |
|-----------|-------------|-------------|--------|--------------|-------------|
| | | ☐ Critical ☐ High ☐ Medium ☐ Low | ☐ High ☐ Medium ☐ Low | | |
| | | ☐ Critical ☐ High ☐ Medium ☐ Low | ☐ High ☐ Medium ☐ Low | | |
| | | ☐ Critical ☐ High ☐ Medium ☐ Low | ☐ High ☐ Medium ☐ Low | | |
| | | ☐ Critical ☐ High ☐ Medium ☐ Low | ☐ High ☐ Medium ☐ Low | | |

### Technical Assets (Components & Infrastructure)

| Component | Category | Technology | Exposure | Interfaces |
|-----------|----------|------------|----------|------------|
| | ☐ Web App ☐ API ☐ Database ☐ Service ☐ Other | | ☐ External ☐ Internal ☐ Public | |
| | ☐ Web App ☐ API ☐ Database ☐ Service ☐ Other | | ☐ External ☐ Internal ☐ Public | |
| | ☐ Web App ☐ API ☐ Database ☐ Service ☐ Other | | ☐ External ☐ Internal ☐ Public | |
| | ☐ Web App ☐ API ☐ Database ☐ Service ☐ Other | | ☐ External ☐ Internal ☐ Public | |
| | ☐ Web App ☐ API ☐ Database ☐ Service ☐ Other | | ☐ External ☐ Internal ☐ Public | |

### Phase 1 Notes
**Key Findings:**
- [List any important observations about assets]

**Questions for Clarification:**
- [Note any uncertainties that need product owner input]

---

## Phase 2: Threat Identification
**Duration:** 25 minutes
**Goal:** Identify most important threats using visual techniques

### Threat Categories Reference
- **Spoofing:** Identity impersonation and forgery
- **Tampering:** Unauthorized data modification
- **Repudiation:** Action denial and non-repudiation failures
- **Information Disclosure:** Unwanted data exposure
- **Denial of Service:** Availability disruption
- **Elevation of Privilege:** Unauthorized access escalation

### Identified Threats

| Asset Name | Threat Category | Description | Likelihood | Impact | Sprint Context |
|------------|----------------|-------------|------------|--------|----------------|
| | ☐ Spoofing ☐ Tampering ☐ Repudiation ☐ Info Disclosure ☐ DoS ☐ Elevation | | ☐ High ☐ Medium ☐ Low | ☐ High ☐ Medium ☐ Low | |
| | ☐ Spoofing ☐ Tampering ☐ Repudiation ☐ Info Disclosure ☐ DoS ☐ Elevation | | ☐ High ☐ Medium ☐ Low | ☐ High ☐ Medium ☐ Low | |
| | ☐ Spoofing ☐ Tampering ☐ Repudiation ☐ Info Disclosure ☐ DoS ☐ Elevation | | ☐ High ☐ Medium ☐ Low | ☐ High ☐ Medium ☐ Low | |
| | ☐ Spoofing ☐ Tampering ☐ Repudiation ☐ Info Disclosure ☐ DoS ☐ Elevation | | ☐ High ☐ Medium ☐ Low | ☐ High ☐ Medium ☐ Low | |
| | ☐ Spoofing ☐ Tampering ☐ Repudiation ☐ Info Disclosure ☐ DoS ☐ Elevation | | ☐ High ☐ Medium ☐ Low | ☐ High ☐ Medium ☐ Low | |
| | ☐ Spoofing ☐ Tampering ☐ Repudiation ☐ Info Disclosure ☐ DoS ☐ Elevation | | ☐ High ☐ Medium ☐ Low | ☐ High ☐ Medium ☐ Low | |
| | ☐ Spoofing ☐ Tampering ☐ Repudiation ☐ Info Disclosure ☐ DoS ☐ Elevation | | ☐ High ☐ Medium ☐ Low | ☐ High ☐ Medium ☐ Low | |
| | ☐ Spoofing ☐ Tampering ☐ Repudiation ☐ Info Disclosure ☐ DoS ☐ Elevation | | ☐ High ☐ Medium ☐ Low | ☐ High ☐ Medium ☐ Low | |

### Threat Scenarios (High-Level Attack Narratives)

| Scenario ID | Threat Title | Preconditions | Attack Steps | Detection Methods |
|-------------|--------------|---------------|--------------|-------------------|
| TS-001 | | | | |
| TS-002 | | | | |
| TS-003 | | | | |

### Phase 2 Notes
**Most Critical Threats:**
- [List top 3 threats by risk level]

**New Threats Identified:**
- [Any threats specific to this sprint's changes]

**Assumptions Made:**
- [Note any assumptions that should be validated]

---

## Phase 3: Mitigation Planning
**Duration:** 30 minutes
**Goal:** Develop practical mitigation strategies with implementation priorities

### Existing Security Controls
**Check all that apply:**
- ☐ Authentication (username/password, MFA, etc.)
- ☐ Authorization (RBAC, ABAC, etc.)
- ☐ Encryption (at rest, in transit)
- ☐ Input validation and sanitization
- ☐ Logging and monitoring
- ☐ Network security (firewalls, WAF, etc.)
- ☐ Rate limiting and DoS protection
- ☐ Backup and recovery
- ☐ Security testing (SAST, DAST, etc.)

**Other existing controls:**
- [List any additional security measures]

### Mitigation Plans

| Threat | Mitigations | Priority | Effort Estimate | Owner | Sprint |
|--------|-------------|----------|-----------------|-------|--------|
| | | ☐ Critical ☐ High ☐ Medium ☐ Low | [Story Points] | | Current |
| | | ☐ Critical ☐ High ☐ Medium ☐ Low | [Story Points] | | Current |
| | | ☐ Critical ☐ High ☐ Medium ☐ Low | [Story Points] | | Current |
| | | ☐ Critical ☐ High ☐ Medium ☐ Low | [Story Points] | | Current |
| | | ☐ Critical ☐ High ☐ Medium ☐ Low | [Story Points] | | Current |
| | | ☐ Critical ☐ High ☐ Medium ☐ Low | [Story Points] | | Current |
| | | ☐ Critical ☐ High ☐ Medium ☐ Low | [Story Points] | | Current |
| | | ☐ Critical ☐ High ☐ Medium ☐ Low | [Story Points] | | Current |

### Acceptance Criteria
**Security requirements that must be met:**

| Criteria | Testable? | Owner | Status |
|----------|-----------|-------|--------|
| All critical/high priority threats have mitigation plans | ☐ Yes ☐ No | | ☐ Complete ☐ Pending |
| Mitigation plans are feasible within current sprint | ☐ Yes ☐ No | | ☐ Complete ☐ Pending |
| Security requirements are documented and testable | ☐ Yes ☐ No | | ☐ Complete ☐ Pending |
| Threat model is reviewed by security team | ☐ Yes ☐ No | | ☐ Complete ☐ Pending |

### Phase 3 Notes
**Implementation Challenges:**
- [Note any technical challenges or dependencies]

**Additional Resources Needed:**
- [Security tools, training, or external expertise required]

**Follow-up Actions:**
- [Actions needed after this session]

---

## Phase 4: Validation
**Duration:** 15 minutes
**Goal:** Quick validation and planning for next iteration

### Validation Checklist

| Validation Item | Status | Notes |
|----------------|--------|-------|
| All critical assets identified | ☐ Complete ☐ Partial ☐ Missing | |
| Major threats addressed with mitigations | ☐ Complete ☐ Partial ☐ Missing | |
| Security requirements documented | ☐ Complete ☐ Partial ☐ Missing | |
| No obvious gaps in coverage | ☐ Complete ☐ Partial ☐ Missing | |
| Mitigation plans are actionable | ☐ Complete ☐ Partial ☐ Missing | |
| Owners assigned to all high-priority items | ☐ Complete ☐ Partial ☐ Missing | |

### Identified Gaps

| Gap Description | Impact | Action Required | Timeline |
|----------------|--------|----------------|----------|
| | ☐ High ☐ Medium ☐ Low | | |
| | ☐ High ☐ Medium ☐ Low | | |
| | ☐ High ☐ Medium ☐ Low | | |

### Next Sprint Planning

| Activity | Sprint | Owner | Status |
|----------|--------|-------|--------|
| Review threat model in sprint planning | Next | Scrum Master | ☐ Planned |
| Include security stories in backlog | Next | Product Owner | ☐ Planned |
| Conduct security testing | Next | QA Team | ☐ Planned |
| Security retrospective | Next+1 | Team | ☐ Planned |
| Update threat model | Next+1 | Security Champion | ☐ Planned |

### Recommendations

| Recommendation | Priority | Rationale |
|----------------|----------|-----------|
| | ☐ High ☐ Medium ☐ Low | |
| | ☐ High ☐ Medium ☐ Low | |
| | ☐ High ☐ Medium ☐ Low | |
| | ☐ High ☐ Medium ☐ Low | |

### Phase 4 Notes
**Overall Assessment:**
- ☐ Threat model is complete and actionable
- ☐ Some gaps identified but acceptable for this sprint
- ☐ Major gaps require immediate attention
- ☐ Threat model needs significant rework

**Confidence Level:** ☐ High ☐ Medium ☐ Low

**Key Success Factors:**
- [What went well in this session]
- [What could be improved next time]

---

## Visual Diagrams

### Asset Map Template
```
[External Users] → [Web Application] → [API Gateway] → [Database]
                        ↓
                 [Authentication Service]
```

### Threat Overlay Template
```
[External Users] → [Web Application] → [API Gateway] → [Database]
      ⚠️ Spoofing     🔓 Injection      🚫 Auth Bypass   💀 Data Breach
                        ↓
                 [Authentication Service]
                      🔑 Weak Auth
```

### Mitigation Map Template
```
[External Users] → [WAF] → [Web Application] → [API Gateway] → [Database]
                        ↓                      ↓
                 [MFA Service]          [Rate Limiting]
```

---

## Security User Stories

### Template Format
```
As a [user type],
I want [security control]
So that [threat is mitigated]

Acceptance Criteria:
- [Testable security requirement]
- [Implementation verification]
- [Testing approach]
```

### Example User Stories

**Authentication Story:**
```
As a system administrator,
I want multi-factor authentication for admin access
So that unauthorized users cannot impersonate administrators

Acceptance Criteria:
- MFA is required for all admin login attempts
- Failed MFA attempts are logged and monitored
- Users can enroll multiple MFA devices
- MFA can be disabled only by another admin
```

**Data Protection Story:**
```
As a customer,
I want my payment information encrypted
So that my financial data cannot be stolen if the database is compromised

Acceptance Criteria:
- Payment data is encrypted at rest using AES-256
- Encryption keys are rotated annually
- Encryption does not impact payment processing performance
- Decryption is only possible with proper authorization
```

---

## Session Checklist

### Pre-Session Preparation
- ☐ Sprint backlog reviewed
- ☐ System architecture diagram available
- ☐ Key stakeholders identified and invited
- ☐ Meeting room/whiteboard reserved
- ☐ Template printed or digital access ready
- ☐ Time-boxing timer prepared

### During Session
- ☐ Session goal clearly stated
- ☐ All participants introduced
- ☐ Time boxes enforced for each phase
- ☐ Note taker assigned
- ☐ Parking lot for off-topic items
- ☐ Regular check-ins for understanding

### Post-Session
- ☐ Template completed and saved
- ☐ Action items assigned with owners
- ☐ Security stories added to backlog
- ☐ Follow-up meeting scheduled if needed
- ☐ Session retrospective conducted
- ☐ Documentation shared with team

### Success Metrics
- ☐ All phases completed within time boxes
- ☐ Actionable security requirements identified
- ☐ Team alignment on security priorities
- ☐ No critical gaps left unaddressed
- ☐ Security stories properly sized and prioritized

---

## Navigation

| Previous | Current | Next |
|----------|---------|------|
| [[./implementation|VAST Implementation]] | VAST Template | [[../octave/index|OCTAVE Methodology]] |

## See Also

### Related Templates
- [[../stride/template|STRIDE Template]] - Technical threat modeling
- [[../pasta/template|PASTA Template]] - Risk-focused analysis
- [[../../../workflows/templates|Workflow Templates]] - Process automation

### Implementation Guides
- [[./implementation|VAST Implementation]] - Code automation
- [[../../../agile-security|Agile Security Practices]] - Sprint integration
- [[../../../workflows/examples/devsecops|DevSecOps Examples]] - CI/CD security

---

**Tags:** #vast-template #agile-threat-modeling #sprint-planning #security-stories #threat-modeling-template

**Last Updated:** October 2025
**Version:** 1.0
**Reading Time:** 25 minutes
**Difficulty:** Intermediate