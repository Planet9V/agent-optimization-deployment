# IEC 62443 Complete Technical Specifications Reference

## Comprehensive Security Requirements, Levels, and Implementation Framework

**Version 2.0 - Extended Technical Edition**
**Document Date: October 2025**

---

## Executive Summary

This document provides exhaustive technical specifications for implementing IEC/ISA 62443 cybersecurity standards in Industrial Automation and Control Systems (IACS). It includes complete mappings of all Security Requirements (SRs) and Requirement Enhancements (REs) across all seven Foundational Requirements (FRs), detailed security level specifications, criticality assessment methodologies, and zone/asset classification frameworks.

**Key Statistics:**

- **82 Total Security Requirements** (51 Base Requirements + 31 Requirement Enhancements)
- **4 Security Levels** (SL 1-4) with escalating protection capabilities
- **7 Foundational Requirements** covering all aspects of IACS security
- **3 Security Level Types** (Capability, Target, Achieved) for comprehensive assessment

This technical reference provides the foundation for implementing IEC 62443 cybersecurity standards in industrial environments. Key takeaways:

1. **82 Security Requirements** across 7 Foundational Requirements provide comprehensive coverage of IACS security
2. **Four Security Levels** (SL 1-4) enable risk-based protection tailored to threat environment and asset criticality
3. **7 Foundational Requirements** covering all aspects of IACS security
4. **3 Security Level Types** (Capability, Target, Achieved) for comprehensive assessment
5. **Risk-Based Approach** through consequence assessment, threat analysis, and SL-T determination ensures security investments align with business risks
6. **Zone and Conduit Architecture** provides structured approach to network segmentation and boundary protection
7. **Phased Implementation** enables pragmatic, achievable progress toward mature security posture
8. **Asset-Specific Guidance** recognizes that different device types require different approaches and compensating controls

Organizations should use this reference in conjunction with the complete IEC 62443 standard series and engage qualified professionals for risk assessment, design, and implementation support.

## Table of Contents

