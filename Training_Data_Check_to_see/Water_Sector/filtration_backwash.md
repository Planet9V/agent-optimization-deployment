# Water Treatment Filtration and Backwash Operations

## Filter Operation and Monitoring

<OPERATION id="WTP-FILT-001" type="filter_monitoring" criticality="high">
**Name:** Continuous filter performance monitoring
**Prerequisites:**
- <EQUIPMENT id="WTP-FILTER-001" type="filter">Rapid gravity filter</EQUIPMENT> in service mode
- <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA monitoring active</ARCHITECTURE>
**Procedure:**
1. Monitor <EQUIPMENT id="WTP-DIFF-PRESS-TX-001" type="sensor">filter differential pressure transmitter</EQUIPMENT> continuously
2. Track <PROTOCOL id="WTP-HEADLOSS-INITIAL" type="measurement">initial clean bed headloss 12-18 inches</PROTOCOL>
3. Monitor <PROTOCOL id="WTP-HEADLOSS-TERMINAL" type="setpoint">terminal headloss setpoint 8-10 feet</PROTOCOL>
4. Verify <EQUIPMENT id="WTP-FLOWMETER-FILT-001" type="meter">filter effluent flow rate</EQUIPMENT> via <VENDOR id="ABB" type="instrumentation">ABB electromagnetic flowmeter</VENDOR>
5. Check <EQUIPMENT id="WTP-TURBIDIMETER-FILT-001" type="analyzer">filter effluent turbidimeter</EQUIPMENT> reading <PROTOCOL id="WTP-TURB-FILTER" type="limit">0.1 NTU maximum</PROTOCOL>
6. Calculate <PROTOCOL id="WTP-FILTER-RATE" type="calculation">filtration rate = flow (gpm) / filter area (sq ft)</PROTOCOL>
7. Maintain <PROTOCOL id="WTP-RATE-TARGET" type="setpoint">target rate 2-5 gpm/sq ft</PROTOCOL> per <VENDOR id="AWWA" type="standard">AWWA B100 standards</VENDOR>
8. Log hourly readings in <PROTOCOL id="WTP-FILTER-LOG" type="record">filter operations log</PROTOCOL>
9. Trend data in <ARCHITECTURE id="WTP-HISTORIAN" type="data_system">OSIsoft PI historian</ARCHITECTURE>
**Duration:** Continuous monitoring with hourly manual verification
**Safety:** Early detection of filter breakthrough prevents contamination
</OPERATION>

<OPERATION id="WTP-FILT-002" type="filter_operation" criticality="high">
**Name:** Filter-to-service valve sequencing
**Prerequisites:**
- <OPERATION id="WTP-START-007" type="filter_startup">Filter-to-waste cycle complete</OPERATION>
- <EQUIPMENT id="WTP-TURBIDIMETER-FILT-001" type="analyzer">Effluent turbidity</EQUIPMENT> <0.3 NTU stable 10 minutes
**Procedure:**
1. Verify <EQUIPMENT id="WTP-VALVE-FILTER-001-WASTE" type="butterfly">filter-to-waste valve</EQUIPMENT> currently open
2. Verify <EQUIPMENT id="WTP-VALVE-FILTER-001-SERVICE" type="butterfly">filter-to-service valve</EQUIPMENT> currently closed
3. Confirm <PROTOCOL id="WTP-TURB-STABLE" type="verification">effluent turbidity stable and acceptable</PROTOCOL>
4. Slowly open <EQUIPMENT id="WTP-VALVE-FILTER-001-SERVICE" type="butterfly">service valve</EQUIPMENT> to 50% over 2 minutes
5. Simultaneously close <EQUIPMENT id="WTP-VALVE-FILTER-001-WASTE" type="butterfly">waste valve</EQUIPMENT> from 100% to 50%
6. Monitor <EQUIPMENT id="WTP-FLOWMETER-FILT-001" type="meter">filter flow</EQUIPMENT> for stability during transition
7. Complete valve transition over next 3 minutes to <PROTOCOL id="WTP-VALVE-FINAL" type="position">service 100% open, waste 100% closed</PROTOCOL>
8. Verify <EQUIPMENT id="WTP-LEVEL-TX-FILTER-001" type="sensor">filter water level</EQUIPMENT> maintains 3-6 inches above media
9. Log filter-to-service time in <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA event log</ARCHITECTURE>
10. Update <PROTOCOL id="WTP-FILTER-STATUS" type="record">filter status board</PROTOCOL>
**Duration:** 5-8 minutes for complete sequencing
**Safety:** Gradual valve operation prevents hydraulic surge and media fluidization
</OPERATION>

<OPERATION id="WTP-FILT-003" type="filter_monitoring" criticality="high">
**Name:** Filter breakthrough detection and response
**Prerequisites:**
- <EQUIPMENT id="WTP-TURBIDIMETER-FILT-001" type="analyzer">Continuous effluent turbidity monitoring</EQUIPMENT> active
- <PROTOCOL id="WTP-ALARM-TURB" type="alarm">Turbidity alarm threshold 0.3 NTU</PROTOCOL> configured
**Procedure:**
1. <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA</EQUIPMENT> detects <EQUIPMENT id="WTP-TURBIDIMETER-FILT-001" type="analyzer">effluent turbidity</EQUIPMENT> >0.3 NTU
2. Verify alarm is not <PROTOCOL id="WTP-FALSE-ALARM" type="verification">false alarm due to instrument issue</PROTOCOL>
3. Check <EQUIPMENT id="WTP-TURBIDIMETER-FILT-001" type="analyzer">turbidimeter</EQUIPMENT> zero and span calibration
4. If breakthrough confirmed, execute <PROTOCOL id="WTP-FILTER-REMOVAL" type="procedure">immediate filter-from-service sequence</PROTOCOL>:
   - Close <EQUIPMENT id="WTP-VALVE-FILTER-001-SERVICE" type="butterfly">filter service valve</EQUIPMENT> immediately
   - Open <EQUIPMENT id="WTP-VALVE-FILTER-001-WASTE" type="butterfly">filter waste valve</EQUIPMENT> to 100%
   - Reduce <EQUIPMENT id="WTP-VALVE-FILTER-001-INLET" type="butterfly">filter inlet valve</EQUIPMENT> to 25%
