# Government Sector - Operations and Maintenance

## Security Operations Center (SOC)

### SOC Staffing and Organization
**SOC Roles and Responsibilities**
- **SOC Manager/Director**: Overall SOC operations oversight
- **SOC Supervisor/Shift Lead**: Shift supervision, escalation point
- **Security Analysts (Tier 1, 2, 3)**: Monitoring, analysis, response
- **Security Engineers**: System configuration, tuning, integration
- **Incident Responders**: Active incident investigation and containment
- **Threat Intelligence Analysts**: Threat research and intelligence gathering
- **Forensic Analysts**: Digital forensics and evidence collection
- **Compliance Analysts**: Audit support, compliance monitoring

**Shift Schedules**
- 24/7/365 monitoring coverage
- 8-hour shifts (3 shifts: day, evening, overnight)
- 12-hour shifts (2 shifts: day, night) - common in government
- Follow-the-sun model (global SOCs)
- On-call rotation for escalations
- Weekend and holiday coverage

**SOC Facility Requirements**
- Secure access control (restricted to authorized personnel)
- Video wall displays (situational awareness)
- Operator workstations (multi-monitor setups)
- Private conference rooms (incident response, briefings)
- Secure communications (classified/unclassified separation)
- Backup power (UPS, generator)
- Environmental controls (24/7 HVAC)
- Break room and rest facilities

### Monitoring Systems and Tools
**Security Information and Event Management (SIEM)**
- Splunk Enterprise Security
- IBM QRadar
- LogRhythm NextGen SIEM
- ArcSight (Micro Focus)
- Microsoft Sentinel (cloud SIEM)
- Elastic Security (ELK stack)
- AlienVault OSSIM (open-source)

**SIEM Functions**
- Log aggregation and correlation
- Real-time alerting
- Threat detection (signatures, anomalies, behavior)
- Dashboards and visualization
- Incident investigation and forensics
- Compliance reporting (FISMA, NIST, PCI-DSS)
- Threat intelligence integration
- User and entity behavior analytics (UEBA)

**Video Management Systems (VMS)**
- Milestone XProtect Corporate
- Genetec Security Center
- Avigilon Control Center
- Honeywell MAXPRO VMS
- Hanwha Wave
- Live monitoring (multiple camera views)
- Event-driven viewing (alarm integration)
- Video search and forensics
- Incident clip export

**Access Control Management**
- Lenel OnGuard
- Software House C•CURE 9000
- AMAG Symmetry
- HID VertX EVO
- Real-time access events
- Alarm monitoring (door forced, door held open)
- Cardholder search and management
- Badge activation/deactivation
- Integration with video (alarm verification)

**Intrusion Detection Monitoring**
- Central station monitoring (UL-listed)
- Alarm receiving software (SureView, MASterMind)
- Zone status display
- Alarm verification (video, audio)
- Guard dispatch
- Law enforcement notification
- Alarm history and reporting

**Building Automation Monitoring**
- Johnson Controls Metasys
- Honeywell Enterprise Buildings Integrator
- Siemens Desigo CC
- Schneider Electric EcoStruxure Building Operation
- HVAC system status
- Energy monitoring
- Equipment alarms and faults
- Environmental monitoring (temperature, humidity)

### Standard Operating Procedures (SOPs)
**Alarm Response Procedures**
- **Intrusion Alarms**: Video verification, dispatch guard/law enforcement
- **Access Control Alarms**: Review video, contact employee/guard
- **Fire Alarms**: Verify alarm, notify fire department, initiate evacuation
- **Duress Alarms**: Silent alarm response, law enforcement dispatch
- **Medical Emergencies**: EMS dispatch, AED deployment
- **Video Analytics Alerts**: Review video, assess threat, dispatch as needed

**Incident Classification**
- **Priority 1 (Critical)**: Active threat, life safety, terrorism
- **Priority 2 (High)**: Intrusion, unauthorized access, security breach
- **Priority 3 (Medium)**: Alarm verification needed, suspicious activity
- **Priority 4 (Low)**: Routine patrols, maintenance issues
- **Priority 5 (Informational)**: Status updates, system alerts

