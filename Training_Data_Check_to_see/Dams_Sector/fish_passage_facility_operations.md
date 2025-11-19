# Fish Passage Facility Operations

## Overview
Operational procedures for fish ladder, fish lift, and fish screen systems facilitating upstream and downstream fish migration while complying with environmental regulations and species protection requirements.

## Annotations

### 1. Fish Ladder Hydraulic Operation
**Entity Type**: FACILITY_OPERATION
**Description**: Maintaining optimal water flow velocities and depths in fish ladder pools for target species passage
**Related Entities**: Flow Control, Attraction Flow, Species Requirements
**Technical Context**: Pool-and-weir ladders, vertical slot designs, 1 ft/s target velocity, 1-foot head differential
**Safety Considerations**: Flow stability, debris clearance, water quality, seasonal adjustments

### 2. Attraction Flow Management
**Entity Type**: OPERATIONAL_PROCEDURE
**Description**: Supplemental water flow at ladder entrance attracting migrating fish from tailrace to passage entrance
**Related Entities**: Fish Behavior, Passage Efficiency, Flow Distribution
**Technical Context**: Attraction flow 5-10% of river flow, entrance location optimization, plume distribution
**Safety Considerations**: Flow competition with turbines, attraction effectiveness monitoring, adaptive management

### 3. Fish Counting System Operation
**Entity Type**: MONITORING_SYSTEM
**Description**: Automated video or resistivity counter systems quantifying species-specific passage numbers
**Related Entities**: Biological Monitoring, Species Identification, Regulatory Reporting
**Technical Context**: Vaki Riverwatcher, infrared counters, video analytics, manual validation, species algorithms
**Safety Considerations**: Data accuracy, system calibration, backup counting, statistical validation

### 4. Seasonal Operational Windows
**Entity Type**: OPERATIONAL_SCHEDULING
**Description**: Time-based operation schedules aligned with migration timing for salmon, steelhead, and other species
**Related Entities**: Species Life Cycles, Environmental Compliance, Biological Effectiveness
**Technical Context**: Spring chinook (Mar-Jun), fall chinook (Aug-Oct), steelhead (year-round), lamprey passage
**Safety Considerations**: Critical migration periods, climate change adaptations, delayed migration response

### 5. Fish Lift (Whoosh) System Operation
**Entity Type**: MECHANICAL_SYSTEM
**Description**: Mechanical elevator or lock system transporting fish upstream at high-head dams
**Related Entities**: High-Head Passage, Collection Efficiency, Transport Safety
**Technical Context**: Crowder mechanisms, holding tanks, hopper lifts, 15-minute cycle times, water quality maintenance
**Safety Considerations**: Fish injury prevention, stress minimization, predator exclusion, system reliability

### 6. Debris Removal and Maintenance
**Entity Type**: MAINTENANCE_PROCEDURE
**Description**: Regular cleaning of trash racks, ladder pools, and entrance areas preventing flow obstruction
**Related Entities**: Flow Maintenance, Operational Reliability, Access Safety
**Technical Context**: Automated trash rakes, manual cleaning, flood damage repair, seasonal debris loads
**Safety Considerations**: Worker safety, confined space entry, flow control during maintenance, equipment operation

### 7. Fish Screen System Operation
**Entity Type**: PROTECTIVE_SYSTEM
**Description**: Rotating or stationary screens protecting downstream-migrating juvenile fish from turbine entrainment
**Related Entities**: Juvenile Protection, Bypass Systems, Entrainment Reduction
**Technical Context**: Approach velocity <0.4 ft/s, screen mesh sizing, bypass flow systems, cleaning mechanisms
**Safety Considerations**: Screen integrity, bypass effectiveness, debris accumulation, maintenance access

### 8. Water Quality Monitoring in Ladders
**Entity Type**: ENVIRONMENTAL_MONITORING
**Description**: Continuous monitoring of dissolved oxygen, temperature, and pH in fish passage facilities
**Related Entities**: Fish Health, Passage Success, Regulatory Compliance
**Technical Context**: DO >6 mg/L, temperature <20°C for salmonids, real-time sensors, supplemental aeration
**Safety Considerations**: Hypoxia prevention, thermal barriers, water quality standards, adaptive operations

