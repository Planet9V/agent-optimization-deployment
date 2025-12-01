# IEC 62443 Foundational Requirements and System Requirements

## Entity Type
SECURITY_STANDARD, ICS_SECURITY, REQUIREMENT

## Overview
IEC 62443 provides cybersecurity standards for Industrial Automation and Control Systems (IACS). This dataset covers Foundational Requirements (FR), System Requirements (SR) from IEC 62443-3-3, and Component Requirements (CR) from IEC 62443-4-2, with practical implementation patterns for SL 1-4.

## Foundational Requirement 1: Identification and Authentication Control (FR 1)

### SR 1.1: Human User Identification and Authentication (400+ patterns)

#### Pattern: Multi-Factor Authentication for SCADA Access (SL 3-4)
- **Requirement**: Unique identification and authentication of all human users
- **Security Level**: SL 3-4 requires multi-factor authentication
- **Implementation**: Username/password + hardware token (YubiKey) or biometric
- **IACS Context**: Engineering workstation, HMI, SCADA server access
- **Technical Controls**:
  - RADIUS/TACACS+ authentication server
  - Integration with Active Directory + second factor
  - Local accounts disabled on SCADA servers
  - Session timeout after 15 minutes inactivity (SL 3)
- **STRIDE Mapping**: Prevents Spoofing, Elevation of Privilege
- **NIST 800-53**: IA-2(1) Multi-factor Authentication, IA-2(2) Network Access to Privileged Accounts
- **Verification**: Test authentication with valid/invalid credentials, test second factor requirement
- **Common Gaps**: Only password auth (SL 1-2), shared accounts, weak password policies
- **Cost Impact**: Medium (token deployment, AAA infrastructure)

#### Pattern: Individual Accountability - No Shared Accounts (All SLs)
- **Requirement**: Each user has unique identifier, no shared accounts
- **Implementation**: Individual AD accounts, named service accounts, audit trails
- **IACS Context**: Eliminate "operator", "engineer", "admin" shared accounts
- **Technical Controls**:
  - Unique usernames per individual
  - Role-based access control (RBAC)
  - Audit logging of all authentication events (SR 6.1)
- **STRIDE Mapping**: Prevents Repudiation (establishes accountability)
- **NIST 800-53**: IA-2, AC-2 Account Management
- **Common Challenge**: Legacy HMI systems with single "admin" account
- **Mitigation**: Where technically infeasible, compensating controls (video surveillance, logbook)
- **Verification**: Review user accounts, verify no generic/shared accounts

#### Pattern: Biometric Authentication for High-Security Areas (SL 4)
- **Requirement**: Strong authentication for SL 4 critical systems
- **Implementation**: Fingerprint + PIN for safety system access
- **IACS Context**: Safety instrumented systems (SIS), critical process control
- **Technical Controls**:
  - Biometric reader on engineering workstation
  - Liveness detection to prevent spoofing
  - Fallback to backup authentication if biometric fails
- **STRIDE Mapping**: Prevents Spoofing
- **NIST 800-53**: IA-3 Device Identification, IA-2(3) Local Access
- **Considerations**: Environmental factors (oil, dirt on hands), user acceptance
- **Cost Impact**: High (biometric hardware, enrollment, maintenance)

### SR 1.2: Software Process and Device Identification and Authentication (300+ patterns)

#### Pattern: Certificate-Based Device Authentication (SL 2-4)
- **Requirement**: Authenticate devices before allowing network communication
- **Security Level**: SL 2 recommended, SL 3-4 required
- **Implementation**: X.509 certificates for PLCs, HMIs, field devices
- **IACS Context**: Device joins industrial network, establishes trust
- **Technical Controls**:
  - Internal PKI (Certificate Authority)
  - Unique certificate per device
  - Certificate revocation capability
  - Mutual TLS authentication between devices
- **STRIDE Mapping**: Prevents Spoofing (device impersonation)
- **NIST 800-53**: IA-3 Device Identification and Authentication, IA-5(2) PKI-based Authentication
- **Implementation Challenge**: Many legacy devices lack certificate support
- **Compensating Control**: Network segmentation, MAC-based access control
- **Verification**: Attempt to connect unauthorized device, verify rejection

