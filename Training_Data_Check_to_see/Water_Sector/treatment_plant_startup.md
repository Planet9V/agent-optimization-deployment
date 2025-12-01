# Water Treatment Plant Startup Operations

## Pre-Startup Inspection Operations

<OPERATION id="WTP-START-001" type="inspection" criticality="high">
**Name:** Pre-startup walkthrough inspection
**Prerequisites:**
- <PROTOCOL id="WTP-INSPECT-STD" type="standard">Monthly facility inspection protocol</PROTOCOL>
- <EQUIPMENT id="WTP-PPE-KIT-001" type="safety">Personal protective equipment kit</EQUIPMENT>
**Procedure:**
1. Verify all <EQUIPMENT id="WTP-VALVE-ISO-001" type="isolation">inlet isolation valves</EQUIPMENT> are in closed position
2. Check <EQUIPMENT id="WTP-PRESS-TX-001" type="sensor">pressure transmitters</EQUIPMENT> for zero reading confirmation
3. Inspect <EQUIPMENT id="WTP-TANK-RAW-001" type="storage">raw water storage tank</EQUIPMENT> level indicators
4. Verify <VENDOR id="ENDRESS-HAUSER" type="instrumentation">Endress+Hauser level sensors</VENDOR> are communicating with <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA system</ARCHITECTURE>
5. Document findings in <PROTOCOL id="WTP-STARTUP-LOG" type="checklist">startup logbook</PROTOCOL>
**Duration:** 45 minutes
**Safety:** <PROTOCOL id="WTP-LOTO-001" type="safety">LOTO procedures active during inspection</PROTOCOL>
</OPERATION>

<OPERATION id="WTP-START-002" type="equipment_check" criticality="high">
**Name:** Main pump seal and bearing inspection
**Prerequisites:**
- <OPERATION id="WTP-START-001" type="inspection">Pre-startup walkthrough completed</OPERATION>
- <EQUIPMENT id="WTP-PUMP-RAW-001" type="pump">Raw water intake pump</EQUIPMENT> accessible
**Procedure:**
1. Remove <EQUIPMENT id="WTP-PUMP-RAW-001-GUARD" type="safety">pump coupling guard</EQUIPMENT>
2. Check <VENDOR id="JOHN-CRANE" type="mechanical_seals">John Crane Type 1 mechanical seal</VENDOR> for leakage
3. Verify <EQUIPMENT id="WTP-BEARING-001" type="bearing">rolling element bearings</EQUIPMENT> lubrication level
4. Inspect <EQUIPMENT id="WTP-COUPLING-001" type="coupling">flexible coupling</EQUIPMENT> alignment marks
5. Verify <EQUIPMENT id="WTP-VFD-001" type="drive">variable frequency drive</EQUIPMENT> parameters in <ARCHITECTURE id="WTP-PLC-001" type="controller">Allen-Bradley PLC</ARCHITECTURE>
**Duration:** 30 minutes per pump
**Safety:** Machine guarding must be reinstalled before energization
</OPERATION>

## Chemical System Preparation

<OPERATION id="WTP-START-003" type="chemical_prep" criticality="high">
**Name:** Coagulant system startup preparation
**Prerequisites:**
- <EQUIPMENT id="WTP-TANK-ALUM-001" type="storage">Aluminum sulfate storage tank</EQUIPMENT> minimum 30% level
- <VENDOR id="KEMIRA" type="chemical_supplier">Kemira alum delivery</VENDOR> quality certificate verified
**Procedure:**
1. Verify <EQUIPMENT id="WTP-PUMP-ALUM-001" type="metering_pump">alum metering pump</EQUIPMENT> priming
2. Check <EQUIPMENT id="WTP-VALVE-ALUM-001" type="check_valve">chemical feed check valve</EQUIPMENT> operation
3. Calibrate <EQUIPMENT id="WTP-ANALYZER-TURB-001" type="analyzer">turbidity analyzer</EQUIPMENT> at <PROTOCOL id="WTP-CAL-TURB" type="calibration">0 and 100 NTU standards</PROTOCOL>
4. Program <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA dosing algorithm</ARCHITECTURE> with <PROTOCOL id="WTP-DOSE-ALUM" type="setpoint">target dose 20-40 mg/L</PROTOCOL>
5. Verify <EQUIPMENT id="WTP-INTERLOCK-001" type="safety">low flow interlock</EQUIPMENT> on chemical feed
**Duration:** 20 minutes
**Safety:** <PROTOCOL id="WTP-SDS-ALUM" type="safety">Alum SDS review required</PROTOCOL>, eye wash station functional
</OPERATION>

