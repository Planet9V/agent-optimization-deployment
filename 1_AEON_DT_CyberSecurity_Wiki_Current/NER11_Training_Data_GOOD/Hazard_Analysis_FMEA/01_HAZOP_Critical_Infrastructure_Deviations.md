# HAZOP Analysis: Critical Infrastructure Deviations with Cybersecurity Context

## Overview
HAZOP (Hazard and Operability Study) is a systematic deviation-based analysis technique. This document applies HAZOP methodology to cybersecurity threats in critical infrastructure control systems.

## HAZOP Guide Words Applied to Cyber-Physical Systems
- **NO/NOT**: Complete absence of intended function
- **MORE**: Quantitative increase beyond design parameters
- **LESS**: Quantitative decrease below design parameters
- **AS WELL AS**: Additional unintended functions
- **PART OF**: Only partial achievement of intended function
- **REVERSE**: Opposite of intended operation
- **OTHER THAN**: Complete substitution of intended function

---

## Deviation Scenarios

### Scenario 1: Water Treatment Plant - Chlorine Dosing
The HAZOP deviation **MORE FLOW** in [[EQUIPMENT: Chemical dosing pump]] caused by [[ATTACK_PATTERN: Command injection]] through [[VULNERABILITY: Unauthenticated MODBUS commands]] creates [[HAZARD: Excessive chlorine discharge]] leading to public water contamination. [[MITIGATION: Rate limiting]] and [[ARCHITECTURE: DMZ isolation]] protect against [[THREAT_ACTOR: Cyber-terrorist group]].

### Scenario 2: Power Grid - Circuit Breaker Operation
The HAZOP deviation **NO FLOW** in [[EQUIPMENT: Circuit breaker]] caused by [[ATTACK_PATTERN: Denial of service]] exploiting [[VULNERABILITY: Buffer overflow in protection relay]] creates [[HAZARD: Grid cascade failure]] leading to widespread blackout. [[MITIGATION: Redundant communication paths]] and [[ARCHITECTURE: Defense-in-depth]] defend against [[THREAT_ACTOR: Nation-state APT]].

### Scenario 3: Natural Gas Pipeline - Pressure Control
The HAZOP deviation **MORE PRESSURE** in [[EQUIPMENT: Gas compressor station]] caused by [[ATTACK_PATTERN: Setpoint manipulation]] through [[VULNERABILITY: Weak authentication in HMI]] creates [[HAZARD: Pipeline rupture]] leading to explosion risk. [[MITIGATION: Integrity checking]] and [[ARCHITECTURE: Unidirectional gateway]] protect from [[THREAT_ACTOR: Hacktivist collective]].

### Scenario 4: Nuclear Reactor - Coolant System
The HAZOP deviation **LESS FLOW** in [[EQUIPMENT: Primary coolant pump]] caused by [[ATTACK_PATTERN: False data injection]] exploiting [[VULNERABILITY: Man-in-the-middle vulnerability]] creates [[HAZARD: Reactor overheating]] leading to core damage. [[MITIGATION: Cryptographic verification]] and [[ARCHITECTURE: Air-gapped safety system]] prevent attacks from [[THREAT_ACTOR: Advanced persistent threat]].

### Scenario 5: Manufacturing Plant - Robotic Assembly
The HAZOP deviation **REVERSE** in [[EQUIPMENT: Industrial robot]] caused by [[ATTACK_PATTERN: PLC ladder logic manipulation]] through [[VULNERABILITY: Default credentials]] creates [[HAZARD: Worker injury]] leading to safety incident. [[MITIGATION: Multi-factor authentication]] and [[ARCHITECTURE: Safety instrumented system]] protect against [[THREAT_ACTOR: Insider threat]].

### Scenario 6: Wastewater Treatment - Aeration System
The HAZOP deviation **NO FLOW** in [[EQUIPMENT: Blower system]] caused by [[ATTACK_PATTERN: Firmware tampering]] exploiting [[VULNERABILITY: Unsigned firmware updates]] creates [[HAZARD: Anaerobic conditions]] leading to environmental damage. [[MITIGATION: Code signing]] and [[ARCHITECTURE: Secure boot]] defend from [[THREAT_ACTOR: Eco-terrorist group]].