#### Pattern: Service Account Authentication and Management (SL 2-4)
- **Requirement**: Non-human accounts (services, APIs) must authenticate
- **Implementation**: Unique service accounts with strong passwords or API keys
- **IACS Context**: SCADA polling PLC data, historian collecting telemetry
- **Technical Controls**:
  - Named service accounts (not generic "service")
  - Managed passwords (automatic rotation via Vault, CyberArk)
  - API keys with expiration
  - Principle of least privilege for service accounts
- **STRIDE Mapping**: Prevents Elevation of Privilege
- **NIST 800-53**: IA-4 Identifier Management, AC-2 Account Management
- **Common Gap**: Hardcoded passwords in SCADA scripts
- **Mitigation**: Secret management solution, encrypted configuration
- **Cost Impact**: Medium (secret management tool)

### SR 1.3: Account Management (250+ patterns)

#### Pattern: Account Provisioning and De-provisioning Process (All SLs)
- **Requirement**: Timely creation and removal of accounts
- **Implementation**: Automated onboarding/offboarding workflow
- **IACS Context**: New engineer granted SCADA access, terminated employee removal
- **Technical Controls**:
  - HR system integration (trigger on hire/termination)
  - Account creation approval workflow
  - Immediate deactivation on termination
  - Periodic account review (quarterly for SL 3-4)
- **STRIDE Mapping**: Prevents Elevation of Privilege (orphaned accounts)
- **NIST 800-53**: AC-2 Account Management
- **Common Gap**: Accounts remain active after termination
- **Verification**: Audit active accounts, compare to HR system
- **Cost Impact**: Low (process automation)

#### Pattern: Privilege Escalation Workflow (SL 3-4)
- **Requirement**: Temporary elevation to privileged access with approval
- **Implementation**: Just-in-time (JIT) privileged access management
- **IACS Context**: Engineer needs temporary admin rights for PLC programming
- **Technical Controls**:
  - PAM solution (CyberArk, BeyondTrust)
  - Approval workflow (manager + security)
  - Time-limited elevation (4 hours)
  - Session recording
  - Automatic revocation after time limit
- **STRIDE Mapping**: Prevents Elevation of Privilege, Repudiation
- **NIST 800-53**: AC-6(2) Non-privileged Access for Nonsecurity Functions
- **Cost Impact**: High (PAM solution)

### SR 1.5: Authenticator Management (200+ patterns)

#### Pattern: Strong Password Policy (SL 2-4)
- **Requirement**: Password complexity, length, expiration requirements
- **Security Level Differentiation**:
  - SL 1: 8 characters, basic complexity
  - SL 2: 10 characters, complexity, 90-day expiration
  - SL 3: 12 characters, complexity, 60-day expiration, no reuse (10 previous)
  - SL 4: 14+ characters or passphrase, 30-day expiration, MFA required
- **IACS Context**: Accounts accessing SCADA, HMI, engineering workstations
- **Technical Controls**:
  - Domain Group Policy (Windows)
  - PAM password vault
  - Password complexity enforcement at authentication system
- **STRIDE Mapping**: Prevents Spoofing (credential guessing), Elevation of Privilege
- **NIST 800-53**: IA-5(1) Password-based Authentication
- **Common Gap**: Default/vendor passwords unchanged
- **Verification**: Attempt to set weak password, verify rejection

## Foundational Requirement 2: Use Control (FR 2)

### SR 2.1: Authorization Enforcement (500+ patterns)

#### Pattern: Role-Based Access Control (RBAC) for SCADA Operations (All SLs)
- **Requirement**: Enforce authorization for all access attempts
- **Implementation**: RBAC with predefined roles (Operator, Engineer, Administrator)
- **IACS Context**: Operator can view but not modify setpoints, Engineer can modify
- **Roles Example**:
  - **Operator**: View HMI, acknowledge alarms (Read-only on critical parameters)
  - **Advanced Operator**: Operator + adjust non-critical setpoints
  - **Engineer**: Advanced Operator + modify PLC logic, configure devices
  - **Administrator**: All privileges + user management, system configuration
