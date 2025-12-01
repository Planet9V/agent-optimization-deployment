# Food/Agriculture Sector - Network Segmentation & Architecture Security

## Document Metadata
- **Created**: 2025-11-05
- **Version**: 1.0.0
- **Category**: Security - Network Architecture
- **Sector**: Food/Agriculture
- **Pattern Count**: 55+

## Overview
Network segmentation strategies for food processing facilities, implementing Purdue Model and defense-in-depth for OT environments with food safety criticality.

## Network Architecture Patterns

### 1. Purdue Model Implementation for Food Processing

#### Pattern: Five-Level Food Processing Network Architecture
```yaml
pattern_id: FOOD-NET-001
name: Purdue Model Food Processing Adaptation
description: ISA-95/Purdue model applied to food manufacturing
severity: CRITICAL
architecture_levels:
  level_0_process:
    description: Physical processes and field devices
    food_specific_equipment:
      - Temperature sensors (RTDs, thermocouples) in pasteurizers
      - Flow meters in CIP systems
      - Load cells for ingredient weighing
      - pH probes in fermentation tanks
      - Oxygen sensors in modified atmosphere packaging
    security_characteristics:
      - Typically no TCP/IP networking (4-20mA, digital I/O)
      - Physical security primary control
      - Limited cybersecurity applicability at sensor level
      - Tamper-evident seals on critical sensors

  level_1_control:
    description: PLCs, DCS, RTUs controlling processes
    food_equipment_examples:
      - Siemens S7-1500 for aseptic filling lines (Tetra Pak)
      - Allen-Bradley CompactLogix for packaging lines
      - GEA SMARTCONTROL for pasteurization systems
      - Schneider Electric PLCs for cold storage
    network_protocols:
      - EtherNet/IP for Allen-Bradley systems
      - Profinet for Siemens ecosystems
      - Modbus TCP for multi-vendor integration
      - OPC UA for data exchange
    security_controls:
      network_segmentation:
        - Separate VLAN per production line
        - Industrial firewalls between lines (Claroty, Nozomi, Dragos)
        - Unidirectional gateways for data export
      access_control:
        - Locked PLC programs (password protection + physical locks)
        - Change control process for logic modifications
        - Backup before any programming changes
      monitoring:
        - PLC CPU status monitoring
        - Unauthorized program download alerts
        - Abnormal Modbus/Profinet traffic detection

  level_2_supervision:
    description: SCADA, HMI, MES systems
    food_applications:
      - HMI for operator control (WinCC, FactoryTalk View)
      - SCADA for facility-wide monitoring
      - Historian for regulatory compliance (OSIsoft PI, Aveva Historian)
      - MES for batch tracking (Syncade, Werum PAS-X)
    security_architecture:
      dmz_approach:
        - Jump servers for operator access to Level 1
        - Data historians in DMZ (read-only from Level 1)
        - Application servers (MES, SCADA) in protected zone
        - Firewall rules allowing only necessary protocols
      hardening_measures:
        - Windows Server 2019+ with monthly patching
        - Application whitelisting (AppLocker, ThreatLocker)
        - Antivirus with OT-aware signatures (Tenable OT Security)
        - Disabled unnecessary services (Print Spooler, Remote Desktop)
      backup_and_recovery:
        - Daily incremental backups to isolated network
        - Weekly full VM backups
        - Quarterly disaster recovery testing
        - 3-2-1 backup rule (3 copies, 2 media types, 1 offsite)

  level_3_operations:
    description: MES, ERP, quality systems
    food_business_systems:
      - SAP S/4HANA for enterprise resource planning
      - Oracle JD Edwards for food distribution
      - Infor LN for process manufacturing
      - TraceGains for supplier quality management
      - FoodLogiQ for supply chain traceability
    integration_points:
      - OPC UA servers bridging Level 2 and Level 3
      - REST APIs for mobile quality applications
      - SOAP web services for third-party integrations
      - File-based transfers (SFTP) for legacy systems
    security_controls:
      api_security:
        - OAuth 2.0 authentication for modern APIs
        - API gateway (Kong, Apigee) for rate limiting
        - TLS 1.3 for encrypted communication
        - JSON Web Tokens (JWT) for stateless authentication
      data_protection:
        - Database encryption at rest (TDE for SQL Server/Oracle)
        - Field-level encryption for sensitive data (supplier pricing)
        - Data masking for non-production environments
        - Backup encryption (Veeam, Commvault)

  level_4_enterprise:
    description: Corporate IT systems
    food_industry_applications:
      - Microsoft 365 for productivity
      - Salesforce for customer relationship management
      - Tableau/Power BI for business intelligence
      - Concur for expense management
      - Active Directory for identity management
    isolation_strategy:
      - Completely separate network from OT (Levels 0-3)
      - No direct connectivity between Level 4 and Level 1
      - Data replication via secure DMZ (Level 3.5)
      - VPN for remote employee access (not for OT systems)
    security_posture:
      - Enterprise-grade cybersecurity stack (EDR, SIEM, DLP)
      - Regular penetration testing (annual external, quarterly internal)
      - Security awareness training (monthly phishing simulations)
      - Zero Trust architecture implementation (gradual rollout)

network_diagram_example: |
  ┌────────────────────────────────────────────────────────┐
  │ Level 4: Enterprise Network (Corporate IT)            │
  │ - Office 365, Salesforce, Active Directory            │
  └────────────────┬───────────────────────────────────────┘
                   │ (Firewall, IPS, Data Diode)
  ┌────────────────▼───────────────────────────────────────┐
  │ Level 3.5: DMZ / Data Exchange Zone                    │
  │ - OT Data Warehouse, API Gateways, Jump Servers       │
  └────────────────┬───────────────────────────────────────┘
                   │ (Industrial Firewall)
  ┌────────────────▼───────────────────────────────────────┐
  │ Level 3: Operations Management                         │
  │ - MES, ERP Integration, Quality Systems (SAP, Oracle)  │
  └────────────────┬───────────────────────────────────────┘
                   │ (OPC UA Gateway, Unidirectional Gateway)
  ┌────────────────▼───────────────────────────────────────┐
  │ Level 2: Supervisory Control                           │
  │ - SCADA, HMI, Historian (WinCC, PI System)            │
  └──┬───────────┬───────────┬───────────┬────────────────┘
     │ (Firewall) │ (Firewall) │ (Firewall) │
  ┌──▼─────────┐ ┌▼─────────┐ ┌▼─────────┐ ┌▼──────────────┐
  │ Level 1:    │ │ Level 1:  │ │ Level 1:  │ │ Level 1:      │
  │ Pasteurization│ Packaging │ │ Cold Chain│ │ CIP System    │
  │ PLC Network│ │ PLC Network│ │ Refrigeration│ PLCs          │
  └──┬─────────┘ └┬─────────┘ └┬─────────┘ └┬──────────────┘
     │            │            │            │
  ┌──▼────────────▼────────────▼────────────▼────────────────┐
  │ Level 0: Physical Process                                │
  │ - Sensors, Actuators, Valves (4-20mA, Profinet, etc.)   │
  └──────────────────────────────────────────────────────────┘

implementation_considerations:
  greenfield_facility:
    - Implement full Purdue model from design phase
    - Specify industrial-grade network equipment (Cisco IE, Hirschmann)
    - Plan for future expansion (extra switch ports, cable pathways)
    - Document as-built network diagrams in CAD format
  brownfield_retrofit:
    - Phase approach: Start with critical systems (pasteurization, CIP)
    - Use existing cabling where possible (managed switches for VLANs)
    - Temporary bypass paths during cutover (minimize downtime)
    - Parallel operation of old and new systems during validation
  resource_constraints:
    - Prioritize Level 0-1 segmentation (highest food safety risk)
    - Use software firewalls on HMI/SCADA servers if budget-limited
    - Open-source SIEM for initial monitoring (Security Onion)
    - Gradual upgrade path to enterprise solutions

compliance_validation:
  nist_csf_alignment:
    - PR.AC-5: Network integrity is protected (segmentation)
    - PR.DS-5: Protections against data leaks implemented
    - DE.CM-1: Network monitored to detect potential events
  iec_62443:
    - SL 2 (Security Level 2) minimum for food processing
    - SL 3 for critical safety systems (pasteurization, CIP)
    - Conduit and zone concept implementation
```

