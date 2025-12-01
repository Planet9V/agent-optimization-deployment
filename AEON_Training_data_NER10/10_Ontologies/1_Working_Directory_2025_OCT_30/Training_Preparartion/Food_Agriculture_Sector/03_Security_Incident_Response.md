# Food/Agriculture Sector - Cyber Incident Response & Recovery

## Document Metadata
- **Created**: 2025-11-05
- **Version**: 1.0.0
- **Category**: Security - Incident Response
- **Sector**: Food/Agriculture
- **Pattern Count**: 50+

## Overview
Cyber incident response procedures specific to food processing, cold chain, and agricultural operations where incidents can impact food safety, product quality, and animal welfare.

## Incident Response Framework

### 1. Food Safety Cyber Incident Classification

#### Pattern: Incident Severity Matrix for Food Processing
```yaml
pattern_id: FOOD-IR-001
name: Food Safety Cyber Incident Severity Classification
description: Prioritization framework for cyber incidents in food manufacturing
severity: CRITICAL
incident_categories:
  category_1_critical:
    definition: Immediate food safety threat or active contamination
    examples:
      - Pasteurization system compromised during active production
      - Water treatment control system failure introducing microbial risk
      - CIP system bypassed leading to allergen cross-contact
      - Refrigeration system shutdown causing temperature abuse
      - Foreign material detection system disabled during packaging
    response_time: Immediate (< 15 minutes)
    response_team:
      - Food Safety Team Lead (on-site)
      - Plant Manager (decision authority)
      - Quality Assurance Director
      - Cybersecurity Incident Commander
      - Legal counsel (for FDA reporting)
    immediate_actions:
      - Emergency stop of affected production lines
      - Product quarantine (lot codes traced and isolated)
      - Activate food safety incident response plan
      - Engage cyber forensics team
      - Prepare for regulatory notification (FDA/USDA 24-hour rule)
    notification_requirements:
      - FDA Reportable Food Registry (if reasonable probability of serious adverse health consequences)
      - USDA FSIS (for meat/poultry within 24 hours)
      - Customers (if product already shipped)
      - Insurance carrier (cyber policy and product liability)

  category_2_high:
    definition: Significant process deviation affecting product quality or compliance
    examples:
      - Temperature excursion in cold storage (above critical limits but caught quickly)
      - Fill weight system manipulation (underfilling packages)
      - Date code system altered (incorrect expiration dates printed)
      - Metal detector sensitivity reduced (increased foreign material risk)
      - Batch record system tampering (21 CFR Part 11 violation)
    response_time: < 1 hour
    response_team:
      - Quality Assurance Manager
      - Production Supervisor
      - IT Security Analyst
      - Plant Manager (for escalation decisions)
    immediate_actions:
      - Hold affected product pending investigation
      - Document exact timeline of deviation
      - Secure digital evidence (logs, screen captures)
      - Assess product disposition (release, rework, or destroy)
    notification_requirements:
      - Internal management (QA Director, VP Operations)
      - Customers (if product shipped, may be voluntary hold)
      - Potentially FDA (if investigation reveals food safety impact)

  category_3_medium:
    definition: Process disruption without immediate safety/quality impact
    examples:
      - Packaging line control system ransomware (line stopped, no safety risk)
      - SCADA historian database corruption (data loss but processes running)
      - Warehouse management system compromised (inventory inaccuracy)
      - Email system phishing attack (credential theft)
      - Website defacement (reputational risk)
    response_time: < 4 hours
    response_team:
      - IT Security Team
      - Production IT support
      - Affected department managers
    immediate_actions:
      - Isolate affected systems from network
      - Activate backup/manual procedures
      - Assess data integrity and recovery needs
    notification_requirements:
      - Internal IT management
      - Senior leadership (daily status reports)

  category_4_low:
    definition: Security event with no operational impact
    examples:
      - Failed phishing attempt (employee reported without clicking)
      - Intrusion detection alert (blocked by firewall, no compromise)
      - Vulnerability scan findings (no evidence of exploitation)
      - Unauthorized USB device detected (blocked by endpoint protection)
    response_time: < 24 hours
    response_team:
      - IT Security Analyst
      - System Administrator (for remediation)
    immediate_actions:
      - Document event in security information and event management (SIEM)
      - Review logs for related activity
      - User education (if employee involved)
    notification_requirements:
      - IT Security Manager (weekly summary reports)

escalation_criteria:
  category_4_to_3:
    - Multiple failed phishing attempts indicate targeted campaign
    - Vulnerability actively being scanned by external actors
    - Unauthorized access attempts to production systems

  category_3_to_2:
    - Ransomware begins encrypting production control systems
    - Evidence of data exfiltration includes proprietary formulations
    - System disruption exceeds 4-hour recovery window

  category_2_to_1:
    - Investigation reveals actual product contamination
    - Temperature excursion duration/magnitude creates safety risk
    - Traceability data lost preventing effective recall
    - Allergen cross-contact confirmed by testing

decision_tree_example: |
  Cyber Incident Detected
  │
  ├─ Does it affect active food production processes?
  │  ├─ YES → Is there risk of contamination or safety deviation?
  │  │  ├─ YES → CATEGORY 1 CRITICAL
  │  │  └─ NO → Is product quality compromised?
  │  │     ├─ YES → CATEGORY 2 HIGH
  │  │     └─ NO → CATEGORY 3 MEDIUM
  │  └─ NO → Is data integrity compromised?
  │     ├─ YES → CATEGORY 3 MEDIUM
  │     └─ NO → CATEGORY 4 LOW
```

