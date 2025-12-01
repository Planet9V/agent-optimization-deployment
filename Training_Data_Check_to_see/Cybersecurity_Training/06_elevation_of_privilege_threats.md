# STRIDE: Elevation of Privilege Threats

## Entity Type
THREAT_MODEL, ATTACK_VECTOR, MITIGATION

## Overview
Elevation of Privilege involves gaining higher authorization levels than intended. This includes privilege escalation, unauthorized access, bypassing access controls, and obtaining administrative or system-level privileges.

## Threat Patterns (200+ patterns)

### Operating System Privilege Escalation

#### Pattern: Kernel Exploit for Root/SYSTEM
- **Threat**: Exploit kernel vulnerability to gain root/SYSTEM privileges
- **DFD Element**: Process (User Application) → Process (Kernel)
- **Attack Vector**: Kernel memory corruption, use-after-free, integer overflow
- **Impact**: Complete system compromise, persistent access, security control bypass
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: Kernel patches, address space layout randomization (ASLR), kernel hardening, least privilege
- **NIST Controls**: SI-2 (Flaw Remediation), SI-16 (Memory Protection), AC-6 (Least Privilege)
- **IEC 62443**: FR 3 (System Integrity), SR 3.4 (Software Integrity)
- **Detection**: EDR, behavior monitoring, kernel integrity checking

#### Pattern: SUID/SGID Binary Exploitation
- **Threat**: Exploit SUID/SGID binaries to execute code as owner (often root)
- **DFD Element**: Data Store (SUID Binary) → Process (Elevated Execution)
- **Attack Vector**: Buffer overflow, command injection, path traversal in SUID program
- **Impact**: Root access, system compromise
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: Minimize SUID binaries, security audits, input validation, capability-based security
- **NIST Controls**: CM-7 (Least Functionality), SI-16, AC-6
- **IEC 62443**: FR 2 (Use Control), SR 3.4
- **Detection**: SUID binary monitoring, file integrity monitoring, execution monitoring

#### Pattern: Sudo Configuration Exploitation
- **Threat**: Exploit misconfigured sudo rules to gain root access
- **DFD Element**: Process (sudo) configuration → Process (Elevated Command)
- **Attack Vector**: Wildcards in sudoers, vulnerable commands with NOPASSWD, sudo vulnerabilities
- **Impact**: Root access without password, privilege escalation
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: Strict sudoers configuration, no wildcards, regular audits, sudo version updates
- **NIST Controls**: CM-6 (Configuration Settings), AC-6, IA-5 (Authenticator Management)
- **IEC 62443**: FR 2, SR 2.1 (Authorization Enforcement)
- **Detection**: Sudoers file monitoring, sudo command logging

#### Pattern: PATH Environment Variable Hijacking
- **Threat**: Manipulate PATH to execute malicious binaries instead of intended ones
- **DFD Element**: Process (Environment) → Process (Command Execution)
- **Attack Vector**: Write malicious binary to writable directory early in PATH
- **Impact**: Code execution as privileged user, privilege escalation
- **STRIDE Category**: Elevation of Privilege + Tampering
- **Mitigation**: Use absolute paths in scripts, restrict PATH in privileged contexts, file permissions
- **NIST Controls**: CM-6, SI-7 (Software Integrity), AC-6
- **IEC 62443**: FR 3, SR 3.3 (Security Functionality Verification)
- **Detection**: PATH monitoring, execution monitoring, unexpected binaries

#### Pattern: DLL Hijacking/Search Order Exploitation
- **Threat**: Place malicious DLL in search path before legitimate DLL
- **DFD Element**: Data Store (Malicious DLL) → Process (Application Load)
- **Attack Vector**: Writable directories in DLL search order
- **Impact**: Code execution in application context, privilege escalation if elevated app
- **STRIDE Category**: Elevation of Privilege + Tampering
- **Mitigation**: SafeDllSearchMode, application manifests, signed DLLs, directory permissions
- **NIST Controls**: SI-7, CM-7, AC-6
- **IEC 62443**: SR 3.3, FR 3
- **Detection**: DLL load monitoring, signature verification, unexpected DLLs

### Windows-Specific Privilege Escalation