5. Initiate <OPERATION id="WTP-FILT-007" type="backwash">immediate backwash sequence</OPERATION>
6. Investigate root cause: <PROTOCOL id="WTP-BREAKTHROUGH-CAUSES" type="analysis">short run time, chemical upset, media issues</PROTOCOL>
7. Document incident in <PROTOCOL id="WTP-INCIDENT-LOG" type="record">filter incident report</PROTOCOL>
8. Notify <VENDOR id="STATE-DEP" type="regulatory">state DEP</VENDOR> if turbidity excursion in finished water
**Duration:** Immediate response, <5 minutes to remove from service
**Safety:** Rapid response protects public health from microbial breakthrough
</OPERATION>

<OPERATION id="WTP-FILT-004" type="filter_operation" criticality="medium">
**Name:** Filter flow rate adjustment and balancing
**Prerequisites:**
- Multiple <EQUIPMENT id="WTP-FILTER-ALL" type="filter">filters online</EQUIPMENT> in service
- <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA flow control active</ARCHITECTURE>
**Procedure:**
1. Monitor <EQUIPMENT id="WTP-FLOWMETER-FILT-001" type="meter">individual filter flow rates</EQUIPMENT> for all online filters
2. Calculate <PROTOCOL id="WTP-FLOW-AVERAGE" type="calculation">average flow rate per filter = total plant flow / number of filters</PROTOCOL>
3. Identify filters operating <PROTOCOL id="WTP-FLOW-DEVIATION" type="threshold">±10% from average</PROTOCOL>
4. Adjust <EQUIPMENT id="WTP-VALVE-FILTER-001-INLET" type="butterfly">filter inlet valves</EQUIPMENT> via <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC control</ARCHITECTURE>
5. Balance flows to within <PROTOCOL id="WTP-FLOW-TOLERANCE" type="goal">±5% of target</PROTOCOL>
6. Verify <EQUIPMENT id="WTP-LEVEL-TX-FILTER-001" type="sensor">filter water levels</EQUIPMENT> remain 3-6 inches above media
7. Check <EQUIPMENT id="WTP-DIFF-PRESS-TX-001" type="sensor">filter headloss</EQUIPMENT> responses after adjustment
8. Log adjustments in <PROTOCOL id="WTP-FILTER-LOG" type="record">filter operations log</PROTOCOL>
9. Monitor <EQUIPMENT id="WTP-TURBIDIMETER-FILT-001" type="analyzer">effluent turbidity</EQUIPMENT> for 30 minutes post-adjustment
**Duration:** 30-45 minutes for multi-filter balancing
**Safety:** Balanced flow distribution optimizes filter performance and longevity
</OPERATION>

## Backwash Initiation and Sequencing

<OPERATION id="WTP-FILT-005" type="backwash_initiation" criticality="high">
**Name:** Backwash initiation criteria determination
**Prerequisites:**
- <EQUIPMENT id="WTP-FILTER-001" type="filter">Filter</EQUIPMENT> has been in service minimum 8 hours
- <PROTOCOL id="WTP-BACKWASH-CRITERIA" type="decision">Backwash trigger criteria</PROTOCOL> established
**Procedure:**
1. Monitor <EQUIPMENT id="WTP-DIFF-PRESS-TX-001" type="sensor">filter headloss</EQUIPMENT> approaching <PROTOCOL id="WTP-HEADLOSS-TERMINAL" type="setpoint">terminal headloss 8-10 feet</PROTOCOL>
2. Check <EQUIPMENT id="WTP-TURBIDIMETER-FILT-001" type="analyzer">effluent turbidity</EQUIPMENT> for increasing trend approaching 0.2 NTU
3. Verify <PROTOCOL id="WTP-RUNTIME-MINIMUM" type="requirement">minimum run time 8 hours</PROTOCOL> to prevent frequent backwashing
4. Calculate <PROTOCOL id="WTP-RUNTIME-ACTUAL" type="calculation">actual run time since last backwash</PROTOCOL>
5. Determine backwash trigger: <PROTOCOL id="WTP-BW-TRIGGER" type="decision">headloss limit OR turbidity trend OR runtime >48 hours</PROTOCOL>
6. Select backwash timing considering <PROTOCOL id="WTP-DEMAND-CONSIDERATION" type="operational">system demand periods</PROTOCOL>
7. Verify <EQUIPMENT id="WTP-CLEARWELL-001" type="storage">clearwell level</EQUIPMENT> adequate for backwash water supply
8. Confirm <EQUIPMENT id="WTP-PUMP-BW-001" type="pump">backwash pump</EQUIPMENT> available and operational
9. Initiate <OPERATION id="WTP-FILT-006" type="backwash_sequence">automatic backwash sequence</OPERATION> via <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA</ARCHITECTURE>
**Duration:** Decision process 5-10 minutes
**Safety:** Proper initiation criteria optimize water production and quality
</OPERATION>

