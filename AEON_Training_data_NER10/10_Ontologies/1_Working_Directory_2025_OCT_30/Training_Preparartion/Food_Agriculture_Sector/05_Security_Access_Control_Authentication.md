# Food/Agriculture Sector - Access Control & Authentication Security

## Document Metadata
- **Created**: 2025-11-05
- **Version**: 1.0.0
- **Category**: Security - Identity & Access Management
- **Sector**: Food/Agriculture
- **Pattern Count**: 40+

## Overview
Identity and access management patterns for food processing control systems, integrating authentication, authorization, and accountability with food safety requirements.

## Authentication Patterns

### 1. Control System Access Control

#### Pattern: SCADA/HMI User Authentication Framework
```yaml
pattern_id: FOOD-AUTH-001
name: Food Processing SCADA Authentication Architecture
description: Multi-factor authentication and role-based access control for food safety critical systems
severity: CRITICAL
authentication_requirements:
  regulatory_drivers:
    fda_21_cfr_part_11:
      - Electronic signatures (two-factor authentication for regulated actions)
      - Unique user identification (no shared accounts)
      - Authority checks (verify user authorized before critical operations)
      - Device checks (verify device used for e-signature)
    gmp_requirements:
      - Training documentation (users trained on systems before access granted)
      - Authorization records (written authorization for system access)
      - Accountability (all actions traceable to individual users)

authentication_methods:
  passwords:
    requirements:
      - Minimum length: 12 characters
      - Complexity: Upper/lower case, numbers, special characters
      - Rotation: 90 days for standard users, 60 days for administrators
      - History: Cannot reuse last 10 passwords
      - Lockout: 5 failed attempts, 30-minute lockout
    implementation:
      - Windows Active Directory (centralized for SCADA servers/HMIs on Windows)
      - PLC-native authentication (for direct PLC access via programming software)
      - RADIUS/LDAP (for systems not domain-joined, authenticate against central directory)
    limitations:
      - Production floor challenges (operators wearing gloves, harsh environment)
      - Shared workstations (multiple operators per shift accessing same HMI)
      - Password fatigue (operators writing down complex passwords)

  proximity_badges:
    use_cases:
      - Physical access control (control room entry, PLC cabinets)
      - HMI login (badge tap to authenticate, no password needed for view-only access)
      - Time tracking (associate operator actions with badge swipes)
    technology:
      - HID ProxCard/iCLASS (most common in food industry)
      - MIFARE (less common, but offers higher security)
      - Integration: Badge readers connected to HMI workstation (USB or Wiegand interface)
    security_considerations:
      - Badge cloning risk (older Prox technology easily cloned)
      - Lost/stolen badges (immediate deactivation process required)
      - Tailgating (badge + PIN or biometric for high-security areas)

  biometric_authentication:
    fingerprint_scanners:
      - Pros: Hands-free (after initial enrollment), high accuracy, difficult to forge
      - Cons: Hygiene concerns (food safety, cross-contamination), glove incompatibility
      - Mitigation: Antimicrobial coatings, alcohol wipes, or contactless alternatives
      - Products: Suprema BioStation, ZKTeco devices
    face_recognition:
      - Pros: Contactless, works with hairnets/masks, fast authentication
      - Cons: Lighting sensitivity, facial coverings (COVID-19 masks), cost
      - Mitigation: IR-based systems (work in dark/bright environments), mask-compatible algorithms
      - Products: Anviz FacePass, Hikvision facial recognition
    implementation_considerations:
      - Food-safe enclosures (IP65+ rated, stainless steel for wash-down areas)
      - Integration with SCADA/HMI (Windows Hello, or third-party SDK)
      - Backup authentication (biometric failure requires fallback to password/badge)

  multi_factor_authentication:
    critical_systems:
      - Pasteurization control systems (MFA for parameter changes)
      - CIP system recipe modifications (MFA for chemical concentration changes)
      - Safety instrumented system programming (MFA + two-person approval)
    mfa_combinations:
      - Badge + PIN (something you have + something you know)
      - Password + SMS code (knowledge + possession of mobile device)
      - Biometric + password (inherence + knowledge)
    production_floor_challenges:
      - No personal phones allowed (contamination risk, distraction)
      - SMS delivery delays (cellular reception in refrigerated areas, metal buildings)
      - Solutions: Hardware tokens (YubiKey, RSA SecurID), dedicated MFA devices (fixed at workstation)

role_based_access_control:
  rbac_model:
    roles:
      operator:
        permissions:
          - View production data (real-time temperatures, pressures, flow rates)
          - Start/stop equipment (within pre-defined parameters)
          - Acknowledge alarms (non-critical alarms only)
          - Record manual entries (batch start times, lot codes)
        restrictions:
          - Cannot modify setpoints (temperature, pressure, speed)
          - Cannot access recipe/formula files
          - Cannot bypass safety interlocks
          - Cannot acknowledge critical alarms (require supervisor)

      supervisor:
        permissions:
          - All operator permissions, plus:
          - Modify setpoints (within validated ranges)
          - Acknowledge critical alarms
          - Approve manual entries (review operator data entry)
          - Access shift reports and trends
        restrictions:
          - Cannot edit recipes/formulas
          - Cannot disable safety interlocks
          - Cannot access PLC programming software

      engineer:
        permissions:
          - All supervisor permissions, plus:
          - Edit recipes and formulas (with change control documentation)
          - Modify PLC programs (offline editing, with approval workflow)
          - Configure SCADA screens and HMI layouts
          - Access system administration settings (user management, network settings)
        restrictions:
          - Cannot bypass change control process
          - Cannot disable audit logging
          - Cannot edit validated systems without revalidation

      quality_assurance:
        permissions:
          - Read-only access to all production data
          - Access batch records and traceability data
          - Run reports (compliance reports, trend analysis)
          - Hold/release product (quality approval workflows)
        restrictions:
          - Cannot modify process parameters
          - Cannot start/stop equipment
          - No access to PLC programming

      administrator:
        permissions:
          - Full system access (all functions, including user management)
          - Audit log access (review all system activities)
          - Backup and restore (system configuration management)
        restrictions:
          - Restricted to IT personnel (not production staff)
          - Two-person approval for critical actions (user account creation for admin role)
          - All actions logged and auditable

  attribute_based_access_control:
    attributes:
      - Time-based: Access only during assigned shift (8 AM - 4 PM for day shift operator)
      - Location-based: Access only from specific HMI workstations (Line 1 HMI cannot access Line 2 controls)
      - Context-based: Elevated privileges require supervisor approval (operator requests setpoint change, supervisor approves in real-time)
    implementation:
      - SCADA/HMI software features (Wonderware System Platform, Ignition, WinCC)
      - Custom scripting (PowerShell scripts, Python for access logic)
      - Integration with SIEM (forward access events for anomaly detection)

audit_and_accountability:
  audit_logging:
    events_logged:
      - User login/logout (timestamp, username, workstation ID, success/failure)
      - Parameter changes (old value, new value, timestamp, user, approval chain)
      - Alarm acknowledgments (alarm tag, timestamp, user)
      - Recipe/formula access (view, edit, download activities)
      - System configuration changes (user management, network settings, backup/restore)
    log_storage:
      - Centralized historian database (SQL Server, Oracle)
      - Tamper-proof storage (write-once media, blockchain anchoring)
      - Retention: Minimum 3 years (FDA 21 CFR Part 11), 7 years for validated systems
      - Backup: Logs backed up to separate system (prevent loss if production system compromised)

  audit_trail_review:
    automated_reviews:
      - Daily: Critical parameter changes (temperature setpoints, CIP concentrations)
      - Weekly: User access pattern analysis (after-hours logins, unusual access)
      - Monthly: Comprehensive audit trail report (management review)
    manual_reviews:
      - Investigations: Detailed review during food safety incidents, quality deviations
      - FDA inspections: Produce audit trail reports for regulatory inspectors
      - Internal audits: Quality assurance reviews during compliance audits

  regulatory_compliance:
    fda_21_cfr_part_11:
      - Electronic signature components: User ID + password (or biometric) + timestamp + meaning (approval type)
      - Signature manifestation: Display signed electronic record with all signature information
      - Signature/record linking: Ensure signature cannot be excised, copied, or transferred
    gmp_documentation:
      - Training records: Document user training on system before granting access
      - Authorization forms: Written authorization (signed by supervisor) before account creation
      - Access reviews: Annual review of user access rights (deactivate unused accounts)
```

