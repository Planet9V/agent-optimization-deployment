---
title: "ETCS (European Train Control System) Commissioning Procedure"
category: "operational-procedures"
sector: "transportation"
domain: "rail-signaling"
procedure_type: "commissioning-validation"
safety_critical: true
regulatory_compliance:
  - "ERA ERTMS Baseline 3"
  - "CENELEC EN 50126"
  - "CENELEC EN 50129"
  - "SUBSET-076"
  - "SUBSET-094"
related_systems:
  - "ETCS Level 1"
  - "ETCS Level 2"
  - "ETCS Level 3 (Hybrid)"
  - "Radio Block Centre (RBC)"
  - "Eurobalise"
  - "GSM-R"
revision: "1.0"
date: "2025-11-05"
author: "Transportation Operations Team"
keywords:
  - ETCS-commissioning
  - ERTMS
  - train-control-system
  - eurobalise
  - RBC
  - onboard-equipment
---

# ETCS (European Train Control System) Commissioning Procedure

## Overview and Purpose

The European Train Control System (ETCS) is the signaling and train control component of the European Rail Traffic Management System (ERTMS), designed to enable seamless cross-border rail operations across Europe and increasingly deployed worldwide. ETCS commissioning is the critical process of validating that installed ETCS equipment meets safety specifications, operates according to approved logic, and integrates correctly with existing railway infrastructure and operations.

This procedure covers commissioning of ETCS installations across three application levels:

**ETCS Level 1:** Spot transmission via Eurobalises, with continuous supervision using onboard equipment
**ETCS Level 2:** Continuous radio-based communication between trains and Radio Block Centre (RBC), eliminating most trackside signals
**ETCS Level 3/Hybrid Level 3:** Train integrity monitoring enabling virtual blocks and increased capacity without additional infrastructure

The commissioning process validates:
- Safety integrity (SIL 4) of all ETCS components
- Correct operation according to ERTMS specifications (Baseline 3 Release 2 current standard)
- Integration with existing signaling infrastructure (interlocking, signals, track circuits)
- Radio communication system performance (GSM-R or future FRMCS)
- Onboard equipment functionality and driver interface usability
- Eurobalise positioning and data content accuracy
- Interoperability across railway networks and national borders

ETCS commissioning requires meticulous attention to detail, extensive testing under diverse scenarios, and rigorous documentation for regulatory approval. This procedure provides comprehensive guidance for commissioning engineers, test coordinators, and railway authorities.

## Prerequisites and Safety Requirements

### Personnel Qualifications

ETCS commissioning requires highly specialized multidisciplinary teams:

**ETCS Commissioning Engineer (Lead):**
- Professional railway signal engineer with minimum 7 years experience
- ETCS-specific training and certification (ERA-approved training program)
- Thorough understanding of ERTMS specifications (SUBSET-026, SUBSET-036, SUBSET-076)
- Experience with specific ETCS vendor system (Alstom Atlas, Siemens Trainguard, Hitachi, Thales)
- Radio communication systems knowledge (GSM-R, GPRS, FRMCS)
- Project management certification for complex commissioning programs
- Authorization to approve safety-critical system commissioning

**ETCS Test Engineers (2-3 minimum):**
- Railway signaling engineering degree or equivalent
- ETCS theory and application training (minimum 80 hours formal training)
- Hands-on experience with ETCS test equipment and procedures
- Familiarity with diagnostic tools (RBC monitoring, Eurobalise programmers)
- Radio frequency (RF) measurement and troubleshooting skills
- Train operations knowledge for realistic operational scenario testing

**Train Driver/Operator Representatives:**
- Qualified train drivers with ETCS operational training
- Minimum 1000 hours experience operating ETCS-equipped trains
- Understanding of Driver Machine Interface (DMI) operation and interpretation
- Ability to provide operational feedback during commissioning
- Current certification for route being commissioned

**Railway Operations Coordinator:**
- Railway traffic controller or operations manager
- Understanding of operational implications of ETCS commissioning
- Authority to coordinate test trains and traffic management during commissioning
- Communication liaison between commissioning team and operations center

**Independent Safety Assessor:**
- Qualified independent safety assessor (ISA) per EN 50129
- Not involved in system design or installation (independence requirement)
- Experience with ETCS safety case validation
- Authority to approve or reject commissioning based on safety criteria

### Safety Prerequisites

**Possession and Protection:**
- Formal possession order for track sections being commissioned
- All regular traffic suspended or operating under special procedures
- Protection established at limits of ETCS commissioning zone
- Adjacent tracks protected with speed restrictions where ETCS interfaces exist
- Emergency communication procedures established with all test trains

**System Integration Status:**
- ETCS trackside equipment installation 100% complete and factory tested
- Interlocking system integration tested and verified
- Power supply systems operational with backup power confirmed
- Communication systems (GSM-R) network operational and coverage verified
- Existing signaling systems operational (for fallback during commissioning)
- All software versions documented and approved (trackside and onboard)

