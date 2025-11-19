# 5G Security Architecture - Communications Sector

## Entity-Rich Introduction

5G security architecture defined by 3GPP TS 33.501 implements multi-layer defense mechanisms with home network public key infrastructure enabling SUCI (Subscription Concealed Identifier) protection using ECIES (Elliptic Curve Integrated Encryption Scheme) with Curve25519 or P-256 elliptic curves, concealing IMSI from IMSI catchers and preventing subscriber tracking across cell boundaries. Security anchor functionality resides in AUSF (Authentication Server Function) executing 5G-AKA (Authentication and Key Agreement) protocol deriving 256-bit anchor key KAUSF from permanent key K stored in USIM, subsequently generating KSEAF (256-bit), KAMF (256-bit), and KgNB (256-bit) through SHA-256 HMAC key derivation functions following NIST SP 800-108 recommendations. User plane encryption utilizes NEA1 (SNOW 3G), NEA2 (AES-CTR), or NEA3 (ZUC) algorithms providing 128-bit or 256-bit confidentiality protection with integrity algorithms NIA1 (SNOW 3G), NIA2 (AES-CMAC), NIA3 (ZUC) generating 32-bit MAC-I (Message Authentication Code for Integrity) tags appended to control plane messages. Network slicing security enforces per-slice isolation with dedicated security contexts, separate encryption keys per PDU session, and slice-specific access control policies implemented through PCF (Policy Control Function) provisioning differentiated QoS and security policies for eMBB, URLLC, and mMTC network slices.

## Technical Specifications

**5G Authentication and Key Agreement**:
- 5G-AKA Protocol: Mutual authentication between UE and network
- Primary Authentication: AUSF executes AV (Authentication Vector) generation
- Key Hierarchy: K (permanent) → KAUSF → KSEAF → KAMF → KgNB → KUPenc/KUPint
- Algorithm: Milenage (128-bit) or TUAK (128/256-bit) in USIM
- SQN Management: Sequence number synchronization preventing replay attacks
- SUCI Schemes: Scheme 1 (ECIES Profile A, Curve25519), Scheme 2 (ECIES Profile B, P-256)
- Public Key: Home network public key pre-provisioned in USIM or bootstrap server
- SUPI Types: IMSI, NAI (Network Access Identifier), GCI (Global Cable Identifier)
- Anti-Bidding Down: UE rejects security capability downgrade attempts
- Re-authentication: Periodic authentication every 2-8 hours configurable

**User Plane and Control Plane Encryption**:
- Encryption Algorithms: 128-EEA1 (SNOW 3G), 128-EEA2 (AES-CTR), 128-EEA3 (ZUC), 256-bit variants
- Integrity Algorithms: 128-EIA1 (SNOW 3G), 128-EIA2 (AES-CMAC), 128-EIA3 (ZUC)
- Algorithm Negotiation: UE and network exchange security capability lists
- Null Encryption: Prohibited in commercial networks, allowed only for emergency calls
- Ciphering Activation: Initiated by AMF after successful authentication
- COUNT Value: 32-bit sequence (5-bit HFN + 27-bit PDCP SN) preventing replay
- Integrity Protection: Applied to NAS and RRC control plane messages
- User Plane Option: UP integrity optional for eMBB, mandatory for URLLC

**Network Slicing Security Architecture**:
- Slice Isolation: Logical separation of network resources per slice type
- Slice ID: S-NSSAI (Single Network Slice Selection Assistance Information)
- Security Contexts: Independent encryption keys per PDU session within slice
- Access Control: PCF enforces per-slice subscriber authorization policies
- QoS Enforcement: 5QI (5G QoS Identifier) values 1-9 (GBR), 10-79 (non-GBR)
- UE Slice Selection: NSSAI (Network Slice Selection Assistance Information) in registration
- Slice Admission: AMF validates slice subscription in UDM before PDU session establishment

**Fronthaul and Midhaul Security**:
- eCPRI Encryption: IPsec ESP with AES-256-GCM authenticated encryption
- MACsec: IEEE 802.1AE with GCM-AES-256, 128-bit ICV (Integrity Check Value)
- Key Management: IKEv2 with X.509 certificates, pre-shared keys (PSK) fallback
- PTP Security: IEEE 1588v2 with authentication TLVs preventing timing attacks
- CU-DU Split: F1-C and F1-U interfaces protected with IPsec tunnels
- Certificate Validation: OCSP stapling, CRL checking, certificate pinning

**API and Interface Security**:
- Service-Based Architecture: HTTP/2 with TLS 1.3 mandatory
- OAuth 2.0: NRF (Network Repository Function) issues access tokens
- mTLS: Mutual authentication between network functions using X.509 certificates
- API Gateway: Rate limiting (1000 req/sec per NF), DDoS protection, input validation
- N2 Interface: SCTP over IPsec protecting NGAP messages
- N3 Interface: GTP-U with optional IPsec ESP encryption
- N4 Interface: PFCP over DTLS 1.2 securing SMF-UPF communication

**Edge Computing Security (MEC)**:
- UPF Local Breakout: User plane traffic routed to local data network
- Application Authentication: OAuth 2.0 JWT tokens for MEC app authorization
- Traffic Steering: URSP (UE Route Selection Policy) rules enforcing edge routing
- Data Residency: GDPR compliance with geo-fencing preventing data egress
- Container Security: Kubernetes RBAC, pod security policies, network policies

## Integration & Operations