- **Technical Controls**:
  - SCADA application RBAC
  - Group-based access in Active Directory
  - Database-level permissions (read vs. write)
- **STRIDE Mapping**: Prevents Elevation of Privilege, Tampering
- **NIST 800-53**: AC-3 Access Enforcement, AC-6 Least Privilege
- **Verification**: Test each role's permissions, verify denials
- **Cost Impact**: Medium (RBAC configuration, testing)

#### Pattern: Least Privilege for Service Accounts (SL 2-4)
- **Requirement**: Service accounts have minimum necessary permissions
- **Implementation**: Dedicated service accounts with specific permissions
- **IACS Context**: Historian service account can only read PLC data, not write
- **Technical Controls**:
  - Separate service account per service
  - Database permissions: SELECT only (historian), no INSERT/UPDATE/DELETE
  - File system: Read-only access to configuration files
  - Network: Firewall rules limit source/destination
- **STRIDE Mapping**: Prevents Elevation of Privilege, Tampering
- **NIST 800-53**: AC-6 Least Privilege
- **Common Gap**: Service accounts with "Domain Admin" or equivalent
- **Cost Impact**: Low (permission configuration)

### SR 2.2: Wireless Use Control (SL 2-4)
- **Requirement**: Control and monitor wireless access to IACS
- **Implementation**: Wireless disabled in control network, or tightly controlled
- **IACS Context**: Wireless sensors, mobile HMI tablets
- **Technical Controls**:
  - WPA3-Enterprise with 802.1X authentication
  - Separate VLAN for wireless devices
  - MAC address whitelisting
  - Wireless IDS (Airmagnet, Cisco ISE)
  - Regular RF spectrum scans for rogue APs
- **STRIDE Mapping**: Prevents Spoofing, Information Disclosure (eavesdropping)
- **NIST 800-53**: AC-18 Wireless Access
- **IEC 62443**: SR 5.1 (Network Segmentation) for wireless VLAN
- **Cost Impact**: Medium (wireless security infrastructure)

### SR 2.3: Use Control for Portable and Mobile Devices (SL 2-4)
- **Requirement**: Control USB drives, laptops, tablets accessing IACS
- **Implementation**: Device whitelisting, encryption requirements
- **IACS Context**: Laptop for PLC programming, USB for firmware updates
- **Technical Controls**:
  - Device Control policy (block unauthorized USB)
  - Whitelist approved devices by serial number
  - Malware scanning on USB insertion
  - Full disk encryption requirement (BitLocker, FileVault)
  - MDM for mobile devices (InTune, MobileIron)
- **STRIDE Mapping**: Prevents Tampering (malware introduction), Information Disclosure (data theft)
- **NIST 800-53**: MP-7 Media Use, AC-19 Access Control for Mobile Devices
- **Common Gap**: Unrestricted USB usage, personal laptops on OT network
- **Cost Impact**: Low to Medium (device control software)

## Foundational Requirement 3: System Integrity (FR 3)

### SR 3.1: Communication Integrity (400+ patterns)

#### Pattern: Protocol Security for SCADA Communications (SL 3-4)
- **Requirement**: Protect integrity of information during transmission
- **Implementation**: Encrypted and authenticated protocol wrappers
- **IACS Context**: SCADA server ↔ PLC communication using Modbus/DNP3
- **Technical Solutions**:
  - **Option 1**: TLS wrapper around Modbus/TCP
  - **Option 2**: DNP3 Secure Authentication (DNP3-SA)
  - **Option 3**: IPsec tunnel for field device communication
  - **Option 4**: Protocol gateway with encryption
- **Technical Controls**:
  - Mutual authentication (both endpoints)
  - Encryption of payload (AES-256)
  - Message authentication codes (HMAC)
  - Replay protection (sequence numbers, timestamps)
- **STRIDE Mapping**: Prevents Tampering (message modification), Spoofing
- **NIST 800-53**: SC-8 Transmission Confidentiality and Integrity
- **Implementation Challenge**: Legacy devices without encryption capability
- **Compensating Control**: Dedicated physically isolated network
- **Cost Impact**: Medium to High (protocol gateways, device upgrades)