**Test Train Preparation:**
- Test train equipped with certified ETCS onboard equipment
- Onboard equipment software version matches trackside compatibility
- DMI fully functional with data recording capability
- Train-to-shore radio communication operational (GSM-R or test radio)
- Juridical Recording Unit (JRU) operational for complete data logging
- Emergency communication equipment operational (radio, GSM-R cab radio)

**Documentation Readiness:**
- ETCS engineering design approved and current
- Eurobalise positioning plans with telegrams defined
- RBC logic tables reviewed and approved
- Interlocking interface specifications documented
- Hazard log and safety case current and accepted
- Commissioning test specifications approved by railway authority

**Environmental and Operational Conditions:**
- Weather suitable for safe test train operations
- Visibility adequate for visual verification (if required)
- Electromagnetic environment assessed (no excessive EMI affecting GSM-R or balises)
- Coordination with adjacent railway operations to prevent interference

### Required Equipment and Tools

**ETCS Test Equipment:**
- **Eurobalise Programmer:** Device for programming and verifying Eurobalise telegram content
- **Balise Test Transmission Module (BTM) Analyzer:** Verifies telegram reception by onboard equipment
- **RBC Monitoring Workstation:** Real-time monitoring of RBC-train communication and logic
- **GSM-R Radio Test Equipment:** Radio analyzer, spectrum analyzer, field strength meter
- **DMI Simulator:** For testing onboard equipment responses without train movement
- **Juridical Recording Unit (JRU) Reader:** Retrieves and analyzes recorded data from test trains

**Communication Test Equipment:**
- **GSM-R Mobile Station:** Handheld GSM-R radio for communication testing
- **Radio Coverage Mapping Equipment:** GPS-enabled field strength measurement system
- **Protocol Analyzer:** Captures and decodes ETCS-GSM-R data packets
- **Network Quality Tester:** Measures latency, packet loss, and handover performance

**Measurement Instruments:**
- **GPS Receiver:** High-precision positioning for verifying Eurobalise locations (±1 meter accuracy)
- **Laser Distance Meter:** Verification of physical distances (balise spacing, signal placement)
- **Oscilloscope:** Troubleshooting of electrical interfaces (100 MHz bandwidth minimum)
- **Spectrum Analyzer:** Radio frequency analysis (covering GSM-R band 876-880/921-925 MHz)

**Documentation Equipment:**
- **Laptop Computers:** Running ETCS diagnostic software, data analysis tools, test management software
- **Data Loggers:** Automated recording of test results synchronized with GPS time
- **Video Recording Equipment:** Dashboard cameras for visual documentation of test runs
- **Digital Cameras:** High-resolution photography of equipment and installations
- **Tablets:** Electronic checklists and real-time data entry during field testing

**Safety and Communication:**
- **Railway Radio Equipment:** GSM-R cab radios, handheld radios, spare batteries
- **PPE:** Hi-visibility clothing, safety helmets, safety boots, hearing protection, safety glasses
- **Emergency Equipment:** First aid kit, fire extinguisher, emergency lighting, detonators/track protection devices
- **Mobile Phones:** Backup communication independent of railway systems

## Step-by-Step Commissioning Procedure

### Phase 1: Pre-Commissioning Verification (3-5 days)

**Step 1: Documentation Review and Validation**
- Assemble complete ETCS engineering package:
  - System Requirements Specification (SRS) approved by railway authority
  - ETCS Functional Requirements Specification (FRS) per SUBSET-026
  - Eurobalise layout and telegram content (SUBSET-036, SUBSET-044)
  - RBC configuration and logic tables
  - Interlocking interface specifications and safety case
  - Hazard log with all identified hazards addressed and risk mitigated to acceptable levels
- Review approval documentation:
  - Design approval certificate from railway authority (ERA or national safety authority)
  - Type approval certificates for all ETCS equipment (onboard, trackside, RBC)
  - Software version authorization (only approved software deployed)
  - Safety case acceptance by independent safety assessor
- Cross-check consistency between documents:
  - Verify Eurobalise locations match approved engineering drawings
  - Confirm RBC logic reflects approved interlocking interfaces
  - Validate onboard equipment configuration matches approved application

**Step 2: Physical Installation Verification**
- Inspect Eurobalise installations:
  - Confirm each balise location matches engineering specification (GPS verification ±0.5m)
  - Verify balise orientation correct (transmission uplink antenna toward onboard equipment)
  - Check physical mounting secure (resistance to vandalism and track maintenance equipment)
  - Inspect cable routing and protection (mechanical protection from ballast and maintenance)
  - Verify balise identification labels present and match documentation
  - Photograph each balise installation from multiple angles (include milepost markers in photos)
- Inspect Lineside Electronic Unit (LEU) installations (Level 1):
  - Verify LEU cabinet location per design (typically near interlocking or signal location)
  - Check LEU-to-balise cable connections secure and properly terminated
  - Confirm power supply operational (measure voltage at LEU terminals)
  - Verify interlocking interface connections per approved design
  - Test LEU diagnostic indicators and alarm functions
