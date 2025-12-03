# Air Traffic Control Handoff Procedures

## Operational Overview
This document details Air Traffic Control (ATC) coordination and aircraft handoff procedures between controllers ensuring seamless aircraft transfer between control sectors, facilities, and airspace boundaries maintaining continuous positive control and separation standards.

## Annotations

### 1. Radar Handoff Initiation - Point-Out Procedure
**Context**: Initial coordination when aircraft approaches sector boundary requiring control transfer
**ICS Components**: Radar displays, flight data processing systems, voice communication systems, coordination tools
**Procedure**: Transferring controller initiates handoff 2-5 minutes before aircraft reaches boundary by flashing data block on receiving controller's radar display; receiving controller accepts handoff by clicking data block or pressing keyboard command; verbal coordination required for any non-standard situations
**Safety Critical**: Both controllers must maintain positive radar identification during handoff; lost radar contact requires immediate coordination
**Standards**: FAA Order 7110.65 Air Traffic Control procedures, ICAO PANS-ATM Doc 4444
**Vendors**: Raytheon STARS (Standard Terminal Automation Replacement System), Lockheed Martin ERAM (En Route Automation Modernization)

### 2. Flight Progress Strip Management
**Context**: Paper or electronic strip printing and coordination for non-radar environments
**ICS Components**: Flight data processing, strip printers, electronic flight strip systems, coordination boards
**Procedure**: Flight plan data automatically prints on flight progress strips at appropriate sectors 20-30 minutes before aircraft arrival; controllers manually coordinate amendments, altitude requests, and routing changes by marking strips and verbal coordination; strips transferred physically or electronically with aircraft handoff
**Safety Critical**: Strip errors or failures to coordinate amendments can cause separation losses or traffic conflicts
**Standards**: FAA Order 7110.65 Chapter 2 Flight Progress Strip procedures
**Vendors**: Indra Aeronautics electronic flight strips, Saab Sensis flight data processing

### 3. Inter-Facility Coordination - Automated Handoffs
**Context**: Coordination between different ATC facilities (TRACON to Center, Center to Center)
**ICS Components**: Inter-facility data communications, automated handoff protocols, coordination messages
**Procedure**: Automated systems transfer flight data and radar tracks between facilities; transferring facility controller approves handoff when aircraft 5-15 miles from boundary; receiving facility automatically accepts unless non-standard conditions exist requiring voice coordination
**Safety Critical**: Data link failures require manual phone coordination and procedural separation increases
**Standards**: FAA inter-facility coordination procedures, ICAO regional coordination agreements
**Vendors**: Harris ATCFSS (ATC Facilities Support System), L3Harris communication systems

### 4. Altitude Assignment and Clearance Coordination
**Context**: Coordinating altitude changes when aircraft transitioning between sectors
**ICS Components**: Automation conflict probe tools, altitude filters, coordination menus
**Procedure**: Transferring controller ensures aircraft cleared to altitude acceptable to receiving controller or coordinates different altitude via verbal communication or data link messaging; automation conflict probe verifies separation with all other traffic before altitude clearance issued
**Safety Critical**: Uncoordinated altitude changes can cause loss of separation with other aircraft
**Standards**: FAA altitude assignment procedures, vertical separation standards (1000 feet below FL290, 2000 feet above)
**Vendors**: Automation conflict probe tools in ERAM and STARS systems

### 5. Speed Control and Sequencing Coordination
**Context**: Coordination of speed assignments when establishing arrival sequences
**ICS Components**: Arrival management systems (Time-Based Flow Management), speed advisories, metering tools
**Procedure**: Terminal controllers coordinate arrival sequence and speed control with center controllers typically 40-100 miles from airport; center issues speed restrictions to achieve proper spacing; speed controls released to terminal controllers at handoff point
**Safety Critical**: Poor speed coordination causes inadequate spacing or go-arounds affecting airport capacity
**Standards**: FAA Order 7110.65 arrival sequencing procedures, TFM (Traffic Flow Management) directives
**Vendors**: NASA CTAS (Center-TRACON Automation System), Metron TFDM (Terminal Flight Data Manager)

### 6. Departure Release Coordination
**Context**: Coordination between tower and departure controllers for IFR departure release
**ICS Components**: Departure management systems, release timers, MIT (Miles-in-Trail) restrictions
**Procedure**: Tower controller requests departure release from TRACON or Center; release issued with time restriction and heading assignment; tower must release aircraft within release window or request new release time; TRACON coordinates spacing with other departures and overflights
**Safety Critical**: Failure to comply with release restrictions can cause traffic conflicts with other departures or overflights
**Standards**: FAA departure procedures, letters of agreement between facilities
**Vendors**: Integrated into STARS and ERAM automation platforms