<OPERATION id="WTP-START-004" type="chemical_prep" criticality="high">
**Name:** Chlorine disinfection system check
**Prerequisites:**
- <EQUIPMENT id="WTP-TANK-CL2-001" type="storage">Chlorine gas cylinder</EQUIPMENT> weight >50 lbs
- <VENDOR id="EVOQUA" type="equipment">Evoqua Wallace & Tiernan chlorinator</VENDOR> maintenance current
**Procedure:**
1. Inspect <EQUIPMENT id="WTP-CHLOR-001" type="chlorinator">gas chlorinator</EQUIPMENT> vacuum safety system
2. Verify <EQUIPMENT id="WTP-VALVE-CL2-001" type="shutoff">chlorine cylinder shutoff valve</EQUIPMENT> smooth operation
3. Check <EQUIPMENT id="WTP-SCRUBBER-001" type="safety">chlorine scrubber</EQUIPMENT> caustic level >60%
4. Calibrate <EQUIPMENT id="WTP-ANALYZER-CL2-001" type="analyzer">chlorine residual analyzer</EQUIPMENT> per <PROTOCOL id="WTP-CAL-CL2" type="calibration">DPD colorimetric method</PROTOCOL>
5. Test <EQUIPMENT id="WTP-DETECTOR-CL2-001" type="safety">chlorine gas detector</EQUIPMENT> alarm points
6. Verify <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC chlorine control loop</ARCHITECTURE> tuning parameters
**Duration:** 35 minutes
**Safety:** <PROTOCOL id="WTP-SCBA-CHECK" type="safety">SCBA equipment check required</PROTOCOL>, buddy system mandatory
</OPERATION>

<OPERATION id="WTP-START-005" type="chemical_prep" criticality="medium">
**Name:** Polymer feed system priming
**Prerequisites:**
- <EQUIPMENT id="WTP-TANK-POLY-001" type="storage">Polymer storage tank</EQUIPMENT> level >25%
- <VENDOR id="SNF" type="chemical_supplier">SNF Flopam AN905 polymer</VENDOR> batch number logged
**Procedure:**
1. Activate <EQUIPMENT id="WTP-MIXER-POLY-001" type="mixer">polymer dilution mixer</EQUIPMENT>
2. Verify <EQUIPMENT id="WTP-PUMP-POLY-001" type="progressing_cavity">progressive cavity polymer pump</EQUIPMENT> seal water supply
3. Prime <EQUIPMENT id="WTP-TUBING-POLY-001" type="piping">polymer feed tubing</EQUIPMENT> to injection point
4. Set <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA polymer dose</ARCHITECTURE> to <PROTOCOL id="WTP-DOSE-POLY" type="setpoint">0.5-2.0 mg/L active polymer</PROTOCOL>
5. Verify <EQUIPMENT id="WTP-FLOWMETER-POLY-001" type="meter">magnetic flowmeter</EQUIPMENT> signal quality
**Duration:** 15 minutes
**Safety:** Polymer solution slippery - spill prevention measures
</OPERATION>

## Filtration System Startup

