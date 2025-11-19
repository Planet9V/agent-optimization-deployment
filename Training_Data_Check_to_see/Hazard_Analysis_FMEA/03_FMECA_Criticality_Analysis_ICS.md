# FMECA: Criticality Analysis for Industrial Control Systems

## Overview
FMECA (Failure Modes, Effects, and Criticality Analysis) extends FMEA by adding criticality analysis to prioritize failure modes by their impact on system mission. This document analyzes ICS component criticality with cybersecurity threat integration.

## Criticality Matrix
**Criticality Number (Cr) = Probability × Severity × Mission Impact**
- **Categories**: I (Catastrophic), II (Critical), III (Marginal), IV (Negligible)
- **Mission Impact**: α (Loss of mission), β (Mission degradation), γ (Maintenance impact)

---

## Criticality Analysis Scenarios

### Critical Item 1: Safety PLC in Nuclear Reactor
The [[EQUIPMENT: Safety instrumented system PLC]] with criticality **Category I-α** experiences failure mode **safety function defeat** caused by [[ATTACK_PATTERN: Safety logic rootkit]] exploiting [[VULNERABILITY: Lack of secure boot in safety PLC]] creating [[HAZARD: Reactor protection system bypass]] with mission impact of **complete safety system loss**. **Criticality: 0.92**. [[MITIGATION: Formally verified safety logic]] and [[ARCHITECTURE: Diverse actuation system]] protect from [[THREAT_ACTOR: Nation-state nuclear program attacker]].

### Critical Item 2: Emergency Shutdown System
The [[EQUIPMENT: Emergency shutdown valve]] with criticality **Category I-α** experiences failure mode **ESD system disable** caused by [[ATTACK_PATTERN: Final element attack]] through [[VULNERABILITY: Unprotected valve controller]] creating [[HAZARD: Loss of emergency protection]] with mission impact of **catastrophic failure unmitigated**. **Criticality: 0.88**. [[MITIGATION: Hardwired ESD logic]] and [[ARCHITECTURE: Pneumatic safety backup]] defend against [[THREAT_ACTOR: Process safety attacker]].

### Critical Item 3: Grid Protection Relay
The [[EQUIPMENT: Power system protection relay]] with criticality **Category I-β** experiences failure mode **incorrect trip decision** caused by [[ATTACK_PATTERN: IEC 61850 GOOSE manipulation]] exploiting [[VULNERABILITY: Unauthenticated substation communications]] creating [[HAZARD: Cascading grid failure]] with mission impact of **regional blackout**. **Criticality: 0.85**. [[MITIGATION: IEC 62351 security implementation]] and [[ARCHITECTURE: Independent protection zones]] prevent [[THREAT_ACTOR: Grid warfare actor]].

### Critical Item 4: Aviation Control Tower System
The [[EQUIPMENT: Air traffic control automation]] with criticality **Category I-α** experiences failure mode **aircraft separation loss** caused by [[ATTACK_PATTERN: Radar data injection]] through [[VULNERABILITY: Unsecured radar feed]] creating [[HAZARD: Mid-air collision risk]] with mission impact of **complete ATC loss**. **Criticality: 0.91**. [[MITIGATION: Radar authentication]] and [[ARCHITECTURE: Independent radar correlation]] protect from [[THREAT_ACTOR: Aviation infrastructure terrorist]].

### Critical Item 5: Dam SCADA Master
The [[EQUIPMENT: Hydroelectric dam SCADA]] with criticality **Category I-α** experiences failure mode **spillway control loss** caused by [[ATTACK_PATTERN: SCADA server takeover]] exploiting [[VULNERABILITY: Remote access vulnerability]] creating [[HAZARD: Uncontrolled water release]] with mission impact of **downstream flooding**. **Criticality: 0.89**. [[MITIGATION: SCADA hardening]] and [[ARCHITECTURE: Local manual override]] defend against [[THREAT_ACTOR: Critical infrastructure saboteur]].