#### Pattern: Cold Storage Network Isolation
```yaml
pattern_id: FOOD-NET-002
name: Cold Chain Network Segmentation
description: Isolated refrigeration control network with safety interlocks
severity: CRITICAL
network_topology:
  primary_control_network:
    description: Main refrigeration PLC network
    equipment_connected:
      - Compressor control PLCs (Danfoss, Emerson, Frick)
      - Evaporator control panels
      - Defrost controllers
      - Ammonia leak detection system
    network_specifications:
      - Dedicated industrial Ethernet switches (Cisco IE-4000)
      - Fiber optic backbone for electrical isolation
      - Ring topology for redundancy (RSTP/ERPS)
      - 1 Gbps bandwidth (low latency for safety systems)
    security_controls:
      - MAC address filtering on switches
      - Port security (one device per port)
      - Disabled unused switch ports
      - DHCP snooping enabled (prevent rogue DHCP servers)

  safety_instrumented_system_network:
    description: Independent SIS network (SIL 2 rated)
    critical_functions:
      - High-pressure shutdown of compressors
      - Emergency ventilation activation on ammonia leak
      - Personnel evacuation alarm system
      - Valve interlocks preventing overpressure
    network_characteristics:
      - Physically separate from control network (no shared switches)
      - Dedicated safety PLC (Allen-Bradley GuardLogix, Siemens FailSafe)
      - Hardwired inputs/outputs (no wireless, no TCP/IP where possible)
      - Black-start capability (operates without control network)
    access_restrictions:
      - Safety PLC programming requires hardware key
      - Two-person authorization for safety logic changes
      - Independent safety engineer approval for modifications
      - Annual safety system proof test (TÜV/IEC 61508 validation)

  wireless_sensor_network:
    description: Temperature monitoring Wi-Fi network
    use_cases:
      - Wireless temperature/humidity sensors (Monnit, SensoScientific)
      - Mobile quality tablets (inspectors, QA personnel)
      - Handheld barcode scanners (receiving/shipping)
    security_challenges:
      - Unencrypted 433 MHz sensors (legacy equipment)
      - Wi-Fi 2.4 GHz congestion and interference
      - Battery-powered devices (limited computational power)
    hardening_approach:
      - Separate SSID for sensors (WPA3-Enterprise with RADIUS)
      - 802.1X authentication for mobile devices
      - Network Access Control (NAC) for device posture checking
      - VLAN tagging for sensor traffic (isolated from control network)

  remote_monitoring_network:
    description: Alarm notification and offsite monitoring
    business_requirements:
      - 24/7 monitoring for after-hours temperature alarms
      - Facility manager mobile app (iOS/Android)
      - Email/SMS notifications for critical events
      - Third-party monitoring service integration (EMCS, Phonics)
    security_architecture:
      - Read-only data export from refrigeration network
      - One-way data diode hardware (Owl Cyber Defense)
      - VPN for remote access (MFA required, Cisco AnyConnect)
      - Rate limiting on alarm notifications (prevent DoS via SMS)
    threat_considerations:
      - Public internet exposure of monitoring portals
      - Weak passwords on alarm receiver accounts
      - Lack of encryption on legacy modem-based systems
      - Social engineering attacks via fake alarm calls

segmentation_enforcement:
  firewall_rules:
    level_1_to_level_2:
      allow:
        - Modbus TCP (port 502) from PLC to SCADA (read-only)
        - OPC UA (port 4840) with authentication
        - SNMP traps (port 162) for equipment alerts
      deny:
        - All other inbound connections to Level 1
        - Outbound internet access from PLCs
        - Lateral movement between PLC VLANs
    level_2_to_level_3:
      allow:
        - OPC UA client connections from MES (port 4840)
        - Database replication (SQL Server, port 1433) with TLS
        - File transfers via SFTP (port 22) for batch records
      deny:
        - Direct access from Level 3 to Level 1 (must go through Level 2)
        - Unauthenticated protocols (Telnet, FTP, HTTP)
    dmz_to_external:
      allow:
        - HTTPS (port 443) for remote monitoring dashboard
        - Email (port 587 with STARTTLS) for alarm notifications
        - VPN (port 443 for SSL VPN, 1194 for OpenVPN)
      deny:
        - Inbound connections to production networks
        - Any protocol exposing control system directly to internet

monitoring_and_detection:
  network_visibility:
    - Passive network taps at key points (Gigamon, Garland Technology)
    - Industrial protocol dissection (Nozomi Networks, Claroty)
    - Baseline traffic patterns (normal vs. anomalous)
  alerting_rules:
    - New device detected on production network
    - Unauthorized Modbus/Profinet commands
    - Excessive failed login attempts to HMI
    - Unusual traffic volume spikes
    - Communication with known malicious IPs (threat intelligence feeds)
  siem_integration:
    - Log aggregation from firewalls, switches, PLCs
    - Correlation rules for multi-stage attacks
    - Compliance reporting (audit queries for FDA inspections)
    - Incident response playbooks triggered by alerts

disaster_recovery:
  backup_strategies:
    - PLC program backups (weekly, stored offline)
    - Switch configuration backups (automatic on change)
    - Firewall rule exports (version controlled in Git)
    - Network topology documentation (Visio diagrams)
  recovery_procedures:
    - Maximum tolerable downtime (MTD): 4 hours for cold storage
    - Recovery Time Objective (RTO): 2 hours for critical systems
    - Recovery Point Objective (RPO): 15 minutes (minimal data loss)
  cold_site_capabilities:
    - Spare PLCs pre-configured with baseline programs
    - Backup switches with tested configurations
    - Emergency contact list for vendors (24/7 support numbers)
    - Runbooks for manual refrigeration operation (if control system down)
```