### Scenario 7: Petrochemical Refinery - Distillation Column
The HAZOP deviation **MORE TEMPERATURE** in [[EQUIPMENT: Distillation tower]] caused by [[ATTACK_PATTERN: Control system override]] through [[VULNERABILITY: SQL injection in historian database]] creates [[HAZARD: Thermal runaway]] leading to explosion. [[MITIGATION: Input validation]] and [[ARCHITECTURE: Network segmentation]] prevent [[THREAT_ACTOR: Ransomware operator]].

### Scenario 8: Electric Substation - Voltage Regulation
The HAZOP deviation **MORE VOLTAGE** in [[EQUIPMENT: Voltage regulator]] caused by [[ATTACK_PATTERN: IEC 61850 GOOSE message spoofing]] exploiting [[VULNERABILITY: Unauthenticated multicast messages]] creates [[HAZARD: Equipment damage]] leading to grid instability. [[MITIGATION: Message authentication]] and [[ARCHITECTURE: VLAN isolation]] protect against [[THREAT_ACTOR: Script kiddie]].

### Scenario 9: Water Distribution - Pump Station
The HAZOP deviation **AS WELL AS** in [[EQUIPMENT: Water pump]] caused by [[ATTACK_PATTERN: Ladder logic injection]] through [[VULNERABILITY: Exposed PLC programming port]] creates [[HAZARD: Simultaneous conflicting operations]] leading to system failure. [[MITIGATION: Port security]] and [[ARCHITECTURE: Jump server access control]] defend from [[THREAT_ACTOR: Disgruntled contractor]].

### Scenario 10: Oil Pipeline - Flow Control Valve
The HAZOP deviation **PART OF** in [[EQUIPMENT: Motorized valve]] caused by [[ATTACK_PATTERN: DNP3 protocol manipulation]] exploiting [[VULNERABILITY: Cleartext SCADA communications]] creates [[HAZARD: Partial valve operation]] leading to pressure surge. [[MITIGATION: Protocol encryption]] and [[ARCHITECTURE: IDS deployment]] prevent [[THREAT_ACTOR: Organized crime]].

### Scenario 11: Smart Grid - Demand Response
The HAZOP deviation **OTHER THAN** in [[EQUIPMENT: Smart meter]] caused by [[ATTACK_PATTERN: Firmware replacement]] through [[VULNERABILITY: Remote code execution]] creates [[HAZARD: False demand signals]] leading to grid destabilization. [[MITIGATION: Secure firmware updates]] and [[ARCHITECTURE: Zero trust architecture]] protect from [[THREAT_ACTOR: State-sponsored actor]].

### Scenario 12: Chemical Plant - Batch Reactor
The HAZOP deviation **MORE FLOW** in [[EQUIPMENT: Reactor feed pump]] caused by [[ATTACK_PATTERN: Memory corruption exploit]] exploiting [[VULNERABILITY: Stack overflow in RTU]] creates [[HAZARD: Overpressure condition]] leading to vessel failure. [[MITIGATION: Memory protection]] and [[ARCHITECTURE: Safety PLC isolation]] defend against [[THREAT_ACTOR: Competitor sabotage]].

### Scenario 13: Metro Rail System - Train Control
The HAZOP deviation **REVERSE** in [[EQUIPMENT: Rail switch motor]] caused by [[ATTACK_PATTERN: Wireless protocol attack]] through [[VULNERABILITY: Unencrypted radio commands]] creates [[HAZARD: Train derailment]] leading to casualties. [[MITIGATION: Encrypted communications]] and [[ARCHITECTURE: Physical safety interlocks]] prevent [[THREAT_ACTOR: Terrorist organization]].

