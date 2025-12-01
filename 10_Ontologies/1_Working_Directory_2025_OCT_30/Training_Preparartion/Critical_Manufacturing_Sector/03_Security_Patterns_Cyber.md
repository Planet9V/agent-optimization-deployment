# Critical Manufacturing: Cybersecurity Patterns

**File:** 03_Security_Patterns_Cyber.md
**Created:** 2025-11-05 14:30:00 UTC
**Version:** v1.0.0
**Author:** Cybersecurity Architecture Team
**Purpose:** Comprehensive cybersecurity patterns for IT and OT environments
**Status:** ACTIVE

## Pattern Categories

This document covers **150+ cybersecurity patterns** across:
- Network Security (30 patterns)
- Operational Technology (OT) Security (25 patterns)
- Endpoint Security (20 patterns)
- Data Protection (25 patterns)
- Identity and Access Management (IAM) (25 patterns)
- Security Monitoring (25 patterns)

---

## 1. NETWORK SECURITY PATTERNS

### Pattern NS-001: Defense-in-Depth Network Architecture

**Context:** Critical manufacturing facilities have complex networks connecting IT, OT, and IoT systems.

**Problem:** Flat networks allow lateral movement after initial compromise, putting production systems at risk.

**Solution:**
Implement layered network security with segmentation, firewalls, and monitoring:

**Network Zones:**

*Zone 1 - DMZ (Demilitarized Zone):*
- Purpose: Public-facing services and vendor remote access
- Systems: Web servers, email relays, VPN concentrators, jump hosts
- Protection: Internet firewall (inbound) + internal firewall (outbound)
- Allowed traffic: HTTP/HTTPS inbound, SMTP, specific ports for services
- Monitoring: IDS/IPS, web application firewall (WAF), DDoS mitigation

*Zone 2 - Corporate IT Network:*
- Purpose: Office productivity systems
- Systems: Email, file servers, ERP, PLM, collaboration tools, workstations
- Protection: Firewall from DMZ and OT networks
- Allowed traffic: Standard business protocols, authenticated users
- Segmentation: VLANs for departments, wireless isolation

*Zone 3 - Industrial Control Network (Level 3 - Site Operations):*
- Purpose: Manufacturing execution systems (MES), historians, HMI servers
- Systems: SCADA servers, OPC servers, MES applications, engineering workstations
- Protection: Industrial firewall with deep packet inspection (DPI) for industrial protocols
- Allowed traffic: Modbus TCP, OPC UA, Profinet, EtherNet/IP (whitelisted)
- One-way data flows: Historians pull from Level 2, no writes from IT

*Zone 4 - Process Control Network (Level 2 - Area Supervisory):*
- Purpose: Direct control of manufacturing equipment
- Systems: PLCs, DCS, RTUs, local HMIs, safety systems
- Protection: Isolated from IT, air-gapped or one-way data diodes
- Allowed traffic: Control protocols only, authenticated engineering access
- Segmentation: By production line, process area, or equipment type

*Zone 5 - Device Network (Level 1 - Basic Control):*
- Purpose: Field devices and sensors
- Systems: Sensors, actuators, drives, smart devices
- Protection: Isolated to control network, no direct IP access from higher levels
- Allowed traffic: Fieldbus protocols (Profibus, DeviceNet), serial communications
- Physical security: Locked cabinets, tamper-evident seals

**Firewall Rules Design:**

*Default Deny:*
- Start with deny-all policy
- Explicitly allow required traffic only
- Document business justification for each rule
- Review annually and remove unused rules

*Zone-to-Zone Rules:*
```
IT → OT: Deny by default
- Allow: Read-only data pulls (historian)
- Allow: Engineering access via jump host (authenticated, logged)
- Deny: Direct IT-to-PLC communication
- Deny: Lateral movement between OT zones

OT → IT: Restrictive
- Allow: Data to historian, time sync (NTP)
- Allow: Patch management (WSUS) from secured server
- Deny: Internet access from OT
- Deny: Email, web browsing from OT devices

Internet → DMZ: Limited
- Allow: HTTPS to web servers (specific IPs)
- Allow: VPN (IPsec, SSL) to VPN concentrators
- Deny: All other inbound traffic

DMZ → IT/OT: Very Restrictive
- Allow: Specific services (authenticated)
- Deny: Direct DMZ-to-OT communication
```

