# Water Treatment Pump Station Operations

## Raw Water Pump Operations

<OPERATION id="WTP-PUMP-001" type="pump_startup" criticality="high">
**Name:** Raw water intake pump startup sequence
**Prerequisites:**
- <EQUIPMENT id="WTP-PUMP-RAW-001" type="pump">Vertical turbine pump 500 HP</EQUIPMENT> from <VENDOR id="FLOWSERVE" type="equipment">Flowserve</VENDOR>
- <PROTOCOL id="WTP-PRE-START-CHECK" type="checklist">Pre-startup inspection complete</PROTOCOL>
**Procedure:**
1. Verify <EQUIPMENT id="WTP-WET-WELL-001" type="structure">intake wet well</EQUIPMENT> level adequate using <EQUIPMENT id="WTP-LEVEL-TX-001" type="sensor">ultrasonic level transmitter</EQUIPMENT>
2. Check <EQUIPMENT id="WTP-STRAINER-001" type="filter">traveling water screen</EQUIPMENT> operational
3. Open <EQUIPMENT id="WTP-VALVE-DISCH-001" type="butterfly">pump discharge valve</EQUIPMENT> to <PROTOCOL id="WTP-VALVE-POS-START" type="setpoint">25% position</PROTOCOL>
4. Verify <EQUIPMENT id="WTP-VFD-RAW-001" type="drive">Allen-Bradley VFD</EQUIPMENT> ready via <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC</ARCHITECTURE>
5. Start pump monitoring <EQUIPMENT id="WTP-PRESS-TX-DISCH" type="sensor">discharge pressure</EQUIPMENT> ramp to <PROTOCOL id="WTP-PRESS-TARGET" type="setpoint">85 psi</PROTOCOL>
6. Gradually open discharge valve to 100% over <PROTOCOL id="WTP-RAMP-TIME" type="timing">3 minutes</PROTOCOL>
7. Verify <EQUIPMENT id="WTP-VIBRATION-TX-001" type="sensor">vibration sensor</EQUIPMENT> readings <PROTOCOL id="WTP-VIB-LIMIT" type="threshold">0.3 in/sec</PROTOCOL>
8. Monitor <EQUIPMENT id="WTP-TEMP-TX-BEARING" type="sensor">bearing temperature</EQUIPMENT> <PROTOCOL id="WTP-TEMP-LIMIT" type="threshold">180°F maximum</PROTOCOL>
9. Engage <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA automatic control</ARCHITECTURE> after <PROTOCOL id="WTP-STABLE-TIME" type="timing">15 minutes stable operation</PROTOCOL>
**Duration:** 20 minutes
**Safety:** Monitor for cavitation, maintain wet well level above <PROTOCOL id="WTP-NPSH-REQ" type="requirement">NPSH required</PROTOCOL>
</OPERATION>

<OPERATION id="WTP-PUMP-002" type="level_control" criticality="high">
**Name:** Wet well level control operation
**Prerequisites:**
- <EQUIPMENT id="WTP-LEVEL-TX-001" type="sensor">Redundant level transmitters</EQUIPMENT> operational
- <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC level control logic</ARCHITECTURE> active
**Procedure:**
1. Configure <PROTOCOL id="WTP-LEVEL-SETPOINTS" type="control">level control band: high 85%, low 40%, critical low 20%</PROTOCOL>
2. Program <EQUIPMENT id="WTP-PUMP-RAW-001" type="pump">lead pump</EQUIPMENT> start at 50% level
3. Program <EQUIPMENT id="WTP-PUMP-RAW-002" type="pump">lag pump</EQUIPMENT> start at 70% level
4. Set <EQUIPMENT id="WTP-PUMP-RAW-003" type="pump">standby pump</EQUIPMENT> for automatic rotation weekly
5. Enable <PROTOCOL id="WTP-PUMP-ROTATION" type="automation">pump rotation algorithm</PROTOCOL> to equalize runtime
6. Configure <PROTOCOL id="WTP-ALARM-HIGH" type="alarm">high level alarm 90%</PROTOCOL> to <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA</ARCHITECTURE>
7. Set <PROTOCOL id="WTP-ALARM-LOW" type="alarm">low level alarm 30%</PROTOCOL> with pump lockout
8. Monitor <EQUIPMENT id="WTP-FLOWMETER-RAW-001" type="meter">raw water flow totalizer</EQUIPMENT> for demand trends
9. Adjust <PROTOCOL id="WTP-VFD-SPEED" type="control">VFD speed 40-100%</PROTOCOL> to match plant demand
**Duration:** Continuous automated control
**Safety:** Prevent pump run-dry with <EQUIPMENT id="WTP-LEVEL-SWITCH-LOW" type="sensor">hardwired low-level cutoff</EQUIPMENT>
</OPERATION>