### Critical Item 6: Hospital Oxygen Control
The [[EQUIPMENT: Medical gas control system]] with criticality **Category I-α** experiences failure mode **oxygen pressure loss** caused by [[ATTACK_PATTERN: Building management system attack]] through [[VULNERABILITY: Unprotected BMS interface]] creating [[HAZARD: Patient life support failure]] with mission impact of **mass casualty event**. **Criticality: 0.87**. [[MITIGATION: Medical system isolation]] and [[ARCHITECTURE: Independent oxygen monitoring]] prevent [[THREAT_ACTOR: Healthcare terrorist]].

### Critical Item 7: Railway Signaling Interlocking
The [[EQUIPMENT: Railway interlocking system]] with criticality **Category I-α** experiences failure mode **signal aspect falsification** caused by [[ATTACK_PATTERN: Signaling protocol attack]] exploiting [[VULNERABILITY: Legacy signaling vulnerability]] creating [[HAZARD: Train collision]] with mission impact of **railway safety system failure**. **Criticality: 0.90**. [[MITIGATION: Vital signaling logic]] and [[ARCHITECTURE: Fail-safe signaling design]] protect from [[THREAT_ACTOR: Railway saboteur]].

### Critical Item 8: LNG Terminal Control
The [[EQUIPMENT: LNG terminal control system]] with criticality **Category I-α** experiences failure mode **loading arm emergency release failure** caused by [[ATTACK_PATTERN: Safety interlock bypass]] through [[VULNERABILITY: Safety system network access]] creating [[HAZARD: LNG spill and fire]] with mission impact of **terminal catastrophic failure**. **Criticality: 0.86**. [[MITIGATION: Independent safety layers]] and [[ARCHITECTURE: Mechanical safety barriers]] defend against [[THREAT_ACTOR: Energy infrastructure attacker]].

### Critical Item 9: Chemical Reactor Batch Control
The [[EQUIPMENT: Batch reactor controller]] with criticality **Category II-α** experiences failure mode **runaway reaction** caused by [[ATTACK_PATTERN: Recipe database manipulation]] exploiting [[VULNERABILITY: Unencrypted recipe storage]] creating [[HAZARD: Reactor explosion]] with mission impact of **plant production loss**. **Criticality: 0.78**. [[MITIGATION: Recipe integrity verification]] and [[ARCHITECTURE: Reactor safety instrumented system]] prevent [[THREAT_ACTOR: Chemical plant saboteur]].

### Critical Item 10: Metro Train ATO System
The [[EQUIPMENT: Automatic train operation]] with criticality **Category I-β** experiences failure mode **ATO braking failure** caused by [[ATTACK_PATTERN: Train control message spoofing]] through [[VULNERABILITY: Radio-based train control vulnerability]] creating [[HAZARD: Station overrun]] with mission impact of **passenger injuries**. **Criticality: 0.84**. [[MITIGATION: Secure train control protocols]] and [[ARCHITECTURE: Trackside ATP backup]] protect from [[THREAT_ACTOR: Public transportation attacker]].

### Critical Item 11: Petrochemical Plant DCS
The [[EQUIPMENT: Distributed control system]] with criticality **Category II-α** experiences failure mode **process upset** caused by [[ATTACK_PATTERN: DCS controller reprogramming]] exploiting [[VULNERABILITY: Engineering workstation compromise]] creating [[HAZARD: Hazardous material release]] with mission impact of **environmental incident**. **Criticality: 0.75**. [[MITIGATION: Engineering station security]] and [[ARCHITECTURE: Change management system]] defend against [[THREAT_ACTOR: Environmental saboteur]].

### Critical Item 12: Airport Baggage Sorting
The [[EQUIPMENT: Baggage handling control]] with criticality **Category III-β** experiences failure mode **sorting system jam** caused by [[ATTACK_PATTERN: PLC logic corruption]] through [[VULNERABILITY: Unprotected PLC memory]] creating [[HAZARD: Airport operations disruption]] with mission impact of **flight delays**. **Criticality: 0.58**. [[MITIGATION: PLC memory protection]] and [[ARCHITECTURE: Manual baggage handling backup]] prevent [[THREAT_ACTOR: Airport operations disruptor]].