- Inspect Radio Block Centre (RBC) installation (Level 2/3):
  - Verify RBC server hardware installed and operational
  - Confirm network connectivity to GSM-R base stations
  - Validate interlocking interface connections (data links, vital communication protocols)
  - Check backup power and redundant server failover (test automatic switchover)
  - Verify environmental controls (HVAC, fire suppression) operational

**Step 3: Communication System Verification**
- Test GSM-R network coverage along commissioned route:
  - Drive route with GSM-R radio field strength measurement equipment
  - Record received signal strength at 10-meter intervals (minimum -95 dBm required)
  - Identify coverage gaps or weak spots requiring attention
  - Test handover zones between GSM-R base stations (handovers should complete <5 seconds)
  - Verify GSM-R emergency communication functions (functional addressing, priority calls)
- Test RBC-to-GSM-R interface:
  - Verify RBC can establish connections to GSM-R base stations
  - Test data throughput and latency (packet transit time <500ms typical)
  - Verify GPRS data connection stability (no unexpected disconnections)
  - Test RBC behavior during GSM-R network faults (should maintain safe state)
- Document baseline communication performance:
  - Record signal strength profile along entire route
  - Document handover locations and timing
  - Identify any EMI sources affecting communication quality

**Step 4: Eurobalise Programming and Verification**
- Program each Eurobalise with approved telegram content:
  - Connect Eurobalise programmer to LEU or balise directly
  - Upload telegram data per SUBSET-036 specification
  - Verify checksum and packet integrity
  - Document balise identity, telegram version, and programming date
- Verify telegram content correctness:
  - Compare programmed content to engineering specification
  - Verify linking information correct (distance to next balise, signal, point)
  - Confirm national values appropriate for country/railway (varies by jurisdiction)
  - Check speed restrictions, gradient profiles, and temporary speed restrictions if pre-programmed
- Test Eurobalise transmission:
  - Use BTM analyzer to read telegram from balise (simulates onboard equipment)
  - Verify telegram readable at specified train speeds (up to maximum line speed)
  - Check consistency of multiple reads (should be identical across 10+ reads)
  - Test at various heights above balise (account for different bogie heights)
- Create Eurobalise installation database:
  - Record GPS coordinates of each balise (latitude, longitude, altitude)
  - Document telegram content and version
  - Photograph balise and record physical condition
  - Generate report with all balise verification data

**Step 5: RBC Configuration and Logic Verification**
- Load approved RBC configuration:
  - Import interlocking interface data (track layout, signal locations, routes)
  - Configure RBC logic per approved specification
  - Verify national values appropriate for area (varies by country)
  - Load train data configuration (train categories, braking characteristics)
- Test RBC internal logic using simulation mode:
  - Simulate train movements through all possible routes
  - Verify movement authorities (MA) generated correctly for each scenario
  - Test gradient profiles and speed restrictions included in MA
  - Confirm RBC respects interlocking route locks and track circuit occupancy
  - Verify emergency stop functionality (all trains receive immediate RBC emergency stop command)
- Test RBC-to-interlocking interface:
  - Simulate interlocking route requests from RBC
  - Verify interlocking responds correctly (grants or rejects routes based on track conditions)
  - Test track circuit status reporting from interlocking to RBC
  - Confirm RBC receives signal aspect information correctly
  - Test failure scenarios (loss of interlocking communication should cause RBC to fail-safe)

### Phase 2: Static Testing (5-7 days)

**Step 6: Onboard Equipment Bench Testing**
- Test ETCS onboard equipment with stationary train:
  - Power up onboard equipment and verify startup sequence correct
  - Test DMI functionality (all display elements operational, touchscreen responsive)
  - Verify JRU recording (data being logged correctly with accurate timestamps)
  - Test odometry system calibration (if required before commissioning)
- Conduct DMI usability assessment:
  - Present various operational scenarios on DMI
  - Confirm information display clear and unambiguous
  - Verify color coding, symbols, and text meet standards (SUBSET-091)
  - Obtain feedback from train driver representatives
  - Document any display issues for resolution
- Test onboard equipment interfaces:
  - Verify interface to train braking system (brake commands executed correctly)
  - Test traction cut-off interface (train power removed when required by ETCS)
  - Confirm train data entry (driver can enter train category, length, speed capability)
  - Verify ETCS mode transitions (from Standby to Full Supervision to Staff Responsible, etc.)

**Step 7: Level 1 Static Testing (Eurobalise Read Testing)**
- Position test train over Eurobalise:
  - Align BTM antenna directly over balise (typically ±0.5m lateral tolerance)
  - Verify onboard equipment receives and decodes telegram
  - Check DMI displays balise information (if configured to display)
  - Verify JRU records balise telegram with GPS position
- Test balise read consistency:
  - Read same balise 20 times without moving train
  - Verify all reads produce identical results (100% consistency required)
  - Document any read failures or corrupted telegrams
  - If failures occur, check balise transmission power, antenna alignment, electromagnetic environment
- Test balise read at various train positions:
  - Position train at multiple lateral offsets (track centerline ±1.5m)
  - Verify balise readable across full range of train positions
  - Document minimum and maximum read distance/position
