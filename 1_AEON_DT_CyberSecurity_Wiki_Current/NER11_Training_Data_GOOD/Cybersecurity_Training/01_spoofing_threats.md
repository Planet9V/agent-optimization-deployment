# STRIDE: Spoofing Identity Threats

## Entity Type
THREAT_MODEL, ATTACK_VECTOR

## Overview
Spoofing involves pretending to be something or someone other than yourself. This category includes authentication bypasses, impersonation attacks, and identity theft scenarios.

## Threat Patterns (200+ patterns)

### IP Spoofing Attacks

#### Pattern: TCP SYN Flood with Spoofed Source
- **Threat**: Attacker sends TCP SYN packets with forged source IP addresses
- **DFD Element**: External Entity → Process (Network Service)
- **Attack Vector**: Network layer manipulation
- **Impact**: Denial of service, resource exhaustion, legitimate connection blocking
- **STRIDE Category**: Spoofing + Denial of Service
- **Mitigation**: SYN cookies, rate limiting, ingress filtering (BCP38)
- **NIST Controls**: SC-5 (Denial of Service Protection), SC-7 (Boundary Protection)
- **Detection**: Asymmetric traffic patterns, half-open connection monitoring

#### Pattern: IP Source Address Forgery
- **Threat**: Attacker modifies packet headers to hide true origin
- **DFD Element**: External Entity → Data Flow
- **Attack Vector**: Raw socket manipulation, packet crafting tools
- **Impact**: Bypass IP-based access controls, hide attack origin
- **STRIDE Category**: Spoofing
- **Mitigation**: Anti-spoofing filters, reverse path forwarding (RPF)
- **NIST Controls**: SC-7(4), SC-7(5)
- **Detection**: BCP38 compliance checking, ingress filtering validation

#### Pattern: Land Attack (Same Source/Destination IP)
- **Threat**: TCP packet with identical source and destination addresses
- **DFD Element**: External Entity → Process
- **Attack Vector**: Crafted TCP packets
- **Impact**: System crash, kernel panic, resource exhaustion
- **STRIDE Category**: Spoofing + Denial of Service
- **Mitigation**: Input validation, sanity checking, modern TCP/IP stack
- **NIST Controls**: SI-10 (Information Input Validation)
- **Detection**: Packet inspection for identical source/dest addresses

### ARP Spoofing and Cache Poisoning

#### Pattern: ARP Cache Poisoning MITM
- **Threat**: Attacker sends forged ARP replies to associate their MAC with victim IP
- **DFD Element**: Data Flow between processes on same network
- **Attack Vector**: Gratuitous ARP replies, ARP request/reply manipulation
- **Impact**: Man-in-the-middle, traffic interception, session hijacking
- **STRIDE Category**: Spoofing + Information Disclosure
- **Mitigation**: Static ARP entries, Dynamic ARP Inspection (DAI), port security
- **NIST Controls**: SC-8 (Transmission Confidentiality), SC-23 (Session Authenticity)
- **Detection**: ARP table monitoring, duplicate MAC address detection

#### Pattern: ARP Spoofing for DoS
- **Threat**: Map victim IP to non-existent MAC address
- **DFD Element**: Data Flow → Process
- **Attack Vector**: Forged ARP replies
- **Impact**: Network connectivity loss, service disruption
- **STRIDE Category**: Spoofing + Denial of Service
- **Mitigation**: DAI, DHCP snooping, port security
- **NIST Controls**: SC-5, SC-7
- **Detection**: Failed ARP resolution patterns, connectivity issues

#### Pattern: Gratuitous ARP Attack
- **Threat**: Unsolicited ARP replies to poison cache entries
- **DFD Element**: Network segment data flows
- **Attack Vector**: Broadcast gratuitous ARP packets
- **Impact**: Traffic redirection, MITM positioning
- **STRIDE Category**: Spoofing
- **Mitigation**: Reject gratuitous ARPs, static bindings, DAI
- **NIST Controls**: SC-7(4), SC-8(1)
- **Detection**: Unsolicited ARP reply monitoring