### Critical Item 13: Semiconductor Fab Cluster Tool
The [[EQUIPMENT: Wafer processing cluster tool]] with criticality **Category II-β** experiences failure mode **process chamber contamination** caused by [[ATTACK_PATTERN: Process recipe attack]] exploiting [[VULNERABILITY: FabWide system vulnerability]] creating [[HAZARD: Wafer scrap]] with mission impact of **production yield loss**. **Criticality: 0.72**. [[MITIGATION: Recipe authentication]] and [[ARCHITECTURE: Equipment control system isolation]] protect from [[THREAT_ACTOR: Competitive intelligence actor]].

### Critical Item 14: Data Center Cooling
The [[EQUIPMENT: CRAC control system]] with criticality **Category II-α** experiences failure mode **cooling loss** caused by [[ATTACK_PATTERN: BACnet DoS attack]] through [[VULNERABILITY: Building automation exposure]] creating [[HAZARD: Server thermal shutdown]] with mission impact of **data center outage**. **Criticality: 0.70**. [[MITIGATION: BACnet security implementation]] and [[ARCHITECTURE: Redundant cooling systems]] defend against [[THREAT_ACTOR: Data center saboteur]].

### Critical Item 15: Water Treatment SCADA
The [[EQUIPMENT: Water treatment SCADA system]] with criticality **Category II-α** experiences failure mode **disinfection control loss** caused by [[ATTACK_PATTERN: SCADA historian manipulation]] exploiting [[VULNERABILITY: Database injection vulnerability]] creating [[HAZARD: Water quality failure]] with mission impact of **public health risk**. **Criticality: 0.74**. [[MITIGATION: Database security hardening]] and [[ARCHITECTURE: Water quality monitoring redundancy]] prevent [[THREAT_ACTOR: Water infrastructure terrorist]].

### Critical Item 16: Mining Ventilation Control
The [[EQUIPMENT: Mine ventilation control]] with criticality **Category I-β** experiences failure mode **ventilation fan shutdown** caused by [[ATTACK_PATTERN: VFD parameter attack]] exploiting [[VULNERABILITY: Unsecured drive communications]] creating [[HAZARD: Toxic gas accumulation]] with mission impact of **miner safety emergency**. **Criticality: 0.82**. [[MITIGATION: Drive communication security]] and [[ARCHITECTURE: Redundant ventilation systems]] protect from [[THREAT_ACTOR: Mining saboteur]].

### Critical Item 17: Pharmaceutical Clean Room
The [[EQUIPMENT: Clean room control system]] with criticality **Category II-β** experiences failure mode **pressure differential loss** caused by [[ATTACK_PATTERN: HVAC setpoint manipulation]] through [[VULNERABILITY: BMS web interface flaw]] creating [[HAZARD: Product contamination]] with mission impact of **batch rejection and recall**. **Criticality: 0.68**. [[MITIGATION: Web interface security]] and [[ARCHITECTURE: Differential pressure monitoring]] defend against [[THREAT_ACTOR: Pharmaceutical saboteur]].

### Critical Item 18: Steel Mill Ladle Tracking
The [[EQUIPMENT: Ladle tracking system]] with criticality **Category II-α** experiences failure mode **ladle position error** caused by [[ATTACK_PATTERN: RFID spoofing]] exploiting [[VULNERABILITY: Unencrypted RFID tags]] creating [[HAZARD: Molten steel spill]] with mission impact of **worker fatalities**. **Criticality: 0.76**. [[MITIGATION: Encrypted RFID implementation]] and [[ARCHITECTURE: Optical position verification]] prevent [[THREAT_ACTOR: Steel mill saboteur]].

