# Dams Sector - Equipment & Systems Catalog

**Document Version:** 1.0
**Classification:** Equipment Inventory
**Last Updated:** 2025-11-05
**Coverage:** Hydroelectric & Dam Safety Equipment

## Executive Summary

This document catalogs the major equipment systems found in dam facilities, including specifications, operational characteristics, maintenance requirements, and cybersecurity considerations. Equipment is organized by functional system and criticality to dam operations and safety.

---

## 1. Hydraulic Turbines (70+ Patterns)

### 1.1 Francis Turbines

**FRANCIS-001: High-Head Francis Turbines (>150m head)**
```
SPECIFICATIONS:
Head range: 150m - 700m
Capacity: 50 MW - 800 MW per unit
Runner diameter: 2m - 6m
Rotational speed: 300 - 600 RPM
Efficiency: 92-95% at best efficiency point (BEP)

APPLICATIONS:
- Large storage dams
- Pumped storage (upper reservoirs)
- Mountain hydroelectric plants
- Examples: Hoover Dam, Grand Coulee Dam

RUNNER CONFIGURATION:
- Fixed blades: 9-17 blades typical
- Material: Cast or welded stainless steel (CA6NM, 13Cr4Ni)
- Cavitation resistance: Special coatings, optimal profiles
- Blade thickness: Varies from inlet to outlet

WICKET GATE SYSTEM:
- Number of gates: 16-32 gates typical
- Actuation: Servo motor (hydraulic cylinder or electric motor)
- Control range: 0% (fully closed) to 100% (fully open)
- Synchronization: Distribution ring connects all gates
- Position accuracy: ±0.5% of full travel

DRAFT TUBE:
- Type: Elbow or straight cone
- Purpose: Pressure recovery, efficiency improvement
- Cavitation prevention: Air admission valves
- Material: Concrete lined with steel plate or epoxy coating

GOVERNOR SYSTEM:
- Type: Electro-hydraulic or fully digital
- Response time: <0.1 second to 95% of setpoint
- Control modes: Speed, load, gate position
- Stability: PID tuning, dashpot damping
- Safety: Overspeed trip, pressure relief

OPERATIONAL CHARACTERISTICS:
- Startup time: 5-15 minutes from rest to full load
- Load ramping: 10-50 MW/minute typical
- Minimum flow: 20-40% of rated (to prevent recirculation)
- Cavitation limits: Head-dependent, σ (sigma) factor

MAINTENANCE:
Annual Inspection:
- Wicket gate linkage: Pins, bushings, seals
- Runner visual inspection: Cavitation damage, cracks
- Governor system: Hydraulic oil, servo valves
- Seals: Labyrinth seals, shaft packing

5-Year Overhaul:
- Runner removal and inspection
- Non-destructive testing (ultrasonic, magnetic particle)
- Bearing replacement
- Seal replacement

CYBERSECURITY CONSIDERATIONS:
- Governor PLC: Secure configuration, patching
- Position sensors: Dual redundancy, tamper detection
- Control network: Isolated from IT network
- Remote access: VPN with 2FA if allowed
```