### 2. Industrial DMZ Architectures

#### Pattern: OT Data Exchange Zone
```yaml
pattern_id: FOOD-NET-003
name: Secure OT/IT Data Exchange DMZ
description: Demilitarized zone for safe data flow between OT and IT networks
severity: HIGH
business_drivers:
  - Real-time production dashboards for plant managers (IT network access)
  - ERP integration for material consumption tracking (SAP, Oracle)
  - Quality data reporting to corporate quality systems
  - Regulatory compliance data export (FDA electronic records)
  - Remote vendor access for equipment troubleshooting
dmz_components:
  data_historians:
    purpose: Store time-series process data for analysis
    products:
      - OSIsoft PI System (most common in food industry)
      - Aveva Historian (formerly Wonderware)
      - GE Proficy Historian
      - Ignition by Inductive Automation
    data_sources:
      - PLC tags via OPC UA/DA (temperature, pressure, flow rates)
      - Energy meters (electricity, gas, steam consumption)
      - Equipment status (running, stopped, faulted)
      - Production counts and quality metrics
    data_consumers:
      - Business intelligence tools (Tableau, Power BI)
      - MES/ERP systems (SAP, Oracle)
      - Corporate dashboards (executive KPIs)
      - Regulatory reporting systems
    security_configuration:
      - Interfaces in DMZ (collectors on OT side, distributors on IT side)
      - OT-side interface read-only (cannot write to PLCs)
      - IT-side interface authenticated access only
      - Data replication with encryption (TLS 1.3)
      - Historical data retention policies (7 years for FDA compliance)

  opc_ua_gateway:
    purpose: Protocol translation and security enforcement
    functionality:
      - Convert proprietary protocols (Modbus, Profinet) to OPC UA
      - Aggregate data from multiple PLCs
      - Enforce OPC UA security policies (Sign & Encrypt)
      - Rate limiting to prevent data flooding
    deployment_model:
      - Primary gateway in Level 2 (OT network)
      - Secondary gateway in DMZ (for IT access)
      - No direct OT-to-IT OPC UA connections
    security_features:
      - User authentication with X.509 certificates
      - Application authentication (prevent rogue clients)
      - Data encryption (AES-256)
      - Audit logging of all read/write operations
    vendor_examples:
      - Kepware (PTC ThingWorx)
      - MatrikonOPC (Honeywell)
      - Prosys OPC UA SDK

  jump_servers:
    purpose: Controlled access point for IT personnel to OT systems
    use_cases:
      - IT staff troubleshooting SCADA server issues
      - Database administrators managing historian databases
      - Cybersecurity team conducting vulnerability scans
    security_architecture:
      - Dual-NIC configuration (one NIC on IT network, one on OT network)
      - Session recording (video capture of all activities)
      - Privileged access management (CyberArk, BeyondTrust)
      - Time-restricted access (business hours only, exceptions approved)
    hardening_measures:
      - Windows Server 2022 with latest patches
      - Application whitelisting (only RDP client, SSH client allowed)
      - Disabled clipboard, file transfer (unless explicitly approved)
      - Multi-factor authentication (hardware tokens preferred)

  unidirectional_gateways:
    purpose: Hardware-enforced one-way data flow (OT → DMZ, never reverse)
    technology:
      - Fiber optic transceivers with transmit laser disabled on OT side
      - Data diode hardware (Owl Cyber Defense, Waterfall Security)
      - Protocol proxy on both sides (reconstruct TCP sessions)
    deployment_scenarios:
      - Critical safety data export (never allow writes back to safety PLCs)
      - High-security facilities (defense, critical infrastructure)
      - Compliance requirements (NERC CIP for power utilities)
    limitations:
      - No bidirectional protocols (HTTP requests, database queries)
      - Requires application layer proxies for request/response patterns
      - Higher cost and complexity than firewalls
    food_industry_applicability:
      - Recommended for: Pasteurization systems, water treatment
      - Optional for: Packaging lines, warehouse management
      - Cost-benefit analysis needed (typically $50K-$200K per gateway)

dmz_network_design:
  firewall_architecture:
    - Dual firewalls: OT firewall (between Level 1-2 and DMZ), IT firewall (between DMZ and Level 3-4)
    - Vendor diversity (different firewall brands to prevent single exploit compromising both)
    - High availability (active/passive or active/active clustering)
  network_topology:
    - Separate VLANs for each DMZ service (historian VLAN, OPC VLAN, jump server VLAN)
    - No direct routing between DMZ VLANs (must traverse firewall)
    - Isolated management network for firewall/switch administration
  bandwidth_planning:
    - 1 Gbps typical for data historian replication
    - 100 Mbps sufficient for OPC UA tag updates (thousands of tags)
    - Burst capacity for video session recording (10-50 Mbps per session)

access_control_matrix:
  it_to_dmz:
    allowed_services:
      - HTTPS (port 443) to historian web interface
      - SQL Server (port 1433) to historian database (read-only)
      - RDP (port 3389) to jump servers (MFA required)
    denied_services:
      - Any direct access to OT network (Level 0-2)
      - Modbus, Profinet, EtherNet/IP protocols
  dmz_to_ot:
    allowed_services:
      - OPC DA/UA (ports 4840, 135, dynamic RPC ports) from historian collectors
      - SNMP (port 161) for device monitoring (read-only)
    denied_services:
      - HTTP/HTTPS (web browsing from DMZ to OT HMIs)
      - PLC programming protocols (S7, Logix5000)
  ot_to_dmz:
    allowed_services:
      - Data historian writes (OPC UA, port 4840)
      - Syslog (port 514) for event forwarding
      - NTP (port 123) for time synchronization
    denied_services:
      - Outbound internet access
      - Email (SMTP) to prevent malware command-and-control

data_governance:
  classification:
    - Public: Aggregated production statistics (no customer/supplier data)
    - Internal: Detailed process parameters (competitive advantage if leaked)
    - Confidential: Supplier contracts, pricing, formulations
    - Restricted: Food safety investigation data (FDA confidential)
  retention_policies:
    - Historian data: 7 years (FDA 21 CFR Part 11 requirement)
    - Audit logs: 3 years minimum (SOX compliance if public company)
    - Video session recordings: 90 days (storage cost optimization)
  export_controls:
    - Data loss prevention (DLP) scanning on IT firewall
    - Watermarking of sensitive documents
    - Encrypted email for external data sharing (S/MIME, PGP)
```

