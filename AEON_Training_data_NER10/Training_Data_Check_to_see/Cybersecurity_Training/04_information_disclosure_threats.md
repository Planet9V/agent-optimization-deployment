# STRIDE: Information Disclosure Threats

## Entity Type
THREAT_MODEL, ATTACK_VECTOR, MITIGATION

## Overview
Information Disclosure involves unauthorized exposure of sensitive data. This includes confidentiality violations, data leakage, eavesdropping, unintended information exposure, and privacy breaches.

## Threat Patterns (250+ patterns)

### Network Eavesdropping and Interception

#### Pattern: Unencrypted Wi-Fi Sniffing
- **Threat**: Capture cleartext traffic on open/WEP Wi-Fi networks
- **DFD Element**: Data Flow (Wireless Network Traffic)
- **Attack Vector**: Packet capture tools (Wireshark, tcpdump, airodump-ng)
- **Impact**: Credential theft, session hijacking, sensitive data exposure
- **STRIDE Category**: Information Disclosure
- **Mitigation**: WPA3, 802.1X authentication, VPN, TLS/SSL for applications
- **NIST Controls**: SC-8 (Transmission Confidentiality), AC-18 (Wireless Access)
- **IEC 62443**: FR 4 (Data Confidentiality), SR 4.1 (Communication Confidentiality)
- **Detection**: Rogue AP detection, network monitoring, traffic analysis

#### Pattern: DNS Query Leakage
- **Threat**: DNS queries reveal browsing history and internal infrastructure
- **DFD Element**: Data Flow (DNS Queries) from clients
- **Attack Vector**: Unencrypted DNS, passive monitoring, DNS server logs
- **Impact**: Intelligence gathering, privacy violation, internal network mapping
- **STRIDE Category**: Information Disclosure
- **Mitigation**: DNS over HTTPS (DoH), DNS over TLS (DoT), encrypted DNS, split-horizon
- **NIST Controls**: SC-8(1), SC-20 (Secure Name Resolution)
- **IEC 62443**: FR 4, SR 4.1
- **Detection**: DNS traffic monitoring, privacy policy compliance

#### Pattern: TLS/SSL Downgrade and Interception
- **Threat**: Force downgrade to weak ciphers or plaintext for MITM
- **DFD Element**: Data Flow (TLS Negotiation) between entities
- **Attack Vector**: MITM position, protocol manipulation, cipher suite downgrade
- **Impact**: Encrypted traffic decryption, credential theft, data exposure
- **STRIDE Category**: Information Disclosure + Tampering
- **Mitigation**: HSTS, TLS 1.3 minimum, strong cipher suites, certificate pinning
- **NIST Controls**: SC-8, SC-13 (Cryptographic Protection), SC-23
- **IEC 62443**: SR 4.3 (Use of Cryptography), FR 4
- **Detection**: TLS version monitoring, certificate validation alerts

#### Pattern: BGP Hijacking for Traffic Interception
- **Threat**: Announce false BGP routes to redirect traffic for inspection
- **DFD Element**: Data Flow (Internet Routing) manipulation
- **Attack Vector**: BGP trust model, route announcement
- **Impact**: Large-scale traffic interception, state-level surveillance
- **STRIDE Category**: Information Disclosure + Spoofing
- **Mitigation**: RPKI, BGP route filtering, end-to-end encryption, certificate validation
- **NIST Controls**: SC-7 (Boundary Protection), SC-8
- **IEC 62443**: FR 5 (Restricted Data Flow), FR 4
- **Detection**: BGP monitoring, route anomaly detection, latency changes

#### Pattern: VPN Traffic Correlation Attack
- **Threat**: Correlate encrypted VPN traffic patterns to identify users/activity
- **DFD Element**: Data Flow (VPN Encrypted Traffic) metadata
- **Attack Vector**: Traffic analysis, timing analysis, packet size patterns
- **Impact**: User de-anonymization, activity profiling despite encryption
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Traffic padding, constant-rate tunnels, onion routing, obfuscation
- **NIST Controls**: SC-8, SC-12 (Cryptographic Key Management)
- **IEC 62443**: FR 4, SR 4.1
- **Detection**: Statistical traffic analysis (defender must implement countermeasures)