- Test balise read in adverse conditions:
  - Test with train at various heights (simulate different loading conditions)
  - Test with wet rails (water should not significantly affect transmission)
  - Test with ice/snow if environmental conditions allow

**Step 8: Level 2 Static Testing (RBC Communication Testing)**
- Establish RBC communication session:
  - Power up onboard equipment with GSM-R radio active
  - Initiate RBC session manually (driver enters RBC phone number)
  - Verify RBC session establishment (onboard equipment registers with RBC)
  - Confirm DMI displays RBC connection status
- Test RBC-train message exchange:
  - Verify Movement Authority (MA) received from RBC
  - Confirm onboard equipment acknowledges messages correctly
  - Test position reporting from train to RBC (periodic updates per SUBSET-037)
  - Verify MA updates in response to simulated track condition changes (RBC shortens or extends MA)
- Test RBC session robustness:
  - Simulate temporary loss of GSM-R coverage (disconnect radio link)
  - Verify onboard equipment behavior (should maintain safe braking curve, sound alarm)
  - Restore radio link and verify session re-establishment
  - Test RBC session handover (moving between RBC areas if applicable)
- Test emergency scenarios:
  - Trigger RBC emergency stop command
  - Verify onboard equipment applies emergency brake immediately (<1 second response)
  - Test revocation of emergency stop (train can resume after acknowledgment)

### Phase 3: Dynamic Testing (10-15 days)

**Step 9: Low-Speed Dynamic Testing (up to 40 km/h)**
- Conduct initial test runs at low speed:
  - Test train operates in ETCS Full Supervision mode
  - Verify Eurobalises readable at low speeds (20-40 km/h)
  - Confirm onboard equipment processes telegrams correctly (DMI updates as expected)
  - Test braking curves displayed correctly on DMI
  - Verify speed supervision functions (warning and braking interventions at preset test points)
- Test specific operational scenarios:
  - Approach signal at danger (verify ETCS enforces stop before signal)
  - Test temporary speed restrictions (TSR) enforcement
  - Verify point machine position detection (via balise or RBC)
  - Test gradient profile supervision (uphill vs. downhill braking)
- Document low-speed test results:
  - JRU data downloaded and analyzed after each test run
  - Speed profiles, brake applications, DMI events recorded
  - Comparison to expected behavior documented
  - Any anomalies investigated immediately before proceeding to higher speeds

**Step 10: Medium-Speed Dynamic Testing (40-120 km/h)**
- Conduct progressive speed increase:
  - Gradually increase test speeds in 20 km/h increments
  - Re-test all operational scenarios at each speed increment
  - Verify balise read reliability at higher speeds (should remain 100%)
  - Test brake curve calculations at higher speeds (more critical due to longer stopping distances)
- Test braking intervention scenarios:
  - Overspeed by 5 km/h and verify warning intervention (audible alarm, visual indication)
  - Overspeed by 10+ km/h and verify service brake intervention
  - Continue overspeeding and verify emergency brake intervention if service brake insufficient
  - Confirm brake release when speed back within permitted limits
- Test Mode Profile enforcement:
  - Verify mode transitions at designated locations (Full Supervision to Staff Responsible at station platform, etc.)
  - Test reversible sections (bidirectional operation) if applicable
  - Verify level crossings protected (train cannot exceed speed limit approaching crossing until gates confirmed down)
- Test radio communication stability at speed:
  - Monitor GSM-R link quality during movement
  - Verify MA updates received without delay during movement
  - Test handovers between GSM-R cells at operational speeds (should be seamless)

**Step 11: High-Speed Dynamic Testing (120+ km/h up to maximum line speed)**
- Conduct full-speed testing:
  - Test at maximum authorized line speed for ETCS-equipped route
  - Verify all ETCS functions operate correctly at maximum speed
  - Test emergency braking from maximum speed (verify braking distances within safe margins)
  - Confirm balise read reliability at maximum speed (acceptance: >99.9% successful reads)
- Test worst-case scenarios:
  - Emergency stop from maximum speed (full service brake then emergency brake application)
  - Rapid MA shortening (RBC suddenly reduces MA due to track occupation ahead)
  - Unexpected radio dropout at high speed (train should coast down under onboard supervision)
  - Multiple consecutive speed restrictions (verify smooth braking to comply with each restriction)
- Test high-speed operational scenarios:
  - Approach stations at high speed with station stop enforcement
  - Test speed increase after restriction lifted (verify ETCS permits acceleration)
  - Verify tunnel operation (radio communication maintained in tunnels)
  - Test platform overshoot prevention (if configured)

**Step 12: Integrated System Testing (All Levels and Modes)**
- Test ETCS level transitions:
  - Transition from Level 1 to Level 2 (typically at balise marked as level transition point)
  - Verify seamless transition without loss of supervision
  - Test reverse transition (Level 2 to Level 1, Level 2 to Level 0 for unfitted areas)
  - Verify appropriate DMI indications and driver acknowledgments