**FRANCIS-002: Medium-Head Francis Turbines (50m-150m)**
```
SPECIFICATIONS:
Head range: 50m - 150m
Capacity: 10 MW - 300 MW per unit
Runner diameter: 2.5m - 8m
Rotational speed: 120 - 300 RPM
Efficiency: 93-96% at BEP (highest efficiency range)

APPLICATIONS:
- Run-of-river plants
- Medium storage dams
- Diversion dams
- Most common head range for Francis turbines

RUNNER DESIGN:
- Blade profile: Optimized for specific head and flow
- Blade count: 13-19 typical
- Hub-to-tip ratio: 0.3-0.5
- Material: Stainless steel castings

OPERATIONAL RANGE:
- Optimal: 70-100% load
- Minimum: 30-40% (recirculation zone)
- Overload: 110% for short periods (10-15 minutes)

CONTROL SYSTEM:
Modern Digital Governor:
- PLC-based: Allen-Bradley, Siemens, ABB
- Control algorithms: Adaptive PID, model-based
- Load management: AGC (Automatic Generation Control) integration
- Data logging: Performance tracking, efficiency monitoring

PERFORMANCE MONITORING:
- Efficiency curves: Head-flow-power relationships
- Cavitation monitoring: Vibration analysis, acoustic sensors
- Temperature monitoring: Bearing, generator, guide bearing
- Flow measurement: Winter-Kennedy (differential pressure) method

REFURBISHMENT OPTIONS:
Runner Replacement:
- Typical life: 30-50 years
- Uprate potential: 10-25% power increase
- CFD design: Computational fluid dynamics optimization
- Cost: $2M-$10M depending on size

Wicket Gate Replacement:
- Typical life: 40-60 years
- Improved seals: Reduce leakage
- Cost: $500K-$3M

Governor Upgrade:
- Replace mechanical-hydraulic with digital
- Improved response, flexibility, monitoring
- Cost: $200K-$1M including commissioning
```

**FRANCIS-003: Low-Head Francis Turbines (<50m)**
```
SPECIFICATIONS:
Head range: 10m - 50m
Capacity: 1 MW - 100 MW per unit
Runner diameter: 3m - 10m
Rotational speed: 60 - 150 RPM
Efficiency: 90-94% at BEP

APPLICATIONS:
- Low-head river dams
- Irrigation diversion dams
- Rehabilitation of old dams
- Small hydroelectric projects

DESIGN CHALLENGES:
- Large diameter runners: Manufacturing and transportation
- Low speed: Large generators, high pole count
- Fish-friendly: Reduced blade count, biological design

FISH-FRIENDLY DESIGNS:
- Reduced blade count: 5-9 blades (vs. 13-19 standard)
- Larger blade spacing: Reduces fish strike mortality
- Smooth flow paths: Minimizes shear stress
- Leading edge profile: Rounded, less damaging
- Trade-off: 1-3% efficiency reduction

OPERATIONAL CONSIDERATIONS:
- High inertia: Slower start/stop times
- Debris vulnerability: Trash rack maintenance critical
- Sediment: Coating wear, requires hard-facing

MAINTENANCE:
- Trash rack cleaning: Daily during high flow, debris seasons
- Runner coating: Epoxy or polyurethane, reapply every 5-10 years
- Bearing maintenance: Large thrust bearing, oil lubrication
```

### 1.2 Kaplan Turbines

**KAPLAN-001: Adjustable-Blade Kaplan Turbines**
```
SPECIFICATIONS:
Head range: 5m - 50m
Capacity: 5 MW - 250 MW per unit
Runner diameter: 3m - 11m
Blade count: 4-8 blades (adjustable pitch)
Rotational speed: 50 - 150 RPM
Efficiency: 90-95% at BEP

ADJUSTABLE BLADE MECHANISM:
Runner Hub:
- Oil-filled: Hydraulic oil for blade servos
- Blade shaft: Rotates within hub
- Servo mechanism: Hydraulic cylinder or rack-and-pinion
- Position feedback: Potentiometer or LVDT

Blade Actuation:
- Oil supplied through hollow turbine shaft
- Rotating seals: Prevent oil leakage
- Control linkage: Synchronizes all blades
- Position accuracy: ±0.5 degrees

DOUBLE REGULATION:
- Wicket gates: Control flow admission
- Runner blades: Control blade angle
- Coordination: Cam relationship between gate and blade position
- Efficiency: Wide operating range (50-100% load)

CAM CURVE:
- Relationship: Gate position vs. blade angle
- Optimization: Maintain efficiency across load range
- Tuning: Field testing, flow measurement
- Example: 100% gate = 25° blade, 50% gate = 15° blade

CONTROL SYSTEM:
Dual-Servo Governor:
- Gate servo: Hydraulic cylinder for wicket gates
- Blade servo: Hydraulic cylinder for runner blades
- Coordination: Electronic cam profile in PLC
- Monitoring: Position feedback, oil pressure, leakage

OPERATIONAL ADVANTAGES:
- Wide efficiency range: 50-100% load at >90% efficiency
- Partial load operation: Better than Francis
- Startup efficiency: Efficient at low flows
- Overload capacity: 115-120% for short periods

MAINTENANCE CHALLENGES:
- Oil system complexity: Shaft seals, rotating seals
- Blade mechanism wear: Pins, bushings, linkages
- Oil contamination: Water ingress detection
- Overhaul cost: Higher than fixed-blade designs

TYPICAL MAINTENANCE:
Annual:
- Check oil levels and quality
- Inspect blade position sensors
- Test blade movement (full travel)
- Check for oil leaks

5-Year Major:
- Runner removal
- Blade mechanism overhaul
- Seal replacement
- Bearing replacement
```

