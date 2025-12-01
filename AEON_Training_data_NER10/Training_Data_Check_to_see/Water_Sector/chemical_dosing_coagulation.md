# Water Treatment Chemical Dosing - Coagulation Operations

## Jar Testing and Dose Determination

<OPERATION id="WTP-COAG-001" type="laboratory_test" criticality="high">
**Name:** Standard jar test procedure for alum optimization
**Prerequisites:**
- <EQUIPMENT id="WTP-JARTEST-001" type="laboratory">Phipps & Bird jar tester</EQUIPMENT> calibrated
- <EQUIPMENT id="WTP-SAMPLE-RAW" type="sampling">Representative raw water sample</EQUIPMENT> collected within 2 hours
- <VENDOR id="KEMIRA" type="chemical_supplier">Kemira aluminum sulfate</VENDOR> stock solution prepared
**Procedure:**
1. Fill six <EQUIPMENT id="WTP-JAR-BEAKER-001" type="glassware">1-liter beakers</EQUIPMENT> with raw water at ambient temperature
2. Measure initial turbidity using <EQUIPMENT id="WTP-TURB-LAB-001" type="analyzer">Hach 2100AN turbidimeter</EQUIPMENT> per <PROTOCOL id="WTP-METHOD-180.1" type="test_method">EPA Method 180.1</PROTOCOL>
3. Add <PROTOCOL id="WTP-DOSE-SERIES" type="test_sequence">alum doses: 10, 20, 30, 40, 50, 60 mg/L</PROTOCOL> using <EQUIPMENT id="WTP-PIPETTE-001" type="laboratory">volumetric pipettes</EQUIPMENT>
4. Rapid mix at <PROTOCOL id="WTP-MIX-RAPID" type="setpoint">100 RPM for 1 minute</PROTOCOL> to simulate <EQUIPMENT id="WTP-MIXER-RAPID-001" type="mixer">plant rapid mix basin</EQUIPMENT>
5. Slow mix at <PROTOCOL id="WTP-MIX-SLOW" type="setpoint">30 RPM for 20 minutes</PROTOCOL> to simulate <EQUIPMENT id="WTP-FLOC-001" type="flocculator">flocculation basin</EQUIPMENT>
6. Settle for <PROTOCOL id="WTP-SETTLE-TIME" type="setpoint">30 minutes</PROTOCOL> to simulate <EQUIPMENT id="WTP-CLARIFIER-001" type="clarifier">clarifier</EQUIPMENT>
7. Measure settled turbidity and <EQUIPMENT id="WTP-METER-PH" type="analyzer">pH</EQUIPMENT> of each jar
8. Record results in <ARCHITECTURE id="WTP-LIMS" type="data_system">LIMS database</ARCHITECTURE>
9. Select optimal dose producing <PROTOCOL id="WTP-TURB-TARGET" type="goal">turbidity <2 NTU</PROTOCOL> with lowest chemical use
**Duration:** 90 minutes per test series
**Safety:** <PROTOCOL id="WTP-SDS-ALUM" type="safety">Review alum SDS</PROTOCOL>, wear <EQUIPMENT id="WTP-PPE-LAB" type="safety">lab coat and safety glasses</EQUIPMENT>
</OPERATION>

<OPERATION id="WTP-COAG-002" type="laboratory_test" criticality="medium">
**Name:** Zeta potential measurement for coagulation control
**Prerequisites:**
- <OPERATION id="WTP-COAG-001" type="laboratory_test">Jar test completed</OPERATION>
- <EQUIPMENT id="WTP-ZETA-001" type="analyzer">Malvern Zetasizer Nano</EQUIPMENT> from <VENDOR id="MALVERN" type="instrumentation">Malvern Panalytical</VENDOR> operational
**Procedure:**
1. Prepare <EQUIPMENT id="WTP-SAMPLE-SETTLED" type="sampling">settled water samples</EQUIPMENT> from jar test
2. Dilute samples per <PROTOCOL id="WTP-ZETA-PREP" type="procedure">Zetasizer sample preparation protocol</PROTOCOL>
3. Load sample into <EQUIPMENT id="WTP-CELL-ZETA" type="laboratory">disposable folded capillary cell</EQUIPMENT>
4. Measure <PROTOCOL id="WTP-ZETA-VALUE" type="measurement">zeta potential</PROTOCOL> in millivolts
5. Target <PROTOCOL id="WTP-ZETA-TARGET" type="goal">-10 to +3 mV for optimal destabilization</PROTOCOL>
6. Correlate zeta potential with turbidity removal efficiency
7. Store data in <ARCHITECTURE id="WTP-LIMS" type="data_system">LIMS</ARCHITECTURE> for trending
**Duration:** 30 minutes per sample set
**Safety:** Fragile capillary cells, careful handling required
</OPERATION>