### 7. Special Use Airspace Coordination
**Context**: Coordination when aircraft routing requires crossing active restricted, prohibited, or military operating areas
**ICS Components**: Special use airspace (SUA) scheduling systems, ERAM airspace status displays, coordination phone lines
**Procedure**: Controllers verify SUA status before issuing clearances crossing those areas; active SUA requires coordination with controlling agency for approval to penetrate or requires rerouting aircraft around the airspace; automation displays real-time SUA status
**Safety Critical**: Unauthorized SUA penetration can conflict with military training operations or cause security violations
**Standards**: FAA Special Use Airspace procedures, military coordination procedures
**Vendors**: SUA scheduling through FAA SWIM (System Wide Information Management) services

### 8. Emergency Aircraft Priority Handling
**Context**: Coordination procedures for aircraft declaring emergencies (Mayday/Pan-Pan)
**ICS Components**: Emergency alert systems, priority handling tools, coordination phone lines to emergency services
**Procedure**: Controller receiving emergency declaration immediately alerts supervisory personnel and adjacent controllers; priority handling given to emergency aircraft including direct routing, altitude assignment, and airport/runway assignment; continuous coordination maintained with all affected sectors and approach/tower controllers
**Safety Critical**: Delays in emergency coordination can affect life-safety outcomes
**Standards**: FAA Order 7110.65 Chapter 10 Emergency Procedures, ICAO Annex 2 emergency rules
**Vendors**: Emergency notification integrated into STARS/ERAM systems

### 9. Weather Deviation Coordination
**Context**: Coordination when aircraft requesting weather deviations affecting other sectors
**ICS Components**: Weather radar integration, graphical weather displays, conflict prediction tools
**Procedure**: Pilot requests deviation around weather; controller coordinates with adjacent sectors if deviation crosses boundaries; automation runs conflict checks with other aircraft in deviation path; approval granted or modified routing issued maintaining separation
**Safety Critical**: Uncoordinated weather deviations can cause unexpected traffic conflicts
**Standards**: FAA weather deviation procedures, ICAO procedures for weather avoidance
**Vendors**: Weather integration from ITT Exelis, Baron Weather, integrated into ATC displays

### 10. Oceanic Track System Coordination
**Context**: North Atlantic Tracks (NATs) and Pacific Organized Track System (PACOTS) coordination
**ICS Components**: Oceanic ATC systems, HF radio communications, CPDLC (Controller-Pilot Data Link), satellite communications
**Procedure**: Oceanic clearances issued before aircraft enters oceanic airspace specifying track, altitude, Mach number, and oceanic entry/exit points; domestic controllers coordinate transfers to oceanic control typically 30 minutes before oceanic entry; procedural separation standards applied (50-100 NM longitudinal)
**Safety Critical**: Oceanic separation standards larger than radar separation due to limited surveillance and communications
**Standards**: ICAO North Atlantic operations manual, Pacific region coordination procedures
**Vendors**: Harris Aeronautical oceanic systems, Nav Canada NAT systems

### 11. Military-Civilian ATC Coordination
**Context**: Coordination between FAA civilian controllers and military ATC facilities
**ICS Components**: Military radar feeds, inter-service communications, letters of agreement (LOAs)
**Procedure**: Military aircraft receiving services from civilian ATC facilities or vice versa requires coordination per facility letters of agreement; military controllers transfer aircraft to FAA controllers at boundary using standard handoff procedures; special procedures apply for military formation flights and tactical operations
**Safety Critical**: Coordination failures between military and civilian facilities can cause separation losses
**Standards**: FAA-DOD coordination procedures, facility-specific LOAs
**Vendors**: Joint FAA-DOD automation systems for radar data sharing

### 12. Automation Conflict Alert Resolution
**Context**: Response to automated conflict alert warnings predicting separation violations
**ICS Components**: Conflict probe algorithms, visual/aural alerts on controller displays, resolution advisories
**Procedure**: When conflict alert activates, controller immediately assesses situation; issues traffic advisories to both aircraft; takes action to resolve conflict via heading, altitude, or speed changes; coordinates resolution with other affected controllers; suppresses nuisance alerts after assessing false alarm
**Safety Critical**: Conflict alerts require immediate action; ignoring or suppressing valid alerts can lead to mid-air collisions
**Standards**: FAA Order 7110.65 conflict alert procedures, TCAS integration standards
**Vendors**: Conflict detection algorithms in ERAM, STARS systems with 1-2 minute look-ahead