#### Pattern: Secure Remote Access (SL 2-4)
- **Requirement**: Protect remote access sessions
- **Implementation**: VPN with MFA for remote engineer access
- **IACS Context**: Vendor support, remote troubleshooting
- **Technical Controls**:
  - IPsec or SSL VPN
  - Multi-factor authentication (MFA)
  - Jump host/bastion within DMZ (no direct OT access)
  - Session recording and audit
  - Time-limited access (auto-disconnect after 4 hours)
- **STRIDE Mapping**: Prevents Spoofing, Tampering, Information Disclosure
- **NIST 800-53**: AC-17 Remote Access, SC-8, IA-2(1) MFA
- **IEC 62443**: SR 1.13 Access via Untrusted Networks
- **Cost Impact**: Medium (VPN infrastructure, MFA)

### SR 3.3: Security Functionality Verification (200+ patterns)

#### Pattern: Code Signing for PLC Logic (SL 3-4)
- **Requirement**: Verify integrity of software and configuration
- **Implementation**: Digital signatures on PLC programs
- **IACS Context**: Upload logic to PLC, verify not tampered
- **Technical Controls**:
  - Code signing certificate for engineers
  - PLC firmware validates signature before accepting logic
  - Reject unsigned or invalid signature
  - Audit log of signature verification results
- **STRIDE Mapping**: Prevents Tampering (malicious logic), Elevation of Privilege
- **NIST 800-53**: SI-7 Software, Firmware, and Information Integrity
- **Implementation Challenge**: Many older PLCs don't support signature verification
- **Compensating Control**: Network segmentation, engineering workstation hardening
- **Cost Impact**: Medium (PKI infrastructure, PLC upgrades if needed)

#### Pattern: Firmware Integrity Verification (SL 2-4)
- **Requirement**: Verify firmware integrity before and after updates
- **Implementation**: Cryptographic hash verification
- **IACS Context**: Firmware update for HMI, PLC, field device
- **Technical Controls**:
  - Vendor-provided hash (SHA-256) of firmware file
  - Hash verification before flashing
  - Secure boot (if supported by device)
  - TPM or hardware root of trust
  - Rollback to previous version if integrity check fails
- **STRIDE Mapping**: Prevents Tampering (malicious firmware)
- **NIST 800-53**: SI-7, SA-12 Supply Chain Protection
- **IEC 62443**: SR 3.4 Software and Information Integrity
- **Cost Impact**: Low (process), High if hardware upgrades needed

### SR 3.4: Software and Information Integrity (300+ patterns)

#### Pattern: Application Whitelisting on Engineering Workstations (SL 3-4)
- **Requirement**: Prevent execution of unauthorized software
- **Implementation**: Application whitelisting (AppLocker, McAfee Application Control)
- **IACS Context**: Engineering workstation can only run approved PLC programming software
- **Technical Controls**:
  - Whitelist by publisher (code signing certificate)
  - Whitelist by file hash (for unsigned tools)
  - Whitelist by path (C:\Program Files\Siemens\...)
  - Block script execution (PowerShell, VBS) except signed
  - Audit mode initially, then enforcement
- **STRIDE Mapping**: Prevents Elevation of Privilege (malware execution), Tampering
- **NIST 800-53**: CM-7 Least Functionality, SI-7
- **Common Gap**: Antivirus only (signature-based, reactive)
- **Cost Impact**: Medium (whitelisting solution, management overhead)

## Foundational Requirement 4: Data Confidentiality (FR 4)

### SR 4.1: Information Confidentiality (350+ patterns)

#### Pattern: Encryption of Sensitive Data at Rest (SL 3-4)
- **Requirement**: Protect confidentiality of stored information
- **Implementation**: Database encryption, encrypted file systems
- **IACS Context**: Historian database with process data, recipe files
- **Technical Controls**:
  - Transparent Data Encryption (TDE) for databases
  - BitLocker/LUKS for disk encryption
  - Encrypted backups
  - Key management system (HSM, KMS)
