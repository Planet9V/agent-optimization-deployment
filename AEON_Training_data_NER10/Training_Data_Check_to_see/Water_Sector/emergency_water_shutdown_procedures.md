# Emergency Water Shutdown Procedures

## Operational Overview
This document details emergency protocols for rapid water system isolation and shutdown in response to contamination events, infrastructure failures, or security incidents. Procedures ensure public safety while maintaining critical service continuity.

## Annotations

### 1. Contamination Event - Initial Detection
**Context**: Detection of potential water contamination through SCADA alarms, water quality monitoring, or public reports
**ICS Components**: Water quality event detection systems (CANARY), SCADA alarm management, supervisor notification systems
**Procedure**: Upon contamination alarm: (1) Verify with secondary sensors (2) Review SCADA trends for anomaly confirmation (3) Initiate incident command within 5 minutes (4) Escalate to emergency operations center
**Safety Critical**: False alarms can cause unnecessary public panic; true contamination events require immediate response to prevent exposure
**Standards**: EPA Water Security Incident Protocols, AWWA Emergency Preparedness Practices
**Vendors**: EPA CANARY software, Hach Guardian Blue, Halo WaterSentinel

### 2. Isolation Zone Identification
**Context**: Mapping affected distribution zone for targeted isolation minimizing service disruption
**ICS Components**: GIS hydraulic models, SCADA valve position tracking, pressure zone mapping
**Procedure**: Hydraulic model identifies minimum isolation zone containing contaminated area; SCADA displays all valves requiring closure; system generates valve closure sequence preventing water hammer
**Safety Critical**: Closing wrong valves or improper sequence can cause transient pressure events rupturing pipes
**Standards**: AWWA M32 Computer Modeling of Water Distribution Systems
**Vendors**: Innovyze InfoWater hydraulic modeling, Bentley WaterGEMS

### 3. Remote Valve Closure Sequence
**Context**: SCADA-controlled automated valve closure to isolate affected zones
**ICS Components**: Motorized gate valves, PLC valve control sequences, position feedback sensors
**Procedure**: Execute automated valve closure sequence from SCADA HMI; valves close at controlled rate (10-30 seconds per valve) preventing pressure surges; visual and audible confirmation of each valve position
**Safety Critical**: Rapid valve closure causes destructive water hammer; verify position feedback before proceeding to next valve
**Standards**: AWWA M44 Distribution Valves: Selection, Installation, Field Testing, and Maintenance
**Vendors**: AMERICAN Flow Control motorized valves, AVK gate valves with electric actuators

### 4. Manual Valve Isolation - Field Operations
**Context**: Field crew dispatch for manual valve closure when SCADA control unavailable
**ICS Components**: Paper valve maps, GPS navigation, portable valve keys, communication radios
**Procedure**: Dispatch two-person crew per valve location; crew confirms valve identification using GIS tags; operates valve slowly (1 revolution per 10 seconds); reports position to operations center every 15 minutes
**Safety Critical**: Incorrect valve closure can isolate wrong areas including hospitals and firefighting infrastructure
**Standards**: OSHA 1910.146 confined space entry when accessing valve vaults
**Vendors**: Mueller valve keys, Trimble GPS handhelds for field navigation

### 5. Customer Notification - Emergency Alert System
**Context**: Rapid public notification of water shutoff and contamination warnings
**ICS Components**: Reverse 911 systems, social media integration, website emergency banners, local media contacts
**Procedure**: Within 30 minutes of contamination confirmation: (1) Activate reverse 911 calls to affected area (2) Post emergency notices on utility website and social media (3) Issue press release to local media (4) Staff emergency hotline
**Safety Critical**: Delayed notification allows continued consumption of contaminated water
**Standards**: EPA Public Notification Rule requiring notification within timeframes based on contamination severity
**Vendors**: Everbridge emergency notification platform, Nixle community alerts