**Escalation Procedures**
- Tier 1 response (initial assessment and action)
- Tier 2 escalation (complex incidents, supervisor notification)
- Tier 3 escalation (management notification, law enforcement coordination)
- Executive notification (critical incidents)
- After-hours emergency contact procedures

**Incident Documentation**
- Real-time incident logging (CAD - Computer-Aided Dispatch)
- Incident report writing (who, what, when, where, why, how)
- Video clip export and attachment
- Evidence collection and chain of custody
- Photo documentation
- Witness statements
- Post-incident review and lessons learned

### Guard Force Operations
**Guard Services**
- **Contract Guard Services**: Allied Universal, Securitas, G4S, Whelan
- **Proprietary Guards**: In-house security force
- **Federal Protective Service (FPS)**: Federal facility protection
- **Police Officers**: On-site law enforcement presence
- **Armed vs. Unarmed**: Based on facility risk assessment

**Guard Posts and Patrols**
- **Fixed Posts**: Lobby reception, security desk, vehicle checkpoint
- **Roving Patrols**: Foot patrols, vehicle patrols, interior/exterior
- **Screening Posts**: X-ray operator, metal detector, hand wand
- **Emergency Response**: First responder to incidents
- **Access Control**: Badge verification, visitor escort
- **CCTV Monitoring**: Video surveillance monitoring

**Guard Training and Certification**
- State security license (armed/unarmed)
- Federal facility training (FPS Level II, III, IV)
- CPR/First Aid/AED certification
- FEMA ICS-100, ICS-200 (Incident Command System)
- Defensive tactics and use of force
- Report writing and documentation
- Customer service and communication
- Site-specific post orders training
- Annual refresher training

**Guard Management**
- Post orders (detailed instructions for each post)
- Daily Activity Reports (DAR)
- Incident reports
- Visitor logs
- Vehicle logs
- Patrol tour verification (guard tour systems)
- Performance evaluations
- Contract oversight and quality assurance

## Preventive Maintenance Programs

### Access Control System Maintenance
**Regular Maintenance Tasks**
- Door hardware inspection and lubrication (quarterly)
- Card reader cleaning and testing (quarterly)
- Lock testing (maglocks, electric strikes, mortise locks) - monthly
- Door closer adjustment (semi-annual)
- Turnstile lubrication and alignment (quarterly)
- Battery backup testing (monthly)
- Controller health check and firmware updates (quarterly)
- Credential reader alignment and functionality testing

**Preventive Maintenance Schedule**
- Daily: System health monitoring, alarm review
- Weekly: Door function testing (sample)
- Monthly: Battery backup test, lock testing
- Quarterly: Comprehensive door hardware inspection
- Semi-Annual: System performance review, firmware updates
- Annual: Full system audit, load testing, contract renewal

**Access Control Database Maintenance**
- Cardholder database cleanup (remove terminated employees)
- Audit user permissions and access levels (quarterly)
- Review access groups and schedules (semi-annual)
- Archive old transactions (annual)
- Database backup (daily, weekly, monthly retention)
- Test database restore procedures (quarterly)

### Video Surveillance System Maintenance
**Camera Maintenance**
- Lens cleaning (quarterly or as needed)
- Focus and alignment adjustment (semi-annual)
- Weatherproof housing inspection (semi-annual)
- Heater/blower functionality test (annual, before winter)
- IR illuminator testing (annual)
- Mounting bracket tightness check (annual)
- Camera health monitoring (daily, via VMS)

**NVR/Server Maintenance**
- Hard drive health monitoring (daily)
- Storage capacity monitoring (weekly)
- RAID status verification (daily)
- Firmware and software updates (quarterly)
- Log file review and cleanup (monthly)
- Backup configuration files (monthly)
- Clean filters and fans (quarterly)
- Test failover and redundancy (semi-annual)