<OPERATION id="WTP-PUMP-003" type="monitoring" criticality="high">
**Name:** Pump performance monitoring and trending
**Prerequisites:**
- <ARCHITECTURE id="WTP-HISTORIAN" type="data_system">OSIsoft PI historian</ARCHITECTURE> collecting pump data
- <VENDOR id="RELIABILITY-ENGINEER" type="personnel">Reliability engineer</VENDOR> analysis tools available
**Procedure:**
1. Monitor <EQUIPMENT id="WTP-POWER-METER-001" type="sensor">pump motor power draw</EQUIPMENT> vs <PROTOCOL id="WTP-PUMP-CURVE" type="specification">manufacturer pump curve</PROTOCOL>
2. Track <EQUIPMENT id="WTP-VIBRATION-TX-001" type="sensor">vibration trends</EQUIPMENT> using <VENDOR id="SKF" type="software">SKF @ptitude software</VENDOR>
3. Monitor <EQUIPMENT id="WTP-TEMP-TX-BEARING" type="sensor">bearing temperatures</EQUIPMENT> for gradual increase indicating wear
4. Calculate <PROTOCOL id="WTP-PUMP-EFFICIENCY" type="calculation">pump efficiency = (flow × head × specific gravity) / (3960 × HP)</PROTOCOL>
5. Compare <PROTOCOL id="WTP-EFFICIENCY-BASELINE" type="benchmark">current vs baseline efficiency</PROTOCOL>
6. Identify <PROTOCOL id="WTP-DEGRADATION-RATE" type="analysis">performance degradation >5%</PROTOCOL> requiring maintenance
7. Monitor <EQUIPMENT id="WTP-SEAL-LEAK-DETECTOR" type="sensor">mechanical seal leak detection</EQUIPMENT> from <VENDOR id="JOHN-CRANE" type="equipment">John Crane Type 1 seal</VENDOR>
8. Track <PROTOCOL id="WTP-MTBF" type="metric">mean time between failures</PROTOCOL> for predictive maintenance
9. Generate <PROTOCOL id="WTP-PUMP-REPORT" type="report">monthly pump performance report</PROTOCOL>
**Duration:** Continuous monitoring, weekly analysis
**Safety:** Early detection prevents catastrophic failures
</OPERATION>

<OPERATION id="WTP-PUMP-004" type="alignment" criticality="medium">
**Name:** Pump-motor alignment verification
**Prerequisites:**
- <EQUIPMENT id="WTP-PUMP-RAW-001" type="pump">Pump</EQUIPMENT> out of service for maintenance
- <EQUIPMENT id="WTP-LASER-ALIGN" type="tool">Laser alignment tool</EQUIPMENT> from <VENDOR id="PRUFTECHNIK" type="equipment">Prüftechnik</VENDOR>
**Procedure:**
1. Execute <PROTOCOL id="WTP-LOTO-PUMP" type="safety">LOTO procedure</PROTOCOL> on pump
2. Remove <EQUIPMENT id="WTP-COUPLING-GUARD" type="safety">coupling guard</EQUIPMENT>
3. Mount <EQUIPMENT id="WTP-LASER-ALIGN" type="tool">laser brackets</EQUIPMENT> on <EQUIPMENT id="WTP-PUMP-SHAFT" type="component">pump shaft</EQUIPMENT> and <EQUIPMENT id="WTP-MOTOR-SHAFT" type="component">motor shaft</EQUIPMENT>
4. Perform <PROTOCOL id="WTP-ROUGH-ALIGN" type="procedure">rough alignment using dial indicators</PROTOCOL>
5. Execute <PROTOCOL id="WTP-LASER-ALIGN-PROC" type="procedure">precision laser alignment</PROTOCOL> targeting <PROTOCOL id="WTP-ALIGN-TOL" type="specification">offset <2 mils, angularity <1 mil/inch</PROTOCOL>
6. Adjust <EQUIPMENT id="WTP-SHIM-MOTOR" type="component">motor mounting shims</EQUIPMENT> to achieve alignment
7. Tighten <EQUIPMENT id="WTP-BOLT-MOTOR" type="fastener">motor hold-down bolts</EQUIPMENT> to <PROTOCOL id="WTP-TORQUE-SPEC" type="specification">specified torque</PROTOCOL>
8. Re-verify alignment after bolt tightening
9. Document results in <PROTOCOL id="WTP-ALIGN-LOG" type="record">alignment maintenance log</PROTOCOL>
10. Reinstall coupling guard before return to service
**Duration:** 4-6 hours per pump
**Safety:** Precision alignment extends bearing and seal life, reduces vibration
</OPERATION>