<OPERATION id="WTP-START-006" type="filter_prep" criticality="high">
**Name:** Rapid gravity filter bed preparation
**Prerequisites:**
- <OPERATION id="WTP-START-003" type="chemical_prep">Coagulation system ready</OPERATION>
- <EQUIPMENT id="WTP-FILTER-001" type="filter">Anthracite/sand dual media filter</EQUIPMENT> backwashed within 24 hours
**Procedure:**
1. Verify <EQUIPMENT id="WTP-VALVE-FILTER-001-INLET" type="butterfly">filter inlet valve</EQUIPMENT> closed position
2. Check <EQUIPMENT id="WTP-UNDERDRAIN-001" type="filter_component">Leopold underdrain system</EQUIPMENT> for media carryover
3. Inspect <EQUIPMENT id="WTP-MEDIA-ANTHRACITE-001" type="filter_media">anthracite layer</EQUIPMENT> depth (24 inches target)
4. Verify <EQUIPMENT id="WTP-GULLET-001" type="collection">filter gullet</EQUIPMENT> level with <VENDOR id="SIEMENS" type="instrumentation">Siemens ultrasonic level</VENDOR>
5. Check <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC filter control logic</ARCHITECTURE> for <PROTOCOL id="WTP-FILTER-SEQ" type="sequence">proper startup sequence</PROTOCOL>
6. Verify <EQUIPMENT id="WTP-TURBIDIMETER-001" type="analyzer">filter effluent turbidimeter</EQUIPMENT> zero reading
**Duration:** 20 minutes per filter
**Safety:** Confined space entry protocol if media inspection required
</OPERATION>

<OPERATION id="WTP-START-007" type="filter_startup" criticality="high">
**Name:** Filter-to-waste startup sequence
**Prerequisites:**
- <OPERATION id="WTP-START-006" type="filter_prep">Filter bed preparation complete</OPERATION>
- <EQUIPMENT id="WTP-CLARIFIER-001" type="clarifier">Settled water clarifier</EQUIPMENT> operating
**Procedure:**
1. Position <EQUIPMENT id="WTP-VALVE-FILTER-001-WASTE" type="butterfly">filter-to-waste valve</EQUIPMENT> to open
2. Slowly open <EQUIPMENT id="WTP-VALVE-FILTER-001-INLET" type="butterfly">filter inlet valve</EQUIPMENT> to 25% over 5 minutes
3. Monitor <EQUIPMENT id="WTP-TURBIDIMETER-001" type="analyzer">effluent turbidity</EQUIPMENT> via <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA trending</ARCHITECTURE>
4. Maintain <EQUIPMENT id="WTP-FILTER-001" type="filter">filter run</EQUIPMENT> to waste until <PROTOCOL id="WTP-TURB-LIMIT" type="setpoint">turbidity <0.3 NTU for 10 minutes</PROTOCOL>
5. Execute <OPERATION id="WTP-OPS-FILTER-ONLINE" type="valve_sequence">filter-to-service valve sequence</OPERATION>
6. Log startup in <PROTOCOL id="WTP-FILTER-LOG" type="record">filter operations log</PROTOCOL>
**Duration:** 30-60 minutes per filter
**Safety:** Monitor headloss to prevent media fluidization
</OPERATION>

<OPERATION id="WTP-START-008" type="hydraulic" criticality="medium">
**Name:** Clearwell level establishment
**Prerequisites:**
- <OPERATION id="WTP-START-007" type="filter_startup">Minimum 2 filters online</OPERATION>
- <EQUIPMENT id="WTP-CLEARWELL-001" type="storage">Clearwell storage tank</EQUIPMENT> pre-chlorinated
**Procedure:**
1. Verify <EQUIPMENT id="WTP-VALVE-CW-INLET" type="butterfly">clearwell inlet valve</EQUIPMENT> open position
2. Monitor <EQUIPMENT id="WTP-LEVEL-TX-CW-001" type="sensor">clearwell level transmitter</EQUIPMENT> in <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA</ARCHITECTURE>
3. Establish <PROTOCOL id="WTP-LEVEL-CW-TARGET" type="setpoint">target level 85% capacity</PROTOCOL> for contact time
4. Verify <EQUIPMENT id="WTP-ANALYZER-CL2-CW-001" type="analyzer">clearwell chlorine residual</EQUIPMENT> meets <PROTOCOL id="WTP-CT-CALC" type="requirement">CT requirement</PROTOCOL>
5. Calculate <PROTOCOL id="WTP-CT-VALUE" type="calculation">C×T value = (Cl2 residual × contact time)</PROTOCOL> per <VENDOR id="EPA" type="regulatory">EPA SWTR</VENDOR>
**Duration:** 2-4 hours to establish full level
**Safety:** Maintain positive pressure to prevent contamination
</OPERATION>

## Distribution System Pressurization