- Test ETCS mode transitions:
  - Full Supervision to Shunting Mode (for low-speed yard movements)
  - Full Supervision to Staff Responsible (when ETCS temporarily not available)
  - Standby to Full Supervision (at start of journey)
  - Test all National Trip mode (failure mode requiring staff assistance)
- Test degraded mode operations:
  - Simulate RBC failure (onboard switches to balise-based supervision or limited supervision)
  - Test operation with DMI partially failed (backup display functional)
  - Simulate balise failure (onboard uses dead reckoning between balises)
  - Verify driver override procedures (only allowed under specific conditions)
- Test complex operational scenarios:
  - Train following another train closely (verify safe separation maintained)
  - Multiple trains on same route (RBC manages multiple MA without conflict)
  - Train reversing direction (if applicable)
  - Coupling/uncoupling trains (ETCS data transfer between coupled units)

### Phase 4: Integration with Existing Systems (7-10 days)

**Step 13: Interlocking Integration Validation**
- Test all interlocked routes with ETCS:
  - For each route, verify ETCS issues correct MA
  - Confirm route locking prevents conflicting movements
  - Test approach locking (ETCS enforces stopping distance)
  - Verify overlap protection (ETCS includes overlap in braking calculations)
- Test interlocking failure scenarios:
  - Simulate loss of interlocking communication to RBC
  - Verify ETCS defaults to safe state (restrictive MA or no MA issued)
  - Test restoration of interlocking communication (ETCS resumes normal operation)
  - Verify fail-safe interlocking behavior reflected in ETCS MA
- Test points (switches) under ETCS control:
  - Verify RBC receives point position correctly from interlocking
  - Test diverging routes (ETCS enforces correct speed for point position)
  - Confirm point not movable while train approaching under ETCS supervision
  - Test point failure detection (ETCS should prevent movement over failed point)

**Step 14: Conventional Signal Integration**
- Test ETCS operation with existing signal displays (Level 1 or hybrid systems):
  - Verify ETCS supervision matches signal aspect (onboard speed limits match signal indication)
  - Test signal aspect changes during train approach (ETCS dynamically updates supervision)
  - Confirm signal-passed detection (used for approach locking and block clearing)
- Test Level 1 operation in fully signaled territory:
  - Verify each balise conveys information equivalent to signal aspect
  - Test fallback to conventional signals if ETCS fails (driver operates by visual signals)
  - Verify ETCS does not contradict signal display (no conflicts between ETCS and signals)
- Test Level 2 Dark Territory (no lineside signals):
  - Verify drivers can operate solely by DMI indications
  - Test driver confidence operating without visual signal references
  - Confirm all necessary information displayed on DMI (speed limits, distance to target, mode indicators)

**Step 15: Level Crossing Integration** (if applicable)
- Test level crossing protection with ETCS:
  - Verify ETCS enforces approach speed ensuring gates down before train arrival
  - Test level crossing failure scenarios (gates fail to lower)
  - Confirm ETCS prevents train proceeding if crossing not protected
  - Verify crossing obstacle detection triggers ETCS braking
- Test level crossing priority handling:
  - Verify priority given to trains over road traffic
  - Test multiple trains approaching crossing in quick succession
  - Confirm crossing closure time optimized (minimize road traffic delay while ensuring train safety)

**Step 16: Adjacent Track Protection** (for multi-track installations)
- Test ETCS operation on multiple parallel tracks:
  - Verify ETCS on each track operates independently
  - Test scenarios where work ongoing on adjacent track (ETCS enforces speed restrictions)
  - Confirm trains on different tracks do not interfere with each other's ETCS operation
- Test GSM-R handover between adjacent tracks:
  - Verify GSM-R handoff correct when trains pass each other
  - Test radio interference mitigation (multiple trains on different tracks using GSM-R simultaneously)

### Phase 5: Performance Validation and Optimization (5-7 days)

**Step 17: Performance Metrics Collection**
- Measure and document ETCS system performance:
  - Balise read success rate (target: >99.9%)
  - RBC message delivery latency (target: <500ms)
  - GSM-R handover success rate (target: 100%)
  - Position reporting accuracy (target: ±5 meters)
  - Brake intervention response time (target: <1 second from overspeed detection)
- Collect statistical data over multiple test runs:
  - Run minimum 50 test trains over full commissioned route
  - Document all anomalies, failures, and performance issues
  - Calculate mean time between failures (MTBF) and compare to specification
  - Identify any systematic issues requiring correction
- Analyze JRU data for comprehensive performance review:
  - Extract all recorded events (brake applications, balise reads, mode transitions)
  - Identify patterns or trends indicating potential issues
  - Compare actual vs. expected behavior across all scenarios
  - Generate performance report for railway authority review

**Step 18: Driver Human-Machine Interface (HMI) Validation**
- Conduct formal DMI usability testing:
  - Train drivers operate system under supervision
  - Collect driver feedback on DMI clarity and usability
  - Identify any confusing or ambiguous displays
  - Test driver response time to ETCS alerts (should acknowledge within 3-5 seconds)
- Validate driver training effectiveness:
  - Test drivers on ETCS operational procedures without reference materials
  - Verify drivers understand all DMI indications and modes
  - Test driver response to failure scenarios (degraded modes, emergency situations)
  - Confirm drivers confident operating ETCS independently