### DNS Spoofing and Cache Poisoning

#### Pattern: DNS Cache Poisoning (Kaminsky Attack)
- **Threat**: Inject false DNS records into resolver cache
- **DFD Element**: External Entity (DNS Server) → Process (Resolver)
- **Attack Vector**: Transaction ID prediction, birthday attack on query IDs
- **Impact**: Traffic redirection, phishing, malware distribution
- **STRIDE Category**: Spoofing + Information Disclosure
- **Mitigation**: DNSSEC, source port randomization, 0x20 encoding
- **NIST Controls**: SC-20 (Secure Name/Address Resolution), SC-21
- **Detection**: DNSSEC validation failures, unexpected DNS responses

#### Pattern: DNS Response Spoofing
- **Threat**: Race condition to respond before legitimate DNS server
- **DFD Element**: Data Flow (DNS Query/Response)
- **Attack Vector**: Network position, fast response generation
- **Impact**: User redirection to malicious sites
- **STRIDE Category**: Spoofing
- **Mitigation**: DNSSEC, DNS over HTTPS (DoH), DNS over TLS (DoT)
- **NIST Controls**: SC-20, SC-8(1)
- **Detection**: Multiple responses for same query, TTL anomalies

#### Pattern: Local DNS Hijacking
- **Threat**: Modify local DNS settings or hosts file
- **DFD Element**: Data Store (Configuration Files)
- **Attack Vector**: Malware, compromised system access
- **Impact**: All DNS queries redirected
- **STRIDE Category**: Spoofing + Tampering
- **Mitigation**: File integrity monitoring, least privilege, endpoint protection
- **NIST Controls**: CM-3 (Configuration Change Control), SI-7 (Software Integrity)
- **Detection**: Hosts file changes, DNS settings modifications

#### Pattern: DNS Homograph Attack (IDN Spoofing)
- **Threat**: Use visually similar Unicode characters in domain names
- **DFD Element**: External Entity (Malicious Domain)
- **Attack Vector**: Internationalized Domain Names (IDN)
- **Impact**: Phishing, credential theft, brand impersonation
- **STRIDE Category**: Spoofing
- **Mitigation**: Punycode display, IDN blacklisting, user education
- **NIST Controls**: AT-2 (Security Awareness Training)
- **Detection**: Visual similarity algorithms, reported phishing domains

### Email Spoofing

#### Pattern: SMTP Header Injection
- **Threat**: Forge email headers including From, Reply-To, Return-Path
- **DFD Element**: External Entity → Process (Mail Server)
- **Attack Vector**: Lack of sender authentication
- **Impact**: Phishing, social engineering, reputation damage
- **STRIDE Category**: Spoofing
- **Mitigation**: SPF, DKIM, DMARC implementation
- **NIST Controls**: SC-23, IA-4 (Identifier Management)
- **Detection**: SPF/DKIM/DMARC failures, anomalous sender patterns

#### Pattern: Display Name Spoofing
- **Threat**: Use legitimate display name with different email address
- **DFD Element**: Process (Email Client) display logic
- **Attack Vector**: Email header manipulation
- **Impact**: Executive impersonation, wire fraud, credential phishing
- **STRIDE Category**: Spoofing
- **Mitigation**: Display actual email address, warning indicators, DMARC
- **NIST Controls**: AT-2, SC-23
- **Detection**: Display name/address mismatch, first-time sender indicators

#### Pattern: Reply-To Header Manipulation
- **Threat**: Set Reply-To to attacker-controlled address
- **DFD Element**: Data Flow (Email Response)
- **Attack Vector**: Header field manipulation
- **Impact**: Response interception, information disclosure
- **STRIDE Category**: Spoofing + Information Disclosure
- **Mitigation**: Display Reply-To prominently, user awareness
- **NIST Controls**: AT-2, SC-23
- **Detection**: Reply-To different from From address

