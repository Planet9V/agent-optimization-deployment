# 5G Network Architecture - Communications Sector

## Entity-Rich Introduction

5G Standalone (SA) network architecture implements Service-Based Architecture (SBA) defined by 3GPP Release 15/16 specifications, decomposing monolithic 4G EPC functions into cloud-native microservices with RESTful APIs enabling horizontal scaling and vendor interoperability. Radio Access Network utilizes gNodeB base stations (Ericsson AIR 3268, Nokia AirScale ABIA) connecting to 5G Core via N2 interface transporting NGAP control messages and N3 interface carrying GTP-U encapsulated user plane traffic through disaggregated CU-DU-RU architecture with fronthaul eCPRI protocol over 25 Gbps Ethernet. 5G Core Network Functions deploy on Red Hat OpenShift 4.12 Kubernetes platform running containerized AMF (Access and Mobility Management Function) handling 200,000 registrations/second, SMF (Session Management Function) managing 15 million PDU sessions, and UPF (User Plane Function) processing 600 Gbps throughput with DPDK packet acceleration. Network slicing capability creates logically isolated end-to-end networks sharing physical infrastructure: eMBB slice (S-NSSAI SST=1) for consumer broadband with best-effort QoS, URLLC slice (SST=2) for industrial automation requiring <1ms latency and 99.9999% reliability, mMTC slice (SST=3) for IoT sensors supporting 1 million devices per km² with 10-year battery life.

## Technical Specifications

**5G Service-Based Architecture Network Functions**:
- AMF (Access and Mobility Management): Registration, connection, mobility, reachability management
- SMF (Session Management Function): Session establishment, modification, release, IP address allocation
- UPF (User Plane Function): Packet routing, forwarding, QoS enforcement, usage reporting
- PCF (Policy Control Function): Policy rules, QoS parameters, charging control
- UDM (Unified Data Management): Subscription data, authentication credentials, context management
- AUSF (Authentication Server Function): 5G-AKA authentication, credential verification
- NEF (Network Exposure Function): External API exposure, capability negotiation
- NRF (Network Repository Function): Service discovery, registration, authorization
- NSSF (Network Slice Selection Function): Slice selection, NSSAI validation
- UDR (Unified Data Repository): Unified data storage supporting UDM/PCF/NEF
- CHF (Charging Function): Online/offline charging, quota management, CDR generation
- SEPP (Security Edge Protection Proxy): Inter-PLMN security, N32 interface protection

**5G Core Interfaces (Service-Based)**:
- Namf: AMF services (communication, event exposure, location, MT)
- Nsmf: SMF services (PDU session, event exposure)
- Nausf: AUSF services (UE authentication, SoR protection)
- Nudm: UDM services (subscriber data management, UE context management)
- Nnrf: NRF services (NFDiscovery, NFManagement, AccessToken)
- Npcf: PCF services (AM policy, SM policy, UE policy, BDT policy)
- Naf: Application function services (traffic influence, event exposure)
- HTTP/2: All SBI using HTTP/2 with TLS 1.3 mandatory encryption
- REST APIs: JSON payloads, OAuth 2.0 authentication, rate limiting

**RAN Architecture (CU-DU-RU Split)**:
- RU (Radio Unit): RF transmission, beamforming, antenna integration (Ericsson AIR 3268)
- DU (Distributed Unit): PHY-High, MAC, RLC layers, real-time L1 processing
- CU (Centralized Unit): PDCP, SDAP, RRC layers, non-real-time functions
- CU-CP: Control plane functions, RRC, PDCP-C
- CU-UP: User plane functions, PDCP-U, SDAP
- F1 Interface: F1-C (control plane), F1-U (user plane) between CU and DU
- Fronthaul: eCPRI over Ethernet (25 Gbps) or CPRI (option 7/8/10)
- Midhaul: F1 interface using IP/Ethernet, typical 10-50 km distance

**Network Slicing Architecture**:
- Slice Types: eMBB (SST=1), URLLC (SST=2), mMTC (SST=3), V2X (SST=4)
- S-NSSAI: Single NSSAI identifying slice (8-bit SST + 24-bit SD)
- NSSAI: Network Slice Selection Assistance Information (up to 8 S-NSSAIs)
- Slice Isolation: Dedicated compute/network resources per slice type
- Slice Admission: PCF controls per-slice subscriber authorization
- Slice SLA: eMBB (1 Gbps, 20ms), URLLC (10 Mbps, 1ms, 99.9999%), mMTC (100 kbps, 10s)
- Resource Allocation: Dedicated RAN PRBs, core UPF instances, transport bandwidth

