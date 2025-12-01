# 911 Dispatch CAD Operations

## Overview
Operational procedures for Computer-Aided Dispatch (CAD) systems managing emergency call intake, resource allocation, unit dispatching, and incident tracking for police, fire, and EMS services.

## Annotations

### 1. Call Answer and Priority Classification
**Entity Type**: OPERATIONAL_PROCEDURE
**Description**: Rapid call answering and NENA EMD protocol-based priority classification determining response urgency
**Related Entities**: Emergency Medical Dispatch, Call Processing, Priority Systems
**Technical Context**: NENA standards, EMD cards, Omega/Alpha/Bravo/Charlie/Delta/Echo codes, ProQA software
**Safety Considerations**: Life-threatening recognition, caller interrogation, pre-arrival instructions, call retention

### 2. Computer-Aided Dispatch Interface
**Entity Type**: SOFTWARE_SYSTEM
**Description**: Integrated dispatch workstation combining telephony, mapping, unit status, and incident management
**Related Entities**: Public Safety Software, Situational Awareness, Multi-Agency Coordination
**Technical Context**: Motorola CommandCentral, Tyler New World, Hexagon Intergraph, CAD-to-CAD interoperability
**Safety Considerations**: System redundancy, backup procedures, data integrity, training requirements

### 3. Automatic Vehicle Location (AVL) Integration
**Entity Type**: TRACKING_SYSTEM
**Description**: GPS-based real-time tracking of emergency response units supporting optimal resource deployment
**Related Entities**: Fleet Management, Response Time Optimization, Geospatial Systems
**Technical Context**: GPS receivers, cellular/radio telemetry, GIS mapping, closest-unit determination, breadcrumb trails
**Safety Considerations**: Officer safety, tracking accuracy, system reliability, privacy considerations

### 4. Recommended Unit Assignment Algorithm
**Entity Type**: DECISION_SUPPORT
**Description**: CAD algorithms recommending optimal unit assignments based on location, availability, and capability
**Related Entities**: Resource Optimization, Response Time, Incident Type Matching
**Technical Context**: Geographic zones, unit capabilities, mutual aid, dynamic deployment, workload balancing
**Safety Considerations**: Override capabilities, dispatcher judgment, special circumstances, safety protocols

### 5. Multi-Channel Radio Dispatch
**Entity Type**: COMMUNICATION_SYSTEM
**Description**: Coordinated radio traffic management across multiple tactical channels and talk groups
**Related Entities**: Radio Systems, P25 Networks, Channel Management
**Technical Context**: P25 Phase II, talk groups, encryption, patch groups, interoperability channels, console interfaces
**Safety Considerations**: Channel congestion, priority traffic, emergency activation, interoperability coordination

### 6. Incident Status Tracking
**Entity Type**: WORKFLOW_MANAGEMENT
**Description**: Real-time tracking of incident lifecycle from dispatch through on-scene to clearance
**Related Entities**: Unit Status, Time Stamping, Performance Metrics
**Technical Context**: Status buttons, automatic timestamps, NFPA 1710/1221 standards, event timelines
**Safety Considerations**: Accountability, officer check-ins, duration monitoring, backup unit triggers

### 7. Emergency Medical Dispatch Protocol
**Entity Type**: MEDICAL_GUIDANCE
**Description**: Scripted interrogation protocols providing pre-arrival instructions for medical emergencies
**Related Entities**: Medical Priority Dispatch, Caller Instructions, Life-Saving Support
**Technical Context**: IAED/NAED protocols, ProQA/PowerPhone systems, quality assurance, cardiac arrest recognition
**Safety Considerations**: CPR instructions, choking protocols, bleeding control, pandemic screening

### 8. GIS Mapping and Geocoding
**Entity Type**: GEOSPATIAL_SYSTEM
**Description**: Address validation, latitude/longitude assignment, and map-based incident visualization
**Related Entities**: Address Management, Spatial Analysis, Routing
**Technical Context**: MSAG (Master Street Address Guide), ALI database, Esri ArcGIS, geocoding accuracy, landmark search
**Safety Considerations**: Address verification, rural addressing, new construction, mapping errors