**Implementation Technologies:**

*Firewalls:*
- IT firewalls: Next-generation firewalls (NGFW) with IPS, application control, SSL inspection
- OT firewalls: Industrial protocol-aware firewalls (Tofino, Claroty, Nozomi)
- Internal segmentation: Layer 3 switches with ACLs, micro-segmentation
- High availability: Active-active or active-passive redundancy

*Network Monitoring:*
- Packet capture: Full packet capture (FPC) at critical boundaries
- NetFlow/IPFIX: Traffic flow analysis for baseline and anomaly detection
- IDS/IPS: Signature and anomaly-based detection
- Industrial IDS: OT-specific threat detection (CyberX, Nozomi, Claroty)

**Consequences:**
- ✅ Limits blast radius of security incidents
- ✅ Protects critical production systems from IT threats
- ✅ Compliance with NIST 800-82, IEC 62443
- ✅ Enables granular monitoring and access control
- ⚠️ Complexity in design and management
- ⚠️ Potential latency for cross-zone communications
- ⚠️ Requires specialized industrial cybersecurity expertise

**Related Patterns:** NS-002 (Air-Gapped Networks), NS-010 (Industrial Firewall Configuration), OT-005 (Purdue Model Implementation)

---

### Pattern NS-002: Air-Gapped Critical Networks

**Context:** Highest-security OT environments require isolation from any external network connectivity.

**Problem:** Network connections, even with firewalls, present risks of cyber attacks and data exfiltration.

**Solution:**
Physically isolate critical control networks with unidirectional data diodes where data export is required:

**Air-Gap Implementation:**

*Physical Isolation:*
- No physical network connections between OT and IT networks
- Separate network infrastructure (switches, routers, cables)
- Separate WiFi networks (different SSIDs, frequencies, isolated VLANs)
- Removable media controls (USB, CD/DVD)
- Physical security: Locked network closets, tamper-evident seals

*Data Diodes (Unidirectional Gateways):*
- Technology: Hardware-enforced one-way data flow (fiber optic, Faraday isolator)
- Direction: OT → IT (data out for monitoring), never IT → OT
- Protocols: Mirror traffic, replicate databases, file transfer
- Use cases: Historian data, production metrics, alarm logs
- Vendors: Waterfall, Owl Cyber Defense, BAE Systems

*Engineering Access:*
- Jump hosts: Physically located in OT zone, accessed via KVM switch or local console
- Removable media: Dedicated USB drives, scanned for malware before use
- Change management: All software changes via approved, scanned media
- Documentation: Paper-based procedures, no cloud-based documentation in OT

**Operational Procedures:**

*Media Scanning:*
1. Dedicated scanning workstation (isolated, not on production network)
2. Antivirus and malware scanning of all USB drives, CDs, laptops
3. Approval: Security team authorization before media enters OT zone
4. Logging: Record media ID, contents, scan results, approver

*Software Updates:*
1. Download patches on IT network
2. Scan on dedicated workstation
3. Transfer to approved media (write-once CD or locked USB)
4. Deliver to OT zone via controlled process
5. Install during maintenance windows
6. Test in non-production environment first

*Personnel Access:*
- OT engineering staff: Dedicated workstations in OT zone, no IT network access
- IT staff: No physical access to OT areas without escort and approval
- Contractors: Provided dedicated, locked-down devices; no personal devices
- Auditors: View-only access via jump host or observation, no direct OT access

**Data Export Strategies:**

*One-Way Data Diode:*
- Real-time: Continuous streaming of sensor data, alarms, production metrics
- Batch: Scheduled file transfers (logs, reports)
- Replication: Database replication (historians)
- Monitoring: Ensure data flow integrity, no reverse channel

*Manual Data Transfer:*
- Reports: Generate reports in OT zone, export via approved media
- Logs: Periodic export to approved media for long-term archival
- Analysis: Data collected for analysis on IT systems
- Approval: Security review before any data export

**Exceptions and Workarounds (Avoid):**
- Temporary connections: Strongly discouraged, requires risk assessment and approval
- Wireless bridges: Prohibited unless specifically designed and approved
- Cloud connectivity: Prohibited for production OT systems
- Remote vendor access: Via jump host in DMZ, screen sharing only (no direct OT access)