#### Pattern: Cousin Domain Attack
- **Threat**: Register similar domain with typosquatting or character substitution
- **DFD Element**: External Entity (Lookalike Domain)
- **Attack Vector**: Domain registration, visual similarity
- **Impact**: Credential phishing, wire fraud, data exfiltration
- **STRIDE Category**: Spoofing
- **Mitigation**: Domain monitoring, DMARC reject policy, trademark protection
- **NIST Controls**: RA-5 (Vulnerability Scanning - external domain monitoring)
- **Detection**: Brand monitoring services, reported phishing domains

### Web Spoofing

#### Pattern: Homograph Domain Phishing
- **Threat**: Register visually identical domain using Unicode lookalikes
- **DFD Element**: External Entity (Phishing Website)
- **Attack Vector**: IDN homograph, Punycode domain registration
- **Impact**: Credential theft, malware distribution, financial fraud
- **STRIDE Category**: Spoofing
- **Mitigation**: Browser IDN protection, certificate transparency monitoring
- **NIST Controls**: AT-2, IA-2(1) (Multi-factor Authentication)
- **Detection**: Certificate transparency logs, user reports

#### Pattern: SSL Certificate Misissuance
- **Threat**: Obtain valid certificate for targeted domain through CA compromise
- **DFD Element**: External Entity (Rogue CA or Compromised CA)
- **Attack Vector**: CA validation bypass, compromised CA infrastructure
- **Impact**: MITM with valid certificate, undetected interception
- **STRIDE Category**: Spoofing
- **Mitigation**: Certificate Transparency, certificate pinning, CAA records
- **NIST Controls**: IA-5(2) (PKI-based Authentication), SC-17
- **Detection**: CT log monitoring, certificate pinning violations

#### Pattern: Browser Address Bar Spoofing
- **Threat**: Display fake URL in browser through UI manipulation
- **DFD Element**: Process (Browser) UI rendering
- **Attack Vector**: JavaScript manipulation, browser vulnerabilities
- **Impact**: User deception, credential submission to phishing site
- **STRIDE Category**: Spoofing
- **Mitigation**: Browser security updates, EV certificates, user education
- **NIST Controls**: SI-2 (Flaw Remediation), AT-2
- **Detection**: Browser security testing, reported vulnerabilities

#### Pattern: Open Redirect Exploitation
- **Threat**: Abuse legitimate site's redirect to mask phishing URL
- **DFD Element**: Process (Web Application) redirect logic
- **Attack Vector**: Unvalidated redirect parameter
- **Impact**: Phishing URL appears legitimate, bypasses filters
- **STRIDE Category**: Spoofing
- **Mitigation**: Validate redirect destinations, use indirect references
- **NIST Controls**: SI-10, SI-11 (Error Handling)
- **Detection**: Code review for redirect parameters, SAST tools

### Caller ID and VoIP Spoofing

#### Pattern: SIP INVITE Header Spoofing
- **Threat**: Forge From header in SIP messages
- **DFD Element**: External Entity → Process (VoIP Server)
- **Attack Vector**: Lack of SIP authentication, open relay
- **Impact**: Vishing attacks, impersonation, social engineering
- **STRIDE Category**: Spoofing
- **Mitigation**: SIP authentication, TLS for signaling, certificate validation
- **NIST Controls**: IA-3 (Device Identification and Authentication), SC-8
- **Detection**: SIP header analysis, call pattern anomalies

#### Pattern: STIR/SHAKEN Bypass
- **Threat**: Present calls as authenticated when they are not
- **DFD Element**: Data Flow (Call Signaling)
- **Attack Vector**: Incomplete STIR/SHAKEN deployment, gateway manipulation
- **Impact**: Spoofed caller ID appears verified
- **STRIDE Category**: Spoofing
- **Mitigation**: Full STIR/SHAKEN implementation, attestation verification
- **NIST Controls**: IA-3, IA-9 (Service Identification)
- **Detection**: Attestation validation, inconsistent signatures

