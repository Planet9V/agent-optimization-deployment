# Reservoir Level Control Operations

## Operational Overview
This document details SCADA-based reservoir level control operations, including overflow prevention, drought management, and automated control system procedures for municipal water supply reservoirs.

## Annotations

### 1. Normal Operations - Level Monitoring
**Context**: Continuous monitoring of reservoir water levels using SCADA systems
**ICS Components**: RTU sensors, PLC controllers, HMI displays, ultrasonic level transmitters
**Procedure**: Operators monitor real-time water levels on SCADA HMI screens with high/low alarm setpoints configured at 95% and 20% capacity respectively
**Safety Critical**: Level sensor redundancy required with minimum two independent measurement systems per reservoir
**Standards**: AWWA C606 for level measurement instrumentation
**Vendors**: Siemens SITRANS LUT400 ultrasonic level transmitters, Yokogawa EJA pressure transmitters

### 2. Automated Inlet Control
**Context**: SCADA-controlled inlet valve operation based on reservoir level
**ICS Components**: Motorized butterfly valves, PLC logic controllers, flow meters
**Procedure**: PLC executes proportional-integral control algorithm to modulate inlet valve position maintaining target level setpoint with ±0.5m tolerance
**Safety Critical**: Inlet valve position feedback verification prevents runaway filling conditions
**Standards**: ISA-75.01 control valve sizing standard
**Vendors**: Emerson Fisher Control Valves, AUMA electric actuators

### 3. Overflow Prevention - High Level Response
**Context**: Emergency procedures when reservoir approaches maximum capacity
**ICS Components**: High-level alarm systems, emergency spillway gates, SCADA notification systems
**Procedure**: At 95% capacity trigger Level 1 alarm; at 98% initiate automatic spillway gate opening sequence; at 99.5% activate emergency overflow protocols and notify operations management
**Safety Critical**: Spillway gate position sensors must confirm opening; manual override available for automation failures
**Standards**: USBR Dam Safety Guidelines
**Vendors**: ASCO Red Hat solenoid valves for spillway control, Rotork electric actuators

### 4. Low Level Drought Management
**Context**: Conservation operations during drought conditions or supply shortages
**ICS Components**: Distribution pressure control systems, demand management PLCs
**Procedure**: At 30% capacity implement Stage 1 water restrictions; at 20% reduce distribution network pressure by 10 PSI; at 15% activate emergency water sourcing protocols
**Safety Critical**: Minimum 10% reserve capacity must be maintained for firefighting and critical services
**Standards**: EPA Water Conservation Plan Guidelines
**Vendors**: ABB System 800xA for integrated conservation management

### 5. Inlet Flow Rate Calculation
**Context**: Real-time calculation of optimal inlet flow rates based on demand forecasting
**ICS Components**: Flow computers, SCADA trending software, weather station integration
**Procedure**: SCADA system calculates 24-hour rolling average demand, adjusts inlet flow to maintain target level while accounting for predicted rainfall and evaporation
**Safety Critical**: Flow rate limits prevent water hammer in supply pipelines
**Standards**: AWWA M36 Water Audits and Loss Control Programs
**Vendors**: Honeywell Experion PKS SCADA platform

### 6. Emergency Drawdown Operations
**Context**: Rapid reservoir emptying for dam safety or contamination events
**ICS Components**: Large-diameter drain valves, emergency power systems, downstream flow monitoring
**Procedure**: Activate emergency drawdown at maximum safe rate not exceeding downstream channel capacity; continuous monitoring of structural integrity during drawdown
**Safety Critical**: Downstream flood risk assessment required before initiating drawdown exceeding 500 m³/hour
**Standards**: FEMA Technical Manual for Dam Owners
**Vendors**: VAG Gate Valves for emergency drawdown systems

### 7. Seasonal Level Adjustment
**Context**: Pre-positioning reservoir levels for seasonal demand variations
**ICS Components**: Long-term trending software, automated seasonal scheduling
**Procedure**: Pre-summer filling campaign targets 90% capacity by May 1st; pre-winter drawdown to 70% capacity by November 1st allows for spring melt storage
**Safety Critical**: Seasonal adjustment rates limited to prevent rapid level changes affecting reservoir slopes
**Standards**: USBR Reservoir Operations Guidelines
**Vendors**: OSIsoft PI System for historical trending and seasonal planning

### 8. Multi-Reservoir Cascade Control
**Context**: Coordinated control of multiple interconnected reservoirs
**ICS Components**: Master PLC controllers, inter-reservoir communication networks, cascade control algorithms
**Procedure**: Master controller optimizes water distribution across three reservoirs maintaining aggregate storage target while minimizing pumping costs
**Safety Critical**: Communication failure defaults to independent reservoir control mode
**Standards**: ISA-88 Batch Control Standard (adapted for water systems)
**Vendors**: Rockwell Automation FactoryTalk for cascade control implementation

