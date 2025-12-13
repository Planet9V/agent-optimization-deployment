# IEC 62443 Project Information Requirements

## Complete Data Collection and Prerequisites Checklist for CSMS, ZCR, and Implementation

**Version 1.0**  
**Document Date: October 2025**

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Critical Prerequisites](#prerequisites)
3. [Organizational Information Requirements](#organizational)
4. [Asset Inventory Data Requirements](#asset-inventory)
5. [Network and Architecture Information](#network)
6. [Business and Operational Information](#business-operations)
7. [Security Current State Assessment](#current-state)
8. [Regulatory and Compliance Requirements](#regulatory)
9. [Personnel and Training Information](#personnel)
10. [Documentation and Records](#documentation)
11. [Information Sources and Collection Methods](#sources)
12. [Data Collection Checklist](#checklist)

---

## 1. Executive Summary {#executive-summary}

Implementing IEC 62443 standards and creating a Cybersecurity Management System (CSMS) with proper zone and conduit documentation requires comprehensive information gathering. This document provides a complete checklist of required information organized by category.

**Total Information Categories**: 10  
**Essential Data Points**: 200+  
**Typical Collection Timeline**: 4-12 weeks

### Quick Reference: What You Absolutely Need to Start

**Minimum Required Information** (Week 1-2):
1. ✅ **Organizational chart** with key contacts
2. ✅ **Asset inventory** (even preliminary/incomplete)
3. ✅ **Network diagrams** (high-level acceptable)
4. ✅ **List of critical business processes** dependent on control systems
5. ✅ **Regulatory requirements** applicable to your industry
6. ✅ **Current security policies** (if any exist)
7. ✅ **Recent security incidents** or near-misses
8. ✅ **Budget and timeline constraints**

---

## 2. Critical Prerequisites {#prerequisites}

### 2.1 Executive Sponsorship and Commitment

**Required Documentation**:

| Item | Description | Purpose |
|------|-------------|---------|
| **Executive Sponsor Letter** | Formal commitment from C-level executive | Demonstrates management support |
| **Project Charter** | Defines scope, objectives, authority | Establishes project framework |
| **Budget Authorization** | Approved budget with line items | Ensures adequate resources |
| **Resource Allocation** | Dedicated personnel assignments | Identifies key team members |

**Key Questions to Answer**:
- [ ] Who is the executive sponsor for this initiative?
- [ ] What is the business driver (regulatory, risk reduction, customer requirement)?
- [ ] What is the approved budget range?
- [ ] What is the target timeline for compliance/certification?
- [ ] Are there competing priorities that could affect resources?

### 2.2 Scope Definition

**System Under Consideration (SuC) Definition**:

```
Required Information:
├─ SuC Name and Identifier
├─ Physical Boundaries
│  ├─ Geographic locations included
│  ├─ Facilities/sites
│  └─ Excluded areas (with justification)
├─ Logical Boundaries
│  ├─ Network boundaries
│  ├─ System boundaries
│  └─ Excluded systems (with justification)
├─ Business Processes Supported
│  ├─ Production processes
│  ├─ Safety systems
│  └─ Support systems
└─ Connected External Systems
   ├─ Corporate networks
   ├─ Vendor remote access
   └─ Cloud services
```

**Scope Documentation Template**:

```markdown
# System Under Consideration: [SuC Name]

## Geographic Scope
- **Sites Included**: [List all sites]
- **Sites Excluded**: [List excluded sites with rationale]

## System Scope
- **Control Systems**: [List SCADA, DCS, PLC networks, etc.]
- **Safety Systems**: [List SIS, F&G, ESD, etc.]
- **Support Systems**: [List historians, engineering workstations, etc.]
- **Excluded Systems**: [List with justification]

## Business Process Scope
- **Primary Processes**: [e.g., Production, Distribution, Treatment]
- **Support Processes**: [e.g., Maintenance, Engineering, Quality]

## Interfaces and Boundaries
- **External Connections**: [Corporate, vendor, cloud, partners]
- **Trust Boundaries**: [Where does our control/responsibility end?]

## Constraints
- **Technical**: [e.g., Cannot modify safety systems]
- **Operational**: [e.g., 24/7 operations, cannot tolerate downtime]
- **Regulatory**: [e.g., Must comply with specific regulations]
- **Budget**: [e.g., Limited to $XXX]
- **Timeline**: [e.g., Must achieve SL-2 by Q4 2026]
```

### 2.3 Team Formation

**Required Roles and Contact Information**:

| Role | Name | Department | Email | Phone | Responsibilities |
|------|------|------------|-------|-------|------------------|
| **Project Sponsor** | | Executive | | | Overall authority and funding |
| **Project Manager** | | IT/OT | | | Day-to-day project management |
| **CISO / Security Lead** | | Security | | | Security strategy and oversight |
| **OT Manager** | | Operations | | | Operations and process expertise |
| **IT Manager** | | IT | | | IT systems and infrastructure |
| **Network Engineer** | | IT/OT | | | Network architecture and design |
| **Control Systems Engineer** | | Engineering | | | Control system configuration |
| **Safety Manager** | | HSE | | | Safety system integration |
| **Compliance Officer** | | Legal/Compliance | | | Regulatory requirements |
| **Risk Manager** | | Risk/Finance | | | Risk assessment methodology |

**Additional Expertise Needed**:
- [ ] IEC 62443 certified consultant/assessor (internal or external)
- [ ] Risk assessment facilitator
- [ ] Technical writer (for documentation)
- [ ] Network security architect
- [ ] Vendor representatives (for component certification)

---

## 3. Organizational Information Requirements {#organizational}

### 3.1 Company and Site Information

**Basic Information**:

```yaml
Company_Information:
  legal_name: ""
  trade_name: ""
  headquarters_location: ""
  industry_sector: ""  # Manufacturing, Utilities, Chemical, etc.
  company_size: ""     # Employees, revenue range
  
Sites:
  - site_id: ""
    site_name: ""
    address: ""
    geographic_coordinates: ""
    site_type: ""      # Production, Distribution, Support
    operational_hours: ""  # 24/7 or scheduled
    personnel_count: ""
    critical_to_business: "" # High/Medium/Low
```

### 3.2 Organizational Structure

**Required Diagrams and Information**:

1. **Overall Organization Chart**
   - Corporate structure
   - Site structure
   - Reporting relationships
   - Dotted-line relationships

2. **Security Organization**
   - Security governance structure
   - Security committee composition
   - Escalation paths
   - Decision-making authority

3. **IT/OT Organizational Structure**
   - IT department structure
   - OT/Operations department structure
   - Shared services
   - Vendor support relationships

**RACI Matrix Template** (for security activities):

| Activity | IT Manager | OT Manager | Security | Network Eng | Executives |
|----------|-----------|------------|----------|-------------|------------|
| Risk Assessment | C | A | R | C | I |
| Zone Design | I | C | R | A | I |
| Policy Approval | I | I | R | I | A |
| Incident Response | C | A | R | R | I |
| Change Management | C | A | C | R | I |

Legend: R=Responsible, A=Accountable, C=Consulted, I=Informed

### 3.3 Policies and Procedures

**Existing Documentation to Collect**:

| Document Type | Current Status | Location | Last Updated | Notes |
|---------------|----------------|----------|--------------|-------|
| Information Security Policy | ☐ Exists ☐ Doesn't Exist | | | |
| Access Control Policy | ☐ Exists ☐ Doesn't Exist | | | |
| Password Policy | ☐ Exists ☐ Doesn't Exist | | | |
| Remote Access Policy | ☐ Exists ☐ Doesn't Exist | | | |
| Change Management Procedures | ☐ Exists ☐ Doesn't Exist | | | |
| Incident Response Plan | ☐ Exists ☐ Doesn't Exist | | | |
| Business Continuity Plan | ☐ Exists ☐ Doesn't Exist | | | |
| Disaster Recovery Plan | ☐ Exists ☐ Doesn't Exist | | | |
| Patch Management Procedures | ☐ Exists ☐ Doesn't Exist | | | |
| Backup Procedures | ☐ Exists ☐ Doesn't Exist | | | |
| Physical Security Plan | ☐ Exists ☐ Doesn't Exist | | | |
| Personnel Security Procedures | ☐ Exists ☐ Doesn't Exist | | | |
| Vendor Management Procedures | ☐ Exists ☐ Doesn't Exist | | | |

---

## 4. Asset Inventory Data Requirements {#asset-inventory}

### 4.1 Comprehensive Asset Inventory

**Required for EVERY Asset**:

```yaml
Asset_Record:
  # Identification
  asset_id: ""           # Unique identifier
  asset_name: ""         # Descriptive name
  asset_tag: ""          # Physical asset tag number
  
  # Classification
  asset_type: ""         # Server, PLC, HMI, Workstation, Network Device, etc.
  asset_category: ""     # Control System, Safety System, IT System, Network, etc.
  manufacturer: ""
  model: ""
  serial_number: ""
  
  # Location
  site: ""
  building: ""
  room: ""
  rack_location: ""      # If applicable
  zone_assignment: ""    # To be determined during ZCR
  
  # Technical Specifications
  operating_system: ""
  os_version: ""
  firmware_version: ""
  ip_address_primary: ""
  ip_address_secondary: ""  # If redundant
  mac_address: ""
  hostname: ""
  
  # Network Connectivity
  network_interfaces: []
  vlan_assignment: []
  connected_networks: []
  protocols_used: []     # Modbus, OPC, DNP3, etc.
  
  # Function and Criticality
  function_description: ""
  business_process: ""   # What process does this support?
  criticality: ""        # Critical, High, Medium, Low
  safety_related: ""     # Yes/No
  sil_level: ""          # If safety instrumented system
  
  # Availability Requirements
  required_uptime: ""    # 99.9%, 99.99%, etc.
  max_tolerable_downtime: ""  # Hours or minutes
  redundancy: ""         # Yes/No
  backup_device: ""      # Asset ID of backup
  
  # Security Attributes
  security_level_capability: ""  # SL-C (1-4)
  security_level_target: ""      # SL-T (to be determined)
  security_level_achieved: ""    # SL-A (current state)
  authentication_method: ""
  encryption_capability: ""
  audit_logging_enabled: ""
  antivirus_installed: ""
  firewall_enabled: ""
  
  # Patch Management
  patch_status: ""       # Current, Behind, Critical Gaps
  last_patched_date: ""
  next_patch_window: ""
  patching_constraints: ""  # e.g., Cannot patch - vendor restriction
  
  # Lifecycle
  installation_date: ""
  warranty_expiration: ""
  eol_date: ""           # End of life
  eos_date: ""           # End of support
  planned_replacement_date: ""
  
  # Ownership and Contact
  asset_owner: ""        # Department/person responsible
  technical_contact: ""
  vendor_contact: ""
  support_contract: ""   # Contract number if applicable
  
  # Documentation
  technical_manual_location: ""
  configuration_backup_location: ""
  as-built_drawings: ""
  
  # Vulnerability and Compliance
  known_vulnerabilities: []  # CVE numbers
  compliance_requirements: []  # Regulations applicable
  last_vulnerability_scan: ""
  last_security_audit: ""
```

### 4.2 Asset Inventory Collection Methods

**Available Collection Methods** (use combination):

1. **Network Discovery Scans**
   - Tools: Nessus, Qualys, Tenable.ot, Claroty, Nozomi Networks
   - Caution: Passive scanning preferred for OT; active scanning may disrupt
   - Provides: IP addresses, open ports, services, some OS detection

2. **Manual Surveys**
   - Site walkdowns with asset tagging
   - Interviews with operators and engineers
   - Review of existing spreadsheets/databases

3. **Configuration Management Database (CMDB)**
   - Export from existing IT asset management systems
   - May be incomplete for OT assets

4. **Engineering Documentation Review**
   - P&IDs (Process and Instrumentation Diagrams)
   - Control system architecture documents
   - Network diagrams
   - Equipment lists

5. **Procurement Records**
   - Purchase orders
   - Vendor quotes
   - Asset tags assigned during receiving

**Asset Inventory Template** (Minimum CSV Format):

```csv
Asset_ID,Name,Type,Location,IP_Address,OS,Criticality,Zone,Owner,Notes
ASSET-001,SCADA-01,Server,Control Room A,10.1.1.50,Windows Server 2022,High,TBD,OT Team,Primary SCADA
ASSET-002,PLC-101,PLC,Field Cabinet 1,10.2.1.10,Proprietary,Critical,TBD,Operations,Production Line 1
...
```

### 4.3 Special Asset Categories

**Safety Systems** (require special attention):

| Attribute | Information Needed |
|-----------|-------------------|
| SIL Level | SIL 1, 2, 3, or 4 |
| Safety Function | Description of safety function |
| Certification | TÜV, FM, etc. certification details |
| Proof Test Interval | Frequency of safety function testing |
| Bypass Procedures | How system can be bypassed and controls |
| Maintenance Restrictions | Any limitations on maintenance |

**Legacy Systems** (may have limited security capability):

| Attribute | Information Needed |
|-----------|-------------------|
| Age | Years in service |
| Vendor Support Status | Supported, limited, end-of-life |
| Known Limitations | Cannot authenticate, cannot patch, etc. |
| Compensating Controls | What protections are in place |
| Replacement Plan | When will this be upgraded/replaced |

**Third-Party Managed Systems**:

| Attribute | Information Needed |
|-----------|-------------------|
| Service Provider | Company name and contact |
| Support Contract | Contract terms and SLAs |
| Access Method | How do they connect (VPN, remote, etc.) |
| Access Schedule | When is access permitted |
| Monitoring | How is their access monitored |

---

## 5. Network and Architecture Information {#network}

### 5.1 Network Diagrams

**Required Network Documentation**:

1. **High-Level Network Diagram**
   - All major network segments
   - Firewalls and security boundaries
   - External connections
   - Approximate asset counts per segment

2. **Detailed Network Diagrams** (per site/area)
   - All network devices (switches, routers)
   - All connected assets
   - IP addressing scheme
   - VLANs
   - Physical and logical topology

3. **Data Flow Diagrams**
   - Communication paths between systems
   - Protocols used
   - Direction of data flow
   - External data flows

**Network Information to Document**:

```yaml
Network_Segment:
  segment_id: ""
  segment_name: ""
  description: ""
  
  # Addressing
  ip_subnet: ""          # e.g., 10.1.0.0/24
  vlan_id: ""
  vlan_name: ""
  gateway: ""
  dns_servers: []
  
  # Physical
  switches: []           # List of switch names/IPs
  physical_location: ""
  cable_type: ""         # Copper, Fiber, Wireless
  
  # Security
  firewall_protected: "" # Yes/No
  ids_ips_monitored: ""  # Yes/No
  segmented_from: []     # Other segments
  allowed_protocols: []
  
  # Assets
  asset_count: 0
  asset_types: []        # Types of assets on segment
  critical_assets: []    # List of critical assets
  
  # Usage
  purpose: ""            # Production, Safety, IT, DMZ
  bandwidth_usage: ""
  typical_traffic: ""    # Description
```

### 5.2 Network Device Inventory

**For Each Network Device** (switches, routers, firewalls):

| Attribute | Information Needed |
|-----------|-------------------|
| Device Name | Hostname |
| Device Type | Managed switch, router, firewall, etc. |
| Location | Physical location |
| Management IP | IP address for management |
| Make/Model | Manufacturer and model |
| OS/Firmware Version | Current version |
| Configuration Backup | Date and location of last backup |
| VLAN Configuration | List of VLANs |
| Port Configuration | Trunk ports, access ports |
| Access Control | How is device accessed (SSH, console, etc.) |
| Redundancy | Redundant pair, standalone |

### 5.3 Communication Protocols

**Protocol Inventory**:

| Protocol | Where Used | Security Features | Risks | Mitigations |
|----------|------------|-------------------|-------|-------------|
| Modbus TCP | Control network | None (plaintext) | Unauthorized commands | Network segmentation, firewall rules |
| OPC UA | SCADA to DCS | TLS encryption, authentication | Misconfiguration | Proper certificate management |
| DNP3 | SCADA to RTUs | Optional SA (Secure Authentication) | Man-in-the-middle | Enable SA where supported |
| Profibus DP | Field devices | None | Physical access | Physical security |
| EtherNet/IP | Allen-Bradley devices | CIP Security | Unauthorized access | Device authentication |
| BACnet | Building automation | Optional BACnet/SC | None in legacy | Network segmentation |
| ... | ... | ... | ... | ... |

### 5.4 External Connections

**For Each External Connection**:

```yaml
External_Connection:
  connection_id: ""
  connection_name: ""
  
  # Connected Party
  external_party: ""     # Company/entity name
  purpose: ""            # Vendor support, data exchange, etc.
  
  # Technical Details
  connection_type: ""    # VPN, leased line, internet, etc.
  bandwidth: ""
  protocols: []
  
  # Access Control
  authentication_method: ""
  access_hours: ""       # 24/7, business hours, on-demand
  approval_process: ""   # Who approves access
  monitoring: ""         # How is this connection monitored
  
  # Security
  encryption: ""         # Yes/No, method
  firewall_rules: ""     # Reference to ruleset
  mfa_required: ""       # Yes/No
  jump_host_required: "" # Yes/No
  
  # Business
  contract_reference: ""
  business_owner: ""
  technical_contact: ""
  
  # Risk
  risk_level: ""         # High/Medium/Low
  compensating_controls: []
```

---

## 6. Business and Operational Information {#business-operations}

### 6.1 Business Process Mapping

**For Each Critical Business Process**:

```yaml
Business_Process:
  process_id: ""
  process_name: ""
  description: ""
  
  # Business Impact
  criticality: ""        # Critical, High, Medium, Low
  revenue_impact: ""     # $/hour of downtime
  safety_impact: ""      # Description of safety consequences
  environmental_impact: ""
  regulatory_impact: ""  # Fines, reporting requirements
  reputation_impact: ""
  
  # Process Details
  owner: ""
  supporting_systems: [] # List of IACS/IT systems
  dependencies: []       # Other processes this depends on
  upstream_processes: []
  downstream_processes: []
  
  # Operations
  operating_hours: ""    # 24/7, scheduled
  staffing: ""           # Number of operators
  production_rate: ""    # Units/hour, etc.
  
  # Availability Requirements
  required_availability: ""  # 99.9%, etc.
  maximum_tolerable_outage: ""  # Minutes or hours
  recovery_time_objective: ""   # RTO
  recovery_point_objective: ""  # RPO
  
  # Failure Scenarios
  typical_failures: []   # Historical failures
  failure_frequency: ""
  mean_time_to_repair: ""  # MTTR
  
  # Cybersecurity Considerations
  cyber_dependent: ""    # High/Medium/Low
  cyber_attack_consequences: ""  # Description
  existing_cyber_controls: []
```

### 6.2 Operational Constraints

**Constraints That Affect Implementation**:

| Constraint Type | Details | Impact on IEC 62443 |
|-----------------|---------|---------------------|
| **Operational Hours** | 24/7 production | Limited maintenance windows |
| **Safety Restrictions** | Cannot modify SIS without re-certification | Need compensating controls |
| **Production Schedule** | Peak season June-August | Plan changes around schedule |
| **Staffing** | Limited IT/OT personnel | May need external support |
| **Training Requirements** | Operators must be certified | Training time required |
| **Environmental** | Harsh environment (temperature, dust) | Hardware limitations |
| **Physical Access** | Remote locations, limited access | Maintenance challenges |
| **Union Agreements** | Work rules | May affect who can do what |

### 6.3 Financial Information

**Budget Information**:

```yaml
Budget:
  # Capital Budget
  capex_available: 0
  capex_approval_process: ""
  capex_timeline: ""
  
  # Operating Budget
  opex_available: 0
  opex_approval_process: ""
  
  # Cost Categories
  hardware_budget: 0
  software_licensing: 0
  external_consultants: 0
  training: 0
  travel: 0
  certification_fees: 0
  contingency: 0
  
  # Cost Justification Data
  current_cyber_insurance_premium: 0
  historical_incident_costs: []
  regulatory_fine_risk: 0
  business_interruption_cost_per_hour: 0
```

**ROI Calculation Inputs**:

| Factor | Current State | Target State | Benefit |
|--------|---------------|--------------|---------|
| Cyber Insurance Premium | $XXX/year | $YYY/year (with IEC 62443) | Savings |
| Incident Frequency | X/year | Projected reduction | Avoided costs |
| Compliance Fines Risk | $XXX potential | Reduced to $YYY | Risk reduction |
| Audit Costs | $XXX/year | Reduced by automation | Savings |
| Customer Requirements | May lose business | Competitive advantage | Revenue protection |

---

## 7. Security Current State Assessment {#current-state}

### 7.1 Existing Security Controls Inventory

**Technical Controls**:

| Control Category | Control | Implemented? | Coverage | Effectiveness | Notes |
|------------------|---------|--------------|----------|---------------|-------|
| **Network Segmentation** | Firewalls | ☐ Yes ☐ Partial ☐ No | __% of boundaries | ☐ Effective ☐ Partial ☐ Ineffective | |
| | VLANs | ☐ Yes ☐ Partial ☐ No | | | |
| | Air gaps | ☐ Yes ☐ Partial ☐ No | | | |
| **Access Control** | Authentication | ☐ Yes ☐ Partial ☐ No | | | |
| | Authorization | ☐ Yes ☐ Partial ☐ No | | | |
| | MFA | ☐ Yes ☐ Partial ☐ No | | | |
| **Monitoring** | IDS/IPS | ☐ Yes ☐ Partial ☐ No | | | |
| | SIEM | ☐ Yes ☐ Partial ☐ No | | | |
| | Log collection | ☐ Yes ☐ Partial ☐ No | | | |
| **Endpoint Protection** | Antivirus | ☐ Yes ☐ Partial ☐ No | __% of systems | | |
| | Application whitelisting | ☐ Yes ☐ Partial ☐ No | | | |
| | Host firewalls | ☐ Yes ☐ Partial ☐ No | | | |
| **Patch Management** | Patch tracking | ☐ Yes ☐ Partial ☐ No | | | |
| | Testing process | ☐ Yes ☐ Partial ☐ No | | | |
| | Deployment automation | ☐ Yes ☐ Partial ☐ No | | | |
| **Backup** | Automated backups | ☐ Yes ☐ Partial ☐ No | | | |
| | Offsite storage | ☐ Yes ☐ Partial ☐ No | | | |
| | Restoration testing | ☐ Yes ☐ Partial ☐ No | | | |
| **Encryption** | Data at rest | ☐ Yes ☐ Partial ☐ No | | | |
| | Data in transit | ☐ Yes ☐ Partial ☐ No | | | |
| **Physical Security** | Access control | ☐ Yes ☐ Partial ☐ No | | | |
| | Surveillance | ☐ Yes ☐ Partial ☐ No | | | |
| | Environmental monitoring | ☐ Yes ☐ Partial ☐ No | | | |

### 7.2 Security Incidents and Near-Misses

**Historical Incident Information**:

| Date | Incident Type | Affected Systems | Impact | Root Cause | Resolution | Lessons Learned |
|------|---------------|------------------|--------|------------|------------|-----------------|
| | | | | | | |

**Near-Miss Events** (things that could have been serious):

| Date | Event | Potential Impact | Why Avoided | Remediation |
|------|-------|------------------|-------------|-------------|
| | | | | |

### 7.3 Vulnerability Assessment

**Known Vulnerabilities**:

| CVE / Vulnerability | Affected Assets | CVSS Score | Exploitability | Current Mitigation | Remediation Plan |
|---------------------|-----------------|------------|----------------|-------------------|------------------|
| | | | | | |

**Common Weaknesses**:
- [ ] Default passwords in use
- [ ] Unpatched systems (list how many)
- [ ] No network segmentation
- [ ] No monitoring/logging
- [ ] Shared accounts
- [ ] No access control
- [ ] Unnecessary services enabled
- [ ] Cleartext protocols in use
- [ ] No backup procedures
- [ ] No incident response plan

### 7.4 Previous Assessments

**Previous Security Assessments to Collect**:

| Assessment Type | Date | Performed By | Key Findings | Actions Taken |
|-----------------|------|--------------|--------------|---------------|
| Vulnerability Scan | | | | |
| Penetration Test | | | | |
| Security Audit | | | | |
| Compliance Audit | | | | |
| Risk Assessment | | | | |
| Architecture Review | | | | |

---

## 8. Regulatory and Compliance Requirements {#regulatory}

### 8.1 Applicable Regulations

**Identify ALL Applicable Regulations**:

| Sector | Common Regulations |
|--------|-------------------|
| **Electric Utilities** | NERC CIP, FERC, DOE orders |
| **Water/Wastewater** | America's Water Infrastructure Act (AWIA), state regulations |
| **Oil & Gas** | TSA Pipeline Security Directives, API standards |
| **Chemical** | CFATS (Chemical Facility Anti-Terrorism Standards) |
| **Manufacturing** | Industry-specific (FDA for pharma, etc.) |
| **All Sectors** | NIST CSF, ISO 27001, SOC 2, state breach notification laws |
| **EU Operations** | NIS2 Directive, GDPR, Cyber Resilience Act (CRA) |
| **Export Controlled** | ITAR, EAR compliance |

**Regulatory Requirements Template**:

```yaml
Regulation:
  regulation_name: ""
  authority: ""
  applicability: ""      # Why does this apply to us?
  
  # Requirements
  key_requirements: []
  reporting_requirements: []
  audit_frequency: ""
  penalties_for_noncompliance: ""
  
  # Current Status
  current_compliance_status: ""  # Compliant, Partial, Non-Compliant
  gaps: []
  remediation_timeline: ""
  
  # Resources
  internal_sme: ""       # Subject matter expert
  external_counsel: ""   # Legal or compliance consultant
  certification_required: ""  # Yes/No
```

### 8.2 Customer and Contractual Requirements

**Customer Security Requirements**:

| Customer | Requirement | Verification Method | Deadline | Status |
|----------|-------------|---------------------|----------|--------|
| | | | | |

**Contractual Obligations**:
- [ ] Service Level Agreements (SLAs) for availability
- [ ] Security requirements in vendor contracts
- [ ] Insurance policy requirements
- [ ] Partner interconnection agreements

---

## 9. Personnel and Training Information {#personnel}

### 9.1 Personnel Inventory

**Current Personnel with Security Roles**:

| Name | Role | Department | IEC 62443 Training | Security Clearance | Years Experience |
|------|------|------------|-------------------|-------------------|------------------|
| | | | ☐ Yes ☐ No | ☐ Yes ☐ No | |

### 9.2 Training Needs Assessment

**Required Training**:

| Training Topic | Target Audience | Current Competency | Training Gap | Priority |
|----------------|-----------------|-------------------|--------------|----------|
| IEC 62443 Overview | Management | Low | High | High |
| IEC 62443-2-1 CSMS | Security team | None | Critical | High |
| IEC 62443-3-2 Risk Assessment | Risk team | None | Critical | High |
| Zone & Conduit Design | Network/Security | Low | High | High |
| Secure Operations | Operators | Low | Medium | Medium |
| Incident Response | IT/OT/Security | Medium | Low | Medium |

### 9.3 Vendor and Contractor Personnel

**Third-Party Personnel with Access**:

| Company | Personnel | Access Type | Access Schedule | Security Training | Background Check |
|---------|-----------|-------------|-----------------|-------------------|------------------|
| | | | | ☐ Yes ☐ No | ☐ Yes ☐ No |

---

## 10. Documentation and Records {#documentation}

### 10.1 Existing Technical Documentation

**System Documentation to Collect**:

| Document Type | System | Last Updated | Location | Format |
|---------------|--------|--------------|----------|--------|
| System Architecture | | | | |
| Network Diagrams | | | | |
| P&IDs | | | | |
| Logic Diagrams | | | | |
| I/O Lists | | | | |
| Configuration Backups | | | | |
| As-Built Drawings | | | | |
| Vendor Manuals | | | | |
| Maintenance Records | | | | |
| Change Logs | | | | |

### 10.2 Operational Records

**Records to Review/Collect**:

- **Maintenance Logs**: What maintenance activities occur and when
- **Alarm Logs**: System alarms and operator responses
- **Change Records**: All changes made to systems (last 2 years)
- **Incident Reports**: All operational incidents
- **Access Logs**: Who accesses systems and when
- **Training Records**: Who has been trained on what
- **Audit Logs**: System audit trails (if available)

---

## 11. Information Sources and Collection Methods {#sources}

### 11.1 Information Sources

**Where to Find Required Information**:

| Information Category | Primary Sources | Secondary Sources |
|----------------------|-----------------|-------------------|
| **Asset Inventory** | CMDB, EAM system, network scans | Site walkdowns, procurement records |
| **Network Architecture** | Network management tools, diagrams | Firewall configs, switch configs |
| **Business Processes** | Process engineers, operations managers | Process documentation, P&IDs |
| **Policies** | SharePoint, document management system | Department file shares |
| **Incidents** | Incident tracking system, SIEM | Email archives, meeting notes |
| **Vulnerabilities** | Vulnerability scanners, vendor bulletins | Security assessments |
| **Regulations** | Legal/compliance department | Industry associations, consultants |
| **Personnel** | HR system, org charts | Direct manager, team leads |

### 11.2 Data Collection Methods

**Recommended Approach** (phased):

**Phase 1: Quick Assessment (Week 1-2)**
- Collect readily available information
- Interview key personnel
- Review existing documentation
- Preliminary network scans (passive)

**Phase 2: Detailed Collection (Week 3-6)**
- Comprehensive asset discovery
- Detailed interviews and workshops
- Site surveys and walkdowns
- Document analysis

**Phase 3: Validation and Gap Filling (Week 7-8)**
- Verify collected information
- Fill identified gaps
- Reconcile conflicting information
- Document assumptions

**Phase 4: Documentation and Organization (Week 9-12)**
- Organize collected information
- Create initial documentation
- Establish data management processes
- Set up ongoing update procedures

### 11.3 Interview and Workshop Approach

**Key Interviews to Conduct**:

1. **Executive Interview** (1-2 hours)
   - Business drivers and objectives
   - Budget and timeline
   - Risk tolerance
   - Regulatory requirements

2. **IT Manager Interview** (2-3 hours)
   - IT systems and architecture
   - Security controls
   - Policies and procedures
   - Change management

3. **OT Manager Interview** (2-3 hours)
   - Control systems architecture
   - Operational constraints
   - Business processes
   - Maintenance practices

4. **Operations/Engineering Workshop** (half day)
   - Walk through processes
   - Identify critical systems
   - Discuss failure scenarios
   - Review network architecture

5. **Security Team Interview** (2-3 hours)
   - Current security posture
   - Known vulnerabilities
   - Incident history
   - Monitoring capabilities

---

## 12. Data Collection Checklist {#checklist}

### 12.1 Master Checklist

Use this checklist to track information collection progress:

#### Organizational Information
- [ ] Executive sponsor identified and committed
- [ ] Project charter approved
- [ ] Budget authorized
- [ ] Team formed with roles assigned
- [ ] Organizational chart collected
- [ ] RACI matrix created
- [ ] Scope defined (SuC documented)
- [ ] Existing policies collected

#### Asset Inventory
- [ ] Asset discovery tools deployed
- [ ] Network scans completed
- [ ] Site walkdowns completed
- [ ] Asset list compiled (minimum: name, location, IP, function)
- [ ] Asset criticality assessed
- [ ] Legacy systems identified
- [ ] Safety systems documented
- [ ] Vendor-managed systems identified

#### Network and Architecture
- [ ] High-level network diagram obtained
- [ ] Detailed network diagrams collected
- [ ] Data flow diagrams created
- [ ] Network device inventory compiled
- [ ] Protocol inventory completed
- [ ] External connections documented
- [ ] Firewall rulesets collected
- [ ] VLAN configurations documented

#### Business and Operations
- [ ] Critical business processes identified
- [ ] Business impact analysis completed
- [ ] Operational constraints documented
- [ ] Availability requirements defined
- [ ] Maintenance windows identified
- [ ] Financial information collected
- [ ] Budget allocated

#### Security Current State
- [ ] Existing security controls inventoried
- [ ] Security incidents reviewed
- [ ] Known vulnerabilities documented
- [ ] Previous assessments collected
- [ ] Gap analysis completed (preliminary)

#### Regulatory and Compliance
- [ ] Applicable regulations identified
- [ ] Regulatory requirements documented
- [ ] Customer requirements collected
- [ ] Contractual obligations reviewed
- [ ] Compliance gaps identified

#### Personnel and Training
- [ ] Key personnel identified
- [ ] Current training assessed
- [ ] Training needs identified
- [ ] Vendor/contractor personnel documented
- [ ] Access requirements defined

#### Documentation
- [ ] Technical documentation collected
- [ ] Operational records reviewed
- [ ] Change history documented
- [ ] Maintenance records collected
- [ ] Training records obtained

### 12.2 Readiness Assessment

**Are You Ready to Start?**

**Minimum to Begin IEC 62443 Implementation**:
- ✅ Executive sponsorship secured (with budget)
- ✅ Scope defined (at least high-level)
- ✅ Team formed (at least core team)
- ✅ Preliminary asset list available
- ✅ High-level network diagram available
- ✅ Critical business processes identified
- ✅ Regulatory requirements understood

**Indicators You're Ready for Detailed Work**:
- ✅ >80% of assets inventoried
- ✅ Detailed network information available
- ✅ Business impact analysis completed
- ✅ Current security posture understood
- ✅ Constraints and limitations identified

**Red Flags That Will Slow You Down**:
- ❌ No executive support or unclear sponsorship
- ❌ No budget allocated
- ❌ No idea what assets exist
- ❌ No network documentation
- ❌ Can't identify critical systems
- ❌ No personnel available for project

---

## Conclusion

Implementing IEC 62443 requires comprehensive information gathering across multiple domains. Use this document as a guide to systematically collect the information needed to:

1. **Establish a CSMS** (IEC 62443-2-1)
2. **Perform Risk Assessment** (IEC 62443-3-2)
3. **Define Zones and Conduits** (IEC 62443-3-2)
4. **Implement Security Controls** (IEC 62443-3-3)
5. **Ensure Secure Development** (IEC 62443-4-1)
6. **Certify Components** (IEC 62443-4-2)

**Next Steps After Information Collection**:

1. Organize collected information into structured formats
2. Identify and document gaps
3. Perform initial risk assessment (IEC 62443-3-2 ZCR 2)
4. Begin zone and conduit partitioning (IEC 62443-3-2 ZCR 3)
5. Develop CSMS framework (IEC 62443-2-1)
6. Create documentation artifacts (see IEC 62443 Documentation Guide)

**Remember**: Information collection is iterative. You'll continue to refine and update information throughout the IEC 62443 implementation journey.

---

**Document Version**: 1.0  
**Last Updated**: October 2025  
**For Questions**: Contact your IEC 62443 consultant or ISAGCA (gca.isa.org)