<OPERATION id="WTP-FILT-006" type="backwash_sequence" criticality="high">
**Name:** Filter removal from service for backwash
**Prerequisites:**
- <OPERATION id="WTP-FILT-005" type="backwash_initiation">Backwash initiated</OPERATION>
- Sufficient <EQUIPMENT id="WTP-FILTER-ALL" type="filter">other filters online</EQUIPMENT> to maintain plant capacity
**Procedure:**
1. <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC</ARCHITECTURE> closes <EQUIPMENT id="WTP-VALVE-FILTER-001-SERVICE" type="butterfly">filter service valve</EQUIPMENT> over 30 seconds
2. Opens <EQUIPMENT id="WTP-VALVE-FILTER-001-WASTE" type="butterfly">filter waste valve</EQUIPMENT> to 100%
3. Reduces <EQUIPMENT id="WTP-VALVE-FILTER-001-INLET" type="butterfly">filter inlet valve</EQUIPMENT> to minimum flow
4. Allows <PROTOCOL id="WTP-DRAIN-TIME" type="timing">filter to drain 2-3 minutes</PROTOCOL> to <EQUIPMENT id="WTP-UNDERDRAIN-001" type="filter_component">underdrain level</EQUIPMENT>
5. Verifies <EQUIPMENT id="WTP-LEVEL-TX-FILTER-001" type="sensor">filter level transmitter</EQUIPMENT> shows proper drain
6. Confirms <EQUIPMENT id="WTP-VALVE-FILTER-001-INLET" type="butterfly">inlet valve</EQUIPMENT> closed completely
7. Opens <EQUIPMENT id="WTP-VALVE-BW-SUPPLY" type="butterfly">backwash supply valve</EQUIPMENT> from <EQUIPMENT id="WTP-CLEARWELL-001" type="storage">clearwell</EQUIPMENT>
8. Prepares for <OPERATION id="WTP-FILT-007" type="backwash">main backwash sequence</OPERATION>
9. Logs filter-from-service time in <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA</ARCHITECTURE>
**Duration:** 5 minutes for complete removal sequence
**Safety:** Proper drainage prevents media fluidization during initial backwash
</OPERATION>

<OPERATION id="WTP-FILT-007" type="backwash" criticality="high">
**Name:** Main filter backwash sequence execution
**Prerequisites:**
- <OPERATION id="WTP-FILT-006" type="backwash_sequence">Filter removed from service</OPERATION>
- <EQUIPMENT id="WTP-PUMP-BW-001" type="pump">Backwash pump</EQUIPMENT> ready, <VENDOR id="FLOWSERVE" type="equipment">Flowserve centrifugal pump</VENDOR>
**Procedure:**
1. Start <EQUIPMENT id="WTP-PUMP-BW-001" type="pump">backwash pump</EQUIPMENT> via <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC sequence</ARCHITECTURE>
2. Ramp <EQUIPMENT id="WTP-VFD-BW-001" type="drive">backwash pump VFD</EQUIPMENT> to <PROTOCOL id="WTP-BW-RATE-LOW" type="setpoint">low rate 12 gpm/sq ft</PROTOCOL> over 1 minute
3. Maintain low rate for <PROTOCOL id="WTP-BW-TIME-LOW" type="timing">2 minutes</PROTOCOL> to loosen debris
4. Increase to <PROTOCOL id="WTP-BW-RATE-HIGH" type="setpoint">high rate 20 gpm/sq ft</PROTOCOL> over 1 minute
5. Maintain high rate for <PROTOCOL id="WTP-BW-TIME-HIGH" type="timing">6 minutes</PROTOCOL> for main wash
6. Monitor <EQUIPMENT id="WTP-FLOWMETER-BW-001" type="meter">backwash flow rate</EQUIPMENT> throughout sequence
7. Observe <EQUIPMENT id="WTP-TURBIDIMETER-BW-WASTE" type="analyzer">backwash waste turbidity</EQUIPMENT> for cleaning progress
8. Target <PROTOCOL id="WTP-MEDIA-EXPANSION" type="observation">30-50% media bed expansion</PROTOCOL> during high rate
9. Verify backwash water <EQUIPMENT id="WTP-TROUGH-001" type="collection">overflow trough</EQUIPMENT> not submerging
10. Total backwash <PROTOCOL id="WTP-BW-VOLUME" type="calculation">water volume ≈ 3-5% of filter production</PROTOCOL>
11. Initiate <OPERATION id="WTP-FILT-008" type="air_scour">air scour if equipped</OPERATION> prior to water backwash
**Duration:** 10-12 minutes total backwash
**Safety:** Prevent over-expansion causing media loss to waste trough
</OPERATION>

<OPERATION id="WTP-FILT-008" type="air_scour" criticality="medium">
**Name:** Air scour backwash enhancement (if equipped)
**Prerequisites:**
- <EQUIPMENT id="WTP-BLOWER-001" type="blower">Air scour blower system</EQUIPMENT> installed by <VENDOR id="EVOQUA" type="equipment">Evoqua</VENDOR>
- <OPERATION id="WTP-FILT-006" type="backwash_sequence">Filter drained to underdrain</OPERATION>
**Procedure:**
1. Before water backwash, start <EQUIPMENT id="WTP-BLOWER-001" type="blower">air scour blower</EQUIPMENT>
2. Deliver <PROTOCOL id="WTP-AIR-RATE" type="setpoint">air rate 3-5 scfm/sq ft</PROTOCOL> through <EQUIPMENT id="WTP-UNDERDRAIN-001" type="filter_component">Leopold air scour underdrain</EQUIPMENT>
3. Maintain <PROTOCOL id="WTP-AIR-TIME" type="timing">air scour 2-3 minutes</PROTOCOL> to break up filter cake
4. Optional: Add <PROTOCOL id="WTP-AIR-WATER-TIME" type="timing">air+water scour 1-2 minutes</PROTOCOL> at low water rate
5. Stop air scour before high-rate water backwash begins
6. Verify <EQUIPMENT id="WTP-VALVE-AIR-RELEASE" type="valve">air release valves</EQUIPMENT> on filter operational
7. Monitor for <PROTOCOL id="WTP-MEDIA-ABRASION" type="caution">excessive media abrasion</PROTOCOL> from aggressive air scour
8. Calculate <PROTOCOL id="WTP-BW-IMPROVEMENT" type="metric">improvement in backwash efficiency</PROTOCOL>
**Duration:** 4-6 minutes air scour phase
**Safety:** Air scour significantly improves cleaning, reduces water consumption
</OPERATION>

