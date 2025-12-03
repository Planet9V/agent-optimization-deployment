# Dams Sector - Operational Procedures & Best Practices

**Document Version:** 1.0
**Classification:** Operational Guidelines
**Last Updated:** 2025-11-05
**Framework:** FERC Operations, USACE Safety Standards, NERC CIP

## Executive Summary

This document outlines operational procedures, best practices, and standard operating procedures (SOPs) for dam operations encompassing hydroelectric generation, flood control, water supply management, and safety operations. Procedures integrate cybersecurity, physical security, and operational resilience requirements.

---

## 1. Normal Operations Procedures (100+ Patterns)

### 1.1 Hydroelectric Generation Operations

**HGO-001: Unit Startup Procedure**
```
PRE-START CHECKS:
1. Verify unit lockout/tagout clear
2. Confirm bearing oil levels and cooling water flow
3. Check generator stator cooling (air/water systems)
4. Verify excitation system operational
5. Confirm governor hydraulic pressure normal
6. Check protection relay status - no alarms
7. Verify transformer oil level and temperature
8. Confirm switchyard breaker availability
9. Check reservoir level adequate for generation
10. Verify downstream flow requirements met

STARTUP SEQUENCE:
1. Close unit intake gates (wicket gates to minimum position)
2. Open main inlet valve slowly
3. Engage turbine turning gear, verify rotation
4. Disengage turning gear
5. Open wicket gates gradually to speed-no-load (SNL)
6. Monitor turbine speed, vibration, bearing temperatures
7. Close generator field breaker (excite generator)
8. Adjust excitation to rated voltage
9. Verify generator synchronized to grid frequency
10. Close generator breaker at synchronization point
11. Load unit gradually per manufacturer specifications
12. Monitor MW, MVAr, voltage, current, power factor
13. Transfer to automatic generation control (AGC) if available

DOCUMENTATION:
- Log start time, initial conditions, parameters
- Note any anomalies or deviations from normal
- Record start-up curves for trend analysis
```

**HGO-002: Unit Normal Operation Monitoring**
```
EVERY 15 MINUTES:
- MW output, MVAr, power factor
- Generator voltage, current, frequency
- Excitation current and voltage
- Turbine speed and gate position
- Reservoir level and tailwater elevation
- Bearing temperatures (generator, turbine, thrust)
- Vibration levels (bearing housings, generator frame)
- Cooling water temperatures (stator, bearings, air coolers)
- Transformer oil temperature (top oil, winding)
- Governor oil pressure
- Station service voltage and frequency

HOURLY:
- Record generation totals (MWh)
- Log water flow (CFS) and head (feet)
- Calculate unit efficiency
- Check SCADA alarm history
- Verify communication links operational

SHIFT CHANGE:
- Complete comprehensive unit walkdown
- Document any changes in unit condition
- Transfer all current operational notes
- Review pending maintenance, work orders
- Confirm emergency equipment availability
```

**HGO-003: Unit Load Changes**
```
NORMAL LOAD CHANGES (AGC):
- Automatic response to grid signals
- Rate limits: 1-5% per minute typical
- Governor deadband: ±0.036 Hz typical
- Monitor for hunting or instability

MANUAL LOAD CHANGES:
1. Verify grid frequency stable
2. Confirm reservoir level adequate
3. Check transformer loading limits
4. Coordinate with system operator
5. Adjust governor setpoint gradually
6. Monitor generator, transformer temperatures
7. Log change in operations log

EMERGENCY LOAD REJECTION:
1. Generator breaker trips - full load rejection
2. Turbine gates close rapidly (3-10 seconds)
3. Overspeed protection activates if necessary
4. Monitor pressure surge, water hammer
5. Check for equipment damage
6. Investigate cause before restart
```

**HGO-004: Unit Shutdown Procedure**
```
NORMAL SHUTDOWN:
1. Reduce unit load to minimum (10-20% typically)
2. Open generator breaker
3. Reduce excitation to minimum
4. Open generator field breaker
5. Close wicket gates to stop turbine
6. Engage turning gear once speed < 10% rated
7. Close main inlet valve
8. Verify unit stopped, turning gear operational
9. Monitor bearing, winding cooldown
10. Log shutdown time, parameters, reason

POST-SHUTDOWN:
- Continue cooling water flow per manufacturer specs
- Monitor bearing temperatures during cooldown
- Verify all protection relays reset
- Update unit status in SCADA
- Document shutdown in operations log

EMERGENCY SHUTDOWN:
- Emergency stop button activates
- Generator breaker trips immediately
- Wicket gates close in 3-5 seconds
- All auxiliaries maintain operation
- Investigate cause, inspect unit before restart
```

