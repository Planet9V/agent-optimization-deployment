# IEC 62443 Technical Requirements Reference
**Project:** Cyber-62443-Assure
**Purpose:** Complete Technical Lookup for Semantic Search

---

## 1. Security Level Definitions

### 1.1 Security Level Types (SL-T, SL-C, SL-A)

| Type | Name | Definition | When Determined |
|:---|:---|:---|:---|
| **SL-T** | Target Security Level | The desired/required level of security for a zone or conduit, determined by risk assessment | During IEC 62443-3-2 risk assessment |
| **SL-C** | Capability Security Level | The native security functionalities built into a system/component | During product design (IEC 62443-3-3, 4-2) |
| **SL-A** | Achieved Security Level | The actual security level attained after implementation and testing | After system deployment and verification |

### 1.2 Numerical Security Levels (SL-0 to SL-4)

| Level | Name | Threat Profile | Attacker Characteristics |
|:---|:---|:---|:---|
| **SL-0** | No Protection | No specific security requirements | N/A |
| **SL-1** | Casual/Coincidental | Unintentional misuse, human error | Low motivation, generic skills, no IACS knowledge |
| **SL-2** | Intentional (Simple) | Simple attack, script kiddies | Low resources, basic tools, general IT skills |
| **SL-3** | Intentional (Sophisticated) | Targeted attack, moderate APT | Moderate resources, IACS-specific knowledge, automation expertise |
| **SL-4** | State-Level | Nation-state, advanced APT | Extensive resources, deep IACS expertise, high motivation |

---

## 2. Foundational Requirements (FR1-FR7)

| FR | Code | Name | Purpose |
|:---|:---|:---|:---|
| 1 | **IAC** | Identification and Authentication Control | Ensure all users, processes, and devices are uniquely identified and authenticated |
| 2 | **UC** | Use Control | Enforce authorization and least-privilege access |
| 3 | **SI** | System Integrity | Protect against unauthorized modification of software/data |
| 4 | **DC** | Data Confidentiality | Protect sensitive information from unauthorized disclosure |
| 5 | **RDF** | Restricted Data Flow | Control and segment data flow between zones |
| 6 | **TRE** | Timely Response to Events | Enable timely detection and response to security events |
| 7 | **RA** | Resource Availability | Ensure resources remain available (DoS protection) |

---

## 3. System Requirements (SR) by Foundational Requirement

### FR1: Identification and Authentication Control (IAC)

| SR | Requirement | Description | SL1 | SL2 | SL3 | SL4 |
|:---|:---|:---|:---|:---|:---|:---|
| **SR 1.1** | Human User Identification and Authentication | Control system must identify and authenticate all human users | ✓ | ✓ | ✓ | ✓ |
| **SR 1.2** | Software Process and Device Identification | Identify and authenticate all software processes and devices | - | ✓ | ✓ | ✓ |
| **SR 1.3** | Account Management | Capability to add, modify, disable, remove accounts | ✓ | ✓ | ✓ | ✓ |
| **SR 1.4** | Identifier Management | Unique identifiers for all users and processes | ✓ | ✓ | ✓ | ✓ |
| **SR 1.5** | Authenticator Management | Secure management of passwords, tokens, certificates | ✓ | ✓ | ✓ | ✓ |
| **SR 1.6** | Wireless Access Management | Control and monitor wireless access points | - | ✓ | ✓ | ✓ |
| **SR 1.7** | Strength of Password-Based Authentication | Password complexity, length, rotation requirements | ✓ | ✓ | ✓ | ✓ |
| **SR 1.8** | Public Key Infrastructure Certificates | PKI certificate management and validation | - | - | ✓ | ✓ |
| **SR 1.9** | Strength of Public Key Authentication | Key length, algorithm requirements | - | - | ✓ | ✓ |
| **SR 1.10** | Authenticator Feedback | Obscure authentication feedback (no plaintext) | ✓ | ✓ | ✓ | ✓ |
| **SR 1.11** | Unsuccessful Login Attempts | Lock accounts after failed attempts | ✓ | ✓ | ✓ | ✓ |
| **SR 1.12** | System Use Notification | Display legal warning before login | - | ✓ | ✓ | ✓ |
| **SR 1.13** | Access via Untrusted Networks | Control access from external networks | - | ✓ | ✓ | ✓ |