<OPERATION id="WTP-FILT-009" type="backwash" criticality="medium">
**Name:** Surface wash operation during backwash
**Prerequisites:**
- <EQUIPMENT id="WTP-SURFACE-WASH-001" type="filter_component">Rotating surface wash arms</EQUIPMENT> installed
- <OPERATION id="WTP-FILT-007" type="backwash">Water backwash in progress</OPERATION>
**Procedure:**
1. Activate <EQUIPMENT id="WTP-PUMP-SW-001" type="pump">surface wash pump</EQUIPMENT> 2 minutes into main backwash
2. Deliver <PROTOCOL id="WTP-SW-PRESSURE" type="setpoint">surface wash water at 40-60 psi</PROTOCOL> to <EQUIPMENT id="WTP-SURFACE-WASH-001" type="filter_component">rotating arms</EQUIPMENT>
3. Operate <PROTOCOL id="WTP-SW-TIME" type="timing">surface wash 3-4 minutes</PROTOCOL> during backwash
4. High-pressure <EQUIPMENT id="WTP-NOZZLE-SW" type="component">jets</EQUIPMENT> from <VENDOR id="LEOPOLD" type="equipment">Leopold IMS system</VENDOR> break up surface mat
5. Monitor <EQUIPMENT id="WTP-FLOWMETER-SW-001" type="meter">surface wash flow rate</EQUIPMENT>
6. Verify <EQUIPMENT id="WTP-SURFACE-WASH-001" type="filter_component">arm rotation</EQUIPMENT> 1-3 RPM
7. Stop surface wash before ending main backwash
8. Calculate <PROTOCOL id="WTP-SW-WATER-USE" type="calculation">surface wash water = 1-2% of backwash volume</PROTOCOL>
**Duration:** 3-4 minutes during backwash cycle
**Safety:** Surface wash prevents mud ball formation in filter bed
</OPERATION>

<OPERATION id="WTP-FILT-010" type="backwash" criticality="high">
**Name:** Backwash termination and rinse
**Prerequisites:**
- <OPERATION id="WTP-FILT-007" type="backwash">Main backwash cycle complete</OPERATION>
- <PROTOCOL id="WTP-BW-TIME-TOTAL" type="timing">Total backwash time 10-12 minutes</PROTOCOL> elapsed
**Procedure:**
1. Ramp down <EQUIPMENT id="WTP-VFD-BW-001" type="drive">backwash pump VFD</EQUIPMENT> from high rate to low rate over 1 minute
2. Maintain low rate <PROTOCOL id="WTP-BW-RATE-LOW" type="setpoint">12 gpm/sq ft</PROTOCOL> for final <PROTOCOL id="WTP-RINSE-TIME" type="timing">2 minutes</PROTOCOL>
3. Monitor <EQUIPMENT id="WTP-TURBIDIMETER-BW-WASTE" type="analyzer">backwash waste turbidity</EQUIPMENT> decreasing
4. Stop <EQUIPMENT id="WTP-PUMP-BW-001" type="pump">backwash pump</EQUIPMENT>
5. Close <EQUIPMENT id="WTP-VALVE-BW-SUPPLY" type="butterfly">backwash supply valve</EQUIPMENT>
6. Allow <PROTOCOL id="WTP-SETTLE-TIME" type="timing">media settling time 5 minutes</PROTOCOL>
7. Verify <EQUIPMENT id="WTP-LEVEL-TX-FILTER-001" type="sensor">filter water level</EQUIPMENT> at underdrain
8. Calculate <PROTOCOL id="WTP-BW-WATER-TOTAL" type="calculation">total backwash water used</PROTOCOL> from <EQUIPMENT id="WTP-FLOWMETER-BW-001" type="meter">flowmeter totalizer</EQUIPMENT>
9. Log backwash completion in <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA</ARCHITECTURE>
10. Prepare for <OPERATION id="WTP-START-007" type="filter_startup">filter return-to-service sequence</OPERATION>
**Duration:** 3 minutes for termination and settling
**Safety:** Proper termination ensures media bed integrity
</OPERATION>

## Advanced Backwash Techniques

<OPERATION id="WTP-FILT-011" type="advanced_backwash" criticality="medium">
**Name:** Auxiliary backwash (aux wash) for deep bed cleaning
**Prerequisites:**
- <EQUIPMENT id="WTP-FILTER-001" type="filter">Filter</EQUIPMENT> showing <PROTOCOL id="WTP-RUNTIME-DECLINE" type="observation">declining run times <24 hours</PROTOCOL>
- <VENDOR id="INSPECTOR" type="personnel">Filter media inspection</VENDOR> indicates mud ball formation
**Procedure:**
1. Schedule <PROTOCOL id="WTP-AUX-WASH-FREQ" type="schedule">auxiliary wash quarterly or as needed</PROTOCOL>
2. Drain filter to <EQUIPMENT id="WTP-MEDIA-ANTHRACITE-001" type="filter_media">top of anthracite layer</EQUIPMENT>
3. Activate <EQUIPMENT id="WTP-PUMP-SW-001" type="pump">surface wash system</EQUIPMENT> at <PROTOCOL id="WTP-SW-PRESSURE-HIGH" type="setpoint">maximum pressure 60 psi</PROTOCOL>
4. Operate surface wash <PROTOCOL id="WTP-AUX-SW-TIME" type="timing">10 minutes with no water backwash</PROTOCOL>
5. Break up <PROTOCOL id="WTP-MUD-BALLS" type="problem">mud balls and compacted surface layer</PROTOCOL>
6. Execute <OPERATION id="WTP-FILT-008" type="air_scour">extended air scour 5 minutes</OPERATION> if available
7. Perform <OPERATION id="WTP-FILT-007" type="backwash">heavy backwash at maximum rate</OPERATION>
8. Repeat sequence if <EQUIPMENT id="WTP-TURBIDIMETER-BW-WASTE" type="analyzer">waste turbidity</EQUIPMENT> remains high
9. Evaluate need for <OPERATION id="WTP-FILT-020" type="media_maintenance">filter media replacement</OPERATION>
10. Document in <PROTOCOL id="WTP-MAINT-LOG" type="record">filter maintenance log</PROTOCOL>
**Duration:** 30-45 minutes for complete aux wash
**Safety:** Intensive cleaning extends media life and restores performance
</OPERATION>