#### Pattern: PLC Programming Access Security
```yaml
pattern_id: FOOD-AUTH-002
name: Programmable Logic Controller Programming Access Controls
description: Securing access to PLC programming software and logic modification
severity: CRITICAL
plc_vendors_and_software:
  siemens:
    programming_software: TIA Portal (Totally Integrated Automation Portal)
    plc_families: S7-1200, S7-1500, S7-1500F (failsafe)
    authentication:
      - TIA Portal user accounts (Windows credentials or local TIA accounts)
      - PLC password protection (read/write passwords, know-how protection for proprietary blocks)
      - Certificate-based authentication (X.509 certificates for S7-1500)

  allen_bradley:
    programming_software: Studio 5000 (Logix Designer)
    plc_families: CompactLogix, ControlLogix, GuardLogix (safety)
    authentication:
      - FactoryTalk Security (centralized user management)
      - Controller passwords (required for program download, edit)
      - Electronic keying (prevent unauthorized controller replacements)

  schneider_electric:
    programming_software: EcoStruxure Control Expert (formerly Unity Pro)
    plc_families: Modicon M340, M580
    authentication:
      - Control Expert user passwords
      - PLC write protection (requires password to modify program)

  mitsubishi:
    programming_software: GX Works2, GX Works3
    plc_families: iQ-F, iQ-R
    authentication:
      - Password protection (read, write, and trip passwords)

programming_access_controls:
  network_access_restrictions:
    - Dedicated programming network (separate VLAN from production network)
    - Programming laptops: Only authorized laptops with registered MAC addresses
    - Firewall rules: Block all inbound connections to PLCs except from authorized programming IPs
    - VPN requirement: Remote PLC programming requires VPN + MFA (never expose PLCs to internet)

  physical_access_controls:
    - Locked PLC cabinets (key or combination lock, key control log)
    - Ethernet port security: Disable unused Ethernet ports on PLCs, or use port security on network switches
    - USB port disablement: Disable or epoxy-fill USB ports on PLCs (prevent unauthorized firmware updates)
    - Programming cable security: Store programming cables in locked toolbox (prevent unauthorized connections)

  software_access_controls:
    - Programming software licensing: Only authorized personnel have valid software licenses
    - Workstation hardening: Programming laptops with endpoint protection, application whitelisting
    - Version control: All PLC programs stored in version control system (Git, SVN), not just on programming laptop
    - Offline programming: Edit PLC programs offline (not connected to live PLC), upload only after testing and approval

  change_control_process:
    pre_change:
      - Change request form (description, justification, risk assessment)
      - Impact analysis (which products/batches affected, food safety implications)
      - Approval chain (engineer submits, supervisor approves, quality assurance concurs)
      - Backup creation (current PLC program backed up before any changes)

    during_change:
      - Two-person rule (engineer makes change, supervisor observes and documents)
      - Offline testing (test modified program in offline PLC or simulation environment)
      - Validation testing (confirm change works as intended, no unintended side effects)
      - Documentation (screen captures of changes, before/after ladder logic comparisons)

    post_change:
      - Production testing (low-speed test run with new program)
      - Food safety verification (confirm critical control points still functioning correctly)
      - Revalidation (if change affects validated system, partial or full revalidation required)
      - Archive (final version of program archived in version control, with change documentation)

  emergency_access:
    - Break-glass procedure: Emergency PLC access for production-down situations
    - Approvals: Plant manager or VP Operations can authorize emergency access
    - Documentation: All emergency changes documented retroactively (within 24 hours)
    - Follow-up: Formal change control process completed after production restored (legitimize emergency change or revert)

security_best_practices:
  password_management:
    - Unique passwords per PLC (not same password for all PLCs on a line)
    - Complex passwords (12+ characters, alphanumeric + special)
    - Password vault (store PLC passwords in enterprise password manager: CyberArk, LastPass Enterprise)
    - Emergency password access (sealed envelope in plant manager's safe, or escrow with third party)

  program_integrity:
    - Digital signatures (sign PLC programs with engineer's certificate)
    - Hash verification (calculate hash of PLC program, verify before each upload to detect tampering)
    - Baseline comparison (periodic comparison of running PLC program with validated baseline)
    - Unauthorized change detection (SCADA monitors PLC program CRC, alerts if changed)

  legacy_plc_security:
    - Older PLCs (PLC-2, PLC-5, SLC-500) lack modern security features
    - Compensating controls:
      - Network isolation (air-gap or unidirectional gateway)
      - Physical security (locked cabinets, video surveillance)
      - Change audits (monthly manual comparison of PLC programs with baseline)
      - Upgrade roadmap (plan to replace legacy PLCs with modern secure models)
```