**KAPLAN-002: Fixed-Blade Propeller Turbines**
```
SPECIFICATIONS:
Head range: 5m - 30m
Capacity: 1 MW - 50 MW per unit
Runner diameter: 2m - 8m
Blade count: 4-8 blades (fixed pitch)
Rotational speed: 60 - 180 RPM
Efficiency: 88-92% at BEP (narrower than adjustable Kaplan)

DESIGN CHARACTERISTICS:
- Fixed blade angle: Optimized for single operating point
- Simpler construction: No blade adjustment mechanism
- Lower cost: 20-30% less than adjustable Kaplan
- Trade-off: Reduced efficiency at partial loads

APPLICATIONS:
- Run-of-river: Steady flow, minimal load variation
- Small hydro: Cost-sensitive projects
- Irrigation: Predictable seasonal flows
- Rehabilitation: Replace old fixed-pitch turbines

EFFICIENCY CURVE:
- Peak efficiency: 90-92% at 100% load
- 80% load: 85-88% efficiency
- 60% load: 75-80% efficiency (significant drop-off)

OPERATIONAL STRATEGY:
- Operate near full load: Maximize efficiency
- Multiple units: Stage units for varying flows
- Seasonal optimization: Summer vs. winter flows

MAINTENANCE:
- Simpler than adjustable Kaplan
- No oil system for blades
- Runner inspection: Easier, no blade mechanism
- Lower overhaul costs
```

### 1.3 Pelton Turbines

**PELTON-001: High-Head Pelton Turbines**
```
SPECIFICATIONS:
Head range: 300m - 2000m
Capacity: 50 MW - 500 MW per unit
Jet count: 2-6 jets per runner
Runner diameter: 2m - 5m
Rotational speed: 300 - 1000 RPM
Efficiency: 90-94% at BEP

PELTON WHEEL DESIGN:
Buckets:
- Count: 15-35 buckets on runner periphery
- Material: Stainless steel casting or machining
- Shape: Double-cup, splitter ridge
- Surface finish: Polished to reduce friction

Jet Nozzles:
- Needle valve: Controls flow per jet
- Spear: Conical tip, slides in/out of nozzle
- Servo motor: Electric or hydraulic actuation
- Flow range: 0-100% per jet

Deflector:
- Purpose: Rapid load rejection (bypass jet)
- Actuation: Fast-acting hydraulic or pneumatic
- Response time: <1 second to full deflection
- Use case: Emergency shutdown, prevent overspeed

GOVERNOR CONTROL:
Multi-Jet Coordination:
- Simultaneous control: All jets move together (typical)
- Sequential control: Stage jets for efficiency (advanced)
- Deflector logic: Activate on rapid load rejection

Pressure Control:
- Surge tank: Dampen pressure transients
- Bypass valves: Relieve pressure during closure
- Water hammer: Limit rate of needle closure

OPERATIONAL CHARACTERISTICS:
- No draft tube: Atmospheric exhaust
- Free jet: No back pressure effects
- Efficiency: Relatively flat over 30-100% load range
- Partial jets: Operate with 1, 2, 3, etc. jets active

MAINTENANCE:
Bucket Inspection:
- Erosion: Sand abrasion, cavitation pitting
- Cracks: Fatigue from cyclic loading
- Coating: Hard-facing (tungsten carbide) for sand-laden water
- Replacement: Individual buckets or entire runner

Needle Valve Maintenance:
- Seal replacement: Prevent leakage
- Stem straightness: Check for bending
- Servo calibration: Position accuracy

CHALLENGES:
- Erosion in sandy water: Requires hard coatings
- Splashing: Water containment, powerhouse drainage
- Noise: High-velocity jets, sound dampening required
```