### 13. Minimum Safe Altitude Warning (MSAW) Response
**Context**: Response to automated terrain proximity warnings for aircraft descending dangerously close to terrain
**ICS Components**: Digital terrain elevation database, MSAW algorithms, visual/aural controller alerts
**Procedure**: MSAW alert triggers when aircraft trajectory predicts terrain conflict within 30-60 seconds; controller immediately issues safety alert to pilot: "Low altitude alert, check your altitude immediately, MEA in your area is [altitude]"; monitors aircraft climb to safe altitude
**Safety Critical**: MSAW alerts prevent controlled flight into terrain (CFIT) accidents; immediate response essential
**Standards**: FAA Order 7110.65 safety alert procedures, ICAO terrain awareness standards
**Vendors**: MSAW integrated into STARS terminal automation, ERAM for en route

### 14. Flow Control and Ground Delay Programs
**Context**: Coordination with Air Traffic Control System Command Center (ATCSCC) for traffic management initiatives
**ICS Components**: Traffic Flow Management System (TFMS), Collaborative Decision Making (CDM) tools, ground delay program assignments
**Procedure**: ATCSCC issues ground delay programs (GDP) or ground stops when arrival demand exceeds airport capacity; controllers apply assigned EDCTs (Expected Departure Clearance Times) to departing flights; departures held on ground rather than airborne holding; coordination with airlines via CDM system
**Safety Critical**: Ground delays prevent airborne congestion maintaining safe separation standards
**Standards**: FAA Traffic Management procedures, CDM principles
**Vendors**: Metron Aviation TFMS, Leidos flow management tools

### 15. International Boundary Transfer Coordination
**Context**: Aircraft transfer between countries requiring coordination with foreign ATC services
**ICS Components**: International coordination systems, letters of agreement with foreign ANSPs (Air Navigation Service Providers)
**Procedure**: Transfer coordination initiated 10-20 minutes before boundary crossing; automated message exchange systems transmit flight data to foreign ATC; voice coordination for non-standard situations; pilot instructed to contact foreign frequency at designated point
**Safety Critical**: Coordination failures at international boundaries can result in aircraft operating without ATC service
**Standards**: ICAO regional coordination procedures, bilateral agreements between countries
**Vendors**: EUROCONTROL IFPS (Integrated Flight Plan Processing System) for European coordination, AFTN message exchange

### 16. Pilot-Controller Communication Standardization
**Context**: Standardized phraseology ensuring clear and unambiguous communication
**ICS Components**: Voice communication recording systems, phraseology training systems
**Procedure**: Controllers and pilots use standardized ICAO phraseology for all clearances and instructions; readback/hearback errors corrected immediately; critical clearances (altitude, heading, speed) require pilot readback verification; non-standard phraseology avoided to prevent misunderstandings
**Safety Critical**: Communication errors major contributing factor in aviation incidents; standardization reduces confusion
**Standards**: ICAO Annex 10 Aeronautical Telecommunications, FAA Pilot/Controller Glossary
**Vendors**: Voice recording systems from L3Harris, NICE recording solutions

### 17. Controller Workload Management and Relief
**Context**: Managing controller workload and position relief procedures maintaining continuity
**ICS Components**: Workload monitoring tools, position relief briefing protocols, supervisor oversight
**Procedure**: Controllers work positions maximum 2 hours followed by break period; position relief requires verbal briefing covering all active aircraft, pending clearances, weather, and special situations; relieving controller acknowledges understanding before assuming position; supervisor monitors traffic complexity adjusting sector boundaries if excessive workload
**Safety Critical**: Excessive controller fatigue or inadequate position relief briefings contribute to errors
**Standards**: FAA Order 7210.3 Air Traffic Controller Training and Certification, fatigue management policies
**Vendors**: Workload monitoring through automation metrics in ERAM/STARS

### 18. Lost Communication Procedures
**Context**: Procedures when radio communications with aircraft are lost
**ICS Components**: Emergency frequency monitoring (121.5 MHz), relay attempts through other aircraft, coordination with adjacent facilities
**Procedure**: After loss of radio contact, controller attempts alternate frequencies; requests nearby aircraft to relay messages; coordinates with adjacent facilities to attempt contact; aircraft expected to follow NORDO (No Radio) procedures continuing last clearance; emergency services alerted if prolonged communications loss
**Safety Critical**: Lost communication aircraft unpredictable; other traffic must be separated from NORDO aircraft flight path
**Standards**: FAA NORDO procedures, ICAO Annex 2 lost communication rules
**Vendors**: Multi-frequency monitoring capabilities in FAA radio systems

