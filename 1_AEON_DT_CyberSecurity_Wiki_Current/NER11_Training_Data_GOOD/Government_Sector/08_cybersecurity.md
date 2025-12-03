# Government Sector - Cybersecurity and IT Security

## Network Security Architecture

### Network Segmentation
**Air-Gapped Networks**
- Classified networks (SIPRNET, JWICS)
- Unclassified networks (NIPRNET)
- Physical separation (no network connection)
- Separate hardware and infrastructure
- Cross-domain solutions (CDS) for authorized data transfer
- Strict access controls and monitoring
- TEMPEST shielding for SCIF areas

**Network Zones and VLANs**
- Corporate network (office workstations, email, internet)
- Building automation network (BAS, HVAC, lighting)
- Security systems network (access control, video surveillance)
- Industrial control systems (SCADA, DCS)
- Guest network (visitor Wi-Fi, isolated)
- IoT network (sensors, smart devices)
- Management network (network infrastructure management)
- Out-of-band management (console access, isolated)

**Network Segmentation Technologies**
- VLANs (Virtual Local Area Networks)
- Firewalls (next-generation, stateful)
- ACLs (Access Control Lists) on routers and switches
- Private VLANs (PVLAN) for isolation
- Network Address Translation (NAT)
- DMZ (Demilitarized Zone) for public-facing services
- Microsegmentation (data center, zero trust)

### Firewall Architecture
**Firewall Types**
- **Next-Generation Firewalls (NGFW)**: Application-aware, IPS, user identity
- **Stateful Inspection Firewalls**: Track connection state
- **Web Application Firewalls (WAF)**: HTTP/HTTPS protection
- **Cloud Firewalls**: AWS Security Groups, Azure NSG, GCP Firewall Rules

**Firewall Vendors**
- Palo Alto Networks (PA-Series, VM-Series)
- Cisco Firepower (FTD, ASA)
- Fortinet FortiGate
- Check Point (Quantum Security Gateways)
- Juniper Networks SRX Series
- Sophos XG Firewall
- pfSense (open-source)

**Firewall Rules and Policies**
- Default deny (block all, allow specific)
- Least privilege access
- Source/destination IP filtering
- Port and protocol filtering
- Application control (allow/block applications)
- User/group-based policies
- Geolocation filtering
- URL filtering and web content filtering
- SSL/TLS inspection (decrypt and inspect)

**High Availability and Redundancy**
- Active-passive failover
- Active-active load balancing
- State synchronization between firewalls
- Redundant ISP connections
- Automatic failover on link or device failure

### Intrusion Detection and Prevention
**IDS/IPS Technologies**
- **NIDS (Network-based IDS)**: Monitors network traffic
- **NIPS (Network-based IPS)**: Blocks malicious traffic
- **HIDS (Host-based IDS)**: Monitors system logs and files
- **HIPS (Host-based IPS)**: Blocks malicious processes

**IDS/IPS Vendors**
- Cisco Firepower (Sourcefire)
- Palo Alto Networks Threat Prevention
- Fortinet FortiGate IPS
- Trend Micro TippingPoint
- McAfee Network Security Platform
- Snort (open-source NIDS)
- Suricata (open-source IDS/IPS)
- Zeek (formerly Bro) - network analysis

**Detection Methods**
- **Signature-based**: Known attack patterns (fast, limited to known threats)
- **Anomaly-based**: Detects deviations from baseline (behavioral analysis)
- **Heuristic-based**: Rule-based detection
- **Machine learning**: AI-powered threat detection
- **Reputation-based**: IP/domain reputation databases

**IPS Deployment Modes**
- Inline mode (blocks malicious traffic)
- Passive mode (alerts only, no blocking)
- Tap mode (network tap, monitoring only)
- Virtual patching (IPS compensates for unpatched vulnerabilities)

### Virtual Private Networks (VPNs)
**VPN Types**
- **Site-to-Site VPN**: Connect branch offices to headquarters
- **Remote Access VPN**: Connect remote users to corporate network
- **Client-to-Site VPN**: VPN client software on user devices
- **SSL VPN**: Browser-based VPN (clientless)
- **IPsec VPN**: Site-to-site and remote access

