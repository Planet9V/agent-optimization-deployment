# STRIDE: Tampering with Data Threats

## Entity Type
THREAT_MODEL, ATTACK_VECTOR, MITIGATION

## Overview
Tampering involves malicious modification of data, whether in transit, at rest, or during processing. This includes data integrity violations, unauthorized modifications, and manipulation of system behavior through data corruption.

## Threat Patterns (200+ patterns)

### Data-in-Transit Tampering

#### Pattern: Man-in-the-Middle (MITM) Data Modification
- **Threat**: Intercept and modify data between two communicating parties
- **DFD Element**: Data Flow (Network Communication)
- **Attack Vector**: Network position, ARP poisoning, rogue Wi-Fi, DNS hijacking
- **Impact**: Transaction manipulation, credential theft, malware injection
- **STRIDE Category**: Tampering + Information Disclosure
- **Mitigation**: TLS/SSL with certificate validation, mutual authentication, certificate pinning
- **NIST Controls**: SC-8 (Transmission Confidentiality and Integrity), SC-13 (Cryptographic Protection)
- **IEC 62443**: FR 4 (Data Confidentiality), FR 3 (System Integrity)
- **Detection**: TLS certificate warnings, unexpected certificate changes, traffic analysis

#### Pattern: SSL/TLS Downgrade Attack
- **Threat**: Force connection to use weaker or no encryption
- **DFD Element**: Data Flow (Encrypted Channel Negotiation)
- **Attack Vector**: Protocol manipulation, MITM position
- **Impact**: Expose encrypted traffic, enable plaintext interception
- **STRIDE Category**: Tampering + Information Disclosure
- **Mitigation**: HSTS (HTTP Strict Transport Security), TLS version enforcement, cipher suite restrictions
- **NIST Controls**: SC-8(1), SC-13
- **IEC 62443**: FR 4.1, SR 4.1
- **Detection**: TLS version monitoring, HSTS policy violations

#### Pattern: HTTP Parameter Tampering
- **Threat**: Modify URL parameters, form data, or cookies in HTTP requests
- **DFD Element**: Data Flow (HTTP Request) → Process
- **Attack Vector**: Browser developer tools, proxy tools, automated scripts
- **Impact**: Price manipulation, privilege escalation, access control bypass
- **STRIDE Category**: Tampering + Elevation of Privilege
- **Mitigation**: Server-side validation, cryptographic signatures, session tokens, HMAC
- **NIST Controls**: SI-10 (Information Input Validation), AC-3 (Access Enforcement)
- **IEC 62443**: FR 2 (Use Control), SR 2.1
- **Detection**: Input validation failures, anomalous parameter values

#### Pattern: JSON/XML Manipulation in API Calls
- **Threat**: Modify structured data in API requests
- **DFD Element**: Data Flow (API Request Body) → Process
- **Attack Vector**: Proxy interception, API client modification
- **Impact**: Business logic bypass, unauthorized operations, data corruption
- **STRIDE Category**: Tampering
- **Mitigation**: Request signing, JSON/XML validation, schema enforcement, API gateway
- **NIST Controls**: SI-10, AC-3
- **IEC 62443**: SR 3.1 (Communication Integrity)
- **Detection**: Schema validation failures, signature verification failures

#### Pattern: Replay Attack with Modified Data
- **Threat**: Capture legitimate traffic, modify, and replay
- **DFD Element**: Data Flow → Process
- **Attack Vector**: Network capture, request replay with modifications
- **Impact**: Duplicate transactions, unauthorized operations
- **STRIDE Category**: Tampering + Spoofing
- **Mitigation**: Nonces, timestamps, sequence numbers, request signing
- **NIST Controls**: SC-23 (Session Authenticity), SC-8
- **IEC 62443**: SR 3.1, SR 1.1 (Human User Identification)
- **Detection**: Duplicate request detection, timestamp validation

### Data-at-Rest Tampering