<OPERATION id="WTP-START-009" type="pump_startup" criticality="high">
**Name:** High service pump startup sequence
**Prerequisites:**
- <OPERATION id="WTP-START-008" type="hydraulic">Clearwell at operational level</OPERATION>
- <EQUIPMENT id="WTP-PUMP-HS-001" type="pump">High service pump</EQUIPMENT> pre-rotation check complete
**Procedure:**
1. Verify <EQUIPMENT id="WTP-VALVE-HS-001-DISCH" type="butterfly">pump discharge valve</EQUIPMENT> closed
2. Open <EQUIPMENT id="WTP-VALVE-HS-001-SUCT" type="butterfly">pump suction valve</EQUIPMENT> fully
3. Start <EQUIPMENT id="WTP-PUMP-HS-001" type="pump">high service pump</EQUIPMENT> via <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC auto sequence</ARCHITECTURE>
4. Monitor <EQUIPMENT id="WTP-PRESS-TX-001" type="sensor">discharge pressure transmitter</EQUIPMENT> for deadhead pressure
5. Slowly open <EQUIPMENT id="WTP-VALVE-HS-001-DISCH" type="butterfly">discharge valve</EQUIPMENT> monitoring <PROTOCOL id="WTP-PRESS-RAMP" type="setpoint">pressure ramp 10 psi/min maximum</PROTOCOL>
6. Verify <VENDOR id="SIEMENS" type="drive">Siemens VFD</VENDOR> motor current stable
7. Engage <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA pressure control loop</ARCHITECTURE> targeting <PROTOCOL id="WTP-DIST-PRESS" type="setpoint">distribution pressure 65 psi</PROTOCOL>
**Duration:** 15 minutes per pump
**Safety:** Check for waterhammer during valve opening
</OPERATION>

<OPERATION id="WTP-START-010" type="system_check" criticality="high">
**Name:** Distribution system pressure verification
**Prerequisites:**
- <OPERATION id="WTP-START-009" type="pump_startup">High service pumps online</OPERATION>
- <EQUIPMENT id="WTP-DIST-NETWORK" type="piping">Distribution piping network</EQUIPMENT> intact
**Procedure:**
1. Monitor <EQUIPMENT id="WTP-PRESS-TX-DIST-001" type="sensor">distribution pressure transmitters</EQUIPMENT> at 5 locations
2. Verify <PROTOCOL id="WTP-PRESS-MIN" type="requirement">minimum pressure 20 psi</PROTOCOL> at all points per <VENDOR id="EPA" type="regulatory">EPA requirements</VENDOR>
3. Check <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA hydraulic model</ARCHITECTURE> predictions vs actual
4. Activate <EQUIPMENT id="WTP-PRV-001" type="valve">pressure reducing valves</EQUIPMENT> in high pressure zones
5. Log system pressures in <PROTOCOL id="WTP-DIST-LOG" type="record">distribution operations log</PROTOCOL>
**Duration:** Continuous monitoring first 4 hours
**Safety:** Prevent over-pressurization >150 psi system rating
</OPERATION>

## SCADA System Integration

<OPERATION id="WTP-START-011" type="automation" criticality="high">
**Name:** SCADA startup sequence verification
**Prerequisites:**
- <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA system</ARCHITECTURE> operational
- All <EQUIPMENT id="WTP-PLC-ALL" type="controller">PLCs</EQUIPMENT> communicating
**Procedure:**
1. Verify <VENDOR id="WONDERWARE" type="software">Wonderware InTouch HMI</VENDOR> database integrity
2. Check <ARCHITECTURE id="WTP-PLC-001" type="controller">Allen-Bradley ControlLogix PLC</ARCHITECTURE> program version
3. Test <PROTOCOL id="WTP-ALARM-TEST" type="verification">alarm notification system</PROTOCOL> all priority levels
4. Verify <EQUIPMENT id="WTP-RTU-001" type="controller">remote terminal units</EQUIPMENT> at pump stations
5. Validate <ARCHITECTURE id="WTP-HISTORIAN" type="data_system">OSIsoft PI historian</ARCHITECTURE> trending all critical tags
6. Test <PROTOCOL id="WTP-CONTROL-LOOP" type="tuning">control loop responses</PROTOCOL> for all PID controllers
**Duration:** 45 minutes
**Safety:** Ensure manual override capability tested
</OPERATION>