**VPN Protocols**
- **IPsec**: IP Security (AH, ESP)
- **SSL/TLS**: Secure Sockets Layer VPN
- **IKEv2**: Internet Key Exchange version 2
- **L2TP/IPsec**: Layer 2 Tunneling Protocol with IPsec
- **WireGuard**: Modern, fast, lightweight VPN protocol
- **OpenVPN**: Open-source VPN solution

**VPN Gateways and Concentrators**
- Cisco ASA with AnyConnect
- Palo Alto Networks GlobalProtect
- Fortinet FortiGate VPN
- Check Point VPN
- Pulse Secure (Ivanti)
- Cisco VPN routers (ISR, ASR)
- OpenVPN Access Server

**VPN Security**
- Multi-factor authentication (MFA)
- Certificate-based authentication (PKI)
- Strong encryption (AES-256)
- Perfect forward secrecy (PFS)
- Split tunneling (policy-based)
- Idle session timeout
- User activity logging

### Wireless Security
**Wi-Fi Security Standards**
- **WPA3-Enterprise**: Latest, most secure (802.1X authentication)
- **WPA2-Enterprise**: Still widely used (AES encryption)
- **WPA2-PSK**: Pre-shared key (home/small business)
- **WPA3-Personal**: Enhanced PSK security
- **Avoid WEP and WPA**: Obsolete, insecure

**Enterprise Wireless Authentication**
- 802.1X authentication (RADIUS)
- EAP-TLS (certificate-based, most secure)
- PEAP-MSCHAPv2 (username/password)
- EAP-TTLS
- Certificate validation (RADIUS server)
- User and device authentication

**Wireless Intrusion Prevention Systems (WIPS)**
- Rogue access point detection
- Evil twin detection
- Denial-of-service (DoS) attack prevention
- Man-in-the-middle attack detection
- Unauthorized device detection
- RF spectrum analysis
- Automatic threat mitigation

**Wireless Network Design**
- Guest network isolation (separate VLAN, captive portal)
- Corporate network (802.1X authentication)
- IoT network (dedicated SSID, restricted access)
- Site survey and RF design
- Channel planning (non-overlapping channels)
- Coverage and capacity planning
- Roaming optimization

## Endpoint Security

### Antivirus and Anti-Malware
**Endpoint Protection Platforms (EPP)**
- CrowdStrike Falcon
- Microsoft Defender for Endpoint
- Symantec Endpoint Protection
- Trend Micro Apex One
- McAfee Endpoint Security
- Sophos Intercept X
- Kaspersky Endpoint Security
- Bitdefender GravityZone

**Endpoint Detection and Response (EDR)**
- CrowdStrike Falcon Insight
- Microsoft Defender for Endpoint (EDR)
- SentinelOne Singularity
- Carbon Black (VMware)
- Palo Alto Networks Cortex XDR
- Trend Micro Vision One
- Cisco Secure Endpoint (AMP)

**EPP/EDR Capabilities**
- Real-time file scanning
- Behavioral analysis and anomaly detection
- Machine learning threat detection
- Ransomware protection and rollback
- Exploit prevention
- Fileless malware detection
- Memory scanning
- Threat intelligence integration
- Automated response and remediation
- Forensic investigation and root cause analysis

### Patch Management
**Patch Management Tools**
- Microsoft WSUS (Windows Server Update Services)
- Microsoft SCCM (System Center Configuration Manager)
- JAMF (macOS, iOS management)
- Ivanti Patch Management
- ManageEngine Patch Manager Plus
- SolarWinds Patch Manager
- Red Hat Satellite (Linux)
- Ansible (configuration management and patching)

**Patch Management Process**
- **Patch Identification**: Monitor vendor security bulletins
- **Risk Assessment**: Evaluate patch criticality and impact
- **Testing**: Test patches in lab environment
- **Approval**: Change management approval
- **Deployment**: Phased rollout (pilot, production)
- **Verification**: Confirm successful installation
- **Reporting**: Compliance reporting and metrics

**Patching Timelines**
- **Critical patches**: 30 days or less (federal mandate)
- **High-risk patches**: 60 days
- **Medium-risk patches**: 90 days
- **Low-risk patches**: 180 days or as needed
- **Emergency patches**: Immediate (zero-day vulnerabilities)