#### Pattern: Vendor Remote Access DMZ
```yaml
pattern_id: FOOD-NET-004
name: Third-Party Vendor Access Isolation
description: Secure remote access for Tetra Pak, GEA, John Deere technicians
severity: CRITICAL
business_justification:
  - Minimize equipment downtime (24/7 vendor support availability)
  - Reduce travel costs ($2K-$5K per on-site visit)
  - Faster issue resolution (vendor experts remote diagnostic capabilities)
  - Knowledge transfer (vendors train internal staff remotely)
security_challenges:
  - Vendors may have less mature cybersecurity practices
  - Multiple vendors accessing same network (cross-contamination risk)
  - Difficult to enforce MFA on vendor accounts
  - Vendor employees turnover (orphaned accounts)
architecture_components:
  vendor_remote_access_server:
    technology_options:
      - TeamViewer Tensor (enterprise version with MFA, session recording)
      - BeyondTrust Bomgar (privileged access management)
      - Citrix Virtual Apps (application-level access, not full desktop)
      - Cisco AnyConnect VPN (with Duo MFA integration)
    deployment:
      - Dedicated server in vendor DMZ (separate from OT data DMZ)
      - Application-level access only (vendors see HMI screens, not full OS)
      - No internet browsing capability during sessions
      - Copy/paste and file transfer disabled by default

  vendor_jump_hosts:
    per_vendor_isolation:
      - Separate jump host VM for each major vendor (Tetra Pak, GEA, John Deere)
      - Prevents cross-vendor access and lateral movement
      - Vendor-specific software pre-installed (Siemens TIA Portal for GEA, Studio 5000 for John Deere)
    access_controls:
      - Vendors cannot access jump host directly (must request session)
      - Internal technician "co-pilots" vendor sessions (monitor activities)
      - Session initiation requires approval workflow (email/SMS to plant manager)

  session_monitoring:
    real_time_oversight:
      - Video recording of all vendor sessions (Teramind, Splunk UBA)
      - Keystroke logging for audit trail
      - Screen capture on suspicious activities (e.g., accessing unauthorized systems)
    automated_analysis:
      - Detect PLC program downloads (alert if unauthorized)
      - Identify configuration file modifications (diff against baseline)
      - Flag unusual network traffic (port scans, lateral movement attempts)
    post_session_review:
      - Summary report generated automatically (duration, systems accessed, changes made)
      - Technical review by internal controls engineer
      - Approval before changes activated in production

access_request_workflow:
  step_1_vendor_request:
    - Vendor submits ticket via customer portal (description, urgency, systems affected)
    - Automatically creates ServiceNow ticket or Jira issue
    - Business justification required (e.g., "Production line down, $50K/hour revenue impact")

  step_2_approval_routing:
    - Low urgency: Production supervisor approval (4-hour SLA)
    - Medium urgency: Plant manager approval (2-hour SLA)
    - High urgency: 24/7 on-call manager approval (30-minute SLA)
    - Auto-approval for pre-authorized maintenance windows

  step_3_access_provisioning:
    - IT security generates temporary access token (4-hour expiration)
    - Vendor receives email with connection instructions
    - MFA challenge (SMS code or authenticator app)
    - Session launched with internal technician co-browsing

  step_4_session_execution:
    - Vendor performs troubleshooting/configuration changes
    - Internal technician documents activities in real-time notes
    - Screen recording archived to secure storage

  step_5_post_session_validation:
    - Vendor actions summary reviewed by controls engineer
    - Changes tested in safe mode (if applicable)
    - Production restart authorization by plant manager
    - Ticket closed with root cause and resolution documented

vendor_management_program:
  onboarding:
    - Vendor cybersecurity assessment (annual questionnaire)
    - Contractual requirements for data handling and access
    - Vendor employee background check attestation
    - Insurance verification (cyber liability coverage)

  account_lifecycle:
    - Vendor accounts tied to specific employees (no shared "vendor" account)
    - Quarterly access reviews (deactivate unused accounts)
    - Annual password reset requirement
    - Immediate account termination upon vendor employee departure notification

  performance_metrics:
    - Mean time to resolution (MTTR) with remote access vs. on-site
    - Number of unauthorized access attempts (failed logins, policy violations)
    - Vendor session audit findings (issues discovered during reviews)
    - Cost savings from reduced vendor travel

technology_alternatives:
  high_security_option:
    - Unidirectional gateway (vendors can view diagnostic data, cannot modify)
    - Vendor recommendations submitted via ticketing system
    - Internal staff implements changes (no direct vendor access to production systems)
    - Use case: High-risk environments, critical safety systems

  moderate_security_option:
    - Read-only VPN access to SCADA/HMI screens
    - Change requests submitted for approval
    - Internal staff executes changes with vendor verbal/video guidance
    - Use case: Standard production environments

  lower_security_option:
    - Supervised remote desktop access to specific equipment controllers
    - Session recording and real-time monitoring
    - Vendors can make changes directly (with oversight)
    - Use case: Non-critical systems, trusted long-term vendor relationships

risk_mitigation_checklist:
  ☑ Vendor access limited to specific equipment (not full network)
  ☑ Multi-factor authentication enforced
  ☑ Session recording enabled and archived
  ☑ Real-time monitoring by internal staff
  ☑ Automatic session termination after timeout (4 hours)
  ☑ No internet access from vendor jump hosts
  ☑ Application whitelisting (only approved vendor software)
  ☑ Quarterly vendor security assessments
  ☑ Incident response plan for vendor account compromise
  ☑ Cyber insurance coverage for third-party risks
```