#### Pattern: Database Direct Modification
- **Threat**: Bypass application logic to directly modify database
- **DFD Element**: Data Store (Database)
- **Attack Vector**: SQL injection, database credential compromise, privilege escalation
- **Impact**: Data corruption, fraud, audit trail manipulation
- **STRIDE Category**: Tampering + Repudiation
- **Mitigation**: Stored procedures, database access controls, audit logging, encryption
- **NIST Controls**: AC-3, AU-2 (Audit Events), SI-10
- **IEC 62443**: FR 2 (Use Control), SR 2.1
- **Detection**: Database activity monitoring, trigger-based alerts

#### Pattern: File System Tampering
- **Threat**: Modify critical files (configuration, executables, libraries)
- **DFD Element**: Data Store (File System)
- **Attack Vector**: Unauthorized file system access, privilege escalation, malware
- **Impact**: System compromise, backdoor installation, data loss
- **STRIDE Category**: Tampering + Elevation of Privilege
- **Mitigation**: File integrity monitoring (FIM), access controls, read-only mounts, code signing
- **NIST Controls**: CM-3 (Configuration Change Control), SI-7 (Software Integrity), AC-6
- **IEC 62443**: FR 3 (System Integrity), SR 3.3
- **Detection**: FIM alerts, hash verification failures

#### Pattern: Registry/Configuration Tampering (Windows)
- **Threat**: Modify Windows Registry or system configuration
- **DFD Element**: Data Store (System Registry)
- **Attack Vector**: Malware, privilege escalation, persistence mechanisms
- **Impact**: System behavior modification, security control bypass, persistence
- **STRIDE Category**: Tampering + Elevation of Privilege
- **Mitigation**: Registry permissions, FIM, group policy enforcement, least privilege
- **NIST Controls**: CM-3, CM-6 (Configuration Settings), AC-6
- **IEC 62443**: SR 3.3, FR 2
- **Detection**: Registry monitoring tools, unexpected registry changes

#### Pattern: Log File Tampering/Deletion
- **Threat**: Modify or delete audit logs to cover tracks
- **DFD Element**: Data Store (Log Files)
- **Attack Vector**: Compromised system access, privilege escalation
- **Impact**: Loss of audit trail, inability to detect/investigate incidents
- **STRIDE Category**: Tampering + Repudiation
- **Mitigation**: Centralized logging, write-once storage, log signing, SIEM
- **NIST Controls**: AU-9 (Protection of Audit Information), AU-4 (Audit Storage Capacity)
- **IEC 62443**: FR 6 (Timely Response to Events), SR 6.1
- **Detection**: Log integrity validation, missing log entries, gaps in timestamps

#### Pattern: Firmware/BIOS Tampering
- **Threat**: Modify device firmware or BIOS
- **DFD Element**: Data Store (Firmware/BIOS)
- **Attack Vector**: Physical access, firmware update mechanisms, supply chain compromise
- **Impact**: Persistent rootkit, hardware-level backdoor, recovery difficulty
- **STRIDE Category**: Tampering + Elevation of Privilege
- **Mitigation**: Secure boot, firmware signing, measured boot, TPM
- **NIST Controls**: SI-7, CM-3, SA-10 (Developer Configuration Management)
- **IEC 62443**: SR 3.3, SR 7.1 (Denial of Service Protection)
- **Detection**: Boot integrity checks, TPM measurements, firmware version validation

### Code Tampering

#### Pattern: Binary Patching/Modification
- **Threat**: Modify compiled executables or libraries
- **DFD Element**: Data Store (Executable Files)
- **Attack Vector**: File system access, malware, compromised build process
- **Impact**: Backdoor installation, malicious functionality, license bypass
- **STRIDE Category**: Tampering
- **Mitigation**: Code signing, digital signatures, hash verification, read-only storage
- **NIST Controls**: SI-7, CM-3, SA-10
- **IEC 62443**: SR 3.1, SR 3.3
- **Detection**: Signature verification, hash comparison, behavior analysis