### Data Loss Prevention (DLP)
**DLP Solutions**
- Symantec Data Loss Prevention
- McAfee Total Protection for DLP
- Forcepoint DLP
- Digital Guardian DLP
- Microsoft Purview (Information Protection)
- Proofpoint DLP
- Trend Micro DLP

**DLP Technologies**
- **Network DLP**: Monitors network traffic (email, web, FTP)
- **Endpoint DLP**: Monitors data on endpoints (copy, print, USB)
- **Cloud DLP**: Monitors cloud applications (SaaS, IaaS)
- **Discovery DLP**: Scans data repositories (file servers, SharePoint, databases)

**DLP Policies**
- Sensitive data classification (confidential, secret, top secret)
- Content inspection (keywords, patterns, regular expressions)
- Contextual analysis (sender, recipient, file type)
- Encryption enforcement
- USB/removable media blocking
- Email attachment encryption
- Cloud upload restrictions
- Print and screen capture blocking

### Mobile Device Management (MDM)
**MDM Solutions**
- Microsoft Intune
- VMware Workspace ONE
- Citrix Endpoint Management
- IBM MaaS360
- Jamf Pro (Apple devices)
- Blackberry UEM
- Google Workspace (Android management)
- Samsung Knox Manage

**MDM Capabilities**
- Device enrollment and provisioning
- Configuration profiles (Wi-Fi, VPN, email)
- Application management (app deployment, blacklist/whitelist)
- Security policies (passcode, encryption, jailbreak detection)
- Remote wipe and lock
- Location tracking
- Compliance monitoring
- Containerization (work/personal data separation)

**BYOD (Bring Your Own Device) Policies**
- Device registration and approval
- Personal vs. corporate data separation
- Application containerization (work apps isolated)
- Remote wipe of corporate data only
- Acceptable use policies
- Privacy considerations

## Identity and Access Management (IAM)

### User Authentication
**Multi-Factor Authentication (MFA)**
- **Something you know**: Password, PIN
- **Something you have**: Hardware token (YubiKey, RSA SecurID), smartphone app (Duo, Microsoft Authenticator)
- **Something you are**: Biometrics (fingerprint, facial recognition)

**MFA Solutions**
- Duo Security (Cisco)
- Microsoft Authenticator
- Okta Verify
- RSA SecurID
- YubiKey (FIDO2, U2F, OTP)
- Google Authenticator (TOTP)
- Symantec VIP
- Ping Identity

**Authentication Protocols**
- **SAML 2.0**: Security Assertion Markup Language (SSO)
- **OAuth 2.0**: Authorization framework
- **OpenID Connect**: Identity layer on top of OAuth 2.0
- **Kerberos**: Network authentication protocol (Active Directory)
- **RADIUS**: Remote Authentication Dial-In User Service
- **LDAP**: Lightweight Directory Access Protocol

### Single Sign-On (SSO)
**SSO Solutions**
- Okta
- Microsoft Azure AD (Entra ID)
- Ping Identity
- OneLogin
- Auth0 (Okta)
- JumpCloud
- Google Workspace SSO

**SSO Benefits**
- Reduced password fatigue
- Improved user experience
- Centralized access management
- Enhanced security (one strong password)
- Reduced help desk calls (password resets)
- Compliance and audit logging

### Privileged Access Management (PAM)
**PAM Solutions**
- CyberArk Privileged Access Security
- BeyondTrust Privileged Remote Access
- Thycotic Secret Server
- Delinea (formerly Centrify)
- HashiCorp Vault
- Keeper Security
- ManageEngine PAM360

**PAM Capabilities**
- Privileged account discovery
- Password vaulting and rotation
- Session recording and monitoring
- Just-in-time (JIT) access
- Privilege elevation and delegation
- Least privilege enforcement
- Access request and approval workflow
- Audit logging and compliance reporting

**Privileged Accounts**
- Domain admin accounts
- Local administrator accounts
- Service accounts
- Application accounts
- Database admin accounts
- Network device admin accounts (routers, switches, firewalls)
- Cloud admin accounts (AWS root, Azure Global Admin)

### Directory Services
**Active Directory (AD)**
- User and computer account management
- Group Policy (GPO)
- Organizational Units (OU)
- Domain controller replication
- Kerberos authentication
- LDAP queries
- DNS integration
- Forest and domain trusts

