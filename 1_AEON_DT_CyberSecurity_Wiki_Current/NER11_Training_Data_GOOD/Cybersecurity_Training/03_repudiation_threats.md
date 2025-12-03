# STRIDE: Repudiation Threats

## Entity Type
THREAT_MODEL, ATTACK_VECTOR, MITIGATION

## Overview
Repudiation threats involve actions that cannot be proven or traced back to the actor. This includes denial of actions, lack of non-repudiation, audit trail manipulation, and inability to prove who performed what action.

## Threat Patterns (150+ patterns)

### Log Manipulation and Deletion

#### Pattern: Security Log Deletion
- **Threat**: Delete security event logs to hide malicious activity
- **DFD Element**: Data Store (Audit Logs)
- **Attack Vector**: Elevated privileges, malware, compromised account
- **Impact**: Loss of forensic evidence, inability to detect/investigate breaches
- **STRIDE Category**: Repudiation + Tampering
- **Mitigation**: Centralized logging, write-once storage, log forwarding, SIEM
- **NIST Controls**: AU-9 (Protection of Audit Information), AU-11 (Audit Record Retention)
- **IEC 62443**: FR 6 (Timely Response to Events), SR 6.1 (Audit Log Accessibility)
- **Detection**: Log integrity checks, missing log entries, time gaps

#### Pattern: Application Log Tampering
- **Threat**: Modify application logs to alter recorded events
- **DFD Element**: Data Store (Application Logs) → Process (Log Analysis)
- **Attack Vector**: File system access, database modification, log injection
- **Impact**: False evidence, hidden transactions, altered audit trail
- **STRIDE Category**: Repudiation + Tampering
- **Mitigation**: Log signing, hash chains, immutable logging, centralized collection
- **NIST Controls**: AU-9, AU-10 (Non-repudiation)
- **IEC 62443**: SR 6.1, FR 6
- **Detection**: Log signature validation, hash chain verification, timestamps

#### Pattern: Windows Event Log Clearing
- **Threat**: Clear Windows Event Logs using wevtutil or API
- **DFD Element**: Data Store (Windows Event Logs)
- **Attack Vector**: Administrative privileges, scripting, malware
- **Impact**: Loss of security events, hidden lateral movement, forensics gaps
- **STRIDE Category**: Repudiation
- **Mitigation**: Forward logs immediately, protected event forwarding, detect clearlog events
- **NIST Controls**: AU-9, SI-4 (Information System Monitoring)
- **IEC 62443**: SR 6.1, SR 6.2 (Continuous Monitoring)
- **Detection**: Event ID 1102 (audit log cleared), missing events, SIEM alerts

#### Pattern: Syslog Flood to Rotate Logs
- **Threat**: Generate massive log volume to force rotation and deletion
- **DFD Element**: Data Flow (Syslog) → Data Store (Log Files)
- **Attack Vector**: Automated log generation, application abuse
- **Impact**: Critical events rotated out before analysis
- **STRIDE Category**: Repudiation + Denial of Service
- **Mitigation**: Rate limiting, log filtering, adequate storage, retention policies
- **NIST Controls**: AU-4 (Audit Storage Capacity), AU-5 (Response to Audit Failure)
- **IEC 62443**: SR 6.1, FR 7 (Resource Availability)
- **Detection**: Abnormal log volume, rapid rotation, storage alerts

#### Pattern: Database Audit Trail Deletion
- **Threat**: Delete or disable database audit trails
- **DFD Element**: Data Store (Database Audit Tables)
- **Attack Vector**: DBA privileges, SQL injection, privilege escalation
- **Impact**: Untraced database modifications, compliance violations
- **STRIDE Category**: Repudiation + Tampering
- **Mitigation**: Separate audit database, restricted access, database activity monitoring
- **NIST Controls**: AU-2 (Audit Events), AU-9, AC-6 (Least Privilege)
- **IEC 62443**: SR 6.1, FR 2 (Use Control)
- **Detection**: Audit table modifications, missing audit records, DAM alerts

### Timestamp Manipulation

#### Pattern: System Clock Tampering
- **Threat**: Modify system time to alter log timestamps
- **DFD Element**: Process (System Clock) → Data Store (Logs)
- **Attack Vector**: Admin privileges, time service manipulation
- **Impact**: Incorrect event sequencing, forensic timeline corruption
- **STRIDE Category**: Repudiation + Tampering
- **Mitigation**: NTP synchronization, protected time source, timestamp signing
- **NIST Controls**: AU-8 (Time Stamps), SC-45 (System Time Synchronization)
- **IEC 62443**: SR 6.1, FR 6
- **Detection**: Time drift alerts, NTP sync failures, timestamp anomalies

