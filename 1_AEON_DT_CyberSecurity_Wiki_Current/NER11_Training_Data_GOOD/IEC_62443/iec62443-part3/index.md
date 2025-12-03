# IEC 62443-3-3: System Security Requirements and Security Levels

## Overview

IEC 62443-3-3 defines the security requirements for industrial automation and control systems (IACS) based on seven foundational requirements (FR) and seven security levels (SL). This standard provides detailed technical specifications for implementing security controls in industrial environments.

**Version:** IEC 62443-3-3:2021
**Focus:** System security requirements and security levels
**Scope:** Technical security controls for IACS components

---

## Breadcrumb Navigation
[Home](../../../../index.md) > [Cybersecurity](../../../index.md) > [IEC 62443](../../index.md) > Part 3-3

---

## Table of Contents

### Foundational Requirements (FR)
- [[./fr1-identification-authentication|FR 1: Identification and Authentication Control (IAC)]] - User and device authentication
- [[./fr2-use-control|FR 2: Use Control (UC)]] - Access control and authorization
- [[./fr3-system-integrity|FR 3: System Integrity (SI)]] - Protection against unauthorized changes
- [[./fr4-data-confidentiality|FR 4: Data Confidentiality (DC)]] - Protection of sensitive information
- [[./fr5-restricted-data-flow|FR 5: Restricted Data Flow (RDF)]] - Control of data movement
- [[./fr6-timely-response|FR 6: Timely Response to Events (TRE)]] - Event detection and response
- [[./fr7-resource-availability|FR 7: Resource Availability (RA)]] - System availability protection

### Security Level Requirements
- [[./security-levels|Security Level Requirements (SL 2-4)]] - Advanced security capabilities

### Implementation Support
- [[./implementation-checklists|Implementation Checklists]] - SL-specific checklists
- [[./audit-procedures|Audit Procedures]] - Assessment methodologies
- [[./case-studies|Case Studies]] - Real-world implementations

---

## 🎯 Standard Overview

IEC 62443-3-3 establishes the technical security requirements that industrial automation and control systems must meet. It defines seven foundational requirements that address all aspects of system security, from basic access control to advanced threat detection.

### Key Objectives
- **Comprehensive Security:** Address all aspects of system security through foundational requirements
- **Scalable Protection:** Provide security levels that scale with risk and consequences
- **Technical Implementation:** Specify concrete security controls and mechanisms
- **Industrial Focus:** Address unique requirements of industrial control systems

### Foundational Requirements Framework

The seven foundational requirements provide a comprehensive security framework:

1. **Identification and Authentication Control (IAC)** - Ensures only authorized entities access systems
2. **Use Control (UC)** - Manages access rights and permissions
3. **System Integrity (SI)** - Protects against unauthorized system changes
4. **Data Confidentiality (DC)** - Protects sensitive information from disclosure
5. **Restricted Data Flow (RDF)** - Controls how data moves within and between systems
6. **Timely Response to Events (TRE)** - Ensures security events are detected and addressed
7. **Resource Availability (RA)** - Protects system availability and performance

### Security Level Structure

The standard defines four security levels that build upon each other:

- **SL 1:** Prevention of unauthorized access (basic protection)
- **SL 2:** Use of security features (standard protection)
- **SL 3:** Systematic security management (high protection)
- **SL 4:** Adaptation and learning (extreme protection)

---

## Security Level Comparison

| Security Level | Protection Focus | Technical Controls | Management Requirements |
|----------------|------------------|-------------------|------------------------|
| **SL 1** | Basic Access Control | Passwords, basic ACLs | Minimal documentation |
| **SL 2** | Security Features | MFA, RBAC, malware protection | Basic policies and procedures |
| **SL 3** | Systematic Management | Certificate auth, IDS, monitoring | Comprehensive security program |
| **SL 4** | Advanced Threats | HSM, biometric auth, automated response | Continuous adaptation and learning |

---

## Integration with Other Standards

### IEC 62443 Family
- **Part 1-1:** Security foundations and terminology
- **Part 2-4:** Security program requirements for service providers
- **Part 3-2:** Security risk assessment for system design
- **Part 3-3:** System security requirements (this document)
- **Part 4-1:** Secure development lifecycle requirements
- **Part 4-2:** Technical security requirements for components

### Related Standards
- **NIST SP 800-53:** Security and privacy controls for federal systems
- **ISO 27001:** Information security management systems
- **NERC CIP:** Critical infrastructure protection standards

---

## Implementation Benefits

### Security Benefits
- **Structured Approach:** Seven FRs provide comprehensive security coverage
- **Risk-Based Levels:** Four SLs allow appropriate security for different risk levels
- **Industrial Focus:** Addresses ICS-specific security challenges
- **Certification Path:** Clear path to IEC 62443 certification

### Business Benefits
- **Compliance:** Meet regulatory and industry security requirements
- **Risk Reduction:** Systematic approach to security implementation
- **Cost Optimization:** Appropriate security levels based on risk assessment
- **Market Access:** Required for many industrial markets and contracts

---

## Getting Started

### Assessment Phase
1. **Risk Assessment:** Evaluate system risks and required security level
2. **Current State:** Assess existing security controls and gaps
3. **Gap Analysis:** Identify gaps against required security level
4. **Roadmap Development:** Create implementation roadmap

### Implementation Phase
1. **FR Prioritization:** Address most critical foundational requirements first
2. **SL Achievement:** Implement controls to achieve target security level
3. **Integration:** Ensure security controls work together effectively
4. **Testing:** Validate security control effectiveness

### Validation Phase
1. **Control Testing:** Test individual security controls
2. **Integration Testing:** Test security control interactions
3. **Assessment:** Conduct formal security assessment
4. **Certification:** Pursue IEC 62443 certification if required

---

## Navigation

| Previous | Current | Next |
|----------|---------|------|
| [[../iec62443-part2|IEC 62443 Part 2]] | IEC 62443 Part 3-3 | [[../iec62443-part4|IEC 62443 Part 4]] |

## See Also

### Related Standards
- [[../iec62443-part1|IEC 62443 Part 1]] - Security foundations
- [[../iec62443-part2|IEC 62443 Part 2]] - Security program requirements
- [[../iec62443-part4|IEC 62443 Part 4]] - Secure development lifecycle
- [[../iec62443-part3-2|IEC 62443 Part 3-2]] - Security risk assessment

### Implementation Resources
- [[../../network-design|Network Design]] - Network segmentation requirements
- [[../../identity-management|Identity Management]] - Authentication frameworks
- [[../../device-management|Device Management]] - Industrial device security
- [[../../endpoint-protection|Endpoint Protection]] - Host-based security

---

**Tags:** #iec62443 #industrial-security #ics-security #system-security #security-levels #foundational-requirements

**Last Updated:** October 2025
**Version:** 1.0
**Reading Time:** 6 minutes
**Difficulty:** Intermediate