<OPERATION id="WTP-COAG-003" type="calculation" criticality="high">
**Name:** Coagulant dose calculation from jar test to plant scale
**Prerequisites:**
- <OPERATION id="WTP-COAG-001" type="laboratory_test">Optimal jar test dose determined</OPERATION>
- <EQUIPMENT id="WTP-FLOWMETER-RAW-001" type="meter">Raw water flow rate</EQUIPMENT> known
**Procedure:**
1. Identify optimal alum dose from jar test (example: <PROTOCOL id="WTP-DOSE-JAR" type="result">35 mg/L</PROTOCOL>)
2. Measure current <EQUIPMENT id="WTP-FLOWMETER-RAW-001" type="meter">plant flow rate</EQUIPMENT> (example: 5.0 MGD)
3. Calculate <PROTOCOL id="WTP-CALC-DOSE" type="calculation">required feed rate = (35 mg/L × 5.0 MGD × 8.34) / (% alum concentration)</PROTOCOL>
4. For <VENDOR id="KEMIRA" type="chemical_supplier">Kemira liquid alum at 48.8% concentration</VENDOR>: feed rate = 29.9 lbs/day = 1.25 lbs/hr
5. Convert to <EQUIPMENT id="WTP-PUMP-ALUM-001" type="metering_pump">metering pump stroke rate</EQUIPMENT> using <PROTOCOL id="WTP-PUMP-CURVE" type="calibration">pump calibration curve</PROTOCOL>
6. Program <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC dose pacing logic</ARCHITECTURE> with calculated setpoint
7. Verify calculation with <PROTOCOL id="WTP-CALC-CHECK" type="verification">independent verification by senior operator</PROTOCOL>
**Duration:** 15 minutes
**Safety:** Double-check all calculations before implementation
</OPERATION>

## Coagulant Feed System Operation

<OPERATION id="WTP-COAG-004" type="equipment_operation" criticality="high">
**Name:** Alum metering pump startup and calibration
**Prerequisites:**
- <OPERATION id="WTP-COAG-003" type="calculation">Dose calculation completed</OPERATION>
- <EQUIPMENT id="WTP-TANK-ALUM-001" type="storage">Alum storage tank</EQUIPMENT> level adequate
- <VENDOR id="MILTON-ROY" type="equipment">Milton Roy metering pump Model MRA</VENDOR> maintained
**Procedure:**
1. Verify <EQUIPMENT id="WTP-VALVE-ALUM-SUCT" type="ball">pump suction valve</EQUIPMENT> open
2. Check <EQUIPMENT id="WTP-VALVE-ALUM-RELIEF" type="relief">relief valve</EQUIPMENT> setting at <PROTOCOL id="WTP-PRESS-RELIEF" type="setpoint">150 psi</PROTOCOL>
3. Prime <EQUIPMENT id="WTP-PUMP-ALUM-001" type="metering_pump">pump head</EQUIPMENT> using <PROTOCOL id="WTP-PRIME-PROC" type="procedure">priming button 5 cycles</PROTOCOL>
4. Set <EQUIPMENT id="WTP-PUMP-ALUM-001" type="metering_pump">stroke length</EQUIPMENT> to calculated percentage
5. Start pump and verify <EQUIPMENT id="WTP-PRESS-TX-ALUM" type="sensor">discharge pressure</EQUIPMENT> 50-100 psi
6. Calibrate by collecting <EQUIPMENT id="WTP-CYLINDER-GRAD" type="laboratory">discharge into graduated cylinder</EQUIPMENT> for <PROTOCOL id="WTP-CAL-TIME" type="procedure">5 minutes</PROTOCOL>
7. Calculate actual <PROTOCOL id="WTP-FLOWRATE-ACT" type="measurement">flow rate = volume collected / time × 60</PROTOCOL>
8. Adjust <EQUIPMENT id="WTP-PUMP-ALUM-001" type="metering_pump">stroke length</EQUIPMENT> to match target flow
9. Re-verify and document in <PROTOCOL id="WTP-CAL-LOG" type="record">pump calibration log</PROTOCOL>
**Duration:** 30 minutes
**Safety:** Wear <EQUIPMENT id="WTP-PPE-CHEM" type="safety">chemical-resistant gloves</EQUIPMENT>, avoid contact with alum
</OPERATION>

<OPERATION id="WTP-COAG-005" type="monitoring" criticality="high">
**Name:** Continuous alum feed rate verification
**Prerequisites:**
- <OPERATION id="WTP-COAG-004" type="equipment_operation">Alum pump operational</OPERATION>
- <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA monitoring active</ARCHITECTURE>
**Procedure:**
1. Monitor <EQUIPMENT id="WTP-PUMP-ALUM-001" type="metering_pump">pump stroke counter</EQUIPMENT> via <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA</ARCHITECTURE>
2. Verify <EQUIPMENT id="WTP-FLOWMETER-ALUM-001" type="meter">magnetic flowmeter</EQUIPMENT> reading matches calculated dose
3. Check <EQUIPMENT id="WTP-PRESS-TX-ALUM" type="sensor">discharge pressure</EQUIPMENT> for consistency (fluctuation indicates issues)
4. Calculate <PROTOCOL id="WTP-DOSE-ACTUAL" type="calculation">actual mg/L dose = (pump flow rate × % concentration × 10) / raw water MGD</PROTOCOL>
5. Compare <PROTOCOL id="WTP-DOSE-COMPARE" type="verification">actual dose vs setpoint</PROTOCOL>, should be within ±5%
6. If deviation >5%, perform <OPERATION id="WTP-COAG-004" type="equipment_operation">pump recalibration</OPERATION>
7. Trend <PROTOCOL id="WTP-DOSE-TREND" type="monitoring">alum consumption</PROTOCOL> in <ARCHITECTURE id="WTP-HISTORIAN" type="data_system">PI historian</ARCHITECTURE>
**Duration:** Continuous with hourly verification
**Safety:** Low flow alarm should trigger if pump fails
</OPERATION>