### FR2: Use Control (UC)

| SR | Requirement | Description | SL1 | SL2 | SL3 | SL4 |
|:---|:---|:---|:---|:---|:---|:---|
| **SR 2.1** | Authorization Enforcement | Enforce least-privilege access for all users | ✓ | ✓ | ✓ | ✓ |
| **SR 2.2** | Wireless Use Control | Monitor and restrict wireless access | - | ✓ | ✓ | ✓ |
| **SR 2.3** | Use Control for Portable/Mobile Devices | Control USB, laptops, mobile devices | - | ✓ | ✓ | ✓ |
| **SR 2.4** | Mobile Code | Control execution of mobile code | - | ✓ | ✓ | ✓ |
| **SR 2.5** | Session Lock | Auto-lock inactive sessions | ✓ | ✓ | ✓ | ✓ |
| **SR 2.6** | Remote Session Termination | Terminate remote sessions | - | ✓ | ✓ | ✓ |
| **SR 2.7** | Concurrent Session Control | Limit concurrent sessions per user | - | - | ✓ | ✓ |
| **SR 2.8** | Auditable Events | Define and log security-relevant events | ✓ | ✓ | ✓ | ✓ |
| **SR 2.9** | Audit Storage Capacity | Ensure sufficient audit log storage | ✓ | ✓ | ✓ | ✓ |
| **SR 2.10** | Response to Audit Processing Failures | Handle audit failures gracefully | - | ✓ | ✓ | ✓ |
| **SR 2.11** | Timestamps | Accurate timestamps for audit records | ✓ | ✓ | ✓ | ✓ |
| **SR 2.12** | Non-Repudiation | Prevent denial of actions | - | - | ✓ | ✓ |

### FR3: System Integrity (SI)

| SR | Requirement | Description | SL1 | SL2 | SL3 | SL4 |
|:---|:---|:---|:---|:---|:---|:---|
| **SR 3.1** | Communication Integrity | Protect transmitted data integrity | ✓ | ✓ | ✓ | ✓ |
| **SR 3.2** | Malicious Code Protection | Anti-malware protection | ✓ | ✓ | ✓ | ✓ |
| **SR 3.3** | Security Functionality Verification | Verify security functions during maintenance | - | ✓ | ✓ | ✓ |
| **SR 3.4** | Software and Information Integrity | Detect unauthorized changes | - | ✓ | ✓ | ✓ |
| **SR 3.5** | Input Validation | Validate all inputs | ✓ | ✓ | ✓ | ✓ |
| **SR 3.6** | Deterministic Output | Predictable, safe outputs | - | ✓ | ✓ | ✓ |
| **SR 3.7** | Error Handling | Secure error handling | ✓ | ✓ | ✓ | ✓ |
| **SR 3.8** | Session Integrity | Protect session state | - | ✓ | ✓ | ✓ |
| **SR 3.9** | Protection of Audit Information | Protect audit logs from tampering | ✓ | ✓ | ✓ | ✓ |

### FR4: Data Confidentiality (DC)

| SR | Requirement | Description | SL1 | SL2 | SL3 | SL4 |
|:---|:---|:---|:---|:---|:---|:---|
| **SR 4.1** | Information Confidentiality | Protect data at rest and in transit | - | ✓ | ✓ | ✓ |
| **SR 4.2** | Information Persistence | Secure data disposal | - | ✓ | ✓ | ✓ |
| **SR 4.3** | Use of Cryptography | Employ approved cryptographic algorithms | - | ✓ | ✓ | ✓ |

### FR5: Restricted Data Flow (RDF)