### Critical Item 19: Refinery Flare System
The [[EQUIPMENT: Emergency flare control]] with criticality **Category II-α** experiences failure mode **flare ignition failure** caused by [[ATTACK_PATTERN: Igniter control attack]] through [[VULNERABILITY: Unsecured ignition logic]] creating [[HAZARD: Unignited hydrocarbon release]] with mission impact of **vapor cloud explosion risk**. **Criticality: 0.71**. [[MITIGATION: Hardwired ignition backup]] and [[ARCHITECTURE: Diverse ignition sources]] protect from [[THREAT_ACTOR: Refinery safety attacker]].

### Critical Item 20: Desalination RO System
The [[EQUIPMENT: Reverse osmosis control]] with criticality **Category II-β** experiences failure mode **membrane fouling** caused by [[ATTACK_PATTERN: Chemical dosing manipulation]] exploiting [[VULNERABILITY: Dosing pump controller access]] creating [[HAZARD: Plant capacity loss]] with mission impact of **water supply shortage**. **Criticality: 0.66**. [[MITIGATION: Dosing system security]] and [[ARCHITECTURE: Water quality monitoring]] defend against [[THREAT_ACTOR: Water scarcity exploiter]].

### Critical Item 21: Wind Farm SCADA
The [[EQUIPMENT: Wind turbine SCADA]] with criticality **Category III-β** experiences failure mode **turbine shutdown** caused by [[ATTACK_PATTERN: SCADA command injection]] through [[VULNERABILITY: Weak SCADA authentication]] creating [[HAZARD: Power generation loss]] with mission impact of **revenue impact**. **Criticality: 0.54**. [[MITIGATION: Strong SCADA authentication]] and [[ARCHITECTURE: Turbine local control backup]] prevent [[THREAT_ACTOR: Renewable energy saboteur]].

### Critical Item 22: Food Processing Pasteurizer
The [[EQUIPMENT: Pasteurization control]] with criticality **Category II-α** experiences failure mode **insufficient heating** caused by [[ATTACK_PATTERN: Temperature transmitter attack]] exploiting [[VULNERABILITY: Analog signal manipulation]] creating [[HAZARD: Pathogen survival]] with mission impact of **foodborne illness outbreak**. **Criticality: 0.73**. [[MITIGATION: Signal integrity protection]] and [[ARCHITECTURE: Redundant temperature measurement]] protect from [[THREAT_ACTOR: Food terrorism actor]].

### Critical Item 23: Parking Garage Fire Alarm
The [[EQUIPMENT: Fire detection system]] with criticality **Category II-α** experiences failure mode **fire detection failure** caused by [[ATTACK_PATTERN: Fire panel manipulation]] exploiting [[VULNERABILITY: Fire system network access]] creating [[HAZARD: Delayed evacuation]] with mission impact of **occupant casualties**. **Criticality: 0.69**. [[MITIGATION: Fire system network isolation]] and [[ARCHITECTURE: Diverse detection methods]] defend against [[THREAT_ACTOR: Arson facilitator]].

### Critical Item 24: Semiconductor Cleanroom FFU
The [[EQUIPMENT: Fan filter unit control]] with criticality **Category II-β** experiences failure mode **particle contamination** caused by [[ATTACK_PATTERN: FFU controller attack]] through [[VULNERABILITY: Building automation vulnerability]] creating [[HAZARD: Wafer defects]] with mission impact of **yield loss**. **Criticality: 0.65**. [[MITIGATION: Cleanroom system isolation]] and [[ARCHITECTURE: Particle monitoring]] prevent [[THREAT_ACTOR: Fab saboteur]].

### Critical Item 25: Metro Power Rail
The [[EQUIPMENT: Traction power substation]] with criticality **Category I-β** experiences failure mode **power supply loss** caused by [[ATTACK_PATTERN: Rectifier control attack]] exploiting [[VULNERABILITY: Substation SCADA vulnerability]] creating [[HAZARD: Train stalling]] with mission impact of **passenger stranding**. **Criticality: 0.80**. [[MITIGATION: Substation security hardening]] and [[ARCHITECTURE: Multiple feeder circuits]] protect from [[THREAT_ACTOR: Transit infrastructure attacker]].

