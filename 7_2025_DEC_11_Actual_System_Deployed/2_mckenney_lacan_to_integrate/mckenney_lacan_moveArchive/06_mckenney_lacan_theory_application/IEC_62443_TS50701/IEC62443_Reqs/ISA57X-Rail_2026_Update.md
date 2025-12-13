## Comprehensive Research Report: IEC 63452 Railway Cybersecurity Standard \& Auckland CRL Project Implementation

### Executive Summary

The railway cybersecurity landscape is undergoing a significant transformation with the development of **IEC 63452**, the first international standard specifically designed for railway applications. This standard, currently in Committee Draft for Vote (CDV) stage as of August 2025 with expected publication by mid-2026, represents a major advancement over the existing CENELEC TS 50701. For the **Auckland City Rail Link (CRL) project**—New Zealand's largest transport infrastructure project valued at \$5.493 billion—implementing robust cybersecurity measures following IEC 62443 and the emerging IEC 63452 framework is critical for protecting this transformational underground rail system.[^1_1][^1_2][^1_3][^1_4][^1_5][^1_6][^1_7]

### IEC 63452: The New Railway Cybersecurity Standard

#### Background and Development

IEC 63452 is being developed under **IEC TC9 / PT 63452** with contributions from over 20 countries and strong collaboration with stakeholders including UITP, ERA (European Union Agency for Railways), and ENISA. The standard builds upon and adapts **IEC 62443** (industrial automation cybersecurity) specifically for the railway domain's unique operational environment, addressing the distributed nature of railway systems and complex ownership models.[^1_1][^1_5][^1_6][^1_7][^1_8][^1_9]

**Key Timeline:**

- **Current Status (2025):** Committee Draft for Vote (CDV) stage[^1_10][^1_11]
- **Expected FDIS:** February 2026
- **Publication:** Mid-2026[^1_6][^1_11]
- **Will Replace:** CENELEC TS 50701 across Europe[^1_9][^1_6]

#### Core Principles and Structure

IEC 63452 introduces several critical advancements over previous standards:[^1_5][^1_1][^1_6][^1_9]

**1. Lifecycle Integration**
The standard interfaces cybersecurity with the generic Reliability, Availability, Maintainability, and Safety (RAMS) lifecycle of IEC 62278 series standards, ensuring cybersecurity is embedded throughout the entire railway application lifecycle.[^1_7][^1_10][^1_9]

**2. Continuous Monitoring and Evaluation**
Unlike static security approaches, IEC 63452 emphasizes continuous cybersecurity evaluation and **handover planning throughout the lifecycle**, not just at commissioning.[^1_6][^1_9]

**3. Railway-Specific Risk Management**
The standard provides detailed methodologies for risk assessment that go beyond IEC 62443's generic industrial approach, incorporating:

- Threat identification specific to railway operations
- Security requirements aligned with operational constraints
- Acceptance criteria tailored to railway safety requirements[^1_9][^1_6]

**4. Clear Role-Based System Modeling**
IEC 63452 guides operators in modeling systems across:

- **Physical layers:** Onboard, trackside, central control
- **Functional subsystems:** Signaling, communications, traction power, passenger systems
- **Security zones:** With clearly defined boundaries and conduits[^1_6]


### Critical Artifacts and Deliverables (IEC 63452)

Based on the draft standard, the following key artifacts are essential for railway cybersecurity projects:[^1_10]

#### Planning and Management Phase

**1. Cybersecurity Management Plan (CMP)**

- **Reference:** LC-02-01, LC-02-02, LC-02-03[^1_10]
- **Purpose:** Defines cybersecurity activities from project initiation through handover
- **Content:** Project scope, roles/responsibilities, milestones, interfaces with safety/RAM teams, resource allocation
- **Owner:** Project Cybersecurity Manager
- **Tailoring:** Must be adapted to project-specific context and approved by stakeholders

**2. Project Cybersecurity Manager Assignment**

- **Reference:** LC-01-01[^1_10]
- **Requirement:** Dedicated role with defined competencies and authority
- **Responsibilities:** Overall cybersecurity delivery, stakeholder coordination, issue escalation

**3. Threat Log**

- **Reference:** Various requirements throughout standard
- **Purpose:** Living document tracking identified threats, vulnerabilities, and risk treatment measures
- **Updates:** Continuous throughout project lifecycle
- **Handover:** Current state transferred to operations team


#### Risk Assessment Phase

**4. Initial Risk Assessment (IRA)**

- **Reference:** ZR-02-01[^1_10]
- **Purpose:** High-level identification of broad threats and potential impacts
- **Output:** Preliminary risk landscape for the System under Consideration (SuC)

**5. Zones and Conduits Model**

- **Reference:** ZR-03-01[^1_12][^1_10]
- **Purpose:** Logical partitioning of the railway system into security zones with common requirements
- **Critical Components:**
    - **Zones:** Groupings of assets (e.g., Control Centre Zone, Signaling Zone, Station Systems Zone, Traction Power Zone)[^1_13][^1_14]
    - **Conduits:** Communication pathways between zones with defined security controls[^1_14][^1_15]
    - **Security Level Target (SL-T):** Defined for each zone (SL-1 to SL-4 based on risk)[^1_16][^1_13]

**6. Detailed Risk Assessment (DRA)**

- **Reference:** ZR-05-01 through ZR-05-11[^1_10]
- **Activities:**
    - Threat identification (ZR-05-02)
    - Vulnerability identification (ZR-05-03)
    - Threat/vulnerability management (ZR-05-04)
    - Code of practice application (ZR-05-05)
    - Explicit risk evaluation when needed (ZR-05-07 to ZR-05-09)
    - Threat coverage and risk acceptance (ZR-05-10)
    - Documentation (ZR-05-11)