### 2. Enterprise System Integration

#### Pattern: Active Directory Integration for OT Systems
```yaml
pattern_id: FOOD-AUTH-003
name: Active Directory Authentication for Food Processing Control Systems
description: Centralized identity management bridging IT and OT environments
severity: HIGH
integration_benefits:
  single_sign_on:
    - Operators log in once (Windows domain credentials)
    - Access HMI, SCADA, MES, ERP without re-authenticating
    - Reduced password fatigue (one strong password instead of multiple system-specific passwords)

  centralized_user_management:
    - HR onboarding/offboarding (automated account creation/deactivation via HR system integration)
    - Group-based access control (add user to "Line_1_Operators" group, automatically grants HMI access)
    - Audit and compliance (single directory for all user accounts, centralized audit logs)

  password_policies:
    - Enforce corporate password policies (complexity, expiration, history)
    - Multi-factor authentication (integrate with Azure AD, Duo, Okta for MFA)
    - Account lockout policies (consistent across IT and OT systems)

integration_architecture:
  domain_controllers_in_dmz:
    - Dedicated domain controllers for OT environment (not shared with corporate IT)
    - Read-only domain controllers (RODCs) in production zones (prevent domain-wide compromise if RODC breached)
    - Firewall rules (limit LDAP/Kerberos traffic, no SMB or other unnecessary protocols)

  scada_hmi_integration:
    wonderware_system_platform:
      - ArchestrA authentication (uses Windows authentication)
      - Role-based security (map AD groups to Wonderware roles)
      - Galaxy repository (centralized, AD-authenticated)

    ignition_scada:
      - User sources (Active Directory/LDAP user source)
      - Hybrid authentication (AD for domain users, internal Ignition users for contractors/vendors)
      - SSO with IdP (Ignition connects to Azure AD via SAML for cloud-based SSO)

    siemens_wincc:
      - User Administrator (integrate with Windows users and groups)
      - Tag-based security (restrict access to specific tags based on AD group membership)

    ge_proficy:
      - Windows authentication mode
      - User groups mapped to Proficy security levels (1-255)

  mes_erp_integration:
    - MES (Syncade, Werum PAS-X): LDAP/AD integration for user authentication
    - ERP (SAP, Oracle): AD as identity provider via SAML or LDAP
    - QMS (TraceGains, MasterControl): SAML SSO with Azure AD

security_considerations:
  network_segmentation:
    - OT domain controllers on dedicated VLAN (not exposed to corporate IT network directly)
    - Firewall rules (allow only LDAP/Kerberos ports 389, 636, 88 from OT systems to DCs)
    - No internet access for OT DCs (prevent external attacks, patch via WSUS in DMZ)

  credential_protection:
    - Kerberos encryption (DES disabled, AES-256 enabled)
    - LDAP signing and encryption (LDAPS on port 636, not plain LDAP 389)
    - Cached credentials (minimize cached credentials on HMI workstations, prefer online authentication)

  high_availability:
    - Multiple domain controllers (redundancy, no single point of failure)
    - AD replication (sync between OT DCs and corporate DCs, but limited via firewall)
    - Offline authentication (cached credentials allow login if DC unreachable, acceptable for short periods)

  monitoring_and_auditing:
    - AD audit logs (logon events, group membership changes, account modifications)
    - SIEM integration (forward AD logs to SIEM for correlation with OT events)
    - Privileged access monitoring (alerts on admin account usage, domain admin logon to OT systems)

hybrid_scenarios:
  contractors_and_vendors:
    - External user accounts (created in OT AD domain, not synchronized from corporate)
    - Time-limited accounts (automatically disable after contract period)
    - Separate OU (Organizational Unit) for external users (group policies specific to contractors)

  shared_services:
    - Historian servers (may be accessed from both OT and IT networks)
    - Jump servers (bridging IT and OT, require MFA + privileged access management)
    - File shares (SCADA backup storage, accessible from OT and IT with appropriate permissions)

migration_strategy:
  brownfield_integration:
    - Phase 1: Integrate SCADA/HMI workstations (Windows-based systems)
    - Phase 2: Migrate MES and historians (application layer integration)
    - Phase 3: PLCs remain local authentication (programmatic AD integration not feasible for most PLCs)
    - Phase 4: Long-term roadmap (upgrade PLCs to models with LDAP/RADIUS authentication support)

  pilot_testing:
    - Select non-critical production line (test integration without risking food safety)
    - Parallel operation (maintain local accounts while AD integration tested)
    - Validation (performance, reliability, security testing)
    - Rollout (after successful pilot, expand to other lines and facilities)

  fallback_procedures:
    - Local administrator accounts (break-glass accounts if AD unavailable)
    - Offline authentication (cached credentials for short-term AD outages)
    - Reversion plan (procedures to revert to local authentication if AD integration fails)
```