- **STRIDE Mapping**: Prevents Information Disclosure
- **NIST 800-53**: SC-28 Protection of Information at Rest
- **Data Classification**:
  - Critical: Recipes, proprietary process parameters (AES-256)
  - Sensitive: Historian data (AES-128 acceptable)
  - Public: HMI screen layouts (no encryption needed)
- **Cost Impact**: Medium (encryption implementation, key management)

#### Pattern: Network Encryption for Confidential Data (SL 2-4)
- **Requirement**: Encrypt confidential information in transit
- **Implementation**: TLS/IPsec for sensitive communications
- **IACS Context**: Proprietary recipe download to PLC
- **Technical Controls**:
  - TLS 1.2+ for web interfaces (HMI, SCADA)
  - IPsec for site-to-site VPN (plant to corporate)
  - MACsec for Layer 2 encryption (switches)
- **STRIDE Mapping**: Prevents Information Disclosure (eavesdropping)
- **NIST 800-53**: SC-8 Transmission Confidentiality and Integrity
- **Trade-off**: Encryption overhead vs. confidentiality need
- **Cost Impact**: Low to Medium (TLS certificates, VPN appliances)

### SR 4.2: Information Persistence (200+ patterns)

#### Pattern: Secure Data Deletion (SL 2-4)
- **Requirement**: Prevent recovery of purged information
- **Implementation**: Cryptographic erasure or physical destruction
- **IACS Context**: Decommissioned HMI with process data
- **Technical Controls**:
  - Data wiping tool (DBAN, DoD 5220.22-M)
  - Crypto-shredding (destroy encryption keys)
  - Physical destruction of media (hard drives)
  - Certificate of destruction
- **STRIDE Mapping**: Prevents Information Disclosure (from disposed equipment)
- **NIST 800-53**: MP-6 Media Sanitization
- **Regulatory**: GDPR Right to Erasure, HIPAA disposal requirements
- **Cost Impact**: Low (software tools), Medium if outsourced destruction

#### Pattern: Temporary File and Cache Management (SL 2-4)
- **Requirement**: Protect or purge temporary files containing sensitive info
- **Implementation**: Encrypted temp directories, automatic cleanup
- **IACS Context**: Engineering software temp files during PLC download
- **Technical Controls**:
  - Encrypted file system for temp directories
  - Automatic cleanup on session end
  - Memory-only temp storage where possible
  - Overwrite temp files on delete (not just unlink)
- **STRIDE Mapping**: Prevents Information Disclosure
- **NIST 800-53**: SC-28, MP-6
- **Cost Impact**: Low (configuration)

## Foundational Requirement 5: Restricted Data Flow (FR 5)

### SR 5.1: Network Segmentation (500+ patterns)

#### Pattern: Purdue Model Network Architecture (All SLs)
- **Requirement**: Segment network into security zones based on criticality
- **Implementation**: Purdue Model (Levels 0-5) with firewalls between levels
- **IACS Context**: Physical separation between IT (Level 4-5) and OT (Level 0-3)
- **Zone Definition**:
  - **Level 5 (Enterprise)**: Corporate network, business systems
  - **Level 4 (Business Planning)**: ERP, MES, enterprise databases
  - **Level 3 (Manufacturing Operations)**: SCADA, historians, MES interfaces
  - **Level 3.5 (DMZ)**: Firewall, data diode, secure interface between Level 3-4
  - **Level 2 (Supervisory Control)**: HMIs, engineering workstations, OPC servers
  - **Level 1 (Basic Control)**: PLCs, RTUs, DCS controllers, safety systems
  - **Level 0 (Process)**: Sensors, actuators, field devices
- **Firewall Rules**:
  - Level 4→3: Read-only (historian replication)
  - Level 3→2: Specific protocols only (OPC-UA port 4840)
  - Level 2→1: Control protocols (Modbus port 502, EtherNet/IP)
  - Level 1→0: I/O protocols only
  - Default deny all, explicit allow only
- **STRIDE Mapping**: Limits Tampering, Elevation of Privilege, DoS
- **NIST 800-53**: SC-7 Boundary Protection, AC-4 Information Flow Enforcement
- **Cost Impact**: High (firewalls, network redesign)