### 9. Predator Exclusion Management
**Entity Type**: BIOLOGICAL_MANAGEMENT
**Description**: Preventing sea lions, birds, and other predators from accessing fish holding or passage areas
**Related Entities**: Fish Survival, Species Protection, Operational Efficiency
**Technical Context**: Grates, netting, exclusion devices, hazing techniques, monitoring programs
**Safety Considerations**: Non-lethal deterrents, Marine Mammal Protection Act compliance, effectiveness monitoring

### 10. Adult Fish Sorting and Trapping
**Entity Type**: OPERATIONAL_PROCEDURE
**Description**: Selective sorting of adult fish for hatchery broodstock collection or species management
**Related Entities**: Hatchery Integration, Species Management, Harvest Management
**Technical Context**: Sorting gates, fish handling protocols, anesthetic use, transport systems
**Safety Considerations**: Fish stress minimization, handling safety, disease prevention, regulatory compliance

### 11. Lamprey Passage Modifications
**Entity Type**: SPECIALIZED_PASSAGE
**Description**: Specialized substrates and flow conditions facilitating Pacific lamprey upstream migration
**Related Entities**: Non-Salmonid Species, Cultural Resources, Ecological Diversity
**Technical Context**: Roughened surfaces, low-velocity resting areas, auxiliary water systems, lamprey-specific designs
**Safety Considerations**: Species-specific requirements, passage effectiveness research, adaptive management

### 12. Fish Passage Flow Coordination with Generation
**Entity Type**: OPERATIONAL_COORDINATION
**Description**: Balancing fish passage water requirements with hydroelectric generation operations
**Related Entities**: Water Budget, Power Generation, Multi-Objective Operations
**Technical Context**: Passage water 5-15 cfs, generation efficiency impacts, operational flexibility, real-time adjustments
**Safety Considerations**: Minimum flow guarantees, priority during critical periods, generation compensation

### 13. Video Monitoring and Biological Evaluation
**Entity Type**: MONITORING_SYSTEM
**Description**: Underwater video systems documenting fish behavior, passage success, and facility performance
**Related Entities**: Effectiveness Monitoring, Behavioral Research, Adaptive Management
**Technical Context**: Underwater cameras, infrared imaging, DVR storage, remote viewing, behavior analysis
**Safety Considerations**: Camera maintenance, data management, biological interpretation, research coordination

### 14. Ice Management in Fish Passage
**Entity Type**: WINTER_OPERATIONS
**Description**: Preventing ice formation in fish passage facilities during winter steelhead and lamprey migration
**Related Entities**: Seasonal Operations, Species Protection, Operational Reliability
**Technical Context**: Bubbler systems, flow adjustments, de-icing protocols, temperature monitoring
**Safety Considerations**: Ice damage prevention, worker safety, species requirements, operational continuity

### 15. Fish Passage Emergency Shutdown
**Entity Type**: EMERGENCY_PROCEDURE
**Description**: Protocols for safely shutting down passage facilities during mechanical failures or unsafe conditions
**Related Entities**: Emergency Response, Fish Safety, System Reliability
**Technical Context**: Stop-log installation, dewatering procedures, fish salvage, notification requirements
**Safety Considerations**: Fish stranding prevention, rapid response, communication protocols, backup systems

### 16. Bypass Flow System Operation
**Entity Type**: JUVENILE_PASSAGE
**Description**: Surface or deep bypass systems routing downstream-migrating juveniles around turbines
**Related Entities**: Smolt Protection, Survival Improvement, Alternative Passage
**Technical Context**: Surface collectors, sluiceway operations, bypass pipes, tailrace release, survival monitoring
**Safety Considerations**: Bypass effectiveness, predator avoidance, operational flexibility, flow optimization

### 17. Fish Passage Research and Monitoring
**Entity Type**: SCIENTIFIC_PROGRAM
**Description**: Biological studies evaluating passage effectiveness and informing operational improvements
**Related Entities**: Adaptive Management, Regulatory Compliance, Performance Verification
**Technical Context**: PIT tag detection, radio telemetry, survival studies, passage efficiency calculations
**Safety Considerations**: Research coordination, data quality, statistical validity, management applications