### 9. Algal Bloom Prevention - Circulation Operations
**Context**: Prevention of stratification and algal blooms through water circulation
**ICS Components**: Submersible circulation pumps, water quality sensors, automated circulation scheduling
**Procedure**: Activate circulation pumps for 4-hour cycles when water temperature exceeds 20°C and dissolved oxygen drops below 6 mg/L at depth
**Safety Critical**: Pump operation monitoring prevents cavitation and equipment damage
**Standards**: EPA Guidelines for Managing Cyanobacteria in Drinking Water
**Vendors**: Medora Corporation SolarBee circulation systems

### 10. Ice Formation Monitoring - Winter Operations
**Context**: Monitoring and management of ice formation on reservoir surface
**ICS Components**: Ice thickness sensors, de-icing aerator systems, intake depth control
**Procedure**: When surface ice thickness exceeds 15cm, activate submerged aerators to prevent complete freeze-over and maintain intake accessibility
**Safety Critical**: Intake structure protection from ice damage requires minimum 3m water depth above intake
**Standards**: Cold Regions Research and Engineering Laboratory (CRREL) guidelines
**Vendors**: Kasco Marine De-Icing systems

### 11. Seismic Event Response Protocol
**Context**: Post-earthquake reservoir inspection and safety procedures
**ICS Components**: Seismic sensors, automated shutdown systems, structural monitoring
**Procedure**: For seismic events >4.0 magnitude within 50km: automatic SCADA alarm, visual dam inspection within 2 hours, structural assessment before resuming normal operations
**Safety Critical**: Precautionary drawdown initiated if any structural concerns identified
**Standards**: ASDSO Guidelines for Seismic Evaluation
**Vendors**: Kinemetrics seismic monitoring systems for dam safety

### 12. Turbidity Management - Storm Inflow Control
**Context**: Managing high turbidity during storm events and runoff
**ICS Components**: Turbidity sensors, inlet valve control, settling basin management
**Procedure**: When inlet turbidity exceeds 50 NTU, reduce inlet flow rate by 50% and divert to settling basin; resume normal operations when turbidity drops below 25 NTU
**Safety Critical**: Turbidity exceedances above 100 NTU trigger treatment plant notification
**Standards**: EPA Surface Water Treatment Rule
**Vendors**: Hach Solitax turbidity sensors

### 13. Power Outage - Emergency Operations
**Context**: Reservoir operations during electrical power failures
**ICS Components**: Backup generators, battery-backed UPS systems, manual valve controls
**Procedure**: Upon power loss, SCADA systems switch to UPS power (4-hour capacity); generator auto-starts within 30 seconds; critical monitoring continues on backup power
**Safety Critical**: Manual valve operation procedures documented for complete power failure scenarios
**Standards**: IEEE 446 Emergency and Standby Power Systems
**Vendors**: Caterpillar diesel generators, Eaton UPS systems

### 14. Wildlife Exclusion - Intake Protection
**Context**: Preventing wildlife entry and protecting aquatic life at intakes
**ICS Components**: Intake screen differential pressure sensors, automated screen cleaning systems
**Procedure**: Monitor screen differential pressure; activate automated brush cleaning system when pressure differential exceeds 0.5 PSI; manual inspection required for persistent blockages
**Safety Critical**: Intake velocity maintained below 0.5 ft/s to protect fish populations
**Standards**: EPA 316(b) Rule for Cooling Water Intake Structures (adapted)
**Vendors**: Hydrolox intake screen systems

### 15. Evaporation Compensation Calculations
**Context**: Accounting for water loss due to evaporation in inventory management
**ICS Components**: Weather stations, evaporation models, inventory reconciliation software
**Procedure**: SCADA calculates daily evaporation loss using Penman equation with local temperature, humidity, wind speed, and solar radiation data; adjusts inventory calculations accordingly
**Safety Critical**: Evaporation losses averaged 2-8mm per day depending on climate; significant discrepancies trigger leak investigation
**Standards**: FAO Irrigation and Drainage Paper 56 for evapotranspiration calculations
**Vendors**: Campbell Scientific weather stations, Aquatic Informatics AQUARIUS for water balance calculations

### 16. Intake Depth Optimization
**Context**: Adjusting intake depth to draw highest quality water from stratified reservoir
**ICS Components**: Motorized intake gates, multi-level water quality sensors, stratification monitoring
**Procedure**: During summer stratification, draw from thermocline depth (typically 8-12m) where temperature and dissolved oxygen are optimal; adjust intake depth daily based on vertical water quality profiles
**Safety Critical**: Avoid drawing from hypolimnion layer with low dissolved oxygen and high manganese
**Standards**: AWWA M21 Groundwater manual (stratification principles)
**Vendors**: YSI EXO multi-parameter sondes for vertical profiling