**HGO-005: Pumped Storage Operations**
```
GENERATING MODE:
- Follow standard generation startup procedures
- Monitor upper reservoir level
- Coordinate with pool schedule
- Typical operation: 6-10 hours daily

PUMPING MODE:
1. Unit must be at rest (not generating)
2. Reverse turbine rotation using motor starting
3. Open lower reservoir gates
4. Establish flow from lower to upper reservoir
5. Monitor motor current, voltage, power factor
6. Track pumping efficiency and water transferred
7. Typical operation: off-peak hours (10PM-6AM)

TRANSITION (GENERATING TO PUMPING):
1. Shut down generating mode per normal procedure
2. Wait for unit to stop completely
3. Reconfigure hydraulic systems
4. Switch electrical configuration to motor mode
5. Start pumping sequence
6. Verify all parameters within limits
```

**HGO-006: Black Start Operations**
```
PREREQUISITES:
- Grid blackout confirmed
- Black start unit designated and ready
- Station service power available (diesel gen)
- Reservoir level adequate
- Unit mechanically ready

BLACK START SEQUENCE:
1. Energize station service from diesel generator
2. Establish DC control power
3. Energize black start unit field
4. Start turbine per normal procedure
5. Bring unit to rated voltage and frequency
6. Energize station service transformer
7. Transfer station service to black start unit
8. Energize transmission line (dead line charging)
9. Close transmission line to substation
10. Coordinate with grid operator for restoration

BLACK START DRILLS:
- Conducted annually minimum
- Simulates grid blackout conditions
- Tests diesel generator automatic start
- Verifies operator proficiency
- Documents restoration timeline
```

**HGO-007: Distributed Generation Coordination**
```
GRID INTERCONNECTION:
- Synchronizing to grid: frequency ±0.1 Hz
- Voltage matching: ±5% of nominal
- Phase angle: <10 degrees
- Synchroscope rotating slowly clockwise

ISLANDED OPERATION:
- Grid separation detected
- Unit(s) supply station load only
- Frequency and voltage control local
- Load shedding if generation < load
- Automatic resynchronization when grid available

POWER QUALITY:
- Voltage regulation: ±2.5% steady-state
- Frequency regulation: ±0.036 Hz (droop)
- Harmonic distortion: <5% THD
- Power factor: 0.95 leading to 0.90 lagging
```

### 1.2 Flood Control Operations

**FCO-001: Reservoir Level Management**
```
NORMAL OPERATIONS:
- Maintain conservation pool elevation
- Monitor inflow vs. outflow
- Follow rule curve for seasonal targets
- Coordinate with downstream releases
- Document hourly reservoir levels

CONSERVATION POOL TARGETS:
- Summer (May-September): Maximum for recreation
- Fall (October-November): Drawdown for flood space
- Winter (December-March): Flood control pool
- Spring (April): Begin refill for summer

DEVIATIONS:
- Drought conditions: Maintain minimum pool
- Above-normal precipitation: Begin precautionary releases
- All deviations require coordination with water master
```

**FCO-002: Flood Forecasting & Monitoring**
```
REAL-TIME DATA SOURCES:
- USGS stream gauges (upstream, downstream)
- NWS precipitation forecasts
- Reservoir inflow measurements
- Tributary flow contributions
- Snowpack data (for spring runoff)
- Soil moisture conditions

FORECAST UPDATES:
- Monitor NWS river forecasts every 6 hours
- Update reservoir inflow forecasts daily
- Coordinate with upstream dam operators
- Participate in river forecast center calls
- Issue internal flood alerts as appropriate

DECISION SUPPORT:
- Reservoir routing models (HEC-ResSim)
- Real-time inflow forecasting
- Downstream flow capacity analysis
- Levee system limitations
- Evacuation threshold identification
```

**FCO-003: Controlled Release Operations**
```
RELEASE PLANNING:
1. Determine desired downstream flow
2. Calculate required gate openings
3. Consider tailwater effects
4. Coordinate with downstream entities
5. Issue public release notification (24-48 hrs advance)
6. Document release plan in operations log

GATE OPERATION SEQUENCE:
- Open gates sequentially, not simultaneously
- Monitor vibration, flow characteristics
- Typical opening rate: 1 foot per 5 minutes
- Maximum rate: per manufacturer specifications
- Video record gate operations

DOWNSTREAM NOTIFICATIONS:
- Recreation users (campgrounds, boat ramps)
- Hydroelectric plants (downstream)
- Municipal water intakes
- Irrigation districts
- Fish and wildlife agencies
- Navigation interests

RELEASE MONITORING:
- Downstream gauge readings
- Tailwater elevation
- Gate position verification
- Flow measurement (if available)
- Visual observation for debris, vortices
```