### Application-Level Information Disclosure

#### Pattern: SQL Injection for Data Exfiltration
- **Threat**: Extract database contents through SQL injection vulnerabilities
- **DFD Element**: Data Store (Database) ← Process (Web Application)
- **Attack Vector**: Unsanitized user input in SQL queries
- **Impact**: Entire database exposure, customer data breach, credential theft
- **STRIDE Category**: Information Disclosure + Tampering
- **Mitigation**: Parameterized queries, ORMs, input validation, least privilege DB accounts
- **NIST Controls**: SI-10 (Input Validation), AC-6 (Least Privilege), SC-8
- **IEC 62443**: SR 3.5 (Input Validation), FR 2 (Use Control)
- **Detection**: WAF, database activity monitoring, anomalous query detection

#### Pattern: Directory Traversal/Path Traversal
- **Threat**: Access files outside intended directory using ../ sequences
- **DFD Element**: Data Store (File System) ← Process (Web Application)
- **Attack Vector**: Unvalidated file path parameters
- **Impact**: Configuration file exposure, source code disclosure, credential files
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Input validation, chroot jails, canonicalization, allowlisting
- **NIST Controls**: SI-10, AC-3 (Access Enforcement), CM-6
- **IEC 62443**: SR 3.5, FR 2
- **Detection**: WAF rules, file access monitoring, anomalous path patterns

#### Pattern: Insecure Direct Object Reference (IDOR)
- **Threat**: Access other users' data by manipulating object IDs
- **DFD Element**: Process (Application) → Data Store (User Data)
- **Attack Vector**: Predictable IDs, insufficient authorization checks
- **Impact**: Unauthorized data access, privacy breach, account information exposure
- **STRIDE Category**: Information Disclosure + Elevation of Privilege
- **Mitigation**: Indirect references, authorization checks, UUIDs, access control enforcement
- **NIST Controls**: AC-3, AC-6, SI-10
- **IEC 62443**: FR 2, SR 2.1 (Authorization Enforcement)
- **Detection**: Anomalous data access patterns, authorization failure monitoring

#### Pattern: API Excessive Data Exposure
- **Threat**: API returns more data than UI needs (mobile/web client filtering)
- **DFD Element**: Process (API) → Data Flow (API Response)
- **Attack Vector**: Over-privileged API endpoints, lazy filtering
- **Impact**: Sensitive data exposure, privacy violations, reconnaissance data
- **STRIDE Category**: Information Disclosure
- **Mitigation**: API field filtering, DTO patterns, principle of least privilege, GraphQL field-level auth
- **NIST Controls**: AC-6, SC-8, AC-3
- **IEC 62443**: FR 2, SR 2.1
- **Detection**: API response analysis, data minimization audits

#### Pattern: Mass Assignment Vulnerability
- **Threat**: Modify internal object properties through API parameter injection
- **DFD Element**: Process (API) parameter binding → Data Store
- **Attack Vector**: Unprotected object binding, lack of allowlisting
- **Impact**: Information disclosure via error messages, privilege escalation, data corruption
- **STRIDE Category**: Information Disclosure + Tampering
- **Mitigation**: Allowlist parameters, DTOs, disable auto-binding, explicit mapping
- **NIST Controls**: SI-10, AC-3
- **IEC 62443**: SR 3.5, FR 2
- **Detection**: Parameter anomaly detection, unexpected field modifications

### Error Disclosure and Information Leakage

#### Pattern: Verbose Error Messages
- **Threat**: Detailed error messages reveal system internals, stack traces, SQL queries
- **DFD Element**: Process (Error Handling) → Data Flow (Error Response)
- **Attack Vector**: Exception handling exposing sensitive details
- **Impact**: Database structure disclosure, framework version exposure, internal paths
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Generic error messages, centralized error handling, logging sensitive details securely
- **NIST Controls**: SI-11 (Error Handling), AU-2 (Audit Events)
- **IEC 62443**: FR 2, SR 3.5
- **Detection**: Error message monitoring, security testing for verbose errors