#### Pattern: Incident Response Team Structure
```yaml
pattern_id: FOOD-IR-002
name: Food Manufacturing Cyber Incident Response Team
description: Multi-disciplinary team for cyber incidents in food operations
severity: CRITICAL
core_team_roles:
  incident_commander:
    primary: Director of IT or VP Operations
    backup: Plant Manager or Corporate Security Director
    responsibilities:
      - Overall incident coordination and decision authority
      - Stakeholder communication (CEO, Board, customers, regulators)
      - Resource allocation (budget approval for forensics, remediation)
      - Interface with legal counsel and PR team
    qualifications:
      - Senior leadership with operational and IT understanding
      - Food safety regulatory knowledge (FDA, USDA)
      - Crisis management experience
    contact:
      - Mobile phone (24/7 reachability)
      - Satellite phone (backup if cellular compromised)
      - Encrypted messaging (Signal, WhatsApp for secure coordination)

  food_safety_lead:
    primary: Director of Food Safety & Quality Assurance
    backup: QA Manager or Food Safety Specialist
    responsibilities:
      - Assess food safety impact of cyber incident
      - Determine product disposition (hold, release, recall)
      - Interface with regulatory agencies (FDA, USDA)
      - Manage product traceability and recall logistics
    qualifications:
      - PCQI (Preventive Controls Qualified Individual) certification
      - HACCP training and experience
      - Regulatory inspection experience
    tools_and_resources:
      - Traceability system access (ERP, WMS)
      - Rapid microbial testing capabilities
      - Laboratory analysis vendor contacts (third-party testing)
      - Recall execution checklist (FDA/USDA templates)

  cybersecurity_lead:
    primary: CISO or IT Security Manager
    backup: Senior Security Analyst or external MSSP
    responsibilities:
      - Technical incident investigation and forensics
      - Threat containment and eradication
      - Recovery coordination (system restoration)
      - Evidence preservation for potential legal action
    qualifications:
      - CISSP, GIAC, or equivalent cybersecurity certifications
      - OT/ICS security experience (SCADA, PLCs)
      - Digital forensics training
    tools_and_resources:
      - SIEM (Splunk, QRadar, LogRhythm)
      - Endpoint detection and response (EDR)
      - Forensic imaging tools (FTK Imager, EnCase)
      - Threat intelligence feeds (Food-ISAC, MS-ISAC)

  production_operations_lead:
    primary: Plant Manager or Production Manager
    backup: Production Supervisor or Shift Manager
    responsibilities:
      - Operational impact assessment (downtime, throughput loss)
      - Manual process activation (if automation compromised)
      - Employee safety during incident (lock-out/tag-out procedures)
      - Customer communication (order fulfillment delays)
    qualifications:
      - Deep knowledge of production processes
      - Emergency response training
      - Communication skills for shift workforce
    tools_and_resources:
      - Manual operating procedures (paper backups)
      - Critical spare parts inventory
      - Vendor emergency contacts (24/7 support)

  it_operations_lead:
    primary: IT Manager or Systems Administrator
    backup: Network Engineer or Database Administrator
    responsibilities:
      - System recovery and restoration
      - Data backup validation and restore
      - Network isolation and segmentation
      - Coordination with vendors (SCADA, ERP, MES)
    qualifications:
      - Windows/Linux system administration
      - Industrial network protocols (Modbus, OPC UA)
      - Backup/disaster recovery experience
    tools_and_resources:
      - Backup systems (Veeam, Commvault)
      - Network management tools (SolarWinds, Cisco Prime)
      - Vendor support portals and hotlines

  legal_counsel:
    primary: General Counsel or Corporate Attorney
    backup: External law firm specializing in food/cyber law
    responsibilities:
      - Regulatory reporting obligations
      - Privilege protection for investigation findings
      - Contract review (vendor liability, insurance claims)
      - Litigation preparedness (if third-party or customer claims)
    qualifications:
      - Food law expertise (FDA, USDA regulations)
      - Cyber incident legal experience
      - E-discovery and digital evidence handling

  communications_lead:
    primary: VP of Communications or PR Director
    backup: Marketing Manager or Corporate Communications
    responsibilities:
      - Internal communications (employee updates)
      - External communications (customers, media, public)
      - Social media monitoring and response
      - Reputation management
    qualifications:
      - Crisis communications training
      - Media relations experience
      - Food industry knowledge
    tools_and_resources:
      - Pre-drafted communications templates
      - Social media monitoring tools (Hootsuite, Sprinklr)
      - Media contact database
      - Customer notification system (email, phone tree)

extended_team_members:
  - Human Resources (employee investigations, terminations if insider threat)
  - Finance (cost tracking, insurance claims)
  - Facilities/Engineering (physical security, HVAC/building systems)
  - Supply Chain (supplier/customer coordination)
  - External advisors (forensics firm, crisis management consultants)

activation_procedures:
  initial_alert:
    - Any employee detecting cyber incident contacts IT helpdesk or security
    - Helpdesk escalates to IT Security Lead (< 15 minutes)
    - IT Security Lead assesses severity and activates Incident Commander

  team_assembly:
    - Incident Commander sends alert via mass notification system (Everbridge, OnSolve)
    - Team members acknowledge via mobile app (< 30 minutes for Category 1)
    - Virtual or physical war room established

  initial_briefing:
    - Incident Commander convenes team (video conference or in-person)
    - Situation report from Cybersecurity Lead
    - Food Safety Lead assesses safety implications
    - Incident Commander assigns roles and establishes update cadence (hourly for Category 1)

communication_protocols:
  internal_updates:
    - Category 1: Hourly updates to executive leadership
    - Category 2: Every 4 hours updates
    - Category 3: Daily summary reports

  external_notifications:
    - Regulatory: As required by law (24 hours for FDA/USDA reportable events)
    - Customers: Within 24-48 hours for supply chain impacts
    - Media: Only via approved communications lead (no individual employee statements)
    - Insurance: Within policy notification period (typically 24-72 hours)

training_and_exercises:
  tabletop_exercises:
    - Frequency: Biannual (every 6 months)
    - Scenarios: Pasteurization system compromise, ransomware, supply chain attack
    - Participants: Full incident response team + key stakeholders
    - Outcomes: Lessons learned, plan updates, team familiarization

  technical_drills:
    - Frequency: Quarterly
    - Focus: System recovery, forensic evidence collection, backup restoration
    - Participants: IT Operations, Cybersecurity, Production IT support
    - Metrics: Recovery time objectives (RTO), recovery point objectives (RPO)

  regulatory_mock_recalls:
    - Frequency: Annual (required by FSMA)
    - Scenario: Cyber-induced contamination requiring product recall
    - Participants: Food Safety, QA, Supply Chain, Legal, Communications
    - Goal: Complete mock recall exercise in < 4 hours (FDA expectation)
```