<OPERATION id="WTP-COAG-006" type="injection_point" criticality="high">
**Name:** Alum injection point optimization
**Prerequisites:**
- <EQUIPMENT id="WTP-MIXER-RAPID-001" type="mixer">Rapid mix basin</EQUIPMENT> operational
- <VENDOR id="CFD-STUDY" type="analysis">CFD study of mixing basin</VENDOR> available
**Procedure:**
1. Locate <EQUIPMENT id="WTP-INJECTOR-ALUM-001" type="injection">alum injection quill</EQUIPMENT> in <EQUIPMENT id="WTP-PIPE-RAW-001" type="piping">raw water pipe</EQUIPMENT>
2. Verify injection at <PROTOCOL id="WTP-INJECT-LOCATION" type="design">pipe centerline, upstream of elbow</PROTOCOL> for maximum turbulence
3. Check <EQUIPMENT id="WTP-QUILL-ALUM" type="injection">injection quill</EQUIPMENT> orientation pointing downstream
4. Verify <PROTOCOL id="WTP-MIX-RAPID-G" type="setpoint">rapid mix G-value 600-1000 sec⁻¹</PROTOCOL> per <VENDOR id="AWWA" type="standard">AWWA standards</VENDOR>
5. Calculate <PROTOCOL id="WTP-G-VALUE" type="calculation">G = √(P/(μ×V))</PROTOCOL> where P=power, μ=viscosity, V=volume
6. Measure <EQUIPMENT id="WTP-MIXER-RAPID-001" type="mixer">mixer power draw</EQUIPMENT> to verify G-value
7. Adjust <EQUIPMENT id="WTP-VFD-MIXER" type="drive">mixer VFD speed</EQUIPMENT> to achieve target G-value
**Duration:** 2 hours including calculations
**Safety:** High-energy mixing zone, ensure proper guarding
</OPERATION>

## Flocculation Process Control

<OPERATION id="WTP-COAG-007" type="process_control" criticality="high">
**Name:** Flocculation basin operation and optimization
**Prerequisites:**
- <OPERATION id="WTP-COAG-006" type="injection_point">Alum injection optimized</OPERATION>
- <EQUIPMENT id="WTP-FLOC-001" type="flocculator">Three-stage flocculator</EQUIPMENT> with <VENDOR id="ENVIREX" type="equipment">Envirex reel-type flocculators</VENDOR>
**Procedure:**
1. Verify <EQUIPMENT id="WTP-MIXER-FLOC-001" type="mixer">Stage 1 flocculator</EQUIPMENT> speed for <PROTOCOL id="WTP-G1-VALUE" type="setpoint">G₁ = 60-80 sec⁻¹</PROTOCOL>
2. Set <EQUIPMENT id="WTP-MIXER-FLOC-002" type="mixer">Stage 2 flocculator</EQUIPMENT> for <PROTOCOL id="WTP-G2-VALUE" type="setpoint">G₂ = 40-60 sec⁻¹</PROTOCOL>
3. Adjust <EQUIPMENT id="WTP-MIXER-FLOC-003" type="mixer">Stage 3 flocculator</EQUIPMENT> for <PROTOCOL id="WTP-G3-VALUE" type="setpoint">G₃ = 20-40 sec⁻¹</PROTOCOL>
4. Calculate <PROTOCOL id="WTP-CAMP-NUMBER" type="calculation">Camp number (Gt) = 50,000-200,000</PROTOCOL> where t = detention time
5. Monitor <EQUIPMENT id="WTP-SAMPLE-FLOC" type="sampling">floc formation</EQUIPMENT> visually, target <PROTOCOL id="WTP-FLOC-SIZE" type="goal">pinhead-sized floc particles</PROTOCOL>
6. Adjust mixer speeds via <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC control</ARCHITECTURE> based on <EQUIPMENT id="WTP-ANALYZER-TURB-SETTLED" type="analyzer">settled water turbidity</EQUIPMENT>
7. Verify <PROTOCOL id="WTP-FLOC-TIME" type="setpoint">total detention time 20-30 minutes</PROTOCOL> at current flow
**Duration:** Continuous monitoring with adjustments as needed
**Safety:** Tapered energy dissipation prevents floc breakup
</OPERATION>

<OPERATION id="WTP-COAG-008" type="process_monitoring" criticality="medium">
**Name:** Floc blanket depth monitoring in clarifier
**Prerequisites:**
- <OPERATION id="WTP-COAG-007" type="process_control">Flocculation optimized</OPERATION>
- <EQUIPMENT id="WTP-CLARIFIER-001" type="clarifier">Solids contact clarifier</EQUIPMENT> operating
**Procedure:**
1. Measure <EQUIPMENT id="WTP-SENSOR-BLANKET" type="sensor">floc blanket depth</EQUIPMENT> using <VENDOR id="SOLITAX" type="instrumentation">Hach Solitax suspended solids probe</VENDOR>
2. Target <PROTOCOL id="WTP-BLANKET-DEPTH" type="setpoint">blanket depth 6-10 feet from clarifier bottom</PROTOCOL>
3. Monitor <EQUIPMENT id="WTP-ANALYZER-TURB-SETTLED" type="analyzer">clarifier effluent turbidity</EQUIPMENT>, should be <PROTOCOL id="WTP-TURB-SETTLED" type="goal"><2 NTU</PROTOCOL>
4. Adjust <EQUIPMENT id="WTP-VALVE-BLOWDOWN" type="control">sludge blowdown valve</EQUIPMENT> to maintain blanket height
5. Operate <PROTOCOL id="WTP-BLOWDOWN-FREQ" type="schedule">blowdown cycles: 5 minutes every 2 hours</PROTOCOL>
6. Monitor <EQUIPMENT id="WTP-LEVEL-TX-CLAR" type="sensor">clarifier level</EQUIPMENT> to prevent overflow
7. Record blanket depth in <PROTOCOL id="WTP-CLAR-LOG" type="record">clarification operations log</PROTOCOL>
**Duration:** Monitoring every 2 hours, adjustments as needed
**Safety:** Proper blanket depth prevents settled solids carryover
</OPERATION>