### 9. Mobile Data Terminal (MDT) Integration
**Entity Type**: FIELD_CONNECTIVITY
**Description**: Bi-directional data communication between dispatch center and vehicle-mounted computers
**Related Entities**: Officer Safety, Information Access, Status Updates
**Technical Context**: LTE broadband, messaging, CAD queries, RMS access, AVL reporting, touchscreen interfaces
**Safety Considerations**: Distracted driving, encryption, authentication, silent alarm activation

### 10. Call Recording and Playback
**Entity Type**: DOCUMENTATION_SYSTEM
**Description**: Audio recording of 911 calls and radio traffic for quality assurance and legal evidence
**Related Entities**: Evidence Preservation, Quality Control, Legal Compliance
**Technical Context**: Digital logging recorders, redundant storage, instant playback, search/retrieval, retention policies
**Safety Considerations**: Chain of custody, storage security, retention compliance, discovery requests

### 11. Mutual Aid and Interagency Coordination
**Entity Type**: OPERATIONAL_COORDINATION
**Description**: Procedures for requesting and deploying resources across jurisdictional boundaries
**Related Entities**: Multi-Agency Response, Regional Coordination, Resource Sharing
**Technical Context**: Mutual aid agreements, CAD-to-CAD sharing, regional dispatch centers, NIMS compliance
**Safety Considerations**: Command structure, resource tracking, liability, communication protocols

### 12. Priority Dispatch and Call Stacking
**Entity Type**: WORKLOAD_MANAGEMENT
**Description**: Managing multiple pending incidents prioritizing life-threatening calls during high-demand periods
**Related Entities**: Call Volume Management, Resource Allocation, Queue Management
**Technical Context**: Priority queuing, pending incident lists, resource availability, delayed response protocols
**Safety Considerations**: Life safety priority, caller updates, delayed response notification, triage protocols

### 13. Silent/Panic Alarm Processing
**Entity Type**: EMERGENCY_RESPONSE
**Description**: Protocols for responding to officer panic button activations and silent alarm signals
**Related Entities**: Officer Safety, Emergency Activation, Critical Response
**Technical Context**: Emergency button monitoring, GPS tracking, automatic notifications, immediate dispatch
**Safety Considerations**: False alarm verification, backup unit dispatch, supervisor notification, tactical response

### 14. CAD Redundancy and Failover
**Entity Type**: SYSTEM_RELIABILITY
**Description**: Backup CAD systems and contingency procedures maintaining operations during system failures
**Related Entities**: Business Continuity, Disaster Recovery, High Availability
**Technical Context**: Hot standby servers, automatic failover, geographic redundancy, manual procedures, backup terminals
**Safety Considerations**: Seamless transition, data synchronization, training, testing schedules

### 15. PSAP-to-PSAP Transfer Protocols
**Entity Type**: CALL_ROUTING
**Description**: Standardized procedures transferring 911 calls between jurisdictions with call and location data
**Related Entities**: Jurisdictional Boundaries, Call Routing, Information Continuity
**Technical Context**: Selective routing, MSAG boundaries, CAD-to-CAD data transfer, administrative transfers
**Safety Considerations**: Transfer speed, data completeness, caller confusion, verification protocols

### 16. Premise Hazard Warnings
**Entity Type**: SAFETY_INFORMATION
**Description**: Database of location-specific hazards, weapons, dangerous persons, and structural information
**Related Entities**: Officer Safety, Situational Awareness, Intelligence Systems
**Technical Context**: Premise history, flag alerts, BOLO integration, photo attachments, automatic display on dispatch
**Safety Considerations**: Information accuracy, privacy, liability, update procedures, officer notification

### 17. Caller Location Technology
**Entity Type**: E911_SYSTEMS
**Description**: Automatic location identification for wireline, wireless, and VoIP 911 callers
**Related Entities**: Enhanced 911, Phase II Wireless, NG911
**Technical Context**: ALI/ANI delivery, Phase II coordinates, uncertainty radius, Z-axis altitude, dispatchable location
**Safety Considerations**: Location accuracy, rebid requirements, VoIP challenges, SMS location