**7. Cybersecurity Requirements Specification (CRS)**

- **Reference:** ZR-06-01[^1_12][^1_10]
- **Purpose:** Documented security requirements derived from risk assessment
- **Content:** Functional and technical security requirements, security levels, compensating measures
- **Traceability:** Must trace back to identified threats and risks


#### Design and Architecture Phase

**8. Cybersecurity Architecture Document**

- **Reference:** AA-01-01, AA-01-02[^1_10]
- **Content:** Functional architecture showing how security requirements are met
- **Validation:** Must demonstrate security does not adversely impact essential functions

**9. Security Level Achievement Documentation**

- **Reference:** ZR-04-01[^1_10]
- **Purpose:** Evidence of achieved security level (SL-A) versus target (SL-T)
- **Requirement:** Gap analysis and mitigation for any shortfalls

**10. Compensating Countermeasures Documentation**

- **Reference:** AA-01-04[^1_10]
- **Purpose:** Documents alternative security measures when standard controls cannot be fully implemented
- **Justification:** Risk-based rationale for compensating measures


#### Assurance and Validation Phase

**11. Cybersecurity Evaluation Plan**

- **Reference:** CA-01-01[^1_10]
- **Content:** Test strategy, test cases, success criteria, independence requirements
- **Coverage:** Verification and validation activities for all security requirements

**12. Verification and Validation Reports**

- **Reference:** CA-01-03 to CA-01-05[^1_10]
- **Components:**
    - Deliverables verification (CA-01-04)
    - Railway solution validation (CA-01-05)
    - Test execution records
    - Non-conformance reports and resolutions

**13. Cybersecurity Case**

- **Reference:** CA-01-06[^1_10]
- **Purpose:** **THE MOST CRITICAL HANDOVER DOCUMENT** - Demonstrates that cybersecurity risks are managed to acceptable levels
- **Content Structure:**
    - System description and boundaries
    - Security context and assumptions
    - Risk assessment summary
    - Security requirements and their implementation
    - Verification/validation evidence
    - Residual risks and acceptance
    - Operational security requirements
- **Approval:** Must be approved by asset owner before handover (CA-02-03)[^1_10]


#### Handover Phase - The Critical Transition

**14. Cybersecurity Handover Plan**

- **Reference:** CA-02-01[^1_10]
- **Purpose:** **ESSENTIAL HANDOVER ARTIFACT** - Defines the complete handover process
- **Content:**
    - Handover scope and boundaries
    - Documentation package list
    - Training and competency requirements
    - Acceptance criteria
    - Roles and responsibilities during transition
    - Schedule and milestones
- **Approval:** CA-02-02 - Must be approved before execution[^1_10]

**15. Handover Documentation Package**

- **Reference:** CA-02-04[^1_10]
- **Complete Set Includes:**
    - All documents listed above (1-13)
    - As-built security architecture
    - Configuration baselines
    - Incident response procedures
    - Vulnerability and patch management procedures
    - Monitoring and logging configurations
    - Access control lists and authentication mechanisms
    - Training materials and competency records

**16. Asset Owner's Approval**

- **Reference:** ZR-07-01, CA-02-05[^1_10]
- **Critical Gateway:** Final approval required from operations team (Auckland Transport and KiwiRail for CRL)
- **Validates:** System readiness for operational acceptance

![Cybersecurity Implementation Timeline for Railway Infrastructure Projects (IEC 63452 Lifecycle)](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/b9edcb3387838054890b038d1737994c/98aad263-d7fc-4ee5-a836-540e7b087948/1c349487.png)

Cybersecurity Implementation Timeline for Railway Infrastructure Projects (IEC 63452 Lifecycle)

### Auckland CRL Project: Cybersecurity Context and Challenges

#### Project Overview

The Auckland City Rail Link represents New Zealand's most ambitious infrastructure project:[^1_2][^1_3][^1_4]

**Technical Specifications:**

- **Length:** 3.45km twin-tunnel underground rail link
- **Depth:** Up to 42 meters below Auckland city center
- **Stations:** Two new underground stations (Te Waihorotiu/Aotea, Karanga-a-Hape) plus redeveloped Maungawhau and converted Waitematā
- **Budget:** \$5.493 billion (NZD)
- **Completion:** Late 2025 (construction), Opening 2026
- **Operators:** Auckland Transport and KiwiRail[^1_3][^1_4][^1_2]

**Delivery Model:**

- **Link Alliance:** Consortium of seven companies including City Rail Link Limited
- **Key Partner:** Downer Group (infrastructure, stations, rail systems integration)[^1_17][^1_18][^1_19][^1_20]
- **Testing:** 31 test plans covering all systems[^1_21][^1_2]


#### Integrated Systems Requiring Cybersecurity Protection

The CRL incorporates highly integrated control and communication systems from **Honeywell**:[^1_22]

**1. Integrated Control System (ICS)**

- Enterprise Buildings Integrator (EBI)
- Building Management System (BMS)
- Over 20,000 sensor points across stations and tunnels
- Unified view of all subsystems[^1_22]

**2. Critical OT Systems:**