#### Pattern: PRI/ISDN Caller ID Injection
- **Threat**: Set arbitrary caller ID on PRI/ISDN trunks
- **DFD Element**: External Entity (Telecom Carrier) → Process
- **Attack Vector**: Carrier trust model, inadequate validation
- **Impact**: Law enforcement impersonation, financial fraud
- **STRIDE Category**: Spoofing
- **Mitigation**: Carrier-side validation, origination verification
- **NIST Controls**: IA-3, AC-3 (Access Enforcement)
- **Detection**: Carrier-level fraud detection systems

### Authentication Bypass through Spoofing

#### Pattern: MAC Address Spoofing for Network Access
- **Threat**: Clone authorized device MAC address
- **DFD Element**: External Entity → Process (Network Access Control)
- **Attack Vector**: MAC address modification, network sniffing
- **Impact**: Bypass MAC filtering, unauthorized network access
- **STRIDE Category**: Spoofing + Elevation of Privilege
- **Mitigation**: 802.1X authentication, port security, NAC
- **NIST Controls**: AC-17 (Remote Access), AC-18 (Wireless Access)
- **Detection**: Duplicate MAC detection, 802.1X enforcement

#### Pattern: Bluetooth Device Impersonation
- **Threat**: Spoof trusted Bluetooth device identity
- **DFD Element**: External Entity (Fake BT Device) → Process
- **Attack Vector**: Bluetooth pairing vulnerabilities, weak authentication
- **Impact**: Unauthorized access, data interception, device control
- **STRIDE Category**: Spoofing
- **Mitigation**: Bluetooth authentication, out-of-band pairing verification
- **NIST Controls**: AC-18, SC-8
- **Detection**: Pairing anomalies, unexpected device connections

#### Pattern: NFC Relay Attack
- **Threat**: Relay NFC communication to spoof proximity
- **DFD Element**: Data Flow (NFC Communication)
- **Attack Vector**: NFC signal relay using two devices
- **Impact**: Unauthorized payment, access control bypass
- **STRIDE Category**: Spoofing
- **Mitigation**: Distance bounding, transaction verification, anomaly detection
- **NIST Controls**: IA-3, SC-23
- **Detection**: Transaction time analysis, location verification

#### Pattern: RFID Tag Cloning
- **Threat**: Copy RFID tag data to counterfeit tag
- **DFD Element**: External Entity (Cloned RFID) → Process (Reader)
- **Attack Vector**: RFID skimming, replay attack
- **Impact**: Physical access control bypass, asset tracking evasion
- **STRIDE Category**: Spoofing
- **Mitigation**: Encrypted RFID, challenge-response authentication
- **NIST Controls**: PE-3 (Physical Access Control), IA-3
- **Detection**: Duplicate tag detection, access pattern analysis

### Session Spoofing

#### Pattern: Session Token Prediction
- **Threat**: Predict valid session identifiers through weak generation
- **DFD Element**: Process (Session Management) → Data Store
- **Attack Vector**: Sequential token generation, inadequate entropy
- **Impact**: Account takeover, unauthorized access
- **STRIDE Category**: Spoofing + Elevation of Privilege
- **Mitigation**: Cryptographically secure random generation, sufficient entropy
- **NIST Controls**: IA-5(1) (Password-based Authentication), SC-12 (Cryptographic Key)
- **Detection**: Session token analysis, brute-force detection

#### Pattern: Session Fixation
- **Threat**: Force user to authenticate with attacker-known session ID
- **DFD Element**: Process (Authentication) session handling
- **Attack Vector**: Set session ID before authentication
- **Impact**: Session hijacking post-authentication
- **STRIDE Category**: Spoofing + Elevation of Privilege
- **Mitigation**: Regenerate session ID after authentication
- **NIST Controls**: SC-23, IA-2
- **Detection**: Pre-authentication session ID persistence

