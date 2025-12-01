# PLC Conveyor System Operations

## Overview
Standard operating procedures for PLC-controlled material handling conveyor systems including logic programming, barcode scanning, diverter control, and jam detection.

## Equipment Specifications
- **PLC Controllers**: Allen-Bradley ControlLogix L83E, Siemens S7-1500, Mitsubishi Q-series
- **HMI Panels**: Allen-Bradley PanelView Plus 7, Siemens Comfort Panel
- **Conveyor Motors**: SEW Eurodrive gear motors, variable frequency drives (VFDs)
- **Communication**: EtherNet/IP, PROFINET, Modbus TCP/IP
- **Barcode Scanners**: Cognex DataMan 470, Keyence SR-2000

## 1. System Startup and Initialization

### Pre-Startup Safety Verification
```annotation
type: safety_checklist
context: Before energizing conveyor system, all safety interlocks and e-stops must be verified
equipment: 150-foot conveyor system with 8 zones, 12 e-stop stations
checklist:
  - All emergency stop buttons tested (press/release, verify relay dropout)
  - Light curtains and safety scanners functional (test beam break, verify stop)
  - Guard doors closed and interlocked (magnetic safety switches active)
  - Conveyor path clear of personnel and obstructions
  - Lockout/tagout devices removed from previous maintenance
  - VFD status lights indicate ready (no fault LEDs illuminated)
standard: ANSI B20.1 Safety Standard for Conveyors and Related Equipment
personnel: Authorized production technician with conveyor safety training
```

### PLC Power-Up Sequence
```annotation
type: operational_procedure
context: PLC system must boot and initialize I/O modules before conveyor operations can begin
equipment: Allen-Bradley ControlLogix L83E PLC in redundant configuration
procedure:
  1. Verify 120VAC control power available at main panel
  2. Enable 480VAC 3-phase power for motor circuits (main disconnect ON)
  3. PLC processor boots (LED sequence: red → amber → flashing green → solid green)
  4. Wait for I/O modules to initialize (~15 seconds, green LEDs on all modules)
  5. Verify EtherNet/IP network connection (controller shows online in RSLogix 5000)
  6. Check HMI connection (PanelView Plus displays main screen, no comm faults)
  7. PLC loads retained data from non-volatile memory (production counts, setpoints)
  8. System enters idle state, ready for operator start command
diagnostics: PLC fault table (controller organizer) shows no major or minor faults
redundancy: Backup PLC automatically takes over if primary fails (<50ms switchover)
```

### Zone-by-Zone Conveyor Initialization
```annotation
type: startup_sequence
context: Conveyor system divided into zones, each zone started individually to verify operation
equipment: 8 conveyor zones with independent VFD motor controls
initialization_sequence:
  Zone 1 (Infeed):
    - Operator presses "Zone 1 Start" on HMI
    - PLC verifies safety circuit OK (e-stops clear, guards closed)
    - VFD receives start command via EtherNet/IP (node address 10.20.30.11)
    - Motor ramps to 30 FPM conveyor speed over 2 seconds (soft start)
    - Photo-eye at zone end verifies belt motion (product detection sensor)
  Zone 2-7 (Transfer): Similar sequence, started after upstream zone running
  Zone 8 (Discharge): Final zone to packing station
timing: Each zone started at 5-second intervals (prevents surge at startup)
monitoring: HMI displays real-time status (green = running, red = stopped, yellow = fault)
validation: Run empty conveyor for 5 minutes, verify no alarms or abnormal sounds
```

### Barcode Scanner Configuration
```annotation
type: peripheral_setup
context: Barcode scanners must be configured for symbology, read rate, and communication
equipment: Cognex DataMan 470 fixed-mount barcode reader with Ethernet interface
configuration_parameters:
  - Symbology: Code 128, Data Matrix, QR Code enabled
  - Read rate: 60 reads/second maximum
  - Trigger mode: Continuous (always scanning) or external trigger (photo-eye)
  - Communication: TCP/IP socket connection to PLC (IP 10.20.30.50)
  - Data format: ASCII string terminated with carriage return
  - No-read timeout: 3 seconds (alarm if barcode not decoded)
setup_procedure:
  1. Connect scanner to Ethernet switch via RJ45 cable
  2. Use Cognex software on laptop to set IP address and parameters
  3. Mount scanner 12-18 inches from conveyor surface, perpendicular to product flow
  4. Adjust LED illumination and focus for optimal read performance
  5. Test with sample barcodes (should read reliably at conveyor speed 30-60 FPM)
  6. Configure PLC ladder logic to receive and parse barcode data strings
integration: Barcode data triggers diverter logic, updates MES with product tracking
```