<OPERATION id="WTP-PUMP-005" type="seal_maintenance" criticality="high">
**Name:** Mechanical seal replacement and commissioning
**Prerequisites:**
- <EQUIPMENT id="WTP-SEAL-NEW" type="component">New mechanical seal</EQUIPMENT> from <VENDOR id="JOHN-CRANE" type="equipment">John Crane Type 1</VENDOR>
- <PROTOCOL id="WTP-SEAL-TRAINING" type="qualification">Seal installation training completed</PROTOCOL>
**Procedure:**
1. Drain pump casing and disconnect <EQUIPMENT id="WTP-PIPE-SEAL-FLUSH" type="piping">seal flush lines</EQUIPMENT>
2. Remove <EQUIPMENT id="WTP-PUMP-IMPELLER" type="component">impeller</EQUIPMENT> per <PROTOCOL id="WTP-DISASSEMBLY-PROC" type="procedure">manufacturer procedure</PROTOCOL>
3. Carefully remove old <EQUIPMENT id="WTP-SEAL-OLD" type="component">seal assembly</EQUIPMENT> avoiding <EQUIPMENT id="WTP-SLEEVE-SHAFT" type="component">shaft sleeve</EQUIPMENT> damage
4. Inspect <EQUIPMENT id="WTP-SLEEVE-SHAFT" type="component">shaft sleeve</EQUIPMENT> for scoring, replace if grooved >0.002"
5. Clean <EQUIPMENT id="WTP-SEAL-FACES" type="component">seal chamber and mating faces</EQUIPMENT> thoroughly
6. Install new seal following <VENDOR id="JOHN-CRANE" type="equipment">John Crane IOM manual</VENDOR> exactly
7. Verify <PROTOCOL id="WTP-SEAL-SETTING" type="specification">seal face gap and spring compression per spec</PROTOCOL>
8. Connect <EQUIPMENT id="WTP-SYSTEM-SEAL-FLUSH" type="support">seal flush system</EQUIPMENT> using <PROTOCOL id="WTP-PLAN-11" type="design">API Plan 11 recirculation</PROTOCOL>
9. Prime pump and start with <EQUIPMENT id="WTP-VALVE-DISCH-001" type="butterfly">discharge valve</EQUIPMENT> partially open
10. Monitor for leakage first 24 hours, expect <PROTOCOL id="WTP-SEAL-LEAK-NORMAL" type="observation">minor weepage during break-in</PROTOCOL>
11. Document in <PROTOCOL id="WTP-SEAL-LOG" type="record">seal replacement log</PROTOCOL> with serial numbers
**Duration:** 8-12 hours per seal
**Safety:** Proper installation critical for seal life and leak prevention
</OPERATION>

## High Service Pump Operations