**FCO-004: Emergency Release Procedures**
```
TRIGGERS:
- Reservoir approaching spillway crest
- Dam safety concern identified
- Downstream emergency requiring flow reduction
- Structural integrity issue
- Earthquake damage assessment

EMERGENCY RELEASE SEQUENCE:
1. Declare emergency internally
2. Notify emergency management agencies
3. Issue immediate public warning (sirens, EAS)
4. Maximize release capacity immediately
5. Coordinate with downstream dam operators
6. Monitor structural response continuously
7. Prepare for potential evacuation

NOTIFICATION PRIORITY:
1. Dam Safety Officer
2. Emergency Management (county, state)
3. National Weather Service
4. Downstream dam operators
5. Law enforcement agencies
6. Media outlets
7. Public warning systems (sirens, reverse 911)

POST-EMERGENCY:
- Document all actions chronologically
- Conduct after-action review
- Inspect all equipment used
- Update Emergency Action Plan as needed
```

**FCO-005: Seasonal Flood Operations**
```
SPRING RUNOFF MANAGEMENT:
- Begin drawdown in March (snow-fed systems)
- Monitor snowpack water equivalent
- Forecast peak runoff timing
- Maximize pre-runoff releases (if safe)
- Coordinate with irrigation districts

STORM EVENT OPERATIONS:
- Monitor weather forecasts 5 days ahead
- Begin precautionary releases 48 hours before storm
- Increase monitoring frequency (hourly or continuous)
- Activate additional operations staff
- Prepare emergency equipment

POST-FLOOD OPERATIONS:
- Resume conservation pool refill
- Inspect spillways, gates, structures
- Remove debris from intakes, gates
- Document high water marks
- Update flood of record data
```

### 1.3 Water Supply Operations

**WSO-001: Municipal Supply Releases**
```
DAILY RELEASES:
- Coordinate with water treatment plants
- Typical release: continuous flow per contract
- Minimum flow: maintain downstream requirements
- Maximum flow: treatment plant capacity
- Quality monitoring: temperature, turbidity

SUPPLY CONTRACTS:
- Annual allocation volume
- Daily maximum and minimum flows
- Seasonal priorities
- Drought curtailment provisions
- Water quality parameters

DROUGHT OPERATIONS:
- Implement allocation reductions per contract
- Prioritize domestic supply over irrigation
- Coordinate with state water resources agency
- Monitor storage projections
- Implement water conservation measures
```

**WSO-002: Irrigation District Operations**
```
IRRIGATION SEASON (Typical: April-September):
1. Meet with districts in March - finalize allocation
2. Begin filling canals in April
3. Daily orders from districts (24-hour advance)
4. Release water per order schedule
5. Measure and document deliveries
6. Coordinate with district operators
7. End season after last delivery

ORDER PROCESSING:
- Districts submit orders by 8AM for next day
- Calculate required gate settings
- Schedule release timing
- Monitor delivery to district headgate
- Document actual delivery vs. ordered

ALLOCATION MANAGEMENT:
- Track cumulative deliveries to each district
- Compare to seasonal allocation
- Alert districts approaching allocation limit
- Implement priority system during shortages
```

**WSO-003: Environmental Flow Requirements**
```
MINIMUM FLOW REQUIREMENTS:
- Federal Energy Regulatory Commission (FERC) license
- State water quality certification
- Endangered Species Act biological opinion
- Tribal water rights agreements

TYPICAL REQUIREMENTS:
- Base flow: year-round minimum (e.g., 50 CFS)
- Ramping rates: maximum change per hour (e.g., 1 ft/hr)
- Temperature: maintain cold water (<18°C) for fish
- Dissolved oxygen: >6 mg/L minimum
- Flow variability: seasonal high flow events

MONITORING & COMPLIANCE:
- Continuous downstream flow measurement
- Water quality monitoring (temp, DO, turbidity)
- Fish passage monitoring (fish ladders, screens)
- Annual compliance reporting to FERC
- Adaptive management adjustments
```

### 1.4 Safety & Surveillance

**SAS-001: Daily Dam Inspections**
```
DAILY WALKDOWN CHECKLIST:
□ Crest and downstream face visual inspection
□ Seepage observation at toe of dam
□ Spillway gates and mechanisms
□ Piezometer readings (if manual)
□ Powerhouse visual and audible inspection
□ Turbine bearing temperatures
□ Generator condition
□ Tailrace area inspection
□ Access road conditions
□ Fencing and security barriers
□ Instrumentation review (automated systems)
□ Any unusual conditions noted

DOCUMENTATION:
- Daily inspection form completed
- Photographs of any anomalies
- Immediate reporting of safety concerns
- Trending of measurements over time
```

**SAS-002: Instrumentation Monitoring**
```
AUTOMATED MONITORING (Real-Time):
- Piezometric levels (seepage pressure)
- Inclinometers (deformation)
- Strain gauges (structural stress)
- Settlement monuments (vertical movement)
- Strong motion accelerometers (seismic)
- Reservoir level and tailwater elevation
- Gate position indicators
- Flow measurements

MANUAL READINGS (Weekly/Monthly):
- Survey monuments (geodetic)
- Weir measurements (seepage flow)
- Visual crack monitoring
- Joint opening measurements

ALARM THRESHOLDS:
- Piezometer: 80% of critical level
- Inclinometer: 0.1 inch movement
- Seepage flow: 50% increase over baseline
- Immediate notification to Dam Safety Officer
```