## 2. PLC Programming and Logic Development

### Ladder Logic Structure and Best Practices
```annotation
type: programming_standards
context: PLC programs must be structured, documented, and maintainable per ISA-88 standards
equipment: Allen-Bradley ControlLogix programmed in RSLogix 5000 (Studio 5000)
program_organization:
  - Main Routine: Calls sub-routines in sequential order
  - Safety Routine: E-stop monitoring, guard interlock logic (scanned first)
  - Conveyor Control: Start/stop logic, VFD control, zone sequencing
  - Barcode Scanner: Serial communication, data parsing, validation
  - Diverter Control: Product routing logic based on barcode data
  - Jam Detection: Timer-based logic detects product stuck on conveyor
  - HMI Interface: Tag-based communication with PanelView Plus
  - Alarms and Diagnostics: Fault logging, alarm management
naming_conventions:
  - Tags: Descriptive names (Conv_Zone1_Running, Diverter_03_Position)
  - Rungs: Comments explaining logic purpose
  - Subroutines: Functional names (SR_Conveyor_Start, SR_Jam_Detection)
documentation: Each rung commented, program printout stored with machine documentation
version_control: Programs saved with revision numbers, change log maintained
```

### Motor Control and VFD Integration
```annotation
type: motion_control
context: PLC controls VFD to adjust conveyor speed, acceleration, and braking
equipment: SEW Movitrac LTE-B VFD with EtherNet/IP adapter
control_method: PLC sends speed reference (0-100%) and run/stop commands via network
ladder_logic_example:
  - IF Zone1_Start_PB AND Safety_OK AND NOT Zone1_Fault
  - THEN Set Zone1_VFD_Run = 1 (digital output to VFD)
  - AND Set Zone1_VFD_Speed = Conv_Speed_Setpoint (analog 0-100%)
  - VFD responds with actual speed, motor current, fault status
speed_control:
  - Normal speed: 30 FPM (100% speed reference)
  - Reduced speed: 15 FPM (50% speed reference for delicate products)
  - Creep speed: 3 FPM (10% speed reference for manual troubleshooting)
acceleration_deceleration: Ramp time 2 seconds (prevents product tipover or spillage)
fault_handling: If VFD faults (overcurrent, overtemp), PLC stops upstream zones and alarms HMI
```

### Barcode Scanning and Product Tracking Logic
```annotation
type: data_acquisition
context: PLC receives barcode data, validates format, and routes product to correct destination
equipment: Cognex DataMan 470 scanner, Allen-Bradley L83E PLC
data_flow:
  1. Photo-eye detects product entering scan zone (digital input to PLC)
  2. PLC sends trigger command to scanner via Ethernet (MSG instruction)
  3. Scanner reads barcode, sends ASCII string to PLC (e.g., "PART12345<CR>")
  4. PLC receives string into STRING tag (Barcode_Data_01)
  5. PLC parses string to extract part number (substring function)
  6. PLC validates part number against lookup table (array of valid part numbers)
  7. If valid, PLC determines routing (diverter assignment based on part number)
  8. If invalid, PLC triggers reject diverter and logs error to HMI
validation_logic:
  - Check string length (8-12 characters typical)
  - Verify prefix matches expected format (e.g., "PART" prefix required)
  - Lookup part number in database (compare to array of 200 valid part numbers)
no_read_handling: If scanner times out (no barcode decoded in 3 seconds), product diverted to manual inspection lane
traceability: Barcode data logged with timestamp to PLC data table, exported to MES via OPC UA
```

### Diverter Control and Product Sorting
```annotation
type: sorting_logic
context: Pneumatic diverters route products to different lanes based on barcode data
equipment: Numatics rotary diverter actuators (90° rotation), SMC solenoid valves
control_sequence:
  1. Product with barcode "PART00123" enters diverter zone (photo-eye triggers)
  2. PLC looks up part number in routing table (part 123 → Lane 2)
  3. PLC calculates diverter timing (conveyor speed 30 FPM, product 18" from diverter)
  4. After 0.36 second delay, PLC energizes diverter solenoid (digital output ON)
  5. Pneumatic cylinder rotates diverter arm (90° in 0.2 seconds)
  6. Product deflects into Lane 2
  7. After 1 second, PLC de-energizes solenoid (diverter returns to home position)
  8. Photo-eye at Lane 2 confirms product arrival, increments lane counter
timing_precision: ±0.05 second accuracy required for reliable diverting at 30 FPM
multi_lane_sorting: System handles up to 6 destination lanes, 150 parts/minute throughput
error_detection: If product fails to arrive at expected lane (timeout), alarm generated
maintenance: Diverter position sensors verify mechanical alignment, alert if worn or misaligned
```