#### Pattern: Log Timestamp Falsification
- **Threat**: Directly modify log entry timestamps
- **DFD Element**: Data Store (Log Entries) timestamp fields
- **Attack Vector**: Direct database/file access, log injection
- **Impact**: False alibi, timeline confusion, forensic misdirection
- **STRIDE Category**: Repudiation + Tampering
- **Mitigation**: Cryptographic timestamps, blockchain logging, trusted timestamping
- **NIST Controls**: AU-8, AU-10
- **IEC 62443**: SR 6.1
- **Detection**: Timestamp sequence violations, signature failures

#### Pattern: NTP Server Manipulation
- **Threat**: Compromise or spoof NTP server to alter client times
- **DFD Element**: External Entity (NTP Server) → Process (Time Sync)
- **Attack Vector**: NTP amplification, MITM, unauthenticated NTP
- **Impact**: Mass timestamp manipulation, coordinated time skew
- **STRIDE Category**: Repudiation + Spoofing
- **Mitigation**: Authenticated NTP (NTS), multiple time sources, time bound checking
- **NIST Controls**: AU-8, SC-45
- **IEC 62443**: SR 1.1, FR 6
- **Detection**: Time source validation, multiple NTP server comparison

### Authentication and Session Repudiation

#### Pattern: Shared Account Usage
- **Threat**: Multiple users share accounts, preventing attribution
- **DFD Element**: Process (Authentication) → External Entity (User)
- **Attack Vector**: Policy violation, convenience over security
- **Impact**: Inability to attribute actions, accountability loss
- **STRIDE Category**: Repudiation
- **Mitigation**: Individual accounts, identity federation, prohibit account sharing
- **NIST Controls**: IA-2 (Identification and Authentication), AC-2 (Account Management)
- **IEC 62443**: FR 1 (Identification and Authentication), SR 1.1
- **Detection**: Policy violations, simultaneous logins, behavioral patterns

#### Pattern: Session Token Reuse Without Logging
- **Threat**: Reuse session tokens without logging individual actions
- **DFD Element**: Data Flow (Session Token) → Process (Application)
- **Attack Vector**: Session sharing, token theft, loose session management
- **Impact**: Actions attributed to wrong user, unclear accountability
- **STRIDE Category**: Repudiation
- **Mitigation**: Per-action logging, session fingerprinting, device binding
- **NIST Controls**: AU-2, SC-23 (Session Authenticity), IA-2
- **IEC 62443**: SR 1.1, SR 6.1
- **Detection**: Session behavior analysis, device mismatch

#### Pattern: Anonymous Transaction Processing
- **Threat**: Process transactions without recording initiator identity
- **DFD Element**: Process (Transaction) → Data Store (Records)
- **Attack Vector**: Design flaw, insufficient logging
- **Impact**: Financial fraud unattributable, compliance violations
- **STRIDE Category**: Repudiation
- **Mitigation**: Mandatory authentication, transaction signing, audit trails
- **NIST Controls**: AU-2, AU-10, IA-2
- **IEC 62443**: FR 1, SR 6.1
- **Detection**: Audit trail review, compliance scans

#### Pattern: Guest/Anonymous Access Abuse
- **Threat**: Malicious actions performed through guest accounts
- **DFD Element**: Process (Guest Access) → Data Store
- **Attack Vector**: Anonymous features, unrestricted guest access
- **Impact**: Untraceable malicious activity, system abuse
- **STRIDE Category**: Repudiation + Elevation of Privilege
- **Mitigation**: Minimize guest access, require registration, rate limiting, captcha
- **NIST Controls**: AC-14 (Permitted Actions without Identification), AU-2
- **IEC 62443**: FR 1, FR 2
- **Detection**: Guest activity monitoring, abuse pattern detection

### Non-Repudiation Bypass

#### Pattern: Unsigned Transactions
- **Threat**: Critical transactions processed without cryptographic signatures
- **DFD Element**: Process (Transaction Processing)
- **Attack Vector**: Missing digital signature requirement
- **Impact**: Transaction repudiation, dispute resolution difficulty
- **STRIDE Category**: Repudiation
- **Mitigation**: Digital signatures, transaction signing, PKI infrastructure
- **NIST Controls**: AU-10, SC-13 (Cryptographic Protection), IA-5(2)
- **IEC 62443**: SR 1.13 (Access via Untrusted Networks), SR 4.3 (Cryptography)
- **Detection**: Unsigned transaction detection, compliance monitoring