**SAS-003: Periodic Inspections**
```
FORMAL INSPECTIONS:
- FERC Part 12 Inspection: 5-year cycle (federal dams)
- State Dam Safety Inspection: varies by state (often annual)
- Owner's inspection: annual minimum
- Independent consultant: every 5 years
- Comprehensive evaluation: 10-15 years

INSPECTION SCOPE:
- Structural condition assessment
- Operational functionality testing
- Instrumentation calibration verification
- Emergency equipment testing
- Documentation review
- Regulatory compliance verification

FOLLOW-UP:
- Inspection report within 90 days
- Deficiency prioritization (high/medium/low)
- Corrective action plan development
- Tracking of remediation actions
```

**SAS-004: Earthquake Response**
```
IMMEDIATE POST-EARTHQUAKE (<1 HOUR):
1. Account for all personnel safety
2. Conduct rapid visual inspection of dam
3. Review strong motion accelerometer data
4. Check for obvious damage (cracking, settlement)
5. Inspect spillway gates for operability
6. Verify instrumentation functionality
7. Assess reservoir level and stability
8. Notify Dam Safety Officer immediately

DETAILED INSPECTION (1-24 HOURS):
- Underwater inspection of upstream face
- Detailed structural survey
- Piezometer reading comparison
- Seepage flow measurements
- Gallery inspection (if accessible)
- Powerhouse equipment inspection
- Coordination with structural engineer

LONG-TERM MONITORING:
- Increased instrumentation frequency
- Comparison to pre-earthquake baseline
- Structural analysis if significant motion
- Operational restrictions if necessary
```

---

## 2. Emergency Operations (80+ Patterns)

### 2.1 Dam Safety Emergencies

**DSE-001: Emergency Action Plan Activation**
```
ACTIVATION AUTHORITY:
- Dam Safety Officer
- Operations Manager
- On-call duty officer
- Automatic triggers (instrumentation thresholds)

ACTIVATION LEVELS:
Level 1 - UNUSUAL EVENT: Developing condition, no immediate threat
Level 2 - POTENTIAL FAILURE: Unusual condition with potential threat
Level 3 - IMMINENT FAILURE: Failure highly probable or occurring

LEVEL 1 - UNUSUAL EVENT ACTIONS:
1. Increase monitoring frequency
2. Notify Dam Safety Officer
3. Assess condition with engineers
4. Implement precautionary measures
5. Prepare for escalation if necessary

LEVEL 2 - POTENTIAL FAILURE ACTIONS:
1. Activate Emergency Operations Center (EOC)
2. Notify downstream emergency management
3. Place National Weather Service on standby
4. Prepare for public notification
5. Stage emergency equipment
6. Increase operational staff

LEVEL 3 - IMMINENT FAILURE ACTIONS:
1. Issue immediate evacuation warning
2. Activate Emergency Alert System (EAS)
3. Sound sirens (if available)
4. Notify all downstream communities
5. Attempt emergency measures (if safe)
6. Document all actions continuously
7. Withdraw personnel to safe location
```

**DSE-002: Overtopping Emergency**
```
INDICATORS:
- Reservoir level approaching spillway crest
- Inflow exceeds maximum release capacity
- Spillway gates inoperable
- Extreme precipitation event

IMMEDIATE ACTIONS:
1. Open all available spillway gates to maximum
2. Calculate time to overtopping
3. Notify emergency management agencies
4. Prepare evacuation warning message
5. Attempt emergency measures:
   - Portable pumps if available
   - Sandbag non-critical areas
   - Emergency spillway activation
6. Evacuate non-essential personnel

NOTIFICATION SEQUENCE:
- County Emergency Management: Immediate
- National Weather Service: Immediate
- State Dam Safety Office: Within 15 minutes
- Downstream communities: Within 30 minutes
- FERC (if applicable): Within 1 hour
```

**DSE-003: Internal Erosion/Piping**
```
INDICATORS:
- Sudden increase in seepage flow
- Turbid seepage water
- Sinkholes on dam crest or downstream face
- Piezometer pressure increases
- Material exiting seepage areas

EMERGENCY RESPONSE:
1. Assess magnitude and location
2. Lower reservoir immediately if possible
3. Monitor progression continuously
4. Deploy filter material to seepage exit (if safe)
5. Evaluate structural stability with engineer
6. Prepare for potential evacuation
7. Document progression with photos, video

DECISION CRITERIA:
- Continue monitoring: Stable, low flow increase
- Prepare evacuation: Progressive, increasing turbidity
- Evacuate immediately: Rapid progression, structural movement
```