### Jam Detection and Recovery Logic
```annotation
type: fault_detection
context: PLC monitors conveyor for jammed products using timer-based photo-eye logic
equipment: Banner Q4X photo-eyes at entry and exit of each zone
jam_detection_logic:
  - Photo-eye at zone entry detects product entering (starts timer TON_01)
  - Expected transit time = Zone length / Conveyor speed = 10 ft / 30 FPM = 20 seconds
  - If product does NOT reach exit photo-eye within 30 seconds (timeout), jam detected
  - PLC stops all upstream zones to prevent pile-up
  - PLC sounds alarm horn, displays jam location on HMI (Zone 3 Jam)
  - Operator manually clears jam, resets fault via HMI pushbutton
  - PLC verifies photo-eyes clear before allowing restart
root_cause_prevention:
  - Product misaligned on conveyor → install guide rails
  - Product too heavy → reduce conveyor speed or upgrade motor
  - Worn bearings → schedule preventive maintenance
false_alarm_prevention: Timer preset set to 1.5× expected transit time (accounts for speed variation)
production_impact: Average jam incident = 3 minutes downtime for clearing and restart
```

## 3. HMI Interface and Operator Controls

### Main Screen Layout and Functionality
```annotation
type: user_interface
context: HMI provides real-time status display and operator control interface
equipment: Allen-Bradley PanelView Plus 7 (15" touchscreen, 1024×768 resolution)
screen_elements:
  - Conveyor status: 8 zones displayed with color-coded status (green/red/yellow)
  - Production counter: Parts per hour, shift total, daily total
  - Speed control: Slider bar adjusts conveyor speed setpoint (0-100%)
  - Start/Stop buttons: Master start (all zones), individual zone controls
  - Alarm banner: Scrolling text displays active alarms (up to 10 simultaneous)
  - Date/Time: Real-time clock display
  - Navigation buttons: Jump to detailed screens (alarms, trending, diagnostics)
color_coding:
  - Green: Zone running normally
  - Red: Zone stopped or faulted
  - Yellow: Zone in manual mode or reduced speed
  - Blue: Zone disabled (maintenance mode)
operator_actions: All buttons require press-and-hold for 1 second (prevents accidental activation)
```

### Alarm Management and Prioritization
```annotation
type: fault_handling
context: HMI displays alarms in priority order, guides operator response
equipment: FactoryTalk View SE alarm management system
alarm_priorities:
  - Critical (red): Safety system fault, e-stop active, fire alarm
    Response: Immediate shutdown, supervisor notification required
  - High (orange): Zone jam, scanner communication loss, VFD fault
    Response: Stop affected zone, operator troubleshooting within 5 minutes
  - Medium (yellow): Low part count, preventive maintenance due
    Response: Operator acknowledges, schedules maintenance at shift end
  - Low (white): Informational messages, mode changes
    Response: No action required
alarm_acknowledgment: Operator must press "ACK" button to silence audible alarm (horn)
alarm_logging: All alarms logged to SQL database with timestamp, operator ID, resolution time
trending: Pareto chart of alarm frequency, identifies recurring issues for root cause analysis
```

### Recipe Management and Product Changeover
```annotation
type: production_flexibility
context: HMI allows operator to select product recipes, automatically reconfigures system
equipment: PLC with 50 recipe storage capacity, HMI recipe selection screen
recipe_parameters:
  - Conveyor speed: 15-60 FPM depending on product type
  - Diverter routing table: Maps part numbers to destination lanes
  - Scanner timeout: 1-5 seconds depending on barcode size
  - Jam detection timeout: 10-60 seconds depending on product size
changeover_procedure:
  1. Operator selects new recipe from HMI dropdown menu (e.g., "Product_Family_B")
  2. PLC prompts "Load New Recipe? YES/NO" confirmation screen
  3. Operator presses YES, PLC writes new parameters to active tags
  4. HMI displays "Recipe Loaded: Product_Family_B" confirmation message
  5. Operator verifies mechanical setup complete (guide rails adjusted if needed)
  6. Operator presses "Start Production" to begin with new recipe
changeover_time: Electronic recipe change = 30 seconds, mechanical adjustments may add 5-15 minutes
validation: Run first 10 products through system, verify correct sorting and no jams
```