#### Pattern: Conduit Definition and Protection (SL 2-4)
- **Requirement**: Define and protect all communication paths between zones
- **Implementation**: Document all conduits, apply appropriate security
- **IACS Context**: Conduit from SCADA (Level 3) to PLC (Level 1)
- **Conduit Documentation**:
  - Source zone: Level 3 (SCADA server subnet 192.168.3.0/24)
  - Destination zone: Level 1 (PLC subnet 10.1.1.0/24)
  - Protocol: Modbus/TCP port 502
  - Initiator: SCADA server (192.168.3.10)
  - Responder: PLC (10.1.1.50-70)
  - Security: Firewall rule, IDS monitoring, TLS wrapper (SL 3+)
- **STRIDE Mapping**: Prevents Tampering (unauthorized communication)
- **NIST 800-53**: AC-4 Information Flow Enforcement
- **IEC 62443-3-2**: Zone and conduit methodology
- **Cost Impact**: Low (documentation), Medium (security implementation)

### SR 5.2: Zone Boundary Protection (400+ patterns)

#### Pattern: Industrial Firewall with Deep Packet Inspection (SL 2-4)
- **Requirement**: Monitor and control traffic at zone boundaries
- **Implementation**: Industrial protocol-aware firewall
- **IACS Context**: Firewall between Level 3 (SCADA) and Level 2 (HMI/Engineering)
- **Technical Controls**:
  - Stateful inspection firewall (Cisco ISA, Palo Alto, Fortinet)
  - Deep packet inspection (DPI) for industrial protocols
  - Modbus/DNP3/EtherNet/IP protocol validation
  - Anomaly detection (unexpected commands, out-of-range values)
  - Rate limiting (DoS protection)
  - Log all denied connections
- **STRIDE Mapping**: Prevents Tampering, Elevation of Privilege, DoS
- **NIST 800-53**: SC-7 Boundary Protection, SI-4 System Monitoring
- **Cost Impact**: High (industrial firewalls are expensive)

#### Pattern: Data Diode for Unidirectional Flow (SL 3-4)
- **Requirement**: Enforce one-way data flow (typically OT→IT)
- **Implementation**: Hardware data diode between Level 3 and Level 4
- **IACS Context**: Historian data replication from OT to IT (read-only)
- **Technical Controls**:
  - Hardware data diode (Waterfall, Owl Cyber Defense)
  - Physically prevents reverse traffic
  - Replication protocol (one-way UDP, file transfer)
  - Integrity checking on IT side
- **STRIDE Mapping**: Prevents Tampering (IT cannot write to OT), Elevation of Privilege
- **NIST 800-53**: AC-4 Information Flow Enforcement
- **IEC 62443**: Highest level of boundary protection
- **Trade-off**: No bidirectional comms (e.g., remote acknowledgements impossible)
- **Cost Impact**: High (hardware diode $10K-50K+)

### SR 5.3: General Purpose Person-to-Person Communication Restrictions (SL 2-4)
- **Requirement**: Restrict email, web browsing, IM on OT systems
- **Implementation**: Block or tightly control general internet access from OT
- **IACS Context**: Engineering workstation in Level 2
- **Technical Controls**:
  - No direct internet access from OT zones
  - Web proxy with whitelist (only vendor support sites)
  - Email restricted or via jump host in DMZ
  - Block personal email (Gmail, Yahoo) and social media
  - No USB drives from external sources
- **STRIDE Mapping**: Prevents Tampering (malware via email), Elevation of Privilege
- **NIST 800-53**: AC-4, SC-7
- **Rationale**: Reduce phishing and malware vectors in OT
- **User Impact**: Inconvenience, dedicated IT workstation needed for general tasks
- **Cost Impact**: Low (firewall rules, proxy)

## Foundational Requirement 6: Timely Response to Events (FR 6)

### SR 6.1: Audit Log Accessibility (300+ patterns)

#### Pattern: Centralized Logging for IACS (All SLs)
- **Requirement**: Collect, protect, and review audit logs
- **Implementation**: Syslog server collecting logs from all OT devices
- **IACS Context**: Logs from SCADA, HMIs, PLCs, firewalls, switches
- **Log Sources**:
  - SCADA server: User logins, command execution, alarms
  - HMI workstations: User actions, configuration changes
  - PLCs: Logic uploads/downloads, mode changes, communication errors
  - Firewalls: Denied connections, policy violations
  - Network switches: Port status, MAC changes