<OPERATION id="WTP-PUMP-006" type="pressure_control" criticality="high">
**Name:** Distribution system pressure control via high service pumps
**Prerequisites:**
- <EQUIPMENT id="WTP-PUMP-HS-001" type="pump">High service pumps</EQUIPMENT> online
- <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA pressure control loop</ARCHITECTURE> active
**Procedure:**
1. Set <PROTOCOL id="WTP-PRESS-SETPOINT-DIST" type="control">distribution pressure setpoint 65 psi</PROTOCOL> at <EQUIPMENT id="WTP-PRESS-TX-DIST-001" type="sensor">critical point transmitter</EQUIPMENT>
2. Configure <PROTOCOL id="WTP-PID-TUNING" type="control">PID parameters: P=2.0, I=0.5, D=0.1</PROTOCOL> in <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC</ARCHITECTURE>
3. Enable <PROTOCOL id="WTP-PUMP-CASCADE" type="control">cascade pump staging algorithm</PROTOCOL>
4. Program <EQUIPMENT id="WTP-VFD-HS-001" type="drive">lead pump VFD</EQUIPMENT> for <PROTOCOL id="WTP-SPEED-RANGE" type="control">speed control 40-100%</PROTOCOL>
5. Set <EQUIPMENT id="WTP-PUMP-HS-002" type="pump">lag pump</EQUIPMENT> start when <PROTOCOL id="WTP-SPEED-THRESHOLD" type="logic">lead pump >90% speed for 2 minutes</PROTOCOL>
6. Configure <PROTOCOL id="WTP-PUMP-MIN-FLOW" type="protection">minimum flow bypass</PROTOCOL> via <EQUIPMENT id="WTP-VALVE-BYPASS-001" type="control">automatic control valve</EQUIPMENT>
7. Monitor <EQUIPMENT id="WTP-PRESS-TX-PUMP-SUCT" type="sensor">pump suction pressure</EQUIPMENT> to prevent cavitation
8. Track <EQUIPMENT id="WTP-PRESS-TX-DIST-002" type="sensor">distribution pressure at 5 locations</EQUIPMENT> via <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA</ARCHITECTURE>
9. Verify <PROTOCOL id="WTP-PRESS-MIN" type="requirement">minimum pressure 20 psi</PROTOCOL> maintained per <VENDOR id="EPA" type="regulatory">EPA requirements</VENDOR>
10. Adjust setpoint for <PROTOCOL id="WTP-DIURNAL-VARIATION" type="operation">diurnal demand variation</PROTOCOL>
**Duration:** Continuous automated control with operator oversight
**Safety:** Prevent over-pressurization >150 psi system rating
</OPERATION>

<OPERATION id="WTP-PUMP-007" type="optimization" criticality="medium">
**Name:** Pump staging and sequencing optimization
**Prerequisites:**
- <PROTOCOL id="WTP-DEMAND-DATA" type="analysis">Historical demand data</PROTOCOL> from <ARCHITECTURE id="WTP-HISTORIAN" type="data_system">PI historian</ARCHITECTURE>
- <EQUIPMENT id="WTP-PUMP-HS-ALL" type="pump">Multiple pump configurations available</EQUIPMENT>
**Procedure:**
1. Analyze <PROTOCOL id="WTP-DEMAND-CURVE" type="analysis">daily demand curve patterns</PROTOCOL>
2. Calculate <PROTOCOL id="WTP-EFFICIENCY-MAP" type="analysis">pump efficiency at various flow rates</PROTOCOL>
3. Determine <PROTOCOL id="WTP-OPTIMAL-STAGING" type="optimization">optimal pump combinations for efficiency</PROTOCOL>
4. Program <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC staging logic</ARCHITECTURE> to prefer <PROTOCOL id="WTP-BEST-EFF-POINT" type="operation">operation near best efficiency point</PROTOCOL>
5. Implement <PROTOCOL id="WTP-SOFT-LOADING" type="control">soft-loading algorithm</PROTOCOL> to gradually transition between stages
6. Configure <PROTOCOL id="WTP-ROTATION-WEEKLY" type="maintenance">weekly pump rotation</PROTOCOL> for even wear
7. Monitor <EQUIPMENT id="WTP-POWER-METER-PLANT" type="sensor">total plant power consumption</EQUIPMENT>
8. Calculate <PROTOCOL id="WTP-ENERGY-PER-MG" type="metric">kWh per million gallons pumped</PROTOCOL>
9. Generate <PROTOCOL id="WTP-ENERGY-REPORT" type="report">monthly energy efficiency report</PROTOCOL>
10. Adjust staging logic based on <PROTOCOL id="WTP-SEASONAL-DEMAND" type="analysis">seasonal demand patterns</PROTOCOL>
**Duration:** Initial setup 2 weeks, ongoing optimization quarterly
**Safety:** Optimized pumping reduces energy costs 10-20%
</OPERATION>