#### Pattern: DLL Hijacking/Injection
- **Threat**: Replace legitimate DLLs or inject malicious code
- **DFD Element**: Data Store (DLL Files) → Process (Application)
- **Attack Vector**: Search order exploitation, weak file permissions
- **Impact**: Code execution in context of legitimate process, privilege escalation
- **STRIDE Category**: Tampering + Elevation of Privilege
- **Mitigation**: Application whitelisting, DLL signature verification, safe DLL search mode
- **NIST Controls**: CM-7 (Least Functionality), SI-7, AC-6
- **IEC 62443**: FR 2, SR 1.5 (Authenticator Management)
- **Detection**: DLL load monitoring, signature verification, behavioral analysis

#### Pattern: Source Code Repository Tampering
- **Threat**: Modify source code in version control
- **DFD Element**: Data Store (Source Repository)
- **Attack Vector**: Compromised credentials, insider threat, supply chain attack
- **Impact**: Malicious code introduction, backdoor insertion, IP theft
- **STRIDE Category**: Tampering + Repudiation
- **Mitigation**: Code review, commit signing, access controls, branch protection
- **NIST Controls**: CM-3, AC-2 (Account Management), SA-10
- **IEC 62443**: FR 2, SR 2.1
- **Detection**: Code review process, commit signature verification, anomaly detection

#### Pattern: Build Pipeline Injection
- **Threat**: Inject malicious code during build/compilation process
- **DFD Element**: Process (Build System) → Data Store (Build Artifacts)
- **Attack Vector**: Compromised build server, malicious dependencies, insider threat
- **Impact**: Supply chain compromise, widespread distribution of backdoors
- **STRIDE Category**: Tampering
- **Mitigation**: Build environment hardening, artifact signing, build reproducibility
- **NIST Controls**: SA-10, SA-11 (Developer Security Testing), SI-7
- **IEC 62443**: SR 3.1, FR 3
- **Detection**: Build artifact verification, dependency scanning, SBOM validation

### Memory Tampering

#### Pattern: Process Memory Injection
- **Threat**: Inject code or data into running process memory
- **DFD Element**: Process (Running Application Memory)
- **Attack Vector**: DLL injection, reflective loading, process hollowing
- **Impact**: Code execution, credential theft, security control bypass
- **STRIDE Category**: Tampering + Elevation of Privilege
- **Mitigation**: Address space layout randomization (ASLR), DEP, memory protection
- **NIST Controls**: SI-16 (Memory Protection), SC-3 (Security Function Isolation)
- **IEC 62443**: FR 3, SR 3.4 (Software Integrity)
- **Detection**: EDR solutions, memory scanning, behavioral analysis

#### Pattern: Buffer Overflow for Data Corruption
- **Threat**: Overflow buffer to overwrite adjacent memory
- **DFD Element**: Process (Memory Management)
- **Attack Vector**: Unchecked input, memory safety violations
- **Impact**: Data corruption, code execution, denial of service
- **STRIDE Category**: Tampering + Elevation of Privilege + Denial of Service
- **Mitigation**: Input validation, bounds checking, safe languages, stack canaries
- **NIST Controls**: SI-10, SI-16
- **IEC 62443**: SR 3.4, FR 3
- **Detection**: Crash dumps, anomaly detection, ASAN/memory sanitizers

#### Pattern: Use-After-Free Exploitation
- **Threat**: Access freed memory to corrupt data or control execution
- **DFD Element**: Process (Heap Memory)
- **Attack Vector**: Memory management bugs, race conditions
- **Impact**: Data corruption, arbitrary code execution
- **STRIDE Category**: Tampering + Elevation of Privilege
- **Mitigation**: Safe languages, memory sanitizers, heap protections
- **NIST Controls**: SI-16, SA-11
- **IEC 62443**: SR 3.4
- **Detection**: Memory corruption detection tools, crash analysis

### Network Protocol Tampering