**Transport Network Architecture**:
- Fronthaul: 25 Gbps eCPRI, sub-100 μs latency, IEEE 1588v2 PTP synchronization
- Midhaul: 10-100 Gbps Ethernet, <10ms latency, MPLS/Segment Routing
- Backhaul: 100 Gbps Ethernet/DWDM, <20ms latency, redundant paths
- Routers: Cisco ASR 9000, Juniper MX960, Nokia 7750 SR with 100GE interfaces
- Synchronization: PTP Grandmaster (Microsemi TimeProvider 4100), ±50 ns accuracy
- QoS: Diffserv marking (DSCP values), weighted fair queuing, traffic shaping

**Cloud Infrastructure and Orchestration**:
- Container Platform: Red Hat OpenShift 4.12, Kubernetes 1.25
- Compute: Intel Xeon Scalable (Ice Lake), 128 cores, 512 GB RAM per server
- Storage: Ceph distributed storage, 3-replica data protection, NVMe SSDs
- Networking: SR-IOV, DPDK for user plane acceleration (40 Gbps per UPF pod)
- Orchestration: ONAP (Open Network Automation Platform), ETSI NFV MANO
- CI/CD: Jenkins pipelines, GitLab version control, Helm charts
- Monitoring: Prometheus metrics, Grafana dashboards, Elasticsearch logs
- Availability: Active-active geo-redundancy, pod anti-affinity, auto-healing

## Integration & Operations

5G Standalone network deployment across nationwide carrier infrastructure (MNO-5G-SA-01) implements three-tier architecture with centralized 5G Core functions hosted in 3 regional data centers (DC-EAST, DC-CENTRAL, DC-WEST) providing active-active redundancy, 25 edge UPF locations positioned 15-50 km from metro areas enabling <10ms latency for latency-sensitive applications, and 50,000 gNodeB sites distributing radio coverage across urban/suburban/rural territories. AMF instances deployed in Kubernetes cluster (15-node OpenShift cluster per DC) handle N1/N2 interface traffic from gNodeB base stations utilizing NGAP protocol transporting NAS messages, with horizontal pod autoscaling maintaining <50ms registration latency during peak hours (8-10 AM, 5-7 PM) processing 200,000 registration requests/second across nationwide footprint. SMF integration with edge UPF implements Local Breakout architecture routing enterprise traffic directly to local data networks via N6 interface bypassing core transport, with N4 PFCP (Packet Forwarding Control Protocol) session establishment messages installing packet detection rules (PDR), forwarding action rules (FAR), QoS enforcement rules (QER), and usage reporting rules (URR) enabling granular traffic steering based on application signatures (HTTP, HTTPS, gaming protocols). Network slicing deployment provisions 3 production slices: eMBB slice utilizing shared RAN resources (60% PRB allocation) and best-effort core QoS (5QI=9), URLLC slice with dedicated RAN PRBs (20% allocation) and guaranteed-bit-rate core policy (5QI=1, 100 Mbps GBR, <10ms latency), mMTC slice optimized for IoT devices with extended idle-mode DRX (Discontinuous Reception) cycles reducing power consumption 90% enabling 10-year battery operation for NB-IoT sensors. Service-Based Interface communication between network functions utilizes HTTP/2 protocol over TLS 1.3 mutual authentication, with NRF (Network Repository Function) providing service discovery enabling AMF to discover available SMF instances supporting required S-NSSAI, and PCF to locate UDR instances storing subscription data with OAuth 2.0 access tokens authorizing API invocations. Disaggregated RAN architecture deploys Ericsson Radio System with centralized baseband processing: RU (AIR 3268 Remote Radio Unit) mounted on cell tower transmitting 200W RF power at 3.5 GHz, DU (Distributed Unit) located in street cabinet 2 km distant performing real-time PHY-High/MAC/RLC processing with <250 μs processing latency, CU (Centralized Unit) hosted in regional data center 25 km away executing non-real-time PDCP/RRC functions with F1 interface eCPRI transport over 25 Gbps Ethernet fiber. Fronthaul network synchronization utilizes IEEE 1588v2 PTP (Precision Time Protocol) distribution from Microsemi TimeProvider 4100 Grandmaster Clock with GPS/GNSS input providing ±50 ns time accuracy to RU/DU equipment, essential for TDD frame timing alignment and carrier aggregation across non-collocated cells requiring <3 μs time synchronization tolerance. Performance monitoring infrastructure collects 25,000 KPI metrics every 15 minutes from 100,000 network elements including gNodeB KPIs (cell availability 99.95%, RACH success rate 99%, handover success 98%), Core KPIs (AMF registration success 99.9%, SMF session establishment success 99.5%, UPF throughput 600 Gbps), and Transport KPIs (fiber link utilization 60%, packet loss <0.01%, latency <10ms), feeding Ericsson Expert Analytics ML platform predicting capacity exhaustion 6 weeks in advance.