#### Pattern: Cookie Injection
- **Threat**: Inject session cookie into victim's browser
- **DFD Element**: Data Flow (HTTP Cookie)
- **Attack Vector**: XSS, network MITM, malware
- **Impact**: Session hijacking, account access
- **STRIDE Category**: Spoofing + Tampering
- **Mitigation**: HTTPOnly flag, Secure flag, SameSite attribute
- **NIST Controls**: SC-8, SC-23
- **Detection**: Cookie attribute validation, unexpected cookie origins

### Protocol-Level Spoofing

#### Pattern: ICMP Redirect Attack
- **Threat**: Send forged ICMP redirect messages to alter routing
- **DFD Element**: Data Flow (Network Routing)
- **Attack Vector**: ICMP message injection
- **Impact**: Traffic redirection, MITM, denial of service
- **STRIDE Category**: Spoofing + Denial of Service
- **Mitigation**: Disable ICMP redirects, route authentication
- **NIST Controls**: SC-7, CM-6 (Configuration Settings)
- **Detection**: Unexpected routing changes, ICMP redirect monitoring

#### Pattern: DHCP Spoofing
- **Threat**: Rogue DHCP server provides malicious network configuration
- **DFD Element**: External Entity (Rogue DHCP) → Process (Client)
- **Attack Vector**: Faster DHCP response than legitimate server
- **Impact**: DNS hijacking, default gateway redirection, MITM
- **STRIDE Category**: Spoofing + Elevation of Privilege
- **Mitigation**: DHCP snooping, port security, 802.1X
- **NIST Controls**: SC-7, AC-17
- **Detection**: DHCP snooping binding validation, rogue DHCP detection

#### Pattern: BGP Route Hijacking
- **Threat**: Announce false BGP routes to redirect Internet traffic
- **DFD Element**: External Entity (AS) → Internet routing
- **Attack Vector**: BGP trust model, lack of route validation
- **Impact**: Large-scale traffic interception, blackholing
- **STRIDE Category**: Spoofing + Denial of Service
- **Mitigation**: RPKI, BGP route filtering, IRR validation
- **NIST Controls**: SC-7, SC-24 (Fail in Known State)
- **Detection**: BGP monitoring systems, route anomaly detection

#### Pattern: IPv6 Neighbor Discovery Spoofing
- **Threat**: Similar to ARP spoofing but for IPv6 networks
- **DFD Element**: Data Flow (IPv6 Link-Local)
- **Attack Vector**: Forged Neighbor Advertisement messages
- **Impact**: MITM, traffic interception, DoS
- **STRIDE Category**: Spoofing
- **Mitigation**: ND inspection, SEcure Neighbor Discovery (SEND)
- **NIST Controls**: SC-7, SC-8
- **Detection**: Duplicate address detection anomalies

### Credential Spoofing

#### Pattern: Pass-the-Hash Attack
- **Threat**: Use captured password hash without cracking
- **DFD Element**: Data Flow (Authentication) → Process
- **Attack Vector**: NTLM hash capture, SMB relay
- **Impact**: Lateral movement, privilege escalation
- **STRIDE Category**: Spoofing + Elevation of Privilege
- **Mitigation**: Kerberos instead of NTLM, credential guard, admin account restrictions
- **NIST Controls**: IA-2, AC-6 (Least Privilege)
- **Detection**: Unusual authentication patterns, rare source/destination pairs

#### Pattern: Kerberos Golden Ticket
- **Threat**: Forge Kerberos TGT with krbtgt account hash
- **DFD Element**: Process (KDC) authentication service
- **Attack Vector**: Domain controller compromise, krbtgt hash extraction
- **Impact**: Persistent domain admin access, all service access
- **STRIDE Category**: Spoofing + Elevation of Privilege
- **Mitigation**: Protect domain controllers, rotate krbtgt password, monitor TGT usage
- **NIST Controls**: AC-2 (Account Management), IA-2
- **Detection**: TGT with unusual lifetimes, encryption types, or privileges