### 1.4 Pump-Turbines (Pumped Storage)

**PUMP_TURBINE-001: Reversible Pump-Turbines**
```
SPECIFICATIONS:
Head range: 200m - 700m
Turbine capacity: 200 MW - 500 MW per unit
Pump capacity: 150 MW - 400 MW (as motor)
Runner type: Francis-type reversible runner
Speed: 300 - 600 RPM

OPERATING MODES:
Turbine Mode:
- Water flows from upper to lower reservoir
- Generates electricity during peak demand
- Typical operation: 6-10 hours per day

Pump Mode:
- Water pumped from lower to upper reservoir
- Consumes electricity during off-peak
- Typical operation: 8-12 hours per day
- Motor-Generator operates as motor

Transition:
- Mode change time: 5-15 minutes
- Procedure: Stop → Reverse rotation → Start
- Synchronization: Grid frequency matching

RUNNER DESIGN:
- Compromise: Optimized for both pumping and turbining
- Efficiency trade-off: Lower than dedicated turbine/pump
- Turbine efficiency: 88-92%
- Pump efficiency: 85-90%
- Round-trip efficiency: 75-85% (including losses)

MOTOR-GENERATOR:
- Synchronous machine: Can operate as motor or generator
- Starting: Back-to-back converters or pony motor
- Power electronics: Variable frequency drives for variable speed
- Excitation: Adjustable for leading/lagging power factor

VARIABLE SPEED PUMP-TURBINES:
Technology:
- Doubly-fed induction generator (DFIG) or full-converter
- Speed range: ±10% of synchronous speed
- Advantages: Improved efficiency, grid frequency support
- Cost: 15-20% higher than fixed-speed

Benefits:
- Efficiency gain: 2-5% improvement across operating range
- Grid services: Frequency regulation, reactive power
- Flexibility: Optimize pump/turbine performance separately

CONTROL SYSTEM:
- Complex coordination: Turbine, motor, converter
- Mode transitions: Automated sequences
- Safety interlocks: Prevent improper mode changes
- Monitoring: Vibration, pressure, temperature, efficiency

TYPICAL INSTALLATION:
- Bath County Pumped Storage (Virginia): 3,003 MW, 6 units
- Ludington Pumped Storage (Michigan): 1,872 MW, 6 units
- Raccoon Mountain (Tennessee): 1,652 MW, 4 units
```

---

## 2. Generators & Exciters (60+ Patterns)

### 2.1 Synchronous Generators

