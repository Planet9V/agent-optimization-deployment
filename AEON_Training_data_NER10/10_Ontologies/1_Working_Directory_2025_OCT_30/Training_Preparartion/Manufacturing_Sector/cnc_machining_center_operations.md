# CNC Machining Center Operations

## Overview
Standard operating procedures for Computer Numerical Control (CNC) machining centers including G-code programming, tool offset calibration, workpiece fixturing, and quality inspection protocols.

## Equipment Specifications
- **CNC Controllers**: FANUC 0i-MF Plus, Siemens 840D sl, Heidenhain TNC 640
- **Machine Tools**: 3-axis vertical machining centers, 5-axis horizontal machining centers
- **Tool Management**: Automatic tool changers (ATC) with 40-60 tool capacity
- **Workholding**: Kurt hydraulic vises, Schunk precision vises, custom fixturing

## 1. Machine Startup and Warm-up Procedure

### Pre-Operation Safety Checks
```annotation
type: safety_verification
context: Before energizing CNC machine, operator must complete visual inspection checklist
equipment: HAAS VF-4 vertical machining center with FANUC 0i-MF controller
checklist:
  - Machine guards closed and interlocked
  - Coolant reservoir filled (20-gallon capacity, 5% synthetic coolant concentration)
  - Chip conveyor operational and discharge bin empty
  - Air pressure 90 PSI minimum (pneumatic tool changer and drawbar)
  - Way covers intact and undamaged
  - Emergency stop buttons functional (test press and release)
standard: OSHA 29 CFR 1910.212 Machine Guarding
personnel: Certified CNC machinist with 40-hour safety training
```

### Controller Power-Up Sequence
```annotation
type: operational_procedure
context: CNC controller must be powered up following specific sequence to prevent system errors
equipment: FANUC 0i-MF Plus controller
procedure:
  1. Verify main disconnect switch in OFF position
  2. Enable 480VAC 3-phase power at facility panel
  3. Rotate main disconnect to ON position
  4. Controller boots (POST sequence ~60 seconds)
  5. Acknowledge startup messages on control panel
  6. Initialize absolute encoder reference (home all axes)
  7. Verify G54-G59 work coordinate systems loaded
  8. Check battery voltage (3.6VDC minimum for memory backup)
diagnostics: Controller displays axis position, spindle status, tool number, feed/speed overrides
warmup_required: Yes - minimum 15 minute spindle warmup cycle before production
```

### Spindle Warm-Up Cycle
```annotation
type: maintenance_procedure
context: CNC spindle must be warmed up to operating temperature to achieve dimensional accuracy
equipment: 10,000 RPM belt-driven spindle with through-spindle coolant
warmup_program: G-code routine cycles spindle from 1,000 to 10,000 RPM in 1,000 RPM increments
duration: 15 minutes total (90 seconds per RPM step)
rationale: Thermal growth of spindle bearings and housing affects tool length offset compensation
temperature_monitoring: Spindle bearing temperature monitored via RTD sensor (target: 45°C ±3°C)
production_readiness: Spindle considered thermally stable after 15-minute warmup + 3 production parts
standard: Machine tool builder recommendation (Haas Automation Technical Bulletin TB-001)
```

## 2. Workpiece Setup and Fixturing

### Work Coordinate System (WCS) Setup
```annotation
type: setup_procedure
context: Work coordinate system defines part origin relative to machine home position
equipment: Haimer 3D Taster edge finder, Renishaw OMP60 touch probe
method: Electronic edge finder or touch probe establishes X, Y, Z zero on part datum features
procedure:
  1. Mount workpiece in vise with parallels ensuring part seated and level
  2. Select appropriate work offset register (G54-G59)
  3. Touch off X and Y edges of part using edge finder or probe routine
  4. Set Z zero on top surface of part (or fixture datum plane)
  5. Record offset values in controller work offset table
  6. Verify setup by rapid positioning tool over part features visually
accuracy: ±0.005mm typical for edge finder, ±0.001mm for touch probe
validation: Prove out program in single-block mode at 10% feed rate override before full speed
```