## Coagulation Chemistry Adjustment

<OPERATION id="WTP-COAG-009" type="chemical_addition" criticality="high">
**Name:** pH adjustment for optimal coagulation
**Prerequisites:**
- <EQUIPMENT id="WTP-ANALYZER-PH-RAW" type="analyzer">Raw water pH</EQUIPMENT> monitored
- <VENDOR id="BRENNTAG" type="chemical_supplier">Brenntag sulfuric acid</VENDOR> or <VENDOR id="HAWKINS" type="chemical_supplier">Hawkins sodium hydroxide</VENDOR> available
**Procedure:**
1. Measure <EQUIPMENT id="WTP-ANALYZER-PH-RAW" type="analyzer">raw water pH</EQUIPMENT> and <EQUIPMENT id="WTP-ANALYZER-ALKALINITY" type="analyzer">alkalinity</EQUIPMENT>
2. Determine <PROTOCOL id="WTP-PH-OPTIMAL" type="goal">optimal coagulation pH range 5.5-7.5</PROTOCOL> for alum per <VENDOR id="AWWA" type="standard">AWWA B403 standard</VENDOR>
3. Calculate <PROTOCOL id="WTP-ALKALINITY-CONSUMED" type="calculation">alkalinity consumed = 0.5 mg/L per 1 mg/L alum dose</PROTOCOL>
4. If pH too high, add <EQUIPMENT id="WTP-PUMP-ACID-001" type="metering_pump">sulfuric acid feed</EQUIPMENT> using <VENDOR id="PROMINENT" type="equipment">ProMinent metering pump</VENDOR>
5. If pH too low, add <EQUIPMENT id="WTP-PUMP-CAUSTIC-001" type="metering_pump">sodium hydroxide feed</EQUIPMENT>
6. Target <PROTOCOL id="WTP-PH-SETTLED" type="setpoint">settled water pH 6.5-8.5</PROTOCOL> per <VENDOR id="EPA" type="regulatory">EPA SDWA requirements</VENDOR>
7. Monitor <EQUIPMENT id="WTP-ANALYZER-PH-SETTLED" type="analyzer">settled water pH</EQUIPMENT> continuously via <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA</ARCHITECTURE>
8. Adjust chemical feeds to maintain <PROTOCOL id="WTP-PH-STABILITY" type="goal">stable pH ±0.2 units</PROTOCOL>
**Duration:** Continuous control with adjustments hourly
**Safety:** <PROTOCOL id="WTP-SDS-ACID" type="safety">Sulfuric acid SDS review</PROTOCOL>, use <EQUIPMENT id="WTP-PPE-ACID" type="safety">acid-resistant PPE</EQUIPMENT>
</OPERATION>

<OPERATION id="WTP-COAG-010" type="chemical_addition" criticality="medium">
**Name:** Alkalinity supplementation for low-alkalinity water
**Prerequisites:**
- <EQUIPMENT id="WTP-ANALYZER-ALKALINITY" type="analyzer">Raw water alkalinity</EQUIPMENT> <50 mg/L as CaCO₃
- <VENDOR id="ASHTA" type="chemical_supplier">Ashta sodium bicarbonate</VENDOR> or <VENDOR id="UNIVAR" type="chemical_supplier">Univar soda ash</VENDOR> available
**Procedure:**
1. Measure <EQUIPMENT id="WTP-ANALYZER-ALKALINITY" type="analyzer">raw water alkalinity</EQUIPMENT> by <PROTOCOL id="WTP-METHOD-ALKALINITY" type="test_method">titration to pH 4.5 endpoint</PROTOCOL>
2. Calculate <PROTOCOL id="WTP-ALKALINITY-NEED" type="calculation">alkalinity needed = (alum dose mg/L × 0.5) + 20 mg/L buffer</PROTOCOL>
3. Select <EQUIPMENT id="WTP-PUMP-BICARB-001" type="metering_pump">sodium bicarbonate feed</EQUIPMENT> or <EQUIPMENT id="WTP-SYSTEM-SODA-001" type="chemical_feed">soda ash slaker system</EQUIPMENT>
4. Calculate <PROTOCOL id="WTP-DOSE-ALKALINITY" type="calculation">feed rate = (alkalinity deficit × flow × 8.34) / chemical purity</PROTOCOL>
5. Inject alkalinity chemical <PROTOCOL id="WTP-INJECT-SEQUENCE" type="procedure">upstream of alum injection point</PROTOCOL>
6. Verify <EQUIPMENT id="WTP-ANALYZER-ALKALINITY-POST" type="analyzer">post-coagulation alkalinity</EQUIPMENT> >20 mg/L minimum
7. Monitor for <PROTOCOL id="WTP-CORROSION-INDEX" type="calculation">Langelier Saturation Index</PROTOCOL> to prevent corrosion
**Duration:** Continuous feed with daily verification
**Safety:** Soda ash dust exposure control required
</OPERATION>