**Azure Active Directory (Azure AD / Entra ID)**
- Cloud-based identity service
- Single Sign-On (SSO)
- Multi-Factor Authentication (MFA)
- Conditional Access policies
- Hybrid identity (AD Connect)
- Self-service password reset
- Application integration (SaaS apps)
- Identity protection (risk-based conditional access)

**LDAP Directories**
- OpenLDAP (open-source)
- Red Hat Directory Server
- Oracle Directory Server
- 389 Directory Server
- Apache Directory Server

## Security Monitoring and Incident Response

### Security Information and Event Management (SIEM)
**SIEM Platforms**
- Splunk Enterprise Security
- IBM QRadar
- LogRhythm NextGen SIEM
- ArcSight (Micro Focus)
- Microsoft Sentinel (cloud SIEM)
- Elastic Security (ELK stack)
- AlienVault OSSIM (open-source)
- Sumo Logic (cloud SIEM)

**SIEM Functions**
- Log aggregation from multiple sources
- Real-time correlation and analysis
- Threat detection (signatures, anomalies, ML)
- Alerting and notification
- Incident investigation
- Dashboards and visualization
- Compliance reporting (FISMA, PCI-DSS, HIPAA)
- Threat intelligence integration
- User and Entity Behavior Analytics (UEBA)

**Log Sources**
- Firewalls and network devices
- Intrusion detection/prevention systems (IDS/IPS)
- Endpoint protection (antivirus, EDR)
- Windows event logs
- Linux/Unix syslog
- Web servers and application servers
- Databases
- Cloud services (AWS CloudTrail, Azure Monitor)
- Active Directory and authentication servers
- Physical security systems (access control, video)

### Threat Intelligence
**Threat Intelligence Platforms (TIP)**
- Anomali ThreatStream
- ThreatConnect
- Recorded Future
- Palo Alto Networks AutoFocus
- IBM X-Force Exchange
- MISP (Open-source threat intelligence platform)

**Threat Intelligence Sources**
- US-CERT (United States Computer Emergency Readiness Team)
- DHS CISA (Cybersecurity and Infrastructure Security Agency)
- FBI InfraGard
- ISACs (Information Sharing and Analysis Centers)
- Commercial threat feeds (Proofpoint, FireEye, CrowdStrike)
- Open-source threat feeds (AlienVault OTX, MISP)
- Dark web monitoring
- OSINT (Open-Source Intelligence)

**Threat Intelligence Use Cases**
- Indicator of Compromise (IoC) blocking (IPs, domains, file hashes)
- Threat actor profiling and attribution
- Vulnerability prioritization
- Proactive defense (threat hunting)
- Incident response and forensics
- Security awareness and training
- Risk assessment and decision-making

### Incident Response
**Incident Response Process (NIST SP 800-61)**
1. **Preparation**: IR plan, tools, training, communication
2. **Detection and Analysis**: Identify and analyze incidents
3. **Containment, Eradication, and Recovery**: Isolate, remove threat, restore
4. **Post-Incident Activity**: Lessons learned, improve defenses

**Incident Response Team (IRT/CSIRT)**
- Incident Manager/Coordinator
- Security Analysts (Tier 2/3)
- Forensic Analysts
- Network Engineers
- System Administrators
- Legal Counsel
- Public Relations/Communications
- Management Stakeholders

**Incident Severity Levels**
- **Critical (P1)**: Active data breach, ransomware, system compromise
- **High (P2)**: Confirmed malware, unauthorized access attempt
- **Medium (P3)**: Suspicious activity, policy violation
- **Low (P4)**: Informational, potential threat, false positive

**Incident Response Tools**
- **SIEM**: Splunk, QRadar, LogRhythm
- **Forensic Tools**: EnCase, FTK, Autopsy, Volatility (memory forensics)
- **Network Analysis**: Wireshark, tcpdump, Zeek
- **Malware Analysis**: Cuckoo Sandbox, Any.Run, IDA Pro, Ghidra
- **EDR**: CrowdStrike, SentinelOne, Carbon Black
- **Threat Intelligence**: MISP, ThreatConnect, Recorded Future

**Incident Playbooks**
- Ransomware response
- Phishing and business email compromise (BEC)
- Data breach (exfiltration)
- Insider threat
- Denial of service (DoS/DDoS)
- Malware infection
- Unauthorized access
- Lost or stolen device