#### Pattern: Stack Trace Exposure
- **Threat**: Stack traces reveal code structure, library versions, internal logic
- **DFD Element**: Process (Exception) → External Entity (User/Attacker)
- **Attack Vector**: Unhandled exceptions, debug mode in production
- **Impact**: Reconnaissance, vulnerability identification, architecture disclosure
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Custom error pages, disable debug mode, error logging only
- **NIST Controls**: SI-11, CM-6 (Configuration Settings)
- **IEC 62443**: FR 2, SR 3.5
- **Detection**: Production configuration audits, error output monitoring

#### Pattern: Debug Endpoints in Production
- **Threat**: Exposed debug/admin endpoints reveal sensitive information
- **DFD Element**: Process (Debug Interface) accessible in production
- **Attack Vector**: Forgotten debug code, misconfiguration
- **Impact**: System information disclosure, configuration exposure, code execution
- **STRIDE Category**: Information Disclosure + Elevation of Privilege
- **Mitigation**: Remove debug code in production, feature flags, environment-specific builds
- **NIST Controls**: CM-7 (Least Functionality), SI-11, CM-6
- **IEC 62443**: FR 2, SR 2.1
- **Detection**: Endpoint scanning, production configuration audits

#### Pattern: Commented-Out Sensitive Code
- **Threat**: Sensitive information in source code comments deployed to production
- **DFD Element**: Data Store (Source Code) comments
- **Attack Vector**: Source code disclosure, accidental commits
- **Impact**: Credential exposure, API key leakage, business logic disclosure
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Code review, secret scanning, .gitignore, pre-commit hooks
- **NIST Controls**: SA-15 (Development Process), CM-3
- **IEC 62443**: SR 1.5, FR 2
- **Detection**: Secret scanning tools, code review, SAST

### File and Directory Exposure

#### Pattern: Directory Listing Enabled
- **Threat**: Web server exposes directory contents when index file missing
- **DFD Element**: Data Store (Web Directory) → External Entity
- **Attack Vector**: Misconfigured web server
- **Impact**: File structure disclosure, backup file discovery, reconnaissance
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Disable directory listing, ensure index files, access controls
- **NIST Controls**: CM-6, CM-7, AC-3
- **IEC 62443**: FR 2, SR 2.1
- **Detection**: Web server configuration audits, vulnerability scanning

#### Pattern: Backup File Exposure (.bak, .old, ~)
- **Threat**: Backup files with sensitive content accessible via web
- **DFD Element**: Data Store (Backup Files) accessible via Data Flow (HTTP)
- **Attack Vector**: Predictable filenames, no access restrictions
- **Impact**: Source code disclosure, configuration exposure, old credentials
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Exclude backup files from web root, file extension filtering, proper storage
- **NIST Controls**: CM-6, MP-6 (Media Sanitization), AC-3
- **IEC 62443**: FR 2, CM-6
- **Detection**: File discovery scanning, web configuration audits

#### Pattern: .git Directory Exposure
- **Threat**: Exposed .git directory allows repository reconstruction
- **DFD Element**: Data Store (.git metadata) accessible via HTTP
- **Attack Vector**: Forgotten .git in deployed code, misconfigured web server
- **Impact**: Complete source code history, commit messages, developer info, credentials
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Exclude .git from deployment, web server rules, static site generation
- **NIST Controls**: SA-15, CM-3, AC-3
- **IEC 62443**: FR 2, SR 2.1
- **Detection**: .git scanning tools, deployment audits

#### Pattern: Cloud Storage Bucket Exposure (S3, Blob)
- **Threat**: Publicly accessible cloud storage buckets with sensitive data
- **DFD Element**: Data Store (Cloud Bucket) with public read permissions
- **Attack Vector**: Misconfigured bucket permissions, lack of access controls
- **Impact**: Customer data breach, intellectual property exposure, credential files
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Private by default, bucket policies, access logging, encryption, IAM controls
- **NIST Controls**: AC-3, AC-6, SC-28 (Protection of Information at Rest)
- **IEC 62443**: FR 2, FR 4, SR 4.2
- **Detection**: Bucket permission audits, cloud security posture management (CSPM)