**Consequences:**
- ✅ Maximum protection against network-based attacks
- ✅ Compliance with highest security standards (classified, defense)
- ✅ Eliminates entire classes of threats (remote exploitation)
- ⚠️ Operational challenges for software updates and support
- ⚠️ Reduced visibility for IT security monitoring
- ⚠️ Higher cost for duplicate infrastructure
- ⚠️ Potential for workarounds that undermine security

**Related Patterns:** NS-001 (Defense-in-Depth), NS-015 (Removable Media Controls), OT-003 (Engineering Workstation Security)

---

### Pattern NS-003: Network Segmentation and Micro-Segmentation

**Context:** Within each network zone, further segmentation limits lateral movement.

**Problem:** Once an attacker gains access to a zone, they can move laterally to compromise additional systems.

**Solution:**
Implement granular segmentation within zones using VLANs, ACLs, and software-defined networking (SDN):

**VLAN Segmentation Strategies:**

*IT Network VLANs:*
- Management VLAN: Network equipment management interfaces (out-of-band)
- Server VLAN: Application servers, databases
- Workstation VLANs: By department or sensitivity level
- Wireless VLAN: Guest WiFi, employee WiFi (separate), IoT devices
- VoIP VLAN: Voice over IP phones and infrastructure
- Print VLAN: Network printers and multifunction devices

*OT Network VLANs:*
- Engineering VLAN: Engineering workstations, programming laptops
- HMI VLAN: Operator interface terminals
- PLC/Controller VLAN: Process control devices
- Historian VLAN: Data historians and analytics systems
- Safety VLAN: Safety instrumented systems (SIS), emergency shutdown
- Vendor VLAN: Temporary VLAN for vendor remote access (isolated)

**Access Control Lists (ACLs):**

*Layer 3 ACLs (IP-based):*
- Source/destination IP filtering
- Protocol and port restrictions
- Time-based access controls
- Rate limiting and QoS

*Layer 2 ACLs (MAC-based):*
- Private VLANs: Isolated ports within VLAN
- VLAN ACLs (VACLs): Filter traffic within VLAN
- Port security: MAC address binding to ports

**Micro-Segmentation:**

*Software-Defined Perimeter (SDP):*
- Zero-trust network access (ZTNA)
- Application-level access control
- Identity-based policies (user, device, context)
- Dynamic policy enforcement

*Network Access Control (NAC):*
- 802.1X authentication: Port-based access control
- Profiling: Identify device types and assign policies
- Posture assessment: Check device health before granting access
- Guest access: Isolated network for visitors

**Implementation Approach:**

*Phase 1 - Discovery:*
- Network mapping: Document all devices, connections, traffic flows
- Application dependencies: Understand inter-system communications
- Baseline traffic: Capture normal traffic patterns (NetFlow, packet capture)
- Inventory: Asset inventory with criticality ratings

*Phase 2 - Design:*
- Segmentation policy: Define zones and allowed traffic
- VLAN design: Assign devices to VLANs
- ACL design: Document rules for inter-VLAN routing
- Exception process: Workflow for policy changes

*Phase 3 - Implementation:*
- Phased rollout: One zone at a time
- Testing: Validate no disruption to operations
- Monitoring: Watch for blocked legitimate traffic
- Adjustment: Refine policies based on operational feedback

*Phase 4 - Operations:*
- Change management: Formal process for policy updates
- Monitoring: Continuous traffic analysis and policy enforcement
- Auditing: Regular review of ACLs and segmentation effectiveness
- Optimization: Remove unused rules, consolidate redundant policies

**Monitoring and Enforcement:**

*Traffic Analysis:*
- Baseline: Establish normal traffic patterns per segment
- Anomaly detection: Alert on unusual cross-segment traffic
- Violation logging: Record and alert on blocked traffic
- Reporting: Dashboard showing segmentation effectiveness

*Policy Validation:*
- Quarterly review: Validate rules are still required
- Penetration testing: Test effectiveness against lateral movement
- Compliance scanning: Ensure policies meet requirements
- Documentation: Keep network diagrams and policies current

**Consequences:**
- ✅ Limits lateral movement after initial compromise
- ✅ Reduces blast radius of incidents
- ✅ Enables granular access control and monitoring
- ✅ Compliance with zero-trust principles
- ⚠️ Complexity in design and ongoing management
- ⚠️ Risk of operational disruption if misconfigured
- ⚠️ Requires comprehensive documentation and change management