### Vise and Fixture Installation
```annotation
type: workholding_setup
context: Workpiece must be securely clamped to withstand cutting forces without movement
equipment: Kurt D688 6-inch hydraulic vise, 8,000 lbs clamping force
installation:
  1. Clean T-slot table and vise base (remove chips, coolant residue)
  2. Position vise parallel to Y-axis using dial indicator on fixed jaw (±0.002" in 6")
  3. Install T-slot bolts and torque to 40 ft-lbs
  4. Verify vise jaw parallelism with dial indicator (max 0.001" deviation)
workpiece_prep:
  - Deburr edges to prevent interference with vise jaws
  - Use parallels under part to raise above vise base (allows end mill clearance)
  - Apply vise clamping force gradually to avoid part distortion
inspection: After clamping, probe part edges to verify no shift occurred during tightening
```

### Custom Fixture Validation
```annotation
type: fixture_qualification
context: Custom fixtures must be validated for repeatability and accuracy before production use
equipment: Mitutoyo coordinate measuring machine (CMM), fixture holding workpiece
validation_process:
  1. Load part in fixture per documented procedure
  2. Measure critical part features on CMM (datums, locating points)
  3. Remove part and reload 5 times, repeating measurement
  4. Calculate repeatability (standard deviation of measurements)
acceptance_criteria:
  - Repeatability: 2σ < 0.010mm for all datum features
  - Accuracy: All features within ±0.025mm of nominal CAD dimensions
documentation: CMM inspection report signed by quality engineer, fixture approved for production
maintenance: Re-qualify fixture quarterly or after any modification/repair
```

## 3. Tool Management and Offset Calibration

### Tool Loading and Tool Data Entry
```annotation
type: tool_setup
context: Cutting tools must be loaded in ATC magazine with accurate tool data entered in controller
equipment: 40-position automatic tool changer, HSK-A63 tool interface
procedure:
  1. Select required tools per operation sheet (end mills, drills, taps, reamers)
  2. Assemble tools in tool holders (HSK-A63) with proper torque on collet nuts (25 Nm)
  3. Measure tool length using Haimer Tool Presetter (±0.002mm accuracy)
  4. Enter tool data in controller offset table:
     - Tool number (T01-T40)
     - Tool length offset (Z-axis compensation)
     - Tool diameter offset (for cutter radius compensation)
     - Tool life counter (minutes of spindle run time)
  5. Load tools in ATC magazine per tool call order in program
  6. Verify tool number labels match controller data
tool_life: Tool life limits programmed (e.g., 60 minutes for carbide end mill), alarm when exceeded
```

### Tool Length Offset (TLO) Calibration
```annotation
type: calibration_procedure
context: Tool length offset compensates for different tool lengths, ensuring Z-axis accuracy
equipment: Haimer 3D Sensor or manual edge finder with gage block
manual_method:
  1. Install tool in spindle (e.g., Tool T01)
  2. Jog tool tip to touch 2-inch gage block on machine table
  3. Zero Z-axis at that position
  4. Record Z-axis machine coordinate (e.g., Z-14.275)
  5. Enter value as tool length offset in controller (T01 = -14.275)
automatic_method:
  - Use touch probe on machine table
  - Run automated G-code routine (G43 H01 Z0.1 F25)
  - Controller calculates and stores TLO automatically
accuracy: ±0.001" for precision work, ±0.005" acceptable for non-critical features
verification: After TLO setup, rapid tool to Z0.1 above part surface, visually check clearance
```

### Cutter Radius Compensation Setup
```annotation
type: geometric_compensation
context: G41/G42 cutter compensation adjusts tool path for actual cutter diameter vs. programmed path
equipment: Mitutoyo micrometer (0.0001" resolution) or laser tool measurement system
measurement:
  1. Measure cutter diameter with micrometer or laser tool setter
  2. Enter actual diameter in tool offset table (e.g., T05 D=0.5002" for nominal 0.500" end mill)
  3. Program invokes G41 (left) or G42 (right) compensation based on cut direction
  4. Controller offsets tool path by cutter radius automatically
application: Critical for profile milling, less important for drilling/tapping operations
accuracy: Affects part dimensional accuracy by ±(actual diameter - programmed diameter)/2
verification: Cut test part, measure critical dimensions with calipers or CMM
```