### Scenario 14: Data Center - Cooling System
The HAZOP deviation **LESS FLOW** in [[EQUIPMENT: CRAC unit]] caused by [[ATTACK_PATTERN: BACnet exploitation]] exploiting [[VULNERABILITY: Open building automation protocol]] creates [[HAZARD: Server overheating]] leading to data loss. [[MITIGATION: BACnet security extensions]] and [[ARCHITECTURE: Facility management network isolation]] protect from [[THREAT_ACTOR: Cyber-extortionist]].

### Scenario 15: Steel Mill - Blast Furnace
The HAZOP deviation **MORE TEMPERATURE** in [[EQUIPMENT: Blast furnace]] caused by [[ATTACK_PATTERN: HMI session hijacking]] through [[VULNERABILITY: Session fixation flaw]] creates [[HAZARD: Furnace damage]] leading to production halt. [[MITIGATION: Session management controls]] and [[ARCHITECTURE: Operator workstation hardening]] defend from [[THREAT_ACTOR: Industrial espionage]].

### Scenario 16: Hospital - Medical Gas System
The HAZOP deviation **NO PRESSURE** in [[EQUIPMENT: Oxygen supply system]] caused by [[ATTACK_PATTERN: Building automation system attack]] exploiting [[VULNERABILITY: Default SNMP community strings]] creates [[HAZARD: Patient oxygen deprivation]] leading to medical emergency. [[MITIGATION: SNMPv3 implementation]] and [[ARCHITECTURE: Medical network segmentation]] prevent [[THREAT_ACTOR: Healthcare targeting group]].

### Scenario 17: Airport - Baggage Handling
The HAZOP deviation **REVERSE** in [[EQUIPMENT: Conveyor belt system]] caused by [[ATTACK_PATTERN: EtherNet/IP exploit]] through [[VULNERABILITY: Unpatched CIP vulnerability]] creates [[HAZARD: Baggage misrouting]] leading to operational chaos. [[MITIGATION: Patch management]] and [[ARCHITECTURE: Industrial firewall]] protect against [[THREAT_ACTOR: Hacktivist]].

### Scenario 18: Pharmaceutical Plant - Clean Room
The HAZOP deviation **LESS PRESSURE** in [[EQUIPMENT: HVAC system]] caused by [[ATTACK_PATTERN: BMS protocol fuzzing]] exploiting [[VULNERABILITY: Parsing vulnerabilities]] creates [[HAZARD: Contamination risk]] leading to product recall. [[MITIGATION: Protocol validation]] and [[ARCHITECTURE: Building system isolation]] defend from [[THREAT_ACTOR: Regulatory saboteur]].

### Scenario 19: Mining Operation - Ventilation System
The HAZOP deviation **NO FLOW** in [[EQUIPMENT: Mine ventilation fan]] caused by [[ATTACK_PATTERN: Profinet DCP spoofing]] through [[VULNERABILITY: Unauthenticated network configuration]] creates [[HAZARD: Toxic gas accumulation]] leading to worker fatalities. [[MITIGATION: Network admission control]] and [[ARCHITECTURE: Safety-critical network separation]] prevent [[THREAT_ACTOR: Labor dispute activist]].

### Scenario 20: Food Processing - Pasteurization
The HAZOP deviation **LESS TEMPERATURE** in [[EQUIPMENT: Pasteurization unit]] caused by [[ATTACK_PATTERN: Temperature sensor spoofing]] exploiting [[VULNERABILITY: Analog signal interference]] creates [[HAZARD: Pathogen survival]] leading to foodborne illness. [[MITIGATION: Signal integrity monitoring]] and [[ARCHITECTURE: Sensor network protection]] protect from [[THREAT_ACTOR: Food terrorism]].

### Scenario 21: Telecommunications - Cell Tower
The HAZOP deviation **MORE POWER** in [[EQUIPMENT: RF amplifier]] caused by [[ATTACK_PATTERN: Remote management exploit]] through [[VULNERABILITY: Weak SSL implementation]] creates [[HAZARD: RF interference]] leading to communication disruption. [[MITIGATION: Strong cryptography]] and [[ARCHITECTURE: Management VLAN isolation]] defend against [[THREAT_ACTOR: Communication disruptor]].