**GENERATOR-001: Large Hydro Generators (>100 MVA)**
```
SPECIFICATIONS:
Capacity: 100 MVA - 1000 MVA
Voltage: 13.8 kV - 25 kV (generator terminals)
Cooling: Water or hydrogen
Poles: 32-128 poles (low-speed hydro)
Speed: 60 - 180 RPM (for 60 Hz)
Efficiency: 98-99%

STATOR CONSTRUCTION:
Stator Core:
- Laminations: Silicon steel, 0.35-0.5mm thick
- Insulation: Between laminations to reduce eddy currents
- Stacking: Precision alignment, compressed and clamped
- Cooling ducts: Radial and axial ventilation

Stator Windings:
- Configuration: 3-phase, wye-connected
- Conductor: Copper bars, Roebel transposition
- Insulation: Class F (155°C) or Class H (180°C)
- Cooling: Direct water cooling (hollow conductors) for large units
- Connections: Phase leads to generator circuit breaker

ROTOR CONSTRUCTION:
Rotor Types:
- Salient pole: Hydro generators (low speed, high poles)
- Round rotor: Steam/gas turbines (high speed, 2-4 poles)

Salient Pole Rotor:
- Spider: Structural frame, keyed to shaft
- Poles: 32-128 poles bolted to spider
- Field windings: Copper coils on each pole
- Damper bars: Amortisseur winding for stability
- Fan blades: Mounted on rotor for air circulation

Field Winding:
- Excitation: DC current creates magnetic field
- Insulation: Class F or H
- Connections: Slip rings (or brushless exciter)

COOLING SYSTEMS:
Air Cooling (up to ~150 MVA):
- Open system: Ambient air intake, exhaust to atmosphere
- Closed system: Recirculate cooled air
- Heat exchanger: Air-to-water coolers
- Temperature: Winding 100-120°C, air 40-60°C

Water Cooling (100-500 MVA):
- Stator windings: Direct water through hollow conductors
- Water quality: Demineralized, <1 µS/cm conductivity
- Closed loop: Heat exchanger to cooling tower or river
- Leakage detection: Conductivity monitors

Hydrogen Cooling (>400 MVA):
- Stator core: H2 gas cooling
- Rotor: H2 cooling
- Purity: >95% H2, <4% air (explosion limits)
- Pressure: 45-75 psig
- Seal oil system: Prevent H2 leakage at shaft
- CO2 purging: Safety for maintenance entry

MONITORING:
Temperature Monitoring:
- Stator windings: RTDs embedded in windings
- Rotor: Slip ring temperature
- Bearings: Guide bearing, thrust bearing RTDs
- Cooling medium: Inlet/outlet temperatures

Vibration Monitoring:
- Bearing housings: Accelerometers or velocity sensors
- Shaft: Proximity probes (radial runout, axial position)
- Alarm levels: Alert, danger, trip
- Trending: Detect bearing wear, unbalance

Insulation Monitoring:
- Insulation resistance (IR): Megohm meter (megger test)
- Polarization index (PI): Time-dependent resistance
- Partial discharge (PD): Online PD monitoring
- Testing frequency: Annual or before startup after outage

PROTECTION:
Generator Protection Relays:
- Differential (87G): Internal faults (phase-to-phase, ground)
- Over/under voltage (27/59): Abnormal voltage
- Over/under frequency (81O/81U): Grid disturbances
- Reverse power (32): Motoring, turbine issues
- Loss of excitation (40): Field failure
- Negative sequence (46): Unbalanced loading
- Stator ground (64): Ground faults
- Rotor ground (64F): Field ground faults

MAINTENANCE:
Annual Maintenance:
- Insulation resistance testing
- Winding tightness check (wedge test)
- Cooling system inspection and cleaning
- Bearing oil analysis
- Vibration trending review

Major Overhaul (10-15 years):
- Stator rewind: If insulation degraded
- Rotor rewind: If field insulation degraded
- Bearing replacement or refurbishment
- Core testing: Ring flux or ELCID test
- Reassemble, test, commission
```

**GENERATOR-002: Medium Hydro Generators (10-100 MVA)**
```
SPECIFICATIONS:
Capacity: 10 MVA - 100 MVA
Voltage: 4.16 kV - 13.8 kV
Cooling: Air-cooled (open or closed)
Speed: 100 - 400 RPM
Efficiency: 96-98%

TYPICAL CONFIGURATION:
- Horizontal shaft: Most common for Francis turbines
- Vertical shaft: Kaplan, bulb turbines
- Umbrella generator: Kaplan turbines, generator above turbine

AIR COOLING:
Open Ventilation:
- Air intake: Filtered ambient air
- Cooling: Direct contact with windings, core
- Exhaust: Discharged outside powerhouse
- Maintenance: Filter cleaning, debris removal

Closed Ventilation:
- Recirculation: Air circulated internally
- Heat exchanger: Air-to-water coolers
- Advantages: Cleaner air, less dust, quieter
- Maintenance: Cooler cleaning, water quality

PROTECTION & MONITORING:
- Similar to large generators but simpler
- Fewer monitoring points
- Combined protective relays (multifunction)

COMMON VENDORS:
- Andritz: HydroMatrix (modular generators)
- Voith: Compact hydro generators
- GE: Medium hydro generators
- WEG: Brazilian manufacturer, competitive pricing
```