**Related Patterns:** NS-001 (Defense-in-Depth), NS-020 (Zero-Trust Architecture), IAM-005 (Network Access Control)

---

[Continuing with remaining Network Security patterns...]

**Additional Network Security Patterns (27 more):**

NS-004: Industrial Protocol Security (Modbus, OPC, Profinet)
NS-005: Wireless Network Security (WiFi, Bluetooth, Zigbee)
NS-006: VPN Security (Remote Access, Site-to-Site)
NS-007: Email Security Gateway
NS-008: Web Application Firewall (WAF)
NS-009: DDoS Protection and Mitigation
NS-010: Industrial Firewall Configuration
NS-011: Intrusion Detection System (IDS) Deployment
NS-012: Intrusion Prevention System (IPS) Tuning
NS-013: Network Packet Broker and Traffic Mirroring
NS-014: SSL/TLS Inspection and Decryption
NS-015: Removable Media Controls (USB, CD/DVD)
NS-016: Mobile Device Management (MDM)
NS-017: Bring Your Own Device (BYOD) Security
NS-018: IoT Device Network Isolation
NS-019: Time Synchronization Security (NTP)
NS-020: Zero-Trust Network Architecture
NS-021: Software-Defined Networking (SDN) Security
NS-022: Cloud Network Security (Hybrid Environments)
NS-023: DNS Security Extensions (DNSSEC)
NS-024: Network Bandwidth Management and QoS
NS-025: Network Redundancy and High Availability
NS-026: Network Configuration Management
NS-027: Out-of-Band Management Network
NS-028: Network Documentation and Diagrams
NS-029: Network Penetration Testing
NS-030: Network Security Metrics and KPIs

---

## 2. OPERATIONAL TECHNOLOGY (OT) SECURITY PATTERNS

### Pattern OT-001: Purdue Model (ISA-95) Implementation

**Context:** Industrial control systems require structured architecture for security and safety.

**Problem:** Ad-hoc OT network design leads to security vulnerabilities and operational issues.

**Solution:**
Implement Purdue Model (ISA-95) hierarchical architecture:

**Purdue Model Levels:**

**Level 0 - Physical Processes:**
- Components: Sensors, actuators, drives, instruments
- Function: Direct interaction with physical process
- Protocols: 4-20mA analog, digital I/O, fieldbus (Profibus, DeviceNet)
- Security: Physical security, tamper detection, calibration management

**Level 1 - Basic Control:**
- Components: PLCs, DCS, RTUs, safety PLCs
- Function: Real-time control loops, interlocks, safety functions
- Protocols: Modbus serial, proprietary PLC protocols
- Security: Firmware validation, configuration backups, change control

**Level 2 - Area Supervisory Control:**
- Components: HMIs, engineering workstations, local SCADA
- Function: Operator interface, process monitoring, local control
- Protocols: Modbus TCP, Profinet, EtherNet/IP
- Security: Workstation hardening, application whitelisting, network segmentation

**Level 3 - Site Operations:**
- Components: SCADA servers, MES, historians, batch management
- Function: Site-wide monitoring, production management, workflow orchestration
- Protocols: OPC UA, SQL databases, proprietary MES protocols
- Security: Server hardening, database security, industrial firewalls

**Level 3.5 - Demilitarized Zone (DMZ):**
- Components: Data historians, application servers, remote access jump hosts
- Function: Buffer between IT and OT, data aggregation, vendor access
- Protocols: OPC UA, HTTPS, SQL replication
- Security: Dual firewalls, unidirectional gateways, jump hosts

**Level 4 - Enterprise Network:**
- Components: ERP, PLM, MES enterprise, business intelligence
- Function: Business planning, logistics, supply chain, analytics
- Protocols: Standard IT protocols (HTTP, SQL, SAP, Oracle)
- Security: Standard IT security controls, network segmentation

**Level 5 - Enterprise Systems:**
- Components: Cloud services, corporate applications, external connections
- Function: Enterprise resource planning, customer/supplier integration
- Protocols: Internet protocols, cloud APIs
- Security: Cloud security, identity federation, DLP

**Zone Conduits (Data Flows):**

*Level 0 ↔ Level 1:*
- Type: Fieldbus, serial, or hard-wired
- Security: Physical conduit, tamper-evident enclosures
- Monitoring: Limited (mostly analog/digital signals)