- **Technical Controls**:
  - Syslog server in Level 3 (dedicated logging VLAN)
  - Log forwarding from all devices
  - Write-once storage or log signing (prevent tampering)
  - Retention: 90 days online, 1 year archive (SL 3-4)
  - Automated backup of logs
- **STRIDE Mapping**: Enables detection of all STRIDE categories, prevents Repudiation
- **NIST 800-53**: AU-2 Audit Events, AU-9 Protection of Audit Information
- **Cost Impact**: Medium (syslog server, storage)

#### Pattern: Security Event Correlation and Alerting (SL 3-4)
- **Requirement**: Analyze logs to detect security events
- **Implementation**: SIEM or ICS-specific security monitoring
- **IACS Context**: Detect unauthorized PLC logic changes, unusual network traffic
- **Technical Controls**:
  - SIEM (Splunk, QRadar) or ICS SIEM (Nozomi, Claroty)
  - Correlation rules for common attacks:
    - Multiple failed logins → Brute force alert
    - PLC logic change outside maintenance window → Investigation
    - Network scan detected → Potential reconnaissance
    - Firewall denials from same source → Block at border
  - Automated alerting (email, SMS, ticketing system)
- **STRIDE Mapping**: Detects all STRIDE threats
- **NIST 800-53**: SI-4 Information System Monitoring, IR-4 Incident Handling
- **Cost Impact**: High (SIEM licensing, rules development, analyst time)

### SR 6.2: Continuous Monitoring (250+ patterns)

#### Pattern: ICS Intrusion Detection System (IDS) (SL 2-4)
- **Requirement**: Detect malicious activity in real-time
- **Implementation**: Passive network monitoring with ICS protocol awareness
- **IACS Context**: IDS sensors on network taps at zone boundaries
- **Technical Controls**:
  - ICS-specific IDS (Nozomi Networks, Claroty, Dragos)
  - Passive network tap (no impact on OT traffic)
  - Protocol anomaly detection (malformed Modbus, unexpected commands)
  - Behavioral baseline (learn normal, alert on deviation)
  - Asset inventory auto-discovery
  - Vulnerability detection (device firmware versions)
- **STRIDE Mapping**: Detects Spoofing, Tampering, Elevation of Privilege, DoS
- **NIST 800-53**: SI-4 System Monitoring
- **IEC 62443**: SR 6.2 specifically addresses continuous monitoring
- **Cost Impact**: High (IDS appliances, annual subscriptions)

## Foundational Requirement 7: Resource Availability (FR 7)

### SR 7.1: Denial of Service Protection (300+ patterns)

#### Pattern: Network-Level DoS Mitigation (All SLs)
- **Requirement**: Protect against network flood attacks
- **Implementation**: Rate limiting, traffic shaping, DDoS mitigation
- **IACS Context**: Protect SCADA server from SYN flood, Modbus flood
- **Technical Controls**:
  - Firewall rate limiting (connections/sec per source)
  - SYN cookies on SCADA server TCP stack
  - Traffic prioritization (QoS): Control traffic > Monitoring > Bulk transfer
  - Dedicated bandwidth for control networks (no sharing with IT)
  - Intrusion Prevention System (IPS) to block floods
- **STRIDE Mapping**: Prevents Denial of Service
- **NIST 800-53**: SC-5 Denial of Service Protection
- **IEC 62443**: SR 7.1, SR 7.2 Resource Management
- **Cost Impact**: Low to Medium (firewall features, QoS configuration)

#### Pattern: Application-Level Resource Limits (SL 2-4)
- **Requirement**: Prevent resource exhaustion in applications
- **Implementation**: Connection limits, memory limits, timeout settings
- **IACS Context**: SCADA server limits simultaneous HMI connections
- **Technical Controls**:
  - Max connections: 50 HMI clients to SCADA server
  - Connection timeout: 5 minutes idle for monitoring, 15 min for control
  - Memory limits: SCADA process max 4GB RAM
  - CPU throttling: SCADA server reserves 20% CPU for critical functions
  - Database connection pooling (max 100 connections)