### 6. Pressure Monitoring - System Protection
**Context**: Continuous monitoring of system pressures during emergency isolation
**ICS Components**: Pressure transducers throughout distribution system, SCADA trending, alarm management
**Procedure**: Monitor pressure at boundary of isolation zone; maintain minimum 20 PSI pressure in operating zones; if pressure drops below 20 PSI, expand isolation zone to maintain pressure elsewhere
**Safety Critical**: Negative pressure or <20 PSI allows soil contamination intrusion through pipe leaks
**Standards**: AWWA pressure requirements for distribution systems minimum 20 PSI, target 40-60 PSI
**Vendors**: Sensus iPERL pressure loggers, Mueller pressure recorders

### 7. Fire Department Coordination
**Context**: Ensuring fire suppression capability during water system isolation
**ICS Components**: Fire department notification systems, hydrant GIS mapping, alternative water supply coordination
**Procedure**: Immediately notify fire department dispatch of isolation zones; provide map of operational hydrants; coordinate mutual aid from neighboring districts; position tanker trucks in isolated high-risk areas
**Safety Critical**: Building fires in isolated zones require alternative water supply to prevent loss of life
**Standards**: NFPA 1142 Standard on Water Supplies for Suburban and Rural Fire Fighting
**Vendors**: Fire department coordination via existing emergency management systems

### 8. Critical Facility Bypass - Hospital Priority
**Context**: Establishing alternative water supply to hospitals during system isolation
**ICS Components**: Emergency water tankers, temporary pipe connections, backflow preventers, bulk water supply points
**Procedure**: Within 2 hours of shutdown affecting hospital: (1) Deploy water tanker to hospital (2) Establish temporary feed connection to hospital storage (3) Provide minimum 20,000 gallons per day supply (4) Monitor hospital consumption
**Safety Critical**: Hospitals require continuous water for sanitation, dialysis, sterilization, and patient care
**Standards**: Joint Commission requirements for hospital emergency water supply
**Vendors**: National Tank Truck Carriers association for bulk water hauling

### 9. Flushing Operations - Contamination Removal
**Context**: Systematic flushing to remove contaminated water from distribution system
**ICS Components**: Unidirectional flushing plans, flow meters, hydrant valve controllers, chlorine monitoring
**Procedure**: Open hydrants systematically from source toward extremities; maintain minimum 3 fps velocity; monitor chlorine and turbidity at flushing sites; continue until water quality parameters stable for 30 minutes
**Safety Critical**: Inadequate flushing velocity fails to remove contaminated water from pipe biofilm and dead ends
**Standards**: AWWA M17 Installation, Field Testing, and Maintenance of Fire Hydrants
**Vendors**: Mueller Super Centurion fire hydrants, Clow Guardian hydrants

### 10. Water Quality Verification Sampling
**Context**: Comprehensive sampling to verify contamination clearance before restoring service
**ICS Components**: Sampling protocols, certified laboratory analysis, chain of custody procedures, rapid test kits
**Procedure**: Collect minimum 40 samples from isolated zone at strategic locations; analyze for free chlorine, bacteriological quality, and specific contaminant if known; all samples must meet standards before restoration
**Safety Critical**: Premature restoration exposes customers to contamination
**Standards**: EPA protocol for verification sampling following contamination events
**Vendors**: IDEXX Colilert for rapid coliform testing, certified laboratory analysis for chemical contaminants

### 11. Boil Water Advisory Management
**Context**: Issuing and managing boil water advisories when contamination risk but not confirmed
**ICS Components**: Public notification systems, media coordination, community organization outreach
**Procedure**: Issue boil water advisory if system experiences: pressure loss <20 PSI, main break in contaminated area, positive coliform test; advisory remains until two consecutive days of negative bacteriological samples
**Safety Critical**: Boil water advisories protect public health during uncertainty periods
**Standards**: EPA and state health department boil water advisory protocols
**Vendors**: Standard public notification systems