1. [Security Level Framework](#security-level-framework)
2. [Complete Security Requirements by Foundational Requirement](#complete-security-requirements-by-foundational-requirement)
3. [Security Requirements Mapping Tables](#security-requirements-mapping-tables)
4. [Criticality Assessment and SL-T Determination](#criticality-assessment-and-sl-t-determination)
5. [Zone Classification Framework](#zone-classification-framework)
6. [Implementation Methodology](#implementation-methodology)
7. [Asset-Specific Security Level Guidance](#asset-specific-security-level-guidance)
8. [Appendices](#appendices)

---

## 1. Security Level Framework

### 1.1 Security Level Definitions

IEC 62443-3-3 defines four Security Levels based on the sophistication of threat actors and their capabilities.

#### Complete Security Level Specifications

| Security Level | Protection Against                                                      | Threat Actor Profile                             | Means                              | Resources                           | Skills                  | Motivation                                 |
| -------------- | ----------------------------------------------------------------------- | ------------------------------------------------ | ---------------------------------- | ----------------------------------- | ----------------------- | ------------------------------------------ |
| **SL 0** | No protection required                                                  | None                                             | No special means                   | No resources                        | No special skills       | None                                       |
| **SL 1** | Casual or coincidental violation                                        | Staff member, accidental misuse                  | Simple/readily available           | Individual/Low                      | No specialized skills   | Low/Accidental                             |
| **SL 2** | Intentional violation using simple means                                | Low-level hacker, Script kiddie, Insider         | Simple attack tools                | Low (individual)                    | Generic IT skills       | Low (curiosity, vandalism)                 |
| **SL 3** | Intentional violation using sophisticated means                         | Skilled hacker, Organized crime, Terrorist group | Sophisticated attack methods       | Moderate (hacker groups)            | IACS-specific knowledge | Moderate (financial gain, ideology)        |
| **SL 4** | Intentional violation using sophisticated means with extended resources | Nation state, APT (Advanced Persistent Threat)   | Sophisticated multi-phase campaign | Extended (multi-disciplinary teams) | IACS-specific expertise | High (strategic objectives, cyber warfare) |

### 1.2 Security Level Types

Understanding the three types of Security Levels is critical for proper implementation:

#### Target Security Level (SL-T)

**Definition**: The desired level of security for a particular zone, conduit, or system based on risk assessment.

**Determined By**:

- Consequence analysis (operational, financial, HSE impacts)
- Threat environment assessment
- Regulatory and compliance requirements
- Organizational risk tolerance

**Purpose**:

- Guides procurement specifications
- Defines security control requirements
- Establishes security design objectives
- Sets testing and validation criteria

**Documentation**: Recorded in the Cybersecurity Requirements Specification (CRS)

#### Capability Security Level (SL-C)

**Definition**: The maximum security level that a system or component can provide when properly configured and deployed.

**Applies To**:

- Control systems (IEC 62443-3-3)
- Components: embedded devices, host devices, network devices, software applications (IEC 62443-4-2)

**Purpose**:

- Product selection criteria
- Identifies inherent security capabilities
- Enables gap analysis (SL-T vs SL-C)
- Supports procurement decisions

**Certification**: Products can be certified to specific SL-C levels through ISASecure or IECEE programs

#### Achieved Security Level (SL-A)

**Definition**: The actual security level achieved by a deployed and operational automation solution.

**Determined By**:

- Assessment of implemented controls
- Configuration validation
- Integration testing results
- Operational verification

**Purpose**:

- Validates implementation effectiveness
- Identifies residual gaps requiring compensating controls
- Supports compliance demonstration
- Enables continuous improvement tracking

**Assessment**: Part of Security Program Rating per IEC 62443-2-2

### 1.3 Security Level Progression

Security Levels are **cumulative** - each higher level includes all requirements from lower levels plus additional requirements and enhancements.

**Progression Structure**:

```
SL 4
├── All SL 3 requirements
├── Additional SL 4 base requirements
└── Additional SL 4 requirement enhancements

SL 3
├── All SL 2 requirements
├── Additional SL 3 base requirements
└── Additional SL 3 requirement enhancements

SL 2
├── All SL 1 requirements
├── Additional SL 2 base requirements
└── Additional SL 2 requirement enhancements

SL 1
└── Baseline requirements
```

**Quantitative Progression**:

- **SL 1**: 32 requirements (39% of total)
- **SL 2**: 64 requirements (78% of total) - doubles SL 1 requirements
- **SL 3**: 77 requirements (94% of total) - comprehensive security
- **SL 4**: 82 requirements (100% of total) - maximum security

---

## 2. Complete Security Requirements by Foundational Requirement

### 2.1 FR 1 - Identification and Authentication Control (IAC)

**Purpose**: Ensure that all users (human, software processes, devices) are properly identified and authenticated before being granted access to the IACS.

**Total Requirements**: 22 (13 Base + 9 Enhancements)

#### Security Requirements Detail

| SR ID             | Requirement Name                                  | Type        | Description                                                                                  | SL1 | SL2 | SL3 | SL4 |
| ----------------- | ------------------------------------------------- | ----------- | -------------------------------------------------------------------------------------------- | --- | --- | --- | --- |
| **SR 1.1**  | Human user identification and authentication      | Base        | The control system shall provide the capability to identify and authenticate all human users | R   | R   | R   | R   |
| SR 1.1 RE(1)      | Unique identification and authentication          | Enhancement | Control system shall uniquely identify and authenticate all human users                      |     | R   | R   | R   |
| SR 1.1 RE(2)      | Multifactor authentication for untrusted networks | Enhancement | Control system shall use multifactor authentication for access via untrusted networks        |     |     |     | R   |
| **SR 1.2**  | Software process and device identification        | Base        | Control system shall identify and authenticate all software processes and devices            | R   | R   | R   | R   |
| SR 1.2 RE(1)      | Unique identification and authentication          | Enhancement | Control system shall uniquely identify and authenticate all software processes and devices   |     | R   | R   | R   |
| **SR 1.3**  | Account management                                | Base        | Control system shall provide the capability to support account management functions          | R   | R   | R   | R   |
| SR 1.3 RE(1)      | Dynamic authorization management                  | Enhancement | Control system shall dynamically manage user authorizations                                  |     | R   | R   | R   |
| SR 1.3 RE(2)      | Password generation and lifetime                  | Enhancement | Control system shall enforce password generation and lifetime restrictions                   |     |     | R   | R   |
| **SR 1.4**  | Identifier management                             | Base        | Control system shall provide the capability to manage identifiers                            | R   | R   | R   | R   |
| **SR 1.5**  | Authenticator management                          | Base        | Control system shall provide the capability to manage authenticators                         | R   | R   | R   | R   |
| SR 1.5 RE(1)      | Authenticator content                             | Enhancement | Control system shall obscure authenticator content during authentication                     |     | R   | R   | R   |
| SR 1.5 RE(2)      | Password change                                   | Enhancement | Control system shall provide mechanisms to change/refresh authenticators                     |     |     | R   | R   |
| **SR 1.6**  | Wireless access management                        | Base        | Control system shall provide the capability to authorize and control wireless access         | R   | R   | R   | R   |
| **SR 1.7**  | Strength of password-based authentication         | Base        | Control system shall enforce minimum password strength requirements                          | R   | R   | R   | R   |
| SR 1.7 RE(1)      | Password generation and lifetime restrictions     | Enhancement | Control system shall enforce password complexity and aging requirements                      |     | R   | R   | R   |
| SR 1.7 RE(2)      | Hardware security for authenticators              | Enhancement | Control system shall use hardware-based authentication mechanisms                            |     |     |     | R   |
| **SR 1.8**  | Public key infrastructure certificates            | Base        | Control system shall support PKI certificates for authentication                             |     |     | R   | R   |
| **SR 1.9**  | Strength of public key authentication             | Base        | Control system shall enforce minimum strength for public key authentication                  |     |     | R   | R   |
| **SR 1.10** | Authenticator feedback                            | Base        | Control system shall obscure feedback of authentication information during login             | R   | R   | R   | R   |
| **SR 1.11** | Unsuccessful login attempts                       | Base        | Control system shall enforce limit of consecutive invalid access attempts                    | R   | R   | R   | R   |
| **SR 1.12** | System use notification                           | Base        | Control system shall display use notification messages before granting access                | R   | R   | R   | R   |
| **SR 1.13** | Access via untrusted networks                     | Base        | Control system shall provide mechanisms for secure access via untrusted networks             |     | R   | R   | R   |

**Key Implementation Notes for FR 1**:

- SL 1 establishes baseline authentication (may use group accounts)
- SL 2 requires individual, unique user identification
- SL 3 introduces PKI and stronger cryptographic authentication
- SL 4 mandates multifactor authentication and hardware security tokens

---

### 2.2 FR 2 - Use Control (UC)

**Purpose**: Ensure that authenticated users have appropriate authorization to perform requested actions and that all activities are auditable.

**Total Requirements**: 19 (12 Base + 7 Enhancements)

#### Security Requirements Detail

| SR ID             | Requirement Name                            | Type        | Description                                                                                                  | SL1 | SL2 | SL3 | SL4 |
| ----------------- | ------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------ | --- | --- | --- | --- |
| **SR 2.1**  | Authorization enforcement                   | Base        | Control system shall enforce approved authorizations for controlling access                                  | R   | R   | R   | R   |
| SR 2.1 RE(1)      | Authorization enforcement for all users     | Enhancement | Control system shall enforce authorization for all users including processes and devices                     |     | R   | R   | R   |
| SR 2.1 RE(2)      | Permission mapping to roles                 | Enhancement | Control system shall provide the capability to assign permissions to roles                                   |     |     | R   | R   |
| **SR 2.2**  | Wireless use control                        | Base        | Control system shall protect wireless access consistent with risk to the control system                      | R   | R   | R   | R   |
| **SR 2.3**  | Use control for portable and mobile devices | Base        | Control system shall restrict use of portable and mobile devices                                             | R   | R   | R   | R   |
| **SR 2.4**  | Mobile code                                 | Base        | Control system shall prevent the execution of unauthorized mobile code                                       |     | R   | R   | R   |
| **SR 2.5**  | Session lock                                | Base        | Control system shall provide the capability to lock an interactive session                                   | R   | R   | R   | R   |
| **SR 2.6**  | Remote session termination                  | Base        | Control system shall provide the capability to manually terminate a user's own remote session                |     | R   | R   | R   |
| **SR 2.7**  | Concurrent session control                  | Base        | Control system shall limit the number of concurrent sessions for each user account                           |     | R   | R   | R   |
| **SR 2.8**  | Auditable events                            | Base        | Control system shall provide the capability to generate audit records                                        | R   | R   | R   | R   |
| SR 2.8 RE(1)      | Audit logging                               | Enhancement | Control system shall log all events defined in the capability requirement                                    |     | R   | R   | R   |
| SR 2.8 RE(2)      | Continuous monitoring                       | Enhancement | Control system shall provide continuous monitoring and alerting of auditable events                          |     |     | R   | R   |
| **SR 2.9**  | Audit storage capacity                      | Base        | Control system shall allocate sufficient audit record storage capacity                                       | R   | R   | R   | R   |
| SR 2.9 RE(1)      | Audit log offload                           | Enhancement | Control system shall offload audit logs to another system in real time                                       |     | R   | R   | R   |
| SR 2.9 RE(2)      | Audit storage capacity warning              | Enhancement | Control system shall provide a warning when allocated audit storage capacity is reached                      |     |     | R   | R   |
| **SR 2.10** | Response to audit processing failures       | Base        | Control system shall alert appropriate roles in the event of audit processing failure                        |     | R   | R   | R   |
| **SR 2.11** | Timestamps                                  | Base        | Control system shall provide timestamps for use in audit record generation                                   | R   | R   | R   | R   |
| SR 2.11 RE(1)     | Timing sources                              | Enhancement | Control system shall use redundant authoritative time sources                                                |     | R   | R   | R   |
| **SR 2.12** | Non-repudiation                             | Base        | Control system shall provide the capability to determine whether a given individual took a particular action |     | R   | R   | R   |

**Key Implementation Notes for FR 2**:

- SL 1 requires basic authorization and audit logging capabilities
- SL 2 mandates detailed authorization enforcement and continuous audit logging
- SL 3 adds role-based access control (RBAC) and real-time monitoring
- SL 4 maintains all SL 3 requirements with enhanced rigor

---

### 2.3 FR 3 - System Integrity (SI)

**Purpose**: Ensure the integrity of the control system to guard against unauthorized modification, maintain security functions, and protect information.

**Total Requirements**: 18 (9 Base + 9 Enhancements)

#### Security Requirements Detail

| SR ID            | Requirement Name                               | Type        | Description                                                                                                                           | SL1 | SL2 | SL3 | SL4 |
| ---------------- | ---------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------- | --- | --- | --- | --- |
| **SR 3.1** | Communication integrity                        | Base        | Control system shall protect the integrity of transmitted information                                                                 | R   | R   | R   | R   |
| SR 3.1 RE(1)     | Cryptographic protection                       | Enhancement | Control system shall employ cryptographic mechanisms to recognize changes to information during transmission                          |     | R   | R   | R   |
| **SR 3.2** | Malicious code protection                      | Base        | Control system shall provide mechanisms to detect and prevent malicious code                                                          | R   | R   | R   | R   |
| SR 3.2 RE(1)     | Anti-virus/anti-malware                        | Enhancement | Control system shall employ anti-virus/anti-malware detection and eradication mechanisms                                              |     | R   | R   | R   |
| SR 3.2 RE(2)     | Code execution prevention                      | Enhancement | Control system shall employ application whitelisting to prevent execution of unauthorized code                                        |     |     | R   | R   |
| **SR 3.3** | Security functionality verification            | Base        | Control system shall verify correct operation of security functions upon startup and/or restart                                       | R   | R   | R   | R   |
| SR 3.3 RE(1)     | Notification of failed security tests          | Enhancement | Control system shall notify appropriate personnel of failed security verification tests                                               |     | R   | R   | R   |
| SR 3.3 RE(2)     | Automated verification and response            | Enhancement | Control system shall perform security verification automatically and shut down upon failure                                           |     |     | R   | R   |
| **SR 3.4** | Software and information integrity             | Base        | Control system shall detect unauthorized changes to software and information                                                          | R   | R   | R   | R   |
| SR 3.4 RE(1)     | Authenticity of software and information       | Enhancement | Control system shall verify the authenticity of software and information using checksums, cryptographic hashes, or digital signatures |     | R   | R   | R   |
| SR 3.4 RE(2)     | Automated notification of integrity violations | Enhancement | Control system shall provide automated notifications of detected integrity violations                                                 |     |     | R   | R   |
| **SR 3.5** | Input validation                               | Base        | Control system shall validate the syntax and semantics of all inputs                                                                  |     | R   | R   | R   |
| **SR 3.6** | Deterministic output                           | Base        | Control system shall produce deterministic output in response to specific inputs                                                      |     | R   | R   | R   |
| **SR 3.7** | Error handling                                 | Base        | Control system shall identify and handle error conditions in a secure manner                                                          | R   | R   | R   | R   |
| **SR 3.8** | Session integrity                              | Base        | Control system shall protect the integrity of communications sessions                                                                 |     | R   | R   | R   |
| SR 3.8 RE(1)     | Invalidate session IDs                         | Enhancement | Control system shall invalidate session identifiers upon logout or session termination                                                |     |     | R   | R   |
| **SR 3.9** | Protection of audit information                | Base        | Control system shall protect audit information and audit tools from unauthorized access, modification, and deletion                   | R   | R   | R   | R   |
| SR 3.9 RE(1)     | Access control for audit information           | Enhancement | Control system shall enforce access restrictions to audit information and tools                                                       |     | R   | R   | R   |

**Key Implementation Notes for FR 3**:

- SL 1 establishes basic integrity checking and malware detection awareness
- SL 2 requires cryptographic integrity protection and active anti-malware
- SL 3 mandates application whitelisting and automated integrity monitoring
- SL 4 maintains comprehensive integrity controls with enhanced enforcement

---

### 2.4 FR 4 - Data Confidentiality (DC)

**Purpose**: Prevent unauthorized disclosure of information on communication channels and in data repositories.

**Total Requirements**: 5 (3 Base + 2 Enhancements)

#### Security Requirements Detail

| SR ID            | Requirement Name              | Type        | Description                                                                                                                    | SL1 | SL2 | SL3 | SL4 |
| ---------------- | ----------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------ | --- | --- | --- | --- |
| **SR 4.1** | Information confidentiality   | Base        | Control system shall protect the confidentiality of information requiring confidentiality protection                           |     | R   | R   | R   |
| SR 4.1 RE(1)     | Encryption of data in transit | Enhancement | Control system shall employ cryptographic mechanisms to prevent unauthorized disclosure of information during transmission     |     |     | R   | R   |
| SR 4.1 RE(2)     | Encryption of data at rest    | Enhancement | Control system shall employ cryptographic mechanisms to prevent unauthorized disclosure of information at rest                 |     |     |     | R   |
| **SR 4.2** | Information persistence       | Base        | Control system shall prevent unauthorized and unintended information transfer via shared system resources                      |     | R   | R   | R   |
| **SR 4.3** | Use of cryptography           | Base        | Control system shall implement required cryptographic protections using cryptographic modules adhering to applicable standards |     | R   | R   | R   |

**Key Implementation Notes for FR 4**:

- Not required for SL 1 (casual threats don't typically target confidentiality)
- SL 2 requires protection of confidential information and proper crypto usage
- SL 3 mandates encryption in transit for sensitive data
- SL 4 requires encryption at rest for all sensitive information

---

### 2.5 FR 5 - Restricted Data Flow (RDF)

**Purpose**: Segment the control system into security zones and restrict data flows between zones and to/from external networks.

**Total Requirements**: 6 (4 Base + 2 Enhancements)

#### Security Requirements Detail

| SR ID            | Requirement Name                                            | Type        | Description                                                                                                                             | SL1 | SL2 | SL3 | SL4 |
| ---------------- | ----------------------------------------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------- | --- | --- | --- | --- |
| **SR 5.1** | Network segmentation                                        | Base        | Control system shall provide the capability to segment the network into separate security zones                                         | R   | R   | R   | R   |
| **SR 5.2** | Zone boundary protection                                    | Base        | Control system shall provide protection at the boundaries of security zones                                                             | R   | R   | R   | R   |
| SR 5.2 RE(1)     | Deny all, permit by exception                               | Enhancement | Control system shall deny network communications traffic by default and allow communications traffic by exception                       |     | R   | R   | R   |
| SR 5.2 RE(2)     | Island mode                                                 | Enhancement | Network device shall provide the capability to operate in island mode, preventing all communication through the control system boundary |     |     | R   | R   |
| **SR 5.3** | General purpose person-to-person communication restrictions | Base        | Control system shall prohibit or restrict the use of general purpose person-to-person communication services                            |     | R   | R   | R   |
| **SR 5.4** | Application partitioning                                    | Base        | Control system shall separate user functionality (including user interface services) from control system management functionality       |     | R   | R   | R   |

**Key Implementation Notes for FR 5**:

- SL 1 requires basic network segmentation (may be physical or logical)
- SL 2 mandates default-deny firewalls and elimination of person-to-person communication tools
- SL 3 adds island mode capability for complete isolation during emergencies
- Critical for preventing lateral movement of attackers

---

### 2.6 FR 6 - Timely Response to Events (TRE)

**Purpose**: Enable detection of security violations and support forensic analysis through logging and monitoring.

**Total Requirements**: 2 (2 Base + 0 Enhancements)

#### Security Requirements Detail

| SR ID            | Requirement Name        | Type | Description                                                                           | SL1 | SL2 | SL3 | SL4 |
| ---------------- | ----------------------- | ---- | ------------------------------------------------------------------------------------- | --- | --- | --- | --- |
| **SR 6.1** | Audit log accessibility | Base | Control system shall provide the capability for authorized users to access audit logs | R   | R   | R   | R   |
| **SR 6.2** | Continuous monitoring   | Base | Control system shall provide tools to monitor and log security events continuously    |     | R   | R   | R   |

**Key Implementation Notes for FR 6**:

- SL 1 requires audit log access but not necessarily real-time monitoring
- SL 2 and above require continuous security event monitoring
- Closely related to FR 2 (Use Control) audit requirements
- Foundation for security operations and incident response

---

### 2.7 FR 7 - Resource Availability (RA)

**Purpose**: Ensure availability of the control system in the presence of denial of service attacks or conditions and support recovery from incidents.

**Total Requirements**: 10 (8 Base + 2 Enhancements)

#### Security Requirements Detail

| SR ID            | Requirement Name                            | Type        | Description                                                                                                                           | SL1 | SL2 | SL3 | SL4 |
| ---------------- | ------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------- | --- | --- | --- | --- |
| **SR 7.1** | Denial of service protection                | Base        | Control system shall provide the capability to maintain essential functions during denial of service conditions                       |     |     |     | R   |
| **SR 7.2** | Resource management                         | Base        | Control system shall provide the capability to limit the use of resources by security functions                                       | R   | R   | R   | R   |
| **SR 7.3** | Control system backup                       | Base        | Control system shall provide the capability to perform backups of information                                                         | R   | R   | R   | R   |
| SR 7.3 RE(1)     | Backup verification                         | Enhancement | Control system shall provide the capability to verify the integrity of backup information                                             |     | R   | R   | R   |
| **SR 7.4** | Control system recovery and reconstitution  | Base        | Control system shall provide the capability to recover and reconstitute to a known secure state after a disruption or failure         | R   | R   | R   | R   |
| **SR 7.5** | Emergency power                             | Base        | Control system shall provide emergency power to facilitate transition of the control system to a safe mode in the event of power loss |     |     |     | R   |
| **SR 7.6** | Network and security configuration settings | Base        | Control system shall provide the capability to restrict the ability to configure network and security parameters                      | R   | R   | R   | R   |
| SR 7.6 RE(1)     | Machine-readable reporting                  | Enhancement | Control system shall provide machine-readable reporting of the current configuration state                                            |     | R   | R   | R   |
| **SR 7.7** | Least functionality                         | Base        | Control system shall be configured to provide only essential capabilities                                                             | R   | R   | R   | R   |
| **SR 7.8** | Control system component inventory          | Base        | Control system shall provide the capability to identify all software and firmware components                                          | R   | R   | R   | R   |

**Key Implementation Notes for FR 7**:

- SL 1-3 focus on backup, recovery, and configuration management
- SL 4 adds explicit DoS protection and emergency power requirements
- Asset inventory (SR 7.8) is foundational for all other security activities
- Least functionality (SR 7.7) reduces attack surface at all security levels

---

## 3. Security Requirements Mapping Tables

### 3.1 Summary Statistics

**Total Security Requirements Across All Foundational Requirements**: 82

- **Base Requirements**: 51 (62%)
- **Requirement Enhancements**: 31 (38%)

**Requirements by Security Level**:

| Security Level | Total Requirements | Percentage of Total | Increment from Previous Level    |
| -------------- | ------------------ | ------------------- | -------------------------------- |
| SL 1           | 32                 | 39%                 | Baseline                         |
| SL 2           | 64                 | 78%                 | +32 requirements (100% increase) |
| SL 3           | 77                 | 94%                 | +13 requirements (20% increase)  |
| SL 4           | 82                 | 100%                | +5 requirements (6% increase)    |

**Requirements Distribution by Foundational Requirement**:

| FR              | Foundational Requirement                        | Base Req     | Enhancements | Total        | % of Total SRs |
| --------------- | ----------------------------------------------- | ------------ | ------------ | ------------ | -------------- |
| FR 1            | Identification and Authentication Control (IAC) | 13           | 9            | 22           | 27%            |
| FR 2            | Use Control (UC)                                | 12           | 7            | 19           | 23%            |
| FR 3            | System Integrity (SI)                           | 9            | 9            | 18           | 22%            |
| FR 4            | Data Confidentiality (DC)                       | 3            | 2            | 5            | 6%             |
| FR 5            | Restricted Data Flow (RDF)                      | 4            | 2            | 6            | 7%             |
| FR 6            | Timely Response to Events (TRE)                 | 2            | 0            | 2            | 2%             |
| FR 7            | Resource Availability (RA)                      | 8            | 2            | 10           | 12%            |
| **TOTAL** |                                                 | **51** | **31** | **82** | **100%** |

### 3.2 Security Level Progression Analysis

**Cumulative Requirements by Security Level**:

| FR              | SL 1         | SL 2         | SL 3         | SL 4         | Total Possible |
| --------------- | ------------ | ------------ | ------------ | ------------ | -------------- |
| FR 1 - IAC      | 10           | 16           | 20           | 22           | 22             |
| FR 2 - UC       | 7            | 15           | 19           | 19           | 19             |
| FR 3 - SI       | 6            | 12           | 17           | 18           | 18             |
| FR 4 - DC       | 0            | 3            | 5            | 5            | 5              |
| FR 5 - RDF      | 2            | 6            | 6            | 6            | 6              |
| FR 6 - TRE      | 1            | 2            | 2            | 2            | 2              |
| FR 7 - RA       | 6            | 10           | 10           | 10           | 10             |
| **TOTAL** | **32** | **64** | **77** | **82** | **82**   |

**Key Observations**:

1. **Access Control Focus**: FR 1 (IAC) and FR 2 (UC) together represent 50% of all security requirements, emphasizing the critical importance of identity and access management
2. **SL 1 to SL 2 Jump**: The largest increase occurs between SL 1 and SL 2, doubling the number of requirements
3. **Confidentiality Not Required at SL 1**: FR 4 (Data Confidentiality) has no requirements at SL 1, reflecting that casual threats typically don't target confidentiality
4. **Availability Emphasis**: FR 7 (Resource Availability) maintains consistent requirements across SL 1-3, showing that availability is a constant concern in OT environments
5. **Progressive Enhancement**: Most FRs show steady progression, with SL 3 and SL 4 adding sophisticated protections

---

## 4. Criticality Assessment and SL-T Determination

### 4.1 Overview of SL-T Determination Process

Target Security Level (SL-T) determination is a risk-based process defined in IEC 62443-3-2. The process follows these steps:

1. **Identify System Under Consideration (SuC)**
2. **Perform High-Level Risk Assessment**
3. **Partition SuC into Zones and Conduits**
4. **Perform Detailed Risk Assessment for Each Zone**
5. **Determine SL-T Based on Risk Analysis**
6. **Document Requirements in Cybersecurity Requirements Specification (CRS)**
7. **Obtain Asset Owner Approval**

### 4.2 Consequence Severity Assessment

Evaluate potential consequences across four impact categories:

#### Impact Category Definitions

**1. Operational Impact**

| Severity         | Description                                   | Examples                                | Recovery Time |
| ---------------- | --------------------------------------------- | --------------------------------------- | ------------- |
| **Low**    | Minor disruption; easily recoverable          | Brief interruption, minor quality issue | Minutes       |
| **Medium** | Significant disruption; production affected   | Batch rejection, unplanned shutdown     | Hours         |
| **High**   | Major disruption; extended outage             | Production line stoppage, process upset | Days          |
| **Severe** | Critical failure; complete loss of capability | Plant-wide shutdown, cascading failures | Weeks+        |

**2. Financial Impact**

| Severity         | Description                 | Estimated Loss Range | Business Impact               |
| ---------------- | --------------------------- | -------------------- | ----------------------------- |
| **Low**    | Minimal financial loss      | < $10,000            | Negligible to operations      |
| **Medium** | Moderate financial loss     | $10,000 - $1,000,000 | Noticeable but manageable     |
| **High**   | Significant financial loss  | $1M - $10M           | Major impact on profitability |
| **Severe** | Catastrophic financial loss | > $10 million        | Threatens business viability  |

**3. Health, Safety & Environmental (HSE) Impact**

| Severity         | Description                                                  | Examples                                      | Regulatory Consequence                    |
| ---------------- | ------------------------------------------------------------ | --------------------------------------------- | ----------------------------------------- |
| **Low**    | Minor injury; no environmental impact                        | First aid injury, contained spill             | Internal incident report                  |
| **Medium** | Serious injury; localized environmental impact               | Recordable injury, limited release            | OSHA recordable, local reporting          |
| **High**   | Major injuries or fatality; significant environmental damage | Multiple hospitalizations, major spill        | OSHA investigation, EPA involvement       |
| **Severe** | Multiple fatalities; catastrophic environmental disaster     | Mass casualty event, widespread contamination | Federal investigation, criminal liability |

**4. Regulatory/Compliance Impact**

| Severity         | Description                  | Potential Consequences                          |
| ---------------- | ---------------------------- | ----------------------------------------------- |
| **Low**    | Minor compliance issue       | Warning letters, corrective action              |
| **Medium** | Compliance violation         | Fines, penalties, increased oversight           |
| **High**   | Serious regulatory violation | Consent decrees, operational restrictions       |
| **Severe** | Critical violations          | License suspension/revocation, criminal charges |

### 4.3 Threat Capability and Likelihood Assessment

#### Threat Actor Categorization

| Threat Actor Type                           | Capability Level | Typical Attack Scenarios                                     | Applicable SL |
| ------------------------------------------- | ---------------- | ------------------------------------------------------------ | ------------- |
| **Insider - Accidental**              | Low              | Misconfiguration, unintentional data exposure                | SL 1          |
| **Insider - Malicious**               | Low-Moderate     | Sabotage, data theft, unauthorized access                    | SL 2          |
| **Script Kiddie / Low-Level Hacker**  | Low              | Automated scanning, known exploit usage                      | SL 2          |
| **Skilled Hacker / Cybercriminal**    | Moderate         | Custom exploits, social engineering, ransomware              | SL 3          |
| **Organized Crime / Hactivist Group** | Moderate-High    | Coordinated attacks, APT tactics, extortion                  | SL 3          |
| **Nation State / APT**                | High             | Zero-day exploits, supply chain attacks, long-term campaigns | SL 4          |

#### Likelihood Assessment Factors

Assess likelihood based on:

1. **Historical Attack Data**: Have similar assets/industries been targeted?
2. **Threat Intelligence**: Are active threats known for this sector?
3. **Asset Exposure**: How accessible is the asset to potential attackers?
4. **Attractiveness**: What value does the asset present to attackers?
5. **Existing Controls**: What defenses are currently in place?

**Likelihood Categories**:

- **Unlikely**: Rare occurrence, limited threat actor interest
- **Possible**: Occasional occurrence, some threat actor interest
- **Likely**: Frequent occurrence, high threat actor interest
- **Highly Likely**: Regular occurrence, known active targeting

### 4.4 Risk Matrix for SL-T Determination

Use the following risk matrix to determine appropriate Target Security Level:

| Consequence Severity | Threat Likelihood | Initial Risk Level | Recommended SL-T | Justification                                        |
| -------------------- | ----------------- | ------------------ | ---------------- | ---------------------------------------------------- |
| Low                  | Unlikely          | Low                | **SL 0-1** | Minimal risk; basic controls sufficient              |
| Low                  | Possible          | Low                | **SL 1**   | Low consequence limits maximum risk                  |
| Low                  | Likely            | Medium             | **SL 2**   | Higher likelihood warrants better protection         |
| Low                  | Highly Likely     | Medium             | **SL 2**   | Frequent attacks but limited consequence             |
| Medium               | Unlikely          | Low                | **SL 1**   | Infrequent targeting allows lower controls           |
| Medium               | Possible          | Medium             | **SL 2**   | Balanced risk requires intentional attack protection |
| Medium               | Likely            | High               | **SL 3**   | Probable attacks with moderate consequence           |
| Medium               | Highly Likely     | High               | **SL 3**   | Active targeting with noticeable impact              |
| High                 | Unlikely          | Medium             | **SL 2**   | Rare but serious consequence                         |
| High                 | Possible          | High               | **SL 3**   | Significant risk requires sophisticated protection   |
| High                 | Likely            | Critical           | **SL 4**   | Major consequence with high probability              |
| High                 | Highly Likely     | Critical           | **SL 4**   | Maximum protection required                          |
| Severe               | Possible          | Critical           | **SL 4**   | Catastrophic consequences demand highest security    |
| Severe               | Likely            | Critical           | **SL 4**   | Maximum threat and consequence                       |
| Severe               | Highly Likely     | Critical           | **SL 4**   | Clear and present danger                             |

**Risk Level Definitions**:

- **Low Risk**: Acceptable with minimal controls
- **Medium Risk**: Requires risk mitigation; implement moderate controls
- **High Risk**: Significant risk mitigation required; implement comprehensive controls
- **Critical Risk**: Unacceptable without maximum security; implement all available controls

### 4.5 Asset Criticality Assessment Framework

Assess each asset or zone using the following factors:

#### Criticality Assessment Checklist

| Assessment Factor                 | Weight        | Key Questions                                                                                                                                        | Scoring Guidance                                                                                                                                     |
| --------------------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Process Criticality**     | High (3x)     | • Is this asset essential to primary production?`<br>`• Can operations continue without it?`<br>`• Is it a single point of failure?           | Critical: Essential, no alternatives `<br>`High: Very important `<br>`Medium: Important but not critical `<br>`Low: Nice to have               |
| **Safety Impact**           | Critical (5x) | • Could compromise lead to injury or death?`<br>`• Does it control safety systems?`<br>`• What is worst-case safety consequence?              | Critical: Potential fatalities `<br>`High: Serious injuries `<br>`Medium: Minor injuries `<br>`Low: No direct safety impact                    |
| **Environmental Impact**    | High (3x)     | • Could compromise cause environmental damage?`<br>`• Are hazardous materials involved?`<br>`• What is spill/release potential?               | Critical: Major environmental disaster `<br>`High: Significant damage `<br>`Medium: Localized impact `<br>`Low: Minimal impact                 |
| **Production Impact**       | Medium (2x)   | • What is production/revenue loss if compromised?`<br>`• How long for recovery?`<br>`• What are downstream effects?                           | Critical: > $10M loss `<br>`High: $1M-$10M `<br>`Medium: $10K-$1M `<br>`Low: < $10K                                                            |
| **Quality Impact**          | Medium (2x)   | • Could compromise affect product quality?`<br>`• Could it cause recalls or reputational damage?`<br>`• Are quality control systems involved? | Critical: Major recalls, brand damage `<br>`High: Significant quality issues `<br>`Medium: Minor quality problems `<br>`Low: No quality impact |
| **Regulatory Requirements** | High (3x)     | • Are there specific regulations for this asset?`<br>`• What are compliance obligations?`<br>`• What are penalties for violations?            | Critical: License suspension risk `<br>`High: Significant penalties `<br>`Medium: Fines possible `<br>`Low: Minimal regulatory concern         |
| **Recovery Time**           | Medium (2x)   | • How long to restore after incident?`<br>`• Are spare parts readily available?`<br>`• Is specialized expertise required?                     | Critical: > 7 days `<br>`High: 2-7 days `<br>`Medium: Hours to 2 days `<br>`Low: < 4 hours                                                     |
| **Redundancy Available**    | Medium (2x)   | • Are backup systems available?`<br>`• Can manual operations continue?`<br>`• What is failover capability?                                    | Critical: No redundancy `<br>`High: Limited backup `<br>`Medium: Partial redundancy `<br>`Low: Full redundancy                                 |
| **Attack Surface Exposure** | Medium (2x)   | • How accessible to attackers?`<br>`• Connected to external networks?`<br>`• Known vulnerabilities?                                           | Critical: Internet-exposed `<br>`High: External connections `<br>`Medium: Internal networks only `<br>`Low: Air-gapped                         |
| **Data Sensitivity**        | Medium (2x)   | • Does asset process sensitive data?`<br>`• Are trade secrets involved?`<br>`• Is personal information present?                               | Critical: Critical IP or PHI `<br>`High: Significant proprietary data `<br>`Medium: Some sensitive data `<br>`Low: No sensitive data           |

#### Criticality Scoring Method

1. **Score each factor** on 1-5 scale:

   - 5 = Critical
   - 4 = High
   - 3 = Medium
   - 2 = Low
   - 1 = Minimal/None
2. **Apply weights** (multiply score by weight factor)
3. **Calculate total weighted score**
4. **Determine criticality classification**:

   - **80-100**: Critical Asset (Typically SL 3-4)
   - **60-79**: High Criticality (Typically SL 2-3)
   - **40-59**: Medium Criticality (Typically SL 1-2)
   - **< 40**: Low Criticality (Typically SL 0-1)

**Note**: Safety Impact should be given special consideration - any asset with Critical or High safety impact should automatically be considered for SL 3 or higher, regardless of other factors.

### 4.6 SL-T Determination Methodology

#### Step-by-Step Process

**Step 1: Identify All Assets in Zone or System**

- Create comprehensive asset inventory
- Document asset types, functions, connections
- Identify dependencies and relationships

**Step 2: Assess Consequences**

- Evaluate impact across all four categories (Operational, Financial, HSE, Regulatory)
- Identify worst-case consequence for each category
- Select highest severity rating as overall consequence severity

**Step 3: Determine Threat Likelihood**

- Analyze threat environment
- Review threat intelligence for sector
- Assess asset attractiveness and exposure
- Determine likelihood category

**Step 4: Calculate Risk Level**

- Use Risk Matrix (Section 4.4)
- Map Consequence Severity + Threat Likelihood to Risk Level
- Identify Initial Risk Level

**Step 5: Determine Preliminary SL-T**

- Use Risk Matrix recommendations
- Consider criticality assessment results
- Review regulatory requirements
- Consider organizational risk tolerance

**Step 6: Validate and Adjust**

- Compare with similar zones/systems
- Consider operational constraints
- Verify technical feasibility
- Confirm with stakeholders

**Step 7: Document Rationale**

- Record assessment data
- Document assumptions
- Explain SL-T selection
- Include in Cybersecurity Requirements Specification (CRS)

**Step 8: Obtain Approval**

- Present to asset owner
- Address any concerns
- Obtain formal acceptance
- Document approval

### 4.7 Special Considerations

#### Safety Systems (SIS/ESD)

Safety Instrumented Systems require special consideration:

- **Minimum SL-T**: Typically SL 2 or higher
- **Independence**: Must maintain separation from basic process control
- **Availability Priority**: Security controls must not compromise safety functions
- **Standards Compliance**: Must align with IEC 61508/61511
- **Common Range**: SL 3-4 for critical safety systems

#### Legacy Systems

Systems that cannot be upgraded:

- **Compensating Controls**: Use network segmentation, monitoring, physical security
- **Defense in Depth**: Protect through surrounding architecture
- **Risk Acceptance**: May require formal risk acceptance
- **Isolation**: Consider air-gapping or unidirectional gateways
- **Sunset Planning**: Develop migration strategy

#### Cloud/IIoT Systems

Modern connected systems:

- **Encryption Required**: Data in transit and at rest
- **Identity Management**: Strong authentication and authorization
- **Supply Chain Risk**: Assess vendor security practices
- **Data Residency**: Consider regulatory requirements
- **Typical SL-T**: SL 2-3 depending on data sensitivity

---

## 5. Zone Classification Framework

### 5.1 Standard Zone Types

IEC 62443 recommends organizing IACS into logical security zones. The following table provides typical zone classifications:

| Zone Type                           | Typical Assets                                                                                                                            | Common SL-T Range | Primary Security Concerns                                                                                                | Typical Security Controls                                                                                                                                     |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Corporate/Enterprise Zone** | • Business servers `<br>`• Office workstations `<br>`• Email servers `<br>`• ERP systems                                        | **SL 1**    | • Malware entry point `<br>`• Data confidentiality `<br>`• Phishing attacks                                       | • Endpoint protection `<br>`• User training `<br>`• Email filtering `<br>`• Patch management                                                        |
| **Industrial DMZ**            | • Data historians `<br>`• Application servers `<br>`• HMI/SCADA gateways `<br>`• Reporting servers                              | **SL 2**    | • IT/OT bridge `<br>`• Data exfiltration `<br>`• Lateral movement                                                 | • Firewalls `<br>`• Data diodes `<br>`• Least privilege `<br>`• Network monitoring                                                                  |
| **Supervisory Control Zone**  | • SCADA servers `<br>`• Engineering workstations `<br>`• HMI servers `<br>`• Supervisory PLCs                                   | **SL 2-3**  | • Control integrity `<br>`• Availability `<br>`• Unauthorized changes                                             | • Application whitelisting `<br>`• Change control `<br>`• Access control `<br>`• Backup systems                                                     |
| **Basic Control Zone**        | • Process PLCs `<br>`• DCS controllers `<br>`• Local HMIs `<br>`• Control network switches                                      | **SL 2-3**  | • Process integrity `<br>`• Availability `<br>`• Real-time performance                                            | • Network segmentation `<br>`• Protocol filtering `<br>`• Anomaly detection `<br>`• Physical security                                               |
| **Safety System Zone**        | • Safety PLCs (SIS)`<br>`• Emergency shutdown systems `<br>`• Fire & gas detection `<br>`• Safety controllers                   | **SL 3-4**  | • Safety function integrity `<br>`• Independence from control `<br>`• Availability `<br>`• Unauthorized access | • Air-gapping (where feasible)`<br>`• Strict access control `<br>`• Change management `<br>`• Diverse systems `<br>`• Physical protection        |
| **Field Device Zone**         | • Sensors (temperature, pressure, flow)`<br>`• Actuators (valves, motors)`<br>`• Field instruments `<br>`• RTUs `<br>`• IEDs | **SL 2**    | • Physical tampering `<br>`• Signal integrity `<br>`• Unauthorized devices                                        | • Physical security `<br>`• Device authentication `<br>`• Network access control `<br>`• Asset management                                           |
| **Remote Access Zone**        | • VPN gateways `<br>`• Remote access servers `<br>`• Jump hosts `<br>`• Vendor access systems                                   | **SL 2-3**  | • Authentication `<br>`• Encrypted communications `<br>`• Unauthorized access `<br>`• Lateral movement         | • Multi-factor authentication `<br>`• VPN encryption `<br>`• Session monitoring `<br>`• Time-limited access `<br>`• Privileged access management |

### 5.2 Conduit Security Requirements

Conduits connect zones and must be protected based on the highest SL-T of the zones they connect.

#### Conduit Protection Methods

| Connection Type                        | Typical Conduits                                                              | Required Protection (SL 2+)                                                                                  | Required Protection (SL 3+)                                                                              |
| -------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| **Enterprise to DMZ**            | • Data feeds `<br>`• Reporting queries `<br>`• User access             | • Stateful firewall `<br>`• Deny by default `<br>`• Application filtering                             | • IDS/IPS `<br>`• Advanced threat protection `<br>`• Data loss prevention                         |
| **DMZ to Supervisory**           | • Process data `<br>`• Alarm notifications `<br>`• Engineering access  | • Industrial firewall `<br>`• Protocol validation `<br>`• Deep packet inspection                      | • Unidirectional gateway (data historian)`<br>`• Encrypted channels `<br>`• Continuous monitoring |
| **Supervisory to Basic Control** | • Setpoints `<br>`• Commands `<br>`• Status updates                    | • Network segmentation `<br>`• VLAN isolation `<br>`• ACLs                                            | • Protocol-aware firewall `<br>`• Anomaly detection `<br>`• Rate limiting                         |
| **Basic Control to Field**       | • Sensor readings `<br>`• Actuator commands `<br>`• Fieldbus traffic   | • Physical network separation `<br>`• Protocol filtering `<br>`• Device authentication                | • Encrypted protocols (where feasible)`<br>`• Network access control `<br>`• Intrusion detection  |
| **Safety to Other Zones**        | • Status monitoring `<br>`• Test signals `<br>`• Limited data exchange | • Unidirectional communication (where possible)`<br>`• Strict firewall rules `<br>`• Read-only access | • Air-gap (preferred)`<br>`• Data diodes `<br>`• Separate physical network                        |
| **Remote Access**                | • VPN connections `<br>`• Vendor support `<br>`• Remote monitoring     | • VPN with MFA `<br>`• Session monitoring `<br>`• Time restrictions                                   | • Encrypted VPN `<br>`• Privileged access management `<br>`• Jump host architecture               |

### 5.3 Zone Design Principles

#### 1. Separation of IT and OT

**Rationale**: Different security priorities (IT: Confidentiality, OT: Availability)

**Implementation**:

- Physical or logical network separation
- Industrial DMZ as buffer zone
- Separate authentication systems
- Different patch management schedules

#### 2. Safety System Independence

**Rationale**: Safety systems must remain functional even if control systems are compromised

**Implementation**:

- Dedicated safety zone
- Air-gapped or unidirectional communication
- Independent engineering workstations
- Separate access control

#### 3. Defense in Depth

**Rationale**: Multiple layers of protection slow attackers and provide detection opportunities

**Implementation**:

- Multiple zones with increasing security levels toward critical assets
- Firewall at each zone boundary
- Progressive access restrictions
- Layered monitoring

#### 4. Least Privilege

**Rationale**: Limit access to minimum required for job functions

**Implementation**:

- Zone-specific user accounts
- Role-based access control (RBAC)
- Time-limited access for vendors
- Jump hosts for administrative access

### 5.4 Example Zone Architectures

#### Manufacturing Facility Example

```
┌─────────────────────────────────────────────────────────┐
│ Level 5: Enterprise Zone (SL 1)                        │
│ ERP, Email, Business Applications                       │
└────────────────┬────────────────────────────────────────┘
                 │ Firewall, DMZ
┌────────────────▼────────────────────────────────────────┐
│ Level 3.5: Industrial DMZ (SL 2)                       │
│ Historians, Application Servers, Reporting              │
└────────────────┬────────────────────────────────────────┘
                 │ Industrial Firewall
┌────────────────▼────────────────────────────────────────┐
│ Level 3: Supervisory Control (SL 2-3)                  │
│ SCADA, HMI, Engineering Workstations                    │
└────────┬───────┴────────┬───────────────────────────────┘
         │                │ Protocol Firewall
┌────────▼─────┐  ┌───────▼──────┐  ┌──────────────────┐
│ Level 2:     │  │ Level 2:     │  │ Safety Zone      │
│ Assembly Line│  │ Packaging    │  │ (SL 3-4)         │
│ Control      │  │ Control      │  │ Air-gapped       │
│ (SL 2-3)     │  │ (SL 2)       │  │ Emergency Stop   │
└──────┬───────┘  └──────┬───────┘  └────────┬─────────┘
       │                 │                    │
┌──────▼─────────────────▼────────────────────▼─────────┐
│ Level 1 & 0: Field Devices (SL 2)                     │
│ Sensors, Actuators, Motor Controls                     │
└────────────────────────────────────────────────────────┘
```

#### Process Industry Example (Oil & Gas, Chemical)

```
┌──────────────────────────────────────────────────┐
│ Corporate Network (SL 1)                         │
└────────────┬─────────────────────────────────────┘
             │ Unidirectional Gateway
┌────────────▼─────────────────────────────────────┐
│ DMZ: Historians & Reporting (SL 2)              │
└────────────┬─────────────────────────────────────┘
             │ Firewall
┌────────────▼─────────────────────────────────────┐
│ Control Network: DCS/SCADA (SL 2-3)            │
├──────────────┬───────────────┬───────────────────┤
│              │               │                   │
│  ┌───────────▼──┐  ┌────────▼───────┐  ┌───────▼──────┐
│  │Process Unit 1│  │Process Unit 2  │  │Utilities     │
│  │(SL 2-3)      │  │(SL 2-3)        │  │(SL 2)        │
│  └──────┬───────┘  └────┬───────────┘  └──────────────┘
│         │               │
│  ┌──────▼──────────────▼───────┐
│  │ Field Networks (SL 2)       │
│  └─────────────────────────────┘
│
├────────── Physically Separate ──────────────────┐
│                                                  │
│  ┌──────────────────────────────────────┐      │
│  │ Safety Instrumented System (SL 3-4)  │      │
│  │ - Independent SIS Controllers        │      │
│  │ - Emergency Shutdown Devices         │      │
│  │ - Safety Sensors & Final Elements    │      │
│  └──────────────────────────────────────┘      │
└─────────────────────────────────────────────────┘
```

---

## 6. Implementation Methodology

### 6.1 Phased Implementation Approach

#### Phase 1: Assessment and Planning (Months 1-3)

**Objectives**:

- Understand current state
- Define target state
- Develop roadmap

**Activities**:

1. **Asset Discovery and Inventory**

   - Identify all IACS assets
   - Document network architecture
   - Map communication flows
   - Catalog software versions and configurations
2. **Gap Assessment**

   - Compare current security controls to IEC 62443 requirements
   - Identify missing security capabilities
   - Assess existing security levels (SL-A)
   - Document compensating controls
3. **Risk Assessment**

   - Identify critical assets and processes
   - Perform consequence and likelihood analysis
   - Determine target security levels (SL-T) for zones
   - Document risk treatment decisions
4. **Zone and Conduit Design**

   - Define logical security zones
   - Specify conduit requirements
   - Design network segmentation architecture
   - Plan firewall placements and rules
5. **Roadmap Development**

   - Prioritize initiatives based on risk
   - Sequence projects considering dependencies
   - Estimate resources and budget
   - Define milestones and success criteria

**Deliverables**:

- Asset inventory database
- Current state security assessment
- Zone and conduit architecture diagrams
- Risk assessment report with SL-T assignments
- Cybersecurity Requirements Specification (CRS)
- Multi-year implementation roadmap

#### Phase 2: Quick Wins and Foundation (Months 3-6)

**Objectives**:

- Implement high-value, low-complexity improvements
- Establish security foundations
- Build momentum

**Activities**:

1. **Account and Access Management**

   - Eliminate shared accounts (move SL 1 → SL 2)
   - Implement individual user accounts
   - Deploy role-based access control (RBAC)
   - Remove unnecessary user accounts
2. **Basic Network Segmentation**

   - Implement VLANs to separate zones
   - Deploy basic firewalls at zone boundaries
   - Configure deny-by-default policies
   - Restrict lateral movement
3. **Asset Hardening**

   - Disable unnecessary services (SR 7.7)
   - Remove or disable unused accounts
   - Configure secure defaults
   - Enable logging (SR 2.8)
4. **Visibility and Monitoring**

   - Deploy network monitoring tools
   - Implement SIEM or log aggregation
   - Establish baseline network behavior
   - Create initial detection rules
5. **Policy and Procedure Development**

   - Create security policies
   - Define change management procedures
   - Establish incident response plan
   - Develop backup and recovery procedures

**Deliverables**:

- Improved access control implementation
- Basic network segmentation deployed
- Hardened system configurations
- Monitoring infrastructure operational
- Security policies documented and approved

#### Phase 3: Core Security Controls (Months 6-18)

**Objectives**:

- Implement comprehensive security controls
- Achieve SL 2 for target zones
- Deploy industrial security infrastructure

**Activities**:

1. **Advanced Network Segmentation**

   - Deploy industrial firewalls
   - Implement protocol-aware filtering
   - Configure advanced ACLs
   - Deploy unidirectional gateways for critical data flows
2. **Malware Protection**

   - Deploy anti-virus/anti-malware (SR 3.2)
   - Implement application whitelisting (SR 3.2 RE(2))
   - Configure secure boot where possible
   - Establish malware response procedures
3. **Patch and Vulnerability Management**

   - Implement patch assessment process
   - Create test environments
   - Deploy patch management tools
   - Establish patching schedules by zone
4. **Backup and Recovery**

   - Implement automated backup systems (SR 7.3)
   - Test backup restoration procedures
   - Document recovery procedures (SR 7.4)
   - Establish recovery time objectives (RTO)
5. **Authentication Enhancements**

   - Deploy multi-factor authentication for remote access
   - Implement PKI where feasible (SR 1.8, SR 1.9)
   - Strengthen password policies (SR 1.7)
   - Implement account lockout policies (SR 1.11)
6. **Audit and Logging**

   - Centralize log collection (SR 2.9)
   - Implement log integrity protection (SR 3.9)
   - Configure alerting on security events
   - Establish log retention policies

**Deliverables**:

- Industrial firewall infrastructure deployed
- Malware protection on all applicable systems
- Patch management program operational
- Backup and recovery capabilities tested
- Enhanced authentication deployed
- Comprehensive logging and monitoring

#### Phase 4: Advanced Controls (Months 18-36)

**Objectives**:

- Achieve SL 3 for critical zones
- Implement advanced detection and response
- Establish continuous monitoring

**Activities**:

1. **Enhanced Monitoring and Detection**

   - Deploy IDS/IPS tuned for industrial protocols
   - Implement behavioral anomaly detection
   - Configure automated alerting and response
   - Establish Security Operations Center (SOC) capability
2. **Encryption Implementation**

   - Encrypt sensitive data in transit (SR 4.1 RE(1))
   - Implement VPN encryption for remote access
   - Deploy secure protocols (TLS, SSH)
   - Manage cryptographic keys (SR 4.3)
3. **Advanced Access Controls**

   - Implement privileged access management (PAM)
   - Deploy jump hosts for administrative access
   - Time-limit vendor access
   - Implement session recording for critical access
4. **Integrity Verification**

   - Deploy file integrity monitoring
   - Implement software authentication (SR 3.4 RE(1))
   - Configure automated integrity checking
   - Alert on unauthorized changes
5. **Island Mode Capability**

   - Implement island mode for critical zones (SR 5.2 RE(2))
   - Test isolation procedures
   - Document emergency isolation protocols
   - Train operators on activation procedures
6. **Continuous Improvement**

   - Perform regular security assessments
   - Update threat intelligence
   - Adjust security controls based on lessons learned
   - Refine detection and response procedures

**Deliverables**:

- Advanced threat detection deployed
- Encryption implemented for sensitive data
- Privileged access management operational
- Integrity monitoring established
- Island mode capability tested
- Mature security operations

#### Phase 5: Optimization and Maturity (Ongoing)

**Objectives**:

- Maintain and improve security posture
- Adapt to evolving threats
- Achieve organizational maturity

**Activities**:

1. **Security Program Maturity**

   - Progress from Maturity Level 1 (Initial) to Level 3 (Defined/Practiced)
   - Document all procedures with evidence of practice
   - Establish metrics and KPIs
   - Pursue security program certification
2. **Threat-Informed Defense**

   - Subscribe to threat intelligence feeds
   - Participate in information sharing (ISACs)
   - Conduct threat hunting exercises
   - Update defenses based on emerging threats
3. **Advanced Testing**

   - Perform penetration testing
   - Conduct red team exercises
   - Test incident response plans
   - Validate disaster recovery procedures
4. **Supply Chain Security**

   - Assess vendor security practices
   - Include security requirements in procurement
   - Verify component security levels (SL-C)
   - Manage third-party risks
5. **Training and Awareness**

   - Provide role-specific security training
   - Conduct social engineering awareness
   - Train incident response teams
   - Certify personnel (IEC 62443 certificates)

**Deliverables**:

- Mature security program (ML 3)
- Threat-informed security operations
- Validated security capabilities through testing
- Secured supply chain
- Well-trained workforce

### 6.2 Resource Requirements

#### Personnel Requirements by Phase

| Phase                   | Security Staff | IT/OT Engineering | Operations | External Support            |
| ----------------------- | -------------- | ----------------- | ---------- | --------------------------- |
| Phase 1 (Assessment)    | 1-2 FTE        | 2-3 FTE           | 1-2 FTE    | Consultants for RA & Design |
| Phase 2 (Quick Wins)    | 2 FTE          | 3-4 FTE           | 2 FTE      | Project management          |
| Phase 3 (Core Controls) | 3-4 FTE        | 4-6 FTE           | 2-3 FTE    | Implementation support      |
| Phase 4 (Advanced)      | 4-5 FTE        | 3-4 FTE           | 2-3 FTE    | Specialized expertise       |
| Phase 5 (Optimization)  | 3-4 FTE        | 2-3 FTE           | 2 FTE      | Testing & audit services    |

#### Typical Budget Allocation

| Category                       | % of Total Budget | Typical Range (Medium Facility) |
| ------------------------------ | ----------------- | ------------------------------- |
| Technology (Hardware/Software) | 40-50%            | $500K - $2M                     |
| Professional Services          | 20-30%            | $250K - $1M                     |
| Internal Labor                 | 20-30%            | $300K - $1M                     |
| Training & Certification       | 5-10%             | $50K - $200K                    |
| **TOTAL 3-Year Program** | **100%**    | **$1.1M - $4.2M**         |

*Note: Costs vary significantly based on facility size, complexity, current security posture, and target security levels*

### 6.3 Success Factors

1. **Executive Support**: Secure C-level sponsorship and adequate resources
2. **Cross-Functional Teams**: Involve IT, OT, Engineering, Operations, and Safety
3. **Risk-Based Prioritization**: Focus on highest risks and critical assets first
4. **Pragmatic Approach**: Balance perfect security with operational realities
5. **Change Management**: Communicate changes and provide training
6. **Continuous Improvement**: Treat security as ongoing journey, not one-time project

---

## 7. Asset-Specific Security Level Guidance

### 7.1 Component-Specific Requirements

Different asset types have different applicable security requirements and achievable security levels.

#### Windows-Based Systems (HMI, Historian, Engineering Workstation)

**Characteristics**:

- General-purpose operating systems
- Full SR applicability
- Broad attack surface
- Extensive security control options

**Typical SL-C**: SL 2-3 (SL 4 with hardening and additional controls)

**Key Security Controls by SL**:

| Security Level | Required Controls                                                                                                                                                                                                                                                                                                            |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SL 1** | • Individual user accounts `<br>`• Basic password requirements `<br>`• Windows Defender or equivalent `<br>`• Basic firewall `<br>`• Manual updates                                                                                                                                                             |
| **SL 2** | • Role-based access control `<br>`• Strong password policy `<br>`• Application whitelisting (e.g., AppLocker)`<br>`• Host-based firewall with restrictive rules `<br>`• Centralized logging `<br>`• Regular patching `<br>`• Anti-malware with updates                                                    |
| **SL 3** | • Privileged access management `<br>`• Multi-factor authentication for admin `<br>`• Full application whitelisting `<br>`• File integrity monitoring `<br>`• Encrypted communications `<br>`• Automated patch management `<br>`• EDR/Advanced threat protection `<br>`• Regular vulnerability scanning |
| **SL 4** | • Hardware security modules `<br>`• Full disk encryption `<br>`• Network isolation or air-gap `<br>`• Physical security controls `<br>`• Comprehensive monitoring and alerting `<br>`• Automated response capabilities                                                                                       |

**Applicable FRs**: All (FR 1-7)

**Common Challenges**:

- Patch management without disrupting operations
- Performance impact of security controls
- Legacy applications requiring older OS versions
- User resistance to security restrictions

**Best Practices**:

- Use Windows 10/11 IoT Enterprise LTSC editions
- Leverage Group Policy for centralized management
- Implement staged patching with test environments
- Use separate engineering workstations (not dual-purpose)

#### Programmable Logic Controllers (PLCs)

**Characteristics**:

- Embedded systems with proprietary OS
- Limited security capabilities
- Real-time requirements
- Safety-critical functions

**Typical SL-C**: SL 1-2 (rarely higher without extensive compensating controls)

**Key Security Controls by SL**:

| Security Level | Required Controls                                                                                                                                                                                                                                                                                             |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SL 1** | • Default account password changes `<br>`• Physical security of cabinets `<br>`• Network isolation `<br>`• Program backups `<br>`• Change documentation                                                                                                                                          |
| **SL 2** | • Unique user accounts (if supported)`<br>`• Authentication for programming access `<br>`• Role-based authorization `<br>`• Program version control `<br>`• Digital signatures on program files `<br>`• Network segmentation with firewall `<br>`• Protocol filtering                      |
| **SL 3** | • Strong authentication for all access `<br>`• Encrypted programming connections `<br>`• Integrity verification of firmware `<br>`• Continuous monitoring of network traffic `<br>`• Anomaly detection `<br>`• Defense-in-depth through network controls `<br>`• Physical tamper detection |
| **SL 4** | • Hardware security features (if available)`<br>`• Air-gapped or unidirectional network connections `<br>`• Comprehensive compensating controls `<br>`• Diverse redundant systems                                                                                                                   |

**Limited Capabilities**:

- Most PLCs have minimal logging
- Application whitelisting not applicable (fixed firmware)
- Cannot install endpoint security agents
- Limited authentication options on older models

**Compensating Controls Strategy**:
Since PLCs often cannot meet all SRs directly, achieve target SL through:

- **Network Controls**: Firewalls, protocol filters, IDS/IPS
- **Physical Security**: Locked cabinets, access logging
- **Process Controls**: Change management, version control, testing
- **Monitoring**: Network-based anomaly detection

**Applicable FRs**: Primarily FR 1, FR 2 (limited), FR 5, FR 7

**Best Practices**:

- Select modern PLCs with better security features
- Implement defense-in-depth around PLCs
- Use engineering workstation security to protect programming interface
- Maintain air-gap or strict segmentation where possible
- Consider secure PLCs for new projects (ISASecure certified)

#### Network Infrastructure (Switches, Routers, Firewalls)

**Characteristics**:

- Infrastructure components
- Configuration-based security
- Critical to overall architecture
- Must maintain performance

**Typical SL-C**: SL 2-3 for industrial-grade devices

**Key Security Controls by SL**:

| Security Level | Required Controls                                                                                                                                                                                                                                                        |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **SL 1** | • Change default passwords `<br>`• Disable unnecessary services `<br>`• Enable basic logging `<br>`• Physical security                                                                                                                                         |
| **SL 2** | • Individual admin accounts `<br>`• Role-based access `<br>`• Encrypted management protocols (SSH, HTTPS)`<br>`• Configuration backups `<br>`• Centralized logging `<br>`• Change management `<br>`• Time synchronization                             |
| **SL 3** | • Strong authentication for admin access `<br>`• Multi-factor authentication `<br>`• Automated configuration compliance checking `<br>`• Integrity verification of firmware `<br>`• Advanced logging and alerting `<br>`• Out-of-band management network |
| **SL 4** | • Hardware security modules `<br>`• Redundant security devices `<br>`• Comprehensive monitoring `<br>`• Automated threat response                                                                                                                              |

**Applicable FRs**: FR 1, FR 2, FR 5, FR 6, FR 7

**Best Practices**:

- Use industrial-grade network equipment rated for OT environments
- Implement separate management network (out-of-band)
- Configure deny-by-default policies
- Enable protocol filtering and deep packet inspection
- Maintain configuration version control
- Use network management tools for compliance monitoring

#### Safety Instrumented Systems (SIS)

**Characteristics**:

- Safety-critical functions per IEC 61508/61511
- Must maintain SIL ratings
- High availability requirements
- Independence from basic process control

**Typical SL-T**: SL 3-4 (high criticality)
**Typical SL-C**: SL 1-2 (limited capabilities)

**Special Considerations**:

1. **Safety Priority**: Security controls must not compromise safety functions
2. **Independence**: SIS must remain functional if BPCS is compromised
3. **Availability**: Security controls must not reduce SIS availability
4. **Proven in Use**: Prefer certified safety components

**Security Approach**:

- **Physical Isolation**: Separate network, dedicated engineering workstation
- **Access Control**: Strict limitation on who can modify SIS
- **Change Management**: Rigorous safety assessment of all changes
- **Monitoring**: Read-only connections for status monitoring
- **Testing**: Regular proof testing must not be hindered

**Key Controls**:

- Air-gap or unidirectional gateway from BPCS
- Dedicated SIS engineering workstation (not networked)
- Physical security (locked cabinets, access logging)
- Strict change management with safety review
- Separate user accounts from BPCS
- Configuration management and version control

**Applicable FRs**: FR 1 (limited), FR 2 (limited), FR 5 (critical), FR 7 (availability focus)

**Best Practices**:

- Maintain complete separation from control networks
- Use dedicated engineering tools for SIS
- Implement compensating controls for requirements SIS cannot directly meet
- Coordinate security and safety assessments
- Follow IEC 61511 guidance on cybersecurity

### 7.2 System Integration Considerations

When integrating components to achieve system-level SL-T:

1. **Weakest Link**: System SL-A is limited by the lowest SL-C of critical components
2. **Compensating Controls**: Use system-level controls to raise overall SL-A
3. **Defense in Depth**: Layer controls to provide multiple barriers
4. **Architectural Controls**: Network segmentation and boundary protection are critical
5. **Monitoring**: System-wide monitoring can detect attacks that bypass component controls

---

## 8. Appendices

### Appendix A: Acronyms and Abbreviations

| Acronym | Definition                                |
| ------- | ----------------------------------------- |
| ACL     | Access Control List                       |
| APT     | Advanced Persistent Threat                |
| BPCS    | Basic Process Control System              |
| CMMI    | Capability Maturity Model Integration     |
| CRS     | Cybersecurity Requirements Specification  |
| DCS     | Distributed Control System                |
| DMZ     | Demilitarized Zone                        |
| EDR     | Endpoint Detection and Response           |
| ERP     | Enterprise Resource Planning              |
| ESD     | Emergency Shutdown                        |
| FR      | Foundational Requirement                  |
| HMI     | Human Machine Interface                   |
| HSE     | Health, Safety, and Environment           |
| IACS    | Industrial Automation and Control System  |
| IAC     | Identification and Authentication Control |
| ICS     | Industrial Control System                 |
| IDS     | Intrusion Detection System                |
| IEC     | International Electrotechnical Commission |
| IED     | Intelligent Electronic Device             |
| IPS     | Intrusion Prevention System               |
| ISA     | International Society of Automation       |
| ISCI    | ISA Security Compliance Institute         |
| IT      | Information Technology                    |
| MFA     | Multi-Factor Authentication               |
| OT      | Operational Technology                    |
| PAM     | Privileged Access Management              |
| PLC     | Programmable Logic Controller             |
| PKI     | Public Key Infrastructure                 |
| RA      | Resource Availability                     |
| RBAC    | Role-Based Access Control                 |
| RDF     | Restricted Data Flow                      |
| RE      | Requirement Enhancement                   |
| RTU     | Remote Terminal Unit                      |
| SCADA   | Supervisory Control and Data Acquisition  |
| SIEM    | Security Information and Event Management |
| SIL     | Safety Integrity Level                    |
| SIS     | Safety Instrumented System                |
| SL      | Security Level                            |
| SL-A    | Achieved Security Level                   |
| SL-C    | Capability Security Level                 |
| SL-T    | Target Security Level                     |
| SR      | Security Requirement                      |
| SuC     | System under Consideration                |
| TRE     | Timely Response to Events                 |
| UC      | Use Control                               |
| VPN     | Virtual Private Network                   |

### Appendix B: Reference Standards

| Standard                     | Title                                                                                     | Relevance                           |
| ---------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------- |
| **IEC 62443-1-1**      | Terminology, concepts and models                                                          | Foundational concepts               |
| **IEC 62443-2-1**      | Establishing an IACS security program                                                     | Asset owner requirements            |
| **IEC 62443-2-4**      | Security program requirements for IACS service providers                                  | Service provider requirements       |
| **IEC 62443-3-2**      | Security risk assessment for system design                                                | Risk assessment methodology         |
| **IEC 62443-3-3**      | System security requirements and security levels                                          | THIS DOCUMENT - System requirements |
| **IEC 62443-4-1**      | Product security development lifecycle requirements                                       | Secure development                  |
| **IEC 62443-4-2**      | Technical security requirements for IACS components                                       | Component requirements              |
| IEC 61508                    | Functional safety of electrical/electronic/programmable electronic safety-related systems | Safety systems                      |
| IEC 61511                    | Functional safety - Safety instrumented systems for the process industry sector           | Process safety                      |
| ISO/IEC 27001                | Information security management systems                                                   | IT security framework               |
| NIST SP 800-82               | Guide to Industrial Control Systems (ICS) Security                                        | US guidance                         |
| NIST Cybersecurity Framework | Framework for Improving Critical Infrastructure Cybersecurity                             | Risk management                     |

### Appendix C: Additional Resources

#### Certification Programs

- **ISASecure**: Product certification program for IEC 62443-4-2 and 4-1

  - Website: https://www.isasecure.org
  - Certifies components (EDSA), systems (SDLA), and development processes (SSA)
- **IECEE**: International certification system

  - Coordinates with ISASecure for global recognition

#### Training and Certificates

- **ISA/IEC 62443 Cybersecurity Certificate Programs**:

  - Cybersecurity Fundamentals Specialist
  - Cybersecurity Risk Assessment Specialist
  - Cybersecurity Design Specialist
  - Cybersecurity Maintenance Specialist
  - Cybersecurity Expert (all four specialists)
- **ISA Training Courses**:

  - IC32: Cybersecurity Risk Analysis
  - IC33: Cybersecurity Technologies
  - IC34: Cybersecurity Operations and Management
  - IC37: OT Cybersecurity

#### Information Sharing

- **ISA Global Cybersecurity Alliance (ISAGCA)**

  - Industry collaboration forum
  - Guidance documents and webinars
  - Website: https://gca.isa.org
- **Industry ISACs (Information Sharing and Analysis Centers)**

  - Sector-specific threat intelligence
  - Examples: E-ISAC (electricity), WaterISAC, ONG-ISAC (oil & gas)

#### Professional Organizations

- **ISA**: International Society of Automation
- **IEC TC65/WG10**: Standards development committee
- **NIST**: National Institute of Standards and Technology
- **CISA**: Cybersecurity and Infrastructure Security Agency

---