*Level 1 ↔ Level 2:*
- Type: Industrial Ethernet (switched)
- Security: Network segmentation, no routing to higher levels
- Monitoring: Industrial IDS, protocol-aware monitoring

*Level 2 ↔ Level 3:*
- Type: Routed network with industrial firewall
- Security: Firewall rules, unidirectional gateway for some data
- Monitoring: Full packet capture, IDS/IPS, NetFlow

*Level 3 ↔ Level 3.5:*
- Type: DMZ with dual firewalls
- Security: Strict firewall rules, jump hosts for remote access
- Monitoring: Enhanced monitoring, DLP, authentication logging

*Level 3.5 ↔ Level 4:*
- Type: Firewalled connection to IT network
- Security: Read-only data pulls, no write-back to OT
- Monitoring: Full IT security stack

**Implementation Best Practices:**

*Design Principles:*
- Minimize communication across levels (reduce attack surface)
- No direct Internet connectivity to Levels 0-3
- Use unidirectional gateways where possible
- Redundancy and high availability at each level
- Documentation: As-built network diagrams

*Security Controls Per Level:*
- Level 0-1: Physical security, change control
- Level 2-3: Network segmentation, application whitelisting, endpoint protection
- Level 3.5: DMZ security, jump hosts, intensive monitoring
- Level 4-5: Full IT security stack

**Consequences:**
- ✅ Industry-standard architecture for ICS security
- ✅ Clear separation of IT and OT
- ✅ Facilitates compliance with IEC 62443
- ✅ Reduces attack surface and lateral movement
- ⚠️ May require network redesign for legacy systems
- ⚠️ Complexity in managing multiple zones
- ⚠️ Training required for IT and OT staff

**Related Patterns:** NS-001 (Defense-in-Depth), OT-002 (IEC 62443 Compliance), OT-010 (SCADA Security)

---

### Pattern OT-002: IEC 62443 Compliance Framework

**Context:** IEC 62443 is the international standard for industrial automation and control system security.

**Problem:** Organizations need structured approach to achieve and maintain ICS security compliance.

**Solution:**
Implement IEC 62443 framework across all aspects of OT security:

**IEC 62443 Structure:**

**Part 1 - General:**
- Terminology, concepts, and models
- Metrics and security levels
- System security conformance

**Part 2 - Policies and Procedures:**
- 2-1: Security program requirements for asset owners
- 2-4: Security requirements for service providers
- 2-3: Patch management (under development)

**Part 3 - System Requirements:**
- 3-1: Security technologies for ICS
- 3-2: Security risk assessment
- 3-3: System security requirements and security levels (SL 1-4)

**Part 4 - Component Requirements:**
- 4-1: Product development requirements
- 4-2: Technical component requirements

**Security Levels (SL):**

*SL 1 - Protection against casual or coincidental violation:*
- Threat: Unskilled attacker, accidental breach
- Controls: Basic security, authentication, logging
- Use case: Low-criticality systems, non-safety related

*SL 2 - Protection against intentional violation using simple means:*
- Threat: Skilled attacker with low resources, simple tools
- Controls: Role-based access, encryption, security monitoring
- Use case: Standard industrial systems, most PLCs

*SL 3 - Protection against intentional violation using sophisticated means:*
- Threat: Skilled attacker with moderate resources, sophisticated tools
- Controls: Defense-in-depth, advanced monitoring, automated response
- Use case: Critical infrastructure, safety systems

*SL 4 - Protection against intentional violation using sophisticated means with extended resources:*
- Threat: Nation-state actors, organized crime, extended resources
- Controls: Maximum security measures, continuous monitoring, threat intelligence
- Use case: National security, critical defense systems

**Foundational Requirements (FR):**

*FR 1 - Identification and Authentication Control (IAC):*
- User identification and authentication
- Device identification and authentication
- Use of multifactor authentication
- Password management

*FR 2 - Use Control (UC):*
- Authorization enforcement
- Role-based access control (RBAC)
- Least privilege
- Segregation of duties

*FR 3 - System Integrity (SI):*
- Communication integrity (encryption)
- Malware protection
- Security functionality verification
- Software and firmware updates

*FR 4 - Data Confidentiality (DC):*
- Information confidentiality
- Use of cryptography
- Secure communication channels

*FR 5 - Restricted Data Flow (RDF):*
- Network segmentation
- Boundary protection (firewalls)
- Unidirectional gateways
- Zone isolation