**Network Infrastructure Maintenance**
- Switch health and performance monitoring (daily)
- PoE power budget review (quarterly)
- Network bandwidth utilization (weekly)
- Firmware updates (semi-annual)
- Port status and error monitoring
- Cable testing and certification (as needed)
- UPS battery testing (monthly)

### Fire Alarm System Maintenance
**NFPA 72 Required Testing**
- **Monthly**: System functionality test, battery voltage test
- **Quarterly**: Quarterly inspection (visual inspection of devices)
- **Semi-Annual**: Detector sensitivity testing (addressable systems)
- **Annual**: Full system functional test
  - All smoke detectors tested
  - Heat detectors tested
  - Manual pull stations activated
  - Notification appliances tested (horns, strobes, speakers)
  - Flow switches tested (sprinkler systems)
  - Tamper switches tested
  - Battery load test (discharge and recharge)
  - Communication path testing (DACT, cellular, IP)

**Inspection, Testing, and Maintenance (ITM)**
- Licensed fire alarm technician (NICET certified)
- Annual inspection report
- Device database updates
- Sensitivity testing and detector cleaning
- Device replacement (as needed)
- Firmware updates (panel and devices)

**Sprinkler System Maintenance (NFPA 25)**
- Weekly: Visual inspection (facility staff)
- Monthly: Valve supervision test, gauges checked
- Quarterly: Main drain test, alarm valve inspection
- Semi-Annual: Flow switch test
- Annual: Full system inspection and test
- 5-Year: Internal inspection of valves, piping
- 10-Year: Sprinkler head replacement (standard-response heads)

### Building Automation System Maintenance
**HVAC System Maintenance**
- **Monthly**: Filter replacement, belt inspection, vibration analysis
- **Quarterly**: Coil cleaning, damper actuator inspection, VFD inspection
- **Semi-Annual**: Refrigerant charge check, economizer function test
- **Annual**: Full system performance test, efficiency analysis, calibration

**BAS Controller Maintenance**
- Daily: Alarm review, system health monitoring
- Monthly: Controller status review, communication verification
- Quarterly: Database backup, sequence of operations verification
- Semi-Annual: Firmware updates, software patches
- Annual: Comprehensive control sequence review, energy analysis

**Sensor Calibration**
- Temperature sensors: Annual calibration
- Pressure sensors: Annual calibration
- Humidity sensors: Semi-annual calibration
- CO2 sensors: Semi-annual calibration
- Airflow measuring stations: Annual calibration
- Energy meters: Annual verification

### Elevator and Escalator Maintenance
**Elevator Maintenance**
- Monthly: Full inspection (per ASME A17.1)
  - Car and hoistway inspection
  - Door operation and safety devices
  - Brake testing
  - Governor testing
  - Emergency lighting and communication
  - Machine room inspection
  - Lubrication and adjustments

**Elevator Testing**
- Annual: Load test (125% rated capacity)
- Annual: Fire service test (Phase I and II)
- Annual: Emergency power test
- 5-Year: Full load brake test
- 5-Year: Safety (governor) test

**Escalator Maintenance**
- Monthly: Full inspection and lubrication
- Quarterly: Brake test, handrail speed test
- Semi-Annual: Step chain inspection
- Annual: Emergency stop test, load test

### Electrical System Maintenance
**Generator Maintenance**
- Weekly: Automatic exercise (no-load, 30 minutes)
- Monthly: Loaded exercise (with building load)
- Quarterly: Oil change (depending on runtime)
- Semi-Annual: Fuel system inspection and cleaning
- Annual: Load bank test (full load, 2 hours)
- Annual: Cooling system service
- Annual: Battery load test
- Annual: Transfer switch testing