### Tool Wear Monitoring and Replacement
```annotation
type: preventive_maintenance
context: Cutting tool wear degrades part quality, tools must be replaced before failure
monitoring_methods:
  - Visual inspection: Check cutting edges for chipping, buildup, or excessive wear
  - Spindle load monitoring: Increased amperage indicates dull tool
  - Surface finish degradation: Poor finish indicates tool needs replacement
  - Dimensional drift: Parts measuring oversize (end mill wear) or undersize (hole drill wear)
tool_life_management:
  - Controller tracks spindle-on time per tool
  - Tool life limit programmed (e.g., 60 minutes for carbide end mill in steel)
  - M06 tool change command includes tool life check, alarm if limit exceeded
replacement_procedure:
  1. Remove worn tool from ATC magazine
  2. Install new tool of same type and nominal size
  3. Re-measure tool length and diameter offsets
  4. Update controller tool data
  5. Resume production, monitor first part dimensional accuracy
```

## 4. G-Code Programming and Verification

### CAM-Generated G-Code Post-Processing
```annotation
type: program_development
context: CAM software generates G-code from 3D CAD model, post-processor formats for specific controller
software: Mastercam 2024, post-processor for FANUC 0i-MF controller
workflow:
  1. Import part CAD model (STEP or Parasolid format)
  2. Define stock material, setup origin, clamping method in CAM
  3. Create toolpaths (face mill, contour, pocket, drilling, tapping)
  4. Simulate toolpaths in CAM software for collision detection
  5. Post-process to generate G-code (.nc or .txt file)
  6. Transfer G-code to CNC via RS-232, Ethernet, or USB
validation: CAM simulation verifies no collisions, estimated cycle time 18.3 minutes
optimization: CAM optimizes feed rates for material, calculates chip load per tooth
```

### Manual G-Code Editing and Optimization
```annotation
type: program_modification
context: Shop floor edits to G-code for feed/speed optimization or minor geometry changes
equipment: CNC controller edit mode or laptop with text editor (Notepad++)
common_edits:
  - Adjust feed rates (F parameter) for better surface finish or cycle time
  - Modify spindle RPM (S parameter) based on tool wear or material hardness variation
  - Add/remove tool approach/retract moves for clearance
  - Insert canned cycles (G81 drilling, G84 tapping) to reduce program length
best_practices:
  - Always backup original program before editing
  - Use descriptive comment lines (parentheses or semicolons)
  - Maintain consistent line numbers for traceability
  - Test edited program in single-block mode before full run
version_control: Save programs with revision numbers (PART123_Rev2.nc), log changes in program header
```

### Program Simulation and Dry Run Testing
```annotation
type: verification_procedure
context: New or modified programs must be verified before cutting actual workpieces
simulation_software: Predator CNC Editor with 3D machine simulation, or controller's built-in simulator
procedure:
  1. Load G-code program into simulator
  2. Define tool library with actual tool dimensions
  3. Run simulation, observe tool paths and part material removal
  4. Check for collisions (tool/part, tool/fixture, tool/machine)
  5. Verify program completes without errors or out-of-range moves
dry_run_on_machine:
  - Load program in CNC controller
  - Enable dry run mode (machine rapids through program without cutting)
  - Set feed rate override to 10%, single-block mode ON
  - Manually step through each line, verifying tool moves and spindle commands
  - Gradually increase feed override to 100% if no issues observed
approval: First part produced must be inspected by quality control before continuing production run
```

## 5. Machining Operations Execution