### 2. Incident Containment Strategies

#### Pattern: Emergency Production Shutdown Procedures
```yaml
pattern_id: FOOD-IR-003
name: Safe Production Shutdown During Cyber Incident
description: Procedures to safely halt food production when control systems compromised
severity: CRITICAL
shutdown_scenarios:
  scenario_1_controlled_shutdown:
    trigger: Cyber incident detected early, systems still responding correctly
    procedure:
      - Production supervisor notifies all line operators
      - Complete current batch/product run (if safe to do so)
      - Drain product from equipment to minimize waste
      - Execute normal shutdown sequence via HMI/SCADA
      - Close all valves, de-energize equipment per SOPs
      - Lock-out/tag-out electrical and mechanical energy sources
    estimated_time: 30-60 minutes for typical processing line

  scenario_2_emergency_stop:
    trigger: Immediate safety risk (e.g., pasteurization temperature dropping)
    procedure:
      - Press emergency stop buttons (multiple locations on production floor)
      - Activate safety interlocks (SIS systems independent of main control)
      - Manually close critical valves (steam, chemicals, product flow)
      - Open drain valves to evacuate product from compromised equipment
      - Secure hazardous materials (chlorine, ammonia, caustic chemicals)
    estimated_time: < 5 minutes
    safety_considerations:
      - Ensure personnel clear of moving equipment before e-stop
      - Chemical lines may have residual pressure (vent safely)
      - Hot surfaces require cool-down time before maintenance

  scenario_3_manual_failover:
    trigger: Control system compromised but equipment physically intact
    procedure:
      - Switch HMI/SCADA to manual mode (if available)
      - Use local control panels on equipment (bypass SCADA)
      - Operate critical processes manually (pasteurization, refrigeration)
      - Deploy manual monitoring (operators physically checking gauges)
      - Implement paper-based batch records (electronic system offline)
    estimated_time: 1-2 hours to establish manual operations
    limitations:
      - Reduced throughput (30-50% of normal capacity)
      - Higher labor requirements (3-5x operators needed)
      - Manual monitoring less accurate (human error risk)

product_handling_protocols:
  work_in_progress:
    - Product in processing equipment during shutdown
    - Assessment: Food Safety Lead evaluates safety based on process stage
    - Options:
      1. Complete processing manually (if near end of cycle)
      2. Discard product (if safety cannot be assured)
      3. Hold for testing (if marginal safety, laboratory analysis decides)
    - Documentation: Detailed incident report for traceability records

  finished_product_on_hold:
    - Product manufactured during compromised period
    - Lot code identification (start/end times of incident)
    - Physical quarantine (dedicated hold area, labeled "DO NOT SHIP")
    - Investigation: Review all process data for deviations
    - Release decision: Food Safety Lead approves after verification

  released_product_recall_evaluation:
    - Traceability data: Identify customers and distribution channels
    - Risk assessment: Severity of contamination/deviation likelihood
    - Recall class determination:
      - Class I: Reasonable probability of serious adverse health consequences or death
      - Class II: Low probability of serious adverse health consequences
      - Class III: Not likely to cause adverse health consequences
    - Notification timeline: FDA/USDA within 24 hours if Class I

system_isolation_procedures:
  network_segmentation:
    - Identify compromised network zone (Level 1, Level 2, DMZ, etc.)
    - Disconnect affected zone from enterprise network (pull fiber, disable switch ports)
    - Maintain safety system connectivity (independent SIS network)
    - Isolate specific production lines if compromise limited

  device_quarantine:
    - Power off compromised PLCs, HMIs, SCADA servers
    - Physically disconnect from network (not just logical isolation)
    - Tag with "CONTAMINATED - DO NOT USE" labels
    - Secure in locked area to preserve forensic evidence

  external_communication_control:
    - Block internet access for all OT networks (temporary firewall rules)
    - Disable vendor remote access portals
    - Whitelist only essential communications (safety system updates)

backup_system_activation:
  hot_standby_systems:
    - If redundant PLCs available, switch to backup controller
    - Verify backup system not compromised (check firmware, program integrity)
    - Test outputs before re-energizing production equipment

  cold_backup_restoration:
    - Restore PLC programs from verified clean backups (weekly backups stored offline)
    - Reload HMI screens and recipes from version-controlled repository
    - Re-establish network connectivity incrementally (verify each device)

  manual_mode_operations:
    - Deploy manual standard operating procedures (paper copies)
    - Train operators on manual valve/control panel operation
    - Implement physical monitoring rounds (hourly checks of critical parameters)

safety_considerations:
  personnel_protection:
    - Ensure all employees aware of emergency shutdown (PA system, text alerts)
    - Evacuate personnel from hazardous areas (ammonia refrigeration machinery rooms)
    - Post guards at entrances to prevent re-entry during stabilization

  equipment_protection:
    - Prevent damage from abrupt shutdowns (thermal shock, mechanical stress)
    - Maintain critical utilities (cooling water for hot equipment)
    - Monitor for secondary hazards (steam leaks, chemical spills)

  environmental_protection:
    - Contain product spills (floor drains, spill kits)
    - Prevent chemical releases (close drain valves on CIP systems)
    - Notify environmental authorities if reportable quantities released
```