- Document driver feedback and recommendations:
  - Compile driver comments and suggestions
  - Identify any required DMI configuration changes
  - Plan additional driver training if knowledge gaps identified
  - Obtain formal driver acceptance signatures

**Step 19: System Optimization**
- Optimize ETCS parameters for operational efficiency:
  - Adjust braking curves for optimal balance between safety and operational fluidity
  - Optimize RBC track description (gradients, speed restrictions) for smooth operation
  - Fine-tune temporary speed restriction (TSR) handling
  - Optimize MA extension/shortening logic to minimize unnecessary braking
- Optimize GSM-R radio performance:
  - Adjust base station power levels for optimal coverage
  - Optimize handover parameters to minimize handover failures
  - Configure QoS (Quality of Service) parameters for ETCS data priority
- Optimize Eurobalise positioning if issues identified:
  - Relocate balises if read reliability below target
  - Adjust balise transmission power if necessary
  - Re-program balise linking information if distances incorrect

### Phase 6: Final Acceptance and Documentation (3-5 days)

**Step 20: Independent Safety Assessment**
- Independent Safety Assessor (ISA) reviews all commissioning evidence:
  - Complete review of test results and JRU data
  - Verification all hazards in hazard log adequately addressed
  - Confirmation all non-conformances resolved or accepted with justification
  - Review of driver training records and competency assessments
- ISA witnesses final acceptance test runs:
  - ISA rides test trains to observe ETCS operation firsthand
  - ISA verifies operational procedures followed correctly
  - ISA confirms system behavior safe and compliant with standards
- ISA prepares safety assessment report:
  - Documents all findings and recommendations
  - Provides formal acceptance or rejection recommendation
  - Identifies any conditions or limitations for operational use
  - Issues safety certificate if system acceptable for operational service

**Step 21: Regulatory Authority Acceptance**
- Prepare comprehensive commissioning report package:
  - Executive summary of commissioning program and results
  - Detailed test results for all commissioning phases
  - JRU data analysis and performance statistics
  - Driver feedback and HMI validation results
  - ISA safety assessment report and recommendations
  - Updated hazard log with all residual risks documented
  - Configuration management documentation (all versions and checksums)
- Submit commissioning package to railway authority (ERA or national safety authority):
  - Allow sufficient review time (typically 30-60 days)
  - Respond to any questions or requests for clarification
  - Provide additional testing if requested
- Obtain formal operational authorization:
  - Railway authority issues authorization for operational use
  - Authorization may include conditions or restrictions
  - Document authorization number and effective date
  - Distribute authorization to all relevant stakeholders

**Step 22: Operational Handover**
- Conduct operational handover briefing:
  - Brief railway operations management on ETCS capabilities and limitations
  - Review operational procedures and fallback procedures
  - Establish ongoing support arrangements (maintenance, troubleshooting)
  - Provide contact information for ETCS technical support
- Transition to operational maintenance:
  - Hand over system documentation to maintenance organization
  - Train maintenance personnel on ETCS-specific maintenance procedures
  - Establish preventive maintenance schedule
  - Configure remote monitoring and diagnostic systems
- Document lessons learned:
  - Compile lessons learned from commissioning program
  - Identify procedure improvements for future projects
  - Document any design issues requiring attention in future installations
  - Share knowledge with commissioning teams on other projects

## Required Tools and Equipment Summary

### ETCS-Specific Test Equipment
- **Eurobalise Programmer:** Alstom BlisCheck, Siemens Balise Programming Device, or equivalent
- **BTM Analyzer:** Captures and decodes Eurobalise telegrams as received by onboard equipment
- **RBC Monitoring Console:** Real-time visualization of RBC logic and train positions
- **JRU Reader/Analyzer:** Bombardier/Alstom, Siemens, or Thales JRU data extraction tools
- **DMI Simulator:** Simulates onboard equipment for testing trackside installations without trains

### Radio Communication Test Equipment
- **GSM-R Test Mobile:** Certified GSM-R device for communication testing
- **Spectrum Analyzer:** Covering 876-880 MHz (uplink) and 921-925 MHz (downlink) GSM-R bands
- **Drive Test System:** RF coverage mapping with GPS synchronization
- **Protocol Analyzer:** Wireshark with GSM-R/GPRS decoding capabilities

### Measurement and Positioning
- **High-Precision GPS:** Survey-grade GPS receiver (±0.1m accuracy for balise positioning)
- **Laser Distance Meter:** Long-range (up to 200m) for infrastructure measurements
- **Odometry Calibration Equipment:** For calibrating train odometry systems

## Personnel Requirements Summary

### Core Commissioning Team
- **1x ETCS Commissioning Engineer (Lead):** Overall program management and technical authority
- **2-3x ETCS Test Engineers:** Execute test procedures, analyze data, troubleshoot issues
- **1x Independent Safety Assessor:** Independent safety verification and approval authority
- **2x Train Drivers (ETCS-qualified):** Operate test trains, provide operational feedback
- **1x Railway Operations Coordinator:** Coordination with traffic control and operations management