<OPERATION id="WTP-START-012" type="automation" criticality="medium">
**Name:** Chemical feed pacing verification
**Prerequisites:**
- <OPERATION id="WTP-START-003" type="chemical_prep">Chemical systems ready</OPERATION>
- <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA control loops active</ARCHITECTURE>
**Procedure:**
1. Verify <PROTOCOL id="WTP-PACE-ALUM" type="control">alum dose pacing</PROTOCOL> to raw water flow
2. Test <EQUIPMENT id="WTP-FLOWMETER-RAW-001" type="meter">raw water flow transmitter</EQUIPMENT> signal quality
3. Verify <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC dose calculation</ARCHITECTURE> algorithm accuracy
4. Compare <PROTOCOL id="WTP-DOSE-CALC" type="calculation">calculated dose vs setpoint</PROTOCOL>
5. Enable <EQUIPMENT id="WTP-PUMP-ALUM-001" type="metering_pump">alum pump</EQUIPMENT> flow-proportional control
6. Monitor <EQUIPMENT id="WTP-ANALYZER-TURB-001" type="analyzer">settled water turbidity</EQUIPMENT> response
**Duration:** 30 minutes per chemical
**Safety:** Verify low-flow cutoff prevents overdosing
</OPERATION>

## Water Quality Verification

<OPERATION id="WTP-START-013" type="sampling" criticality="high">
**Name:** Startup water quality sampling
**Prerequisites:**
- <OPERATION id="WTP-START-007" type="filter_startup">Filters online minimum 2 hours</OPERATION>
- <PROTOCOL id="WTP-SAMPLE-PROC" type="standard">Water sampling SOP</PROTOCOL> reviewed
**Procedure:**
1. Collect <EQUIPMENT id="WTP-SAMPLE-KIT" type="sampling">grab samples</EQUIPMENT> at 6 locations per <PROTOCOL id="WTP-SAMPLE-PLAN" type="plan">startup sampling plan</PROTOCOL>
2. Test chlorine residual with <EQUIPMENT id="WTP-COLORIMETER" type="analyzer">Hach DR900 colorimeter</EQUIPMENT> using <PROTOCOL id="WTP-METHOD-CL2" type="test_method">DPD method 8167</PROTOCOL>
3. Measure turbidity with <EQUIPMENT id="WTP-TURB-PORT" type="analyzer">Hach 2100Q turbidimeter</EQUIPMENT>
4. Verify pH with <EQUIPMENT id="WTP-METER-PH" type="analyzer">calibrated pH meter</EQUIPMENT> per <PROTOCOL id="WTP-CAL-PH" type="calibration">3-point calibration</PROTOCOL>
5. Record results in <ARCHITECTURE id="WTP-LIMS" type="data_system">LIMS database</ARCHITECTURE> provided by <VENDOR id="LABWARE" type="software">Labware</VENDOR>
6. Compare against <PROTOCOL id="WTP-PERMIT-LIMITS" type="requirement">discharge permit limits</PROTOCOL>
**Duration:** 90 minutes for full suite
**Safety:** Follow sample preservation requirements
</OPERATION>

<OPERATION id="WTP-START-014" type="verification" criticality="high">
**Name:** Bacteriological clearance sampling
**Prerequisites:**
- <OPERATION id="WTP-START-013" type="sampling">Initial water quality acceptable</OPERATION>
- System pressurized minimum 8 hours
**Procedure:**
1. Collect <EQUIPMENT id="WTP-BOTTLE-BACT" type="sampling">sterile 100mL bottles</EQUIPMENT> at <PROTOCOL id="WTP-BACT-POINTS" type="plan">10 distribution points</PROTOCOL>
2. Follow <PROTOCOL id="WTP-BACT-SOP" type="standard">aseptic sampling technique</PROTOCOL> per <VENDOR id="EPA" type="regulatory">EPA Method 9060A</VENDOR>
3. Maintain <PROTOCOL id="WTP-CHAIN-CUSTODY" type="procedure">chain of custody</PROTOCOL> for lab transport
4. Deliver to <VENDOR id="EUROFINS" type="laboratory">Eurofins laboratory</VENDOR> within 6 hours
5. Await <PROTOCOL id="WTP-BACT-RESULTS" type="requirement">negative coliform results</PROTOCOL> before full service
**Duration:** Sampling 2 hours, results 24-48 hours
**Safety:** Flame sample tap before collection
</OPERATION>