#### Pattern: Forensic Evidence Preservation
```yaml
pattern_id: FOOD-IR-004
name: Digital Forensics in Food Manufacturing Environments
description: Evidence collection procedures for cyber incidents affecting food production
severity: HIGH
evidence_types:
  volatile_data:
    description: Data lost when system powered off (RAM contents, network connections)
    collection_priority: HIGHEST (collect within minutes)
    examples:
      - Running processes on SCADA servers
      - Active network connections from PLCs
      - Logged-in user sessions on HMIs
      - Clipboard contents (if attacker copied data)
    collection_tools:
      - FTK Imager (RAM capture)
      - Volatility Framework (memory analysis)
      - Netstat, Wireshark (network state)
    procedures:
      - Do not power off systems immediately upon discovery
      - Capture volatile data first (before hard drive imaging)
      - Document all actions taken (chain of custody starts now)

  non_volatile_data:
    description: Data persists after power loss (hard drives, USB drives, SD cards)
    collection_priority: HIGH (collect within hours)
    examples:
      - PLC program files on engineering workstations
      - SCADA server hard drives (historian database, HMI projects)
      - Log files (Windows Event Logs, SCADA application logs)
      - Email archives (for phishing investigation)
    collection_tools:
      - FTK Imager (forensic disk imaging)
      - DD (Linux disk duplication)
      - Write blockers (prevent accidental modification)
    procedures:
      - Create forensic images (bit-by-bit copies), never work on originals
      - Calculate hash values (SHA-256) to verify integrity
      - Label and secure physical media (locked evidence storage)

  network_traffic:
    description: Packet captures and flow data
    collection_priority: MEDIUM (historical data from existing captures)
    examples:
      - PCAP files from industrial firewalls (Claroty, Nozomi)
      - NetFlow data from switches
      - Intrusion detection system (IDS) alerts
    collection_tools:
      - Wireshark (PCAP analysis)
      - Zeek (formerly Bro) for protocol analysis
      - Security Onion (IDS log aggregation)
    procedures:
      - Export PCAP files from span ports or network taps
      - Filter for industrial protocols (Modbus, OPC UA, Profinet)
      - Correlate traffic with process events (timestamps critical)

  physical_evidence:
    description: Hardware and physical access records
    collection_priority: MEDIUM to LOW
    examples:
      - USB drives found plugged into HMIs
      - Badge access logs (who entered control room during incident window)
      - Security camera footage (physical access to PLCs)
      - Tamper-evident seals (broken seals on control panels)
    procedures:
      - Photograph evidence in place before collection
      - Package evidence properly (anti-static bags for electronics)
      - Maintain chain of custody forms

chain_of_custody:
  documentation_requirements:
    - Date/time of collection (UTC timestamps preferred)
    - Person collecting evidence (name, title, signature)
    - Description of evidence (e.g., "HMI workstation hard drive, Serial #XYZ")
    - Hash values (SHA-256) for digital evidence
    - Storage location (evidence locker, facility, room number)
    - Transfer log (if evidence moved to forensics lab)

  evidence_handling_rules:
    - Minimize number of people handling evidence
    - Use write blockers when accessing storage media
    - Work on forensic copies, preserve originals
    - Secure evidence when not actively being analyzed

  legal_considerations:
    - Attorney-client privilege: Engage legal counsel before investigation starts
    - Avoid spoliation: Do not destroy evidence, even if seemingly unrelated
    - Privacy laws: Employee monitoring disclosures, GDPR compliance
    - Discovery obligations: If litigation likely, preserve all related data

forensic_analysis_procedures:
  timeline_reconstruction:
    - Establish incident start time (first anomalous event)
    - Map attacker actions chronologically (initial access, lateral movement, impact)
    - Correlate cyber events with process deviations (did temperature drop when PLC compromised?)
    - Identify exit point or persistence mechanisms (is attacker still in network?)

  malware_analysis:
    - Static analysis: Examine malware code without executing (IDA Pro, Ghidra)
    - Dynamic analysis: Run malware in sandbox (Cuckoo Sandbox, Joe Sandbox)
    - Identify malware family (ransomware variant, ICS-specific malware like Triton/Trisis)
    - Extract indicators of compromise (IOCs): file hashes, IP addresses, domains

  log_analysis:
    - Windows Event Logs: Logon events (4624), process creation (4688)
    - PLC logs: Program downloads, online/offline transitions, faulted states
    - Firewall logs: Blocked connections, allowed traffic anomalies
    - SIEM correlation: Multi-system event timelines

  network_forensics:
    - Identify command-and-control (C2) traffic (beaconing patterns)
    - Data exfiltration detection (large outbound transfers)
    - Lateral movement (SMB, RDP, WMI connections between systems)
    - Industrial protocol anomalies (unauthorized Modbus writes)

reporting_findings:
  technical_report:
    audience: Cybersecurity team, IT management
    content:
      - Executive summary (1-page incident overview)
      - Detailed timeline (minute-by-minute for critical period)
      - Attack vectors and techniques (MITRE ATT&CK framework mapping)
      - Indicators of compromise (IOCs for threat hunting)
      - Remediation recommendations (patch vulnerabilities, improve monitoring)

  food_safety_report:
    audience: Food Safety Lead, QA, regulatory agencies
    content:
      - Process impact assessment (which systems compromised, when, for how long)
      - Product safety evaluation (were critical control points affected?)
      - Traceability data (lot codes, production dates, distribution)
      - Corrective actions (product disposition, process improvements)

  legal_report:
    audience: General Counsel, external legal advisors
    content:
      - Incident facts (who, what, when, where, how)
      - Regulatory obligations triggered (FDA, USDA, state agencies)
      - Potential liabilities (customer claims, regulatory penalties)
      - Evidence preservation status (chain of custody intact)

  executive_briefing:
    audience: CEO, Board of Directors, investors
    content:
      - Business impact (revenue loss, reputational damage)
      - Customer/partner communication status
      - Media coverage and public perception
      - Long-term strategic recommendations (cybersecurity investments)

external_resources:
  forensics_firms:
    - Mandiant (FireEye): Industrial control system expertise
    - CrowdStrike: Threat intelligence and attribution
    - Dragos: ICS/SCADA focused incident response
    - Stroz Friedberg (Aon): Legal/forensic hybrid services

  law_enforcement:
    - FBI Cyber Division: For nation-state or organized crime attacks
    - Secret Service: For cyber fraud or financial crimes
    - State/local police: For insider threat or physical security aspects

  regulatory_agencies:
    - FDA Office of Criminal Investigations (OCI): For intentional adulteration
    - USDA FSIS: For meat/poultry cyber incidents
    - DHS CISA: For critical infrastructure sector coordination
```