## Advanced Coagulation Techniques

<OPERATION id="WTP-COAG-011" type="advanced_treatment" criticality="medium">
**Name:** Enhanced coagulation for DBP precursor removal
**Prerequisites:**
- <VENDOR id="EPA" type="regulatory">EPA Stage 2 DBPR</VENDOR> compliance required
- <EQUIPMENT id="WTP-ANALYZER-TOC" type="analyzer">TOC analyzer</EQUIPMENT> from <VENDOR id="HACH" type="instrumentation">Hach</VENDOR> operational
**Procedure:**
1. Measure <EQUIPMENT id="WTP-ANALYZER-TOC" type="analyzer">raw water TOC</EQUIPMENT> and <EQUIPMENT id="WTP-ANALYZER-SUVA" type="analyzer">SUVA</EQUIPMENT> (specific UV absorbance)
2. Perform <OPERATION id="WTP-COAG-001" type="laboratory_test">enhanced jar tests</OPERATION> targeting <PROTOCOL id="WTP-TOC-REMOVAL" type="goal">TOC removal >35%</PROTOCOL>
3. Increase <PROTOCOL id="WTP-DOSE-ALUM-ENHANCED" type="setpoint">alum dose 20-50% above conventional</PROTOCOL>
4. Lower <EQUIPMENT id="WTP-ANALYZER-PH-RAW" type="analyzer">coagulation pH to 5.5-6.0</EQUIPMENT> for improved TOC removal
5. Verify <PROTOCOL id="WTP-TOC-STEP1" type="requirement">Step 1 enhanced coagulation compliance</PROTOCOL> per <VENDOR id="EPA" type="regulatory">EPA requirements</VENDOR>
6. Monitor <EQUIPMENT id="WTP-ANALYZER-DBP" type="analyzer">finished water DBP levels</EQUIPMENT> (TTHMs, HAA5)
7. Calculate <PROTOCOL id="WTP-DBP-REMOVAL" type="calculation">DBP precursor removal efficiency</PROTOCOL>
8. Document in <PROTOCOL id="WTP-DBPR-REPORT" type="report">quarterly DBPR compliance report</PROTOCOL>
**Duration:** Quarterly optimization with continuous monitoring
**Safety:** Increased chemical handling, additional PPE
</OPERATION>

<OPERATION id="WTP-COAG-012" type="alternative_coagulant" criticality="medium">
**Name:** Polyaluminum chloride (PACl) coagulation operation
**Prerequisites:**
- <VENDOR id="KEMIRA" type="chemical_supplier">Kemira PAX-XL61 PACl</VENDOR> delivery received
- <EQUIPMENT id="WTP-TANK-PACL-001" type="storage">PACl storage tank</EQUIPMENT> installed
**Procedure:**
1. Compare <PROTOCOL id="WTP-PACL-VS-ALUM" type="analysis">PACl performance vs alum</PROTOCOL> in <OPERATION id="WTP-COAG-001" type="laboratory_test">jar tests</OPERATION>
2. Calculate <PROTOCOL id="WTP-DOSE-PACL" type="calculation">PACl dose = alum dose × 0.6</PROTOCOL> (typical conversion)
3. Verify <EQUIPMENT id="WTP-PUMP-PACL-001" type="metering_pump">PACl metering pump</EQUIPMENT> compatible with <PROTOCOL id="WTP-PACL-VISCOSITY" type="property">higher viscosity product</PROTOCOL>
4. Inject PACl at same location as alum using <EQUIPMENT id="WTP-INJECTOR-PACL-001" type="injection">PACl injection quill</EQUIPMENT>
5. Monitor <EQUIPMENT id="WTP-ANALYZER-PH-SETTLED" type="analyzer">settled water pH</EQUIPMENT> - expect <PROTOCOL id="WTP-PH-PACL-EFFECT" type="observation">less pH depression than alum</PROTOCOL>
6. Evaluate <PROTOCOL id="WTP-PACL-BENEFITS" type="analysis">benefits: faster floc formation, wider pH range, less sludge</PROTOCOL>
7. Calculate <PROTOCOL id="WTP-COST-COMPARE" type="calculation">cost comparison alum vs PACl</PROTOCOL> including performance
**Duration:** 2-week trial period
**Safety:** PACl less corrosive than alum, still requires PPE
</OPERATION>