#### Pattern: Email Without DKIM/SPF
- **Threat**: Send email without authentication, allowing repudiation
- **DFD Element**: Data Flow (Email) → External Entity
- **Attack Vector**: Lack of sender authentication
- **Impact**: Email content deniability, impersonation opportunity
- **STRIDE Category**: Repudiation + Spoofing
- **Mitigation**: DKIM signing, SPF/DMARC, message signing (S/MIME, PGP)
- **NIST Controls**: AU-10, SC-8 (Transmission Integrity)
- **IEC 62443**: SR 3.1 (Communication Integrity)
- **Detection**: DKIM/SPF validation, email authentication monitoring

#### Pattern: API Call Without Proof of Origin
- **Threat**: API requests processed without verifiable origin proof
- **DFD Element**: Data Flow (API Request) → Process (API Server)
- **Attack Vector**: Missing request signing, weak authentication
- **Impact**: API abuse repudiation, fraudulent request denial
- **STRIDE Category**: Repudiation
- **Mitigation**: API request signing (HMAC, JWT), mutual TLS, audit logging
- **NIST Controls**: AU-10, IA-2, SC-8
- **IEC 62443**: SR 1.1, SR 3.1
- **Detection**: Unsigned request detection, authentication failures

#### Pattern: File Upload Without Provenance
- **Threat**: Accept file uploads without recording uploader identity
- **DFD Element**: Process (File Upload) → Data Store (Files)
- **Attack Vector**: Anonymous upload, insufficient metadata
- **Impact**: Malicious file source unattributable, legal liability
- **STRIDE Category**: Repudiation
- **Mitigation**: Mandatory authentication, metadata logging, file signing
- **NIST Controls**: AU-2, IA-2, SI-10 (Input Validation)
- **IEC 62443**: FR 1, SR 6.1
- **Detection**: Audit trail review, provenance tracking

### Forensic Anti-Analysis

#### Pattern: Anti-Forensics Tool Usage
- **Threat**: Use tools to eliminate forensic artifacts (CCleaner, BleachBit, etc.)
- **DFD Element**: Data Store (Forensic Artifacts) → Process (Cleaning Tool)
- **Attack Vector**: Attacker-run cleanup tools, automated scripts
- **Impact**: Evidence destruction, investigation hindrance
- **STRIDE Category**: Repudiation + Tampering
- **Mitigation**: EDR detection, file access monitoring, artifact protection
- **NIST Controls**: AU-9, SI-4, AU-11
- **IEC 62443**: SR 6.1, FR 6
- **Detection**: Tool execution detection, mass file deletion, artifact gaps

#### Pattern: Secure File Deletion (Wiping)
- **Threat**: Overwrite files multiple times to prevent recovery
- **DFD Element**: Data Store (Files) → Process (Secure Delete)
- **Attack Vector**: Secure delete tools, military-grade wiping
- **Impact**: Evidence irrecoverable, investigation blocked
- **STRIDE Category**: Repudiation + Tampering
- **Mitigation**: Continuous forensic collection, immutable backups, write-once storage
- **NIST Controls**: AU-11, MP-6 (Media Sanitization - detection)
- **IEC 62443**: SR 6.1
- **Detection**: Secure delete tool detection, unusual disk I/O patterns

#### Pattern: Memory-Only Malware (Fileless)
- **Threat**: Operate entirely in memory, leaving no disk artifacts
- **DFD Element**: Process (Memory) only, no Data Store persistence
- **Attack Vector**: PowerShell, WMI, reflective DLL injection
- **Impact**: Difficult attribution, limited forensic evidence
- **STRIDE Category**: Repudiation
- **Mitigation**: Memory forensics, EDR with memory scanning, behavioral detection
- **NIST Controls**: SI-4, IR-4 (Incident Handling), AU-2
- **IEC 62443**: SR 6.2 (Continuous Monitoring)
- **Detection**: Behavioral analytics, memory scanning, parent process anomalies

#### Pattern: Log Injection to Create False Evidence
- **Threat**: Inject false log entries to misdirect investigation
- **DFD Element**: Data Store (Logs) ← Data Flow (Injected Logs)
- **Attack Vector**: Log injection vulnerabilities, application bugs
- **Impact**: False leads, investigator misdirection, false attribution
- **STRIDE Category**: Repudiation + Tampering
- **Mitigation**: Input validation, log structure validation, log signing
- **NIST Controls**: SI-10, AU-9, AU-10
- **IEC 62443**: SR 3.5 (Input Validation), SR 6.1
- **Detection**: Log format validation, signature verification, anomaly detection