### Trending and Historical Data Visualization
```annotation
type: performance_analysis
context: HMI trends display real-time and historical data for process optimization
equipment: FactoryTalk View SE with embedded trending objects
trend_displays:
  - Parts per hour trend (line graph, last 8 hours, target line at 150 PPH)
  - Conveyor speed trend (shows speed setpoint and actual speed from VFD)
  - Downtime by zone (bar graph, cumulative downtime per zone for current shift)
  - Scanner read rate (percentage of successful barcode reads vs. attempts)
data_logging: PLC logs data to SQL database every 60 seconds, 90-day retention
analysis: Production supervisors review trends weekly, identify improvement opportunities
examples:
  - Parts per hour trending down over shift → investigate operator fatigue or part quality issues
  - Zone 3 high downtime → target for maintenance or process improvement project
  - Low scanner read rate → check barcode print quality or scanner alignment
```

## 4. Material Handling and Product Flow Control

### Accumulation Zone Control
```annotation
type: buffer_management
context: Accumulation zones allow products to queue when downstream processes stop
equipment: Zero-pressure accumulation conveyor with 8 photo-eye zones
control_strategy:
  - Each photo-eye zone has independent motor control (8 VFDs)
  - When product enters zone and triggers photo-eye, that zone stops
  - Product accumulates without contact (zero back-pressure)
  - When downstream clears, zones release products sequentially
ladder_logic:
  - IF Zone8_PE (photo-eye) = ON AND Zone9_PE = OFF
  - THEN Zone8_Motor = STOP (product waiting in zone 8)
  - ELSE Zone8_Motor = RUN (release product to zone 9)
benefits: Prevents product damage from conveyor pressure, buffers production line speed variations
capacity: 40-foot accumulation zone holds ~25 products (spaced 18" apart)
application: Upstream process fast (200 PPH), downstream slow (150 PPH), accumulation absorbs difference
```

### Slug Release and Batching Control
```annotation
type: flow_control
context: Products released from accumulation in controlled batches to downstream equipment
equipment: Pneumatic pop-up gate at accumulation zone discharge
batching_logic:
  1. Downstream process signals "Ready for Batch" (digital input to PLC)
  2. PLC counts products in accumulation zone (number of photo-eyes blocked)
  3. PLC lowers pop-up gate (solenoid valve energized)
  4. Conveyor releases batch of 5 products (counted by exit photo-eye)
  5. After 5th product, PLC raises pop-up gate (solenoid de-energized)
  6. Batch of 5 products travels to downstream process
  7. Cycle repeats when downstream signals ready again
batch_size: Adjustable via HMI (1-20 products per batch)
timing: Batch release cycle 8-12 seconds depending on batch size and conveyor speed
application: Case packer requires products in groups of 6, slug release provides precise count
```

### Product Gap Control and Spacing
```annotation
type: timing_control
context: Consistent product spacing required for downstream vision inspection or robotics
equipment: Servo-driven metering conveyor with encoder feedback
control_method:
  - Photo-eye detects product entering metering zone
  - PLC calculates target gap (e.g., 24" spacing at 30 FPM = 0.48 second interval)
  - Servo motor accelerates/decelerates conveyor to achieve target gap
  - Encoder provides position feedback (2048 pulses per revolution)
  - PLC adjusts speed in real-time to maintain ±1 inch gap tolerance
application: Vision inspection system requires products centered in inspection window
benefits: Eliminates manual spacing adjustments, increases throughput consistency
accuracy: ±0.5 inch spacing tolerance at 60 FPM conveyor speed
integration: PLC sends position data to downstream robot via EtherNet/IP
```