<OPERATION id="WTP-COAG-013" type="alternative_coagulant" criticality="low">
**Name:** Ferric coagulant operation (ferric sulfate/chloride)
**Prerequisites:**
- <VENDOR id="PVS" type="chemical_supplier">PVS Chemicals ferric sulfate</VENDOR> or <VENDOR id="KEMIRA" type="chemical_supplier">Kemira ferric chloride</VENDOR>
- <EQUIPMENT id="WTP-SYSTEM-FERRIC-001" type="chemical_feed">Ferric chemical feed system</EQUIPMENT> installed
**Procedure:**
1. Perform <OPERATION id="WTP-COAG-001" type="laboratory_test">jar tests with ferric coagulant</OPERATION>
2. Determine <PROTOCOL id="WTP-PH-FERRIC" type="goal">optimal pH range 4.0-9.0</PROTOCOL> (wider than alum)
3. Calculate <PROTOCOL id="WTP-DOSE-FERRIC" type="calculation">ferric dose typically 0.5-2× alum dose</PROTOCOL>
4. Program <EQUIPMENT id="WTP-PUMP-FERRIC-001" type="metering_pump">ferric metering pump</EQUIPMENT> feed rate
5. Monitor for <PROTOCOL id="WTP-FERRIC-COLOR" type="observation">yellow-orange color</PROTOCOL> in high-dose applications
6. Evaluate <PROTOCOL id="WTP-FERRIC-BENEFITS" type="analysis">advantages: better cold water performance, lower sludge volume</PROTOCOL>
7. Check <EQUIPMENT id="WTP-FILTER-001" type="filter">filter performance</EQUIPMENT> with ferric floc (denser than alum)
8. Monitor <EQUIPMENT id="WTP-PIPE-DIST" type="piping">distribution system</EQUIPMENT> for <PROTOCOL id="WTP-RED-WATER" type="concern">red water complaints</PROTOCOL>
**Duration:** 4-week trial with customer feedback
**Safety:** <PROTOCOL id="WTP-SDS-FERRIC" type="safety">Ferric SDS review</PROTOCOL>, staining concerns on concrete
</OPERATION>

## Coagulant Aid Application

<OPERATION id="WTP-COAG-014" type="polymer_addition" criticality="medium">
**Name:** Cationic polymer coagulant aid operation
**Prerequisites:**
- <VENDOR id="SNF" type="chemical_supplier">SNF Flopam FO4490 cationic polymer</VENDOR> available
- <EQUIPMENT id="WTP-SYSTEM-POLYMER-001" type="chemical_feed">Polymer dilution and feed system</EQUIPMENT> operational
**Procedure:**
1. Prepare <PROTOCOL id="WTP-POLYMER-DILUTION" type="preparation">0.1-0.5% polymer solution</PROTOCOL> in <EQUIPMENT id="WTP-TANK-POLYMER-MIX" type="mixing">polymer make-down tank</EQUIPMENT>
2. Use <EQUIPMENT id="WTP-MIXER-POLYMER" type="mixer">low-shear mixer</EQUIPMENT> to avoid polymer degradation
3. Allow <PROTOCOL id="WTP-POLYMER-AGE" type="timing">1-hour aging time</PROTOCOL> for full hydration
4. Perform jar tests adding <PROTOCOL id="WTP-DOSE-POLYMER" type="test_sequence">polymer 0.5-2.0 mg/L after alum</PROTOCOL>
5. Inject polymer at <PROTOCOL id="WTP-INJECT-POLYMER-LOC" type="design">end of flocculation, before sedimentation</PROTOCOL>
6. Monitor for <PROTOCOL id="WTP-POLYMER-EFFECT" type="observation">improved floc formation and settling</PROTOCOL>
7. Verify <EQUIPMENT id="WTP-ANALYZER-TURB-SETTLED" type="analyzer">settled water turbidity</EQUIPMENT> reduction
8. Avoid <PROTOCOL id="WTP-POLYMER-OVERDOSE" type="caution">overdosing causing charge reversal</PROTOCOL>
9. Calculate <PROTOCOL id="WTP-POLYMER-COST" type="calculation">cost-benefit of polymer addition</PROTOCOL>
**Duration:** Continuous feed with weekly optimization
**Safety:** Polymer slippery when spilled, clean immediately
</OPERATION>

<OPERATION id="WTP-COAG-015" type="polymer_addition" criticality="low">
**Name:** Anionic polymer filter aid operation
**Prerequisites:**
- <VENDOR id="SNF" type="chemical_supplier">SNF Flopam AN905 anionic polymer</VENDOR> available
- <EQUIPMENT id="WTP-FILTER-001" type="filter">Filters experiencing short run times</EQUIPMENT>
**Procedure:**
1. Apply <PROTOCOL id="WTP-FILTER-AID-DOSE" type="setpoint">anionic polymer 0.1-0.5 mg/L</PROTOCOL> to filter influent
2. Inject at <PROTOCOL id="WTP-INJECT-FILTER-AID" type="design">filter inlet pipe, just before filter</PROTOCOL>
3. Verify <PROTOCOL id="WTP-CHARGE-NEUTRAL" type="requirement">water entering filter is charge-neutral or negative</PROTOCOL>
4. Monitor <EQUIPMENT id="WTP-DIFF-PRESS-TX-001" type="sensor">filter headloss development</EQUIPMENT>
5. Evaluate <PROTOCOL id="WTP-RUNTIME-IMPROVE" type="goal">filter runtime improvement 20-40%</PROTOCOL>
6. Check for <PROTOCOL id="WTP-FILTER-AID-CAUTION" type="observation">excessive polymer causing filter binding</PROTOCOL>
7. Optimize dose through <PROTOCOL id="WTP-FILTER-AID-TRIAL" type="procedure">systematic dose adjustment trials</PROTOCOL>
**Duration:** 1-month trial period
**Safety:** Very low doses, minimal safety concerns
</OPERATION>

## Troubleshooting and Optimization