#### Pattern: Token Impersonation/Theft
- **Threat**: Steal or impersonate Windows access token to gain privileges
- **DFD Element**: Process (Token) → Process (Impersonated Context)
- **Attack Vector**: SeImpersonatePrivilege abuse, Juicy Potato, PrintSpoofer
- **Impact**: SYSTEM access, domain admin impersonation
- **STRIDE Category**: Elevation of Privilege + Spoofing
- **Mitigation**: Restrict SeImpersonatePrivilege, named pipe security, service hardening, least privilege
- **NIST Controls**: AC-6, IA-2 (Identification/Authentication), AC-3 (Access Enforcement)
- **IEC 62443**: FR 1, FR 2, SR 1.1
- **Detection**: Token manipulation monitoring, privilege usage monitoring

#### Pattern: Unquoted Service Path Exploitation
- **Threat**: Exploit unquoted service paths with spaces to execute malicious binary
- **DFD Element**: Data Store (Service Config) → Process (Service Execution)
- **Attack Vector**: Place binary in path before intended executable
- **Impact**: SYSTEM privilege code execution
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: Quote all service paths, restrict write permissions on path directories
- **NIST Controls**: CM-6, SI-7, AC-6
- **IEC 62443**: FR 2, SR 3.3
- **Detection**: Service configuration audits, file write monitoring

#### Pattern: Always Install Elevated (MSI)
- **Threat**: Abuse AlwaysInstallElevated policy to install malicious MSI as SYSTEM
- **DFD Element**: Process (Windows Installer) with elevated privileges
- **Attack Vector**: AlwaysInstallElevated registry key enabled
- **Impact**: SYSTEM access through MSI installation
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: Disable AlwaysInstallElevated, application whitelisting, least privilege
- **NIST Controls**: CM-6, CM-7, AC-6
- **IEC 62443**: FR 2, SR 2.1
- **Detection**: Group Policy monitoring, MSI installation monitoring

#### Pattern: Stored Credentials Extraction
- **Threat**: Extract stored credentials from Windows Credential Manager, LSASS, SAM
- **DFD Element**: Data Store (Credential Store) → External Entity (Attacker)
- **Attack Vector**: Mimikatz, procdump on LSASS, SAM/SYSTEM registry hives
- **Impact**: Credential reuse, lateral movement, domain privilege escalation
- **STRIDE Category**: Elevation of Privilege + Information Disclosure
- **Mitigation**: Credential Guard, Protected Process Light (PPL), LSA protection, WDigest disabled
- **NIST Controls**: IA-5, SC-28 (Protection at Rest), AC-6
- **IEC 62443**: FR 4, SR 1.5 (Authenticator Management)
- **Detection**: LSASS access monitoring, credential access events (4648, 4624 type 9)

### Linux-Specific Privilege Escalation

#### Pattern: Dirty COW Exploitation
- **Threat**: Exploit race condition in Linux kernel copy-on-write
- **DFD Element**: Process (User) → Data Store (Read-only File) write via race
- **Attack Vector**: CVE-2016-5195 kernel vulnerability
- **Impact**: Write to read-only files (e.g., /etc/passwd), root access
- **STRIDE Category**: Elevation of Privilege + Tampering
- **Mitigation**: Kernel patching, security updates, vulnerability management
- **NIST Controls**: SI-2, RA-5 (Vulnerability Scanning)
- **IEC 62443**: SR 3.4, FR 3
- **Detection**: Kernel integrity monitoring, file integrity monitoring

#### Pattern: Capability Exploitation
- **Threat**: Abuse Linux capabilities (CAP_DAC_OVERRIDE, CAP_SETUID, etc.)
- **DFD Element**: Process (Capability Set) → Privileged Operation
- **Attack Vector**: Binaries with excessive capabilities, capability escalation
- **Impact**: Privilege escalation, security control bypass
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: Minimal capabilities, capability auditing, least privilege
- **NIST Controls**: AC-6, CM-7
- **IEC 62443**: FR 2, SR 2.1
- **Detection**: Capability monitoring (getcap), execution monitoring

#### Pattern: Cron Job Hijacking
- **Threat**: Modify or replace scripts executed by cron as root
- **DFD Element**: Data Store (Cron Script) → Process (Cron Execution as root)
- **Attack Vector**: Writable cron scripts, world-writable directories in cron path
- **Impact**: Root code execution, persistence
- **STRIDE Category**: Elevation of Privilege + Tampering
- **Mitigation**: Proper file permissions, file integrity monitoring, use absolute paths
- **NIST Controls**: CM-6, SI-7, AC-6
- **IEC 62443**: FR 2, SR 3.3
- **Detection**: Cron file monitoring, unexpected cron execution