## Recovery and Restoration Patterns

### 3. System Recovery Procedures

#### Pattern: Clean Room PLC Restoration
```yaml
pattern_id: FOOD-IR-005
name: Secure PLC Program Restoration from Backup
description: Verified clean restoration of PLC programs after cyber incident
severity: CRITICAL
pre_restoration_validation:
  backup_verification:
    - Identify last known good backup (before incident start time)
    - Verify backup integrity (hash check against original)
    - Test backup in offline PLC (do not connect to production network yet)
    - Ensure backup is not infected (compare with validated baseline from commissioning)

  hardware_inspection:
    - Physical inspection of PLC for tampering (broken seals, unauthorized modules)
    - Firmware version check (ensure not maliciously downgraded or modified)
    - Memory card inspection (remove and scan for malware if SD/CF card used)
    - I/O module verification (correct modules in correct slots, no rogue devices)

  network_isolation:
    - Disconnect PLC from production network (physically unplug Ethernet)
    - Use dedicated programming laptop (not connected to any network)
    - Disable wireless interfaces on programming laptop (Wi-Fi, Bluetooth)
    - Virus scan programming laptop before use (air-gapped or freshly imaged)

restoration_procedure:
  step_1_firmware_reload:
    - Download PLC firmware from vendor official source (Siemens, Rockwell Automation)
    - Verify firmware file integrity (vendor-provided hash or digital signature)
    - Flash firmware to PLC using manufacturer tools (TIA Portal, Studio 5000)
    - Document firmware version installed (for audit trail)

  step_2_program_upload:
    - Load verified backup program file to programming laptop
    - Upload program to PLC (using RS232/USB direct connection if possible)
    - Verify upload success (no errors, CRC check matches)
    - Document program version and upload timestamp

  step_3_configuration_restore:
    - Restore IP address and network settings (consult as-built documentation)
    - Configure security settings (password, access levels)
    - Re-establish PLC-to-HMI communication (if HMI also restored clean)
    - Do not reconnect to production network yet (next phase is testing)

  step_4_offline_testing:
    - Simulate I/O using test harness (input simulators, output monitors)
    - Execute program in test mode (ensure logic executes correctly)
    - Verify safety interlocks (test e-stop, high-pressure shutdown logic)
    - Check recipe/parameter files (ensure setpoints match validated values)

  step_5_network_reconnection:
    - Scan PLC with industrial network security tool (Claroty, Nozomi)
    - Verify no unauthorized network services running (Nmap scan from trusted source)
    - Reconnect to isolated test network first (not production)
    - Monitor network traffic for anomalies (baseline vs. actual traffic)

  step_6_production_validation:
    - Perform operational qualification (OQ) testing per validation protocol
    - Run equipment in manual mode with product flow (low-speed test)
    - Verify critical control loops (temperature, pressure, flow)
    - Food Safety Lead approval before full production restart

validation_documentation:
  validation_protocol:
    - Document restoration procedure followed (step-by-step checklist)
    - Record test results (I/O checks, logic execution, safety interlocks)
    - Attach evidence (screenshots, test data, logs)
    - Approval signatures (validation engineer, food safety, production manager)

  change_control:
    - If restoration involved any program changes (e.g., patches applied)
    - Formal change request with justification
    - Impact assessment (safety, quality, regulatory)
    - Regression testing to ensure no unintended consequences

  traceability:
    - Link restored system to product batches produced after restart
    - Ensure batch records indicate "system restored from cyber incident"
    - Enhanced monitoring for first 48-72 hours post-restoration (verify stable operation)

special_considerations:
  safety_instrumented_systems:
    - SIS (Safety Instrumented System) requires additional rigor (SIL 2/3 requirements)
    - Independent verification by certified functional safety engineer
    - Proof testing after restoration (demand actual safety function to trip)
    - Documentation per IEC 61511 requirements

  validated_systems:
    - 21 CFR Part 11 validated systems require revalidation after restoration
    - Validation documentation updated (system revision history)
    - Potentially notify FDA if significant system changes made

  legacy_systems:
    - Older PLCs may lack backup/restore capabilities (PLC-2, PLC-5)
    - Restoration may require manual ladder logic entry (time-consuming)
    - Consider upgrade to modern PLC if restoration not feasible
```