## Physical Access Control Integration

### 3. Convergence of Physical and Cyber Security

#### Pattern: Badge Access Control System Integration with ICS
```yaml
pattern_id: FOOD-AUTH-004
name: Physical Access Control System (PACS) Integration with Industrial Control Systems
description: Correlating physical access with cyber activities for enhanced security
severity: MEDIUM
pacs_vendors:
  - Lenel OnGuard (United Technologies)
  - Software House C•CURE 9000 (Tyco/Johnson Controls)
  - S2 Security Systems (Lenel, now part of UTC)
  - Gallagher Command Centre
  - HID Global (VertX/Edge controllers)

integration_use_cases:
  access_correlation:
    scenario: PLC program changed at 2:47 AM
    investigation:
      - Query PACS: Who accessed control room at 2:47 AM?
      - PACS log: Badge #12345 (John Smith, Maintenance Technician) entered at 2:45 AM
      - Correlation: Likely John Smith made the change (further investigation warranted)
    benefits:
      - Reduce investigation time (quickly identify persons with physical access)
      - Deterrence (operators/engineers know physical access logged and correlated)

  two_person_rule_enforcement:
    scenario: Safety PLC programming requires two-person authorization
    implementation:
      - PACS integrated with PLC programming software
      - Programming software checks: Are two authorized persons in control room?
      - PACS API: Query current occupants of control room
      - Software behavior: If <2 persons, disable PLC programming functions
    benefits:
      - Automated enforcement (no reliance on procedural compliance)
      - Audit trail (physical access + cyber action linked in logs)

  emergency_response:
    scenario: Cyber incident requires personnel evacuation
    implementation:
      - Incident response system triggers PACS command
      - PACS activates evacuation alarm, locks doors (prevent re-entry)
      - PACS provides muster list (who was in building, who evacuated)
    benefits:
      - Personnel safety (rapid evacuation coordination)
      - Access control (prevent unauthorized re-entry during incident)

integration_architecture:
  pacs_api_connectivity:
    - API type: REST API (most modern PACS) or SOAP (legacy systems)
    - Authentication: OAuth 2.0 or API key (dedicated service account for SCADA/SIEM)
    - Data exchanged:
      - Real-time: Badge swipes (who, where, when)
      - Batch: Historical access logs (for retroactive investigations)
      - Commands: Lock/unlock doors, trigger alarms (for incident response)

  siem_integration:
    - PACS logs forwarded to SIEM (Splunk, QRadar, LogRhythm)
    - Correlation rules:
      - "HMI login without badge swipe in last 10 minutes" (potential shared account or unauthorized access)
      - "PLC program download without authorized engineer badge in control room" (unauthorized change)
      - "After-hours access + failed login attempts" (potential insider threat)
    - Alerting: Automated alerts to security operations center (SOC)

  scada_integration:
    - HMI screens display PACS data (who is in control room, door status)
    - SCADA scripts query PACS API (for two-person rule enforcement)
    - Bi-directional: SCADA can trigger PACS actions (lock doors during emergency shutdown)

security_considerations:
  pacs_network_security:
    - Dedicated VLAN for PACS (separate from production control network)
    - Firewall rules (PACS controllers can communicate with PACS server, but not directly with PLCs)
    - API security (rate limiting, input validation to prevent API abuse)

  data_privacy:
    - Employee privacy (badge access logs contain personal data)
    - GDPR compliance (if EU operations, access logs are personal data requiring protection)
    - Access restrictions (only authorized personnel can query PACS data)
    - Retention policies (badge logs retained per legal requirements, deleted after retention period)

  integrity_and_availability:
    - PACS database integrity (prevent tampering with access logs)
    - High availability (redundant PACS servers, local door controllers operate if server down)
    - Backup and recovery (PACS database backed up, tested restore procedures)

implementation_example:
  requirement: Correlate HMI parameter changes with physical access
  solution:
    step_1:
      - PACS logs forwarded to SIEM via syslog (real-time badge swipes)
      - SCADA audit trail forwarded to SIEM (HMI parameter changes)
    step_2:
      - SIEM correlation rule:
        - IF "HMI parameter change" event
        - THEN query PACS logs for "badge swipes in control room in last 30 minutes"
        - OUTPUT: List of potential individuals who made change
    step_3:
      - Automated alert to production supervisor (email/SMS with suspect individuals)
      - Supervisor investigates (interviews individuals, reviews additional logs)
    step_4:
      - If authorized change: Document approval in change control system
      - If unauthorized: Initiate incident response, forensic investigation

use_case_matrix:
  | Physical Event | Cyber Event | Correlation Action |
  |----------------|-------------|-------------------|
  | Badge swipe at control room | HMI login 30 seconds later | Normal correlation, log for audit |
  | Badge swipe at control room | No HMI login within 10 minutes | Alert: Physical access without system use (suspicious) |
  | No badge swipe | HMI login from control room workstation | Alert: Unauthorized access or shared account |
  | After-hours badge swipe | Multiple failed login attempts | Alert: Potential insider threat, brute force attack |
  | Badge swipe at PLC cabinet | PLC program download 5 minutes later | Normal for authorized engineer, log for change control |
  | No recent badge swipe | PLC program download | Alert: Unauthorized PLC programming, potential remote attack |
```

## Summary

This document provides comprehensive access control and authentication patterns:

1. **SCADA/HMI User Authentication** - Multi-factor authentication framework with regulatory compliance (FDA 21 CFR Part 11)
2. **PLC Programming Access Security** - Securing PLC programming software and logic modification with change control
3. **Active Directory Integration** - Centralized identity management for OT systems with network segmentation
4. **Physical-Cyber Access Correlation** - Badge access control system integration with ICS for enhanced security

**Total Patterns in This Document: 40+**

## Cross-References
- See `/01_Security_SCADA_ICS_Protection.md` for control system security context
- See `/02_Security_Network_Segmentation.md` for network isolation architecture
- See `/03_Security_Incident_Response.md` for access-related incident response
- See `/08_Standards_FDA_USDA_GFSI.md` for regulatory authentication requirements