### Critical Item 26: Chemical Tank Farm Level Control
The [[EQUIPMENT: Tank level control system]] with criticality **Category II-α** experiences failure mode **tank overfill** caused by [[ATTACK_PATTERN: Level transmitter spoofing]] exploiting [[VULNERABILITY: Wireless sensor vulnerability]] creating [[HAZARD: Chemical spill]] with mission impact of **environmental release**. **Criticality: 0.77**. [[MITIGATION: Sensor authentication]] and [[ARCHITECTURE: Independent high-level alarm]] defend against [[THREAT_ACTOR: Environmental terrorist]].

### Critical Item 27: Hospital HVAC BMS
The [[EQUIPMENT: Hospital building management]] with criticality **Category II-α** experiences failure mode **negative pressure room failure** caused by [[ATTACK_PATTERN: BMS database manipulation]] through [[VULNERABILITY: SQL injection in BMS]] creating [[HAZARD: Airborne pathogen spread]] with mission impact of **hospital outbreak**. **Criticality: 0.75**. [[MITIGATION: BMS database security]] and [[ARCHITECTURE: Room pressure monitoring redundancy]] prevent [[THREAT_ACTOR: Healthcare facility attacker]].

### Critical Item 28: Port Crane Control
The [[EQUIPMENT: Ship-to-shore crane control]] with criticality **Category II-β** experiences failure mode **crane positioning error** caused by [[ATTACK_PATTERN: Crane PLC manipulation]] exploiting [[VULNERABILITY: Industrial wireless vulnerability]] creating [[HAZARD: Container drop]] with mission impact of **cargo damage and injury**. **Criticality: 0.70**. [[MITIGATION: Wireless security implementation]] and [[ARCHITECTURE: Crane safety interlocks]] protect from [[THREAT_ACTOR: Port operations saboteur]].

### Critical Item 29: Brewery Fermentation Control
The [[EQUIPMENT: Fermentation temperature control]] with criticality **Category III-β** experiences failure mode **fermentation failure** caused by [[ATTACK_PATTERN: Recipe system attack]] through [[VULNERABILITY: Unprotected recipe database]] creating [[HAZARD: Batch loss]] with mission impact of **production loss**. **Criticality: 0.52**. [[MITIGATION: Recipe system security]] and [[ARCHITECTURE: Fermentation monitoring]] defend against [[THREAT_ACTOR: Brewery competitor]].

### Critical Item 30: Smart Grid AMI
The [[EQUIPMENT: Advanced metering infrastructure]] with criticality **Category III-α** experiences failure mode **meter data corruption** caused by [[ATTACK_PATTERN: Meter firmware attack]] exploiting [[VULNERABILITY: Insecure firmware updates]] creating [[HAZARD: Billing errors]] with mission impact of **revenue loss**. **Criticality: 0.60**. [[MITIGATION: Secure meter firmware]] and [[ARCHITECTURE: Meter data validation]] prevent [[THREAT_ACTOR: Energy theft actor]].

### Critical Item 31: Data Center PDU
The [[EQUIPMENT: Power distribution unit]] with criticality **Category II-β** experiences failure mode **power circuit overload** caused by [[ATTACK_PATTERN: PDU management attack]] through [[VULNERABILITY: Weak PDU credentials]] creating [[HAZARD: Circuit breaker trip]] with mission impact of **server outage**. **Criticality: 0.67**. [[MITIGATION: PDU access control]] and [[ARCHITECTURE: Redundant power feeds]] protect from [[THREAT_ACTOR: Data center saboteur]].