### 12. Alternative Water Supply Distribution
**Context**: Providing bottled or bulk water to affected population during extended outage
**ICS Components**: Emergency water supply contracts, distribution point logistics, community centers for water pickup
**Procedure**: Within 24 hours of shutdown: establish water distribution points at community centers providing minimum 1 gallon per person per day; prioritize delivery to elderly and disabled residents
**Safety Critical**: Dehydration and sanitation issues arise within 48 hours without water access
**Standards**: FEMA Emergency Water Supply guidelines 1 gallon per person per day minimum
**Vendors**: Emergency contracts with bottled water distributors, mutual aid agreements with neighboring utilities

### 13. System Re-pressurization Protocol
**Context**: Controlled restoration of pressure when returning isolated zones to service
**ICS Components**: Automated fill stations, pressure control valves, SCADA monitoring, air release valve management
**Procedure**: Slowly open isolation valves (10% open increments every 5 minutes); monitor pressure rise rate <5 PSI per minute; verify all air release valves functioning; confirm pressure stable at normal operating range
**Safety Critical**: Rapid pressurization causes pressure surges damaging pipes, meters, and customer appliances
**Standards**: AWWA best practices for system pressurization
**Vendors**: Cla-Val pressure control valves, Apco air release valves

### 14. SCADA System Security - Cyber Incident Response
**Context**: Response to cyber attack compromising SCADA system control
**ICS Components**: Intrusion detection systems, firewall logs, backup control systems, manual override capabilities
**Procedure**: Upon detection of SCADA compromise: (1) Isolate SCADA network from internet (2) Switch to manual local control at field sites (3) Deploy cybersecurity incident response team (4) Notify FBI and ICS-CERT
**Safety Critical**: Cyber attacks can manipulate water quality parameters or cause equipment damage
**Standards**: NIST Cybersecurity Framework for Critical Infrastructure
**Vendors**: Nozomi Networks for ICS security monitoring, Dragos cybersecurity platform

### 15. Main Break Emergency Isolation
**Context**: Rapid response to major transmission main failures
**ICS Components**: Leak detection systems, motorized isolation valves, emergency repair crews, bypass pumping equipment
**Procedure**: Within 15 minutes of main break detection: (1) Close isolation valves upstream and downstream of break (2) Assess impact zone population (3) Deploy repair crew (4) Establish temporary bypass if main >24-inch diameter
**Safety Critical**: Major main breaks can cause flooding, property damage, and large-scale service interruption
**Standards**: AWWA emergency repair procedures for transmission mains
**Vendors**: Romco Equipment for tapping machines, Smith-Blair pipe repair clamps

### 16. Treatment Plant Emergency Shutdown
**Context**: Coordinated shutdown of water treatment plant during chemical spill or equipment failure
**ICS Components**: Emergency stop buttons, chemical containment systems, backup power, communication systems
**Procedure**: Emergency shutdown sequence: (1) Stop chemical feeds (2) Stop high service pumps (3) Close raw water intake (4) Switch to alternative source or finished water storage (5) Notify distribution operators
**Safety Critical**: Treatment plant failures can contaminate entire distribution system if not isolated promptly
**Standards**: OSHA PSM (Process Safety Management) for chemical handling
**Vendors**: Standard plant emergency systems per design specifications

### 17. Contamination Source Investigation
**Context**: Rapid forensic investigation to identify contamination point of entry
**ICS Components**: Hydraulic models, backflow investigation equipment, security camera footage, water quality mapping
**Procedure**: Backtrack contamination plume using hydraulic model and water quality data; inspect backflow prevention devices; review security footage at reservoirs and pump stations; sample at suspected entry points
**Safety Critical**: Identifying contamination source prevents recurring events and guides remediation
**Standards**: EPA protocols for contamination source identification
**Vendors**: Hydraulic model software for backtracking, field sampling equipment

### 18. Mutual Aid Activation
**Context**: Requesting assistance from neighboring water utilities during major emergency
**ICS Components**: Mutual aid agreements, emergency contact lists, resource sharing protocols
**Procedure**: Contact neighboring utilities for: equipment loans, staff augmentation, temporary interconnection activation, emergency water supply; document all assistance for FEMA reimbursement
**Safety Critical**: Major emergencies exceed single utility response capabilities
**Standards**: AWWA Mutual Aid and Assistance programs
**Vendors**: State water utility associations coordinate mutual aid networks