### Network and Communication Repudiation

#### Pattern: Tor/VPN Usage for Anonymity
- **Threat**: Use anonymizing networks to hide activity origin
- **DFD Element**: External Entity (Anonymous Actor) → Data Flow (Tor/VPN)
- **Attack Vector**: Legitimate anonymity tools
- **Impact**: Source attribution difficult, investigation complexity
- **STRIDE Category**: Repudiation
- **Mitigation**: Tor/VPN detection, policy enforcement, require authentication
- **NIST Controls**: AC-20 (Use of External Systems), SI-4
- **IEC 62443**: FR 5 (Restricted Data Flow), SR 5.1
- **Detection**: Tor exit node lists, VPN detection, traffic analysis

#### Pattern: MAC Address Randomization
- **Threat**: Continuously change MAC address to avoid tracking
- **DFD Element**: External Entity (Network Device) identity
- **Attack Vector**: OS feature, MAC spoofing tools
- **Impact**: Device tracking impossible, accountability loss
- **STRIDE Category**: Repudiation + Spoofing
- **Mitigation**: 802.1X with certificate auth, network access control, DHCP fingerprinting
- **NIST Controls**: IA-3 (Device Identification), AC-17 (Remote Access)
- **IEC 62443**: FR 1, SR 1.2 (Software Process Identification)
- **Detection**: Authentication methods requiring device identity

#### Pattern: Encrypted Channel Without Logging Endpoints
- **Threat**: End-to-end encryption prevents logging of communication content
- **DFD Element**: Data Flow (E2E Encrypted) between processes
- **Attack Vector**: Legitimate encryption, privacy features
- **Impact**: Content of communication unauditable
- **STRIDE Category**: Repudiation + Information Disclosure (protection)
- **Mitigation**: Metadata logging, endpoint logging, acceptable use policies
- **NIST Controls**: AU-2, AC-20, AT-2 (Awareness Training)
- **IEC 62443**: FR 6, SR 6.1
- **Detection**: Metadata analysis, connection logging, policy violations

#### Pattern: Steganography for Hidden Communication
- **Threat**: Hide messages in images/files, leaving no obvious communication trail
- **DFD Element**: Data Flow (Covert Channel) embedded in Data Store
- **Attack Vector**: Steganography tools, custom encoding
- **Impact**: Covert communication undetected, exfiltration hidden
- **STRIDE Category**: Repudiation + Information Disclosure
- **Mitigation**: DLP with steganalysis, file inspection, outbound filtering
- **NIST Controls**: SI-4, SC-8, AU-2
- **IEC 62443**: SR 6.2, FR 5
- **Detection**: Steganalysis tools, entropy analysis, behavioral patterns

### Blockchain and Cryptocurrency Repudiation

#### Pattern: Cryptocurrency Mixing/Tumbling
- **Threat**: Use mixing services to obfuscate transaction origin
- **DFD Element**: Data Flow (Cryptocurrency Transaction) through External Entity (Mixer)
- **Attack Vector**: Legitimate privacy services
- **Impact**: Fund source attribution difficult, money laundering facilitation
- **STRIDE Category**: Repudiation
- **Mitigation**: Blockchain analysis, transaction monitoring, policy compliance
- **NIST Controls**: AU-2, SI-4, AC-20
- **IEC 62443**: SR 6.1, FR 6
- **Detection**: Known mixer addresses, transaction patterns, forensic blockchain analysis

#### Pattern: Privacy Coin Usage (Monero, Zcash)
- **Threat**: Use cryptocurrencies with built-in transaction obfuscation
- **DFD Element**: Data Flow (Private Cryptocurrency)
- **Attack Vector**: Legitimate privacy-focused blockchain protocols
- **Impact**: Transaction tracing nearly impossible
- **STRIDE Category**: Repudiation
- **Mitigation**: Policy restrictions, detection and blocking, compliance requirements
- **NIST Controls**: AC-20, AU-2, PM-9 (Risk Management Strategy)
- **IEC 62443**: FR 6, SR 6.1
- **Detection**: Network traffic analysis, cryptocurrency protocol detection

### Physical Security Repudiation