#### Pattern: Kerberos Silver Ticket
- **Threat**: Forge service ticket with service account hash
- **DFD Element**: Process (Specific Service)
- **Attack Vector**: Service account compromise, hash extraction
- **Impact**: Persistent access to specific service
- **STRIDE Category**: Spoofing + Elevation of Privilege
- **Mitigation**: Managed service accounts, regular password rotation, monitoring
- **NIST Controls**: IA-5 (Authenticator Management), AC-2
- **Detection**: Service tickets without corresponding TGT request

#### Pattern: SAML Assertion Forgery
- **Threat**: Create or modify SAML assertions for unauthorized access
- **DFD Element**: External Entity (IdP) → Process (Service Provider)
- **Attack Vector**: Weak signature validation, XML signature wrapping
- **Impact**: SSO bypass, unauthorized federated access
- **STRIDE Category**: Spoofing
- **Mitigation**: Strong signature validation, certificate pinning, SAML security best practices
- **NIST Controls**: IA-2, IA-8 (Identification and Authentication)
- **Detection**: Signature validation failures, unexpected assertion sources

#### Pattern: OAuth Token Theft and Replay
- **Threat**: Steal and reuse OAuth access/refresh tokens
- **DFD Element**: Data Flow (OAuth Token) → Process (API)
- **Attack Vector**: XSS, malware, insecure storage, MITM
- **Impact**: Account access, API abuse with user privileges
- **STRIDE Category**: Spoofing + Information Disclosure
- **Mitigation**: Token binding, PKCE, short token lifetimes, secure storage
- **NIST Controls**: IA-5, SC-8, SC-23
- **Detection**: Token usage from unexpected locations/devices

### Biometric Spoofing

#### Pattern: Fingerprint Replica Attack
- **Threat**: Create fake fingerprint to bypass biometric authentication
- **DFD Element**: External Entity → Process (Biometric Reader)
- **Attack Vector**: Lifted prints, 3D printing, molds
- **Impact**: Physical access control bypass, device unlock
- **STRIDE Category**: Spoofing
- **Mitigation**: Liveness detection, multi-factor authentication, capacitive sensors
- **NIST Controls**: IA-3, PE-3
- **Detection**: Liveness check failures, sensor anomaly detection

#### Pattern: Facial Recognition Photo/Video Attack
- **Threat**: Use photo or video to spoof face authentication
- **DFD Element**: External Entity (Presentation Attack) → Process
- **Attack Vector**: Printed photos, video replay, 3D masks
- **Impact**: Device unlock, account access, physical access
- **STRIDE Category**: Spoofing
- **Mitigation**: 3D sensing, liveness detection, infrared imaging, multi-factor
- **NIST Controls**: IA-3, IA-2
- **Detection**: Depth sensing, texture analysis, micro-movements

#### Pattern: Voice Synthesis Attack
- **Threat**: Use AI-generated voice to bypass voice authentication
- **DFD Element**: External Entity (Synthesized Voice) → Process
- **Attack Vector**: Voice cloning ML models, recorded samples
- **Impact**: Phone banking fraud, IVR system access
- **STRIDE Category**: Spoofing
- **Mitigation**: Multi-factor authentication, voice liveness detection, behavioral analysis
- **NIST Controls**: IA-3, IA-2(1)
- **Detection**: Synthetic voice detection algorithms, anomaly analysis

### Application-Level Spoofing

#### Pattern: User-Agent Spoofing for Detection Evasion
- **Threat**: Modify User-Agent header to evade security controls
- **DFD Element**: Data Flow (HTTP Request) → Process
- **Attack Vector**: Header manipulation
- **Impact**: WAF bypass, bot detection evasion, vulnerability scanning
- **STRIDE Category**: Spoofing
- **Mitigation**: Behavioral analysis beyond User-Agent, JavaScript challenges
- **NIST Controls**: SI-10, SC-7
- **Detection**: Behavioral fingerprinting, TLS fingerprinting mismatch