### Roughing Operations
```annotation
type: material_removal
context: Rough machining removes bulk material quickly, leaving finish stock for final pass
tools: Large diameter end mills (0.75" - 1.5"), indexable face mills, roughing end mills
parameters:
  - Spindle speed: 1,200-2,500 RPM (for steel)
  - Feed rate: 15-30 IPM (inches per minute)
  - Depth of cut: 0.100" - 0.250" per pass
  - Width of cut: 50-70% of cutter diameter
  - Coolant: Flood coolant 5% concentration, 20 GPM flow rate
strategy: Adaptive clearing toolpaths maintain consistent chip load, reduce tool wear
cycle_time: Roughing typically 60-70% of total machining time
stock_remaining: Leave 0.010" - 0.030" finish stock on walls, 0.005" - 0.015" on floors
```

### Finish Machining Operations
```annotation
type: precision_cutting
context: Finish passes achieve final part dimensions and surface finish requirements
tools: Sharp carbide end mills, ball nose end mills for contoured surfaces
parameters:
  - Spindle speed: 3,000-6,000 RPM (higher for better finish)
  - Feed rate: 30-60 IPM
  - Depth of cut: 0.005" - 0.020" per pass
  - Stepover: 5-15% of cutter diameter for fine finish
  - Coolant: Flood or through-spindle coolant for chip evacuation and heat control
surface_finish: Ra 1.6 μm (63 μin) typical, Ra 0.8 μm (32 μin) achievable with sharp tools and optimal speeds/feeds
accuracy: ±0.002" dimensional tolerance achievable with proper setup and calibrated machine
validation: Inspect first part with calipers or CMM, adjust offsets if needed before full production run
```

### Drilling and Tapping Operations
```annotation
type: hole_making
context: Holes drilled with twist drills, tapped for threads, reamed for precision diameter
tools: HSS or carbide twist drills, spiral point taps, adjustable reamers
drilling_parameters:
  - Center drill: 1,500 RPM, 5 IPM (prevents drill walk)
  - Twist drill: Calculate RPM = (SFM × 3.82) / Diameter, feed 0.003-0.010 IPR
  - Peck drilling: G83 canned cycle, peck depth 2-3× drill diameter
tapping_parameters:
  - Rigid tapping: G84 canned cycle, RPM and feed synchronized (Feed = RPM × pitch)
  - Example: M8×1.25 tap, 500 RPM, 500 × 1.25mm = 625 mm/min feed
  - Spindle reversing at bottom of hole, tap withdraws
coolant: Through-spindle coolant for deep holes (>3× diameter), improves chip evacuation
accuracy: Reamed holes ±0.0005" tolerance, tapped holes checked with go/no-go thread gauges
```

### High-Speed Machining (HSM) Strategies
```annotation
type: advanced_machining
context: HSM uses high spindle speeds and light cuts for increased productivity and tool life
equipment: High-speed spindle (12,000-20,000 RPM), balanced tool holders (G2.5 @ 25,000 RPM)
parameters:
  - Spindle speed: 8,000-15,000 RPM
  - Feed rate: 100-300 IPM
  - Depth of cut: 0.010" - 0.050" (shallow cuts, high speeds)
  - Radial immersion: 10-30% of cutter diameter (light engagement)
tooling: Carbide end mills with AlTiN coating, 4-6 flutes for aluminum, 2-4 flutes for steel
benefits:
  - Reduced cycle time (30-50% faster than conventional)
  - Improved surface finish
  - Lower cutting forces (gentle on thin-walled parts)
  - Extended tool life (lower chip load per tooth)
challenges: Machine must have high rapid traverse (1,000+ IPM), rigid construction, high-speed CAM toolpaths required
```

## 6. Quality Control and In-Process Inspection