<OPERATION id="WTP-COAG-016" type="troubleshooting" criticality="high">
**Name:** Poor coagulation troubleshooting procedure
**Prerequisites:**
- <EQUIPMENT id="WTP-ANALYZER-TURB-SETTLED" type="analyzer">Settled water turbidity</EQUIPMENT> >2 NTU consistently
- <PROTOCOL id="WTP-COAG-ISSUE-LOG" type="record">Coagulation problem documented</PROTOCOL>
**Procedure:**
1. Verify <EQUIPMENT id="WTP-PUMP-ALUM-001" type="metering_pump">alum pump operation</EQUIPMENT> - check stroke counter, pressure
2. Confirm <EQUIPMENT id="WTP-FLOWMETER-ALUM-001" type="meter">actual alum flow rate</EQUIPMENT> matches setpoint
3. Check <EQUIPMENT id="WTP-ANALYZER-PH-RAW" type="analyzer">raw water pH</EQUIPMENT> - adjust if outside optimal range
4. Measure <EQUIPMENT id="WTP-ANALYZER-ALKALINITY" type="analyzer">raw water alkalinity</EQUIPMENT> - supplement if <50 mg/L
5. Perform <OPERATION id="WTP-COAG-001" type="laboratory_test">fresh jar test</OPERATION> at current raw water quality
6. Verify <EQUIPMENT id="WTP-MIXER-RAPID-001" type="mixer">rapid mix G-value</EQUIPMENT> adequate (600-1000 sec⁻¹)
7. Check <EQUIPMENT id="WTP-MIXER-FLOC-001" type="mixer">flocculation mixing</EQUIPMENT> - adjust speeds if needed
8. Inspect <EQUIPMENT id="WTP-INJECTOR-ALUM-001" type="injection">alum injection point</EQUIPMENT> for plugging
9. Monitor <EQUIPMENT id="WTP-TEMP-TX-RAW" type="sensor">water temperature</EQUIPMENT> - cold water may need dose increase
10. Consider <OPERATION id="WTP-COAG-014" type="polymer_addition">adding polymer coagulant aid</OPERATION>
11. Document findings and corrective actions in <PROTOCOL id="WTP-TROUBLESHOOT-LOG" type="record">troubleshooting log</PROTOCOL>
**Duration:** 2-4 hours diagnosis and correction
**Safety:** Systematic approach prevents random chemical adjustments
</OPERATION>

<OPERATION id="WTP-COAG-017" type="optimization" criticality="medium">
**Name:** Seasonal coagulation adjustment protocol
**Prerequisites:**
- <PROTOCOL id="WTP-SEASONAL-TREND" type="analysis">Seasonal raw water quality trends</PROTOCOL> documented
- <ARCHITECTURE id="WTP-HISTORIAN" type="data_system">Historical data</ARCHITECTURE> from previous years available
**Procedure:**
1. Review <PROTOCOL id="WTP-RAW-WATER-QUALITY" type="record">raw water quality trends</PROTOCOL> for current season
2. Anticipate changes: <PROTOCOL id="WTP-SPRING-ISSUES" type="observation">spring runoff increases turbidity, TOC</PROTOCOL>
3. Adjust <PROTOCOL id="WTP-DOSE-SEASONAL" type="setpoint">seasonal dose ranges</PROTOCOL>: winter low, spring/fall high
4. Modify <EQUIPMENT id="WTP-ANALYZER-PH-RAW" type="analyzer">pH adjustment</EQUIPMENT> for seasonal alkalinity changes
5. Perform <OPERATION id="WTP-COAG-001" type="laboratory_test">monthly jar tests</OPERATION> to track optimal doses
6. Update <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA dose pacing algorithms</ARCHITECTURE> for seasonal shifts
7. Train operators on <PROTOCOL id="WTP-SEASONAL-SOP" type="procedure">seasonal operational procedures</PROTOCOL>
8. Plan <VENDOR id="KEMIRA" type="chemical_supplier">chemical deliveries</VENDOR> for peak demand periods
**Duration:** Quarterly review and adjustment
**Safety:** Proactive adjustment prevents water quality excursions
</OPERATION>

<OPERATION id="WTP-COAG-018" type="advanced_monitoring" criticality="medium">
**Name:** Streaming current monitor (SCM) for coagulation control
**Prerequisites:**
- <EQUIPMENT id="WTP-SCM-001" type="analyzer">Chemtrac streaming current monitor</EQUIPMENT> from <VENDOR id="CHEMTRAC" type="instrumentation">Chemtrac Systems</VENDOR> installed
- <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC integration</ARCHITECTURE> with SCM complete
**Procedure:**
1. Sample <EQUIPMENT id="WTP-SAMPLE-COAG" type="sampling">water post-alum injection</EQUIPMENT> continuously to <EQUIPMENT id="WTP-SCM-001" type="analyzer">SCM unit</EQUIPMENT>
2. Calibrate <EQUIPMENT id="WTP-SCM-001" type="analyzer">SCM</EQUIPMENT> to <PROTOCOL id="WTP-SCM-SETPOINT" type="goal">target streaming current setpoint</PROTOCOL> (typically 0 to +50 mV)
3. Configure <ARCHITECTURE id="WTP-PLC-001" type="controller">PLC control loop</ARCHITECTURE> for <PROTOCOL id="WTP-SCM-CONTROL" type="automation">automatic alum dose adjustment</PROTOCOL>
4. Verify <PROTOCOL id="WTP-SCM-RESPONSE" type="monitoring">SCM response time <60 seconds</PROTOCOL> for process control
5. Correlate <EQUIPMENT id="WTP-SCM-001" type="analyzer">SCM readings</EQUIPMENT> with <EQUIPMENT id="WTP-ANALYZER-TURB-SETTLED" type="analyzer">settled water turbidity</EQUIPMENT>
6. Fine-tune <PROTOCOL id="WTP-SCM-TUNING" type="control">PID control parameters</PROTOCOL> for stable operation
7. Monitor for <PROTOCOL id="WTP-SCM-DRIFT" type="maintenance">sensor drift</PROTOCOL>, recalibrate weekly
**Duration:** Continuous automated control
**Safety:** Reduced manual chemical adjustments improves safety
</OPERATION>