### Vulnerability Management
**Vulnerability Scanning Tools**
- Tenable Nessus (vulnerability scanner)
- Qualys VMDR (Vulnerability Management, Detection and Response)
- Rapid7 InsightVM
- OpenVAS (open-source)
- Greenbone Security Manager
- Tenable.io (cloud-based)
- Microsoft Defender Vulnerability Management

**Vulnerability Scanning Types**
- **Authenticated scans**: Credentialed, deeper inspection
- **Unauthenticated scans**: Non-credentialed, external perspective
- **Internal scans**: Scan internal network
- **External scans**: Scan internet-facing assets
- **Web application scans**: OWASP Top 10, SQL injection, XSS
- **Database scans**: Database-specific vulnerabilities

**Vulnerability Management Process**
1. **Asset Discovery**: Identify all assets (servers, workstations, network devices, applications)
2. **Vulnerability Scanning**: Automated scanning (weekly/monthly)
3. **Vulnerability Assessment**: Analyze and prioritize vulnerabilities
4. **Remediation**: Patch, configure, mitigate
5. **Verification**: Re-scan to confirm remediation
6. **Reporting**: Compliance reporting, metrics, trends

**Vulnerability Severity Ratings**
- **Critical (CVSS 9.0-10.0)**: Immediate action required
- **High (CVSS 7.0-8.9)**: Priority remediation (30 days)
- **Medium (CVSS 4.0-6.9)**: Remediate within 90 days
- **Low (CVSS 0.1-3.9)**: Remediate as resources permit
- **Informational**: No immediate risk, awareness

### Penetration Testing
**Penetration Testing Types**
- **External Penetration Test**: Test internet-facing systems (web, VPN, email)
- **Internal Penetration Test**: Test internal network (simulate insider threat)
- **Web Application Penetration Test**: Test web apps for OWASP Top 10
- **Wireless Penetration Test**: Test Wi-Fi security (WPA2 cracking, rogue AP)
- **Social Engineering**: Phishing, vishing, physical security testing
- **Red Team Exercise**: Full-scope adversary simulation

**Penetration Testing Tools**
- **Kali Linux**: Penetration testing Linux distribution
- **Metasploit**: Exploitation framework
- **Burp Suite**: Web application testing
- **Nmap**: Network scanning and enumeration
- **Wireshark**: Network protocol analyzer
- **John the Ripper / Hashcat**: Password cracking
- **Aircrack-ng**: Wireless security testing
- **Cobalt Strike**: Red team simulation platform

**Penetration Testing Process**
1. **Planning and Scoping**: Define objectives, scope, rules of engagement
2. **Reconnaissance**: Gather information (OSINT, network scanning)
3. **Vulnerability Analysis**: Identify weaknesses
4. **Exploitation**: Attempt to exploit vulnerabilities
5. **Post-Exploitation**: Privilege escalation, lateral movement, data exfiltration
6. **Reporting**: Detailed report with findings, risk ratings, remediation recommendations

**Penetration Testing Standards**
- **PTES (Penetration Testing Execution Standard)**
- **OWASP Testing Guide** (web application testing)
- **NIST SP 800-115** (Technical Guide to Information Security Testing and Assessment)

## Data Protection and Encryption

### Encryption Technologies
**Data at Rest Encryption**
- Full disk encryption (FDE)
  - BitLocker (Windows)
  - FileVault (macOS)
  - LUKS (Linux)
- Database encryption (Transparent Data Encryption - TDE)
- File-level encryption (EFS, GPG)
- Cloud storage encryption (AWS S3, Azure Blob, Google Cloud Storage)

**Data in Transit Encryption**
- TLS/SSL (web, email, APIs)
- IPsec (site-to-site VPN, network layer)
- SSH (secure shell, file transfer)
- SFTP/FTPS (secure file transfer)
- S/MIME (email encryption)
- PGP/GPG (email and file encryption)

**Encryption Algorithms**
- **Symmetric**: AES-128, AES-256 (fast, shared key)
- **Asymmetric**: RSA-2048, RSA-4096, ECC (public/private key)
- **Hashing**: SHA-256, SHA-512, SHA-3 (one-way, integrity)
- **Key Exchange**: Diffie-Hellman, ECDH