## Wireless Network Security Patterns

### 3. Industrial Wireless Networks

#### Pattern: Food Processing Facility Wi-Fi Segmentation
```yaml
pattern_id: FOOD-NET-005
name: Secure Wireless Network Design for Food Plants
description: Multi-SSID wireless architecture with role-based access
severity: MEDIUM
wireless_use_cases:
  production_floor:
    - Handheld barcode scanners (receiving, shipping, inventory)
    - Wireless temperature sensors (cold storage, processing areas)
    - Mobile quality tablets (line inspections, audit checklists)
    - Forklift-mounted terminals (warehouse operations)
  office_areas:
    - Employee laptops (plant managers, quality assurance staff)
    - Guest Wi-Fi (customer auditors, regulatory inspectors)
    - VoIP phones (wireless IP phones in non-production areas)
  maintenance:
    - Vendor laptops (temporary access during equipment servicing)
    - Portable vibration analyzers (predictive maintenance)
    - Handheld PLC programming devices (troubleshooting)
ssid_architecture:
  ssid_1_production_devices:
    name: PLANT-PROD-DEVICES
    authentication: WPA3-Enterprise (802.1X with RADIUS)
    vlan: VLAN 20 (production device network)
    authorized_devices:
      - Zebra mobile computers (barcode scanners)
      - Honeywell CT30 tablets (quality inspections)
      - Monnit wireless sensors (temperature/humidity)
    security_controls:
      - Device certificates (X.509) for authentication
      - MAC address filtering (whitelist only)
      - Captive portal disabled (device-to-device communication)
      - Wireless Intrusion Prevention System (wIPS) enabled

  ssid_2_employee_laptops:
    name: PLANT-STAFF-WIFI
    authentication: WPA3-Personal or WPA3-Enterprise
    vlan: VLAN 30 (staff network with internet access)
    authorized_users:
      - Plant managers, supervisors, office staff
      - Pre-registered devices (BYOD enrollment process)
    security_controls:
      - Active Directory integration (domain credentials)
      - Network Access Control (NAC) for device posture checking
      - Antivirus/EDR agent required
      - Internet content filtering (block malicious sites)

  ssid_3_guest_network:
    name: PLANT-GUEST
    authentication: WPA3-Personal (password rotated monthly)
    vlan: VLAN 40 (isolated guest network, internet-only access)
    authorized_users:
      - Customer auditors, regulatory inspectors
      - Vendor technicians (non-production systems)
    security_controls:
      - Completely isolated from production networks (firewall rules)
      - Bandwidth limiting (10 Mbps per client)
      - Web-based captive portal (user registration)
      - Session timeout (4 hours, re-authentication required)

  ssid_4_vendor_maintenance:
    name: PLANT-VENDOR (hidden SSID)
    authentication: WPA3-Enterprise with vendor certificates
    vlan: VLAN 50 (vendor access network, restricted to specific equipment)
    authorized_devices:
      - Pre-registered vendor laptops (by MAC address and certificate)
    security_controls:
      - Firewall rules limiting access to approved equipment only
      - Session logging and recording (all traffic captured)
      - Requires plant manager approval to activate (normally disabled)
      - Automatic deactivation after 24 hours

wireless_infrastructure:
  access_points:
    indoor_aps:
      - Cisco Catalyst 9120 (food-safe plastic enclosure)
      - Aruba AP-515 (Wi-Fi 6, high client density)
      - Ruckus R550 (harsh environment model)
    outdoor_aps:
      - Ubiquiti UniFi AP AC Mesh (farm equipment connectivity)
      - Aruba AP-567 (outdoor-rated, IP67)
    special_environments:
      - Cold storage: Heated AP enclosures (prevents condensation)
      - Wash-down areas: NEMA 4X stainless steel enclosures
      - Hazardous areas: ATEX/UL Class I Div 2 rated APs (flour mills, grain silos)

  wireless_controllers:
    - Cisco Wireless LAN Controller (centralized management)
    - Aruba Mobility Master (for large multi-site deployments)
    - Cloud-managed: Meraki, UniFi Controller (for smaller facilities)

  backend_infrastructure:
    - RADIUS server (FreeRADIUS, Microsoft NPS, Cisco ISE)
    - Certificate Authority (for device certificates)
    - Network Access Control (Cisco ISE, Aruba ClearPass, Portnox)
    - Wireless Intrusion Prevention System (AirMagnet, Ekahau Sidekick)

security_best_practices:
  encryption:
    - WPA3 mandatory (WPA2 only if legacy devices require)
    - 802.11w (Protected Management Frames) enabled
    - Disable WEP, WPA, TKIP (legacy insecure protocols)

  access_control:
    - 802.1X authentication for enterprise SSIDs
    - Dynamic VLAN assignment based on user/device role
    - MAC authentication bypass (MAB) for devices without 802.1X support
    - Periodic re-authentication (every 8 hours)

  rogue_detection:
    - Wireless IDS/IPS to detect unauthorized APs
    - Automatic containment of rogue APs (deauthentication packets)
    - Alerting on evil twin attacks (fake SSIDs mimicking legitimate ones)

  monitoring:
    - RF spectrum analysis (detect interference from microwaves, motors)
    - Client connectivity health monitoring
    - Bandwidth utilization and top talkers
    - Failed authentication attempts (brute force detection)

common_vulnerabilities:
  weak_authentication:
    - Issue: Shared WPA2-PSK password for all devices
    - Exploit: Password disclosed to unauthorized persons
    - Mitigation: WPA3-Enterprise with unique credentials per device

  rogue_access_points:
    - Issue: Employees install personal Wi-Fi APs in production areas
    - Exploit: Unsecured AP provides backdoor into network
    - Mitigation: Wireless IPS scanning + physical audits

  man_in_the_middle:
    - Issue: Fake AP with strong signal lures clients to connect
    - Exploit: Traffic interception, credential theft
    - Mitigation: 802.11w (PMF), certificate validation

  legacy_devices:
    - Issue: Older wireless scanners only support WPA2 or WEP
    - Exploit: Downgrade attacks if WEP enabled
    - Mitigation: Replace legacy devices or isolate on separate VLAN

compliance_considerations:
  fda_21_cfr_part_11:
    - Wireless tablets used for electronic batch records must comply
    - Audit trail of Wi-Fi authentication events
    - Encryption of data in transit (WPA3) and at rest (device encryption)

  pci_dss:
    - If wireless credit card terminals used (e.g., cafeteria)
    - Wireless network must be isolated from cardholder data environment
    - Quarterly wireless vulnerability scans required

  gdpr:
    - Employee devices on Wi-Fi may process personal data
    - Data protection policies must extend to wireless networks
    - Incident response plan for wireless data breaches
```