### 19. Approach Control Sequencing and Spacing
**Context**: Terminal area controllers establishing arrival sequence maintaining spacing standards
**ICS Components**: Arrival management tools, wake turbulence separation algorithms, precision runway monitor systems
**Procedure**: Approach controllers establish sequence typically 30-40 miles from airport; apply required separation standards (3-6 NM based on wake turbulence category); vector aircraft onto final approach course maintaining spacing; coordinate with tower controllers for landing clearances
**Safety Critical**: Inadequate spacing causes go-arounds or wake turbulence encounters
**Standards**: FAA Order 7110.65 arrival procedures, wake turbulence separation standards
**Vendors**: TFDM (Terminal Flight Data Manager) from Metron Aviation, wake vortex prediction systems

### 20. Runway Incursion Prevention
**Context**: Coordination between tower and ground controllers preventing aircraft/vehicle conflicts on runways
**ICS Components**: Airport Surface Detection Equipment (ASDE-X), runway status lights (RWSL), Final Approach Runway Occupancy Signal (FAROS)
**Procedure**: Ground controller ensures runway clear before issuing taxi clearances crossing active runways; tower controller verifies runway clear on ASDE-X display before issuing takeoff clearance; automated runway status lights illuminate warning vehicles/aircraft of impending conflicts; controllers maintain constant visual scanning
**Safety Critical**: Runway incursions major safety concern; collisions on runways often catastrophic
**Standards**: FAA runway incursion prevention procedures, ICAO runway safety programs
**Vendors**: Raytheon ASDE-X, FAA runway status light systems

### 21. Bird Strike Hazard Coordination
**Context**: Coordination when significant bird activity reported near airports
**ICS Components**: Bird radar systems, wildlife management communications, NOTAM systems
**Procedure**: When significant bird activity detected, airport wildlife management teams activated; controllers issue advisories to arriving/departing aircraft; NOTAM issued if activity severe; operations may be temporarily suspended if bird strike risk extreme
**Safety Critical**: Bird strikes can cause engine failures or aircraft damage especially during critical takeoff/landing phases
**Standards**: FAA wildlife hazard management, ICAO wildlife strike prevention
**Vendors**: Robin Radar bird detection systems, DeTect Inc. avian radar

### 22. Unmanned Aircraft Systems (UAS) Integration
**Context**: Coordination procedures for drone/UAS operations in controlled airspace
**ICS Components**: UAS Service Supplier (USS) systems, LAANC (Low Altitude Authorization and Notification Capability), UAS detection systems
**Procedure**: UAS operators request airspace authorization through LAANC system; ATC facilities receive automated notifications; controllers issue real-time altitude restrictions if UAS operations conflict with manned aircraft; emergency procedures for unauthorized UAS activity include aircraft rerouting and law enforcement notification
**Safety Critical**: Uncoordinated UAS operations pose collision risk to manned aircraft
**Standards**: FAA UAS integration procedures, Part 107 regulations
**Vendors**: AirMap LAANC, Skyward LAANC services, DJI AeroScope UAS detection

### 23. Reduced Vertical Separation Minimum (RVSM) Operations
**Context**: Operations in airspace where 1000-foot vertical separation applied between FL290-FL410
**ICS Components**: Aircraft RVSM certification database, altitude monitoring systems, conflict probe tools
**Procedure**: Only RVSM-certified aircraft approved for operations in RVSM airspace; controllers verify aircraft RVSM status in flight plan; apply 1000-foot vertical separation FL290-FL410; non-RVSM aircraft restricted to altitudes outside RVSM airspace or granted 2000-foot separation
**Safety Critical**: RVSM requires precise altitude-keeping capability; non-certified aircraft require increased separation
**Standards**: FAA RVSM approval procedures, ICAO Doc 9574 RVSM manual
**Vendors**: RVSM monitoring programs operated by EUROCONTROL and FAA

### 24. Controller Training and Certification
**Context**: Comprehensive training programs ensuring controller competency before operational certification
**ICS Components**: Air Traffic Control simulators, on-the-job training (OJT), competency assessment tools
**Procedure**: Controllers complete FAA Academy training followed by 2-3 years facility-specific training; training progresses through ground control, local control, approach control, and en route control positions; certified performance instructors (CPIs) provide OJT; regular proficiency checks maintain certification
**Safety Critical**: Inadequately trained controllers risk making errors causing incidents or accidents
**Standards**: FAA Order 3120.4 Air Traffic Technical Training, certification requirements
**Vendors**: FAA Academy training systems, Adacel MaxSim ATC simulators

## Integration with National Airspace System
All ATC procedures integrate with broader National Airspace System including weather services, flight planning systems, airline operations centers, and airport operations ensuring coordinated and efficient air traffic management.

## Continuous Improvement and Safety Management
ATC facilities operate Safety Management Systems (SMS) continuously analyzing operational data, incident reports, and controller feedback to identify and mitigate safety risks through procedural improvements and system enhancements.