#### Pattern: Docker Socket Exploitation
- **Threat**: Access to Docker socket grants root access to host
- **DFD Element**: Data Store (Docker Socket /var/run/docker.sock)
- **Attack Vector**: User in docker group, exposed Docker socket
- **Impact**: Container escape, host root access, full system compromise
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: Rootless Docker, socket access controls, avoid docker group membership
- **NIST Controls**: AC-6, AC-3, SC-3 (Security Function Isolation)
- **IEC 62443**: FR 2, SR 2.1, SR 2.10 (Unauthorized Guidance)
- **Detection**: Docker socket access monitoring, suspicious container operations

### Application-Level Privilege Escalation

#### Pattern: Vertical Privilege Escalation via IDOR
- **Threat**: Access higher-privileged user accounts through object reference manipulation
- **DFD Element**: Process (Application) → Data Store (User Data)
- **Attack Vector**: Manipulate user ID parameters, predictable identifiers
- **Impact**: Admin account access, unauthorized operations
- **STRIDE Category**: Elevation of Privilege + Information Disclosure
- **Mitigation**: Authorization checks, indirect references, access control enforcement
- **NIST Controls**: AC-3, AC-6, SI-10 (Input Validation)
- **IEC 62443**: FR 2, SR 2.1
- **Detection**: Access pattern monitoring, authorization failures

#### Pattern: Horizontal Privilege Escalation via Parameter Tampering
- **Threat**: Access other users' data at same privilege level
- **DFD Element**: Process (Application) → Data Store (User Records)
- **Attack Vector**: Modify user ID in requests, session manipulation
- **Impact**: Privacy breach, unauthorized data access
- **STRIDE Category**: Elevation of Privilege (horizontal) + Information Disclosure
- **Mitigation**: Server-side authorization, session validation, object-level access control
- **NIST Controls**: AC-3, SC-23 (Session Authenticity)
- **IEC 62443**: FR 2, SR 2.1
- **Detection**: Anomalous access patterns, cross-user access attempts

#### Pattern: Role-Based Access Control (RBAC) Bypass
- **Threat**: Bypass role checks to access unauthorized functions
- **DFD Element**: Process (Authorization Check) bypass
- **Attack Vector**: Direct URL access, API endpoint enumeration, client-side role checks
- **Impact**: Unauthorized administrative functions, data modification
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: Server-side authorization, deny by default, function-level access control
- **NIST Controls**: AC-3, AC-2 (Account Management), AC-6
- **IEC 62443**: FR 2, SR 2.1
- **Detection**: Unauthorized function access, audit log analysis

#### Pattern: JWT Privilege Escalation
- **Threat**: Modify JWT claims to gain higher privileges
- **DFD Element**: Data Flow (JWT Token) → Process (Authorization)
- **Attack Vector**: Algorithm confusion (none algorithm), weak secrets, claim tampering
- **Impact**: Admin access, unauthorized operations
- **STRIDE Category**: Elevation of Privilege + Tampering
- **Mitigation**: Strong signature validation, no "none" algorithm, secret rotation, asymmetric keys
- **NIST Controls**: IA-5, SC-13 (Cryptographic Protection), AC-3
- **IEC 62443**: SR 4.3 (Cryptography), FR 2
- **Detection**: JWT signature validation, anomalous claims

### Database Privilege Escalation

#### Pattern: SQL Injection to DBA Privileges
- **Threat**: Escalate database privileges through SQL injection
- **DFD Element**: Process (Application) → Data Store (Database)
- **Attack Vector**: SQL injection + database-specific privilege escalation functions
- **Impact**: Database administrator access, operating system command execution
- **STRIDE Category**: Elevation of Privilege + Information Disclosure
- **Mitigation**: Parameterized queries, least privilege DB accounts, stored procedures, input validation
- **NIST Controls**: SI-10, AC-6, AC-3
- **IEC 62443**: SR 3.5 (Input Validation), FR 2
- **Detection**: SQL injection detection, privilege change monitoring