**DSE-004: Structural Failure**
```
TYPES OF FAILURE:
- Spillway gate failure (sudden release)
- Outlet works failure (uncontrolled release)
- Concrete cracking (progressive or sudden)
- Embankment sliding
- Foundation failure

IMMEDIATE RESPONSE:
1. Assess failure type and extent
2. Estimate time to breach
3. Calculate downstream flood wave
4. Issue immediate evacuation order
5. Activate all notification systems
6. Attempt to reduce reservoir if possible
7. Evacuate dam personnel
8. Continuous monitoring from safe distance

BREACH ANALYSIS:
- Breach formation time estimate
- Peak outflow calculation
- Downstream inundation mapping
- Evacuation zone verification
- Travel time to downstream communities
```

### 2.2 Cybersecurity Incidents

**CSI-001: Malware Detection**
```
INDICATORS:
- Antivirus alerts on HMI or server
- Unusual process execution
- Network scanning detected
- File modifications on SCADA server
- USB device auto-execution blocked

IMMEDIATE RESPONSE:
1. Isolate affected system from network
2. Document screen, system state
3. Notify IT security team
4. Preserve forensic evidence
5. Assess operational impact
6. Implement manual operations if necessary

CONTAINMENT:
- Disable network interfaces on affected systems
- Block malicious IP addresses at firewall
- Scan all other systems on network segment
- Change credentials for affected systems
- Increase monitoring on critical systems

ERADICATION:
- Malware analysis by cybersecurity team
- Clean or reimage affected systems
- Patch vulnerabilities exploited
- Update antivirus signatures
- Restore from known-good backups

RECOVERY:
- Restore services in priority order
- Verify system integrity before reconnection
- Monitor for persistence mechanisms
- Conduct post-incident review
```

**CSI-002: Unauthorized Access Detected**
```
DETECTION METHODS:
- Failed authentication logs
- Access from unusual IP addresses
- After-hours access by unauthorized user
- Commands issued outside normal operations
- Multiple simultaneous sessions

IMMEDIATE RESPONSE:
1. Disable compromised credentials
2. Lock out unauthorized user
3. Review recent commands executed
4. Assess systems accessed
5. Check for data exfiltration
6. Notify security operations center

INVESTIGATION:
- Log review (authentication, commands, file access)
- Correlation with physical access logs
- Interview potentially affected personnel
- Determine entry method
- Identify attacker tools, techniques, procedures

REMEDIATION:
- Force password resets for all users
- Implement multi-factor authentication
- Enhance access controls
- Additional monitoring on affected systems
- Incident report to management, authorities
```

**CSI-003: Ransomware Incident**
```
INDICATORS:
- File extensions changed (.encrypted, .locked)
- Ransom note displayed on screens
- Inability to access files or applications
- Unusual encryption processes running
- Mass file modifications

IMMEDIATE RESPONSE (DO NOT PAY RANSOM):
1. Isolate infected systems immediately
2. Power down if actively encrypting
3. Disconnect backups from network
4. Assess operational impact
5. Switch to manual operations
6. Notify law enforcement (FBI)
7. Engage incident response team

OPERATIONAL CONTINUITY:
- Manual operation of dam controls
- Use of backup control systems (if available)
- Monitoring via analog instruments
- Increased staffing for manual operations
- Communication via phone, radio (not email)

RECOVERY STRATEGY:
- Restore from offline backups
- Rebuild systems from clean media
- Do not reconnect until vulnerabilities patched
- Enhanced monitoring post-recovery
- Lessons learned and procedure updates
```

**CSI-004: SCADA System Failure**
```
FAILURE TYPES:
- Server crash or freeze
- Network communication loss
- HMI unresponsive
- Data historian failure
- Control logic errors

IMMEDIATE RESPONSE:
1. Verify physical process safety
2. Transfer to backup SCADA (if available)
3. Manual control of critical functions
4. Assess scope of failure
5. Increase monitoring frequency
6. Notify management and vendors

MANUAL OPERATIONS:
- Local control panels at equipment
- Manual gate operation (handwheel or portable motor)
- Visual monitoring of water levels
- Phone coordination between operators
- Paper logs for all actions

RESTORATION:
- Troubleshoot with vendor support
- Failover to hot standby system
- Restore from backup if necessary
- Verify data integrity before resuming automation
- Post-incident analysis of root cause
```

### 2.3 Physical Security Incidents

**PSI-001: Intrusion Detection Response**
```
DETECTION METHODS:
- Perimeter alarm activation
- CCTV motion detection
- Security guard observation
- Employee reporting
- Access control badge alert

IMMEDIATE RESPONSE:
1. Dispatch security to location
2. Review CCTV footage
3. Lock down facility if necessary
4. Notify law enforcement
5. Account for all employees
6. Secure critical systems

ASSESSMENT:
- Determine if intrusion is insider or external
- Identify compromised areas
- Check for device placement
- Review access logs
- Secure evidence for investigation

ESCALATION CRITERIA:
- Armed intruder: Law enforcement immediately
- Critical area breach: Shutdown operations if necessary
- Multiple intruders: Request additional law enforcement
- Potential sabotage: Federal authorities notification
```