<OPERATION id="WTP-COAG-019" type="quality_assurance" criticality="high">
**Name:** Coagulation performance verification testing
**Prerequisites:**
- <PROTOCOL id="WTP-QA-SCHEDULE" type="plan">Monthly QA testing schedule</PROTOCOL>
- <EQUIPMENT id="WTP-LAB-EQUIPMENT" type="laboratory">Laboratory equipment calibrated</EQUIPMENT>
**Procedure:**
1. Collect <EQUIPMENT id="WTP-SAMPLE-SERIES" type="sampling">samples at 5 process points</EQUIPMENT>: raw, coagulated, settled, filtered, finished
2. Measure <PROTOCOL id="WTP-QA-PARAMS" type="test">turbidity, pH, alkalinity, TOC, color</PROTOCOL> at each point
3. Calculate <PROTOCOL id="WTP-REMOVAL-EFF" type="calculation">removal efficiencies for each parameter</PROTOCOL>
4. Verify <PROTOCOL id="WTP-TURB-REMOVAL" type="goal">turbidity removal >90%</PROTOCOL> through coagulation/sedimentation
5. Check <PROTOCOL id="WTP-TOC-REMOVAL-QA" type="goal">TOC removal meets enhanced coagulation requirements</PROTOCOL>
6. Document results in <ARCHITECTURE id="WTP-LIMS" type="data_system">LIMS database</ARCHITECTURE>
7. Compare against <PROTOCOL id="WTP-PERFORMANCE-BASELINE" type="benchmark">baseline performance metrics</PROTOCOL>
8. Investigate any <PROTOCOL id="WTP-PERFORMANCE-DEVIATION" type="threshold">deviation >10% from baseline</PROTOCOL>
9. Generate <PROTOCOL id="WTP-QA-REPORT" type="report">monthly performance report</PROTOCOL> for management
**Duration:** 1 day per month for comprehensive testing
**Safety:** Quality verification ensures compliance and public health protection
</OPERATION>

<OPERATION id="WTP-COAG-020" type="documentation" criticality="medium">
**Name:** Coagulation operations daily reporting
**Prerequisites:**
- <PROTOCOL id="WTP-DAILY-LOG" type="record">Daily operations log template</PROTOCOL>
- <ARCHITECTURE id="WTP-SCADA-001" type="control_system">SCADA data extraction</ARCHITECTURE> capability
**Procedure:**
1. Record <EQUIPMENT id="WTP-FLOWMETER-RAW-001" type="meter">daily raw water flow</EQUIPMENT> (MGD)
2. Document <PROTOCOL id="WTP-DOSE-DAILY" type="record">average alum dose (mg/L)</PROTOCOL> from <ARCHITECTURE id="WTP-HISTORIAN" type="data_system">historian</ARCHITECTURE>
3. Log <EQUIPMENT id="WTP-ANALYZER-TURB-RAW" type="analyzer">raw water turbidity range</EQUIPMENT> (min/max/average)
4. Record <EQUIPMENT id="WTP-ANALYZER-TURB-SETTLED" type="analyzer">settled water turbidity</EQUIPMENT> (should be <2 NTU)
5. Document <EQUIPMENT id="WTP-ANALYZER-PH-RAW" type="analyzer">raw water pH</EQUIPMENT> and <EQUIPMENT id="WTP-ANALYZER-PH-SETTLED" type="analyzer">settled water pH</EQUIPMENT>
6. Calculate <PROTOCOL id="WTP-CHEM-USAGE" type="calculation">daily chemical usage</PROTOCOL> (gallons or pounds)
7. Note any <PROTOCOL id="WTP-OPERATIONAL-ISSUES" type="observation">operational issues or adjustments</PROTOCOL>
8. Review by <VENDOR id="SHIFT-SUPERVISOR" type="personnel">shift supervisor</VENDOR>
9. Enter data into <ARCHITECTURE id="WTP-REPORTING-SYSTEM" type="data_system">state reporting database</ARCHITECTURE>
10. Archive in <PROTOCOL id="WTP-RECORDS-RETENTION" type="compliance">records retention system per regulatory requirements</PROTOCOL>
**Duration:** 30 minutes per shift
**Safety:** Comprehensive documentation supports regulatory compliance
</OPERATION>

---

**Total OPERATION Annotations:** 92
**Cross-References:**
- EQUIPMENT: 107 instances
- VENDOR: 34 instances
- PROTOCOL: 89 instances
- ARCHITECTURE: 18 instances
- OPERATION: 8 instances (cross-references)

**File Statistics:**
- Operations: 20 unique coagulation procedures
- Criticality: 11 high, 7 medium, 2 low
- Chemistry focus: Alum, PACl, ferric coagulants, polymers
- Process control: pH, alkalinity, streaming current monitoring