#### Pattern: Database User Impersonation
- **Threat**: Impersonate higher-privileged database user (EXECUTE AS, SET ROLE)
- **DFD Element**: Process (DB Session) → Process (Impersonated Session)
- **Attack Vector**: Abuse of EXECUTE AS, SET ROLE, or similar features
- **Impact**: Elevated database privileges, data access/modification
- **STRIDE Category**: Elevation of Privilege + Spoofing
- **Mitigation**: Restrict impersonation permissions, audit impersonation, least privilege
- **NIST Controls**: AC-3, AC-6, AU-2 (Audit Events)
- **IEC 62443**: FR 2, SR 2.1, SR 6.1
- **Detection**: Impersonation event monitoring, privilege usage auditing

#### Pattern: UDF (User-Defined Function) Exploitation
- **Threat**: Create malicious UDF to execute OS commands as database user
- **DFD Element**: Data Store (Database UDF) → Process (OS Execution)
- **Attack Vector**: CREATE FUNCTION with OS library (MySQL lib_mysqludf_sys)
- **Impact**: Operating system command execution, privilege escalation to database service account
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: Restrict CREATE FUNCTION privilege, secure database installation, least privilege
- **NIST Controls**: AC-6, CM-7, AC-3
- **IEC 62443**: FR 2, SR 2.1
- **Detection**: UDF creation monitoring, suspicious function execution

### Cloud and Container Privilege Escalation

#### Pattern: IAM Policy Exploitation (AWS/Azure/GCP)
- **Threat**: Exploit overly permissive IAM policies for privilege escalation
- **DFD Element**: Process (Cloud Service) → External Entity (Attacker with escalated role)
- **Attack Vector**: iam:PassRole, iam:CreateAccessKey, sts:AssumeRole abuse
- **Impact**: Administrator access, cross-account access, data breach
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: Least privilege IAM, IAM policy review, SCPs, permission boundaries
- **NIST Controls**: AC-6, AC-2, AC-3
- **IEC 62443**: FR 2, SR 2.1
- **Detection**: IAM activity monitoring, CloudTrail/Activity Log analysis, privilege changes

#### Pattern: Container Escape via Host Path Mount
- **Threat**: Mount host filesystem into container to modify host from container
- **DFD Element**: Process (Container) → Data Store (Host Filesystem)
- **Attack Vector**: --volume /:/host mount, privileged container
- **Impact**: Container escape, host root access
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: Restrict volume mounts, avoid privileged containers, least privilege, admission controllers
- **NIST Controls**: AC-6, SC-3, AC-3
- **IEC 62443**: FR 2, SR 2.1, SR 2.10
- **Detection**: Container configuration monitoring, volume mount auditing

#### Pattern: Kubernetes Service Account Token Exploitation
- **Threat**: Use service account token to escalate privileges in cluster
- **DFD Element**: Data Store (Service Account Token) → Process (Kubernetes API)
- **Attack Vector**: Token from mounted /var/run/secrets/kubernetes.io/serviceaccount
- **Impact**: Cluster admin access, pod creation, secret access
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: RBAC, least privilege service accounts, automountServiceAccountToken: false, OPA/Kyverno
- **NIST Controls**: AC-6, AC-3, IA-5
- **IEC 62443**: FR 2, SR 2.1, SR 1.5
- **Detection**: Kubernetes audit logs, anomalous API calls, privilege changes

#### Pattern: Serverless Function Privilege Escalation
- **Threat**: Exploit function permissions to access other cloud resources
- **DFD Element**: Process (Lambda/Function) → External Entity (Cloud Resources)
- **Attack Vector**: Overly permissive execution role, environment variable injection
- **Impact**: Access to databases, secrets, other functions, data exfiltration
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: Least privilege execution roles, resource-based policies, secret management
- **NIST Controls**: AC-6, AC-3, SC-28
- **IEC 62443**: FR 2, SR 2.1, FR 4
- **Detection**: Function execution monitoring, unusual resource access

### Active Directory Privilege Escalation

#### Pattern: Kerberos Delegation Abuse (Unconstrained/Constrained)
- **Threat**: Abuse Kerberos delegation to impersonate users
- **DFD Element**: Process (Delegated Service) → External Entity (Impersonated User)
- **Attack Vector**: Unconstrained delegation, constrained delegation misconfiguration
- **Impact**: User impersonation, lateral movement, domain admin access
- **STRIDE Category**: Elevation of Privilege + Spoofing
- **Mitigation**: Avoid unconstrained delegation, resource-based constrained delegation, protected users group
- **NIST Controls**: AC-6, IA-2, AC-3
- **IEC 62443**: FR 1, FR 2, SR 1.1
- **Detection**: Delegation monitoring, TGT requests from services, Kerberos ticket anomalies