#### Pattern: TCP Sequence Number Manipulation
- **Threat**: Inject or modify TCP packets by predicting sequence numbers
- **DFD Element**: Data Flow (TCP Stream)
- **Attack Vector**: Sequence number prediction, MITM position
- **Impact**: Connection hijacking, data injection, session termination
- **STRIDE Category**: Tampering + Denial of Service
- **Mitigation**: Randomized sequence numbers, TCP authentication option, IPsec
- **NIST Controls**: SC-8, SC-23
- **IEC 62443**: FR 3, FR 5 (Restricted Data Flow)
- **Detection**: Sequence number anomalies, unexpected RST packets

#### Pattern: ICMP Packet Manipulation
- **Threat**: Inject or modify ICMP packets (redirects, unreachable, etc.)
- **DFD Element**: Data Flow (Network Layer)
- **Attack Vector**: Network position, packet injection
- **Impact**: Routing manipulation, connection disruption, path MTU attacks
- **STRIDE Category**: Tampering + Denial of Service
- **Mitigation**: ICMP filtering, rate limiting, disable ICMP redirects
- **NIST Controls**: SC-7 (Boundary Protection), CM-6
- **IEC 62443**: FR 5, SR 5.1
- **Detection**: ICMP monitoring, unexpected routing changes

#### Pattern: HTTP Response Splitting
- **Threat**: Inject CRLF to split HTTP response into multiple responses
- **DFD Element**: Data Flow (HTTP Response) → Process
- **Attack Vector**: Unsanitized input in HTTP headers
- **Impact**: Web cache poisoning, XSS, session hijacking
- **STRIDE Category**: Tampering + Information Disclosure
- **Mitigation**: Input validation, output encoding, framework protections
- **NIST Controls**: SI-10, SC-8
- **IEC 62443**: FR 3, SR 3.1
- **Detection**: CRLF in response headers, unexpected response structure

#### Pattern: DNS Response Modification
- **Threat**: Modify DNS responses in transit
- **DFD Element**: Data Flow (DNS Response)
- **Attack Vector**: MITM, network position, cache poisoning
- **Impact**: Traffic redirection, phishing, malware distribution
- **STRIDE Category**: Tampering + Spoofing
- **Mitigation**: DNSSEC, DoH/DoT, response validation
- **NIST Controls**: SC-20 (Secure Name/Address Resolution), SC-21
- **IEC 62443**: FR 3, SR 3.1
- **Detection**: DNSSEC validation failures, unexpected DNS responses

### Application Logic Tampering

#### Pattern: Business Logic Bypass through Parameter Manipulation
- **Threat**: Manipulate application parameters to bypass business rules
- **DFD Element**: Process (Business Logic) input validation
- **Attack Vector**: Direct parameter modification
- **Impact**: Price manipulation, workflow bypass, unauthorized discounts
- **STRIDE Category**: Tampering
- **Mitigation**: Server-side validation, state management, transaction signing
- **NIST Controls**: SI-10, AC-3
- **IEC 62443**: FR 2, SR 2.1
- **Detection**: Anomalous transaction patterns, business rule violations

#### Pattern: Race Condition Exploitation (TOCTOU)
- **Threat**: Exploit time gap between check and use to tamper with data
- **DFD Element**: Process (Time-dependent operations)
- **Attack Vector**: Concurrent modification
- **Impact**: Privilege escalation, data corruption, security bypass
- **STRIDE Category**: Tampering + Elevation of Privilege
- **Mitigation**: Atomic operations, locking mechanisms, immutable data
- **NIST Controls**: SC-3, AC-3
- **IEC 62443**: FR 3, SR 3.5 (Input Validation)
- **Detection**: Concurrency monitoring, audit log analysis

#### Pattern: State Machine Manipulation
- **Threat**: Force application into invalid state through improper sequence
- **DFD Element**: Process (State Management)
- **Attack Vector**: Out-of-order requests, state parameter tampering
- **Impact**: Workflow bypass, unauthorized access, data inconsistency
- **STRIDE Category**: Tampering
- **Mitigation**: Server-side state validation, state tokens, workflow enforcement
- **NIST Controls**: AC-3, SI-10
- **IEC 62443**: FR 2, SR 2.1
- **Detection**: State transition monitoring, workflow violation alerts