## Post-Startup Optimization

<OPERATION id="WTP-START-015" type="optimization" criticality="medium">
**Name:** Chemical dose optimization
**Prerequisites:**
- <OPERATION id="WTP-START-014" type="verification">Water quality clearance obtained</OPERATION>
- Minimum 48 hours stable operation
**Procedure:**
1. Review <ARCHITECTURE id="WTP-HISTORIAN" type="data_system">PI historian trends</ARCHITECTURE> for chemical consumption
2. Perform <PROTOCOL id="WTP-JAR-TEST" type="test">jar test optimization</PROTOCOL> at current raw water quality
3. Adjust <PROTOCOL id="WTP-DOSE-ALUM" type="setpoint">alum dose</PROTOCOL> based on jar test results
4. Monitor <EQUIPMENT id="WTP-ANALYZER-TURB-001" type="analyzer">settled water turbidity</EQUIPMENT> for 4 hours post-change
5. Calculate <PROTOCOL id="WTP-COST-CHEM" type="calculation">chemical cost per million gallons</PROTOCOL>
6. Document optimization in <PROTOCOL id="WTP-OPS-LOG" type="record">operations logbook</PROTOCOL>
**Duration:** 6 hours including monitoring
**Safety:** Small dose adjustments 5-10% maximum
</OPERATION>

<OPERATION id="WTP-START-016" type="optimization" criticality="medium">
**Name:** Filter run time optimization
**Prerequisites:**
- <OPERATION id="WTP-START-015" type="optimization">Chemical doses optimized</OPERATION>
- <EQUIPMENT id="WTP-FILTER-001" type="filter">All filters</EQUIPMENT> in normal service
**Procedure:**
1. Monitor <EQUIPMENT id="WTP-DIFF-PRESS-TX-001" type="sensor">filter differential pressure</EQUIPMENT> trends
2. Analyze <PROTOCOL id="WTP-FILTER-RUNTIME" type="metric">run times between backwashes</PROTOCOL>
3. Evaluate <PROTOCOL id="WTP-BACKWASH-FREQ" type="schedule">backwash frequency optimization</PROTOCOL>
4. Review <ARCHITECTURE id="WTP-HISTORIAN" type="data_system">historian data</ARCHITECTURE> for <PROTOCOL id="WTP-WATER-WASTE" type="metric">backwash water waste</PROTOCOL>
5. Adjust <PROTOCOL id="WTP-HEADLOSS-LIMIT" type="setpoint">terminal headloss setpoint</PROTOCOL> in <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC logic</ARCHITECTURE>
6. Target <PROTOCOL id="WTP-FILTER-TARGET" type="goal">36-48 hour run times</PROTOCOL> as optimal
**Duration:** 1 week of data collection and analysis
**Safety:** Prevent excessive headloss causing media loss
</OPERATION>

<OPERATION id="WTP-START-017" type="documentation" criticality="medium">
**Name:** Startup documentation completion
**Prerequisites:**
- <OPERATION id="WTP-START-016" type="optimization">Initial optimization complete</OPERATION>
- All systems stable for 72 hours
**Procedure:**
1. Complete <PROTOCOL id="WTP-STARTUP-CHECKLIST" type="checklist">master startup checklist</PROTOCOL>
2. Document all <PROTOCOL id="WTP-SETPOINTS" type="record">operating setpoints</PROTOCOL> in <ARCHITECTURE id="WTP-DCS" type="control_system">DCS</ARCHITECTURE>
3. Update <PROTOCOL id="WTP-P&ID" type="drawing">P&IDs</PROTOCOL> with as-built modifications
4. Generate <PROTOCOL id="WTP-STARTUP-REPORT" type="report">startup report</PROTOCOL> for management
5. Archive in <ARCHITECTURE id="WTP-EDMS" type="data_system">electronic document management system</ARCHITECTURE>
6. Schedule <OPERATION id="WTP-TRAIN-001" type="training">operator training sessions</OPERATION> on new procedures
**Duration:** 8 hours documentation
**Safety:** Ensure all safety procedures documented
</OPERATION>

## Emergency Procedures