#### Pattern: DCSync Attack
- **Threat**: Use directory replication permissions to dump password hashes
- **DFD Element**: External Entity (Attacker) → Process (Domain Controller) replication
- **Attack Vector**: DS-Replication-Get-Changes permissions
- **Impact**: All domain password hashes, domain admin credentials
- **STRIDE Category**: Elevation of Privilege + Information Disclosure
- **Mitigation**: Restrict replication permissions, monitor replication requests, privileged account protection
- **NIST Controls**: AC-6, AU-2, AC-3
- **IEC 62443**: FR 2, SR 6.1, FR 4
- **Detection**: Event ID 4662 (directory replication), unusual replication sources

#### Pattern: Group Policy Object (GPO) Modification
- **Threat**: Modify GPO to execute code or change settings on domain computers
- **DFD Element**: Data Store (GPO) → Process (Group Policy Application)
- **Attack Vector**: Write permissions on GPO, GPO link creation
- **Impact**: Domain-wide code execution, privilege escalation, persistence
- **STRIDE Category**: Elevation of Privilege + Tampering
- **Mitigation**: Restrict GPO modify permissions, GPO auditing, change monitoring
- **NIST Controls**: CM-3 (Configuration Change Control), AC-6, AU-2
- **IEC 62443**: FR 2, SR 2.1, SR 6.1
- **Detection**: GPO modification events, unauthorized GPO changes

#### Pattern: NTLM Relay to Domain Controller
- **Threat**: Relay captured NTLM authentication to domain controller
- **DFD Element**: External Entity (Attacker) → Process (Domain Controller)
- **Attack Vector**: NTLM relay, SMB signing disabled, LDAP signing disabled
- **Impact**: Domain privilege escalation, account creation, group membership modification
- **STRIDE Category**: Elevation of Privilege + Spoofing
- **Mitigation**: SMB signing required, LDAP signing/channel binding, disable NTLM, Extended Protection
- **NIST Controls**: IA-2, SC-8, AC-6
- **IEC 62443**: FR 1, SR 1.1, SR 3.1
- **Detection**: NTLM relay patterns, suspicious DC authentication, account modifications

### Web Application Privilege Escalation

#### Pattern: File Upload to Code Execution
- **Threat**: Upload malicious file (web shell) to gain code execution
- **DFD Element**: Data Flow (File Upload) → Data Store (Web Directory) → Process (Code Execution)
- **Attack Vector**: Unrestricted file upload, inadequate validation, executable directories
- **Impact**: Web server compromise, privilege escalation to web server user
- **STRIDE Category**: Elevation of Privilege + Tampering
- **Mitigation**: File type validation, content inspection, non-executable upload directories, filename sanitization
- **NIST Controls**: SI-10, AC-6, CM-7
- **IEC 62443**: SR 3.5, FR 2
- **Detection**: File upload monitoring, web shell detection, unexpected file execution

#### Pattern: Command Injection via Web Input
- **Threat**: Inject OS commands through web application input
- **DFD Element**: Data Flow (User Input) → Process (OS Command Execution)
- **Attack Vector**: Unsanitized input passed to system(), exec(), shell commands
- **Impact**: Code execution as web server user, potential privilege escalation
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: Input validation, parameterized commands, avoid system calls, least privilege
- **NIST Controls**: SI-10, AC-6, SI-16
- **IEC 62443**: SR 3.5, FR 2
- **Detection**: Command injection detection, process execution monitoring, WAF alerts

#### Pattern: Server-Side Template Injection (SSTI)
- **Threat**: Inject code into template engine for server-side execution
- **DFD Element**: Data Flow (Template Input) → Process (Template Engine)
- **Attack Vector**: Unsanitized user input in template context (Jinja2, Twig, etc.)
- **Impact**: Remote code execution, server compromise
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: Input validation, sandbox template engines, logic-less templates, CSP
- **NIST Controls**: SI-10, AC-6
- **IEC 62443**: SR 3.5, FR 2
- **Detection**: SSTI payloads detection, anomalous template rendering, WAF