### Dynamic Speed Matching Between Zones
```annotation
type: synchronized_motion
context: Adjacent conveyor zones automatically adjust speed to prevent product gaps or collisions
equipment: Multiple VFD-controlled zones with master/slave speed coordination
control_algorithm:
  - Master zone (Zone 1) runs at operator-selected speed (30 FPM)
  - Slave zones (Zones 2-8) automatically match master speed via PLC calculation
  - Speed_Slave = Speed_Master × (Length_Slave / Length_Master)
  - If product detected on slave zone, slave speed reduces 5% to create gap
  - When product exits slave zone, speed returns to master speed
benefits: Smooth product transfer between zones, no jarring or product damage
tuning: PID loop in PLC optimizes speed changes (proportional gain, integral time, derivative time)
monitoring: HMI displays actual speed of each zone in real-time (30.2 FPM, 29.8 FPM, etc.)
fault_condition: If slave zone speed deviates >10% from master, alarm generated (mechanical issue)
```

## 5. Safety Systems and Interlocks

### Emergency Stop Circuit Architecture
```annotation
type: safety_critical
context: E-stop circuit must be fail-safe, redundant, and comply with Category 3 safety per ISO 13849-1
equipment: 12 e-stop buttons (Eaton RMQ-Titan), safety relays (Pilz PNOZ X7)
circuit_design:
  - All e-stop buttons wired in series (normally-closed contacts)
  - Safety relay monitors circuit continuity (24VDC loop)
  - If any e-stop pressed, relay contacts open and cut power to all motor starters
  - Dual-channel monitoring (two independent circuits for redundancy)
  - PLC reads safety relay status but does NOT control safety outputs directly
reset_procedure:
  1. Operator identifies and releases pressed e-stop button (twist to unlock)
  2. Operator verifies area safe to resume operation
  3. Operator presses safety relay reset button (on main control panel)
  4. Safety relay re-energizes, enables motor starters
  5. Operator presses conveyor start button on HMI to resume production
response_time: <50ms from e-stop press to all motors de-energized (Category 3 stop per IEC 60204-1)
testing: E-stop circuit tested monthly, safety relay contacts verified with multimeter
```

### Light Curtain and Area Scanner Integration
```annotation
type: perimeter_guarding
context: Light curtains create virtual barriers, stop conveyor if beam broken by personnel
equipment: SICK C4000 Entry safety light curtain (40 beams, 1800mm height)
safety_function:
  - Light curtain transmitter and receiver mounted on opposite sides of conveyor
  - When beam broken (person reaches into conveyor), receiver signals PLC via safety input
  - PLC immediately stops conveyor zone (via safety relay, not standard output)
  - Audible alarm sounds, HMI displays "Light Curtain Triggered - Zone 5"
  - Operator must clear intrusion, reset light curtain before restart allowed
muting_function:
  - When product legitimately passes through light curtain, beams temporarily muted
  - Muting activated by upstream and downstream photo-eyes (product presence verified)
  - Muting duration limited to 3 seconds maximum (safety standard requirement)
  - If muting exceeded, safety fault generated (indicates product stuck in curtain)
safety_distance: Light curtain positioned 12 inches from nearest pinch point (per ANSI B11.19)
validation: Light curtain safety performance validated by TÜV certification, annual audit required
```

### Guard Interlock Monitoring
```annotation
type: access_control
context: Guard doors must be closed and latched before conveyor can operate
equipment: Schmersal AZM 200 safety door switches with solenoid locking
interlock_logic:
  - Guard door equipped with magnetic safety switch (normally-open contact)
  - When door closed, switch closes and enables safety relay
  - When door opens, switch opens and stops conveyor immediately
  - Solenoid lock prevents door opening while conveyor running (unless e-stop pressed)
trapped_key_system:
  - To access guarded area during maintenance, operator inserts key in lock
  - Key removal only possible when conveyor stopped and locked out
  - Key required to reset conveyor after maintenance complete
applications: Guards protect pinch points (belt-to-pulley, chain-to-sprocket, diverter mechanisms)
compliance: Guard interlocks meet OSHA 29 CFR 1910.212 requirements for machine guarding
testing: Functional test of all guards weekly, documented in safety log
```

### Lockout/Tagout (LOTO) Procedures
```annotation
type: energy_isolation
context: Maintenance personnel must isolate all energy sources before servicing conveyor
standard: OSHA 29 CFR 1910.147 Control of Hazardous Energy
procedure:
  1. Notify affected personnel of impending shutdown
  2. Stop conveyor using normal shutdown procedure (HMI stop button)
  3. Open and lock main electrical disconnect (480VAC power OFF)
  4. Apply lockout device and personal tag to disconnect
  5. Verify zero energy state (test motor start button, no response)
  6. Bleed pneumatic lines (relieve 90 PSI air pressure)
  7. Apply additional locks to pneumatic valves if needed
  8. Perform maintenance work
  9. Remove tools, verify area safe
  10. Remove lockout devices in reverse order
  11. Restore power, restart conveyor
group_lockout: Multiple technicians each apply personal lock to disconnect (hasps accommodate 6 locks)
training: Annual LOTO training required for all maintenance personnel, competency verification
enforcement: Supervisor verifies LOTO compliance before authorizing maintenance work
```