### Critical Item 32: Automotive Paint Booth
The [[EQUIPMENT: Paint robot control]] with criticality **Category III-β** experiences failure mode **paint defect** caused by [[ATTACK_PATTERN: Robot program manipulation]] exploiting [[VULNERABILITY: Unsecured robot controller]] creating [[HAZARD: Quality failure]] with mission impact of **vehicle rework**. **Criticality: 0.55**. [[MITIGATION: Robot controller security]] and [[ARCHITECTURE: Quality inspection system]] defend against [[THREAT_ACTOR: Manufacturing saboteur]].

### Critical Item 33: Wastewater Lift Station
The [[EQUIPMENT: Sewage pump control]] with criticality **Category III-α** experiences failure mode **pump failure** caused by [[ATTACK_PATTERN: VFD frequency attack]] through [[VULNERABILITY: Unsecured Modbus communications]] creating [[HAZARD: Sewage backup]] with mission impact of **environmental contamination**. **Criticality: 0.62**. [[MITIGATION: Modbus security]] and [[ARCHITECTURE: Pump station redundancy]] prevent [[THREAT_ACTOR: Municipal infrastructure attacker]].

### Critical Item 34: Solar Farm Inverter
The [[EQUIPMENT: Photovoltaic inverter]] with criticality **Category III-β** experiences failure mode **grid synchronization loss** caused by [[ATTACK_PATTERN: Inverter parameter manipulation]] exploiting [[VULNERABILITY: Unencrypted inverter protocol]] creating [[HAZARD: Grid disturbance]] with mission impact of **power quality issues**. **Criticality: 0.58**. [[MITIGATION: Inverter communication security]] and [[ARCHITECTURE: Anti-islanding protection]] protect from [[THREAT_ACTOR: Grid destabilization actor]].

### Critical Item 35: Building Elevator Control
The [[EQUIPMENT: Elevator control system]] with criticality **Category II-α** experiences failure mode **elevator positioning error** caused by [[ATTACK_PATTERN: Elevator controller attack]] through [[VULNERABILITY: Building automation access]] creating [[HAZARD: Passenger entrapment]] with mission impact of **building evacuation failure**. **Criticality: 0.71**. [[MITIGATION: Elevator system isolation]] and [[ARCHITECTURE: Emergency communication system]] defend against [[THREAT_ACTOR: Building infrastructure saboteur]].

### Critical Item 36: Pulp Mill Recovery Boiler
The [[EQUIPMENT: Black liquor recovery boiler]] with criticality **Category I-α** experiences failure mode **boiler explosion** caused by [[ATTACK_PATTERN: Combustion control manipulation]] exploiting [[VULNERABILITY: DCS vulnerability]] creating [[HAZARD: Catastrophic explosion]] with mission impact of **mill destruction**. **Criticality: 0.88**. [[MITIGATION: Combustion safety system]] and [[ARCHITECTURE: Independent boiler protection]] prevent [[THREAT_ACTOR: Pulp mill saboteur]].

### Critical Item 37: Metro Platform Screen Doors
The [[EQUIPMENT: Platform door control]] with criticality **Category II-α** experiences failure mode **door operation failure** caused by [[ATTACK_PATTERN: Door controller attack]] through [[VULNERABILITY: Station control network vulnerability]] creating [[HAZARD: Passenger accident]] with mission impact of **transit safety incident**. **Criticality: 0.74**. [[MITIGATION: Door control security]] and [[ARCHITECTURE: Door safety interlocks]] protect from [[THREAT_ACTOR: Public transit saboteur]].

### Critical Item 38: Desalination Intake Control
The [[EQUIPMENT: Seawater intake control]] with criticality **Category II-β** experiences failure mode **intake blockage** caused by [[ATTACK_PATTERN: Screen control manipulation]] through [[VULNERABILITY: SCADA vulnerability]] creating [[HAZARD: Plant shutdown]] with mission impact of **water supply loss**. **Criticality: 0.68**. [[MITIGATION: SCADA hardening]] and [[ARCHITECTURE: Intake monitoring]] defend against [[THREAT_ACTOR: Water infrastructure attacker]].