**PSI-002: Vehicle-Borne Threat**
```
DETECTION:
- Unauthorized vehicle approaching security perimeter
- Vehicle bypassing checkpoint
- Suspicious vehicle behavior
- Threat call received

RESPONSE PROTOCOL:
1. Deploy vehicle barriers if time permits
2. Evacuate personnel from potential blast radius
3. Establish standoff distance (500 feet minimum)
4. Contact law enforcement explosive ordnance disposal (EOD)
5. Do not approach vehicle
6. Prepare for facility evacuation

COORDINATION:
- On-scene incident commander (law enforcement)
- Facility representative
- Bomb squad/EOD team
- Fire department on standby
- Evacuate dam if directed
```

**PSI-003: Suspicious Package/Device**
```
INDICATORS:
- Unattended package in critical area
- Threatening note or warning
- Unusual device appearance
- Wires, timers, antennas visible

RESPONSE PROTOCOL:
1. DO NOT TOUCH OR MOVE PACKAGE
2. Evacuate 300-foot radius minimum
3. Notify law enforcement immediately
4. Preserve scene for investigation
5. Account for all personnel
6. Do not use radios near device (RF hazard)

BOMB THREAT CALL PROCEDURES:
- Keep caller on line, gather information
- Use bomb threat checklist
- Note caller ID, background noises
- Immediate notification to management, law enforcement
- Search procedures only if safe
- Evacuation decision by incident commander
```

---

## 3. Maintenance Procedures (70+ Patterns)

### 3.1 Scheduled Maintenance

**SCM-001: Annual Turbine Overhaul**
```
PRE-OUTAGE PLANNING (3-6 Months Ahead):
- Schedule outage with grid operator
- Order long-lead-time parts
- Contract specialized labor (if needed)
- Develop detailed work plan
- Arrange equipment rentals (cranes, welding)
- Coordinate with other dam operations

OUTAGE EXECUTION (Typical Duration: 2-4 Weeks):
Week 1: Shutdown and disassembly
- De-energize and lockout/tagout
- Drain turbine and draft tube
- Remove generator rotor
- Remove turbine runner and shaft
- Inspect shaft seals, bearings

Week 2-3: Inspection and repairs
- Non-destructive testing (ultrasonic, magnetic particle)
- Runner blade inspection for cavitation, cracks
- Bearing replacement if needed
- Seal replacement
- Wicket gate linkage inspection
- Governor system overhaul

Week 4: Reassembly and testing
- Re-install turbine runner
- Align shaft and bearings
- Install generator rotor
- Refill systems, leak check
- Electrical testing
- Startup and performance testing

POST-OUTAGE:
- Document all work performed
- Update maintenance records
- Conduct performance baseline test
- Lessons learned review
```

**SCM-002: Spillway Gate Maintenance**
```
MONTHLY MAINTENANCE:
- Lubricate bearings, bushings, pins
- Inspect hydraulic hoses, connections
- Test limit switches
- Cycle gates through full range (if conditions permit)
- Visual inspection for corrosion, damage

ANNUAL MAINTENANCE:
- Drain and clean hydraulic reservoir
- Replace hydraulic oil and filters
- Disassemble and inspect hydraulic cylinders
- Load test gate hoisting mechanism
- Paint touch-up on exposed surfaces
- Gear reducer oil change
- Electrical control cabinet inspection

5-YEAR MAJOR MAINTENANCE:
- Cathodic protection system testing (submerged components)
- Underwater inspection by divers
- Structural steel ultrasonic testing
- Seal replacement
- Cable replacement if needed
```

**SCM-003: Generator Maintenance**
```
QUARTERLY MAINTENANCE:
- Stator winding insulation testing (megger test)
- Bearing oil analysis
- Vibration monitoring and trending
- Air gap measurements (between rotor and stator)
- Brush inspection (for wound-rotor machines)
- Cooling system inspection

ANNUAL MAINTENANCE:
- Stator cleaning (compressed air, vacuum)
- Rotor balancing verification
- Bearing replacement or refurbishment
- Winding tightness check
- Ground fault protection testing
- Protective relay calibration

10-YEAR MAJOR REWIND:
- Complete stator rewinding if insulation degraded
- Rotor rewind or replacement
- Core testing for lamination shorts
- Bearing housings refurbishment
- Cooling system replacement
```

### 3.2 Preventive Maintenance