### First Article Inspection (FAI)
```annotation
type: quality_verification
context: First part from new setup must be fully inspected before continuing production
equipment: Mitutoyo CMM, height gage, pin gages, thread gages, surface finish comparator
inspection_plan:
  - Measure all critical dimensions per drawing (tolerances ±0.005" or tighter)
  - Check hole diameters with pin gages or bore micrometers
  - Verify thread fit with go/no-go thread gages
  - Measure surface finish with profilometer (Ra reading)
  - Inspect for burrs, sharp edges, cosmetic defects
acceptance_criteria: All features within drawing tolerances, surface finish ≤ specified Ra
documentation: FAI report with actual measurements, deviations noted, signed by quality inspector
disposition: If FAI fails, adjust offsets/program, produce new part, re-inspect until pass
standard: AS9102 First Article Inspection for aerospace applications
```

### In-Process Measurement and SPC
```annotation
type: statistical_process_control
context: Critical dimensions monitored during production run to detect process drift
equipment: Mitutoyo digital calipers (0.0005" resolution), dial bore gage for holes
sampling_plan: Measure 1 part every 10 parts produced (10% sampling frequency)
control_chart: X-bar and R chart for critical dimension (e.g., bore diameter 1.2500" ±0.0010")
control_limits:
  - Upper Control Limit (UCL): X-bar + 3σ = 1.2506"
  - Lower Control Limit (LCL): X-bar - 3σ = 1.2494"
  - Specification Limits: 1.2490" to 1.2510"
response:
  - If point exceeds control limits (but within spec): Investigate cause, adjust if needed
  - If point exceeds specification limits: Stop production, scrap part, adjust process
  - If 7 consecutive points trend in one direction: Process drift, adjust tool offsets
process_capability: Cpk = (USL - X-bar) / (3σ) = 1.33 target (indicates capable process)
```

### Surface Finish Verification
```annotation
type: quality_measurement
context: Surface finish (roughness) must meet drawing requirements for functional surfaces
equipment: Mitutoyo SJ-210 portable surface roughness tester
measurement:
  - Ra (arithmetic average roughness): Most common specification (μm or μin)
  - Rz (average peak-to-valley height): Used for critical sealing surfaces
  - Measurement length: 0.8mm (0.03") cutoff filter, 4mm (0.16") evaluation length
specification_examples:
  - As-machined surface: Ra 3.2 μm (125 μin)
  - Finish machined surface: Ra 1.6 μm (63 μin)
  - Ground surface: Ra 0.8 μm (32 μin)
factors_affecting_finish:
  - Tool sharpness (dull tools increase Ra)
  - Spindle speed (higher RPM = better finish)
  - Feed rate (lower feed = better finish)
  - Coolant flow (adequate cooling improves finish)
acceptance: Measured Ra must be ≤ specified value, or surface rejected for rework
```

### CMM Final Inspection
```annotation
type: dimensional_verification
context: Coordinate Measuring Machine provides high-accuracy 3D inspection of complex parts
equipment: Mitutoyo Crysta-Apex CMM with Renishaw PH20 5-axis probe head
measurement_capability: ±0.002mm volumetric accuracy, repeatability ±0.001mm
inspection_program:
  - CAD model imported to CMM software (PC-DMIS or Mitutoyo MCOSMOS)
  - Datum features measured first (establish part coordinate system)
  - Critical features measured in sequence per inspection plan
  - True position, perpendicularity, flatness, cylindricity verified per GD&T callouts
output: Inspection report with actual vs. nominal dimensions, out-of-tolerance features highlighted
frequency: 100% CMM inspection for first article and last part of run, sampling for high-volume production
traceability: CMM calibrated annually with certified master standards, calibration certs on file
```

## 7. Coolant Management and Chip Disposal

### Coolant Concentration Monitoring
```annotation
type: fluid_management
context: Metalworking coolant must be maintained at proper concentration for lubrication and rust prevention
equipment: Refractometer (Brix scale) for concentration measurement
target_concentration: 5-10% for water-soluble synthetic coolant (e.g., Master Chemical Trim SC210)
measurement:
  - Extract coolant sample from machine sump
  - Place 2-3 drops on refractometer prism
  - Read Brix value, convert to concentration using coolant manufacturer's chart
  - Typical: 1 Brix = 1% concentration for synthetic coolant
adjustment:
  - If concentration low (<5%): Add coolant concentrate, mix thoroughly
  - If concentration high (>10%): Add water to dilute
monitoring_frequency: Daily check, adjust as needed
health_hazards: Bacterial growth if concentration too low, skin irritation if too high
disposal: Spent coolant classified as hazardous waste, disposed per EPA regulations
```