### Credential and Secret Disclosure

#### Pattern: Hardcoded Credentials in Source Code
- **Threat**: Passwords, API keys hardcoded in source files
- **DFD Element**: Data Store (Source Code) contains secrets
- **Attack Vector**: Source code access, repository exposure, decompilation
- **Impact**: Authentication bypass, unauthorized access, privilege escalation
- **STRIDE Category**: Information Disclosure + Elevation of Privilege
- **Mitigation**: Environment variables, secret management (Vault, KMS), secret scanning
- **NIST Controls**: IA-5 (Authenticator Management), SC-12 (Cryptographic Keys)
- **IEC 62443**: SR 1.5 (Authenticator Management), FR 4
- **Detection**: Secret scanning (git-secrets, TruffleHog), code review

#### Pattern: API Keys in Client-Side Code
- **Threat**: API keys exposed in JavaScript, mobile apps, or public repositories
- **DFD Element**: Data Flow (Client-Side Code) contains secrets
- **Attack Vector**: Browser developer tools, app decompilation, source inspection
- **Impact**: API abuse, quota exhaustion, unauthorized operations
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Backend proxy, restricted API keys, key rotation, usage monitoring
- **NIST Controls**: IA-5, SC-12, AC-6
- **IEC 62443**: SR 1.5, FR 2
- **Detection**: Client-side code review, API usage monitoring, quota alerts

#### Pattern: Environment Variables in Error Messages
- **Threat**: Error pages or logs expose environment variable values
- **DFD Element**: Process (Error Handler) → Data Flow (Error Output)
- **Attack Vector**: Exception handling, logging verbosity
- **Impact**: Database connection strings, API keys, internal URLs exposed
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Sanitize error output, secure logging, redact sensitive variables
- **NIST Controls**: SI-11, AU-9 (Audit Info Protection)
- **IEC 62443**: FR 2, SR 6.1
- **Detection**: Log review, error message monitoring

#### Pattern: Password in URL Parameters
- **Threat**: Passwords transmitted in URL query strings or path
- **DFD Element**: Data Flow (URL) contains password
- **Attack Vector**: Logged in web server logs, browser history, referrer headers
- **Impact**: Password exposure in logs, proxies, browser history
- **STRIDE Category**: Information Disclosure
- **Mitigation**: POST requests for credentials, never URL parameters, proper authentication
- **NIST Controls**: IA-5, SC-8, AU-9
- **IEC 62443**: SR 1.5, FR 4
- **Detection**: URL parameter audits, web server log analysis

### Memory and Process Disclosure

#### Pattern: Core Dump Exposure
- **Threat**: Core dumps contain process memory including sensitive data
- **DFD Element**: Data Store (Core Dump Files) created from Process memory
- **Attack Vector**: Application crashes, segmentation faults
- **Impact**: Credential exposure, encryption key disclosure, sensitive data in memory
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Disable core dumps in production, encrypt core dumps, secure storage, least privilege access
- **NIST Controls**: SI-16 (Memory Protection), AC-6, MP-6
- **IEC 62443**: FR 4, SR 4.2
- **Detection**: Core dump monitoring, file creation alerts, forensic analysis

#### Pattern: Swap File/Pagefile Analysis
- **Threat**: Sensitive data written to swap/page files persists on disk
- **DFD Element**: Data Store (Swap File) contains Process memory
- **Attack Vector**: System compromise, physical access, forensic analysis
- **Impact**: Credential recovery, encryption key exposure, sensitive data disclosure
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Encrypted swap, disable swap for sensitive apps, memory locking (mlock)
- **NIST Controls**: SC-28 (Protection of Information at Rest), SI-16
- **IEC 62443**: FR 4, SR 4.2
- **Detection**: Swap encryption verification, memory protection audits