5G security deployment in nationwide mobile operator network (MNO-SECURITY-01) provisions AUSF instances in active-active configuration across 3 geographically distributed data centers (DC-EAST, DC-CENTRAL, DC-WEST) processing 150,000 authentication requests/second with <50ms latency utilizing Ericsson Cloud Core AUSF running on Red Hat OpenShift 4.12 with horizontal pod autoscaling. Home network public key infrastructure deploys Curve25519 elliptic curve keypair with 3072-bit equivalent security strength, distributing public key to 200 million USIM cards (Gemalto/Thales SIM manufacturing) through OTA (Over-The-Air) SIM update mechanism utilizing BIP (Bearer Independent Protocol) SMS delivery. Nokia Cloud Packet Core implementation enforces network slice-specific security policies with eMBB slice (SST=1) utilizing 128-bit AES-CTR encryption sufficient for consumer broadband, URLLC slice (SST=2) mandating 256-bit AES-CTR encryption plus integrity protection for industrial control applications requiring <1ms latency and 99.9999% reliability. Security context establishment completes NAS Security Mode Command procedure within 100ms average (target <200ms 99th percentile), with AMF deriving KAMF from KSEAF and transmitting selected encryption algorithm (EEA2) and integrity algorithm (EIA2) to UE in Security Mode Command message. Fronthaul network security between Ericsson AIR 3268 Remote Radio Unit and Cloud RAN baseband pool implements MACsec encryption (IEEE 802.1AE) with GCM-AES-256 on 25 Gbps Ethernet links, utilizing Connectivity Association Key (CAK) with 256-bit entropy rotated every 7 days distributed through MKA (MACsec Key Agreement) protocol authenticated via X.509 certificates. Certificate lifecycle management infrastructure operates Nokia NetGuard Certificate Authority issuing X.509v3 certificates with 2048-bit RSA keys to 100,000 network functions (gNodeB, AMF, SMF, UPF, NEF, NRF), implementing automated renewal 60 days before expiration and OCSP (Online Certificate Status Protocol) validation with <2 second response time. Security monitoring infrastructure deploys Splunk Enterprise Security SIEM aggregating 10 million events/hour from AMF, SMF, PCF, and UPF network functions, correlating authentication failures (>5 failures in 60 seconds triggers account lockout), abnormal mobility patterns (>20 cell reselections in 5 minutes indicating IMSI catcher), and unusual data volume patterns (>10 GB in 1 hour from IoT device). Penetration testing program executes quarterly security assessments simulating attacks: IMSI catching attempts with fake gNodeB (LTE IMSI catcher detection rate 98%), GTP-U user plane interception (encrypted tunnel validation), DoS attacks against AMF (rate limiting effectiveness >99%), and malicious application attempts to exploit NEF API vulnerabilities (WAF blocking rate 95%).

## Security Implementation

Network function security hardens container images following CIS Kubernetes Benchmark with minimal base images (Alpine Linux 3.17), non-root user execution (UID 1000), read-only root filesystem, and automated vulnerability scanning (Aqua Security Trivy) detecting CVEs before deployment to production with zero-tolerance policy blocking High/Critical severity vulnerabilities. Kubernetes security implements Pod Security Policies restricting privileged containers, host network access, and dangerous capabilities (CAP_SYS_ADMIN, CAP_NET_RAW), with admission controllers validating resource requests and OPA (Open Policy Agent) enforcing custom policies preventing sidecar injection attacks and ensuring mTLS configuration on all ingress/egress traffic. SEPP (Security Edge Protection Proxy) deployment at network boundary implements N32 interface security for roaming scenarios, performing TLS termination with forward secrecy (ECDHE key exchange), JSON Web Token (JWT) validation with RS256 signature algorithm (2048-bit RSA), and message filtering blocking malformed SUPI concealment attempts from visited networks. Quantum-safe cryptography preparedness implements hybrid key exchange combining classical ECDHE P-256 with post-quantum CRYSTALS-Kyber algorithm providing 128-bit quantum security strength, protecting against future quantum computer attacks on current TLS 1.3 sessions with estimated 10-year cryptographic lifetime. Hardware security modules (Thales Luna HSM 7) protect AMF master keys with FIPS 140-2 Level 3 certification, enforcing quorum authentication requiring 3-of-5 smart card holders to access root keys, generating 10,000 derived keys/second for subscriber authentication with key backup in geographically separated facility utilizing Shamir's Secret Sharing (5-of-9 threshold). Insider threat mitigation implements privileged access management (CyberArk PAM) requiring just-in-time elevation for administrative operations with approval workflow (manager + security officer), session recording of all CLI commands and GUI clicks, and behavioral analytics detecting anomalous patterns (bulk subscriber data export, configuration changes outside maintenance windows). Supply chain security validates equipment authenticity through TPM-based device identity certificates issued during manufacturing, inspecting baseband firmware signatures against Ericsson/Nokia public keys stored in hardware root of trust, and maintaining vendor-signed bill of materials (SBOM) enabling rapid identification of vulnerable components (e.g., Log4j CVE-2021-44228 affecting management interfaces). Compliance framework addresses regulatory requirements: GDPR Article 32 mandates encryption at rest and in transit, CCPA requires subscriber data deletion within 45 days of request (implemented through UDM data purge API), 47 CFR Part 8 (Network Neutrality) enforces non-discriminatory traffic handling with PCF policy auditing, and Executive Order 14028 mandates SBOM transparency and vulnerability disclosure within 24 hours of discovery. Security metrics dashboard tracks KPIs: authentication success rate (target >99.9%), security context establishment latency (target <200ms), certificate expiration events (target zero), vulnerability remediation time (Critical <7 days, High <30 days), security incident response time (detection to containment <1 hour), and penetration test findings (target <5 High severity per quarter).