| SR | Requirement | Description | SL1 | SL2 | SL3 | SL4 |
|:---|:---|:---|:---|:---|:---|:---|
| **SR 5.1** | Network Segmentation | Segment control system from IT network | ✓ | ✓ | ✓ | ✓ |
| **SR 5.2** | Zone Boundary Protection | Firewall/gateway at zone boundaries | - | ✓ | ✓ | ✓ |
| **SR 5.3** | General Purpose Person-to-Person Communication Restrictions | Restrict unnecessary traffic | - | ✓ | ✓ | ✓ |
| **SR 5.4** | Application Partitioning | Separate application functions | - | - | ✓ | ✓ |

### FR6: Timely Response to Events (TRE)

| SR | Requirement | Description | SL1 | SL2 | SL3 | SL4 |
|:---|:---|:---|:---|:---|:---|:---|
| **SR 6.1** | Audit Log Accessibility | Audit logs readable by authorized personnel | ✓ | ✓ | ✓ | ✓ |
| **SR 6.2** | Continuous Monitoring | Monitor security-relevant events | - | ✓ | ✓ | ✓ |

### FR7: Resource Availability (RA)

| SR | Requirement | Description | SL1 | SL2 | SL3 | SL4 |
|:---|:---|:---|:---|:---|:---|:---|
| **SR 7.1** | Denial of Service Protection | Maintain degraded mode during DoS | ✓ | ✓ | ✓ | ✓ |
| **SR 7.2** | Resource Management | Prevent resource exhaustion | ✓ | ✓ | ✓ | ✓ |
| **SR 7.3** | Control System Backup | Up-to-date backups available | ✓ | ✓ | ✓ | ✓ |
| **SR 7.4** | Control System Recovery and Reconstitution | Quick recovery to secure state | ✓ | ✓ | ✓ | ✓ |
| **SR 7.5** | Emergency Power | Graceful shutdown on power loss | - | ✓ | ✓ | ✓ |
| **SR 7.6** | Network and Security Configuration Settings | Secure configuration baselines | ✓ | ✓ | ✓ | ✓ |
| **SR 7.7** | Least Functionality | Disable unnecessary services | ✓ | ✓ | ✓ | ✓ |
| **SR 7.8** | Control System Component Inventory | Maintain asset inventory | ✓ | ✓ | ✓ | ✓ |

---

## 4. Component Requirements (CR) - IEC 62443-4-2

### Component Types

| Type | Code | Examples |
|:---|:---|:---|
| Software Application | SA | SCADA HMI, Historian, MES |
| Embedded Device | ED | PLC, RTU, Safety Controller |
| Host Device | HD | Workstation, Server, Engineering Station |
| Network Device | ND | Switch, Router, Firewall, Data Diode |

### CR Mapping to SR (Examples)

| CR | FR | Requirement | Component Types |
|:---|:---|:---|:---|
| **CR 1.1** | IAC | Human User Identification and Authentication | SA, HD |
| **CR 1.2** | IAC | Software Process and Device Identification | ED, ND |
| **CR 1.5** | IAC | Authenticator Management | All |
| **CR 1.7** | IAC | Strength of Password-Based Authentication | All |
| **CR 2.1** | UC | Authorization Enforcement | All |
| **CR 3.2** | SI | Malicious Code Protection | SA, HD |
| **CR 3.4** | SI | Software and Firmware Integrity | ED, ND |
| **CR 3.5** | SI | Input Validation | All |
| **CR 4.1** | DC | Information Confidentiality | All |
| **CR 5.1** | RDF | Network Segmentation | ND |
| **CR 6.1** | TRE | Audit Log Accessibility | All |
| **CR 7.1** | RA | DoS Protection | All |

---

## 5. Zone and Conduit Nomenclature

### Zone Types

| Zone Type | Description | Typical SL-T |
|:---|:---|:---|
| **Enterprise Zone** | Corporate IT, ERP, External connections | SL-1 to SL-2 |
| **DMZ Zone** | Data exchange, Historians, Jump servers | SL-2 |
| **Operations Zone** | SCADA, HMI, Control Center | SL-2 to SL-3 |
| **Control Zone** | PLCs, RTUs, Controllers | SL-3 |
| **Safety Zone** | SIS, Safety PLCs, Emergency systems | SL-3 to SL-4 |
| **Field Zone** | Sensors, Actuators, I/O | SL-1 (physical protection) |