### Chip Evacuation and Recycling
```annotation
type: waste_management
context: Metal chips generated during machining must be removed from machine and recycled
equipment: Hinged steel belt chip conveyor, 4,000 lb capacity chip bin
chip_types:
  - Aluminum: Long stringy chips, easy to recycle, high scrap value
  - Steel: Short chips, recyclable, moderate scrap value
  - Stainless steel: Tough chips, harder on tooling, recyclable
conveyor_operation:
  - Chips fall through machine table into conveyor trough
  - Conveyor belt carries chips up incline to discharge chute
  - Chips drop into wheeled bin for transport to recycling area
coolant_recovery: Chip wringer removes coolant from chips (squeeze roller system), returns coolant to sump
recycling: Scrap metal vendor picks up bins weekly, pays per pound for clean segregated chips
safety: Chips are sharp, handle with gloves, avoid reaching into chip bin
```

### Coolant Filtration and Sump Cleaning
```annotation
type: maintenance_procedure
context: Coolant filtration removes fines (small particles) that degrade finish and clog nozzles
equipment: Drum filter (50 μm filter media), magnetic separator for ferrous fines
filtration_process:
  - Coolant pumped through rotating drum filter
  - Filter media captures particles, clean coolant returns to sump
  - Dirty filter media advances to scraper, fines discharged to waste bin
magnetic_separation: Permanent magnets remove ferrous chips and fines, prevent abrasive damage
sump_cleaning: Quarterly task, drain and clean machine coolant sump
procedure:
  1. Pump out coolant to temporary tank
  2. Remove chip sludge from sump bottom (wet-dry vacuum)
  3. Scrub sump walls with brush and cleaner
  4. Rinse with water, inspect for leaks or corrosion
  5. Refill with fresh coolant mix at proper concentration
  6. Run machine for 15 minutes to circulate and purge air
benefit: Clean coolant extends tool life, improves surface finish, prevents coolant-related dermatitis
```

## 8. Preventive Maintenance and Lubrication

### Machine Axis Lubrication
```annotation
type: maintenance_task
context: CNC machine way surfaces and ball screws require regular lubrication for accuracy and longevity
equipment: Automatic lubrication system (Bijur Delimon), way lube oil (Mobil Vactra Oil No. 2)
lubrication_schedule:
  - Way surfaces (X, Y, Z axes): Automatic lube every 8 hours of machine operation
  - Ball screw bearings: Grease every 2,000 hours (Mobil Polyrex EM grease)
  - Spindle bearings: Grease every 5,000 hours or annually (spindle grease per machine manual)
procedure:
  - Automatic system: Controller triggers lube pump, oil distributed to way surfaces via metering valves
  - Manual greasing: Use grease gun at designated fittings, pump until fresh grease appears
  - Check oil reservoir level weekly, refill as needed (5-liter capacity)
consequences_of_neglect: Increased friction, wear on ways, loss of positioning accuracy, costly repairs
inspection: During PM, check for oil leaks, verify lube distribution to all points, clean any clogged lines
```

### Spindle Bearing Maintenance
```annotation
type: critical_maintenance
context: Spindle bearings are precision components requiring proper maintenance for accuracy and uptime
equipment: Angular contact ball bearings or tapered roller bearings, grease or oil lubrication
maintenance_schedule:
  - Grease-lubricated spindles: Re-grease every 5,000 hours or annually
  - Oil-mist lubricated spindles: Check oil level daily, top off as needed
  - Oil-air lubricated spindles: Check pump operation, verify oil flow to bearings
warning_signs:
  - Unusual noise (grinding, squealing) indicates bearing wear
  - Spindle temperature >60°C (140°F) indicates insufficient lubrication
  - Vibration increase (measure with vibration meter, compare to baseline)
  - Runout increase (measure with dial indicator, compare to spec ±0.0002")
repair: Spindle rebuild requires factory service or specialized rebuilder, cost $5,000-$15,000
prevention: Follow manufacturer's lubrication schedule religiously, monitor bearing condition
downtime_impact: Unplanned spindle failure = 3-5 days downtime, planned rebuild = 1-2 days
```