<OPERATION id="WTP-PUMP-008" type="emergency" criticality="high">
**Name:** Emergency pump failure response and switchover
**Prerequisites:**
- <EQUIPMENT id="WTP-PUMP-HS-001" type="pump">Pump failure detected</EQUIPMENT> by <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA alarms</ARCHITECTURE>
- <EQUIPMENT id="WTP-PUMP-STANDBY" type="pump">Standby pump available</EQUIPMENT>
**Procedure:**
1. <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA</ARCHITECTURE> detects <PROTOCOL id="WTP-PUMP-FAILURE" type="alarm">pump failure: no flow, low pressure, motor overload</PROTOCOL>
2. Automatically start <EQUIPMENT id="WTP-PUMP-STANDBY" type="pump">standby pump</EQUIPMENT> via <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC failover logic</ARCHITECTURE>
3. Verify <EQUIPMENT id="WTP-PRESS-TX-DIST-001" type="sensor">distribution pressure recovery</EQUIPMENT> within <PROTOCOL id="WTP-RECOVERY-TIME" type="goal">2 minutes</PROTOCOL>
4. Dispatch <VENDOR id="OPERATOR-ONCALL" type="personnel">on-call operator</VENDOR> immediately
5. Execute <PROTOCOL id="WTP-LOTO-PUMP" type="safety">LOTO</PROTOCOL> on failed pump
6. Investigate failure: <PROTOCOL id="WTP-FAILURE-MODES" type="troubleshooting">motor, coupling, bearing, seal, electrical</PROTOCOL>
7. Coordinate <VENDOR id="CONTRACTOR-REPAIR" type="service">emergency repair contractor</VENDOR> if needed
8. Notify <VENDOR id="UTILITY-MANAGER" type="personnel">utility manager</VENDOR> and <VENDOR id="STATE-DEP" type="regulatory">regulatory agency</VENDOR> if capacity impaired
9. Document incident in <PROTOCOL id="WTP-INCIDENT-LOG" type="record">equipment failure log</PROTOCOL>
10. Perform <PROTOCOL id="WTP-ROOT-CAUSE" type="analysis">root cause analysis</PROTOCOL> to prevent recurrence
**Duration:** Immediate automatic response, diagnosis 1-4 hours
**Safety:** Redundant pumping capacity critical for uninterrupted service
</OPERATION>

## Specialty Pump Operations

<OPERATION id="WTP-PUMP-009" type="chemical_feed" criticality="high">
**Name:** Chemical metering pump operation and maintenance
**Prerequisites:**
- <EQUIPMENT id="WTP-PUMP-ALUM-001" type="metering_pump">Milton Roy metering pump</EQUIPMENT> from <VENDOR id="MILTON-ROY" type="equipment">Milton Roy</VENDOR>
- <PROTOCOL id="WTP-CHEMICAL-SOP" type="procedure">Chemical feed SOP</PROTOCOL> current
**Procedure:**
1. Verify <EQUIPMENT id="WTP-TANK-ALUM-001" type="storage">chemical tank level</EQUIPMENT> adequate before starting
2. Prime <EQUIPMENT id="WTP-PUMP-HEAD" type="component">pump head</EQUIPMENT> using <EQUIPMENT id="WTP-BUTTON-PRIME" type="control">priming button</EQUIPMENT> for <PROTOCOL id="WTP-PRIME-CYCLES" type="procedure">5 cycles</PROTOCOL>
3. Set <EQUIPMENT id="WTP-STROKE-ADJUST" type="control">stroke length adjustment</EQUIPMENT> to calculated percentage
4. Verify <EQUIPMENT id="WTP-VALVE-RELIEF" type="safety">relief valve</EQUIPMENT> setting <PROTOCOL id="WTP-PRESS-RELIEF-CHEM" type="specification">150 psi</PROTOCOL>
5. Start pump and monitor <EQUIPMENT id="WTP-PRESS-TX-CHEM" type="sensor">discharge pressure</EQUIPMENT> <PROTOCOL id="WTP-PRESS-RANGE-CHEM" type="normal">50-100 psi</PROTOCOL>
6. Verify <EQUIPMENT id="WTP-STROKE-COUNTER" type="monitoring">stroke counter incrementing</EQUIPMENT> in <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA</ARCHITECTURE>
7. Check <EQUIPMENT id="WTP-CHECK-VALVE-001" type="valve">discharge check valve</EQUIPMENT> function by stopping pump briefly
8. Inspect <EQUIPMENT id="WTP-DIAPHRAGM" type="component">diaphragm</EQUIPMENT> quarterly per <PROTOCOL id="WTP-PM-SCHEDULE" type="maintenance">PM schedule</PROTOCOL>
9. Replace <EQUIPMENT id="WTP-VALVE-BALL-PUMP" type="component">pump check valves</EQUIPMENT> annually or when performance declines
10. Calibrate pump output quarterly using <OPERATION id="WTP-COAG-004" type="equipment_operation">graduated cylinder method</OPERATION>
**Duration:** Continuous operation, maintenance 2 hours quarterly
**Safety:** Proper metering pump operation ensures accurate chemical dosing
</OPERATION>