### Conduit Security Requirements

| Conduit Type | Protocol | Encryption Required? | SL-T |
|:---|:---|:---|:---|
| IT-to-DMZ | HTTPS, SSH | Yes | SL-2 |
| DMZ-to-OT | OPC UA, MQTT | Yes | SL-3 |
| SCADA-to-PLC | Modbus TCP (legacy) | No (Gap - requires mitigation) | SL-3 |
| SCADA-to-PLC | OPC UA Secure | Yes | SL-3 |
| PLC-to-Safety | Proprietary (Honeywell LEAP) | Yes | SL-4 |
| External VPN | IPSec, OpenVPN | Yes | SL-3 |

---

## 6. IEC 62443 Standard Parts Reference

| Part | Title | Focus |
|:---|:---|:---|
| **62443-1-1** | Terminology, concepts, models | Definitions and framework |
| **62443-1-2** | Master Glossary | Terms and abbreviations |
| **62443-2-1** | Security program requirements for asset owners | Policies and procedures |
| **62443-2-4** | Security program requirements for service providers | Integration and maintenance |
| **62443-3-2** | Security risk assessment for system design | Zone/conduit partitioning, risk methodology |
| **62443-3-3** | System security requirements and security levels | SR definitions by SL |
| **62443-4-1** | Product development requirements | Secure development lifecycle |
| **62443-4-2** | Component security requirements | CR definitions by SL |

---

## 7. Glossary of Key Terms

| Term | Abbreviation | Definition |
|:---|:---|:---|
| Asset Owner | AO | Entity responsible for the IACS |
| Attack Vector | - | Path or means by which an attacker gains access |
| Conduit | - | Logical grouping of communication channels between zones |
| Consequence | - | Impact of a successful attack |
| Defense in Depth | DiD | Multiple layers of security controls |
| Foundational Requirement | FR | Core security requirement category |
| Gap Analysis | - | Comparison of SL-C vs SL-T |
| Hardening | - | Reducing attack surface by disabling unused features |
| Industrial Automation and Control System | IACS | The system under consideration |
| Maturity Level | ML | Organization's cybersecurity management capability |
| Operational Technology | OT | Hardware/software controlling physical processes |
| Purdue Model | - | Reference architecture for industrial networks |
| Residual Risk | - | Risk remaining after controls are applied |
| Requirement Enhancement | RE | Additional requirement for higher SLs |
| Safety Integrity Level | SIL | Functional safety measure (EN 61508/62061) |
| Security Level | SL | Measure of security robustness (SL-0 to SL-4) |
| System Requirement | SR | Specific requirement for systems (62443-3-3) |
| Component Requirement | CR | Specific requirement for components (62443-4-2) |
| System Under Consideration | SUC | Scope of the risk assessment |
| Threat | - | Potential cause of an unwanted incident |
| Vulnerability | - | Weakness that can be exploited |
| Zone | - | Logical/physical grouping of assets with similar security |
| Zone and Conduit Requirements | ZCR | Output of 62443-3-2 |

---

## 8. CRL-Specific Mapping (TVS Example)

| Asset | Zone | SL-T | Key FR | Key SR |
|:---|:---|:---|:---|:---|
| SICE SIDERA SCADA | Operations (Zone 3) | SL-3 | IAC, UC, SI | SR 1.1, SR 2.1, SR 3.2 |
| Honeywell Safety Manager SC | Safety (Zone 3) | SL-4 | IAC, SI, RA | SR 1.2, SR 3.4, SR 7.1 |
| Variable Speed Drives (VSD) | Control (Zone 2) | SL-2 | UC, RA | SR 2.1, SR 7.2 |
| Tunnel Ventilation Controller | Safety (Zone 3) | SL-3 | SI, TRE, RA | SR 3.5, SR 6.2, SR 7.4 |
| Station BMS | Operations (Zone 2) | SL-2 | IAC, UC | SR 1.1, SR 2.1 |
| Fire Detection Panel | Safety (Zone 3) | SL-3 | SI, TRE | SR 3.1, SR 6.2 |