### Controller Battery Replacement
```annotation
type: routine_maintenance
context: CNC controller has backup battery to retain programs, offsets, and parameters during power loss
equipment: Lithium battery (3.6V) in controller cabinet, typical life 5-7 years
warning_signs:
  - "Low Battery" alarm on controller display
  - Battery voltage <3.0V (check with multimeter)
  - Loss of programs/offsets after power cycling
replacement_procedure:
  1. Power up controller (battery replacement must be done with power ON to prevent memory loss)
  2. Open controller cabinet door (key required)
  3. Locate battery (usually on main PCB or in battery holder)
  4. Note battery part number (e.g., Fanuc A98L-0031-0011, Siemens 6FC5247-0AA00-0AA0)
  5. Remove old battery, immediately install new battery (within 30 seconds)
  6. Close cabinet, verify no alarms on controller
  7. Backup all programs to USB drive as precaution
frequency: Replace every 5 years or when low battery alarm appears
consequence_of_failure: Loss of all programs, tool offsets, work offsets, parameters - major downtime!
```

## 9. Troubleshooting and Alarm Response

### Common CNC Alarms and Resolutions
```annotation
type: fault_diagnosis
context: CNC controllers generate alarms for faults, operators trained to diagnose and resolve
alarm_examples:
  - Alarm 010: Emergency stop activated
    Resolution: Identify e-stop button pressed, release, reset alarm
  - Alarm 074: Z-axis overtravel (soft limit)
    Resolution: Jog axis away from limit in opposite direction, verify work offset not incorrect
  - Alarm 201: Servo alarm (following error too large)
    Resolution: Check for mechanical binding, verify axis not hitting obstruction
  - Alarm 410: Tool changer fault (tool not released from spindle)
    Resolution: Check air pressure (90 PSI required), manually cycle drawbar if necessary
  - Alarm 500: Parity alarm (memory error)
    Resolution: Power cycle controller, if persists replace battery and restore backup
response_protocol:
  1. Read alarm number and description on controller screen
  2. Consult alarm manual (book or PDF on shop computer)
  3. Attempt resolution per manual instructions
  4. If unresolved, escalate to maintenance technician
  5. Log alarm event in machine logbook (date, time, operator, resolution)
training: Operators receive 2-hour alarm response training, annual refresher
```

### Crash Recovery Procedure
```annotation
type: emergency_response
context: Machine crash (tool collision with part, fixture, or machine) requires careful recovery
immediate_actions:
  1. Press emergency stop (halt all motion immediately)
  2. Assess damage (visual inspection of tool, part, fixture, machine)
  3. Do NOT attempt to jog axes until damage assessed (may worsen damage)
safety_concerns:
  - Broken tool fragments may be sharp and ejected at high speed
  - Part or fixture may be dislodged and fall
  - Machine accuracy may be compromised (bent ball screw, damaged way surface)
damage_assessment:
  - Inspect tool for breakage (replace if damaged)
  - Check part for damage (scrap if beyond repair)
  - Inspect fixture for cracks or deformation (replace if damaged)
  - Check machine axes for smooth motion (jog slowly, feel for binding)
  - Verify spindle runout (measure with dial indicator, compare to baseline)
recovery_steps:
  1. Replace broken tool
  2. Remove damaged part and fixture if necessary
  3. Carefully jog axes to home position
  4. Run machine diagnostic routine (available in controller diagnostics menu)
  5. If diagnostics pass, run test program on scrap material before resuming production
  6. If diagnostics fail, call machine tool service technician
root_cause_analysis: Investigate why crash occurred (programming error, setup error, tool wear, machine malfunction)
prevention: Crashes are preventable - proper simulation, dry run, operator vigilance critical
```