### Scenario 22: Automotive Factory - Paint Booth
The HAZOP deviation **AS WELL AS** in [[EQUIPMENT: Paint robot]] caused by [[ATTACK_PATTERN: EtherCAT frame injection]] exploiting [[VULNERABILITY: Broadcast storm vulnerability]] creates [[HAZARD: Coating defects]] leading to quality failure. [[MITIGATION: Network traffic filtering]] and [[ARCHITECTURE: Motion control network isolation]] prevent [[THREAT_ACTOR: Corporate espionage]].

### Scenario 23: Desalination Plant - Reverse Osmosis
The HAZOP deviation **MORE PRESSURE** in [[EQUIPMENT: RO membrane unit]] caused by [[ATTACK_PATTERN: Process control override]] through [[VULNERABILITY: Hardcoded credentials]] creates [[HAZARD: Membrane rupture]] leading to plant shutdown. [[MITIGATION: Credential management]] and [[ARCHITECTURE: Process safety system independence]] protect from [[THREAT_ACTOR: Water scarcity exploiter]].

### Scenario 24: Semiconductor Fab - Lithography Tool
The HAZOP deviation **PART OF** in [[EQUIPMENT: Stepper motor controller]] caused by [[ATTACK_PATTERN: SEMI SECS/GEM manipulation]] exploiting [[VULNERABILITY: Protocol implementation flaw]] creates [[HAZARD: Wafer misalignment]] leading to production loss. [[MITIGATION: Protocol conformance testing]] and [[ARCHITECTURE: Fab network microsegmentation]] defend from [[THREAT_ACTOR: Technology theft actor]].

### Scenario 25: Brewery - Fermentation Tank
The HAZOP deviation **MORE TEMPERATURE** in [[EQUIPMENT: Fermentation vessel]] caused by [[ATTACK_PATTERN: Temperature controller reprogramming]] through [[VULNERABILITY: Telnet access enabled]] creates [[HAZARD: Fermentation failure]] leading to batch loss. [[MITIGATION: Secure remote access]] and [[ARCHITECTURE: Recipe management system protection]] prevent [[THREAT_ACTOR: Business competitor]].

### Scenario 26: Wind Farm - Turbine Control
The HAZOP deviation **REVERSE** in [[EQUIPMENT: Blade pitch mechanism]] caused by [[ATTACK_PATTERN: IEC 61400-25 exploitation]] exploiting [[VULNERABILITY: Insufficient input validation]] creates [[HAZARD: Turbine overspeed]] leading to structural failure. [[MITIGATION: Control logic verification]] and [[ARCHITECTURE: Wind farm SCADA hardening]] protect against [[THREAT_ACTOR: Energy market manipulator]].

### Scenario 27: Parking Garage - Access Control
The HAZOP deviation **NO FLOW** in [[EQUIPMENT: Entry gate barrier]] caused by [[ATTACK_PATTERN: Access control system hack]] through [[VULNERABILITY: Cloud API vulnerability]] creates [[HAZARD: Traffic congestion]] leading to emergency access blockage. [[MITIGATION: API security]] and [[ARCHITECTURE: Local override capability]] defend from [[THREAT_ACTOR: Urban infrastructure attacker]].

### Scenario 28: Pulp and Paper Mill - Pulp Digester
The HAZOP deviation **MORE PRESSURE** in [[EQUIPMENT: Pulp digester]] caused by [[ATTACK_PATTERN: Relief valve disable command]] exploiting [[VULNERABILITY: Unsecured safety override]] creates [[HAZARD: Digester explosion]] leading to catastrophic failure. [[MITIGATION: Safety system independence]] and [[ARCHITECTURE: Hardwired safety interlocks]] prevent [[THREAT_ACTOR: Environmental extremist]].

### Scenario 29: Smart Building - HVAC Optimization
The HAZOP deviation **OTHER THAN** in [[EQUIPMENT: VAV controller]] caused by [[ATTACK_PATTERN: BACnet/IP packet injection]] through [[VULNERABILITY: Unrestricted network access]] creates [[HAZARD: Indoor air quality issues]] leading to occupant illness. [[MITIGATION: Network access control]] and [[ARCHITECTURE: Building management system segmentation]] protect from [[THREAT_ACTOR: Disgruntled tenant]].