**UPS Maintenance**
- Monthly: Battery voltage and temperature monitoring
- Quarterly: Battery discharge test (brief)
- Semi-Annual: UPS load test
- Annual: Battery load test (full discharge and recharge)
- Annual: Thermal imaging (connections, components)
- 3-5 Years: Battery replacement (VRLA)
- 10+ Years: Battery replacement (Lithium-Ion)

**Electrical Distribution Maintenance**
- Annual: Infrared thermography (switchgear, panels, connections)
- Annual: Power quality analysis
- 3-5 Years: Circuit breaker testing and calibration
- 5 Years: Ground fault testing
- 10 Years: Arc flash study update

## Corrective and Emergency Maintenance

### Emergency Response Procedures
**Security System Failures**
- Access control failure: Manual lock override, posted guard
- Video surveillance failure: Increase patrols, temporary cameras
- Intrusion detection failure: Central station notification, guard response
- Fire alarm failure: Fire watch patrol (hourly, documented)

**Building System Emergencies**
- HVAC failure: Emergency repair, temporary cooling/heating
- Power outage: Generator activation, UPS monitoring
- Water leak: Shut off valves, extract water, dry out
- Elevator entrapment: Fire department notification, manual lowering procedures

**Emergency Maintenance Contracts**
- 24/7 emergency hotline
- Guaranteed response time (2-4 hours)
- Parts and labor coverage
- Priority service
- Loaner equipment availability

### Work Order Management
**Computerized Maintenance Management System (CMMS)**
- IBM Maximo
- Infor EAM
- SAP Plant Maintenance
- FMX (Facility Management eXpress)
- UpKeep

**Work Order Types**
- **Preventive Maintenance (PM)**: Scheduled recurring maintenance
- **Corrective Maintenance (CM)**: Repair work (non-emergency)
- **Emergency Maintenance (EM)**: Urgent repairs (< 4 hours)
- **Project Work**: Capital improvements, renovations
- **Inspections**: Routine inspections, testing, audits

**Work Order Workflow**
- Request submission (occupant, automated, inspection)
- Work order creation and assignment
- Technician dispatch
- Parts procurement (if needed)
- Work completion and documentation
- Quality inspection
- Work order closure
- Asset history update

**Performance Metrics**
- Mean Time To Repair (MTTR)
- Mean Time Between Failures (MTBF)
- Planned Maintenance Percentage (PMP)
- Work order backlog
- First-time fix rate
- Customer satisfaction scores
- Equipment uptime/availability

## Training and Competency

### Technical Training
**Access Control and Security Systems**
- Manufacturer training (Lenel, Software House, HID, Mercury)
- Certification programs (manufacturer-specific)
- Installation and configuration
- Advanced troubleshooting
- Integration programming
- Cybersecurity for security systems

**Video Surveillance**
- VMS training (Milestone, Genetec, Avigilon)
- Camera installation and configuration
- Network design and troubleshooting
- Video analytics configuration
- ONVIF integration
- Video system cybersecurity

**Fire Alarm Systems**
- NICET Fire Alarm Systems (Level I, II, III, IV)
- Manufacturer training (Simplex, Notifier, Edwards)
- NFPA 72 code compliance
- Fire alarm system design
- Inspection, testing, and maintenance
- Suppression system training

**Building Automation**
- BAS vendor training (JCI, Honeywell, Siemens, Schneider)
- BACnet fundamentals
- HVAC control sequences
- Energy management strategies
- Cybersecurity for building automation
- Advanced programming and graphics

### Operator Training
**SOC Operator Training**
- Security systems operation
- Incident response procedures
- Customer service and communication
- Report writing
- Emergency procedures
- Cybersecurity awareness
- Threat recognition

**Facility Operator Training**
- System-specific training (access control, fire, BAS)
- Emergency procedures
- Building systems overview
- Energy management
- Occupant services
- Customer service