### Cutting Tool Breakage Response
```annotation
type: production_interruption
context: Cutting tool breaks during operation, immediate response required to prevent further damage
detection:
  - Audible change in cutting sound (loud bang or grinding)
  - Spindle load spike (amperage increase)
  - Machine vibration increase
  - Tool breakage detection system alarm (if equipped)
immediate_response:
  1. Press feed hold to pause program (do NOT press e-stop unless danger of collision)
  2. Raise Z-axis to clear part
  3. Inspect tool for breakage (visually or via spindle camera if equipped)
  4. If tool broken, press e-stop and proceed with tool replacement
tool_replacement:
  1. Remove broken tool from spindle (may require manual drawbar release if fragment jammed)
  2. Inspect spindle taper for damage (clean with solvent, check for burrs)
  3. Install new tool (same tool number, pre-measured length and diameter offsets)
  4. Verify tool securely seated in spindle (pull test with 50 lbs force)
  5. Re-zero tool length offset if tool presetter not used
  6. Restart program from safe line (before tool breakage point)
part_inspection: Check part for damage from broken tool (gouges, incorrect feature), scrap if damage found
root_cause: Investigate cause (dull tool, excessive feed/speed, material defect, coolant failure)
```

## 10. Documentation and Traceability

### Setup Sheet and Operation Instructions
```annotation
type: production_documentation
context: Each part number has setup sheet detailing fixtures, tools, and inspection requirements
content:
  - Part number, revision, material specification
  - Fixture and workholding method
  - Tool list (tool number, description, length offset, diameter offset)
  - Program number and revision
  - Critical dimensions and tolerances to check
  - Inspection frequency (first, last, and every 10 parts)
  - Estimated cycle time and parts per hour
  - Special notes (coolant type, deburring requirements, etc.)
location: Laminated setup sheet posted at each CNC machine, digital copy in network folder
revision_control: Engineering controls setup sheets, operators notified of revisions via email
training: New operators review setup sheet with supervisor before running unfamiliar parts
```

### Part Serial Number Traceability
```annotation
type: quality_traceability
context: Critical parts (aerospace, medical) require full traceability from raw material to finished part
marking_method: Dot peen marking, laser engraving, or data matrix code etched on part
serial_number_format: Part number + sequential number + date code (e.g., 12345-00123-2025001)
traceability_data:
  - Raw material heat number and mill test report
  - CNC machine used, program revision, operator ID
  - Inspection data (FAI report, in-process measurements, final CMM inspection)
  - Date and time of production
data_storage: Traceability data stored in MES database, retained 7-10 years per customer requirements
audit: Quality audits verify traceability records complete and accurate, non-conformances addressed
standard: AS9102 for aerospace, ISO 13485 for medical devices
```

### Maintenance and Calibration Records
```annotation
type: equipment_records
context: Machine maintenance and calibration must be documented for quality system compliance
maintenance_log:
  - Date and description of preventive maintenance tasks
  - Parts replaced (spindle bearings, way wipers, coolant pump, etc.)
  - Technician name and hours spent
  - Next scheduled PM date
calibration_records:
  - Laser interferometer calibration of X, Y, Z axis positioning accuracy (annually)
  - Ballbar test for circular interpolation accuracy (semi-annually)
  - Spindle runout measurement (quarterly)
  - Calibration certificates for inspection equipment (CMM, height gage, micrometers)
retention: Maintenance logs retained 5 years, calibration records retained 7 years
audit: ISO 9001 audits verify equipment maintained per schedule, calibration records current
```

## Document Control
- **Version**: 1.8
- **Last Updated**: 2025-11-06
- **Approved By**: Manufacturing Engineering Manager, Quality Manager
- **Review Frequency**: Annual or upon equipment/process changes
- **Distribution**: All CNC machinists, setup personnel, quality inspectors, supervisors