### Scenario 30: Solar Farm - Inverter System
The HAZOP deviation **MORE VOLTAGE** in [[EQUIPMENT: Grid-tie inverter]] caused by [[ATTACK_PATTERN: SunSpec Modbus manipulation]] exploiting [[VULNERABILITY: Unencrypted monitoring protocol]] creates [[HAZARD: Grid overvoltage]] leading to equipment damage. [[MITIGATION: Protocol security]] and [[ARCHITECTURE: Inverter network isolation]] defend against [[THREAT_ACTOR: Grid destabilization actor]].

### Scenario 31: Port Terminal - Crane Operation
The HAZOP deviation **REVERSE** in [[EQUIPMENT: Gantry crane]] caused by [[ATTACK_PATTERN: Wireless controller spoofing]] exploiting [[VULNERABILITY: Radio frequency jamming susceptibility]] creates [[HAZARD: Container drop]] leading to cargo damage. [[MITIGATION: Frequency hopping]] and [[ARCHITECTURE: Safety positioning system]] prevent [[THREAT_ACTOR: Port saboteur]].

### Scenario 32: Cement Plant - Kiln Control
The HAZOP deviation **MORE TEMPERATURE** in [[EQUIPMENT: Rotary kiln]] caused by [[ATTACK_PATTERN: Burner control manipulation]] through [[VULNERABILITY: Legacy protocol vulnerability]] creates [[HAZARD: Refractory damage]] leading to production halt. [[MITIGATION: Protocol gateway]] and [[ARCHITECTURE: Legacy system isolation]] protect from [[THREAT_ACTOR: Industrial sabotage]].

### Scenario 33: Metro - Platform Screen Doors
The HAZOP deviation **NO FLOW** in [[EQUIPMENT: Platform door mechanism]] caused by [[ATTACK_PATTERN: Door control system attack]] exploiting [[VULNERABILITY: Unpatched PLC firmware]] creates [[HAZARD: Passenger trap]] leading to emergency evacuation. [[MITIGATION: Firmware management]] and [[ARCHITECTURE: Emergency override system]] defend against [[THREAT_ACTOR: Public transport disruptor]].

### Scenario 34: LNG Terminal - Liquefaction Process
The HAZOP deviation **LESS TEMPERATURE** in [[EQUIPMENT: Cold box]] caused by [[ATTACK_PATTERN: Refrigeration cycle manipulation]] through [[VULNERABILITY: Control network intrusion]] creates [[HAZARD: Incomplete liquefaction]] leading to safety relief activation. [[MITIGATION: Network intrusion detection]] and [[ARCHITECTURE: Process safety layer]] prevent [[THREAT_ACTOR: Energy infrastructure attacker]].

### Scenario 35: Glass Manufacturing - Float Glass Line
The HAZOP deviation **MORE FLOW** in [[EQUIPMENT: Molten tin bath]] caused by [[ATTACK_PATTERN: Temperature profile attack]] exploiting [[VULNERABILITY: Historian database compromise]] creates [[HAZARD: Glass quality defect]] leading to production scrap. [[MITIGATION: Database security]] and [[ARCHITECTURE: Production control isolation]] protect from [[THREAT_ACTOR: Manufacturing competitor]].

### Scenario 36: Hydroelectric Dam - Turbine Governor
The HAZOP deviation **PART OF** in [[EQUIPMENT: Wicket gate controller]] caused by [[ATTACK_PATTERN: Governor setpoint manipulation]] through [[VULNERABILITY: DNP3 secure authentication bypass]] creates [[HAZARD: Frequency instability]] leading to grid disturbance. [[MITIGATION: Secure DNP3 implementation]] and [[ARCHITECTURE: Governor control hardening]] defend from [[THREAT_ACTOR: Critical infrastructure threat]].