**PRV-001: SCADA System Maintenance**
```
MONTHLY:
- Backup SCADA database
- Review alarm logs for nuisance alarms
- Test communication links
- UPS battery testing
- Software updates review

QUARTERLY:
- Server health check (disk space, memory, CPU)
- Network switch and firewall review
- Redundancy failover test
- Cybersecurity patch assessment

ANNUAL:
- Full system backup and offsite storage
- Disaster recovery drill
- Vendor system health check
- Security vulnerability assessment
- Hardware refresh planning
```

**PRV-002: Instrumentation Calibration**
```
CALIBRATION SCHEDULE:
- Level sensors: Annual
- Flow meters: Bi-annual
- Pressure transmitters: Annual
- Temperature sensors: Bi-annual
- Seismic accelerometers: After each significant event
- Piezometers: Annual (comparison to manual readings)

CALIBRATION PROCEDURE:
1. Isolate instrument from process (if possible)
2. Apply known reference standard
3. Compare instrument reading to standard
4. Adjust if deviation exceeds tolerance
5. Document as-found and as-left values
6. Attach calibration sticker with date, technician
```

**PRV-003: Emergency Equipment Testing**
```
MONTHLY TESTS:
- Diesel generators (30-minute loaded run)
- Emergency lighting systems
- Fire detection and suppression systems
- Communication systems (radios, satellite phones)
- Sump pumps

QUARTERLY TESTS:
- Generator paralleling (if multiple units)
- Automatic transfer switch operation
- Fuel tank inventory and quality
- Battery banks load testing

ANNUAL TESTS:
- Full emergency power load test
- Fuel system cleaning and filter replacement
- Generator protective relays
- Coordination with utility on black start procedures
```

---

## 4. Security Operations (60+ Patterns)

### 4.1 Physical Security Operations

**PSO-001: Access Control Management**
```
DAILY OPERATIONS:
- Verify all access control doors functioning
- Review previous 24 hours access logs
- Investigate any unusual access patterns
- Ensure visitor log complete and accurate

MONTHLY:
- Access rights review (revoke unused access)
- Badge inventory and reconciliation
- Lost/stolen badge follow-up
- Access control system backup

QUARTERLY:
- User access audit (compare to org chart)
- Physical key inventory
- Lock and key replacement program
- Access control system software updates
```

**PSO-002: Perimeter Patrol**
```
SHIFT PATROLS (3x per shift minimum):
- Drive entire perimeter road
- Check fence integrity
- Verify gate locks and chains
- Inspect remote facilities
- Check lighting operational
- Report any discrepancies

PATROL DOCUMENTATION:
- Patrol log entry with time and observations
- Photograph any damage or unusual conditions
- Immediate reporting of security concerns

NIGHT SHIFT EMPHASIS:
- Increased attention to lighting
- Thermal imaging use (if available)
- Coordination with law enforcement patrols
```

**PSO-003: CCTV Monitoring**
```
REAL-TIME MONITORING:
- Central monitoring station staffed during business hours
- Motion detection alerts reviewed immediately
- Cameras aimed at all critical areas
- Recording retention: 90 days minimum

CAMERA COVERAGE AREAS:
- Main gate and entrance
- Perimeter fence line
- Spillway gates
- Powerhouse entrances
- Transformer yard
- Parking areas
- Dock/boat launch areas

MAINTENANCE:
- Weekly camera functionality check
- Monthly lens cleaning
- Quarterly camera repositioning review
- Annual system upgrade assessment
```

**PSO-004: Visitor Management**
```
VISITOR PROCESS:
1. Pre-approval required for all visitors
2. Photo ID verification at gate
3. Visitor badge issuance
4. Escort assignment
5. Safety briefing
6. Restricted area limitations documented
7. Badge return and checkout upon departure

TOUR GROUPS:
- Advanced scheduling (2 weeks minimum)
- Background checks for adult supervisors
- Restricted areas clearly communicated
- Photography policy enforcement
- Group size limits (max 15 people)

CONTRACTOR ACCESS:
- Contractor orientation and safety training
- Work area assignment and restrictions
- Tool and equipment inspection
- Verification of insurance and licenses
- Badging with contractor designation
```

### 4.2 Cybersecurity Operations

**CSO-001: Security Monitoring**
```
DAILY MONITORING:
- Review firewall logs for blocked traffic
- SCADA system authentication logs
- Failed login attempts review
- Antivirus alert review
- Network traffic anomalies

WEEKLY MONITORING:
- Vulnerability scan results
- Security patch status
- Backup verification
- User account review

MONTHLY MONITORING:
- Security metrics report
- Incident trend analysis
- Penetration test scheduling
- Security awareness training completion rates
```