#### Pattern: Cookie Tampering
- **Threat**: Modify cookie values to alter application behavior
- **DFD Element**: Data Flow (HTTP Cookie) → Process
- **Attack Vector**: Browser developer tools, proxy manipulation
- **Impact**: Session hijacking, privilege escalation, price manipulation
- **STRIDE Category**: Tampering + Elevation of Privilege
- **Mitigation**: Signed cookies, encrypted cookies, server-side session storage
- **NIST Controls**: SC-8, AC-3
- **IEC 62443**: FR 4, SR 4.2
- **Detection**: Cookie signature validation, anomalous cookie values

### Cryptographic Tampering

#### Pattern: Hash Collision Attack
- **Threat**: Create different inputs with same hash value
- **DFD Element**: Process (Hash Function)
- **Attack Vector**: Weak hash algorithms (MD5, SHA-1)
- **Impact**: Digital signature forgery, integrity check bypass
- **STRIDE Category**: Tampering + Repudiation
- **Mitigation**: Use SHA-256 or stronger, HMAC for authentication
- **NIST Controls**: SC-13, SC-12 (Cryptographic Key Establishment)
- **IEC 62443**: SR 4.3 (Use of Cryptography)
- **Detection**: Algorithm monitoring, collision detection

#### Pattern: Cipher Block Chaining (CBC) Padding Oracle
- **Threat**: Manipulate ciphertext to decrypt data through error messages
- **DFD Element**: Data Flow (Encrypted Data) → Process (Decryption)
- **Attack Vector**: Padding error observation
- **Impact**: Data decryption, plaintext recovery
- **STRIDE Category**: Tampering + Information Disclosure
- **Mitigation**: Authenticated encryption (GCM), constant-time operations
- **NIST Controls**: SC-13, SC-8
- **IEC 62443**: FR 4, SR 4.3
- **Detection**: Unusual decryption error patterns

#### Pattern: Public Key Infrastructure (PKI) Certificate Manipulation
- **Threat**: Tamper with certificate fields or chain of trust
- **DFD Element**: Data Store (Certificate) → Process (Validation)
- **Attack Vector**: Compromised CA, certificate substitution
- **Impact**: MITM, impersonation, unauthorized access
- **STRIDE Category**: Tampering + Spoofing
- **Mitigation**: Certificate pinning, certificate transparency, OCSP stapling
- **NIST Controls**: IA-5(2) (PKI-based Authentication), SC-17
- **IEC 62443**: SR 1.7 (Strength of Authenticators)
- **Detection**: CT log monitoring, certificate pinning violations

### Industrial Control System (ICS) Tampering

#### Pattern: PLC Logic Modification
- **Threat**: Modify programmable logic controller code or configuration
- **DFD Element**: Data Store (PLC Logic) → Process (ICS Operation)
- **Attack Vector**: Engineering workstation compromise, network access
- **Impact**: Process disruption, equipment damage, safety hazards
- **STRIDE Category**: Tampering + Denial of Service
- **Mitigation**: Code signing, change management, access controls, network segmentation
- **NIST Controls**: CM-3, AC-3, SC-7
- **IEC 62443**: SR 3.1, SR 3.3, FR 2
- **Detection**: Logic comparison, change detection, anomalous process behavior

#### Pattern: SCADA Command Injection
- **Threat**: Inject or modify SCADA commands to industrial equipment
- **DFD Element**: Data Flow (SCADA Commands) → Process (Field Devices)
- **Attack Vector**: Protocol vulnerabilities, network access
- **Impact**: Process manipulation, equipment damage, safety incidents
- **STRIDE Category**: Tampering
- **Mitigation**: Protocol security, command authentication, network segmentation
- **NIST Controls**: SC-8, AC-3, SC-7
- **IEC 62443**: SR 3.1, FR 5, SR 5.1
- **Detection**: Command monitoring, protocol analysis, behavioral anomalies