### Scenario 37: Automotive Assembly - Welding Robot
The HAZOP deviation **AS WELL AS** in [[EQUIPMENT: Welding robot]] caused by [[ATTACK_PATTERN: Motion program injection]] exploiting [[VULNERABILITY: Unsecured robot teach pendant]] creates [[HAZARD: Incorrect weld pattern]] leading to vehicle safety defect. [[MITIGATION: Program verification]] and [[ARCHITECTURE: Robot cell isolation]] prevent [[THREAT_ACTOR: Quality saboteur]].

### Scenario 38: Chemical Storage - Tank Farm
The HAZOP deviation **MORE LEVEL** in [[EQUIPMENT: Chemical storage tank]] caused by [[ATTACK_PATTERN: Level transmitter spoofing]] through [[VULNERABILITY: 4-20mA signal injection]] creates [[HAZARD: Tank overflow]] leading to environmental release. [[MITIGATION: Signal encryption]] and [[ARCHITECTURE: Overfill protection independence]] protect from [[THREAT_ACTOR: Environmental terrorist]].

### Scenario 39: Brewery - Bottling Line
The HAZOP deviation **LESS PRESSURE** in [[EQUIPMENT: CO2 carbonation system]] caused by [[ATTACK_PATTERN: Recipe database tampering]] exploiting [[VULNERABILITY: Unencrypted database connection]] creates [[HAZARD: Product quality failure]] leading to customer complaints. [[MITIGATION: Database encryption]] and [[ARCHITECTURE: Recipe management protection]] defend against [[THREAT_ACTOR: Brand reputation attacker]].

### Scenario 40: Airport - Runway Lighting
The HAZOP deviation **NO FLOW** in [[EQUIPMENT: Airfield lighting system]] caused by [[ATTACK_PATTERN: Lighting control protocol attack]] through [[VULNERABILITY: Obsolete control protocol]] creates [[HAZARD: Landing guidance loss]] leading to aircraft incident. [[MITIGATION: Protocol modernization]] and [[ARCHITECTURE: Lighting system redundancy]] prevent [[THREAT_ACTOR: Aviation infrastructure threat]].

### Scenario 41: Pharmaceutical - Lyophilization
The HAZOP deviation **MORE PRESSURE** in [[EQUIPMENT: Freeze dryer chamber]] caused by [[ATTACK_PATTERN: Vacuum system override]] exploiting [[VULNERABILITY: Supervisory control bypass]] creates [[HAZARD: Product degradation]] leading to drug efficacy loss. [[MITIGATION: Override protection]] and [[ARCHITECTURE: Quality system integration]] protect from [[THREAT_ACTOR: Drug counterfeiting group]].

### Scenario 42: Metro Rail - Traction Power
The HAZOP deviation **REVERSE** in [[EQUIPMENT: Rectifier substation]] caused by [[ATTACK_PATTERN: SCADA command injection]] through [[VULNERABILITY: Weak SCADA authentication]] creates [[HAZARD: Regenerative braking failure]] leading to train collision risk. [[MITIGATION: Strong authentication]] and [[ARCHITECTURE: Traction power system isolation]] defend against [[THREAT_ACTOR: Mass transit saboteur]].

### Scenario 43: Wastewater - Sludge Digester
The HAZOP deviation **MORE TEMPERATURE** in [[EQUIPMENT: Anaerobic digester]] caused by [[ATTACK_PATTERN: Temperature control manipulation]] through [[VULNERABILITY: Exposed control interface]] creates [[HAZARD: Methane over-production]] leading to explosion risk. [[MITIGATION: Interface access control]] and [[ARCHITECTURE: Digester safety system]] prevent [[THREAT_ACTOR: Municipal infrastructure attacker]].

### Scenario 44: Steel Rolling Mill - Rolling Stand
The HAZOP deviation **MORE SPEED** in [[EQUIPMENT: Rolling mill drive]] caused by [[ATTACK_PATTERN: Variable frequency drive hack]] exploiting [[VULNERABILITY: Drive parameter access]] creates [[HAZARD: Steel slab damage]] leading to equipment failure. [[MITIGATION: Drive security hardening]] and [[ARCHITECTURE: Drive network segmentation]] protect from [[THREAT_ACTOR: Production saboteur]].