### Critical Item 39: Semiconductor Gas Cabinet
The [[EQUIPMENT: Gas delivery system]] with criticality **Category I-β** experiences failure mode **toxic gas release** caused by [[ATTACK_PATTERN: Gas cabinet controller attack]] exploiting [[VULNERABILITY: Cabinet control network access]] creating [[HAZARD: Chemical exposure]] with mission impact of **fab evacuation**. **Criticality: 0.83**. [[MITIGATION: Gas system isolation]] and [[ARCHITECTURE: Gas detection redundancy]] prevent [[THREAT_ACTOR: Fab safety attacker]].

### Critical Item 40: Cement Kiln Control
The [[EQUIPMENT: Rotary kiln control system]] with criticality **Category II-α** experiences failure mode **kiln overheating** caused by [[ATTACK_PATTERN: Burner control attack]] through [[VULNERABILITY: Kiln control vulnerability]] creating [[HAZARD: Refractory failure]] with mission impact of **plant shutdown**. **Criticality: 0.72**. [[MITIGATION: Kiln control security]] and [[ARCHITECTURE: Kiln protection system]] protect from [[THREAT_ACTOR: Cement plant saboteur]].

### Critical Item 41: LNG Carrier Loading System
The [[EQUIPMENT: LNG loading arm control]] with criticality **Category I-α** experiences failure mode **emergency release failure** caused by [[ATTACK_PATTERN: ESD system attack]] exploiting [[VULNERABILITY: Safety system vulnerability]] creating [[HAZARD: LNG spill]] with mission impact of **catastrophic fire**. **Criticality: 0.89**. [[MITIGATION: Independent ESD system]] and [[ARCHITECTURE: Mechanical safety barriers]] defend against [[THREAT_ACTOR: Marine terminal terrorist]].

### Critical Item 42: Airport Fuel Hydrant System
The [[EQUIPMENT: Aircraft fueling control]] with criticality **Category II-α** experiences failure mode **fuel contamination** caused by [[ATTACK_PATTERN: Fuel system control manipulation]] through [[VULNERABILITY: Fuel management system vulnerability]] creating [[HAZARD: Aircraft fuel contamination]] with mission impact of **aviation safety incident**. **Criticality: 0.76**. [[MITIGATION: Fuel system security]] and [[ARCHITECTURE: Fuel quality monitoring]] prevent [[THREAT_ACTOR: Aviation saboteur]].

### Critical Item 43: Glass Furnace Control
The [[EQUIPMENT: Glass melting furnace]] with criticality **Category II-β** experiences failure mode **temperature excursion** caused by [[ATTACK_PATTERN: Furnace control attack]] exploiting [[VULNERABILITY: Furnace PLC vulnerability]] creating [[HAZARD: Glass quality failure]] with mission impact of **production scrap**. **Criticality: 0.70**. [[MITIGATION: Furnace control security]] and [[ARCHITECTURE: Temperature monitoring redundancy]] protect from [[THREAT_ACTOR: Glass manufacturer competitor]].

### Critical Item 44: Metro Traction Control
The [[EQUIPMENT: Train traction control]] with criticality **Category II-α** experiences failure mode **acceleration control loss** caused by [[ATTACK_PATTERN: Traction controller attack]] through [[VULNERABILITY: Train control network vulnerability]] creating [[HAZARD: Passenger injury]] with mission impact of **transit safety incident**. **Criticality: 0.75**. [[MITIGATION: Train control security]] and [[ARCHITECTURE: Traction safety system]] defend against [[THREAT_ACTOR: Rail safety saboteur]].