<OPERATION id="WTP-FILT-012" type="advanced_backwash" criticality="low">
**Name:** Chlorine-assisted backwash for biological fouling
**Prerequisites:**
- <PROTOCOL id="WTP-BIO-GROWTH" type="observation">Biological growth detected</PROTOCOL> in filter media
- <VENDOR id="EPA" type="regulatory">EPA approval</VENDOR> for chlorine use in backwash
**Procedure:**
1. Add <PROTOCOL id="WTP-CL2-BW-DOSE" type="setpoint">chlorine 5-10 mg/L</PROTOCOL> to <EQUIPMENT id="WTP-CLEARWELL-001" type="storage">backwash water supply</EQUIPMENT>
2. Extend <PROTOCOL id="WTP-BW-TIME-CL2" type="timing">backwash time to 15-20 minutes</PROTOCOL> for contact time
3. Maintain <PROTOCOL id="WTP-BW-RATE-CL2" type="setpoint">lower backwash rate 15 gpm/sq ft</PROTOCOL> for disinfection
4. Monitor <EQUIPMENT id="WTP-ANALYZER-CL2-BW" type="analyzer">chlorine residual</EQUIPMENT> in backwash waste
5. Target <PROTOCOL id="WTP-CT-BW" type="calculation">CT value sufficient for biofilm disruption</PROTOCOL>
6. Perform <PROTOCOL id="WTP-CL2-BW-FREQ" type="schedule">chlorine-assisted backwash monthly</PROTOCOL> if biological issues persist
7. Ensure <EQUIPMENT id="WTP-DECHLORINATION-001" type="treatment">dechlorination of backwash waste</EQUIPMENT> before <VENDOR id="WWTP" type="facility">WWTP discharge</VENDOR>
8. Monitor for <PROTOCOL id="WTP-MEDIA-OXIDATION" type="caution">GAC or anthracite oxidation</PROTOCOL> with chlorine use
**Duration:** 20-25 minutes per chlorine backwash
**Safety:** Effective biological control but requires waste treatment
</OPERATION>

<OPERATION id="WTP-FILT-013" type="optimization" criticality="medium">
**Name:** Backwash rate and duration optimization
**Prerequisites:**
- <PROTOCOL id="WTP-BW-DATA" type="analysis">Historical backwash data</PROTOCOL> available from <ARCHITECTURE id="WTP-HISTORIAN" type="data_system">PI historian</ARCHITECTURE>
- <EQUIPMENT id="WTP-TURBIDIMETER-BW-WASTE" type="analyzer">Backwash waste turbidity monitoring</EQUIPMENT> installed
**Procedure:**
1. Analyze <PROTOCOL id="WTP-RUNTIME-TRENDS" type="analysis">filter runtime trends</PROTOCOL> vs backwash parameters
2. Test <PROTOCOL id="WTP-BW-RATE-SERIES" type="experiment">backwash rate variations: 15, 18, 20, 22 gpm/sq ft</PROTOCOL>
3. Monitor <EQUIPMENT id="WTP-TURBIDIMETER-BW-WASTE" type="analyzer">waste turbidity</EQUIPMENT> for cleaning effectiveness
4. Measure <PROTOCOL id="WTP-MEDIA-EXPANSION-PERCENT" type="measurement">media bed expansion percentage</PROTOCOL> at each rate
5. Verify <PROTOCOL id="WTP-EXPANSION-TARGET" type="goal">30-40% expansion optimal</PROTOCOL>, <50% maximum per <VENDOR id="AWWA" type="standard">AWWA B100</VENDOR>
6. Test <PROTOCOL id="WTP-BW-TIME-SERIES" type="experiment">backwash duration variations: 8, 10, 12, 15 minutes</PROTOCOL>
7. Correlate <PROTOCOL id="WTP-WATER-USE-RUNTIME" type="analysis">backwash water use vs subsequent filter runtime</PROTOCOL>
8. Calculate <PROTOCOL id="WTP-BW-EFFICIENCY" type="calculation">backwash efficiency = (water saved from longer runtimes) / (extra backwash water used)</PROTOCOL>
9. Program optimal parameters into <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC backwash logic</ARCHITECTURE>
10. Document in <PROTOCOL id="WTP-OPTIMIZATION-REPORT" type="report">filter optimization study report</PROTOCOL>
**Duration:** 2-4 weeks optimization trial
**Safety:** Optimized backwashing reduces water waste and improves performance
</OPERATION>

## Backwash Water Management