### Scenario 45: Smart Grid - Phasor Measurement
The HAZOP deviation **OTHER THAN** in [[EQUIPMENT: PMU device]] caused by [[ATTACK_PATTERN: IEEE C37.118 data corruption]] through [[VULNERABILITY: Synchrophasor protocol vulnerability]] creates [[HAZARD: False grid state estimation]] leading to control decisions error. [[MITIGATION: Data integrity verification]] and [[ARCHITECTURE: PMU network security]] defend against [[THREAT_ACTOR: Grid stability attacker]].

### Scenario 46: Mining - Conveyor System
The HAZOP deviation **REVERSE** in [[EQUIPMENT: Ore conveyor belt]] caused by [[ATTACK_PATTERN: Motion controller reprogramming]] exploiting [[VULNERABILITY: Remote access trojan]] creates [[HAZARD: Material spillage]] leading to production halt. [[MITIGATION: Antimalware protection]] and [[ARCHITECTURE: Conveyor control isolation]] prevent [[THREAT_ACTOR: Mining operation disruptor]].

### Scenario 47: Food Processing - Blast Freezer
The HAZOP deviation **LESS TEMPERATURE** in [[EQUIPMENT: Blast freezer]] caused by [[ATTACK_PATTERN: Refrigeration control attack]] through [[VULNERABILITY: Unencrypted control protocol]] creates [[HAZARD: Food spoilage]] leading to health risk. [[MITIGATION: Protocol encryption]] and [[ARCHITECTURE: Temperature monitoring independence]] protect from [[THREAT_ACTOR: Food safety attacker]].

### Scenario 48: Building Automation - Fire Suppression
The HAZOP deviation **NO FLOW** in [[EQUIPMENT: Sprinkler system valve]] caused by [[ATTACK_PATTERN: Fire alarm panel hack]] exploiting [[VULNERABILITY: BACnet vulnerability]] creates [[HAZARD: Fire suppression failure]] leading to uncontrolled fire. [[MITIGATION: Fire system hardening]] and [[ARCHITECTURE: Life safety system independence]] defend against [[THREAT_ACTOR: Arson facilitator]].

### Scenario 49: Pulp Mill - Chemical Recovery
The HAZOP deviation **MORE FLOW** in [[EQUIPMENT: Black liquor pump]] caused by [[ATTACK_PATTERN: DCS manipulation]] through [[VULNERABILITY: Engineering workstation compromise]] creates [[HAZARD: Recovery boiler upset]] leading to explosion hazard. [[MITIGATION: Workstation security]] and [[ARCHITECTURE: DCS network protection]] prevent [[THREAT_ACTOR: Industrial sabotage group]].

### Scenario 50: Electric Vehicle Charging - Fast Charger
The HAZOP deviation **MORE VOLTAGE** in [[EQUIPMENT: DC fast charger]] caused by [[ATTACK_PATTERN: OCPP protocol manipulation]] through [[VULNERABILITY: Charging protocol vulnerability]] creates [[HAZARD: Vehicle battery damage]] leading to fire risk. [[MITIGATION: Protocol validation]] and [[ARCHITECTURE: Charger network security]] protect from [[THREAT_ACTOR: EV infrastructure attacker]].

---

## Cross-Reference Summary
- **EQUIPMENT**: 50 unique critical infrastructure components
- **ATTACK_PATTERN**: 48 distinct cyber-attack methods
- **VULNERABILITY**: 50 specific security weaknesses
- **HAZARD**: 50 safety consequences
- **MITIGATION**: 50 protective measures
- **ARCHITECTURE**: 50 defense architectures
- **THREAT_ACTOR**: 50 adversary profiles

## HAZOP Methodology Notes
- Systematic examination using guide words (NO, MORE, LESS, REVERSE, etc.)
- Each deviation analyzed for cause, consequence, safeguards, and recommendations
- Cybersecurity threats integrated as deviation causes
- Safety consequences linked to security vulnerabilities
- Multi-layered defense strategies identified