#### Pattern: Referer Header Spoofing
- **Threat**: Forge Referer header to bypass access controls
- **DFD Element**: Data Flow (HTTP Request) header
- **Attack Vector**: Header manipulation
- **Impact**: CSRF protection bypass, referrer-based access control bypass
- **STRIDE Category**: Spoofing
- **Mitigation**: Token-based CSRF protection, proper access controls
- **NIST Controls**: SC-23, AC-3
- **Detection**: Referer validation, multi-factor authorization

#### Pattern: X-Forwarded-For Spoofing
- **Threat**: Manipulate X-Forwarded-For header to spoof client IP
- **DFD Element**: Data Flow (HTTP Header) → Process (Backend)
- **Attack Vector**: Proxy header injection
- **Impact**: IP-based access control bypass, rate limiting evasion, logging evasion
- **STRIDE Category**: Spoofing
- **Mitigation**: Trust only specific proxy IPs, validate header chain
- **NIST Controls**: AC-3, SC-7
- **Detection**: Header validation, inconsistent forwarding chains

#### Pattern: HTTP Host Header Injection
- **Threat**: Manipulate Host header for password reset poisoning, cache poisoning
- **DFD Element**: Data Flow (HTTP Request) → Process
- **Attack Vector**: Host header not validated
- **Impact**: Password reset link hijacking, web cache poisoning
- **STRIDE Category**: Spoofing + Tampering
- **Mitigation**: Validate Host header against whitelist, use absolute URLs
- **NIST Controls**: SI-10, SC-7
- **Detection**: Unexpected Host header values, SAST detection

## DFD Integration Points

### External Entities
- Spoofed identity sources (fake servers, impersonators)
- Rogue network devices (DHCP, DNS, routing)
- Phishing infrastructure

### Processes
- Authentication services (credential validation)
- Network services (DNS, DHCP, routing)
- Session management
- Biometric verification systems

### Data Flows
- Authentication credentials (in-transit)
- Network protocols (IP, ARP, DNS, BGP)
- Session tokens and cookies
- Email headers and content

### Data Stores
- Credential databases
- Session stores
- DNS caches
- ARP caches

## Cross-Framework Mappings

### IEC 62443 Foundational Requirements
- FR 1: Identification and Authentication Control
- FR 2: Use Control (prevents spoofed entity actions)
- FR 3: System Integrity (prevents protocol manipulation)
- FR 5: Restricted Data Flow (prevents spoofed traffic)

### PASTA Integration
- Stage 4: Threat Analysis - Spoofing scenarios by asset
- Stage 6: Attack Modeling - Spoofing attack chains
- Stage 7: Risk scoring for spoofing vulnerabilities

### NIST SP 800-53 Controls
- IA family (Identification and Authentication)
- SC-23 (Session Authenticity)
- SC-20/21 (Secure Name/Address Resolution)
- AC-3 (Access Enforcement - prevent spoofed entities)

## Detection and Monitoring

### Network-Level Detection
- Asymmetric routing patterns
- Duplicate MAC/IP addresses
- ARP cache inconsistencies
- DNS response anomalies
- DNSSEC validation failures
- BGP route anomalies

### Application-Level Detection
- Authentication anomalies (location, time, device)
- Session behavior changes
- Header validation failures
- Certificate transparency violations
- Biometric liveness check failures

### System-Level Detection
- Process authentication failures
- Unexpected service account usage
- Kerberos ticket anomalies
- Token usage patterns
- File integrity violations (hosts file, DNS config)

## Mitigation Hierarchy

### Level 1: Prevent Spoofing
- Strong cryptographic authentication
- Certificate-based authentication
- Multi-factor authentication
- Protocol security extensions (DNSSEC, RPKI, STIR/SHAKEN)

### Level 2: Detect Spoofing
- Anomaly detection
- Behavioral analytics
- Protocol validation
- Certificate transparency
- Biometric liveness detection

### Level 3: Limit Impact
- Least privilege
- Network segmentation
- Session timeouts
- Transaction verification
- Rate limiting

### Level 4: Respond and Recover
- Incident response procedures
- Account lockout mechanisms
- Session termination
- Certificate revocation
- Forensic capabilities