## Security Implementation

5G Core security architecture implements zero-trust principles with service mesh (Istio 1.17) enforcing mutual TLS authentication between all microservices, automatically rotating X.509 certificates every 24 hours using Kubernetes cert-manager with Let's Encrypt ACME protocol, and encrypting all inter-pod communication with TLS 1.3 using ECDHE key exchange and AES-256-GCM cipher suite. Network function security hardens container images following CIS Kubernetes Benchmark with minimal base images (Alpine Linux 3.17, 10 MB size), running as non-root user (UID 1000), read-only root filesystem, and dropping all Linux capabilities except CAP_NET_BIND_SERVICE, with automated vulnerability scanning (Aqua Security Trivy) blocking container deployment if High/Critical CVEs detected. Kubernetes security controls implement Pod Security Policies restricting privileged containers, host network access, and hostPath volume mounts, with admission controllers validating resource requests/limits preventing resource exhaustion attacks, and OPA (Open Policy Agent) enforcing custom policies requiring security context definitions, image signature validation, and mTLS configuration on ingress/egress routes. API security on Service-Based Interfaces implements OAuth 2.0 framework with NRF issuing JWT access tokens (RS256 signature algorithm with 2048-bit RSA keys) to network functions, enforcing scope-based authorization (e.g., namf-comm scope for AMF communication service), rate limiting to 10,000 requests/second per NF instance, and API gateway (Kong) providing centralized authentication, request validation, and DDoS protection. SEPP (Security Edge Protection Proxy) deployment at network boundary secures inter-operator roaming scenarios implementing N32 interface protection with TLS handshake using operator-issued certificates, JSON Web Token validation with signature verification, topology hiding removing internal PLMN addresses from SBI messages, and message filtering blocking malformed requests preventing exploitation of known vulnerabilities (CVE-2019-14899 GTP tunneling attack). Transport network security employs MACsec (IEEE 802.1AE) encryption with GCM-AES-256 on fronthaul eCPRI links protecting timing synchronization (PTP) and control plane traffic from man-in-the-middle attacks, IPsec VPN tunnels (IKEv2 with X.509 authentication, ESP with AES-256-GCM) encrypting midhaul F1 interface traffic between DU and CU, and MPLS Layer 3 VPN (RFC 4364) with BGP route authentication isolating mobile backhaul traffic from internet services. User plane security implements end-to-end encryption with NEA2 (128-bit AES-CTR) or NEA3 (128-bit ZUC) ciphering algorithms protecting user data between UE and gNodeB with per-PDU-session keys derived from KAMF through KDF (Key Derivation Function), integrity protection using NIA2 (AES-CMAC) or NIA3 (ZUC) generating 32-bit MAC-I tags appended to RRC/NAS messages detecting tampering attempts. Subscriber authentication executes 5G-AKA protocol with AUSF validating UE credentials stored in UDM, deriving 256-bit KAUSF anchor key from permanent key K in USIM, and distributing keys to AMF (KAMF) and subsequently to gNodeB (KgNB) enabling air interface encryption activation, with SUCI (Subscription Concealed Identifier) protecting IMSI using ECIES public key encryption (Curve25519) preventing IMSI catchers from tracking subscribers. Hardware security modules (Thales Luna HSM 7) protect cryptographic material with FIPS 140-2 Level 3 certification, storing AMF/SMF/UPF root keys in tamper-resistant hardware, enforcing quorum authentication (3-of-5 smart cards) for key access, and generating 10,000 derived keys/second for subscriber authentication with automatic key backup to geographically separated facility. Security monitoring deploys Splunk Enterprise Security SIEM aggregating logs from 100,000 network elements generating 50 million events/hour, correlating authentication failures (>5 failed attempts in 60 seconds triggers account lockout), API abuse patterns (rate limit violations, invalid token usage), configuration changes (unauthorized parameter modifications detected through configuration baseline comparison), and security events (IDS alerts, certificate expirations, vulnerability scan findings). Compliance framework addresses regulatory requirements including GDPR Article 32 mandating encryption at rest and in transit, lawful intercept capability (ETSI TS 103 221-1) providing authorized access to communication content for law enforcement with warrant, CALEA compliance for US carriers requiring mediation function deployment, and 3GPP SECAM (Security Assurance Methodology) validation of security controls through independent testing labs.