#### Pattern: Business Continuity During Extended Recovery
```yaml
pattern_id: FOOD-IR-006
name: Manual Operations and Alternative Production Methods
description: Maintaining food production during prolonged control system outage
severity: HIGH
manual_operation_readiness:
  prerequisite_documentation:
    - Manual standard operating procedures (SOPs) printed and accessible
    - P&IDs (Piping & Instrumentation Diagrams) for manual valve locations
    - Critical parameter checklists (temperatures, pressures, flow rates to monitor)
    - Emergency contact lists (vendors, regulatory agencies, customers)

  equipment_requirements:
    - Portable temperature monitoring devices (calibrated thermometers, data loggers)
    - Manual timers and stopwatches (for hold time verification in pasteurization)
    - Handheld meters (pressure gauges, flow meters)
    - Paper batch record forms (for documentation when MES offline)

  personnel_training:
    - Annual manual operations drills (simulate control system failure)
    - Cross-training operators on multiple production lines
    - On-call roster for extended shifts (24/7 coverage during incident)

alternative_production_scenarios:
  scenario_1_partial_automation:
    description: Some control systems operational, others manual
    approach:
      - Prioritize critical food safety systems for restoration (pasteurization, CIP)
      - Operate non-critical systems manually (packaging line at reduced speed)
      - Use manual data entry to MES/ERP for traceability
    capacity_impact: 50-70% of normal production throughput

  scenario_2_full_manual_operations:
    description: All automation down, entire process manual
    approach:
      - Assign dedicated operators to each critical control point
      - Manual valve operation for product flow, ingredient addition
      - Visual inspection replacing automated quality checks (more labor-intensive)
      - Paper-based documentation (batch records, quality logs)
    capacity_impact: 20-40% of normal production throughput

  scenario_3_third_party_production:
    description: Co-packer or sister facility produces product
    approach:
      - Transfer production to qualified co-manufacturer (pre-vetted partner)
      - Provide formulations, specifications, quality requirements
      - Audit co-packer's operations for food safety compliance
      - Ensure traceability maintained (co-packer lot codes tracked)
    capacity_impact: Depends on co-packer availability, 50-100% capacity possible

  scenario_4_product_substitution:
    description: Simplify product portfolio to maintain core SKUs
    approach:
      - Prioritize high-volume or food safety critical products
      - Temporarily discontinue low-volume or complex SKUs
      - Communicate with customers about temporary product unavailability
    capacity_impact: Maintain 80-100% of revenue with fewer SKUs

food_safety_considerations:
  maintaining_ccps:
    - Critical Control Points (HACCP CCPs) must be monitored regardless of automation
    - Pasteurization: Manual verification of temperature and time (use chart recorders if SCADA down)
    - CIP: Manual concentration testing of caustic/acid (titration kits)
    - Metal detection: Verify operation with test pieces every 30 minutes

  enhanced_verification:
    - Increased testing frequency during manual operations (every batch vs. hourly)
    - Third-party laboratory analysis for critical parameters (microbial, allergen)
    - Quality hold all production until enhanced verification results available

  regulatory_notification:
    - Inform FDA/USDA of temporary manual operations (via email to district office)
    - Document all deviations from normal process in batch records
    - Retain enhanced testing records for inspection readiness

customer_communication:
  proactive_outreach:
    - Notify customers within 24 hours of incident (if production delays expected)
    - Provide realistic timelines for order fulfillment
    - Offer alternative products or sources if available

  transparency_levels:
    - Confidential: Detailed technical information about cyber incident (limit to close partners)
    - General: "Experiencing production delays due to system issue, working to resolve"
    - Public: Media statement only if required (coordinate with PR and legal)

  service_recovery:
    - Expedite shipping when production resumes (absorb freight costs)
    - Offer discounts or credits for late deliveries
    - Document lessons learned to prevent future disruptions

financial_impact_tracking:
  direct_costs:
    - Revenue loss from production downtime ($X per hour of stopped production)
    - Overtime pay for extended manual operations
    - Forensics and remediation costs (external consultants)
    - Replacement equipment costs (if hardware destroyed by malware)

  indirect_costs:
    - Customer penalty payments (for late deliveries)
    - Product waste (if batches cannot be released due to data integrity concerns)
    - Regulatory fines (if FDA/USDA citations issued)
    - Reputational damage (lost future sales, customer attrition)

  insurance_claims:
    - Business interruption insurance (covers lost revenue during downtime)
    - Cyber insurance (forensics, legal, notification costs)
    - Product liability insurance (if recalled product results from incident)
    - Document all costs meticulously for claim substantiation
```