**CSO-002: Patch Management**
```
PATCH ASSESSMENT PROCESS:
1. Vendor security bulletin received
2. Vulnerability severity assessment
3. Applicability to dam systems
4. Impact analysis on operations
5. Patch testing in lab/dev environment
6. Change control board approval
7. Maintenance window scheduling

PATCH DEPLOYMENT:
- CRITICAL (within 30 days): Remote code execution, privilege escalation
- HIGH (within 90 days): Denial of service, information disclosure
- MEDIUM (within 180 days): Low-impact vulnerabilities
- LOW (annual): Minor issues, end-of-support systems

COMPENSATING CONTROLS:
- Network isolation if patching not possible
- Additional monitoring
- Virtual patching (IPS signatures)
- Access restrictions
```

**CSO-003: Backup & Recovery Operations**
```
BACKUP SCHEDULE:
- SCADA server: Daily incremental, weekly full
- Historian database: Daily
- HMI workstations: Weekly
- Network configurations: After each change
- Offline copies: Weekly, stored offsite

RECOVERY TIME OBJECTIVES (RTO):
- Critical: SCADA master server - 4 hours
- Important: Historian, HMI - 8 hours
- Normal: Engineering workstations - 24 hours

RECOVERY POINT OBJECTIVES (RPO):
- Real-time data: 15 minutes (acceptable loss)
- Historian data: 1 hour
- Configuration changes: 24 hours

BACKUP TESTING:
- Monthly: Test restore of one critical system
- Quarterly: Full disaster recovery exercise
- Annual: Complete system restoration drill
```

---

## 5. Environmental Compliance (50+ Patterns)

### 5.1 Water Quality Operations

**WQO-001: Temperature Monitoring**
```
MONITORING LOCATIONS:
- Reservoir surface (epilimnion)
- Mid-depth (thermocline)
- Bottom release depth (hypolimnion)
- Downstream release point
- Tailwater 1 mile downstream

MONITORING FREQUENCY:
- Summer (June-September): Daily
- Spring/Fall: Weekly
- Winter: Monthly

TEMPERATURE REQUIREMENTS:
- Downstream temperature limit: 20°C maximum (typical)
- Allowable delta: 2°C change per hour
- Seasonal variations per biological opinion

OPERATIONAL ADJUSTMENTS:
- Selective withdrawal system operation
- Blending releases from multiple elevations
- Timing releases for coolest part of day
- Coordination with fish biologists
```

**WQO-002: Dissolved Oxygen Management**
```
DO MONITORING:
- Continuous monitoring at release point
- Downstream profiles weekly during summer
- Vertical reservoir profiles monthly

DO REQUIREMENTS:
- Minimum: 6.0 mg/L at release point
- Target: 7.0 mg/L or higher
- Daily averaging permitted

OXYGENATION SYSTEMS:
- Turbine venting (aspirate atmospheric air)
- Weir structures downstream
- Mechanical aerators in tailwater
- Oxygen injection systems (pure O2)

PERFORMANCE MONITORING:
- System efficiency measurement
- Dissolved oxygen uptake rates
- Cost per pound of oxygen added
```

**WQO-003: Total Dissolved Gas (TDG) Management**
```
TDG CONCERNS:
- Spillway entrainment of air
- Deep release from high head
- Gas bubble trauma in fish

MONITORING:
- TDG sensors at spillway tailwater
- Forebay monitoring
- Downstream at 1, 5, 10 miles

LIMITS:
- 110% saturation maximum (typical)
- 115% saturation short-term allowance
- State water quality standards vary

MITIGATION:
- Flip lips on spillways (surface skimming)
- Flow deflectors to reduce plunge depth
- Operating restrictions during high TDG periods
```

### 5.2 Fish Passage Operations

**FPO-001: Upstream Fish Passage**
```
FISH LADDER OPERATION:
- Season: April-October (salmon, steelhead)
- Attraction flow: 5-10% of river flow
- Pool differential: 1 foot per pool
- Velocity: <4 feet per second
- Debris cleaning: Daily during season

FISH COUNTING:
- Video counting systems
- PIT tag detection
- Manual counts (if no automation)
- Data reported to fish agencies

MAINTENANCE:
- Pre-season inspection and cleaning
- Underwater inspection annually
- Attraction flow verification
- Trash rack cleaning
```

**FPO-002: Downstream Fish Passage**
```
SURFACE BYPASS SYSTEMS:
- Operational timing: 24/7 during outmigration
- Flow: 3-5% of total discharge
- Screen mesh: 1-2mm for juvenile salmon
- Monitoring: Video, PIT tags

TURBINE OPERATIONS FOR FISH:
- Screen existing turbine intakes
- Operational windows (day vs. night)
- Load restrictions during outmigration peaks
- Turbine shut-down if needed

SPILL OPERATIONS FOR FISH:
- Voluntary spill for fish passage
- 30-60% spill percentage typical
- Nighttime spill emphasis
- TDG monitoring and limits
```

---

*This operational procedures document provides comprehensive guidance for safe, secure, and compliant dam operations across all operational scenarios and regulatory requirements.*