#### Pattern: Process Memory Dumping
- **Threat**: Dump running process memory to extract secrets
- **DFD Element**: Process (Running Application) memory
- **Attack Vector**: Debug tools, DLL injection, memory dumpers
- **Impact**: Plaintext credentials, session tokens, encryption keys in memory
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Memory encryption, anti-debugging, credential guard, minimal secrets in memory
- **NIST Controls**: SI-16, SC-12, AC-6
- **IEC 62443**: FR 4, SR 3.4 (Software Integrity)
- **Detection**: Memory access monitoring, EDR solutions

#### Pattern: Browser Password Manager Extraction
- **Threat**: Extract saved passwords from browser password managers
- **DFD Element**: Data Store (Browser Credential Store)
- **Attack Vector**: Malware, physical access, weak OS authentication
- **Impact**: Mass credential exposure, account takeover
- **STRIDE Category**: Information Disclosure + Elevation of Privilege
- **Mitigation**: OS credential protection (Credential Guard), enterprise password manager, MFA
- **NIST Controls**: IA-5, AC-6, SC-28
- **IEC 62443**: SR 1.5, FR 4
- **Detection**: Credential access monitoring, EDR alerts

### Cloud and Virtualization Disclosure

#### Pattern: Cloud Metadata Service Exploitation (SSRF)
- **Threat**: Access cloud instance metadata via SSRF to steal credentials
- **DFD Element**: Process (Web App) → External Entity (Cloud Metadata Service)
- **Attack Vector**: SSRF vulnerability, unvalidated URL parameters
- **Impact**: IAM role credentials, instance metadata, user data scripts
- **STRIDE Category**: Information Disclosure + Elevation of Privilege
- **Mitigation**: IMDSv2 (token-based), network restrictions, input validation, SSRF protection
- **NIST Controls**: SI-10, AC-6, SC-7
- **IEC 62443**: SR 3.5, FR 2, FR 5
- **Detection**: Metadata service access monitoring, SSRF detection

#### Pattern: VM Snapshot Data Extraction
- **Threat**: Extract sensitive data from VM snapshots or backups
- **DFD Element**: Data Store (VM Snapshot) contains Process/Data Store contents
- **Attack Vector**: Snapshot access, backup compromise, cloud storage exposure
- **Impact**: Complete system state disclosure, data breach, credential exposure
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Snapshot encryption, access controls, snapshot lifecycle management
- **NIST Controls**: SC-28, AC-3, MP-6
- **IEC 62443**: FR 4, SR 4.2
- **Detection**: Snapshot access monitoring, unusual snapshot activities

#### Pattern: Container Image Layer Secrets
- **Threat**: Secrets embedded in container image layers persist even if deleted
- **DFD Element**: Data Store (Container Image Layers)
- **Attack Vector**: Container image analysis, registry access
- **Impact**: Credential exposure, API key leakage across image history
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Multi-stage builds, secret mounting at runtime, image scanning, minimalist images
- **NIST Controls**: SA-15, SC-28, IA-5
- **IEC 62443**: SR 1.5, FR 4
- **Detection**: Image scanning tools, secret detection in layers

### Side-Channel Attacks

#### Pattern: Timing Attack on Cryptographic Operations
- **Threat**: Infer secret keys through execution time variations
- **DFD Element**: Process (Cryptographic Function) timing behavior
- **Attack Vector**: Precise timing measurements, statistical analysis
- **Impact**: Encryption key recovery, authentication bypass
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Constant-time algorithms, timing attack-resistant implementations
- **NIST Controls**: SC-13, SC-12, SI-16
- **IEC 62443**: SR 4.3 (Use of Cryptography), FR 4
- **Detection**: Difficult to detect; mitigation is primary defense

#### Pattern: Cache Timing Attack (Spectre/Meltdown)
- **Threat**: Exploit CPU speculative execution to read arbitrary memory
- **DFD Element**: Process memory disclosure via CPU cache side-channel
- **Attack Vector**: Crafted code exploiting speculative execution
- **Impact**: Cross-process memory disclosure, kernel memory read, encryption key exposure
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Microcode updates, OS patches, hardware mitigations, isolation
- **NIST Controls**: SI-16, SC-3 (Security Function Isolation), CM-6
- **IEC 62443**: FR 4, SR 3.4
- **Detection**: Behavioral detection, anomaly detection (mitigations primary defense)