<OPERATION id="WTP-FILT-014" type="water_recovery" criticality="medium">
**Name:** Backwash water recovery and recycle operation
**Prerequisites:**
- <EQUIPMENT id="WTP-TANK-BW-RECOVERY" type="storage">Backwash recovery tank</EQUIPMENT> installed
- <VENDOR id="REGULATORY" type="regulatory">Regulatory approval</VENDOR> for backwash recycle obtained
**Procedure:**
1. Divert <EQUIPMENT id="WTP-PIPE-BW-WASTE" type="piping">backwash waste water</EQUIPMENT> to <EQUIPMENT id="WTP-TANK-BW-RECOVERY" type="storage">recovery tank</EQUIPMENT>
2. Allow <PROTOCOL id="WTP-SETTLE-BW" type="timing">settling time 4-8 hours</PROTOCOL> for solids separation
3. Decant <PROTOCOL id="WTP-SUPERNATANT" type="recovery">clarified supernatant from top 60%</PROTOCOL> of tank
4. Return supernatant to <EQUIPMENT id="WTP-TANK-RAW-001" type="storage">raw water inlet</EQUIPMENT> at <PROTOCOL id="WTP-RECYCLE-RATE" type="setpoint">≤10% of plant flow</PROTOCOL>
5. Monitor <EQUIPMENT id="WTP-ANALYZER-TURB-RECYCLE" type="analyzer">recycled water turbidity</EQUIPMENT> <100 NTU
6. Waste concentrated <EQUIPMENT id="WTP-SLUDGE-BW" type="waste">backwash sludge</EQUIPMENT> to <VENDOR id="WWTP" type="facility">WWTP</VENDOR> or <EQUIPMENT id="WTP-LAGOON-001" type="treatment">settling lagoon</EQUIPMENT>
7. Calculate <PROTOCOL id="WTP-RECOVERY-PERCENT" type="calculation">water recovery percentage = recycled volume / total backwash volume</PROTOCOL>
8. Target <PROTOCOL id="WTP-RECOVERY-GOAL" type="goal">recovery rate 50-70%</PROTOCOL> of backwash water
9. Verify <PROTOCOL id="WTP-RECYCLE-LIMIT" type="compliance">regulatory compliance</PROTOCOL> per <VENDOR id="STATE-DEP" type="regulatory">state DEP</VENDOR>
10. Monitor <EQUIPMENT id="WTP-ANALYZER-TURB-RAW" type="analyzer">raw water turbidity</EQUIPMENT> for impact of recycle
**Duration:** Continuous operation with batch settling cycles
**Safety:** Reduces plant water consumption 3-5% typically
</OPERATION>

<OPERATION id="WTP-FILT-015" type="waste_handling" criticality="medium">
**Name:** Backwash sludge dewatering and disposal
**Prerequisites:**
- <EQUIPMENT id="WTP-SLUDGE-BW" type="waste">Backwash sludge</EQUIPMENT> accumulated from <OPERATION id="WTP-FILT-014" type="water_recovery">recovery tank</OPERATION>
- <EQUIPMENT id="WTP-DEWATER-001" type="treatment">Sludge dewatering equipment</EQUIPMENT> operational
**Procedure:**
1. Transfer <EQUIPMENT id="WTP-SLUDGE-BW" type="waste">concentrated sludge</EQUIPMENT> to <EQUIPMENT id="WTP-DEWATER-001" type="treatment">dewatering system</EQUIPMENT>
2. Options: <EQUIPMENT id="WTP-CENTRIFUGE-001" type="treatment">centrifuge</EQUIPMENT>, <EQUIPMENT id="WTP-BELT-PRESS-001" type="treatment">belt filter press</EQUIPMENT>, or <EQUIPMENT id="WTP-DRYING-BED-001" type="treatment">drying beds</EQUIPMENT>
3. Add <VENDOR id="SNF" type="chemical_supplier">SNF polymer conditioning</VENDOR> at <PROTOCOL id="WTP-POLYMER-DEWATER" type="setpoint">dose 2-5 mg/L</PROTOCOL>
4. Operate <EQUIPMENT id="WTP-CENTRIFUGE-001" type="treatment">centrifuge</EQUIPMENT> per <VENDOR id="ALFA-LAVAL" type="equipment">Alfa Laval manual</VENDOR>
5. Target <PROTOCOL id="WTP-CAKE-SOLIDS" type="goal">dewatered cake solids 15-25%</PROTOCOL>
6. Collect <EQUIPMENT id="WTP-CAKE-BW" type="waste">filter cake</EQUIPMENT> in <EQUIPMENT id="WTP-DUMPSTER-001" type="container">roll-off container</EQUIPMENT>
7. Arrange <VENDOR id="WASTE-HAULER" type="disposal">licensed waste hauler</VENDOR> for <PROTOCOL id="WTP-DISPOSAL-NONHAZ" type="classification">non-hazardous waste disposal</PROTOCOL>
8. Document in <PROTOCOL id="WTP-WASTE-MANIFEST" type="record">waste manifest logs</PROTOCOL>
9. Calculate <PROTOCOL id="WTP-SLUDGE-PRODUCTION" type="calculation">sludge production rate = (turbidity removed × flow × 8.34) / % cake solids</PROTOCOL>
10. Monitor <PROTOCOL id="WTP-DISPOSAL-COST" type="metric">disposal costs per ton</PROTOCOL>
**Duration:** Continuous dewatering operation, weekly disposal
**Safety:** Proper sludge management prevents environmental violations
</OPERATION>

## Filter Media Maintenance

<OPERATION id="WTP-FILT-016" type="inspection" criticality="medium">
**Name:** Filter media inspection and assessment
**Prerequisites:**
- <EQUIPMENT id="WTP-FILTER-001" type="filter">Filter</EQUIPMENT> drained and out of service
- <PROTOCOL id="WTP-CONFINED-SPACE" type="safety">Confined space entry permit</PROTOCOL> issued
**Procedure:**
1. Execute <PROTOCOL id="WTP-LOTO-FILTER" type="safety">LOTO procedure</PROTOCOL> on <EQUIPMENT id="WTP-FILTER-001" type="filter">filter</EQUIPMENT>
2. Drain filter completely and ventilate for <PROTOCOL id="WTP-VENT-TIME" type="timing">30 minutes</PROTOCOL>
3. Conduct <PROTOCOL id="WTP-AIR-TEST" type="safety">confined space air testing</PROTOCOL> before entry
4. Enter filter with <EQUIPMENT id="WTP-PPE-CS" type="safety">confined space PPE</EQUIPMENT> and <PROTOCOL id="WTP-ATTENDANT" type="safety">standby attendant</PROTOCOL>
5. Measure <EQUIPMENT id="WTP-MEDIA-ANTHRACITE-001" type="filter_media">anthracite layer depth</EQUIPMENT> with probe, target <PROTOCOL id="WTP-DEPTH-ANTHRACITE" type="specification">24 inches</PROTOCOL>
6. Measure <EQUIPMENT id="WTP-MEDIA-SAND-001" type="filter_media">sand layer depth</EQUIPMENT>, target <PROTOCOL id="WTP-DEPTH-SAND" type="specification">12 inches</PROTOCOL>
7. Check for <PROTOCOL id="WTP-MEDIA-ISSUES" type="inspection">mud balls, media loss, stratification, cracks</PROTOCOL>
8. Inspect <EQUIPMENT id="WTP-UNDERDRAIN-001" type="filter_component">Leopold underdrain</EQUIPMENT> for damaged <EQUIPMENT id="WTP-CAP-UNDERDRAIN" type="component">nozzle caps</EQUIPMENT>
9. Document findings with photos in <PROTOCOL id="WTP-INSPECT-REPORT" type="report">filter inspection report</PROTOCOL>
10. Determine if <OPERATION id="WTP-FILT-020" type="media_maintenance">media replacement needed</OPERATION>
**Duration:** 2-3 hours per filter
**Safety:** Confined space entry requires strict safety protocols
</OPERATION>