**GENERATOR-003: Small Hydro Generators (<10 MVA)**
```
SPECIFICATIONS:
Capacity: 0.1 MVA - 10 MVA
Voltage: 400V - 4.16 kV
Cooling: Air-cooled, self-ventilated
Speed: 200 - 1800 RPM
Efficiency: 93-96%

DESIGN:
- Simpler construction
- Air-cooled only
- Permanent magnet generators (emerging for very small hydro)
- Lower first cost

APPLICATIONS:
- Small run-of-river projects
- Municipal water systems
- Irrigation districts
- Micro-hydro (<1 MW)

VENDORS:
- Canyon Hydro (USA): Integrated turbine-generator packages
- Gilkes (UK): Small hydro specialists
- Mavel (Italy): Compact turbo-generators
```

### 2.2 Excitation Systems

**EXCITER-001: Static Excitation Systems**
```
DESCRIPTION:
- Power source: Generator terminals via excitation transformer
- Rectification: Thyristor or diode bridge
- Brushes: Slip rings transfer DC to rotor field
- Response: Fast (0.1-0.5 seconds to ceiling voltage)

COMPONENTS:
Excitation Transformer:
- Input: Generator terminals (13.8 kV typical)
- Output: Low voltage AC (300-600 VAC)
- Sizing: 1-3% of generator rating

Thyristor Bridge:
- Configuration: Three-phase, full-wave bridge
- Control: Phase-angle control (firing delay)
- Response: Very fast field current adjustment
- Protection: Overvoltage, overcurrent

Automatic Voltage Regulator (AVR):
- Input: Generator voltage, current, power factor
- Output: Thyristor firing signals
- Control modes: Voltage, power factor, VAR
- Limiters: Over-excitation, under-excitation, V/Hz

ADVANTAGES:
- Fast response: Grid stability, fault clearing
- Reliable: Solid-state, fewer moving parts
- Flexible control: Digital AVR, advanced algorithms
- Common in modern hydro plants

MAINTENANCE:
- Brush replacement: Every 1-2 years depending on load cycles
- Slip ring maintenance: Resurface as needed
- Thyristor testing: Gate signals, commutation
- AVR calibration: Annual or after modifications
```

**EXCITER-002: Brushless Excitation Systems**
```
DESCRIPTION:
- Power source: Pilot exciter on generator shaft
- Main exciter: AC generator on shaft, rotating armature
- Rectification: Rotating diodes (silicon diodes on rotor)
- No brushes: DC directly supplied to generator field

COMPONENTS:
Pilot Exciter:
- Type: Permanent magnet generator (PMG)
- Mounting: On generator shaft
- Output: AC power for main exciter field

Main Exciter:
- Configuration: Inverted AC generator
- Stationary field: Controlled by AVR
- Rotating armature: Outputs AC to rotating rectifier

Rotating Rectifier:
- Location: Mounted on generator rotor
- Diodes: Six diodes (three-phase bridge)
- Fuses: Protect diodes from shorts
- Cooling: Air or generator hydrogen

ADVANTAGES:
- No brushes: Reduced maintenance
- Robust: Fewer components, higher reliability
- Suitable for: Hostile environments (moisture, dust)

MAINTENANCE:
- Minimal: No brush replacement
- Diode inspection: Requires rotor removal
- PMG bearings: Grease or oil lubrication
```

---

*Equipment catalog continues with additional systems including transformers, switchgear, gates, valves, and auxiliary equipment...*