#### Pattern: Power Analysis Attack
- **Threat**: Analyze power consumption to extract cryptographic keys
- **DFD Element**: Process (Hardware Cryptographic Operation) power signature
- **Attack Vector**: Physical proximity, power measurement equipment
- **Impact**: Encryption key recovery from smartcards, HSMs, embedded devices
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Power analysis-resistant hardware, randomized operations, noise injection
- **NIST Controls**: SC-13, PE-3 (Physical Access Control)
- **IEC 62443**: SR 4.3, FR 4, PE-3
- **Detection**: Tamper-evident hardware, environmental monitoring

#### Pattern: Acoustic Cryptanalysis
- **Threat**: Extract encryption keys from sounds emitted during cryptographic operations
- **DFD Element**: Process (Hardware Cryptographic Operation) acoustic signature
- **Attack Vector**: Audio recording, signal processing
- **Impact**: RSA key extraction from laptop sounds, printer eavesdropping
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Acoustic shielding, constant-time operations, secure facilities
- **NIST Controls**: SC-13, PE-3, PE-5 (Access Control for Output Devices)
- **IEC 62443**: FR 4, PE-3
- **Detection**: Environmental monitoring, physical security

### ICS/SCADA Information Disclosure

#### Pattern: PLC Program Download
- **Threat**: Extract PLC logic programs revealing industrial processes
- **DFD Element**: Data Store (PLC Program) → External Entity
- **Attack Vector**: Engineering software, network access, default credentials
- **Impact**: Intellectual property theft, process understanding for targeted attacks
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Network segmentation, authentication, access controls, encryption
- **NIST Controls**: AC-3, SC-8, IA-2
- **IEC 62443**: FR 2, FR 4, SR 1.1, SR 4.1
- **Detection**: PLC access monitoring, program upload/download logging

#### Pattern: SCADA Protocol Eavesdropping (Modbus, DNP3)
- **Threat**: Intercept unencrypted industrial protocol traffic
- **DFD Element**: Data Flow (SCADA Protocol) in cleartext
- **Attack Vector**: Network tap, span port, compromised network device
- **Impact**: Process state disclosure, setpoint values, device identification
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Protocol encryption (TLS for Modbus, DNP3 Secure Authentication), network segmentation
- **NIST Controls**: SC-8, SC-7, AC-4 (Information Flow Enforcement)
- **IEC 62443**: FR 4, FR 5, SR 4.1, SR 5.1
- **Detection**: Network traffic analysis, unexpected traffic patterns

#### Pattern: HMI Screen Capture/Shoulder Surfing
- **Threat**: Capture HMI display showing sensitive process information
- **DFD Element**: Process (HMI Display) → External Entity (Observer)
- **Attack Vector**: Physical observation, screen recording malware, cameras
- **Impact**: Process intelligence, operational secrets, facility layout
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Screen privacy filters, physical security, access controls, screen timeout
- **NIST Controls**: PE-3, PE-5, AC-11 (Session Lock)
- **IEC 62443**: PE-3, FR 2
- **Detection**: Physical security monitoring, access logging

#### Pattern: Asset Discovery via Industrial Protocols
- **Threat**: Discover ICS assets and topology through protocol scanning
- **DFD Element**: External Entity (Scanner) → Processes (ICS Devices)
- **Attack Vector**: Shodan, Censys, active scanning tools
- **Impact**: Attack surface mapping, vulnerability identification, targeting
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Network segmentation, firewalls, protocol filtering, disable unnecessary services
- **NIST Controls**: SC-7, CM-7, AC-4
- **IEC 62443**: FR 5, SR 5.1, SR 7.1
- **Detection**: Network intrusion detection, unusual scan patterns

### Privacy and PII Disclosure

#### Pattern: User Enumeration via Different Responses
- **Threat**: Determine valid usernames through differential responses
- **DFD Element**: Process (Authentication) response variations
- **Attack Vector**: Login, password reset, registration endpoints
- **Impact**: Username harvesting, targeted attacks, privacy violation
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Generic responses, rate limiting, CAPTCHA, account lockout
- **NIST Controls**: IA-5, AC-7 (Unsuccessful Logon Attempts)
- **IEC 62443**: SR 1.1, FR 1
- **Detection**: Enumeration attempt monitoring, failed login patterns