#### Pattern: Sensor Data Manipulation
- **Threat**: Tamper with sensor readings to hide or create false conditions
- **DFD Element**: Data Flow (Sensor Data) → Process (Control Logic)
- **Attack Vector**: Network MITM, sensor compromise, wireless interception
- **Impact**: Incorrect control decisions, safety hazards, process optimization failure
- **STRIDE Category**: Tampering + Information Disclosure
- **Mitigation**: Sensor authentication, encrypted communications, redundant sensors
- **NIST Controls**: SC-8, IA-3 (Device Identification), SC-23
- **IEC 62443**: FR 4, SR 4.1, FR 3
- **Detection**: Sensor validation, cross-sensor correlation, anomaly detection

#### Pattern: HMI Display Tampering
- **Threat**: Modify HMI displays to show false information to operators
- **DFD Element**: Process (HMI) → External Entity (Operator)
- **Attack Vector**: HMI compromise, network MITM
- **Impact**: Operator misinformation, incorrect decisions, safety incidents
- **STRIDE Category**: Tampering + Information Disclosure
- **Mitigation**: HMI integrity monitoring, secure communications, operator training
- **NIST Controls**: SI-7, SC-8, AT-3 (Role-based Training)
- **IEC 62443**: SR 3.3, FR 4, FR 6
- **Detection**: Display consistency checks, operator verification procedures

### Cloud and Virtualization Tampering

#### Pattern: VM Image Tampering
- **Threat**: Modify virtual machine images before deployment
- **DFD Element**: Data Store (VM Images)
- **Attack Vector**: Image repository compromise, supply chain attack
- **Impact**: Backdoored infrastructure, persistent compromise
- **STRIDE Category**: Tampering
- **Mitigation**: Image signing, hash verification, trusted image sources
- **NIST Controls**: CM-3, SI-7, SA-12 (Supply Chain Protection)
- **IEC 62443**: SR 3.3, FR 3
- **Detection**: Image signature verification, baseline comparison

#### Pattern: Container Image Manipulation
- **Threat**: Inject malicious code into container images
- **DFD Element**: Data Store (Container Registry) → Process (Container Runtime)
- **Attack Vector**: Registry compromise, build pipeline injection
- **Impact**: Compromised containerized applications, lateral movement
- **STRIDE Category**: Tampering
- **Mitigation**: Image scanning, content trust, signed images, private registries
- **NIST Controls**: SA-10, SI-7, CM-3
- **IEC 62443**: SR 3.1, SR 3.3
- **Detection**: Image vulnerability scanning, signature verification

#### Pattern: Hypervisor Memory Tampering
- **Threat**: Modify VM memory from hypervisor level
- **DFD Element**: Process (Hypervisor) → Process (Guest VM)
- **Attack Vector**: Hypervisor compromise, privileged access
- **Impact**: Guest VM compromise, data theft, code injection
- **STRIDE Category**: Tampering + Elevation of Privilege
- **Mitigation**: Hypervisor hardening, secure boot, memory encryption
- **NIST Controls**: SC-3, SI-16, AC-6
- **IEC 62443**: FR 3, SR 3.4
- **Detection**: VM introspection, memory integrity monitoring

#### Pattern: Metadata Service Manipulation
- **Threat**: Tamper with cloud instance metadata service
- **DFD Element**: Process (Metadata Service) → Process (Instance)
- **Attack Vector**: SSRF, network access from compromised instance
- **Impact**: Credential theft, privilege escalation, lateral movement
- **STRIDE Category**: Tampering + Elevation of Privilege
- **Mitigation**: IMDSv2 (token-based), network restrictions, least privilege
- **NIST Controls**: AC-6, SC-7, IA-5
- **IEC 62443**: FR 2, SR 2.1
- **Detection**: Metadata access monitoring, anomalous queries