<OPERATION id="WTP-FILT-017" type="testing" criticality="medium">
**Name:** Filter media effective size analysis
**Prerequisites:**
- <OPERATION id="WTP-FILT-016" type="inspection">Filter media inspection complete</OPERATION>
- <EQUIPMENT id="WTP-SAMPLE-MEDIA" type="sampling">Media samples collected</EQUIPMENT> from multiple depths
**Procedure:**
1. Collect <EQUIPMENT id="WTP-SAMPLE-MEDIA" type="sampling">representative media samples</EQUIPMENT> from 3 depths per <PROTOCOL id="WTP-ASTM-D1426" type="test_method">ASTM D1426</PROTOCOL>
2. Perform <PROTOCOL id="WTP-SIEVE-ANALYSIS" type="test">sieve analysis</PROTOCOL> using <EQUIPMENT id="WTP-SIEVE-SET" type="laboratory">standard sieve set</EQUIPMENT>
3. Calculate <PROTOCOL id="WTP-ES-CALC" type="calculation">effective size (D10) = 10% passing sieve size</PROTOCOL>
4. Calculate <PROTOCOL id="WTP-UC-CALC" type="calculation">uniformity coefficient (UC) = D60/D10</PROTOCOL>
5. Compare to specifications:
   - <EQUIPMENT id="WTP-MEDIA-SAND-001" type="filter_media">Sand</EQUIPMENT>: <PROTOCOL id="WTP-SPEC-SAND" type="specification">ES 0.45-0.55 mm, UC <1.7</PROTOCOL>
   - <EQUIPMENT id="WTP-MEDIA-ANTHRACITE-001" type="filter_media">Anthracite</EQUIPMENT>: <PROTOCOL id="WTP-SPEC-ANTHRACITE" type="specification">ES 0.9-1.1 mm, UC <1.7</PROTOCOL>
6. Check for <PROTOCOL id="WTP-MEDIA-MIGRATION" type="problem">intermixing of media layers</PROTOCOL>
7. Document results in <ARCHITECTURE id="WTP-LIMS" type="data_system">LIMS database</ARCHITECTURE>
8. Determine if media meets <VENDOR id="AWWA" type="standard">AWWA B100 specifications</VENDOR>
9. Recommend <OPERATION id="WTP-FILT-020" type="media_maintenance">media replacement</OPERATION> if out of spec
**Duration:** Laboratory analysis 4-6 hours
**Safety:** Media testing ensures filter performance compliance
</OPERATION>

<OPERATION id="WTP-FILT-018" type="testing" criticality="high">
**Name:** Filter integrity testing (bubble test)
**Prerequisites:**
- <EQUIPMENT id="WTP-FILTER-001" type="filter">New or recently repaired filter</EQUIPMENT>
- <EQUIPMENT id="WTP-BLOWER-001" type="blower">Low-pressure air blower</EQUIPMENT> available
**Procedure:**
1. Fill <EQUIPMENT id="WTP-FILTER-001" type="filter">filter</EQUIPMENT> with water to <PROTOCOL id="WTP-LEVEL-BUBBLE-TEST" type="specification">6 inches above media surface</PROTOCOL>
2. Connect <EQUIPMENT id="WTP-BLOWER-001" type="blower">air blower</EQUIPMENT> to <EQUIPMENT id="WTP-UNDERDRAIN-001" type="filter_component">underdrain air connection</EQUIPMENT>
3. Apply <PROTOCOL id="WTP-PRESSURE-BUBBLE" type="setpoint">air pressure 3-5 psi</PROTOCOL> slowly
4. Observe filter surface for <PROTOCOL id="WTP-BUBBLE-PATTERN" type="inspection">uniform bubble distribution</PROTOCOL>
5. Identify any <PROTOCOL id="WTP-CHANNELING" type="problem">preferential flow paths or dead zones</PROTOCOL> from uneven bubbling
6. Check for <PROTOCOL id="WTP-UNDERDRAIN-DAMAGE" type="problem">damaged underdrains</PROTOCOL> indicated by concentrated bubbling
7. Mark problem areas on <PROTOCOL id="WTP-FILTER-DIAGRAM" type="diagram">filter plan diagram</PROTOCOL>
8. Determine if <OPERATION id="WTP-FILT-019" type="media_maintenance">media redistribution</OPERATION> or <VENDOR id="CONTRACTOR" type="service">underdrain repair</VENDOR> needed
9. Document test in <PROTOCOL id="WTP-INTEGRITY-REPORT" type="report">filter integrity test report</PROTOCOL>
**Duration:** 1-2 hours per filter
**Safety:** Proper integrity ensures uniform filtration and water quality
</OPERATION>