#### Pattern: Tailgating Without Badge Scan
- **Threat**: Follow authorized person through access control without badging
- **DFD Element**: Process (Physical Access Control) → Physical Zone
- **Attack Vector**: Social engineering, policy violation
- **Impact**: Unrecorded physical access, no audit trail
- **STRIDE Category**: Repudiation + Elevation of Privilege
- **Mitigation**: Mantrap/turnstiles, security awareness, guards, anti-tailgating detection
- **NIST Controls**: PE-3 (Physical Access Control), PE-2 (Physical Access Authorizations)
- **IEC 62443**: PE-3, SR 1.1
- **Detection**: Video analytics, weight sensors, security guard observation

#### Pattern: Stolen Badge Usage
- **Threat**: Use stolen/cloned access badge for unattributable access
- **DFD Element**: External Entity (Unauthorized Person) with valid badge token
- **Attack Vector**: Badge theft, cloning, lost badge
- **Impact**: Physical access attributed to badge owner, false accusation
- **STRIDE Category**: Repudiation + Spoofing
- **Mitigation**: Multi-factor (badge + PIN/biometric), monitoring, rapid deactivation
- **NIST Controls**: PE-3, IA-2, PE-2
- **IEC 62443**: FR 1, SR 1.1
- **Detection**: Anomalous access patterns, simultaneous badge usage, video verification

#### Pattern: Visitor Sign-In Sheet Falsification
- **Threat**: Provide false information in visitor logs
- **DFD Element**: Data Store (Visitor Log) ← External Entity (Visitor)
- **Attack Vector**: Manual log books, honor system
- **Impact**: Visitor presence deniable, security incident attribution failure
- **STRIDE Category**: Repudiation + Spoofing
- **Mitigation**: ID verification, automated systems, visitor badges with photos
- **NIST Controls**: PE-3, PE-8 (Visitor Access Records), IA-4 (Identifier Management)
- **IEC 62443**: FR 1, SR 6.1
- **Detection**: Video surveillance correlation, ID verification

### Industrial Control System (ICS) Repudiation

#### Pattern: Unsigned PLC Code Changes
- **Threat**: Modify PLC logic without cryptographic proof of author
- **DFD Element**: Data Store (PLC Program) ← Process (Engineering Workstation)
- **Attack Vector**: Lack of code signing, weak change control
- **Impact**: Malicious logic changes unattributable, insider threat undetected
- **STRIDE Category**: Repudiation + Tampering
- **Mitigation**: Code signing, change management, version control with attribution
- **NIST Controls**: CM-3 (Configuration Change Control), AU-10, SA-10
- **IEC 62443**: SR 3.1, SR 3.3, FR 2
- **Detection**: Code comparison, unsigned code detection, version control audits

#### Pattern: HMI Command Without User Attribution
- **Threat**: Execute control commands without logging operator identity
- **DFD Element**: Process (HMI) → Data Flow (Control Command) → Process (Controller)
- **Attack Vector**: Shared HMI accounts, insufficient logging
- **Impact**: Critical command origin unknown, accountability loss
- **STRIDE Category**: Repudiation
- **Mitigation**: Individual operator accounts, per-command logging, two-person rule
- **NIST Controls**: AU-2, AC-2, IA-2, AC-5 (Separation of Duties)
- **IEC 62443**: FR 1, SR 1.1, SR 6.1
- **Detection**: Audit trail review, command logging analysis

#### Pattern: Field Device Configuration Without Audit
- **Threat**: Modify field device settings without creating audit trail
- **DFD Element**: Process (Configuration Tool) → Data Store (Device Config)
- **Attack Vector**: Direct device access, lack of logging
- **Impact**: Safety-critical changes untraced, compliance violations
- **STRIDE Category**: Repudiation + Tampering
- **Mitigation**: Configuration management, change logging, network monitoring
- **NIST Controls**: CM-3, AU-2, CM-6 (Configuration Settings)
- **IEC 62443**: SR 6.1, FR 2, SR 2.1
- **Detection**: Configuration baseline comparison, network traffic analysis

### Cloud and SaaS Repudiation

#### Pattern: Shared Cloud Credentials
- **Threat**: Multiple administrators share cloud account credentials
- **DFD Element**: External Entity (Cloud Admin) → Process (Cloud API)
- **Attack Vector**: Policy violation, convenience over security
- **Impact**: Cloud actions unattributable to individual, investigation hindrance
- **STRIDE Category**: Repudiation
- **Mitigation**: Individual IAM users, federated identity, MFA, CloudTrail
- **NIST Controls**: AC-2, IA-2, AU-2, IA-8 (Identification and Authentication)
- **IEC 62443**: FR 1, SR 1.1
- **Detection**: Policy enforcement, CloudTrail analysis, root account usage alerts