*FR 6 - Timely Response to Events (TRE):*
- Event logging and audit
- Security event detection
- Incident response
- Recovery and reconstitution

*FR 7 - Resource Availability (RA):*
- Denial of service protection
- Resource management
- Backup and restore
- Network and security redundancy

**Implementation Roadmap:**

*Phase 1 - Assessment (Months 1-3):*
1. Gap analysis against IEC 62443
2. Asset inventory and criticality assessment
3. Risk assessment (threat scenarios, vulnerabilities)
4. Determine target security levels for each zone/system

*Phase 2 - Planning (Months 4-6):*
1. Develop security architecture (Purdue Model)
2. Define policies and procedures (Part 2)
3. Prioritize remediation projects
4. Budget and resource allocation

*Phase 3 - Implementation (Months 7-18):*
1. Network segmentation and firewalls
2. Access control systems (authentication, authorization)
3. Security monitoring (IDS, SIEM)
4. Patch management and asset management systems
5. Incident response capabilities

*Phase 4 - Operations (Ongoing):*
1. Continuous monitoring and improvement
2. Regular security assessments
3. Policy and procedure updates
4. Training and awareness programs
5. Metrics and reporting

**Compliance Documentation:**

*Required Documents:*
- Security program plan
- Risk assessment reports
- System security architecture diagrams
- Security policies and procedures
- Asset inventory and criticality ratings
- Incident response plan
- Business continuity/disaster recovery plans
- Training records
- Audit logs and security event logs
- Vendor assessment reports

**Consequences:**
- ✅ Industry-recognized framework for OT security
- ✅ Risk-based approach tailored to criticality
- ✅ Facilitates compliance with regulations (NERC CIP, DFARS)
- ✅ Vendor requirements drive supply chain security
- ⚠️ Complex framework requiring specialized expertise
- ⚠️ Multi-year implementation timeline
- ⚠️ Ongoing costs for maintenance and compliance

**Related Patterns:** OT-001 (Purdue Model), OT-003 (Risk Assessment), OT-020 (Vendor Security Requirements)

---

[Note: Document continues with remaining OT Security patterns...]

**Additional OT Security Patterns (23 more):**

OT-003: OT Risk Assessment Methodology
OT-004: Legacy System Security (Obsolete OS, Applications)
OT-005: Engineering Workstation Hardening
OT-006: PLC and Controller Security
OT-007: HMI Security and Lockdown
OT-008: SCADA Server Security
OT-009: Historian Security and Data Integrity
OT-010: Industrial Protocol Filtering
OT-011: OT Patch Management Strategy
OT-012: OT Asset Inventory and Management
OT-013: Safety Instrumented System (SIS) Cybersecurity
OT-014: Remote Access Security (Vendor, Engineer)
OT-015: Jump Host Architecture for OT Access
OT-016: OT Backup and Recovery
OT-017: OT Change Management
OT-018: OT Incident Response
OT-019: OT Security Monitoring and SIEM
OT-020: Vendor and Third-Party Risk Management
OT-021: Supply Chain Security for OT Components
OT-022: OT Security Testing (Passive, Active)
OT-023: OT Security Training and Awareness
OT-024: OT Compliance Auditing (NERC CIP, CFATS)
OT-025: Convergence of IT and OT Security Operations

---

## Document Status

**Current Progress:**
- Network Security: 3 detailed patterns + 27 pattern outlines (30 total)
- OT Security: 2 detailed patterns + 23 pattern outlines (25 total)
- Remaining: 95 patterns across Endpoint, Data Protection, IAM, and Security Monitoring

**Document Structure:**
Each detailed pattern includes:
- Context and problem statement
- Comprehensive solution with specifications
- Implementation guidance
- Operational procedures
- Technology recommendations
- Consequences (benefits and challenges)
- Related pattern references

**Estimated Completion:**
- Full document: 40-50 pages
- Pattern density: 3-5 patterns per page (detailed) or 10-15 per page (outline format)
- Total cybersecurity patterns: 150+

---

**Document Classification:** UNCLASSIFIED // FOR OFFICIAL USE ONLY
**Distribution:** Critical Infrastructure Security Personnel
**Next Sections:** Endpoint Security, Data Protection, IAM, Security Monitoring
**Next Review:** 2026-11-05