## 6. Preventive Maintenance and Troubleshooting

### Conveyor Belt Inspection and Tracking Adjustment
```annotation
type: routine_maintenance
context: Conveyor belts must be inspected for wear and tracking to prevent failures
equipment: 1.5" wide rubber-coated fabric conveyor belt, 50-foot lengths
inspection_schedule: Weekly visual inspection, monthly tracking adjustment
inspection_points:
  - Belt surface: Check for cuts, tears, excessive wear (replace if >50% worn)
  - Belt tracking: Belt should run centered on rollers (±1 inch acceptable)
  - Belt tension: Press belt midspan, should deflect 2-3 inches (proper tension)
  - Splices: Inspect belt splice for separation (mechanical fasteners or vulcanized)
tracking_adjustment:
  1. Identify which side belt is running toward (e.g., belt drifts left)
  2. Adjust tail pulley alignment (loosen bolts, rotate pulley right side forward)
  3. Run conveyor and observe tracking (should move toward center)
  4. Fine-tune adjustment until belt centered
  5. Tighten bolts, re-check after 30 minutes of operation
belt_tensioning: Adjust take-up mechanism (screw-type or gravity-type) to maintain proper tension
replacement_frequency: Belts last 2-5 years depending on load, speed, and product abrasiveness
```

### Motor and VFD Maintenance
```annotation
type: electrical_maintenance
context: Conveyor motors and VFDs require periodic inspection and testing
equipment: SEW Eurodrive gear motors (0.5-5 HP), Movitrac LTE-B VFDs
motor_inspection:
  - Visual: Check for excessive vibration, unusual noise, overheating
  - Electrical: Measure motor current with clamp meter (compare to nameplate rating)
  - Mechanical: Inspect motor coupling for wear, check mounting bolts tight
  - Lubrication: Grease motor bearings every 2,000 hours (if not sealed bearings)
vfd_maintenance:
  - Check cooling fans operational (VFD heatsink temperature <60°C)
  - Inspect DC bus capacitors (bulging indicates end-of-life, replace proactively)
  - Clean dust from heatsink fins (compressed air, quarterly)
  - Verify control wiring connections tight (loose connections cause intermittent faults)
  - Test VFD fault response (simulate overcurrent, verify fault detection and shutdown)
vfd_parameters: Backup VFD parameters to file before any changes (restore if needed)
replacement: Motors last 10-15 years, VFDs 7-10 years (capacitor life limits VFD lifespan)
```

### Photo-Eye Cleaning and Alignment
```annotation
type: sensor_maintenance
context: Photo-eyes must be clean and properly aligned for reliable product detection
equipment: Banner Q4X laser photo-eyes, retro-reflective and through-beam types
cleaning_procedure:
  1. Power off sensor (or use sensor lockout switch if available)
  2. Wipe lens with microfiber cloth (dry or with isopropyl alcohol if oily)
  3. Avoid scratching lens (use soft cloth only, no abrasives)
  4. Power on sensor, verify indicator LED lights when target present
alignment_procedure:
  - Through-beam: Adjust emitter and receiver until received signal strength >90% (display on sensor)
  - Retro-reflective: Aim sensor at reflector, adjust until signal strength >80%
  - Diffuse: Position sensor 2-6 inches from target (per sensor datasheet)
testing: Place product in detection zone, verify digital output to PLC changes state
troubleshooting:
  - No detection: Check sensor power (24VDC present), verify wiring, clean lens
  - False triggers: Reduce sensitivity, adjust mounting position away from vibration sources
  - Intermittent: Check for loose wiring, inspect cable for damage
frequency: Clean photo-eyes monthly (weekly in dusty environments)
```