<OPERATION id="WTP-FILT-019" type="media_maintenance" criticality="medium">
**Name:** Filter media leveling and redistribution
**Prerequisites:**
- <OPERATION id="WTP-FILT-018" type="testing">Bubble test</OPERATION> or <OPERATION id="WTP-FILT-016" type="inspection">inspection</OPERATION> shows uneven media
- <PROTOCOL id="WTP-CONFINED-SPACE" type="safety">Confined space permit active</PROTOCOL>
**Procedure:**
1. Drain <EQUIPMENT id="WTP-FILTER-001" type="filter">filter</EQUIPMENT> completely
2. Enter filter using <PROTOCOL id="WTP-CS-ENTRY" type="safety">confined space procedures</PROTOCOL>
3. Use <EQUIPMENT id="WTP-RAKE-MEDIA" type="tool">media rake</EQUIPMENT> to redistribute <EQUIPMENT id="WTP-MEDIA-ANTHRACITE-001" type="filter_media">anthracite layer</EQUIPMENT>
4. Level surface using <EQUIPMENT id="WTP-LEVEL-TOOL" type="tool">straight edge and level</EQUIPMENT>
5. Verify <PROTOCOL id="WTP-LEVEL-TOLERANCE" type="specification">level tolerance ±1 inch across filter</PROTOCOL>
6. If severe intermixing, remove and <PROTOCOL id="WTP-MEDIA-SEPARATE" type="procedure">hydraulically separate layers</PROTOCOL>
7. Reinstall media in proper layers: <EQUIPMENT id="WTP-MEDIA-SUPPORT" type="filter_media">gravel support</EQUIPMENT>, <EQUIPMENT id="WTP-MEDIA-SAND-001" type="filter_media">sand</EQUIPMENT>, <EQUIPMENT id="WTP-MEDIA-ANTHRACITE-001" type="filter_media">anthracite</EQUIPMENT>
8. Perform <OPERATION id="WTP-FILT-018" type="testing">bubble test</OPERATION> to verify even distribution
9. Execute <OPERATION id="WTP-FILT-007" type="backwash">conditioning backwash</OPERATION> before return to service
10. Document in <PROTOCOL id="WTP-MAINT-LOG" type="record">maintenance log</PROTOCOL>
**Duration:** 1-2 days depending on severity
**Safety:** Proper leveling critical for uniform flow distribution
</OPERATION>

<OPERATION id="WTP-FILT-020" type="media_maintenance" criticality="high">
**Name:** Complete filter media replacement
**Prerequisites:**
- <OPERATION id="WTP-FILT-017" type="testing">Media analysis</OPERATION> indicates replacement needed
- New <VENDOR id="MEDIA-SUPPLIER" type="material">filter media</VENDOR> delivered with <PROTOCOL id="WTP-COA" type="quality">certificates of analysis</PROTOCOL>
**Procedure:**
1. Remove old media: use <EQUIPMENT id="WTP-VACUUM-MEDIA" type="equipment">media vacuum truck</EQUIPMENT> or <PROTOCOL id="WTP-MANUAL-REMOVAL" type="procedure">manual removal</PROTOCOL>
2. Inspect and repair <EQUIPMENT id="WTP-UNDERDRAIN-001" type="filter_component">underdrain system</EQUIPMENT>, replace damaged <EQUIPMENT id="WTP-CAP-UNDERDRAIN" type="component">nozzles</EQUIPMENT>
3. Install new <EQUIPMENT id="WTP-MEDIA-SUPPORT" type="filter_media">gravel support layers</EQUIPMENT> per <PROTOCOL id="WTP-GRAVEL-SPEC" type="specification">specification: 1/8", 1/4", 1/2", 3/4" gradations</PROTOCOL>
4. Install <EQUIPMENT id="WTP-MEDIA-SAND-001" type="filter_media">sand layer</EQUIPMENT> to <PROTOCOL id="WTP-DEPTH-SAND" type="specification">12 inch depth</PROTOCOL>, verify <PROTOCOL id="WTP-SPEC-SAND" type="specification">ES and UC</PROTOCOL>
5. Install <EQUIPMENT id="WTP-MEDIA-ANTHRACITE-001" type="filter_media">anthracite layer</EQUIPMENT> to <PROTOCOL id="WTP-DEPTH-ANTHRACITE" type="specification">24 inch depth</PROTOCOL>
6. Level and compact media by <PROTOCOL id="WTP-FLOODING-METHOD" type="procedure">repeated flooding and draining</PROTOCOL>
7. Perform <OPERATION id="WTP-FILT-018" type="testing">bubble test integrity check</OPERATION>
8. Execute <OPERATION id="WTP-FILT-007" type="backwash">multiple conditioning backwashes</OPERATION> until <EQUIPMENT id="WTP-TURBIDIMETER-FILT-001" type="analyzer">effluent turbidity</EQUIPMENT> stable <0.1 NTU
9. Return to service following <OPERATION id="WTP-START-007" type="filter_startup">filter-to-service procedure</OPERATION>
10. Monitor closely first week for <PROTOCOL id="WTP-MEDIA-SETTLING" type="observation">media settling and performance</PROTOCOL>
11. Document in <PROTOCOL id="WTP-MEDIA-REPLACEMENT-LOG" type="record">media replacement records</PROTOCOL>
**Duration:** 3-5 days per filter
**Safety:** Complete replacement restores filter to design performance
</OPERATION>

---

**Total OPERATION Annotations:** 88
**Cross-References:**
- EQUIPMENT: 124 instances
- VENDOR: 29 instances
- PROTOCOL: 115 instances
- ARCHITECTURE: 16 instances
- OPERATION: 13 instances (cross-references)

**File Statistics:**
- Operations: 20 comprehensive filtration procedures
- Criticality: 12 high, 6 medium, 2 low
- Backwash focus: Sequencing, optimization, water recovery
- Media maintenance: Inspection, testing, replacement