### 19. Regulatory Notification Requirements
**Context**: Mandatory notifications to regulatory agencies during emergency events
**ICS Components**: Emergency contact lists, documentation systems, reporting templates
**Procedure**: Notify within required timeframes: State health department (2 hours for Tier 1 violations), EPA regional office (24 hours), State environmental agency (immediate for major spills), Governor's office (for critical infrastructure attacks)
**Safety Critical**: Regulatory notifications trigger state/federal assistance and public protection measures
**Standards**: EPA Public Notification Rule, state-specific requirements
**Vendors**: Standard communication systems

### 20. Residential Plumbing Contamination Mitigation
**Context**: Guidance to customers for premise plumbing decontamination after system events
**ICS Components**: Customer communication materials, plumber coordination, sampling protocols
**Procedure**: Provide customers written guidance: (1) Flush all taps for 15 minutes (2) Drain and flush hot water heater (3) Replace point-of-use filters (4) Consider premise plumbing sampling if vulnerable populations present
**Safety Critical**: Contamination can persist in premise plumbing after distribution system is cleared
**Standards**: CDC guidance on premise plumbing decontamination
**Vendors**: Guidance materials from AWWA and EPA

### 21. Emergency Operations Center Activation
**Context**: Establishing unified command for large-scale emergency response
**ICS Components**: Emergency Operations Center facility, communication systems, incident command structure, resource management
**Procedure**: Activate EOC for events affecting >10,000 customers or lasting >24 hours; establish incident command structure with operations, planning, logistics, and finance sections; conduct briefings every 12 hours
**Safety Critical**: Coordinated response prevents conflicting actions and ensures efficient resource use
**Standards**: NIMS (National Incident Management System) ICS protocols
**Vendors**: Emergency management software platforms, WebEOC

### 22. Post-Incident Documentation and Review
**Context**: Comprehensive documentation and lessons-learned analysis following emergency
**ICS Components**: Incident reports, timeline reconstruction, financial documentation, improvement recommendations
**Procedure**: Within 30 days of incident resolution: compile comprehensive incident report including timeline, actions taken, costs incurred, regulatory compliance; conduct after-action review with all stakeholders; update emergency response plans
**Safety Critical**: Lessons learned prevent future incidents and improve response capabilities
**Standards**: AWWA G440 Emergency Preparedness Practices
**Vendors**: Standard documentation and reporting systems

### 23. Media Relations and Public Communication
**Context**: Managing public information during emergency to prevent panic and misinformation
**ICS Components**: Public information officer, media briefing schedules, fact sheet preparation, rumor control
**Procedure**: Designate single public information officer; hold media briefings every 6 hours during active emergency; provide factual information only; establish rumor control hotline; monitor social media for misinformation
**Safety Critical**: Poor communication erodes public trust and can lead to unnecessary panic or non-compliance with safety instructions
**Standards**: Emergency Risk Communication principles from CDC
**Vendors**: Standard media relations protocols

### 24. Service Restoration Verification and Documentation
**Context**: Systematic verification that all systems normal before declaring emergency concluded
**ICS Components**: Restoration checklists, water quality verification, equipment status confirmation, customer complaint monitoring
**Procedure**: Before ending emergency status verify: all water quality samples acceptable, system pressures normal, no active customer complaints, all equipment operational, regulatory agencies notified of resolution, public "all clear" notice issued
**Safety Critical**: Premature declaration of "all clear" can leave residual hazards
**Standards**: Utility-specific restoration protocols based on AWWA guidance
**Vendors**: Standard verification documentation systems

## Integration with Emergency Management
All water utility emergency procedures integrate with city/county emergency management, public health departments, and state environmental agencies through unified incident command structures.

## Staff Training and Exercises
Emergency procedures require annual staff training and tabletop exercises with quarterly full-scale drills of isolation and notification procedures to maintain response readiness.