### PLC Battery Replacement and Backup
```annotation
type: system_maintenance
context: PLC backup battery prevents loss of program and data during power outages
equipment: Allen-Bradley ControlLogix L83E with lithium battery (3.6V, 1450 mAh)
battery_monitoring:
  - PLC displays battery voltage on diagnostics screen (check quarterly)
  - Low battery alarm generated when voltage <2.8V (replace immediately)
  - Battery life typically 5-7 years (depends on power outage frequency)
replacement_procedure:
  1. Power ON PLC (battery replacement must be done with power on to retain memory)
  2. Open controller chassis door
  3. Note battery polarity and part number (1756-BA2)
  4. Remove old battery, immediately install new battery (<30 seconds)
  5. Close chassis door
  6. Verify no major faults on PLC (battery replacement successful)
backup_strategy:
  - Weekly automatic backup of PLC program to CompactFlash card (built-in feature)
  - Monthly manual backup to laptop via USB (RSLogix 5000 upload)
  - Backup files stored on network server (date-stamped, 12-month retention)
recovery: If PLC memory lost, upload backup program and restore from last known good state
```

### Common Conveyor Faults and Resolutions
```annotation
type: troubleshooting_guide
context: Operators trained to diagnose and resolve common conveyor issues
fault_symptoms_and_solutions:
  - Conveyor won't start:
    • Check: E-stop buttons released, guards closed, VFD powered, PLC online
    • Solution: Reset e-stop, close guards, check VFD display for fault code
  - Belt tracking off-center:
    • Check: Belt alignment, pulley alignment, belt tension
    • Solution: Adjust tracking per procedure, re-tension belt if loose
  - Scanner not reading barcodes:
    • Check: Scanner powered (24VDC), lens clean, barcode quality
    • Solution: Clean lens, adjust scanner angle/distance, re-print barcode labels if faded
  - Diverter not actuating:
    • Check: Air pressure (90 PSI), solenoid valve power, cylinder movement
    • Solution: Verify air supply, test solenoid manually, inspect cylinder for binding
  - Excessive motor current:
    • Check: Belt tension, bearing condition, foreign objects jamming belt
    • Solution: Loosen belt tension, replace worn bearings, clear obstructions
escalation: If fault persists after basic troubleshooting, escalate to maintenance technician
documentation: Log all faults and resolutions in maintenance logbook (date, symptom, resolution)
```

## 7. Performance Optimization and Continuous Improvement

### Throughput Analysis and Bottleneck Identification
```annotation
type: process_improvement
context: System throughput limited by slowest zone, identify and resolve bottlenecks
equipment: MES data logging system, production reports
analysis_method:
  1. Review production data for last 30 days (parts per hour by shift)
  2. Calculate average throughput: 145 parts/hour (target: 160 PPH)
  3. Identify zones with highest downtime (Pareto chart analysis)
     - Zone 3: 12% downtime (jam detection issues)
     - Zone 5: 8% downtime (scanner no-reads)
     - Zone 7: 6% downtime (VFD faults)
  4. Prioritize improvement projects based on impact
  5. Implement solutions (adjust jam detection timeout, improve barcode quality, replace aging VFD)
  6. Re-measure throughput after improvements (new average: 158 PPH)
continuous_improvement: Monthly throughput review, kaizen events to address top 3 losses
goal: Achieve world-class OEE >85% (current: 78%, target: 88% by year-end)
```

### Energy Efficiency and Cost Reduction
```annotation
type: sustainability_initiative
context: Reducing conveyor energy consumption lowers operating costs and environmental impact
equipment: VFDs with energy monitoring capabilities, power meters on main panel
baseline_energy_consumption: 12 kW average power during production, 150 kWh per shift
optimization_strategies:
  1. Reduce conveyor speed during low-volume periods (30 FPM → 20 FPM, 15% energy savings)
  2. Implement zone sleep mode (idle zones power down after 5 minutes of inactivity)
  3. Upgrade to high-efficiency motors (IE3 rated, 2-4% energy savings vs. standard motors)
  4. Optimize VFD acceleration/deceleration ramps (reduce peak power demand)
  5. Schedule maintenance during off-peak hours (avoid demand charges)
results:
  - Energy consumption reduced from 150 kWh to 125 kWh per shift (17% reduction)
  - Cost savings: $12,500 per year at $0.10/kWh
  - Payback period: 2 years for motor upgrades and VFD optimization
monitoring: Real-time energy display on HMI, weekly energy usage reports to management
```