#### Pattern: PII in URL or Referrer Headers
- **Threat**: Personal data in URLs leaks to logs, proxies, third-party sites
- **DFD Element**: Data Flow (HTTP Headers) containing PII
- **Attack Vector**: Design flaw, improper data handling
- **Impact**: Privacy violation, GDPR/CCPA violations, PII exposure in logs
- **STRIDE Category**: Information Disclosure
- **Mitigation**: POST for sensitive data, Referrer-Policy headers, no PII in URLs
- **NIST Controls**: PT-2 (PII Processing), PT-3 (PII Disclosure), SC-8
- **IEC 62443**: FR 4, SR 4.1
- **Detection**: URL pattern analysis, privacy compliance audits

#### Pattern: Analytics/Tracking Data Leakage
- **Threat**: Third-party analytics expose user behavior and PII
- **DFD Element**: Data Flow → External Entity (Analytics Service)
- **Attack Vector**: Google Analytics, ad networks, tracking pixels
- **Impact**: Privacy violation, data aggregation, behavioral profiling
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Privacy-preserving analytics, data minimization, consent management, anonymization
- **NIST Controls**: PT-2, PT-7 (Specific PII Processing), AR-2 (Privacy Impact Assessment)
- **IEC 62443**: FR 4, SR 4.2
- **Detection**: Privacy audits, data flow mapping

#### Pattern: Medical Record Disclosure (PHI/ePHI)
- **Threat**: Unauthorized access to protected health information
- **DFD Element**: Data Store (Medical Records) → Unauthorized Access
- **Attack Vector**: IDOR, SQL injection, weak access controls, insider threat
- **Impact**: HIPAA violation, privacy breach, discrimination, identity theft
- **STRIDE Category**: Information Disclosure
- **Mitigation**: Encryption, access controls, audit logging, BAAs, minimum necessary access
- **NIST Controls**: SC-28, AC-3, AU-2, AR-4 (Privacy Monitoring)
- **IEC 62443**: FR 4, FR 2, SR 4.2
- **Detection**: Access monitoring, HIPAA audit logs, anomaly detection

## Cross-Framework Integration

### PASTA Stage 4: Threat Analysis
- Information disclosure scenarios by data classification
- Data flow analysis for confidentiality risks
- Privacy threat modeling

### PASTA Stage 5: Vulnerability Analysis
- Configuration exposures (cloud buckets, directories)
- Cryptographic weaknesses
- Application logic flaws

### IEC 62443 Requirements
- FR 4: Data Confidentiality (primary)
- SR 4.1: Information Confidentiality
- SR 4.2: Information Persistence
- SR 4.3: Use of Cryptography
- FR 5: Restricted Data Flow

### NIST SP 800-53 Controls
- SC-8: Transmission Confidentiality and Integrity
- SC-28: Protection of Information at Rest
- SC-13: Cryptographic Protection
- AC-3: Access Enforcement
- PT-2/3: PII Processing and Disclosure

## Detection Strategy

### Preventive Controls
- Data classification
- Encryption (transit and rest)
- Access controls
- DLP solutions
- Configuration management

### Detective Controls
- Log analysis (access patterns)
- DLP alerts
- Network monitoring
- Anomaly detection
- Security testing (DAST, SAST)

### Response Capabilities
- Incident response
- Breach notification
- Forensic analysis
- Compliance reporting

## Mitigation Hierarchy

### Level 1: Prevent Disclosure
- Encryption
- Access controls
- Data minimization
- Secure configuration
- Privacy by design

### Level 2: Detect Disclosure
- Monitoring and alerting
- DLP solutions
- Log analysis
- Vulnerability scanning
- Penetration testing

### Level 3: Limit Impact
- Data classification
- Segmentation
- Least privilege
- Tokenization/masking
- Time-limited access

### Level 4: Respond and Remediate
- Incident response
- Breach notification
- Forensics
- Lessons learned
- Compliance reporting