- **Signaling and Train Control:** Successfully integrated mid-2025[^1_23]
- **Traction Power Systems:** Control and monitoring
- **Ventilation Systems:** Tunnel and station environmental control
- **Fire Detection and Suppression**
- **Station Control Systems:** Lifts, escalators (including NZ's longest), lighting[^1_21][^1_23]

**3. Communication Systems:**

- **Radio and DAS (Distributed Antenna System):** Emergency services and rail operators
- **Wi-Fi Infrastructure:** Public and operational
- **CCTV and Video Management:** Security monitoring
- **Passenger Information Displays (PIDs)**
- **Help Points**[^1_22]

**4. ICT Infrastructure:**

- Network and Wi-Fi infrastructure for Extra Low Voltage (ELV) systems
- **Cybersecurity auditing and monitoring** (provided by Honeywell)[^1_22]


#### Cybersecurity Imperatives for CRL

**Testing and Integration Challenges**:[^1_21]

- Integration of new CRL systems with existing Auckland rail network
- Testing underground operations (New Zealand's first underground railway)
- Emergency scenario testing below ground
- Steep gradients (70-meter drop from Maungawhau to Waitematā)
- 42 meters depth at deepest point

**Key Risks Identified**:[^1_21]

1. Individual subsystems not meeting performance requirements
2. Lack of integration with wider rail network
3. Unknown operational challenges in underground environment

### Recommended Zone and Conduit Architecture for Auckland CRL

Based on IEC 62443 and railway best practices, the following security architecture is recommended:[^1_13][^1_14][^1_24]

![Auckland CRL Cybersecurity Zone and Conduit Architecture Model (IEC 62443/63452)](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/b9edcb3387838054890b038d1737994c/693e67c9-d1b7-4850-8c2b-06d9d3b36bbc/ce9229d0.png)

Auckland CRL Cybersecurity Zone and Conduit Architecture Model (IEC 62443/63452)

**Zone Definitions:**

**1. Safety-Critical Security Zone (SCSZ) - Security Level 4**

- **Systems:** Train control (CBTC), signaling \& interlocking, automatic train protection (ATP), emergency braking
- **Protection:** Highest security controls, isolated from less critical zones
- **Access:** Strictly controlled, multi-factor authentication, physical and logical separation

**2. Operationally Critical Security Zone (OCSZ) - Security Level 3**

- **Systems:** SCADA (supervisory control), traction power control, tunnel ventilation, station control, fire systems
- **Separation:** Electronic security perimeters from SCSZ and lower zones[^1_24]
- **Controls:** Hardware-based firewalls, intrusion detection, access control

**3. Station and Passenger Systems Zone - Security Level 2**

- **Systems:** CCTV, passenger information displays, help points, ticketing/fare systems, access gates
- **Protection:** Standard network security controls
- **Monitoring:** Continuous surveillance for anomalies

**4. Communications Zone - Security Level 2**

- **Systems:** Radio/DAS, Wi-Fi (public and operational), cellular, network management
- **Isolation:** Separate VLANs and network segments
- **Monitoring:** Traffic analysis and anomaly detection

**5. Enterprise Zone - Security Level 1-2**

- **Systems:** Business IT, asset management, maintenance planning, scheduling, administrative systems
- **Separation:** DMZ between enterprise and OCSZ[^1_24]
- **Access:** Standard IT security controls

**6. External Zone**

- **Connections:** Vendor remote access, internet gateway, third-party services
- **Protection:** VPN, strong authentication, connection through DMZ only
- **Monitoring:** All external connections logged and monitored

**Conduits (Communication Pathways):**

- **SCSZ to OCSZ:** Data diodes (one-way where appropriate), dedicated firewalls, protocol filtering
- **OCSZ to Enterprise:** DMZ architecture, no direct connections[^1_24]
- **Enterprise to External:** Firewall, VPN, intrusion detection/prevention
- **All Conduits:** Encrypted communications, logging, monitoring, access control


### Handover Process for Auckland CRL

![IEC 63452 Cybersecurity Handover Process Flow for Railway Infrastructure](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/b9edcb3387838054890b038d1737994c/d52e95f5-8dc4-4c3b-8e38-51e1af632e72/7bfe255d.png)

IEC 63452 Cybersecurity Handover Process Flow for Railway Infrastructure

**Phase 1: Handover Preparation (Months 21-22)**

**Key Activities:**

1. **Establish Cybersecurity Handover Plan (CA-02-01)**
    - Define handover scope covering all four CRL stations plus tunnel systems
    - Identify all documentation requirements
    - Establish acceptance criteria with Auckland Transport and KiwiRail
    - Define training requirements for operations teams
2. **Compile Handover Documentation Package**
    - Gather all deliverables from construction phase
    - Ensure as-built documentation reflects actual implementation
    - Compile configuration baselines for all security controls
    - Prepare network diagrams showing zones and conduits
3. **Complete Cybersecurity Case (CA-01-06)**
    - Consolidate all risk assessment evidence
    - Document security level achievements (SL-A vs SL-T)
    - Compile verification and validation results
    - Obtain necessary approvals from Link Alliance leadership

**Phase 2: Review and Approval (Months 22-23)**

**Key Activities:**

1. **Approval of Cybersecurity Handover Plan (CA-02-02)**
    - Review by all stakeholders: CRL Ltd, Auckland Transport, KiwiRail
    - Verification that all requirements are addressed
    - Confirmation of readiness criteria
2. **Approval of Cybersecurity Case (CA-02-03)**
    - Independent review by cybersecurity assessors
    - Validation of risk management approach
    - Confirmation of residual risk acceptability
3. **Asset Owner Review and Approval (CA-02-05)**
    - Auckland Transport and KiwiRail formal review
    - Assessment of operational readiness
    - Validation of training completion
    - Sign-off on risk acceptance

**Phase 3: Handover Execution (Month 24)**

**Key Activities:**

1. **Transfer Documentation**
    - Physical and electronic transfer of all handover documents
    - Access credentials for documentation repositories
    - Configuration management database (CMDB) access
2. **Transfer Accountability**
    - Formal transfer ceremony and documentation
    - Insurance and warranty transfers
    - Maintenance responsibilities handover
3. **Transfer Training and Knowledge**
    - Final training sessions for operations staff
    - Competency assessments and certifications
    - Knowledge transfer workshops
4. **Perform Cybersecurity Handover (CA-02-04)**
    - Execute formal handover process
    - Activate operational monitoring (24/7 SOC)
    - Initiate incident response procedures
    - Begin operational phase

**Phase 4: Post-Handover (Month 24+)**

**Key Activities:**

1. **Operations Team Acceptance**
    - Validation of system performance
    - Confirmation of monitoring effectiveness
    - Verification of incident response capability
2. **Deficiency Management**
    - Track and resolve any outstanding items
    - Implement agreed remediation plans
    - Close out warranty items
3. **Warranty Period Management**
    - Monitor system performance
    - Address any security-related issues
    - Document lessons learned

### Complete Handover Checklist for Auckland CRL

The comprehensive handover checklist includes **35 critical items** across seven categories:

**Documentation (7 items):**

- Cybersecurity Management Plan
- Cybersecurity Case (approved)
- Cybersecurity Requirements Specification
- Risk Assessment Reports
- Zone \& Conduit Architecture Diagrams
- As-Built Security Architecture
- Current Threat Log

**Risk \& Compliance (5 items):**

- Security Level Achievement Evidence
- Vulnerability Assessment Reports
- Compliance Matrix (IEC 62443/63452)
- Penetration Testing Results
- Residual Risk Acceptance Documents

**Technical Architecture (5 items):**

- Network Segmentation Evidence
- Security Zone Definitions
- Access Control Lists \& Authentication
- Firewall Rules \& IDS/IPS Configuration
- Encryption Implementation Evidence

**Integration \& Testing (4 items):**

- Systems Integration Test Results
- Cybersecurity Validation Results
- Emergency Scenario Testing Results
- Interface Testing with Existing Network

**Operations Readiness (5 items):**

- Incident Response Plan \& Playbooks
- Vulnerability \& Patch Management Procedures
- SOC Procedures
- Staff Training Records
- 24/7 Monitoring Arrangements

**Security Controls (5 items):**

- Identity \& Access Management Documentation
- Multi-Factor Authentication Implementation
- Logging \& Audit Trail Configuration
- Backup \& Recovery Procedures
- Business Continuity Plan (cyber incidents)

**Governance (4 items):**

- Roles \& Responsibilities (RACI Matrix)
- Security Policies \& Procedures
- Supplier/Vendor Security Agreements
- Change Management Procedures


### Roles and Responsibilities Matrix

**Key Cybersecurity Roles (IEC 63452 Annex H):**

1. **Project Cybersecurity Manager** - Overall delivery, management plan, cybersecurity case, handover coordination
2. **Railway Cybersecurity Architect** - Security architecture, zone/conduit model, requirements specification
3. **Railway Cybersecurity Risk Analyst** - Risk assessments, threat log, vulnerability analysis
4. **Railway Cybersecurity Implementer** - Security controls implementation, configuration
5. **Railway Cybersecurity Penetration Tester** - Security testing, vulnerability assessment
6. **Railway Cybersecurity Assessor** - Evaluation planning, verification, compliance assessment
7. **Railway Cybersecurity Incident Responder** - Incident response plan, playbooks, forensics
8. **Railway Cybersecurity Administrator** - Configuration management, patch management, monitoring

**Project-Specific Roles:**

- **Asset Owner Representatives** (Auckland Transport \& KiwiRail) - Requirements validation, risk acceptance, handover approval
- **Link Alliance Integration Lead** - Systems integration, interface testing
- **Downer Group Systems Engineer** - Infrastructure implementation, technical handover
- **Operations Manager (CRL)** - Operational procedures, training, business continuity
- **SOC Lead** - 24/7 monitoring, threat detection, incident response


### Key Process Enhancements and Best Practices

#### 1. Vulnerability and Patch Management

**Challenge in Railway Environment**:[^1_25][^1_26]

- Short maintenance windows
- Long certification cycles (re-testing required after changes)
- Legacy systems with limited patch support
- Safety-critical systems cannot be easily updated

**Recommended Approach**:[^1_26][^1_25]

- **Risk-based prioritization:** Focus on vulnerabilities with highest operational impact
- **Virtual patching:** Use network-level controls when direct patching isn't feasible
- **Vendor coordination:** Establish clear patch notification and testing protocols
- **Change windows:** Plan updates during scheduled maintenance periods
- **Testing protocols:** Comprehensive testing before production deployment
- **Rollback procedures:** Quick recovery if patches cause issues


#### 2. Threat Intelligence Sharing

**Industry Collaboration**:[^1_27][^1_28]

- Participate in railway-specific information sharing forums (e.g., ER-ISAC in Europe)
- Subscribe to rail-specific threat intelligence feeds
- Engage with government agencies (CERT NZ, NCSC)
- Share anonymized incident data with industry peers
- Collaborate with vendors on vulnerability disclosures

**Rail-Specific Threats to Monitor**:[^1_27]

- Signaling system attacks
- SCADA/traction power compromise
- Wireless protocol vulnerabilities (e.g., CVE-2025-1727 EoT/HoT vulnerability)[^1_29][^1_30]
- Ransomware targeting rail operations
- Supply chain attacks on rail-specific equipment


#### 3. Secure by Design Implementation

**Principles**:[^1_31][^1_32]

- **Security from inception:** Embed security requirements from initial design
- **Defense in depth:** Multiple layers of security controls
- **Least privilege:** Minimal access rights by default
- **Secure defaults:** Systems ship with secure configurations
- **Fail secure:** Systems fail to safe state, not open state
- **Separation of duties:** No single person has complete control

**For CRL Application:**

- All new systems procured with IEC 62443 compliance requirements
- Security requirements in vendor contracts
- Mandatory security testing before system acceptance
- Configuration hardening standards applied to all devices
- Regular security architecture reviews


#### 4. Training and Awareness Programs

**Target Audiences**:[^1_33][^1_34][^1_35][^1_36]

**Board and Executive Level (1 hour - half day):**

- Understanding railway cybersecurity landscape
- Regulatory compliance requirements (NIS2, TSA directives)
- Business impact of cyber incidents
- Risk governance and oversight responsibilities

**Technical Staff (8+ hours):**

- Railway cybersecurity fundamentals
- OT vs IT security differences
- Network security for railway systems
- Securing communications and signaling systems
- Data protection and privacy
- Incident response procedures

**Operations Staff (2-4 hours):**

- Recognizing suspicious activity
- Reporting procedures
- Social engineering awareness
- Physical security integration
- Emergency response protocols

**Ongoing Programs:**

- Quarterly security awareness campaigns
- Simulated phishing exercises
- Tabletop exercises for incident response
- Annual competency assessments


#### 5. Incident Response Planning

**Components of Effective Rail IR Plan**:[^1_37][^1_38]

**1. Preparation:**

- Define incident categories (severity levels)
- Establish Security Operations Center (SOC/CSOC)
- Create response playbooks for common scenarios
- Define escalation paths
- Establish communication protocols

**2. Detection and Analysis:**

- 24/7 monitoring of all security zones
- Automated anomaly detection
- Log aggregation and correlation
- Threat intelligence integration

**3. Containment:**

- Network isolation procedures (by zone)
- Emergency shutdown protocols
- Evidence preservation
- Stakeholder notification

**4. Eradication and Recovery:**

- Root cause analysis
- Malware removal procedures
- System restoration from clean backups
- Validation before returning to service

**5. Post-Incident:**

- Lessons learned documentation
- Playbook updates
- Training adjustments
- Regulatory notifications (if required)

**Rail-Specific Considerations:**

- **Safety first:** Never compromise operational safety for security
- **Operational impact:** Consider service disruption in response decisions
- **Regulatory reporting:** Comply with transport safety reporting requirements
- **Public communication:** Coordinate with PR team for passenger information


### Implementation Recommendations for Auckland CRL

#### Near-Term Actions (Pre-Handover)

**1. Finalize Cybersecurity Case**

- Complete all verification and validation activities
- Document all residual risks with owner acceptance
- Obtain all necessary approvals
- Prepare executive summary for Auckland Transport/KiwiRail boards

**2. Complete Handover Documentation**

- Verify all 35 checklist items are complete
- Conduct internal review of documentation quality
- Ensure as-built documentation reflects actual deployment
- Organize documentation for easy operator access

**3. Operations Team Training**

- Deliver all planned training modules
- Conduct competency assessments
- Provide hands-on exercises in operational environment
- Document training completion for each role

**4. Security Operations Center (SOC) Establishment**

- Deploy 24/7 monitoring infrastructure
- Integrate all security zones into monitoring platform
- Configure alerting and escalation procedures
- Conduct dry-run exercises

**5. Incident Response Testing**

- Tabletop exercises with all stakeholders
- Simulate cyber incident scenarios
- Test communication protocols
- Validate escalation procedures
- Refine playbooks based on learnings


#### Medium-Term Actions (Post-Handover, Year 1)

**1. Continuous Monitoring and Improvement**

- Establish monthly security review meetings
- Analyze security events and trends
- Tune monitoring rules to reduce false positives
- Update threat intelligence feeds

**2. Vulnerability Management Program**

- Establish regular vulnerability scanning schedule
- Define patch testing and deployment windows
- Track vendor security advisories
- Maintain asset inventory with version control

**3. Compliance Monitoring**

- Track compliance with IEC 62443/63452 requirements
- Conduct internal security audits
- Address any non-conformances
- Prepare for external assessments

**4. Training Refreshers**

- Quarterly security awareness updates
- Annual technical training for SOC staff
- Emergency response drills
- Update training materials based on evolving threats


#### Long-Term Strategic Initiatives

**1. Alignment with IEC 63452**

- Monitor standard publication (expected mid-2026)
- Conduct gap analysis against final standard
- Plan remediation for any gaps
- Consider certification when available

**2. Integration with Future Auckland Rail Projects**

- Establish common security architecture patterns
- Share lessons learned from CRL implementation
- Develop standardized handover processes
- Build organizational cybersecurity maturity

**3. Industry Collaboration**

- Participate in Australasian railway cybersecurity forums
- Share anonymized threat intelligence
- Collaborate on common challenges (e.g., legacy system security)
- Contribute to standards development

**4. Technology Evolution**

- Stay current with railway-specific security technologies
- Evaluate AI/ML for anomaly detection
- Consider quantum-safe cryptography for long-term
- Plan for 5G and future communication protocols


### Innovative Ideas and Emerging Practices

#### 1. Digital Twin for Security Testing

**Concept:** Create a digital replica of CRL's operational technology environment for security testing without impacting live operations.

**Benefits:**

- Test security controls in realistic environment
- Simulate attack scenarios safely
- Validate incident response procedures
- Train SOC staff on realistic scenarios
- Test patches before production deployment

**Implementation:** Leverage existing BIM (Building Information Modeling) data from CRL construction extended with cybersecurity attributes.[^1_39][^1_19]

#### 2. AI-Powered Anomaly Detection

**Concept:** Apply machine learning to railway-specific protocols and behaviors to detect subtle anomalies that signature-based systems miss.

**Railway Applications:**

- Train control command analysis
- SCADA protocol anomaly detection
- User behavior analytics for maintenance access
- Network traffic pattern analysis

**Requirements:**

- Rail-specific training data
- Integration with existing monitoring
- Low false-positive tuning
- Explainable AI for incident investigation


#### 3. Zero Trust Architecture for Railway OT

**Concept:** Apply zero trust principles ("never trust, always verify") to railway operational technology.

**Components:**

- Micro-segmentation of zones beyond traditional perimeters
- Continuous authentication and authorization
- Least-privilege access enforcement
- Encrypted communications everywhere
- Comprehensive logging and monitoring

**Challenges:**

- Legacy system integration
- Performance impact on real-time systems
- Operational complexity
- Certificate management at scale


#### 4. Blockchain for Supply Chain Security

**Concept:** Use distributed ledger technology to ensure integrity of software updates and components throughout supply chain.

**Applications:**

- Verify authenticity of vendor patches
- Track component provenance
- Immutable audit trail for configuration changes
- Smart contracts for security compliance verification

**Considerations:**

- Vendor ecosystem participation required
- Scalability for high-transaction environments
- Integration with existing change management


#### 5. Quantum-Safe Cryptography Preparation

**Rationale:** Railway infrastructure has 20+ year lifecycles, but quantum computers may break current encryption within 10-15 years.

**Actions:**

- Inventory all cryptographic implementations
- Identify systems requiring long-term confidentiality
- Plan migration to post-quantum cryptographic algorithms
- Monitor NIST post-quantum cryptography standardization


### Conclusion

The Auckland City Rail Link project represents a transformational opportunity to implement world-class railway cybersecurity following the emerging IEC 63452 standard. The comprehensive handover process outlined in this research—encompassing 23 critical deliverables, 35 handover checklist items, and clearly defined roles and responsibilities—provides a robust framework for transitioning cybersecurity accountability from the Link Alliance construction team to Auckland Transport and KiwiRail operations.

**Key Success Factors:**

1. **Comprehensive Documentation:** The cybersecurity case and handover plan are essential artifacts that demonstrate risk management and operational readiness.
2. **Clear Zone Architecture:** Implementing proper network segmentation with defined security zones and controlled conduits protects safety-critical systems while enabling operational flexibility.
3. **Skilled Teams:** Well-defined cybersecurity roles with appropriate competencies ensure effective security management throughout the lifecycle.
4. **Continuous Processes:** Vulnerability management, threat intelligence, incident response, and training programs must be ongoing, not one-time activities.
5. **Stakeholder Collaboration:** Success requires close coordination among Link Alliance, Downer Group, Auckland Transport, KiwiRail, and the CRL operations team.

As IEC 63452 reaches publication in mid-2026, the CRL project has the opportunity to be an early adopter and reference implementation for this groundbreaking standard. The processes, artifacts, and governance structures established for CRL will serve as a model for future railway infrastructure projects across New Zealand and internationally, contributing to safer, more secure, and more resilient railway systems worldwide.

### Supporting Documentation Files

The following files have been created to support implementation:

**Railway Cybersecurity Deliverables (IEC 63452)** - Comprehensive list of 23 deliverables mapped to standard requirements and responsible parties.

**CRL Cybersecurity Handover Checklist** - Detailed 35-item checklist covering documentation, risk, technical, operations, security, and governance domains.

**CRL Roles and Responsibilities Matrix** - Defines 13 key cybersecurity roles with deliverables and handover involvement.

All information in this report is based on extensive research from 128 sources including IEC draft standards, industry publications, project documentation, and cybersecurity best practices specific to railway infrastructure. Citations are provided throughout the document linking to source materials.
<span style="display:none">[^1_100][^1_101][^1_102][^1_103][^1_104][^1_105][^1_106][^1_40][^1_41][^1_42][^1_43][^1_44][^1_45][^1_46][^1_47][^1_48][^1_49][^1_50][^1_51][^1_52][^1_53][^1_54][^1_55][^1_56][^1_57][^1_58][^1_59][^1_60][^1_61][^1_62][^1_63][^1_64][^1_65][^1_66][^1_67][^1_68][^1_69][^1_70][^1_71][^1_72][^1_73][^1_74][^1_75][^1_76][^1_77][^1_78][^1_79][^1_80][^1_81][^1_82][^1_83][^1_84][^1_85][^1_86][^1_87][^1_88][^1_89][^1_90][^1_91][^1_92][^1_93][^1_94][^1_95][^1_96][^1_97][^1_98][^1_99]</span>

<div align="center">⁂</div>

[^1_1]: https://www.alstom.com/press-releases-news/2024/3/towards-first-railway-cybersecurity-international-standard-why-standards-are-important-secure-railways

[^1_2]: https://www.cityraillink.co.nz/testing

[^1_3]: https://en.wikipedia.org/wiki/City_Rail_Link

[^1_4]: https://www.cityraillink.co.nz/city-rail-link-project-overview

[^1_5]: https://www.icomera.com/proudly-contributing-to-the-next-railway-cybersecurity-standard/

[^1_6]: https://cervello.security/blog/regulations/iec-63452-the-future-of-railway-cybersecurity-and-how-to-get-ready/

[^1_7]: https://standardsdevelopment.bsigroup.com/projects/2022-01003

[^1_8]: https://nteg.com/iec-63452-and-railway-cybersecurity/

[^1_9]: https://www.digitaltransit.co.uk/archives/3072

[^1_10]: https://cdn.standards.iteh.ai/samples/sist/osist-pren-iec-63452-2025/d542d8b4f22f499f94d61d08d47b41c7/osist-pren-iec-63452-2025.pdf

[^1_11]: https://orbik-cybersecurity.com/iec-63452/

[^1_12]: https://www.era.europa.eu/system/files/2022-12/03SRIS-1 - IEC - PT 63452.pdf

[^1_13]: https://shieldworkz.com/blogs/how-to-conduct-an-iec-62443-based-assessment-for-metro-rail-infrastructure

[^1_14]: https://industrialcyber.co/critical-infrastructure/enisa-releases-guidance-on-building-cybersecurity-zones-and-conduits-for-railway-systems/

[^1_15]: https://gca.isa.org/blog/how-to-define-zones-and-conduits

[^1_16]: https://cervello.security/blog/regulations/what-is-rail-cybersecurity-compliance/

[^1_17]: https://www.downergroup.com/first-test-train-rolls-through-auckland

[^1_18]: https://www.linkedin.com/posts/downer_cityraillink-linkalliance-downer-activity-7295917218754613248-VzJt

[^1_19]: https://www.downergroup.com/greening-the-tracks-link-alliances-sustainabl

[^1_20]: https://www.downergroup.com/transport-infrastructure

[^1_21]: https://www.cityraillink.co.nz/executive-march-2024

[^1_22]: https://www.govtechreview.com.au/content/gov-transport/article/controlling-auckland-s-city-rail-link-project-1585577626

[^1_23]: https://nzinfrastructure.nz/aucklands-huge-crl-project-a-win-for-city-and-country/

[^1_24]: https://www.apta.com/wp-content/uploads/Standards_Documents/APTA-SS-CCS-RP-004-16.pdf

[^1_25]: https://www.cylus.com/post/vulnerability-management-in-rail-why-context-is-everything

[^1_26]: https://www.linkedin.com/pulse/vulnerability-management-rail-environments-cyber-critical-zeiler-7ayie

[^1_27]: https://cervello.security/blog/railway-cybersecurity-101/cyber-threat-intelligence-for-rail-operators-anticipating-and-mitigating-attacks-before-they-happen/

[^1_28]: https://www.threatproof.com/cyber-security-in-railways-lessons-from-the-past-to-protect-the-future/

[^1_29]: https://www.cybersecuritydive.com/news/railroad-train-vulnerability-derail-brake-cisa-advisory/752940/

[^1_30]: https://cervello.security/blog/vulnerabilities-incidents/research-cve-2025-1727/

[^1_31]: https://pridesolutions.co.uk/secure-by-design-incorporating-cyber-security-into-trains-from-build/

[^1_32]: https://www.iriusrisk.com/resources-blog/railway-automation

[^1_33]: https://railwayacademy.org/product/8-hrs-certificate-course-in-rail-cybersecurity/

[^1_34]: https://informaconnect.com/ot-railway-cybersecurity-otcs/

[^1_35]: https://www.pertecnica.net/railway-cybersecurity-awareness/

[^1_36]: https://www.railway-cybersecurity.com/Railway_Board_Cybersecurity_Training.html

[^1_37]: https://cervello.security/blog/railway-cybersecurity-101/how-to-ensure-your-rail-cybersecurity-incident-response-plan-meets-top-safety-standards/

[^1_38]: https://www.rsiweb.org/member-article-cervellos-important-considerations-when-building-a-rail-cybersecurity-incident-response-plan/

[^1_39]: https://publications.aecom.com/rail/projects/city-rail-link/

[^1_40]: https://papers.academic-conferences.org/index.php/eccws/article/download/2296/2191/8601

[^1_41]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11680022/

[^1_42]: https://cybershield-consulting.com/en/iec-62443-co-ot-security-for-railway-systems-why-safety-on-rails-doesnt-end-with-ticket-checks/

[^1_43]: https://cervello.security/compliance/

[^1_44]: https://www.mobility.siemens.com/us/en/portfolio/digital-solutions-software/cybersecurity/cybersecurity-in-rail.html

[^1_45]: https://www.sciencedirect.com/science/article/pii/S2949867825000248

[^1_46]: https://www.wsp.com/en-us/projects/city-rail-link

[^1_47]: https://betterthingsarepossible.substack.com/p/maximising-the-value-from-our-investment

[^1_48]: https://www.informa.com.au/insight/delivering-transformation-inside-aucklands-city-rail-link/

[^1_49]: https://www.youtube.com/watch?v=e2eNIRfqCq4

[^1_50]: https://www.enisa.europa.eu/sites/default/files/all_files/01-policy-02-era-jo-de-bosschere.pdf

[^1_51]: https://railroads.dot.gov/elibrary/ptc-communications-cybersecurity-technology-review-and-concept-operations

[^1_52]: https://learninglegacy.crossrail.co.uk/documents/cyber-security-management-and-assurance/

[^1_53]: https://www.cylus.com/event/the-road-to-iec-63452-standardizing-rail-cybersecurity

[^1_54]: https://railroads.dot.gov/sites/fra.dot.gov/files/2020-06/Cyber Security Risk Management-A_0.pdf

[^1_55]: https://industrialcyber.co/control-device-security/global-perspective-on-dealing-with-complexities-of-rail-cybersecurity-using-regulations-collaborations/

[^1_56]: https://www.viavisolutions.com/en-us/literature/cybersecurity-railway-brochures-en.pdf

[^1_57]: https://www.cylus.com/post/navigating-ts-50701-unpacking-the-impact-of-the-cybersecurity-standard-for-rail

[^1_58]: https://mipro.fi/media/blogi/signal-draht-secure-software-development-practices-for-the-compliance-of-railway-applications-with-iec62443/

[^1_59]: https://www.enisa.europa.eu/sites/default/files/publications/Zoning and Conduits for Railways - Security Architecture.pdf

[^1_60]: https://www.railway-cybersecurity.com/Rail_Cyber_Security_Guidance.html

[^1_61]: https://www.cisco.com/c/dam/en/us/td/docs/solutions/Verticals/Transportation/Rail-CBTC/Rail_CBTC_Design_Guide.pdf

[^1_62]: https://www.youtube.com/watch?v=nxjsJ7OQwyY

[^1_63]: https://www.aar.org/wp-content/uploads/2018/10/Rail-Sector-Effective-IT-Procurement-Practices-Final-April-2018.pdf

[^1_64]: https://www.era.europa.eu/system/files/2022-11/enr135-taking_cybersecurity_challenges_into_account_in_railway_safety_en.pdf

[^1_65]: https://www.linkedin.com/pulse/cybersecurity-activities-railway-application-cycle-shiv-thudf

[^1_66]: https://www.era.europa.eu/system/files/2024-10/session 3-1 - iec pt 63452 update - serge benoliel.pdf?t=1733394456

[^1_67]: https://www.cylus.com/post/q-a-the-road-to-iec-63452-webinar

[^1_68]: https://www.downergroup.co.nz/city-rail-link-project-wol-case-study

[^1_69]: https://rail.nridigital.com/future_rail_may25/building_next_generation_railway_cybersecurity

[^1_70]: https://www.ghd.com/en-us/insights/getting-on-track-with-rail-cybersecurity

[^1_71]: https://www.intertechrail.com/railway-cybersecurity-guide

[^1_72]: https://kth.diva-portal.org/smash/get/diva2:1845302/FULLTEXT01.pdf

[^1_73]: https://www.micromindercs.com/railway

[^1_74]: https://media.armis.com/raw/upload/iec-62443-rfp-template.docx

[^1_75]: https://www.cylus.com/resources/practical-guidelines-on-cybersecurity-requirements-in-tendering

[^1_76]: https://assets.new.siemens.com/siemens/assets/api/uuid:78855a92-ddb8-46f3-af38-a5d57920f3e4/Cybersecurity-whitepaper.pdf

[^1_77]: https://www.exida.com/Company/News/exida-releases-updated-templates-based-on-iec-62443-for-end-users

[^1_78]: https://www.sciencedirect.com/science/article/pii/S2773153725000556

[^1_79]: https://zenodo.org/record/3087656/files/RSSRail-2019_paper_39.pdf

[^1_80]: https://www.phoenixcontact.com/en-us/industries/industrial-security/iec-62443-the-industrial-cybersecurity-standard

[^1_81]: https://cervello.security/blog/railway-cybersecurity-101/how-to-create-the-right-cybersecurity-work-plan-for-your-railway-operations/

[^1_82]: https://www.nrc.gov/docs/ML1100/ML110060097.pdf

[^1_83]: https://vaultry.com/cyber-security-risk-management-plan-and-template/

[^1_84]: https://industrialcyber.co/industrial-cyber-attacks/critical-cyber-flaw-linked-to-eot-module-ignored-in-us-rail-systems-for-12-years-fix-not-expected-until-2027/

[^1_85]: https://industrialcyber.co/transport/guarding-the-tracks-cybersecurity-imperatives-for-the-future-of-rail-infrastructure/

[^1_86]: https://www.cyberdefensemagazine.com/why-cybersecurity-compliance-in-rail-transportation-has-never-been-more-important-or-more-challenging-to-keep-on-track/

[^1_87]: https://www.larksuite.com/en_us/topics/project-management-methodologies-for-functional-teams/gantt-chart-for-cybersecurity-teams

[^1_88]: https://www.raildeliverygroup.com/media-centre-docman/acop/279-rdg-ec-gn006cybersecuritysigned/file.html

[^1_89]: https://gca.isa.org/blog/understanding-railway-cybersecurity

[^1_90]: https://www.digitaltransit.co.uk/archives/4713

[^1_91]: https://www.excellentwebworld.com/cybersecurity-risk-management-plan/

[^1_92]: https://www.txone.com/blog/potential-threats-to-railway-industry/

[^1_93]: https://www.sans.org/white-papers/34440

[^1_94]: https://www.nvent.com/en-pr/schroff/cybersecurity-modern-railway-infrastructure

[^1_95]: https://clickup.com/templates/gantt-chart/cybersecurity-professionals

[^1_96]: https://www.railway-cybersecurity.com

[^1_97]: https://www.scribd.com/document/904135710/Gantt-Chart-for-Railway-Management-With-Payment-System

[^1_98]: https://railwayacademy.org/railway-cybersecurity-everything-you-need-to-know/

[^1_99]: https://standardsdevelopment.bsigroup.com/projects/9025-12469

[^1_100]: https://informaconnect.com/cenelec-ts-50701-rail-cyber-security/

[^1_101]: http://scadamag.infracritical.com/index.php/2025/01/26/zones-conduits-and-what-they-mean/

[^1_102]: https://www.linkedin.com/posts/shamikkumar_zoning-in-railways-activity-7323657164194004992-Rugq

[^1_103]: https://digital.aecom.com/project/city-rail-link/

[^1_104]: https://assets.metrolinx.com/image/upload/Documents/Engineering/Metrolinx_Rail_Corridor_Asset_Handover_Protocol.pdf

[^1_105]: https://www.buddlefindlay.com/insights/city-rail-link/

[^1_106]: https://learninglegacy.crossrail.co.uk/documents/information-handover-principles/