### 18. NCIC/NLETS Query Integration
**Entity Type**: DATABASE_ACCESS
**Description**: Real-time access to National Crime Information Center and law enforcement databases
**Related Entities**: Criminal Records, Wants/Warrants, Stolen Property
**Technical Context**: CJIS security, terminal access, query protocols, hit confirmations, NCIC validation
**Safety Considerations**: Officer safety warnings, system security, misuse prevention, hit confirmations

### 19. Dispatch Quality Assurance
**Entity Type**: PERFORMANCE_MANAGEMENT
**Description**: Call review and performance evaluation programs ensuring protocol compliance and excellence
**Related Entities**: Training, Performance Metrics, Continuous Improvement
**Technical Context**: Call review software, compliance scoring, coaching programs, accreditation standards
**Safety Considerations**: Error identification, training needs, protocol adherence, liability reduction

### 20. Text-to-911 Operations
**Entity Type**: ACCESSIBILITY_SERVICE
**Description**: SMS text message handling for deaf/hard-of-hearing or situations requiring silent communication
**Related Entities**: ADA Compliance, Alternative Access, Silent Emergency
**Technical Context**: TDD/TTY, RTT (Real-Time Text), text-to-speech, character-by-character display
**Safety Considerations**: Delayed communication, verification protocols, deaf caller procedures, abuse prevention

### 21. Fire/EMS Pre-Alerts and Notifications
**Entity Type**: OPERATIONAL_COORDINATION
**Description**: Automated hospital notifications and fire apparatus pre-alerts improving response readiness
**Related Entities**: Hospital Coordination, Apparatus Alerting, Readiness Management
**Technical Context**: Station alerting systems, hospital notification systems, automatic unit recommendations
**Safety Considerations**: Response time reduction, hospital capacity, patient handoff, cardiac alert protocols

### 22. Incident Command System (ICS) Integration
**Entity Type**: TACTICAL_COORDINATION
**Description**: CAD support for ICS structure during major incidents with role tracking and resource management
**Related Entities**: NIMS Compliance, Major Incident Management, Command Structure
**Technical Context**: ICS position assignment, tactical channel assignment, resource ordering, situation reporting
**Safety Considerations**: Command clarity, accountability, span of control, tactical communications

### 23. Officer Welfare Check Procedures
**Entity Type**: SAFETY_PROCEDURE
**Description**: Automated and manual procedures verifying officer safety through status updates and location tracking
**Related Entities**: Officer Safety, Accountability, Welfare Monitoring
**Technical Context**: Activity timers, periodic check-ins, location monitoring, no-response protocols
**Safety Considerations**: Check-in enforcement, backup dispatch, prolonged on-scene, officer down procedures

### 24. Performance Metrics and Reporting
**Entity Type**: ANALYTICS_SYSTEM
**Description**: Automated reporting of response times, call volumes, and NFPA/NENA compliance metrics
**Related Entities**: Performance Standards, Reporting Compliance, Management Analytics
**Technical Context**: NFPA 1710 benchmarks, NENA standards, BI tools, dashboard visualization, trend analysis
**Safety Considerations**: Response time monitoring, staffing adequacy, service level maintenance, continuous improvement

## Regulatory Framework
- NENA (National Emergency Number Association) Standards
- NFPA 1221: Standard for Installation, Maintenance, and Use of Emergency Services Communications Systems
- FCC Enhanced 911 Rules
- CJIS Security Policy
- ADA Title II Compliance

## Communication Protocols
- NENA i3 Standard: Next Generation 911
- APCO P25: Digital radio
- SIP/RTP: VoIP telephony
- CAD-to-CAD: Inter-agency data exchange

## Key Vendors & Systems
- Motorola Solutions: CommandCentral CAD
- Tyler Technologies: New World CAD
- Hexagon Safety & Infrastructure: Intergraph CAD
- CentralSquare: CAD systems
- Priority Dispatch: ProQA EMD software