### Continuing Education
**Industry Certifications**
- **PSP (Physical Security Professional)** - ASIS International
- **CPP (Certified Protection Professional)** - ASIS International
- **CFE (Certified Fire Protection Specialist)** - NFPA
- **CEM (Certified Energy Manager)** - AEE
- **LEED AP (LEED Accredited Professional)** - USGBC
- **NICET (National Institute for Certification in Engineering Technologies)**
- **EPA 608 Universal (HVAC refrigerant handling)**

**Professional Development**
- Industry conferences (ASIS, NFPA, ISC, AHR Expo)
- Webinars and online training
- Vendor training and certification
- Code update training (NFPA, ASHRAE, NEC)
- Cybersecurity training and awareness

## Energy Management and Optimization

### Energy Monitoring and Tracking
**Utility Monitoring**
- Real-time energy consumption dashboards
- Peak demand monitoring and alerts
- Utility bill validation
- Energy cost allocation and chargebacks
- Renewable energy production tracking
- Carbon emissions tracking

**Energy Analytics Platforms**
- Schneider Electric EcoStruxure Resource Advisor
- Johnson Controls Metasys Energy Dashboard
- Honeywell Forge Energy Optimization
- EnergyCAP
- Pulse Energy
- SkySpark (analytics platform)

**Key Performance Indicators (KPIs)**
- Energy Use Intensity (EUI) - kBtu/sqft/year
- Energy cost per square foot ($/sqft/year)
- Peak demand (kW)
- Power factor
- Carbon emissions (metric tons CO2e)
- Renewable energy percentage
- ENERGY STAR score (1-100)
- Utility cost avoidance

### Energy Conservation Measures (ECMs)
**HVAC Optimization**
- Optimal start/stop sequences
- Static pressure reset
- Chilled water temperature reset
- Supply air temperature reset
- Economizer optimization (free cooling)
- Demand control ventilation (DCV)
- Equipment scheduling and setback
- Variable speed drive (VFD) installation

**Lighting Optimization**
- LED retrofits
- Occupancy sensor installation
- Daylight harvesting
- Lighting power density reduction
- Exterior lighting controls (photocell, timeclock)
- Task lighting strategies
- Bi-level switching

**Building Envelope Improvements**
- Window film installation
- Weatherstripping and sealing
- Roof insulation upgrades
- Window replacement (high-performance glazing)
- Cool roof coatings
- Air sealing (reduce infiltration)

**Renewable Energy and Storage**
- Rooftop solar PV systems
- Ground-mount solar arrays
- Solar carports
- Battery energy storage systems (BESS)
- Electric vehicle (EV) charging stations
- Geothermal heat pumps
- Combined heat and power (CHP)

### Demand Response Programs
**Utility DR Programs**
- Peak time rebates (PTR)
- Critical peak pricing (CPP)
- Time-of-use (TOU) rates
- Capacity bidding programs (CBP)
- Emergency demand response
- Economic demand response
- Direct load control programs

**Demand Response Strategies**
- Pre-cooling/pre-heating buildings
- HVAC setpoint adjustment during events
- Chiller optimization and load shedding
- Lighting dimming or zone shutdown
- Plug load management (non-critical equipment)
- On-site generator activation
- Battery storage discharge

**Automated Demand Response (Auto-DR)**
- OpenADR 2.0b protocol
- Utility signal integration
- Automated load shedding
- Event notification and reporting
- Performance verification
- Financial settlement and reconciliation

### Commissioning and Retro-Commissioning
**Building Commissioning (Cx)**
- Verification that systems function as designed
- Pre-functional testing
- Functional performance testing
- Systems integration testing
- Training and documentation
- Owner's project requirements (OPR)
- Basis of design (BOD)

**Retro-Commissioning (RCx)**
- Systematic investigation of existing building systems
- Energy and operational improvements
- Low-cost/no-cost improvements
- Sequence of operations optimization
- Control calibration and adjustment
- Documentation updates
- Energy savings verification

**Monitoring-Based Commissioning (MBCx)**
- Continuous commissioning using building automation data
- Automated fault detection and diagnostics (FDD)
- Performance degradation detection
- Trend analysis and alarming
- Automated reporting
- Proactive maintenance