### Public Key Infrastructure (PKI)
**PKI Components**
- **Certificate Authority (CA)**: Issues digital certificates
- **Registration Authority (RA)**: Verifies certificate requests
- **Certificate Revocation List (CRL)**: List of revoked certificates
- **OCSP (Online Certificate Status Protocol)**: Real-time certificate status

**Digital Certificates**
- SSL/TLS certificates (web servers, HTTPS)
- Code signing certificates (software authenticity)
- Email certificates (S/MIME)
- User certificates (smart cards, PIV)
- Device certificates (802.1X, VPN)
- Root CA certificates (trust anchor)

**Certificate Management**
- Certificate issuance and renewal
- Certificate revocation
- Certificate lifecycle management
- Automated certificate management (Let's Encrypt, ACME protocol)
- Certificate pinning (mobile apps, APIs)

### Secure Communications
**Encrypted Email**
- S/MIME (Secure/Multipurpose Internet Mail Extensions)
- PGP/GPG (Pretty Good Privacy / GNU Privacy Guard)
- TLS encryption (transport layer)
- Email gateway encryption (Proofpoint, Mimecast)

**Encrypted Messaging**
- Signal (end-to-end encryption)
- WhatsApp (end-to-end encryption)
- Wickr (secure collaboration)
- Microsoft Teams (encryption at rest and in transit)
- Slack Enterprise (encryption at rest and in transit)

**Secure File Sharing**
- Secure file transfer (SFTP, FTPS, SCP)
- Encrypted file sharing platforms (Box, Egnyte, SharePoint)
- End-to-end encrypted sharing (Tresorit, Sync.com)
- Data room solutions (Intralinks, Firmex)

## Cloud Security

### Cloud Service Models
**IaaS (Infrastructure as a Service)**
- AWS EC2, Azure Virtual Machines, Google Compute Engine
- Customer responsibility: OS, applications, data, network configuration
- Provider responsibility: Physical infrastructure, hypervisor

**PaaS (Platform as a Service)**
- AWS Elastic Beanstalk, Azure App Service, Google App Engine
- Customer responsibility: Applications, data
- Provider responsibility: OS, runtime, middleware

**SaaS (Software as a Service)**
- Microsoft 365, Salesforce, Google Workspace
- Customer responsibility: Data, user access
- Provider responsibility: Application, infrastructure

### Cloud Security Controls
**Identity and Access Management (IAM)**
- AWS IAM (users, groups, roles, policies)
- Azure AD (Entra ID)
- Google Cloud IAM
- Least privilege access
- Service accounts and roles
- Multi-factor authentication (MFA)
- Federated identity (SAML, OpenID Connect)

**Network Security**
- Virtual Private Cloud (VPC) / Virtual Network
- Security Groups (stateful firewall)
- Network Access Control Lists (NACLs) - stateless firewall
- Private subnets (no internet access)
- VPN and Direct Connect (private connectivity)
- Web Application Firewall (WAF)
- DDoS protection (AWS Shield, Azure DDoS Protection)

**Data Protection**
- Encryption at rest (AWS KMS, Azure Key Vault, Google Cloud KMS)
- Encryption in transit (TLS/SSL)
- Key management (customer-managed keys, HSM)
- Data classification and tagging
- Backup and disaster recovery
- Data residency and sovereignty

**Logging and Monitoring**
- AWS CloudTrail (API logging)
- Azure Monitor and Log Analytics
- Google Cloud Logging
- Centralized log aggregation (SIEM integration)
- Security monitoring and alerting
- Compliance auditing

### Cloud Security Standards and Compliance
**FedRAMP (Federal Risk and Authorization Management Program)**
- Cloud security assessment and authorization
- Three impact levels: Low, Moderate, High
- 3PAO (Third-Party Assessment Organization) audits
- Continuous monitoring and reporting
- Required for federal agency cloud adoption

**Cloud Security Alliance (CSA)**
- Cloud Controls Matrix (CCM)
- Security Guidance for Cloud Computing
- STAR Certification (Security, Trust, Assurance, and Risk)
- Cloud security best practices

**Compliance Frameworks**
- SOC 2 Type II (Service Organization Control)
- ISO/IEC 27017 (Cloud Security)
- ISO/IEC 27018 (Privacy in Cloud)
- PCI-DSS (Payment Card Industry Data Security Standard)
- HIPAA (Health Insurance Portability and Accountability Act)