### Supply Chain Tampering

#### Pattern: Third-Party Component Modification
- **Threat**: Tamper with open-source or commercial components
- **DFD Element**: Data Store (Dependency Repository) → Process (Build)
- **Attack Vector**: Package repository compromise, typosquatting
- **Impact**: Supply chain compromise, widespread backdoor distribution
- **STRIDE Category**: Tampering
- **Mitigation**: Dependency pinning, checksum verification, private mirrors, SBOM
- **NIST Controls**: SA-12, SR-4 (Provenance), SR-3 (Supply Chain Controls)
- **IEC 62443**: SR 3.1, FR 3
- **Detection**: Dependency scanning, checksum validation, behavioral analysis

#### Pattern: Hardware Tampering in Supply Chain
- **Threat**: Modify hardware during manufacturing or shipping
- **DFD Element**: External Entity (Hardware Supplier) → Data Store (Hardware)
- **Attack Vector**: Supply chain interdiction, malicious insider
- **Impact**: Hardware backdoor, persistent compromise, difficult detection
- **STRIDE Category**: Tampering
- **Mitigation**: Trusted suppliers, tamper-evident packaging, hardware verification
- **NIST Controls**: SA-12, SR-9 (Tamper Resistance), SR-11 (Component Authenticity)
- **IEC 62443**: SR 3.3, FR 3
- **Detection**: Hardware inspection, boot integrity checks, behavioral anomalies

#### Pattern: Software Update Tampering
- **Threat**: Compromise software update mechanism to distribute malicious updates
- **DFD Element**: Process (Update Mechanism) → Data Store (Installed Software)
- **Attack Vector**: Update server compromise, MITM, DNS hijacking
- **Impact**: Widespread compromise, persistent backdoor, difficult remediation
- **STRIDE Category**: Tampering
- **Mitigation**: Code signing, secure update channels, certificate pinning
- **NIST Controls**: SI-7, SC-8, CM-3
- **IEC 62443**: SR 3.1, SR 3.3
- **Detection**: Signature verification, update source validation

## Cross-Framework Integration

### PASTA Stage 4 (Threat Analysis)
- Tampering threat scenarios by asset class
- Attack tree development for tampering paths
- Threat likelihood assessment

### PASTA Stage 6 (Attack Modeling)
- Tampering attack chain construction
- Proof-of-concept tampering scenarios
- Attack surface analysis for data integrity

### IEC 62443 Requirements
- FR 3: System Integrity (primary)
- SR 3.1: Communication Integrity
- SR 3.3: Integrity of Transmitted Information
- SR 3.4: Software Integrity
- SR 3.5: Input Validation

### NIST SP 800-53 Controls
- SI-7: Software, Firmware, and Information Integrity
- CM-3: Configuration Change Control
- SC-8: Transmission Confidentiality and Integrity
- SI-10: Information Input Validation
- AU-9: Protection of Audit Information

## Detection Strategy

### Signature-Based Detection
- File integrity monitoring (FIM)
- Hash verification
- Digital signature validation
- Known tampering patterns

### Anomaly-Based Detection
- Behavioral analysis
- Statistical deviation
- Machine learning models
- Baseline comparison

### Integrity Verification
- Cryptographic checksums
- Merkle trees
- Blockchain for audit logs
- Trusted Platform Module (TPM)

## Mitigation Hierarchy

### Level 1: Prevent Tampering
- Input validation
- Access controls
- Encryption
- Code signing
- Immutable infrastructure

### Level 2: Detect Tampering
- File integrity monitoring
- Database triggers
- Network traffic analysis
- Audit logging
- SIEM correlation

### Level 3: Limit Impact
- Least privilege
- Segmentation
- Backup and versioning
- Transaction rollback
- Fail-safe defaults

### Level 4: Respond and Recover
- Incident response
- Forensics
- Restore from known-good
- Root cause analysis
- Lessons learned