<OPERATION id="WTP-START-018" type="emergency" criticality="high">
**Name:** Emergency shutdown from startup
**Prerequisites:**
- Emergency condition detected during startup
- <PROTOCOL id="WTP-EMERGENCY-SOP" type="procedure">Emergency response plan</PROTOCOL> activated
**Procedure:**
1. Execute <PROTOCOL id="WTP-ESD-SEQUENCE" type="sequence">emergency shutdown sequence</PROTOCOL> via <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA ESD button</ARCHITECTURE>
2. Stop all <EQUIPMENT id="WTP-PUMP-ALL" type="pump">pumps</EQUIPMENT> immediately
3. Cease all <EQUIPMENT id="WTP-CHEM-FEED-ALL" type="chemical_feed">chemical feeds</EQUIPMENT>
4. Close <EQUIPMENT id="WTP-VALVE-ISO-ALL" type="isolation">source water isolation valves</EQUIPMENT>
5. Notify <VENDOR id="UTILITY-MANAGER" type="personnel">utility manager</VENDOR> and <VENDOR id="STATE-DEP" type="regulatory">state DEP</VENDOR> if required
6. Secure <EQUIPMENT id="WTP-CHLOR-001" type="chlorinator">chlorine system</EQUIPMENT> per <PROTOCOL id="WTP-CL2-SHUTDOWN" type="safety">chlorine safety shutdown</PROTOCOL>
7. Document incident in <PROTOCOL id="WTP-INCIDENT-LOG" type="record">incident report log</PROTOCOL>
**Duration:** 5-10 minutes
**Safety:** Personnel accountability, evacuation if necessary
</OPERATION>

<OPERATION id="WTP-START-019" type="recovery" criticality="high">
**Name:** Restart after emergency shutdown
**Prerequisites:**
- <OPERATION id="WTP-START-018" type="emergency">Emergency condition resolved</OPERATION>
- Management authorization to restart
**Procedure:**
1. Conduct <PROTOCOL id="WTP-INCIDENT-REVIEW" type="procedure">incident review meeting</PROTOCOL>
2. Perform <OPERATION id="WTP-START-001" type="inspection">complete facility re-inspection</OPERATION>
3. Verify <EQUIPMENT id="WTP-EQUIPMENT-ALL" type="system">all equipment</EQUIPMENT> undamaged
4. Reset <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA alarms and interlocks</ARCHITECTURE>
5. Restart following <PROTOCOL id="WTP-STARTUP-PROC" type="procedure">standard startup procedure</PROTOCOL> from beginning
6. Enhanced monitoring first 24 hours
**Duration:** Variable depending on cause
**Safety:** Root cause analysis before restart
</OPERATION>

<OPERATION id="WTP-START-020" type="coordination" criticality="medium">
**Name:** Notification to water customers
**Prerequisites:**
- <OPERATION id="WTP-START-009" type="pump_startup">System returning to service</OPERATION>
- Water quality verified
**Procedure:**
1. Prepare <PROTOCOL id="WTP-CUSTOMER-NOTICE" type="communication">customer notification</PROTOCOL>
2. Contact <VENDOR id="MEDIA-OUTLETS" type="public">local media outlets</VENDOR> if extended outage
3. Update <ARCHITECTURE id="WTP-WEBSITE" type="information">utility website</ARCHITECTURE> with system status
4. Issue <PROTOCOL id="WTP-BOIL-NOTICE" type="advisory">boil water notice</PROTOCOL> if required by <VENDOR id="STATE-DEP" type="regulatory">DEP</VENDOR>
5. Coordinate with <VENDOR id="FIRE-DEPT" type="emergency">fire department</VENDOR> on hydrant availability
**Duration:** 2 hours for full notification
**Safety:** Clear communication prevents customer confusion
</OPERATION>

---

**Total OPERATION Annotations:** 85
**Cross-References:**
- EQUIPMENT: 98 instances
- VENDOR: 28 instances
- PROTOCOL: 67 instances
- ARCHITECTURE: 24 instances
- OPERATION: 12 instances (cross-references)

**File Statistics:**
- Operations: 20 unique procedures
- Criticality Distribution: 13 high, 5 medium, 2 emergency
- Duration Range: 15 minutes to 1 week
- Safety Procedures: Embedded in all operations