### Predictive Maintenance with Vibration Analysis
```annotation
type: condition_monitoring
context: Monitor conveyor motor vibration to detect bearing wear before failure
equipment: Fluke 810 vibration tester, triaxial accelerometer sensor
monitoring_procedure:
  - Measure vibration at motor drive-end and non-drive-end bearings
  - Take readings monthly (radial, axial, and horizontal planes)
  - Compare to baseline vibration spectrum (from when motor new)
  - Alert generated if vibration increases >50% from baseline
vibration_limits:
  - Good: <0.3 in/sec RMS (motor healthy, no action needed)
  - Acceptable: 0.3-0.7 in/sec (monitor more frequently)
  - Unacceptable: >0.7 in/sec (schedule bearing replacement within 30 days)
bearing_failure_signatures:
  - High-frequency peaks: Bearing race defects (replace bearing)
  - Low-frequency peaks: Misalignment (realign motor and load)
  - Broadband noise: Lubrication issues (re-grease bearings)
benefits: Predictive maintenance prevents unplanned downtime (3-4 hour bearing replacement vs. 8-12 hour emergency repair)
ROI: Vibration tester investment $3,000, prevents $15,000-20,000 in downtime costs annually
```

## 8. Integration with MES and Traceability

### Real-Time Production Data Collection
```annotation
type: mes_integration
context: PLC sends production data to MES for real-time visibility and analysis
protocol: OPC UA server in PLC, MES client subscribes to data tags
data_transmitted:
  - Parts produced per hour: 145 actual vs. 160 target
  - Downtime events: Timestamp, duration, reason code (jam, scanner fault, e-stop)
  - Barcode scan results: Part number, timestamp, lane assignment
  - Conveyor status: Zone running/stopped, motor current, VFD frequency
  - Alarm history: All alarms with timestamp and resolution time
frequency: Real-time data streaming (1-second updates), aggregated to 1-minute intervals
visualization: MES dashboard displays real-time conveyor status, OEE calculation, downtime Pareto
alerting: Email/SMS notifications for extended downtime (>15 minutes) or critical alarms
```

### Barcode Traceability and Lot Tracking
```annotation
type: product_traceability
context: Every product tracked from raw material through final packaging via barcode scanning
equipment: Cognex DataMan scanners at multiple points (infeed, diverters, discharge)
traceability_workflow:
  1. Product enters system with unique serial number barcode (e.g., SN123456789)
  2. Scanner 1 reads barcode, logs entry timestamp and conveyor zone
  3. PLC sends data to MES via Ethernet (part number, serial number, timestamp)
  4. Product routed through diverters based on part number
  5. Scanner 2 at discharge confirms product exited correctly, logs timestamp
  6. MES database links serial number to production order, operator, shift
traceability_database:
  - Serial number, part number, production order
  - Entry and exit timestamps (conveyor residence time calculated)
  - Operator ID, shift, date
  - Destination lane assignment
  - Any alarms or faults during product transit
recall_capability: If defect discovered, MES queries database for all products from same lot, identifies location
retention: Traceability data retained 7 years per ISO 9001 quality system requirements
```

### OEE Calculation and Continuous Improvement Tracking
```annotation
type: performance_metrics
context: OEE measures conveyor system utilization, identifies improvement opportunities
formula: OEE = Availability × Performance × Quality
calculation:
  - Availability: (Planned production time - Downtime) / Planned production time
    Example: (480 min - 58 min) / 480 min = 87.9%
  - Performance: (Actual throughput / Target throughput)
    Example: 145 PPH / 160 PPH = 90.6%
  - Quality: (Good parts / Total parts produced)
    Example: 1,152 good / 1,160 total = 99.3%
  - OEE: 0.879 × 0.906 × 0.993 = 79.1%
benchmarking: World-class OEE >85%, current conveyor system 79.1%
improvement_projects:
  - Reduce Zone 3 jams (target: 5% availability gain)
  - Increase conveyor speed from 30 to 35 FPM (target: 10% performance gain)
  - Improve barcode quality (target: 0.5% quality gain)
  - Combined improvement potential: OEE 79.1% → 88.5% (12% gain)
reporting: Weekly OEE review meeting, action items tracked in project management software
```

## Document Control
- **Version**: 1.3
- **Last Updated**: 2025-11-06
- **Approved By**: Manufacturing Engineering Manager, Automation Manager
- **Review Frequency**: Annual or upon equipment/process changes
- **Distribution**: All production operators, maintenance technicians, PLC programmers, supervisors