#### Pattern: Deserialization Exploitation
- **Threat**: Exploit unsafe deserialization to achieve code execution
- **DFD Element**: Data Flow (Serialized Object) → Process (Deserialization) → Code Execution
- **Attack Vector**: Malicious serialized objects (Java, Python pickle, .NET)
- **Impact**: Remote code execution, privilege escalation
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: Avoid deserialization of untrusted data, integrity checks, restricted deserialization
- **NIST Controls**: SI-10, AC-6, SC-8
- **IEC 62443**: SR 3.5, FR 3
- **Detection**: Deserialization monitoring, known gadget chains, behavioral analysis

### ICS/SCADA Privilege Escalation

#### Pattern: Engineering Workstation Compromise
- **Threat**: Compromise engineering workstation with full PLC/RTU access
- **DFD Element**: Process (Engineering Workstation) → Data Store (PLC/RTU)
- **Attack Vector**: Phishing, malware, vulnerability exploitation
- **Impact**: Full control over industrial processes, logic modification, safety system override
- **STRIDE Category**: Elevation of Privilege + Tampering
- **Mitigation**: Network segmentation, 2FA, application whitelisting, least privilege, air gap
- **NIST Controls**: AC-6, SC-7, IA-2(1) (MFA)
- **IEC 62443**: FR 1, FR 2, SR 1.1, SR 2.1
- **Detection**: Workstation activity monitoring, unusual PLC access, code download attempts

#### Pattern: Default Credential Exploitation in ICS
- **Threat**: Use default or vendor credentials to access ICS devices
- **DFD Element**: External Entity → Process (ICS Device) authentication
- **Attack Vector**: Unchanged default passwords, hardcoded credentials
- **Impact**: Device control, configuration modification, privilege escalation
- **STRIDE Category**: Elevation of Privilege
- **Mitigation**: Change default credentials, credential management, password policies
- **NIST Controls**: IA-5, AC-2, CM-6
- **IEC 62443**: SR 1.5, FR 1, SR 1.1
- **Detection**: Default credential usage, authentication monitoring, brute-force detection

#### Pattern: SCADA Protocol Command Injection
- **Threat**: Inject unauthorized commands via SCADA protocols (Modbus, DNP3)
- **DFD Element**: External Entity → Data Flow (SCADA Protocol) → Process (Field Device)
- **Attack Vector**: Unauthenticated protocols, network access, command crafting
- **Impact**: Unauthorized control operations, safety override, process manipulation
- **STRIDE Category**: Elevation of Privilege + Tampering
- **Mitigation**: Protocol authentication (DNP3 SA, TLS), network segmentation, command validation
- **NIST Controls**: AC-3, SC-8, IA-3 (Device Identification)
- **IEC 62443**: FR 1, FR 5, SR 3.1, SR 5.1
- **Detection**: Protocol monitoring, unauthorized commands, command pattern analysis

## Cross-Framework Integration

### PASTA Stage 4: Threat Analysis
- Privilege escalation paths by attack surface
- Trust boundary violations
- Authorization bypass scenarios

### PASTA Stage 6: Attack Modeling
- Attack trees for privilege escalation
- Exploit chain analysis
- Lateral movement + privilege escalation

### IEC 62443 Requirements
- FR 2: Use Control (primary)
- SR 2.1: Authorization Enforcement
- SR 1.1: Human User Identification/Authentication
- FR 1: Identification and Authentication Control

### NIST SP 800-53 Controls
- AC-6: Least Privilege (primary)
- AC-3: Access Enforcement
- AC-2: Account Management
- IA-2: Identification and Authentication
- SI-16: Memory Protection

## Detection Strategy

### Privilege Change Monitoring
- Account privilege modifications
- Role/group membership changes
- Elevation events
- Impersonation detection

### Behavioral Analysis
- Anomalous command execution
- Unusual file access patterns
- Unexpected network connections
- Process ancestry analysis

### Audit Log Correlation
- Failed privilege escalation attempts
- Repeated access denials
- Authentication anomalies
- Configuration changes

## Mitigation Hierarchy

### Level 1: Prevent Escalation
- Least privilege principle
- Strong authentication/MFA
- Secure configuration
- Patching/vulnerability management
- Input validation

### Level 2: Detect Escalation
- Privilege monitoring
- Behavioral analytics
- EDR/SIEM
- Audit logging
- File integrity monitoring

### Level 3: Limit Impact
- Segmentation
- Privilege boundaries
- Just-in-time access
- Ephemeral credentials
- Strong access controls

### Level 4: Respond and Remediate
- Incident response
- Privilege revocation
- Account lockout
- Forensic investigation
- Root cause analysis