#### Pattern: API Key Sharing/Leakage
- **Threat**: API keys shared or leaked, actions unattributable to individual
- **DFD Element**: Data Flow (API Key) used by multiple actors
- **Attack Vector**: Key sharing, accidental commits, insecure storage
- **Impact**: API actions ambiguous attribution, abuse undetected
- **STRIDE Category**: Repudiation + Information Disclosure
- **Mitigation**: Individual API keys, key rotation, secret management, least privilege
- **NIST Controls**: IA-5 (Authenticator Management), AC-2, AU-2
- **IEC 62443**: FR 1, SR 1.5 (Authenticator Management)
- **Detection**: API usage anomalies, key scanning, activity monitoring

#### Pattern: Container Ephemeral Nature
- **Threat**: Containers destroyed after use, losing forensic evidence
- **DFD Element**: Process (Container) → Destruction with no Data Store persistence
- **Attack Vector**: Container orchestration design, legitimate lifecycle
- **Impact**: Activity evidence lost, incident investigation difficulty
- **STRIDE Category**: Repudiation
- **Mitigation**: Centralized logging, log forwarding before destruction, audit sidecar
- **NIST Controls**: AU-4 (Audit Storage Capacity), AU-9, AU-11
- **IEC 62443**: SR 6.1, FR 6
- **Detection**: Log collection verification, runtime security monitoring

### Compliance and Legal Repudiation

#### Pattern: Data Retention Policy Violation
- **Threat**: Delete logs/data before required retention period
- **DFD Element**: Data Store (Logs) → Premature deletion
- **Attack Vector**: Policy non-compliance, malicious destruction
- **Impact**: Legal evidence unavailable, compliance violations, fines
- **STRIDE Category**: Repudiation + Tampering
- **Mitigation**: Automated retention enforcement, immutable storage, compliance monitoring
- **NIST Controls**: AU-11, SI-12 (Information Handling), MP-6
- **IEC 62443**: SR 6.1, FR 6
- **Detection**: Retention policy audits, premature deletion alerts

#### Pattern: E-Discovery Obstruction
- **Threat**: Alter or delete documents subject to legal hold
- **DFD Element**: Data Store (Documents/Emails) under legal preservation
- **Attack Vector**: Deliberate destruction, spoliation
- **Impact**: Obstruction of justice, adverse legal inference, sanctions
- **STRIDE Category**: Repudiation + Tampering
- **Mitigation**: Legal hold automation, document preservation, access controls
- **NIST Controls**: AU-11, MP-6, SI-12
- **IEC 62443**: SR 6.1
- **Detection**: Document tracking, preservation verification, audit trails

## Cross-Framework Integration

### PASTA Stage 4: Threat Analysis
- Repudiation threats by accountability requirement
- Audit trail gap analysis
- Non-repudiation requirement identification

### PASTA Stage 7: Risk and Impact Analysis
- Business impact of attribution loss
- Compliance risk from audit gaps
- Legal liability quantification

### IEC 62443 Requirements
- FR 6: Timely Response to Events (audit logging)
- SR 6.1: Audit Log Accessibility
- SR 6.2: Continuous Monitoring
- FR 1: Identification and Authentication (attribution)

### NIST SP 800-53 Controls
- AU-2: Audit Events
- AU-9: Protection of Audit Information
- AU-10: Non-repudiation
- AU-11: Audit Record Retention
- IA-2: Identification and Authentication

## Detection Strategy

### Proactive Monitoring
- Log integrity checking
- Audit trail completeness validation
- Timestamp consistency verification
- Account activity attribution

### Reactive Investigation
- Forensic artifact collection
- Log correlation and analysis
- Timeline reconstruction
- Attribution through behavioral analysis

## Mitigation Hierarchy

### Level 1: Prevent Repudiation
- Non-repudiation mechanisms (digital signatures)
- Comprehensive logging
- Individual accountability
- Immutable audit trails

### Level 2: Detect Repudiation Attempts
- Log integrity monitoring
- Anti-forensics tool detection
- Anomaly detection
- Compliance monitoring

### Level 3: Preserve Evidence
- Centralized logging
- Write-once storage
- Retention enforcement
- Chain of custody

### Level 4: Attribution and Investigation
- Forensic capabilities
- Log correlation
- Behavioral analysis
- Legal compliance