## Compliance and Auditing

### Security Compliance Audits
**Physical Security Audits**
- ISC (Interagency Security Committee) compliance
- Facility Security Level (FSL) verification
- Countermeasure effectiveness evaluation
- Access control audit (badge usage, access rights)
- Video surveillance coverage review
- Intrusion detection testing
- Security guard post compliance
- Emergency procedures and drills

**Access Control Audits**
- User access rights review (quarterly)
- Terminated employee badge deactivation verification
- Guest and contractor access logs
- Badge issuance and return procedures
- Access control system health check
- Integration testing (video, intrusion, fire)
- Cyber hygiene (password changes, patch status)

**Video Surveillance Audits**
- Camera coverage verification
- Video quality and resolution check
- Recording retention compliance
- Video management system health
- Network bandwidth and storage capacity
- Integration testing (access control, analytics)
- Privacy compliance (masking, retention policies)

### Fire and Life Safety Inspections
**Authority Having Jurisdiction (AHJ) Inspections**
- Fire marshal annual inspection
- Fire alarm system testing (witnessed)
- Sprinkler system inspection
- Fire suppression system testing
- Egress and exit sign inspection
- Emergency lighting testing
- Fire extinguisher inspection (monthly, annual)
- Fire drill documentation review

**Fire Alarm Annual Testing**
- All initiating devices tested (smoke, heat, pull stations)
- All notification appliances tested (horns, strobes, speakers)
- Addressable device communication verified
- Control panel functionality tested
- Battery backup load test
- Alarm transmission to monitoring station verified
- Fire pump and sprinkler system flow switch tested
- HVAC shutdown and smoke control verified

**Sprinkler System Inspection (NFPA 25)**
- Quarterly main drain test
- Semi-annual flow switch test
- Annual full system inspection
- 5-year internal valve inspection
- 10-year sprinkler head replacement (standard-response)
- 50-year sprinkler head replacement (fast-response)
- Backflow preventer testing (annual)

### Building Code Compliance
**Accessibility Compliance (ADA)**
- Accessible routes and entrances
- Door hardware and operation (opening force, closing speed)
- Signage (Braille, tactile, contrast)
- Toilet and bathing facilities
- Parking and drop-off areas
- Visual alarm notification (strobes)

**Energy Code Compliance**
- ASHRAE 90.1 compliance verification
- Building envelope testing (blower door test)
- HVAC equipment efficiency verification
- Lighting power density (LPD) calculation
- Commissioning documentation
- Energy modeling (as-designed vs. as-built)

**Occupancy and Fire Code Compliance**
- Occupancy load calculations
- Egress capacity and travel distance
- Exit signs and emergency lighting
- Fire-rated construction and doors
- Fire alarm and sprinkler system coverage
- Means of egress obstruction prevention

### Cybersecurity Compliance
**NIST Cybersecurity Framework**
- Identify: Asset inventory, risk assessment
- Protect: Access control, awareness training, data security
- Detect: Anomalies and events, continuous monitoring
- Respond: Response planning, communications, analysis, mitigation
- Recover: Recovery planning, improvements, communications

**NIST SP 800-53 Controls**
- Access Control (AC)
- Audit and Accountability (AU)
- Configuration Management (CM)
- Identification and Authentication (IA)
- Incident Response (IR)
- System and Communications Protection (SC)
- System and Information Integrity (SI)

**Vulnerability Management**
- Regular vulnerability scanning (monthly)
- Penetration testing (annual)
- Patch management (critical patches within 30 days)
- Vulnerability remediation tracking
- Risk acceptance documentation
- Compensating controls

**Audit Logging and Monitoring**
- Centralized log collection (SIEM)
- Log retention (1 year minimum, 7 years for some compliance)
- User activity monitoring
- Privileged access monitoring
- Alert tuning and threshold adjustment
- Incident investigation and forensics
- Compliance reporting (FISMA, NIST)