- **STRIDE Mapping**: Prevents Denial of Service (resource exhaustion)
- **NIST 800-53**: SC-6 Resource Availability
- **Cost Impact**: Low (configuration)

### SR 7.2: Resource Management (200+ patterns)

#### Pattern: Time-Critical Communication Prioritization (SL 3-4)
- **Requirement**: Ensure critical control commands get priority
- **Implementation**: QoS with DiffServ or 802.1p priority tagging
- **IACS Context**: Safety system commands prioritized over historian queries
- **QoS Classes**:
  - **Highest (EF - Expedited Forwarding)**: Safety system commands, emergency stop
  - **High (AF41)**: Real-time control commands (PLC to valve actuator)
  - **Medium (AF21)**: HMI monitoring traffic (display updates)
  - **Low (Best Effort)**: Historian data collection, bulk transfers
- **Technical Controls**:
  - 802.1p VLAN priority tagging
  - DiffServ Code Point (DSCP) marking at IP layer
  - Switches and routers honor QoS markings
  - Bandwidth reservation for highest priority
- **STRIDE Mapping**: Prevents Denial of Service (ensures critical function availability)
- **NIST 800-53**: SC-6 Resource Availability
- **IEC 62443**: SR 7.2, SR 7.3 Control System Backup
- **Cost Impact**: Low (QoS configuration on managed switches)

## Security Levels (SL) Differentiation

### SL 1: Protection against casual or coincidental violation
- **Use Case**: Non-critical processes, pilot plants, development environments
- **Authentication**: Username/password acceptable
- **Network Security**: Basic firewall, no segmentation required
- **Monitoring**: Optional logging
- **Example**: Research lab SCADA system

### SL 2: Protection against intentional violation using simple means
- **Use Case**: Standard industrial processes, limited impact if compromised
- **Authentication**: Strong passwords, account management
- **Network Security**: Segmentation (zones), firewall with rules
- **Monitoring**: Centralized logging, basic IDS
- **Example**: Manufacturing plant, food processing

### SL 3: Protection against intentional violation using sophisticated means
- **Use Case**: Critical infrastructure, significant safety/environmental impact
- **Authentication**: Multi-factor authentication (MFA)
- **Network Security**: Defense in depth, industrial firewall, IDS/IPS
- **Monitoring**: SIEM with correlation, continuous monitoring
- **Encryption**: Required for communications
- **Example**: Electric grid SCADA, water treatment, chemical plant

### SL 4: Protection against intentional violation using sophisticated means with extended resources
- **Use Case**: National critical infrastructure, severe consequences if compromised
- **Authentication**: MFA + biometric for critical functions
- **Network Security**: Multiple layers, data diodes, air gaps
- **Monitoring**: 24/7 SOC, advanced threat detection
- **Encryption**: Required (data at rest and in transit)
- **Physical Security**: Enhanced physical controls
- **Example**: Nuclear power plant, military installations

## Cross-Framework Integration

### IEC 62443 to STRIDE Mapping
- **FR 1 (Identification/Authentication)**: Prevents Spoofing
- **FR 2 (Use Control)**: Prevents Elevation of Privilege, Tampering
- **FR 3 (System Integrity)**: Prevents Tampering
- **FR 4 (Data Confidentiality)**: Prevents Information Disclosure
- **FR 5 (Restricted Data Flow)**: Limits all STRIDE threats
- **FR 6 (Timely Response)**: Detects and responds to STRIDE violations
- **FR 7 (Resource Availability)**: Prevents Denial of Service

### IEC 62443 to NIST 800-53 Mapping
Comprehensive alignment between IEC 62443 SRs and NIST controls for integrated compliance approach.

### IEC 62443 to PASTA Integration
- **PASTA Stage 1 (Business Objectives)** informs SL determination
- **PASTA Stage 2 (Technical Scope)** defines zones and conduits
- **PASTA Stage 5 (Vulnerability Analysis)** identifies SR/CR gaps
- **PASTA Stage 7 (Risk Analysis)** validates SL adequacy