### 17. Security Perimeter Monitoring
**Context**: Physical security monitoring of reservoir infrastructure
**ICS Components**: CCTV cameras, motion sensors, access control systems integrated with SCADA
**Procedure**: 24/7 video surveillance with motion detection triggers SCADA alarms; security breach initiates lockdown protocols and law enforcement notification
**Safety Critical**: Tampering with intake structures or control systems classified as critical infrastructure attack
**Standards**: AWWA G430 Security Practices for Operation and Management
**Vendors**: Axis Communications IP cameras, Genetec Security Center

### 18. Sediment Accumulation Management
**Context**: Long-term monitoring and management of reservoir sediment buildup
**ICS Components**: Bathymetric survey systems, sediment density sensors, historical trending
**Procedure**: Annual bathymetric surveys assess sediment accumulation rates; when active storage capacity reduced by 10%, schedule sediment removal operations or intake structure modification
**Safety Critical**: Sediment accumulation affects storage calculations and can impact intake operation
**Standards**: USBR Erosion and Sedimentation Manual
**Vendors**: SonTek acoustic Doppler profilers for sediment monitoring

### 19. Chemical Treatment - Algaecide Application
**Context**: Application of copper sulfate or other algaecides for algae control
**ICS Components**: Chemical dosing pumps, boat-mounted application systems, water quality monitoring
**Procedure**: When chlorophyll-a exceeds 30 μg/L, apply copper sulfate at 0.5 mg/L concentration in affected areas; monitor copper residual levels to ensure compliance with drinking water standards
**Safety Critical**: Copper levels must remain below 1.3 mg/L EPA action level
**Standards**: EPA Registration of Pesticides for use in Water Systems
**Vendors**: SePRO AquaStrike algaecide products

### 20. Instrumentation Calibration Schedule
**Context**: Routine calibration and maintenance of reservoir monitoring instruments
**ICS Components**: Level sensors, flow meters, water quality instruments, SCADA I/O modules
**Procedure**: Quarterly calibration of level transmitters against surveyed benchmarks; annual calibration of flow meters using ultrasonic reference; monthly verification of water quality sensor accuracy
**Safety Critical**: Out-of-calibration sensors can trigger false alarms or mask actual problems
**Standards**: ISA-67.06 Calibration Systems
**Vendors**: Beamex calibration management software and equipment

### 21. Boat-Based Inspection Operations
**Context**: Routine visual inspection of reservoir infrastructure from watercraft
**ICS Components**: Safety equipment, inspection checklists, communication systems
**Procedure**: Monthly boat inspection of dam face, spillway structures, intake towers, and shoreline infrastructure; observations logged in SCADA maintenance module
**Safety Critical**: Two-person minimum crew for all boat operations; life jackets and emergency communications required
**Standards**: OSHA 1910.134 confined space and water safety standards
**Vendors**: Standard marine safety equipment

### 22. Aquatic Vegetation Management
**Context**: Control of invasive aquatic vegetation affecting reservoir operations
**ICS Components**: Vegetation mapping systems, GPS-guided harvesting equipment
**Procedure**: Annual vegetation survey identifies problem areas; mechanical harvesting scheduled when vegetation density exceeds 40% coverage in operational zones near intakes
**Safety Critical**: Herbicide application near drinking water intakes requires EPA approval and public notification
**Standards**: EPA Aquatic Plant Control guidelines
**Vendors**: Aquarius Systems mechanical harvesters

### 23. Recreational User Safety - Restricted Zones
**Context**: Managing recreational use around operational infrastructure
**ICS Components**: Buoy systems, signage, public address systems, patrol boats
**Procedure**: 100m restricted zone around all intake structures and 50m zone around spillway clearly marked with buoys; violators warned via PA system; repeated violations reported to law enforcement
**Safety Critical**: Suction hazards near intakes can cause drowning
**Standards**: USBR Recreational Policy
**Vendors**: Sealite navigational buoys

### 24. Data Historian and Reporting
**Context**: Long-term data storage and regulatory reporting from SCADA systems
**ICS Components**: Data historians, automated report generation, regulatory submission systems
**Procedure**: SCADA historian stores all operational data at 1-minute resolution for minimum 7 years; automated monthly reports generated for regulatory agencies showing compliance with operating permits
**Safety Critical**: Data integrity and cybersecurity essential for regulatory compliance
**Standards**: EPA Safe Drinking Water Information System (SDWIS) reporting requirements
**Vendors**: OSIsoft PI Historian, GE Proficy Historian, Wonderware Historian

## System Integration Notes
All reservoir control operations integrate with centralized water utility SCADA systems. Real-time data exchange with water treatment plants ensures coordinated operations across the entire water supply chain.

## Emergency Contact Protocols
Operations center maintains 24/7 staffing with escalation procedures to management, dam safety engineers, and emergency services as required by operational conditions.