### Support Personnel (part-time involvement)
- **Interlocking Engineer:** Support interlocking integration testing
- **Radio Communication Engineer:** Support GSM-R network verification and optimization
- **Maintenance Engineers:** Training and handover preparation
- **Quality Assurance Auditors:** Verify procedure compliance and documentation quality

### Training Requirements
- **ETCS System Training:** Manufacturer-specific training (5-10 days) covering theory and hands-on
- **ERTMS Specifications Training:** Understanding of SUBSET-026, SUBSET-036, SUBSET-037 (3-5 days)
- **Safety Case Development:** For ISA and lead engineer (2-3 days)
- **Driver Training:** ETCS operational training including normal and degraded modes (3-5 days)

## Troubleshooting Common Issues

### Eurobalise Read Failures
**Symptoms:** Onboard equipment fails to read balise telegrams, intermittent reads, corrupted data
**Likely Causes:**
- Physical obstruction between BTM antenna and balise (debris, ice, snow)
- Balise misalignment or incorrect orientation
- Insufficient balise transmission power
- BTM antenna failure or misalignment on train
- Electromagnetic interference (EMI) from traction power or other sources

**Troubleshooting Steps:**
1. Visually inspect balise and surrounding area (remove any debris or obstructions)
2. Verify balise orientation correct (antenna facing upward toward train)
3. Test balise with portable BTM analyzer (verifies balise transmitting correctly)
4. Measure BTM antenna position on test train (verify within specification)
5. Check for EMI sources (power lines, traction substations, radio transmitters)
6. Replace suspect balise or BTM antenna if hardware failure suspected
7. Reprogram balise with increased transmission power if allowed by specification

### RBC Communication Session Failures
**Symptoms:** Onboard equipment cannot establish RBC session, session drops unexpectedly
**Likely Causes:**
- GSM-R network coverage gaps or weak signal strength
- RBC server overload or malfunction
- GSM-R SIM card issues (incorrect configuration, expired subscription)
- Network congestion during peak usage
- Firewall or network routing issues

**Troubleshooting Steps:**
1. Verify GSM-R signal strength adequate (minimum -95 dBm, preferred -85 dBm or better)
2. Test GSM-R voice call to confirm basic network connectivity
3. Check RBC server status (CPU load, network interfaces, active sessions)
4. Verify GSM-R SIM card correctly provisioned (IMSI, phone number, data APN)
5. Test from different location to isolate coverage vs. RBC issue
6. Review GSM-R network logs for connection rejections or timeouts
7. Check firewalls and IP routing between RBC and GSM-R base stations
8. Contact GSM-R network operator if network issue suspected

### Incorrect Movement Authority (MA) from RBC
**Symptoms:** MA shorter than expected, MA extends beyond safe limits, MA does not update as expected
**Likely Causes:**
- RBC logic configuration error
- Incorrect interlocking interface data (wrong track circuit status)
- RBC train position error (RBC thinks train at different location than actual)
- Timing issue (MA generated based on outdated track status)

**Troubleshooting Steps:**
1. Review RBC monitoring console showing train position and MA calculations
2. Verify train position accurate (compare GPS position to RBC position estimate)
3. Check track circuit status reported to RBC (should match actual track occupancy)
4. Review RBC logic tables for errors in track description or MA calculation
5. Test similar scenario in RBC simulator (isolate logic vs. interface issue)
6. Verify interlocking route correctly granted to RBC
7. Check RBC timing and synchronization (timestamps should be accurate)
8. Review RBC software version (may be known defect requiring update)

### DMI Display Issues or Driver Confusion
**Symptoms:** DMI shows unexpected information, drivers misinterpret displays, DMI freezes or goes blank
**Likely Causes:**
- DMI software defect or incorrect configuration
- Onboard equipment processing error
- Driver training gap (misunderstanding of ETCS operation)
- Ambiguous display design (unclear symbology or color coding)

**Troubleshooting Steps:**
1. Reproduce issue and document exactly what displayed and driver expectation
2. Review JRU data to understand onboard equipment state when issue occurred
3. Compare DMI display to SUBSET-091 specification (DMI standard)
4. Test in simulator to isolate DMI vs. operational context issue
5. Obtain feedback from multiple drivers (individual vs. systematic issue)
6. Review onboard equipment configuration for DMI customization errors
7. Update DMI software if known defect
8. Provide additional driver training if misunderstanding identified

### Speed Supervision Failures (unwanted brake interventions or failure to intervene)
**Symptoms:** ETCS brakes train unnecessarily, ETCS fails to brake when overspeed
**Likely Causes:**
- Incorrect braking curve parameters (overly conservative or optimistic)
- Odometry error (train position or speed inaccurate)
- Gradient profile error in track description
- Adhesion conditions not accounted for (wet rails, leaves on line)
- Software defect in braking calculations