### Critical Item 45: Pharmaceutical Autoclave
The [[EQUIPMENT: Sterilization autoclave]] with criticality **Category II-α** experiences failure mode **sterilization failure** caused by [[ATTACK_PATTERN: Autoclave cycle manipulation]] exploiting [[VULNERABILITY: Autoclave controller vulnerability]] creating [[HAZARD: Product contamination]] with mission impact of **patient safety risk**. **Criticality: 0.73**. [[MITIGATION: Autoclave control security]] and [[ARCHITECTURE: Sterilization validation]] prevent [[THREAT_ACTOR: Pharmaceutical saboteur]].

### Critical Item 46: Hydroelectric Wicket Gate
The [[EQUIPMENT: Turbine wicket gate actuator]] with criticality **Category I-β** experiences failure mode **gate control loss** caused by [[ATTACK_PATTERN: Governor system attack]] through [[VULNERABILITY: Governor control vulnerability]] creating [[HAZARD: Turbine overspeed]] with mission impact of **generator damage**. **Criticality: 0.81**. [[MITIGATION: Governor security hardening]] and [[ARCHITECTURE: Overspeed protection]] protect from [[THREAT_ACTOR: Hydroelectric saboteur]].

### Critical Item 47: Food Processing CIP System
The [[EQUIPMENT: Clean-in-place control]] with criticality **Category II-β** experiences failure mode **cleaning failure** caused by [[ATTACK_PATTERN: CIP recipe manipulation]] exploiting [[VULNERABILITY: Recipe system vulnerability]] creating [[HAZARD: Product contamination]] with mission impact of **food safety incident**. **Criticality: 0.67**. [[MITIGATION: Recipe integrity verification]] and [[ARCHITECTURE: CIP monitoring]] defend against [[THREAT_ACTOR: Food safety saboteur]].

### Critical Item 48: Mining Hoist Control
The [[EQUIPMENT: Mine shaft hoist]] with criticality **Category I-α** experiences failure mode **hoist brake failure** caused by [[ATTACK_PATTERN: Hoist controller attack]] through [[VULNERABILITY: Hoist control network vulnerability]] creating [[HAZARD: Cage free-fall]] with mission impact of **miner fatalities**. **Criticality: 0.90**. [[MITIGATION: Hoist control security]] and [[ARCHITECTURE: Independent brake system]] prevent [[THREAT_ACTOR: Mining saboteur]].

### Critical Item 49: Port Container Scanner
The [[EQUIPMENT: X-ray container scanner]] with criticality **Category III-α** experiences failure mode **scanner data manipulation** caused by [[ATTACK_PATTERN: Scanner system hack]] exploiting [[VULNERABILITY: Scanner network vulnerability]] creating [[HAZARD: Contraband detection failure]] with mission impact of **security breach**. **Criticality: 0.63**. [[MITIGATION: Scanner system security]] and [[ARCHITECTURE: Manual inspection backup]] protect from [[THREAT_ACTOR: Smuggling facilitator]].

### Critical Item 50: District Heating Control
The [[EQUIPMENT: District heating control system]] with criticality **Category II-β** experiences failure mode **heating loss** caused by [[ATTACK_PATTERN: Heat distribution control attack]] through [[VULNERABILITY: SCADA vulnerability]] creating [[HAZARD: Service interruption]] with mission impact of **public discomfort and pipe freezing**. **Criticality: 0.69**. [[MITIGATION: SCADA security hardening]] and [[ARCHITECTURE: Distributed control redundancy]] defend against [[THREAT_ACTOR: Utility infrastructure attacker]].

---

## Criticality Summary
- **Category I (Catastrophic)**: 15 items - Immediate attention required
- **Category II (Critical)**: 30 items - High priority mitigation
- **Category III (Marginal)**: 5 items - Monitoring and improvement
- **Average Criticality**: 0.724
- **Highest Risk**: Mining hoist (0.90), Nuclear safety PLC (0.92), LNG carrier (0.89)
- **Cross-References**: 50 EQUIPMENT, 50 ATTACK_PATTERNS, 50 VULNERABILITIES, 50 HAZARDS, 50 MITIGATIONS, 50 ARCHITECTURES, 50 THREAT_ACTORS