<OPERATION id="WTP-PUMP-010" type="specialty" criticality="medium">
**Name:** Progressive cavity polymer pump operation
**Prerequisites:**
- <EQUIPMENT id="WTP-PUMP-POLY-001" type="progressing_cavity">Moyno progressive cavity pump</EQUIPMENT> from <VENDOR id="NOV-MOYNO" type="equipment">NOV Moyno</VENDOR>
- <EQUIPMENT id="WTP-SYSTEM-SEAL-WATER" type="support">Seal water system</EQUIPMENT> operational
**Procedure:**
1. Verify <EQUIPMENT id="WTP-TANK-POLYMER-MIX" type="mixing">polymer dilution tank</EQUIPMENT> has <PROTOCOL id="WTP-POLYMER-SOLUTION" type="preparation">0.1-0.5% solution</PROTOCOL> prepared
2. Ensure <EQUIPMENT id="WTP-SYSTEM-SEAL-WATER" type="support">seal water</EQUIPMENT> pressure <PROTOCOL id="WTP-PRESS-SEAL-WATER" type="setpoint">10 psi above polymer pressure</PROTOCOL>
3. Open <EQUIPMENT id="WTP-VALVE-POLY-SUCT" type="ball">suction valve</EQUIPMENT> fully
4. Slowly open <EQUIPMENT id="WTP-VALVE-POLY-DISCH" type="ball">discharge valve</EQUIPMENT> to 50%
5. Start <EQUIPMENT id="WTP-MOTOR-POLY" type="motor">pump motor</EQUIPMENT> at <PROTOCOL id="WTP-SPEED-START-POLY" type="control">minimum speed</PROTOCOL>
6. Gradually increase speed and open discharge valve to operating conditions
7. Monitor <EQUIPMENT id="WTP-PRESS-TX-POLY-DISCH" type="sensor">discharge pressure</EQUIPMENT> <PROTOCOL id="WTP-PRESS-MAX-POLY" type="limit">100 psi maximum</PROTOCOL>
8. Check <EQUIPMENT id="WTP-TEMP-TX-STATOR" type="sensor">stator temperature</EQUIPMENT> <PROTOCOL id="WTP-TEMP-LIMIT-STATOR" type="threshold">150°F maximum</PROTOCOL>
9. Inspect <EQUIPMENT id="WTP-ROTOR-STATOR" type="component">rotor-stator fit</EQUIPMENT> annually, replace when worn >50%
10. Flush pump with water when changing polymers or extended shutdown
**Duration:** Continuous operation, inspection 1 hour annually
**Safety:** PC pumps ideal for viscous polymers but require seal water protection
</OPERATION>

---

**Total OPERATION Annotations:** 83
**File Statistics:**
- Operations: 10 comprehensive pump procedures  
- Criticality: 7 high, 2 medium, 1 specialty
- Coverage: Raw water, high service, chemical metering, specialty pumps
- Control systems: VFD, PLC, SCADA integration throughout