### 18. Hatchery Water Supply Coordination
**Entity Type**: OPERATIONAL_COORDINATION
**Description**: Providing reliable water supply from dam operations to adjacent fish hatchery facilities
**Related Entities**: Hatchery Operations, Water Quality, Production Support
**Technical Context**: Water rights, flow reliability, temperature control, pathogen management
**Safety Considerations**: Hatchery production protection, disease prevention, water quality standards

### 19. Fish Passage Lighting Systems
**Entity Type**: BEHAVIORAL_MANAGEMENT
**Description**: Lighting systems influencing fish behavior and passage timing through attraction or deterrence
**Related Entities**: Fish Behavior, Operational Efficiency, Research Applications
**Technical Context**: LED systems, light intensity/wavelength control, photoperiod effects, species-specific responses
**Safety Considerations**: Behavioral effectiveness, energy efficiency, maintenance access, research validation

### 20. Trap-and-Haul Operations
**Entity Type**: ALTERNATIVE_PASSAGE
**Description**: Collecting adult fish below dam and transporting by truck to upstream release locations
**Related Entities**: High-Head Passage, Emergency Operations, Flexible Management
**Technical Context**: Collection facilities, fish transport tanks, oxygenation systems, release protocols
**Safety Considerations**: Fish handling stress, transport mortality, disease transmission, operational logistics

### 21. Fish Passage Compliance Reporting
**Entity Type**: REGULATORY_COMPLIANCE
**Description**: Documentation and reporting of passage operations and biological performance to resource agencies
**Related Entities**: NOAA Fisheries, State Agencies, License Conditions, ESA Compliance
**Technical Context**: Annual reports, passage counts, survival studies, operational metrics, data formats
**Safety Considerations**: Data accuracy, reporting deadlines, agency coordination, adaptive management triggers

### 22. Sound and Vibration Management
**Entity Type**: ENVIRONMENTAL_CONTROL
**Description**: Minimizing underwater noise and vibration affecting fish behavior and passage success
**Related Entities**: Fish Behavior, Acoustic Environment, Turbine Operations
**Technical Context**: Hydrophone monitoring, noise levels, vibration dampening, operational adjustments
**Safety Considerations**: Behavioral impacts, passage delays, species sensitivity, mitigation effectiveness

### 23. Fish Passage Adaptive Management
**Entity Type**: MANAGEMENT_FRAMEWORK
**Description**: Systematic approach to testing operational modifications and evaluating biological responses
**Related Entities**: Performance Improvement, Uncertainty Reduction, Stakeholder Collaboration
**Technical Context**: Hypotheses development, experimental design, statistical analysis, decision frameworks
**Safety Considerations**: Experimental protocols, biological safeguards, stakeholder engagement, regulatory approval

### 24. Climate Change Adaptation Strategies
**Entity Type**: LONG_TERM_PLANNING
**Description**: Operational and structural modifications anticipating climate-driven changes in migration timing and flows
**Related Entities**: Climate Resilience, Species Adaptation, Future Operations
**Technical Context**: Phenology shifts, temperature thresholds, flow regime changes, infrastructure modifications
**Safety Considerations**: Species viability, operational flexibility, infrastructure investment, uncertainty management

## Regulatory Framework
- Endangered Species Act (ESA) Section 7 Consultation
- NOAA Fisheries Biological Opinions
- Clean Water Act Section 401 Certifications
- FERC License Fish Passage Conditions
- State Fish Passage Laws

## Communication Protocols
- PTAGIS: PIT tag data management
- Modbus/SCADA: Facility control
- Video streaming: Remote monitoring
- Data APIs: Agency reporting

## Key Vendors & Systems
- Vaki/Pentair: Fish counting systems
- Whooshh Innovations: Fish transport systems
- ARIS: Acoustic imaging sonar
- Pacific States Marine Fisheries Commission: PTAGIS database
- Biomark: PIT tag systems