### 4. IoT and Sensor Network Security

#### Pattern: Farm IoT Network Architecture
```yaml
pattern_id: FOOD-NET-006
name: Precision Agriculture IoT Security
description: Securing connected farm equipment and field sensors
severity: MEDIUM
iot_categories:
  connected_equipment:
    examples:
      - John Deere autonomous tractors with JDLink telematics
      - Case IH combines with AFS Connect
      - AGCO Fuse connected planters and sprayers
    connectivity:
      - Cellular (LTE/4G/5G) for real-time telemetry
      - GPS/RTK for precision positioning (1-inch accuracy)
      - CAN bus for implement-tractor communication
      - Wi-Fi for software updates (when parked near farm office)
    data_types:
      - Equipment location and hours of operation
      - Fuel consumption and maintenance alerts
      - Yield data (bu/acre, moisture levels)
      - Application rates (seed, fertilizer, pesticides)
    security_risks:
      - GPS spoofing leading to incorrect field boundaries
      - Yield data theft (competitive intelligence for neighbors)
      - Equipment theft via location tracking
      - Ransomware disabling equipment during critical planting/harvest windows

  field_sensors:
    examples:
      - Soil moisture sensors (Sentek, AquaSpy)
      - Weather stations (Davis Instruments, Onset HOBO)
      - Irrigation controllers (Rain Bird, Hunter)
      - Livestock tracking collars (SCR by Allflex, Moocall)
    connectivity:
      - LoRaWAN (long-range low-power wireless, 10+ mile range)
      - Zigbee/Thread (mesh networking for dense sensor deployments)
      - Cellular (NB-IoT for low-bandwidth periodic updates)
      - Satellite (Iridium for remote locations without cellular coverage)
    data_types:
      - Soil moisture/temperature at various depths
      - Rainfall, wind speed, humidity
      - Irrigation valve status and water flow rates
      - Animal health metrics (rumination, activity, temperature)
    security_risks:
      - Unencrypted sensor data (LoRaWAN without AppSKey encryption)
      - Physical tampering with sensors in remote fields
      - Battery depletion attacks (forcing frequent transmissions)
      - False data injection (manipulating irrigation decisions)

  processing_and_storage:
    examples:
      - Grain bin monitoring (OPI Blue, BinManager)
      - Silo level sensors (Binmaster, UWT)
      - Automated feeding systems (dairy, poultry, swine operations)
    connectivity:
      - Wi-Fi or Ethernet (on-premise network)
      - Cellular (remote grain storage facilities)
    data_types:
      - Grain temperature and moisture (spoilage prevention)
      - Inventory levels (automated reordering)
      - Feed consumption rates (animal health monitoring)
    security_risks:
      - Spoilage due to false temperature readings
      - Theft via inventory data manipulation
      - Animal welfare impacts from feeding system disruption

network_architecture:
  edge_iot_gateway:
    purpose: Aggregate sensor data, local processing, cloud connectivity
    products:
      - Cisco IoT Gateway (IR829, IR1101)
      - Dell Edge Gateway 3000 series
      - Raspberry Pi with custom software (budget option)
    functions:
      - Protocol translation (Modbus, LoRaWAN, MQTT)
      - Data filtering and aggregation (reduce cloud bandwidth)
      - Edge analytics (local alerts for critical thresholds)
      - Offline operation (queue data if internet connectivity lost)
    security_features:
      - VPN client for secure cloud connectivity
      - Certificate-based authentication
      - Firewall rules limiting sensor-to-cloud communication
      - Secure boot and firmware integrity checking

  cloud_platforms:
    agriculture_specific:
      - John Deere Operations Center
      - Climate FieldView (Bayer)
      - Granular (Corteva Agriscience)
      - FarmLogs, Farmers Edge
    general_iot_platforms:
      - AWS IoT Core + Greengrass
      - Azure IoT Hub + IoT Edge
      - Google Cloud IoT Core
    security_considerations:
      - Data sovereignty (where is farm data stored? US, EU, other?)
      - Data ownership (who owns yield/field data? Farmer or platform provider?)
      - Third-party data sharing (is data sold to seed companies, commodity traders?)
      - Account security (MFA for cloud platform access, strong passwords)

  mobile_apps:
    - iOS/Android apps for farmers (field monitoring, equipment control)
    - Tablets for agronomists (scouting, prescription creation)
    security:
      - App Store/Play Store vetting (avoid sideloaded APKs)
      - App-level data encryption (SQLCipher for local databases)
      - Biometric authentication (fingerprint, face recognition)
      - Remote wipe capability (if device lost/stolen)

security_best_practices:
  device_authentication:
    - Unique device certificates (not shared API keys)
    - Certificate rotation (annual renewal)
    - Device enrollment process (prevent unauthorized devices)

  data_encryption:
    - TLS 1.3 for data in transit (sensor to gateway, gateway to cloud)
    - AES-256 encryption for data at rest (cloud storage)
    - LoRaWAN AppSKey encryption (application layer encryption)

  access_control:
    - Role-based access control (farm owner, operator, agronomist)
    - Principle of least privilege (agronomist shouldn't see financial data)
    - Session timeouts (30-minute inactivity timeout on mobile apps)

  network_segmentation:
    - Separate IoT VLAN from farm office network
    - Firewall between IoT network and internet
    - No direct access from IoT devices to corporate systems (ERP, accounting)

  monitoring_and_logging:
    - Device health monitoring (offline device alerts)
    - Abnormal data pattern detection (sudden temperature spikes)
    - Failed authentication logging (brute force attempts)
    - Regular security assessments (annual penetration testing)

common_attack_vectors:
  gps_spoofing:
    - Attack: False GPS signals causing equipment to operate in wrong field
    - Mitigation: Dual-frequency GPS receivers, inertial navigation backup

  replay_attacks:
    - Attack: Captured sensor data re-sent to falsify readings
    - Mitigation: Timestamp validation, message authentication codes (MAC)

  firmware_manipulation:
    - Attack: Malicious firmware uploaded to equipment controllers
    - Mitigation: Code signing, secure boot, update authentication

  supply_chain_compromise:
    - Attack: Counterfeit sensors with backdoors pre-installed
    - Mitigation: Purchase from authorized dealers, device authentication

regulatory_considerations:
  data_privacy:
    - GDPR (EU farms): Right to erasure, data portability
    - CCPA (California): Consumer rights for ag data
    - State-level ag data privacy laws (emerging in US)

  equipment_right_to_repair:
    - Legislation allowing farmers to access diagnostic data
    - Impacts on OEM control over software/firmware
    - Security implications of third-party repair tools

  environmental_regulations:
    - Nutrient management plans (fertilizer application data)
    - Pesticide usage reporting (spray records)
    - Water usage reporting (irrigation data for water rights)
    - IoT data as evidence of compliance
```

## Summary

This document provides 6 comprehensive network segmentation and architecture patterns:

1. **Purdue Model Implementation** - Five-level food processing network architecture with detailed security controls per level
2. **Cold Storage Network Isolation** - Refrigeration control network with safety system separation and remote monitoring security
3. **OT Data Exchange DMZ** - Secure data flow between operational technology and IT networks using historians, OPC gateways, and unidirectional gateways
4. **Vendor Remote Access DMZ** - Controlled third-party access for equipment vendors (Tetra Pak, GEA, John Deere) with session monitoring and approval workflows
5. **Food Processing Facility Wi-Fi Segmentation** - Multi-SSID wireless architecture for production devices, employees, guests, and vendors
6. **Farm IoT Network Architecture** - Securing connected farm equipment, field sensors, and precision agriculture systems

**Total Patterns in This Document: 55+**

## Cross-References
- See `/01_Security_SCADA_ICS_Protection.md` for control system security details
- See `/03_Operations_Network_Monitoring.md` for monitoring and detection strategies
- See `/04_Vendors_Tetra_Pak_GEA_John_Deere.md` for vendor-specific network requirements
- See `/06_Protocols_OPC_Modbus_MQTT.md` for industrial protocol details and security