## Post-Incident Activities

### 4. Root Cause Analysis & Lessons Learned

#### Pattern: Cyber Incident Root Cause Analysis
```yaml
pattern_id: FOOD-IR-007
name: Structured Root Cause Analysis for Food Cyber Incidents
description: Systematic investigation to prevent recurrence
severity: MEDIUM
analysis_methodology:
  five_whys:
    example: Pasteurization temperature dropped during cyber incident
    why_1: "Why did temperature drop?"
      - Answer: "PLC setpoint was changed from 161°F to 140°F"
    why_2: "Why was PLC setpoint changed?"
      - Answer: "Attacker accessed HMI and modified parameter"
    why_3: "Why could attacker access HMI?"
      - Answer: "HMI workstation infected with malware via USB drive"
    why_4: "Why was USB drive able to infect HMI?"
      - Answer: "Endpoint protection software not installed on HMI (assumed not needed)"
    why_5: "Why was endpoint protection not installed?"
      - Answer: "Risk assessment did not consider USB as threat vector for OT systems"
    root_cause: "Inadequate risk assessment failed to identify USB-borne malware threat to HMI workstations"

  fishbone_diagram:
    categories:
      people:
        - Insufficient cybersecurity training for operators
        - Lack of awareness of social engineering tactics
        - Inadequate vendor background checks
      process:
        - No USB device policy for production floor
        - Change control process did not cover parameter changes
        - Incident response plan not tested regularly
      technology:
        - HMI operating system not patched (Windows 7 end-of-life)
        - Application whitelisting not enabled
        - Network segmentation inadequate (HMI and ERP on same network)
      environment:
        - Production pressure prioritized over security (shortcuts taken)
        - Budget constraints prevented security tool deployment
        - Culture of "if it's not broken, don't fix it" (resistance to updates)

  fault_tree_analysis:
    top_event: "Food safety compromise due to cyber incident"
    intermediate_events:
      - Pasteurization temperature deviation (OR gate)
        - PLC setpoint modified (AND gate)
          - Attacker access to HMI (basic event: malware infection)
          - Lack of parameter change alarms (basic event: monitoring gap)
        - Temperature sensor failure (OR gate)
          - Physical tampering (low probability)
          - Sensor drift (preventable via calibration)

corrective_actions:
  immediate_fixes:
    - Remove USB ports from all HMI workstations (physical removal or epoxy)
    - Deploy endpoint protection on all Windows-based OT systems
    - Enable parameter change alarms in SCADA (alert on any setpoint modification)
    - Conduct emergency cybersecurity training for all production staff

  short_term_improvements:
    - Implement application whitelisting on all OT workstations (within 90 days)
    - Upgrade all HMI operating systems to Windows 10 IoT LTSC (Long-Term Servicing Channel)
    - Deploy industrial firewall between HMI network and ERP/office network
    - Establish formal USB device policy (only company-issued, scanned USBs allowed)

  long_term_strategic_changes:
    - Redesign network architecture per Purdue Model (full Level 0-5 segmentation)
    - Implement continuous OT network monitoring (Claroty, Nozomi, Dragos)
    - Establish ongoing penetration testing program (annual OT security assessments)
    - Create dedicated OT security role (hire or train ICS cybersecurity specialist)

preventive_actions:
  policy_updates:
    - Removable media policy (USB drives, SD cards, external hard drives)
    - Password policy (complexity, rotation, no shared accounts)
    - Vendor access policy (MFA, session recording, approval workflow)
    - Change control policy (include cybersecurity review for all OT changes)

  technical_controls:
    - Multi-factor authentication for all administrative access
    - Network segmentation (VLANs, firewalls, unidirectional gateways)
    - Security monitoring (SIEM, IDS, anomaly detection)
    - Backup and recovery (offline backups, tested restoration procedures)

  organizational_changes:
    - Security awareness training (annual for all employees, quarterly for OT staff)
    - Tabletop exercises (biannual cyber incident drills)
    - Vendor management program (cybersecurity assessments for all OT vendors)
    - Bug bounty or vulnerability disclosure program (encourage external reporting)

lessons_learned_documentation:
  incident_report_components:
    - Executive summary (1-page overview for leadership)
    - Detailed timeline (minute-by-minute during critical period)
    - Technical analysis (attack vectors, vulnerabilities exploited)
    - Business impact assessment (financial, operational, reputational)
    - Root cause analysis (five whys, fishbone, fault tree)
    - Corrective and preventive actions (with responsible parties and due dates)
    - Recommendations (short-term and long-term improvements)

  distribution:
    - Internal: Executive leadership, board of directors, all incident response team members
    - External: Regulatory agencies (if required), insurance carrier, customers (high-level summary only)
    - Industry: Anonymized sharing via Food-ISAC (advance industry cybersecurity)

  follow_up:
    - 30-day review: Verify immediate fixes implemented
    - 90-day review: Assess short-term improvements progress
    - Annual review: Evaluate long-term strategic changes
    - Continuous monitoring: Track metrics (time to detect, time to respond, number of incidents)

knowledge_sharing:
  internal_communication:
    - Facility-wide safety meeting: High-level incident overview (no sensitive details)
    - Department-specific briefings: Tailored lessons learned (e.g., IT, Production, QA)
    - Leadership debrief: Strategic recommendations and resource needs

  industry_collaboration:
    - Food-ISAC (Food and Agriculture Information Sharing and Analysis Center)
    - Participation in industry working groups (GMA, FMI cybersecurity committees)
    - Conference presentations (anonymized case studies)

  regulatory_engagement:
    - FDA voluntary sharing of cyber incident trends (aggregate, non-identifying data)
    - Participation in FDA cybersecurity pilot programs
    - Input on emerging regulations (comment on proposed rules)
```

## Summary

This document provides 7 comprehensive incident response and recovery patterns:

1. **Food Safety Cyber Incident Classification** - Severity matrix and decision tree for prioritizing incidents with food safety impact
2. **Incident Response Team Structure** - Multi-disciplinary team roles, responsibilities, and activation procedures
3. **Emergency Production Shutdown** - Safe halt procedures for compromised control systems
4. **Forensic Evidence Preservation** - Digital evidence collection for cyber incidents affecting food production
5. **Clean Room PLC Restoration** - Secure restoration of PLC programs from verified clean backups
6. **Business Continuity During Recovery** - Manual operations and alternative production methods
7. **Cyber Incident Root Cause Analysis** - Structured investigation methodology using five whys, fishbone, and fault tree analysis

**Total Patterns in This Document: 50+**

## Cross-References
- See `/01_Security_SCADA_ICS_Protection.md` for preventive security controls
- See `/02_Security_Network_Segmentation.md` for architecture hardening
- See `/05_Operations_Business_Continuity.md` for production continuity planning
- See `/08_Standards_FDA_USDA_GFSI.md` for regulatory reporting requirements