**Troubleshooting Steps:**
1. Analyze JRU data showing speed, permitted speed, and brake interventions
2. Verify odometry calibration correct (compare GPS speed to odometry speed)
3. Check gradient profile in RBC or balise data (should match actual gradients)
4. Review braking parameters (deceleration rates, safety margins, brake build-up time)
5. Test in similar conditions to reproduce issue
6. Adjust braking parameters if within allowed limits
7. Report to manufacturer if software defect suspected
8. Implement operational workaround (temporary speed restriction) if safety issue

## Documentation Requirements

### Commissioning Report Package Contents

**Volume 1: Executive Summary**
- Project overview and scope
- Commissioning schedule and milestones
- Summary of test results and acceptance status
- Key performance metrics achieved
- Regulatory approvals obtained
- Recommendations and lessons learned

**Volume 2: Technical Documentation**
- ETCS system design description
- Eurobalise layout and telegram content database
- RBC configuration and logic tables
- Interlocking interface specifications
- GSM-R network configuration and coverage maps
- Software and firmware version register

**Volume 3: Test Results**
- Detailed test procedures and results for all commissioning phases
- JRU data analysis with performance statistics
- Balise read success rates and coverage
- RBC communication performance metrics
- Braking tests and speed supervision validation
- Integration test results (interlocking, signals, level crossings)

**Volume 4: Safety and Compliance**
- Hazard log with risk assessments and mitigations
- Independent Safety Assessment report
- Regulatory authority approvals and authorizations
- Non-conformance reports and resolutions
- Safety case and safety certificate

**Volume 5: Operations and Maintenance**
- Driver training records and competency assessments
- Operational procedures for ETCS operation
- Maintenance procedures and schedules
- Troubleshooting guides and contact information
- Lessons learned and recommendations for operations

### Record Retention Requirements
- **Commissioning documentation:** Permanent retention (life of ETCS installation plus 10 years)
- **JRU recordings:** 5 years retention for statistical analysis and incident investigation
- **Configuration data:** Current plus 5 previous versions retained
- **Safety case and approvals:** Permanent retention (regulatory requirement)
- **Test videos and photographs:** 10 years retention

## Regulatory Compliance

### ERA ERTMS Baseline 3 Compliance
Commissioning must verify compliance with all applicable SUBSET specifications:
- **SUBSET-026:** System Requirements Specification (functional and interface requirements)
- **SUBSET-036:** FFFIS for Eurobalise (data content and transmission specifications)
- **SUBSET-037:** EuroRadio FIS (radio communication protocol between train and RBC)
- **SUBSET-040:** Dimensioning and Engineering rules (balise positioning, RBC performance)
- **SUBSET-076:** Test Specification for Eurobalise (test procedures and acceptance criteria)
- **SUBSET-091:** Safety Requirements for DMI (human-machine interface design requirements)
- **SUBSET-094:** Functional Requirements for Onboard Test Facility (diagnostics and testing)

### CENELEC Railway Safety Standards
Commissioning process must satisfy CENELEC standards:
- **EN 50126:** RAMS specification and demonstration (reliability, availability, maintainability, safety targets)
- **EN 50128:** Software for railway control systems (software validation and verification)
- **EN 50129:** Safety-related electronic systems (safety integrity level verification, SIL 4 for ETCS)

### National Regulations
Comply with national railway safety authority requirements:
- **Notified Body approvals:** Type approval certificates for all ETCS equipment
- **National values:** Country-specific ETCS parameters implemented correctly
- **Operational authorizations:** Railway operator license to operate ETCS-equipped trains
- **Interoperability:** Cross-border operation authorized if applicable

## References

1. ERA ERTMS Baseline 3 Release 2 - Complete specification set (SUBSET-026 through SUBSET-108)
2. CENELEC EN 50126-1:2017 - Railway applications - RAMS specification
3. CENELEC EN 50128:2011 - Railway applications - Software for railway control and protection systems
4. CENELEC EN 50129:2018 - Railway applications - Safety related electronic systems for signaling
5. ERA/ERTMS/033281 - Guide for the application of COMMISSION REGULATION (EU) 2016/919 (Technical Specification for Interoperability - Control-Command and Signalling)
6. Alstom Atlas ETCS Commissioning Manual (vendor-specific, controlled distribution)
7. Siemens Trainguard ETCS Level 2 Commissioning Procedures (vendor-specific, controlled distribution)
8. UIC Code 406 - Capacity (used for operational capacity calculations with ETCS)
9. AREMA Communications & Signals Manual - Part 2.10 (ETCS implementation guidance for North America)
10. Network Rail Standard NR/L2/SIG/20125 - ERTMS: ETCS Application Design (UK-specific design rules)

---

**Document Classification:** Operational Procedure - Safety Critical - Controlled Distribution
**Distribution:** ETCS Project Teams, Commissioning Engineers, Railway Authorities, Safety Assessors
**Review Cycle:** Reviewed annually, updated whenever ERTMS specifications updated (typically Baseline revisions every 2-3 years)
**Version Control:** 1.0 (2025-11-05) - Initial comprehensive commissioning procedure based on Baseline 3 Release 2
**Security Classification:** Railway Critical Infrastructure - Distribution restricted to authorized personnel